from functools import lru_cache

from app.llms.llm_factory import LLMFactory
from app.rag.rag_pipeline import RAGPipeline
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.upload_service import UploadService
from app.vectorstores.vectorstore_factory import VectorStoreFactory


@lru_cache
def get_vector_store():
    return VectorStoreFactory.get_vector_store()


@lru_cache
def get_llm():
    return LLMFactory.get_llm()


@lru_cache
def get_rag_pipeline():
    return RAGPipeline(
        vector_store=get_vector_store(),
        llm=get_llm(),
    )


def get_chat_service():
    return ChatService(get_rag_pipeline())


def get_upload_service():
    return UploadService(
        DocumentService(get_vector_store())
    )