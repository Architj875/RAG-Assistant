from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseVectorStore(ABC):

    @abstractmethod
    def add_documents(
        self,
        documents: list[Document],
    ):
        """
        Add documents to the vector store.
        """
        pass

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ):
        """
        Retrieve the most relevant documents for
        factual or topic-specific questions.
        """
        pass

    @abstractmethod
    def summary_search(
        self,
        query: str,
        k: int = 5,
    ):
        """
        Retrieve representative and diverse documents
        for document-level summary questions.
        """
        pass

    @abstractmethod
    def delete_collection(self):
        """
        Delete the vector collection.
        """
        pass