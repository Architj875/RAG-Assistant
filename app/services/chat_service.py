from app.exceptions.custom_exceptions import RAGPipelineError

from app.rag.rag_pipeline import RAGPipeline
from app.utils.logger import logger

class ChatService:
    def __init__(self, pipeline: RAGPipeline):
        self.pipeline = pipeline

    def ask(self, question: str) -> str:
        try:
            logger.info(
                "Received question (%d characters)",
                len(question),
            )

            answer = self.pipeline.ask(question)

            logger.info("Answer generated successfully")

            return answer

        except Exception:
            logger.exception("RAG pipeline failed")
            raise RAGPipelineError("Failed to generate answer.")