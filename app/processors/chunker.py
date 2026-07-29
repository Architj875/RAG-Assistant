from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class TextChunker:
    """Utility class for splitting documents into chunks."""

    @staticmethod
    def recursive_chunk_documents(
        documents: list[Document],
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

        chunks = splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = index

        return chunks