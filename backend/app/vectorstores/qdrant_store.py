import math
import re

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config.settings import settings
from app.embeddings.embedding_factory import EmbeddingFactory
from app.utils.logger import logger
from app.vectorstores.base_vectorstore import BaseVectorStore


class QdrantStore(BaseVectorStore):

    # Standard retrieval should prefer the highest-ranked policy chunks.
    # A small penalty still avoids exact-near-duplicate results without
    # displacing relevant chunks merely because they share policy vocabulary.
    STANDARD_DIVERSITY_WEIGHT = 0.05

    STOP_WORDS = {
        "a", "an", "the",
        "is", "are", "was", "were",
        "be", "been", "being",
        "can", "could", "may", "might",
        "shall", "should", "would",
        "do", "does", "did",
        "how", "what", "when", "where",
        "who", "which", "why",
        "many", "much",
        "me", "my", "i", "we", "you", "your",
        "in", "on", "at", "to", "of",
        "for", "from", "with",
        "and", "or", "as", "by", "per",
        "this", "that", "these", "those",
    }

    NUMERIC_QUESTION_TERMS = (
        "how many",
        "how much",
        "number",
        "amount",
        "limit",
        "maximum",
        "minimum",
        "rate",
        "percentage",
        "percent",
        "cost",
        "price",
        "duration",
        "days",
        "day",
        "hours",
        "hour",
        "weeks",
        "week",
        "months",
        "month",
        "years",
        "year",
        "per",
    )

    QUESTION_SIGNALS = {
        "numeric": (
            "how many",
            "how much",
            "what is the",
            "what are the",
            "maximum",
            "minimum",
            "limit",
            "amount",
            "rate",
        ),
        "date": (
            "when",
            "date",
            "deadline",
            "how long",
        ),
        "requirement": (
            "requirement",
            "requirements",
            "eligible",
            "eligibility",
            "required",
        ),
    }

    STRUCTURAL_MARKERS = (
        "table of contents",
        "table of content",
        "list of figures",
        "list of tables",
        "index of",
    )

    SUMMARY_TERMS = (
        "overview",
        "introduction",
        "purpose",
        "about",
        "key points",
        "summary",
        "architecture",
        "workflow",
        "pipeline",
        "important",
        "main",
        "core",
        "objective",
        "objectives",
        "scope",
    )

    def __init__(self):
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.db_path = settings.QDRANT_DB_PATH

        self.embedding = (
            EmbeddingFactory
            .get_embedder()
            .embedding_model
        )

        self.client = QdrantClient(
            path=self.db_path
        )

        self._initialize_collection()

    # ============================================================
    # QDRANT
    # ============================================================

    def _collection_config(self):
        return VectorParams(
            size=768,
            distance=Distance.COSINE,
        )

    def _initialize_collection(self):
        try:
            self.client.get_collection(
                self.collection_name
            )
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=self._collection_config(),
            )

        self._initialize_vector_store()

    def _initialize_vector_store(self):
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )

    # ============================================================
    # DOCUMENTS
    # ============================================================

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    # ============================================================
    # TEXT
    # ============================================================

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def _normalize_token(cls, token: str) -> str:
        """
        Normalize a token for lightweight lexical matching.

        Keep normalization document-agnostic. Semantic relationships
        such as singular/plural or verb forms are handled primarily by
        the embedding model rather than hardcoded stemming rules.
        """
        return token.lower().strip()

    @classmethod
    def _tokens(cls, text: str) -> set[str]:
        return {
            cls._normalize_token(token)
            for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
            if len(token) > 1
        }

    @classmethod
    def _content_tokens(cls, text: str) -> set[str]:
        return (
            cls._tokens(text)
            - cls.STOP_WORDS
        )

    # ============================================================
    # RETRIEVAL SCORING
    # ============================================================

    @classmethod
    def _lexical_overlap(
        cls,
        query: str,
        document_text: str,
    ) -> float:

        query_tokens = cls._content_tokens(query)
        document_tokens = cls._tokens(document_text)

        if not query_tokens:
            return 0.0

        return (
            len(
                query_tokens & document_tokens
            )
            / len(query_tokens)
        )

    @classmethod
    def _important_term_score(
        cls,
        query: str,
        document_text: str,
    ) -> float:

        query_tokens = cls._content_tokens(query)
        document_tokens = cls._tokens(document_text)

        if not query_tokens:
            return 0.0

        total_weight = 0.0
        matched_weight = 0.0

        for token in query_tokens:
            weight = min(
                3.0,
                max(
                    1.0,
                    len(token) / 4.0,
                ),
            )

            total_weight += weight

            if token in document_tokens:
                matched_weight += weight

        return (
            matched_weight / total_weight
            if total_weight
            else 0.0
        )

    @classmethod
    def _phrase_score(
        cls,
        query: str,
        document_text: str,
    ) -> float:

        query_words = [
            word
            for word in cls._normalize_text(query).split()
            if word not in cls.STOP_WORDS
        ]

        if len(query_words) < 2:
            return 0.0

        document_text = cls._normalize_text(
            document_text
        )

        phrases = []

        for size in (4, 3, 2):
            if len(query_words) < size:
                continue

            for index in range(
                len(query_words) - size + 1
            ):
                phrases.append(
                    " ".join(
                        query_words[
                            index:index + size
                        ]
                    )
                )

        if not phrases:
            return 0.0

        matched_weight = 0.0
        total_weight = 0.0

        for phrase in phrases:
            weight = float(
                len(phrase.split()) ** 2
            )

            total_weight += weight

            if phrase in document_text:
                matched_weight += weight

        if not total_weight:
            return 0.0

        return min(
            1.0,
            matched_weight / total_weight,
        )

    @staticmethod
    def _numeric_relevance(
        query: str,
        document_text: str,
    ) -> float:

        query_lower = query.lower()

        if not any(
            term in query_lower
            for term in QdrantStore.NUMERIC_QUESTION_TERMS
        ):
            return 0.0

        patterns = (
            r"\b\d+(?:\.\d+)?\b",
            r"\b\d+(?:\.\d+)?\s*%",
            (
                r"\b\d+(?:\.\d+)?\s*"
                r"(?:day|days|week|weeks|month|months|"
                r"year|years|hour|hours)\b"
            ),
        )

        matches = sum(
            len(
                re.findall(
                    pattern,
                    document_text.lower(),
                )
            )
            for pattern in patterns
        )

        if not matches:
            return 0.0

        return min(
            1.0,
            math.log1p(matches) / math.log(11),
        )

    @classmethod
    def _section_title_score(
        cls,
        query: str,
        document,
    ) -> float:

        section_title = (
            document.metadata.get(
                "section_title",
                "",
            )
            or ""
        )

        if not section_title:
            return 0.0

        query_tokens = cls._content_tokens(query)

        section_tokens = cls._content_tokens(
            section_title
        )

        if not query_tokens or not section_tokens:
            return 0.0

        overlap = (
            query_tokens & section_tokens
        )

        token_score = (
            len(overlap) / len(query_tokens)
        )

        phrase_score = cls._phrase_score(
            query,
            section_title,
        )

        return min(
            1.0,
            0.65 * token_score
            + 0.35 * phrase_score,
        )

    @staticmethod
    def _question_signal_score(
        query: str,
        document_text: str,
    ) -> float:

        query_lower = query.lower()
        document_lower = document_text.lower()

        signals = []

        if any(
            phrase in query_lower
            for phrase in QdrantStore.QUESTION_SIGNALS[
                "numeric"
            ]
        ):
            if any(
                word in document_lower
                for word in (
                    "limit",
                    "maximum",
                    "minimum",
                    "per year",
                    "per month",
                    "per day",
                    "amount",
                    "rate",
                    "entitled",
                    "entitlement",
                )
            ):
                signals.append(1.0)

        if any(
            phrase in query_lower
            for phrase in QdrantStore.QUESTION_SIGNALS[
                "date"
            ]
        ):
            if any(
                word in document_lower
                for word in (
                    "date",
                    "deadline",
                    "within",
                    "days",
                    "weeks",
                    "months",
                    "years",
                )
            ):
                signals.append(1.0)

        if any(
            phrase in query_lower
            for phrase in QdrantStore.QUESTION_SIGNALS[
                "requirement"
            ]
        ):
            if any(
                word in document_lower
                for word in (
                    "required",
                    "requirement",
                    "eligible",
                    "eligibility",
                    "must",
                    "shall",
                )
            ):
                signals.append(1.0)

        return (
            sum(signals) / len(signals)
            if signals
            else 0.0
        )

    @classmethod
    def _rerank_score(
        cls,
        query: str,
        document,
        semantic_score: float,
    ) -> float:

        text = document.page_content

        scores = {
            "lexical": cls._lexical_overlap(
                query,
                text,
            ),
            "important": cls._important_term_score(
                query,
                text,
            ),
            "phrase": cls._phrase_score(
                query,
                text,
            ),
            "numeric": cls._numeric_relevance(
                query,
                text,
            ),
            "question": cls._question_signal_score(
                query,
                text,
            ),
            "section": cls._section_title_score(
                query,
                document,
            ),
        }

        return (
            0.60 * semantic_score
            + 0.12 * scores["lexical"]
            + 0.10 * scores["important"]
            + 0.08 * scores["phrase"]
            + 0.04 * scores["section"]
            + 0.03 * scores["numeric"]
            + 0.03 * scores["question"]
        )

    # ============================================================
    # STRUCTURAL NOISE
    # ============================================================

    @classmethod
    def _is_structural_noise(cls, document) -> bool:
        """
        Detect chunks that are primarily structural/table noise.

        Important:
        - Numeric-heavy policy content is NOT automatically noise.
        - A chunk is considered noise only when there is stronger evidence
          that the numbers are structural rather than meaningful content.
        """

        text = cls._normalize_text(
            document.page_content
        )

        if not text:
            return True

        # Explicit structural markers remain strong evidence.
        if any(
            marker in text
            for marker in cls.STRUCTURAL_MARKERS
        ):
            return True

        words = text.split()

        if len(words) < 25:
            return False

        numbers = re.findall(
            r"\b\d{1,3}\b",
            text,
        )

        if len(numbers) < 8:
            return False

        numeric_ratio = len(numbers) / len(words)

        # Numeric-heavy text is not necessarily noise.
        # Policy rules, limits, dates, timings, categories, etc.
        # can legitimately contain many numbers.
        if numeric_ratio < 0.10:
            return False

        # Check whether the chunk contains meaningful prose.
        sentence_like = re.split(
            r"[.!?]\s+",
            text,
        )

        meaningful_sentences = [
            sentence
            for sentence in sentence_like
            if len(sentence.split()) >= 6
        ]

        # If the chunk contains multiple meaningful sentences,
        # treat it as legitimate content rather than structural noise.
        if len(meaningful_sentences) >= 2:
            return False

        # Stronger indication of structural/table debris:
        # lots of numbers + very little natural language.
        alpha_chars = sum(
            character.isalpha()
            for character in text
        )

        non_space_chars = sum(
            not character.isspace()
            for character in text
        )

        alpha_ratio = (
            alpha_chars / non_space_chars
            if non_space_chars
            else 0
        )

        if alpha_ratio < 0.55:
            return True

        return False

    # ============================================================
    # DEDUPLICATION
    # ============================================================

    @classmethod
    def _deduplicate(cls, results):
        unique = []
        seen = set()

        for item in results:
            document = item["document"]

            content = cls._normalize_text(
                document.page_content
            )

            if not content or content in seen:
                continue

            seen.add(content)
            unique.append(item)

        return unique

    # ============================================================
    # DIVERSITY
    # ============================================================

    @classmethod
    def _max_text_similarity(
        cls,
        document,
        selected_documents,
    ) -> float:

        if not selected_documents:
            return 0.0

        current_tokens = cls._tokens(
            document.page_content
        )

        if not current_tokens:
            return 0.0

        maximum = 0.0

        for selected in selected_documents:
            selected_tokens = cls._tokens(
                selected.page_content
            )

            if not selected_tokens:
                continue

            union = (
                current_tokens | selected_tokens
            )

            if not union:
                continue

            similarity = len(
                current_tokens & selected_tokens
            ) / len(union)

            maximum = max(
                maximum,
                similarity,
            )

        return maximum


    @classmethod
    def _select_diverse_results(
        cls,
        candidates,
        k: int,
        diversity_weight: float = 0.20,
    ):

        if not candidates:
            return []

        selected = [candidates[0]]
        remaining = list(candidates[1:])

        while (
            remaining
            and len(selected) < k
        ):

            best_index = 0
            best_score = float("-inf")

            selected_documents = [
                item["document"]
                for item in selected
            ]

            for index, candidate in enumerate(
                remaining
            ):

                relevance = candidate["final_score"]

                redundancy = cls._max_text_similarity(
                    candidate["document"],
                    selected_documents,
                )

                score = (
                    (1.0 - diversity_weight)
                    * relevance
                    - diversity_weight
                    * redundancy
                )

                if score > best_score:
                    best_score = score
                    best_index = index

            selected.append(
                remaining.pop(best_index)
            )

        return selected

    @classmethod
    def _debug_diversity_selection(
        cls,
        candidates,
        k: int,
        diversity_weight: float = 0.20,
    ):
        """
        Diagnostic-only inspection of diversity selection.

        Shows why each candidate is selected or rejected by the
        diversity stage.

        This method does NOT modify production retrieval behavior.
        """

        if not candidates:
            return {
                "selected": [],
                "rounds": [],
            }

        selected = [candidates[0]]
        remaining = list(candidates[1:])

        rounds = [
            {
                "round": 1,
                "selected_chunk_id": candidates[0]["document"]
                .metadata.get("chunk_id"),
                "reason": "initial highest-ranked candidate",
            }
        ]

        while (
            remaining
            and len(selected) < k
        ):

            selected_documents = [
                item["document"]
                for item in selected
            ]

            evaluations = []

            for index, candidate in enumerate(
                remaining
            ):

                relevance = candidate["final_score"]

                redundancy = cls._max_text_similarity(
                    candidate["document"],
                    selected_documents,
                )

                diversity_score = (
                    (1.0 - diversity_weight)
                    * relevance
                    - diversity_weight
                    * redundancy
                )

                evaluations.append(
                    {
                        "remaining_index": index,
                        "chunk_id": candidate["document"]
                        .metadata.get("chunk_id"),
                        "relevance": float(
                            relevance
                        ),
                        "redundancy": float(
                            redundancy
                        ),
                        "diversity_score": float(
                            diversity_score
                        ),
                        "page": candidate["document"]
                        .metadata.get("page"),
                        "section": candidate["document"]
                        .metadata.get("section_title"),
                    }
                )

            evaluations.sort(
                key=lambda item: item["diversity_score"],
                reverse=True,
            )

            winner = evaluations[0]

            winner_index = winner["remaining_index"]

            selected_item = remaining.pop(
                winner_index
            )

            selected.append(
                selected_item
            )

            rounds.append(
                {
                    "round": len(selected),
                    "selected_chunk_id": winner[
                        "chunk_id"
                    ],
                    "selected_relevance": winner[
                        "relevance"
                    ],
                    "selected_redundancy": winner[
                        "redundancy"
                    ],
                    "selected_diversity_score": winner[
                        "diversity_score"
                    ],
                    "candidates": evaluations,
                }
            )

        return {
            "selected": [
                item["document"]
                .metadata.get("chunk_id")
                for item in selected
            ],
            "rounds": rounds,
        }

    # ============================================================
    # CITATIONS
    # ============================================================

    @staticmethod
    def _assign_citation_ids(documents):
        for citation_id, document in enumerate(
            documents,
            start=1,
        ):
            document.metadata[
                "citation_id"
            ] = citation_id

        return documents

    # ============================================================
    # STANDARD RETRIEVAL
    # ============================================================

    def _retrieve(
        self,
        query: str,
        k: int,
        *,
        diversity_weight: float,
        summary: bool = False,
    ):

        candidate_pool = max(
            k,
            settings.RETRIEVAL_CANDIDATES,
        )

        results = (
            self.vector_store
            .similarity_search_with_score(
                query=query,
                k=candidate_pool,
            )
        )

        logger.info(
            "Candidates retrieved: %d",
            len(results),
        )

        filtered = [
            (document, score)
            for document, score in results
            if score >= settings.MIN_SIMILARITY_SCORE
        ]

        logger.info(
            "After score filtering: %d",
            len(filtered),
        )

        # --------------------------------------------------------
        # Standard retrieval only:
        # remove obvious structural noise before reranking.
        #
        # Summary retrieval may benefit from TOC-like material,
        # so it is intentionally preserved there.
        # --------------------------------------------------------

        if not summary:

            before_noise_filter = len(filtered)

            filtered = [
                (document, score)
                for document, score in filtered
                if not self._is_structural_noise(
                    document
                )
            ]

            logger.info(
                "After structural-noise filtering: %d "
                "(removed %d)",
                len(filtered),
                before_noise_filter - len(filtered),
            )

        ranked = []

        for document, semantic_score in filtered:

            if summary:

                summary_signal = (
                    self._summary_signal_score(
                        document
                    )
                )

                section_score = (
                    self._section_title_score(
                        query,
                        document,
                    )
                )

                final_score = (
                    0.70 * semantic_score
                    + 0.15 * summary_signal
                    + 0.15 * section_score
                )

            else:

                final_score = self._rerank_score(
                    query=query,
                    document=document,
                    semantic_score=semantic_score,
                )

            ranked.append(
                {
                    "document": document,
                    "semantic_score": semantic_score,
                    "final_score": final_score,
                }
            )

        ranked.sort(
            key=lambda item: item["final_score"],
            reverse=True,
        )

        unique = self._deduplicate(
            ranked
        )

        logger.info(
            "After deduplication: %d",
            len(unique),
        )

        selected = self._select_diverse_results(
            unique,
            k=k,
            diversity_weight=diversity_weight,
        )

        documents = self._assign_citation_ids(
            [
                item["document"]
                for item in selected
            ]
        )

        return selected, documents

    # ============================================================
    # RETRIEVAL DEBUGGING
    # ============================================================

    def debug_retrieval(
        self,
        query: str,
        k: int = 5,
    ):
        """
        Diagnostic-only retrieval trace.

        This reproduces the production retrieval pipeline but
        exposes every intermediate stage.

        IMPORTANT:
        This method does NOT modify production retrieval behavior.
        """

        candidate_pool = max(
            k,
            settings.RETRIEVAL_CANDIDATES,
        )

        # --------------------------------------------------------
        # 1. Dense retrieval
        # --------------------------------------------------------

        dense_results = (
            self.vector_store
            .similarity_search_with_score(
                query=query,
                k=candidate_pool,
            )
        )

        # --------------------------------------------------------
        # Helper for serializing a result
        # --------------------------------------------------------

        def serialize_item(
            document,
            semantic_score,
            final_score=None,
        ):
            return {
                "chunk_id": document.metadata.get(
                    "chunk_id"
                ),
                "semantic_score": float(
                    semantic_score
                ),
                "final_score": (
                    float(final_score)
                    if final_score is not None
                    else None
                ),
                "page": document.metadata.get(
                    "page"
                ),
                "page_label": document.metadata.get(
                    "page_label"
                ),
                "section": document.metadata.get(
                    "section_title"
                ),
                "content": document.page_content,
            }

        dense = [
            serialize_item(
                document,
                semantic_score,
            )
            for document, semantic_score
            in dense_results
        ]

        # --------------------------------------------------------
        # 2. Similarity threshold
        # --------------------------------------------------------

        filtered = [
            (document, score)
            for document, score in dense_results
            if score >= settings.MIN_SIMILARITY_SCORE
        ]

        # --------------------------------------------------------
        # 3. Structural-noise filtering
        # --------------------------------------------------------

        noise_filtered = [
            (document, score)
            for document, score in filtered
            if not self._is_structural_noise(
                document
            )
        ]

        # --------------------------------------------------------
        # 4. Reranking
        # --------------------------------------------------------

        ranked = []

        for document, semantic_score in noise_filtered:

            final_score = self._rerank_score(
                query=query,
                document=document,
                semantic_score=semantic_score,
            )

            ranked.append(
                {
                    "document": document,
                    "semantic_score": semantic_score,
                    "final_score": final_score,
                }
            )

        ranked.sort(
            key=lambda item: item["final_score"],
            reverse=True,
        )

        reranked = [
            serialize_item(
                item["document"],
                item["semantic_score"],
                item["final_score"],
            )
            for item in ranked
        ]

        # --------------------------------------------------------
        # 5. Deduplication
        # --------------------------------------------------------

        unique = self._deduplicate(
            ranked
        )

        deduplicated = [
            serialize_item(
                item["document"],
                item["semantic_score"],
                item["final_score"],
            )
            for item in unique
        ]

        # --------------------------------------------------------
        # 6. Diversity selection
        # --------------------------------------------------------

        selected = self._select_diverse_results(
            unique,
            k=k,
            diversity_weight=self.STANDARD_DIVERSITY_WEIGHT,
        )

        final_results = [
            serialize_item(
                item["document"],
                item["semantic_score"],
                item["final_score"],
            )
            for item in selected
        ]

        return {
            "query": query,
            "requested_k": k,
            "candidate_pool": candidate_pool,
            "similarity_threshold": (
                settings.MIN_SIMILARITY_SCORE
            ),
            "stages": {
                "dense": dense,
                "filtered": [
                    serialize_item(
                        document,
                        score,
                    )
                    for document, score in filtered
                ],
                "noise_filtered": [
                    serialize_item(
                        document,
                        score,
                    )
                    for document, score in noise_filtered
                ],
                "reranked": reranked,
                "deduplicated": deduplicated,
                "final": final_results,
            },
        }

    # ============================================================
    # RETRIEVAL COMPONENT DEBUGGING
    # ============================================================

    def debug_retrieval_components(
        self,
        query: str,
        chunk_ids: list[int],
    ):
        """
        Diagnostic-only inspection of specific chunks.

        Shows the individual retrieval signals used by:
        - structural-noise filtering
        - reranking

        This method does NOT modify production retrieval behavior.
        """

        results = (
            self.vector_store
            .similarity_search_with_score(
                query=query,
                k=settings.RETRIEVAL_CANDIDATES,
            )
        )

        output = []

        for document, semantic_score in results:

            chunk_id = document.metadata.get(
                "chunk_id"
            )

            if chunk_id not in chunk_ids:
                continue

            text = document.page_content

            scores = {
                "lexical": self._lexical_overlap(
                    query,
                    text,
                ),
                "important": self._important_term_score(
                    query,
                    text,
                ),
                "phrase": self._phrase_score(
                    query,
                    text,
                ),
                "numeric": self._numeric_relevance(
                    query,
                    text,
                ),
                "question": self._question_signal_score(
                    query,
                    text,
                ),
                "section": self._section_title_score(
                    query,
                    document,
                ),
            }

            rerank_score = self._rerank_score(
                query=query,
                document=document,
                semantic_score=semantic_score,
            )

            output.append(
                {
                    "chunk_id": chunk_id,
                    "semantic_score": float(
                        semantic_score
                    ),
                    "structural_noise": (
                        self._is_structural_noise(
                            document
                        )
                    ),
                    "rerank_score": float(
                        rerank_score
                    ),
                    "signals": scores,
                    "page": document.metadata.get(
                        "page"
                    ),
                    "page_label": document.metadata.get(
                        "page_label"
                    ),
                    "section": document.metadata.get(
                        "section_title"
                    ),
                    "content": text,
                }
            )

        return output

    # ============================================================
    # STANDARD SEARCH
    # ============================================================

    def similarity_search(
        self,
        query: str,
        k: int | None = None,
    ):

        if k is None:
            k = settings.TOP_K

        logger.info(
            "========== RAG RETRIEVAL =========="
        )

        logger.info(
            "Query: %s",
            query,
        )

        logger.info(
            "Requested top-k: %d",
            k,
        )

        logger.info(
            "Candidate pool: %d",
            max(
                k,
                settings.RETRIEVAL_CANDIDATES,
            ),
        )

        selected, documents = self._retrieve(
            query=query,
            k=k,
            diversity_weight=self.STANDARD_DIVERSITY_WEIGHT,
        )

        logger.info(
            "Final results: %d",
            len(documents),
        )

        self._log_results(
            selected,
            title="RETRIEVED DOCUMENT",
        )

        logger.info(
            "========== END RAG RETRIEVAL =========="
        )

        return documents

    # ============================================================
    # SUMMARY
    # ============================================================

    @staticmethod
    def _summary_signal_score(document) -> float:

        text = document.page_content.lower()

        score = 0.0

        matches = sum(
            1
            for term in QdrantStore.SUMMARY_TERMS
            if term in text
        )

        if matches:
            score += min(
                0.7,
                matches * 0.1,
            )

        page = document.metadata.get("page")

        if isinstance(page, int):

            if page == 0:
                score += 0.3

            elif page <= 2:
                score += 0.15

        return min(
            score,
            1.0,
        )

    def summary_search(
        self,
        query: str,
        k: int | None = None,
    ):

        if k is None:
            k = settings.TOP_K

        logger.info(
            "========== SUMMARY RETRIEVAL =========="
        )

        logger.info(
            "Summary Query: %s",
            query,
        )

        logger.info(
            "Requested summary top-k: %d",
            k,
        )

        logger.info(
            "Candidate pool: %d",
            max(
                k,
                settings.RETRIEVAL_CANDIDATES,
            ),
        )

        selected, documents = self._retrieve(
            query=query,
            k=k,
            diversity_weight=0.30,
            summary=True,
        )

        logger.info(
            "Final summary results: %d",
            len(documents),
        )

        self._log_results(
            selected,
            title="SUMMARY DOCUMENT",
            include_scores=False,
        )

        logger.info(
            "========== END SUMMARY RETRIEVAL =========="
        )

        return documents

    # ============================================================
    # LOGGING
    # ============================================================

    @staticmethod
    def _log_results(
        results,
        *,
        title: str,
        include_scores: bool = True,
    ):

        for index, item in enumerate(
            results,
            start=1,
        ):

            document = item["document"]

            if include_scores:

                logger.info(
                    "\n"
                    "========== %s %d ==========\n"
                    "Semantic Score: %.4f\n"
                    "Rerank Score: %.4f\n"
                    "Citation ID: %s\n"
                    "Source: %s\n"
                    "Page: %s\n"
                    "Page Label: %s\n"
                    "Section: %s\n"
                    "Chunk ID: %s\n"
                    "Content:\n%s\n"
                    "============================================",
                    title,
                    index,
                    item["semantic_score"],
                    item["final_score"],
                    document.metadata.get(
                        "citation_id",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "source",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "page",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "page_label",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "section_title",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "chunk_id",
                        "Unknown",
                    ),
                    document.page_content[:1500],
                )

            else:

                logger.info(
                    "\n"
                    "========== %s %d ==========\n"
                    "Citation ID: %s\n"
                    "Source: %s\n"
                    "Page: %s\n"
                    "Page Label: %s\n"
                    "Section: %s\n"
                    "Chunk ID: %s\n"
                    "Content:\n%s\n"
                    "==========================================",
                    title,
                    index,
                    document.metadata.get(
                        "citation_id",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "source",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "page",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "page_label",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "section_title",
                        "Unknown",
                    ),
                    document.metadata.get(
                        "chunk_id",
                        "Unknown",
                    ),
                    document.page_content[:1500],
                )

    # ============================================================
    # DELETE COLLECTION
    # ============================================================

    def delete_collection(self):

        try:

            self.client.delete_collection(
                collection_name=self.collection_name
            )

        except Exception:

            pass

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=self._collection_config(),
        )

        self._initialize_vector_store()
