import re

from langchain_core.documents import Document

class TextCleaner:
    """Utility class for cleaning extracted document text."""

    @staticmethod
    def clean_documents(documents: list[Document]) -> list[Document]:
        """
        clean the page_content of each Document while preserving metadata.
        
        Args: 
            documents: List of LangChain Document objects.
            
        Returns:
            List of cleaned Document objects.
        """
        cleaned_documents = []

        for document in documents:
            cleaned_text = TextCleaner.clean_text(document.page_content)

            cleaned_documents.append(
                Document(
                    page_content=cleaned_text,
                    metadata=document.metadata,
                )
            )
        return cleaned_documents

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalize extracted text.
        
        - Convert Windows line endings (\r\n) to Unix line endings (\n).
        - Replace tabs with spaces
        - Collapse multiple spaces
        - Remove trailing spaces
        - Collapse multiple blank lines
        - Strip surrounding whitespaces
        """

        # Normalize line edings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Replace tabs
        text = text.replace("\t", " ")

        # Collapse multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove trailing spaces on each line
        text = re.sub(r"[ \t]+\n", "\n", text)

        # collapse multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip surrounding Whitespace
        return text.strip()