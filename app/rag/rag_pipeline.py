from app.llms.llm_factory import LLMFactory
from app.rag.prompt_builder import PromptBuilder
from app.vectorstores.vectorstore_factory import VectorStoreFactory
from app.config.settings import settings

class RAGPipeline:

    def __init__(self):

        self.vector_store = VectorStoreFactory.get_vector_store()

        self.llm = LLMFactory.get_llm()

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