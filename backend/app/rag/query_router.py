from enum import Enum


class QueryType(str, Enum):

    FACTUAL = "factual"

    SECTION_SUMMARY = "section_summary"

    DOCUMENT_SUMMARY = "document_summary"


class QueryRouter:
    """
    Classifies the user's question into a small number
    of generic query types.

    The router does NOT determine the answer.

    It only determines what kind of response the
    user is requesting so the RAG pipeline can
    choose an appropriate retrieval/prompt strategy.
    """

    # ============================================================
    # DOCUMENT-LEVEL SUMMARY PHRASES
    # ============================================================

    DOCUMENT_SUMMARY_PHRASES = (
        "this document",
        "the document",
        "entire document",
        "whole document",
        "this file",
        "the file",
        "whole file",
        "entire file",
        "document about",
        "file about",
    )

    # ============================================================
    # GENERIC DOCUMENT SUMMARY QUESTIONS
    # ============================================================

    GENERIC_DOCUMENT_SUMMARY_QUESTIONS = {
        "what is this document about?",
        "what is the document about?",
        "what is this file about?",
        "what is the file about?",
        "what are the key points?",
        "what are the main points?",
        "what are the important points?",
        "what are the key takeaways?",
        "what are the main takeaways?",
        "give me a summary",
        "give me a summary of this document",
        "give me a summary of the document",
        "summarize this",
        "summarize this document",
        "summarize the document",
        "summarize this file",
        "summarize the file",
        "give me an overview",
        "give me an overview of this document",
        "give me an overview of the document",
        "give me an overview of this file",
        "what should i know?",
        "what should i know about this document?",
        "what should i know about the document?",
        "what does this document contain?",
        "what does the document contain?",
        "what does this file contain?",
        "what is contained in this document?",
    }

    # ============================================================
    # SECTION / TOPIC SUMMARY PHRASES
    #
    # IMPORTANT:
    #
    # These phrases describe a request to summarize/explain
    # a topic or section.
    #
    # Rule/requirement/guideline questions are intentionally
    # NOT included here because they can be factual questions.
    # ============================================================

    SECTION_SUMMARY_PHRASES = (
        "summarize the",
        "summary of the",
        "overview of the",
        "key points of the",
        "main points of the",
        "important points of the",
        "key takeaways from the",
        "main takeaways from the",
        "tell me about",
        "explain the",
        "describe the",
    )

    # ============================================================
    # CLASSIFICATION
    # ============================================================

    @classmethod
    def classify(
        cls,
        question: str,
    ) -> QueryType:

        normalized = (
            question
            .strip()
            .lower()
        )

        # --------------------------------------------------------
        # Normalize repeated whitespace.
        # --------------------------------------------------------

        normalized = " ".join(
            normalized.split()
        )

        # ========================================================
        # 1. Explicit document-level questions
        # ========================================================

        if (
            normalized
            in cls.GENERIC_DOCUMENT_SUMMARY_QUESTIONS
        ):
            return QueryType.DOCUMENT_SUMMARY

        # ========================================================
        # 2. Explicit document/file reference + summary intent
        # ========================================================

        if any(
            phrase in normalized
            for phrase in cls.DOCUMENT_SUMMARY_PHRASES
        ):

            document_summary_indicators = (
                "about",
                "overview",
                "summary",
                "summarize",
                "key points",
                "main points",
                "important points",
                "key takeaways",
                "main takeaways",
                "contain",
                "contains",
                "know",
            )

            if any(
                indicator in normalized
                for indicator in document_summary_indicators
            ):
                return QueryType.DOCUMENT_SUMMARY

        # ========================================================
        # 3. Section/topic summary
        # ========================================================

        if any(
            phrase in normalized
            for phrase in cls.SECTION_SUMMARY_PHRASES
        ):
            return QueryType.SECTION_SUMMARY

        # ========================================================
        # 4. Everything else is factual
        # ========================================================

        return QueryType.FACTUAL