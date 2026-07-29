from abc import ABC, abstractmethod
from langchain_core.documents import Document

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, dicuments: list[Document]):
        """Add documents to the vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5):
        """Return the most similar documents."""
        pass

    @abstractmethod
    def delete_collection(self):
        """Delete the collection."""
        pass