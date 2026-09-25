import csv

from langchain_core.documents import Document

from app.loaders.base_loader import BaseLoader


class CSVLoader(BaseLoader):
    """
    CSV doesn't fit the heading-hierarchy model the other loaders
    share - a row is a record, not a paragraph under a section - so
    this doesn't route through assemble_documents(). One row is
    already the correct retrievable unit (the chunker's job is to
    split prose that's too long; a row is normally already a
    complete, short unit on its own). This still standardizes on the
    same metadata schema (source, page_start, page_end, heading_path)
    as every other loader, so downstream code never has to special-
    case CSV.
    """

    def load(self, file_path: str):
        documents = []

        with open(file_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
            reader = csv.DictReader(f)

            for row_index, row in enumerate(reader):
                content = "\n".join(
                    f"{key}: {value}" for key, value in row.items() if key
                )
                if not content.strip():
                    continue

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": file_path,
                            "page_start": row_index,
                            "page_end": row_index,
                            "heading_path": "",
                            "row_index": row_index,
                        },
                    )
                )

        return documents