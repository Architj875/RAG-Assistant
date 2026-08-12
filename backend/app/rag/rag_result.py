from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class RAGResult:
    answer: str
    documents: list[Document]