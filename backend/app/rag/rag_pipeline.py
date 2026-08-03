from app.llms.base_llm import BaseLLM
from app.rag.prompt_builder import PromptBuilder
from app.vectorstores.base_vectorstore import BaseVectorStore
from app.config.settings import settings

class RAGPipeline:

    def __init__(
        self, 
        vector_store: BaseVectorStore,
        llm: BaseLLM,
    ):

        self.vector_store = vector_store
        self.llm = llm

    def ask(self, question: str) -> str:
        documents = self.vector_store.similarity_search(
            query=question,
            k=settings.TOP_K,
        )

        prompt = PromptBuilder.build(
            documents,
            question,
        )

        answer = self.llm.invoke(prompt)
        return answer