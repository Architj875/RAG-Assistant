from langchain_community.document_loaders import TextLoader

from app.loaders.base_loader import BaseLoader

class MarkdownLoader(BaseLoader):

    def load(self, file_path: str):
        loader = TextLoader(file_path)

        return loader.load()