from app.api.schemas import ChatData, Source
from app.exceptions.custom_exceptions import RAGPipelineError
from app.rag.rag_pipeline import RAGPipeline
from app.utils.logger import logger


class ChatService:
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline

    def ask(self, question: str) -> ChatData:
        try:
            logger.info(
                "Received question (%d characters)",
                len(question),
            )

            result = self.pipeline.ask(question)

            unique_sources = {}

            for document in result.documents:
                metadata = document.metadata

                filename = metadata.get(
                    "source",
                    "Unknown",
                ).split("/")[-1]

                page = metadata.get("page")

                key = (filename, page)

                if key not in unique_sources:
                    unique_sources[key] = Source(
                        filename=filename,
                        page=page,
                    )

            logger.info("Answer generated successfully")

            return ChatData(
                answer=result.answer,
                sources=list(unique_sources.values()),
            )

        except Exception:
            logger.exception("RAG pipeline failed")
            raise RAGPipelineError("Failed to generate answer.")