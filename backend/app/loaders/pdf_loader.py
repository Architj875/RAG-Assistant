from langchain_community.document_loaders import PyPDFLoader

from app.loaders.base_loader import BaseLoader

class PDFLoader(BaseLoader):

    def load(self, file_path: str):
        loader = PyPDFLoader(file_path)

        return loader.load()