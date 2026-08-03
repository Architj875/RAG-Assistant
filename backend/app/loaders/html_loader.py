from langchain_community.document_loaders import BSHTMLLoader

from app.loaders.base_loader import BaseLoader

class HTMLLoader(BaseLoader):

    def load(self, file_path: str):
        loader = BSHTMLLoader(file_path)

        return loader.load()