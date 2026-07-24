from pathlib import Path

from app.loaders.csv_loader import CSVLoader
from app.loaders.docx_loader import DOCXLoader
from app.loaders.html_loader import HTMLLoader
from app.loaders.md_loader import MarkdownLoader
from app.loaders.pdf_loader import PDFLoader
from app.loaders.txt_loader import TXTLoader


class LoaderFactory:

    LOADERS = {
        ".pdf": PDFLoader,
        ".docx": DOCXLoader,
        ".txt": TXTLoader,
        ".csv": CSVLoader,
        ".md": MarkdownLoader,
        ".html": HTMLLoader,
    }

    @classmethod
    def get_loader(cls, file_path: str):
        extension = Path(file_path).suffix.lower()

        loader = cls.LOADERS.get(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader()