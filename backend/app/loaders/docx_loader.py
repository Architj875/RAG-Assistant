from langchain_community.document_loaders import Docx2txtLoader

from app.loaders.base_loader import BaseLoader

class DOCXLoader(BaseLoader):

    def load(self, file_path: str):
        loader = Docx2txtLoader(file_path)

        return loader.load()    