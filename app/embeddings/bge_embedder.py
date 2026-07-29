from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.embeddings.base_embedder import BaseEmbedder

class BGEEmbedder(BaseEmbedder):
    """Embedding model using BAAI/bge-base-en-v1.5."""

    def __init__(
            self,
            model_name: str = "BAAI/bge-base-en-v1.5",
        ):
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={
                    "device": "cpu"
                },
                encode_kwargs={
                    "normalize_embeddings" : True,
                },
            )

    def embed_documents(
        self,
        documents: list[Document],
    ) -> list[list[float]]:

          texts = [doc.page_content for doc in documents]

          return self.embedding_model.embed_documents(texts)
    
    def embed_query(
        self,
        query: str,
    ) -> list[float]:
          
        return self.embedding_model.embed_query(query)