from app.api.schemas import ChatData, Source
from app.exceptions.custom_exceptions import RAGPipelineError
from app.rag.rag_pipeline import RAGPipeline
from app.utils.logger import logger


class ChatService:

    def __init__(
        self,
        pipeline: RAGPipeline,
        react_pipeline=None,
    ):
        self.pipeline = pipeline
        self.react_pipeline = react_pipeline

    def _build_chat_data(
        self,
        answer: str,
        documents: list | None,
    ) -> ChatData:
        unique_sources = {}

        if documents:
            for document in documents:
                metadata = document.metadata

                citation_id = metadata.get("citation_id")
                source = metadata.get("source", "Unknown")
                filename = source.split("/")[-1]
                page = metadata.get("page")
                page_label = metadata.get("page_label")

                if citation_id is None:
                    logger.warning(
                        "Document missing citation_id: %s",
                        filename,
                    )
                    continue

                if citation_id not in unique_sources:
                    unique_sources[citation_id] = Source(
                        citation_id=citation_id,
                        filename=filename,
                        page=page,
                        page_label=page_label,
                    )

        sources = list(unique_sources.values())
        sources.sort(key=lambda source: source.citation_id)

        return ChatData(
            answer=answer,
            sources=sources,
        )

    def ask_react(
        self,
        question: str,
    ) -> ChatData:
        try:
            logger.info(
                "Received React question (%d characters)",
                len(question),
            )

            if self.react_pipeline is None:
                raise ValueError("React pipeline is not configured.")

            result = self.react_pipeline.ask(question)

            return self._build_chat_data(
                answer=result.answer,
                documents=getattr(result, "documents", []),
            )

        except Exception:
            logger.exception("React pipeline failed")
            raise RAGPipelineError("Failed to generate answer.")

    def ask(
        self,
        question: str,
    ) -> ChatData:

        try:
            logger.info(
                "Received question (%d characters)",
                len(question),
            )

            result = self.pipeline.ask(question)

            return self._build_chat_data(
                answer=result.answer,
                documents=result.documents,
            )

        except Exception:
            logger.exception("RAG pipeline failed")
            raise RAGPipelineError("Failed to generate answer.")