from abc import ABC, abstractmethod

from langchain_core.documents import Document

class BaseEmbedder(ABC):
    """Abstract base class for embedding models."""

    @abstractmethod
    def embed_documents(
        self,
        documents: list[Document],
    ) -> list[list[float]]:
        """
        Generate embeddings for a list of documents.
        """
        pass

    @abstractmethod
    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """
        pass