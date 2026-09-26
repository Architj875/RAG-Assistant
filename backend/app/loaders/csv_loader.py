import csv

from langchain_core.documents import Document
from app.loaders.base_loader import BaseLoader


class CSVLoader(BaseLoader):
    """
    CSV is row-based, not page-based. Each CSV record should retain
    a location object describing its row position, while still
    staying compatible with the generic document pipeline.
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

                location_label = f"Row {row_index + 1}"

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": file_path,
                            "file_name": file_path.split("/")[-1],
                            "file_type": "csv",
                            "title": file_path.split("/")[-1],
                            "heading_path": [],
                            "location": {
                                "kind": "row",
                                "start": row_index + 1,
                                "end": row_index + 1,
                                "label": location_label,
                            },
                            "row_index": row_index,
                            # keep old fields for compatibility
                            "page_start": None,
                            "page_end": None,
                            "page": None,
                            "page_label": location_label,
                        },
                    )
                )

        return documents