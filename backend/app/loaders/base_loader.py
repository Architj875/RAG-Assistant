from abc import ABC, abstractmethod
from langchain_core.documents import Document

class BaseLoader(ABC):
    """
    Base class for all document loaders.
    """

    @abstractmethod
    def load(self, file_path: str) -> list[Document]:
        """
        Load a document and return LangChain Documnet objects.
        """
        pass