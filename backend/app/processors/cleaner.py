import re

from langchain_core.documents import Document


class TextCleaner:
    """
    Cleans PDF-extracted text while preserving meaningful structure.

    Handles PDFs where normal sentences are extracted as:

        The
        Company
        provides
        all
        leave

    while preserving:
        - headings
        - bullet points
        - paragraph boundaries
        - table-like content
    """

    @staticmethod
    def clean_documents(
        documents: list[Document],
    ) -> list[Document]:

        cleaned_documents = []

        for document in documents:

            cleaned_text = TextCleaner.clean_text(
                document.page_content
            )

            if not cleaned_text:
                continue

            cleaned_documents.append(
                Document(
                    page_content=cleaned_text,
                    metadata=document.metadata.copy(),
                )
            )

        return cleaned_documents

    @staticmethod
    def clean_text(text: str) -> str:

        if not text:
            return ""

        # ==================================================
        # 1. Normalize line endings
        # ==================================================

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # ==================================================
        # 2. Normalize special whitespace
        # ==================================================

        text = text.replace("\u00a0", " ")
        text = text.replace("\u200b", "")
        text = text.replace("\ufeff", "")

        # ==================================================
        # 3. Normalize spaces around newlines
        # ==================================================

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"[ \t]*\n[ \t]*",
            "\n",
            text,
        )

        # ==================================================
        # 4. Fix hyphenated line breaks
        #
        # employ-
        # ment
        #
        # -> employment
        # ==================================================

        text = re.sub(
            r"(?<=\w)-\n(?=\w)",
            "",
            text,
        )

        # ==================================================
        # 5. Join words separated by a single newline
        #
        # The
        # Company
        #
        # -> The Company
        # ==================================================

        text = re.sub(
            r"(?<=[A-Za-z0-9])\n(?=[A-Za-z0-9])",
            " ",
            text,
        )

        # ==================================================
        # 6. Join words separated by multiple artificial
        # newlines.
        #
        # The
        #
        # Company
        #
        # -> The Company
        #
        # IMPORTANT:
        # Don't do this around bullets.
        # ==================================================

        previous = None

        while previous != text:

            previous = text

            text = re.sub(
                r"(?<=[A-Za-z0-9,.;:!?%)\]])"
                r"\n+"
                r"(?=[A-Za-z0-9(\[])",
                " ",
                text,
            )

        # ==================================================
        # 7. Preserve bullet boundaries
        # ==================================================

        text = re.sub(
            r"\s*(●)\s*",
            r"\n● ",
            text,
        )

        # ==================================================
        # 8. Preserve numbered list boundaries
        # ==================================================

        text = re.sub(
            r"\s+(\d+\.)\s+",
            r"\n\1 ",
            text,
        )

        # ==================================================
        # 9. Normalize spaces
        # ==================================================

        text = re.sub(
            r"[ \t]{2,}",
            " ",
            text,
        )

        # ==================================================
        # 10. Remove spaces before punctuation
        # ==================================================

        text = re.sub(
            r"\s+([,.;:!?])",
            r"\1",
            text,
        )

        # ==================================================
        # 11. Normalize excessive blank lines
        # ==================================================

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        # ==================================================
        # 12. Clean whitespace around newlines
        # ==================================================

        text = re.sub(
            r"[ \t]+\n",
            "\n",
            text,
        )

        text = re.sub(
            r"\n[ \t]+",
            "\n",
            text,
        )

        # ==================================================
        # 13. Final whitespace cleanup
        # ==================================================

        return text.strip()