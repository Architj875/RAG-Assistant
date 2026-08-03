from langchain_community.document_loaders import CSVLoader

from app.loaders.base_loader import BaseLoader

class CSVLoader(BaseLoader):

    def load(self, file_path: str):
        loader = CSVLoader(file_path=file_path)
        
        return loader.load()