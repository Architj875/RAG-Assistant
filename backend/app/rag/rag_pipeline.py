from app.config.settings import settings
from app.llms.base_llm import BaseLLM
from app.rag.prompt_builder import PromptBuilder
from app.rag.query_router import (
    QueryRouter,
    QueryType,
)
from app.rag.rag_result import RAGResult
from app.vectorstores.base_vectorstore import BaseVectorStore
from app.utils.logger import logger


class RAGPipeline:

    def __init__(
        self,
        vector_store: BaseVectorStore,
        llm: BaseLLM,
    ):
        self.vector_store = vector_store
        self.llm = llm

    def ask(
        self,
        question: str,
    ) -> RAGResult:

        # ==================================================
        # 1. Classify query
        # ==================================================

        query_type = QueryRouter.classify(
            question
        )

        logger.info(
            "Query: %s",
            question,
        )

        logger.info(
            "Query type: %s",
            query_type.value,
        )

        # ==================================================
        # 2. Select retrieval strategy
        # ==================================================

        if (
            query_type
            == QueryType.DOCUMENT_SUMMARY
        ):

            logger.info(
                "Using document-summary retrieval strategy"
            )

            documents = (
                self.vector_store.summary_search(
                    query=question,
                    k=settings.TOP_K,
                )
            )

        else:

            logger.info(
                "Using standard retrieval strategy"
            )

            documents = (
                self.vector_store.similarity_search(
                    query=question,
                    k=settings.TOP_K,
                )
            )

        logger.info(
            "Documents passed to LLM: %d",
            len(documents),
        )

        # ==================================================
        # 3. Build grounded prompt
        # ==================================================

        prompt = PromptBuilder.build(
            documents=documents,
            question=question,
            query_type=query_type.value,
        )

        # ==================================================
        # 4. Generate answer
        # ==================================================

        answer = self.llm.invoke(
            prompt
        )

        logger.info(
            "Answer generated successfully"
        )

        # ==================================================
        # 5. Return result
        # ==================================================

        return RAGResult(
            answer=answer,
            documents=documents,
        )