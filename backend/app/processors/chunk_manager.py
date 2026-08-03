from langchain_core.documents import Document

from app.processors.cleaner import TextCleaner
from app.processors.chunker import TextChunker

class ChunkManager:
    """Coordinates document cleaning and chunking."""

    @staticmethod
    def process_documents(
        documents: list[Document],
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> list[Document]:
        cleaned_documents = TextCleaner.clean_documents(documents)

        chunks = TextChunker.recursive_chunk_documents(
            cleaned_documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        return chunks