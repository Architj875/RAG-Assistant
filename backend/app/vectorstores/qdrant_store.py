from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

from app.vectorstores.base_vectorstore import BaseVectorStore
from app.embeddings.embedding_factory import EmbeddingFactory


class QdrantStore(BaseVectorStore):

    def __init__(
        self,
        collection_name: str = "employee_handbook",
        db_path: str = "./qdrant_db",
    ):

        self.collection_name = collection_name

        # Embedding model
        self.embedding = EmbeddingFactory.get_embedder().embedding_model

        # Local Qdrant database
        self.client = QdrantClient(path=db_path)

        # Create collection if it doesn't exist
        try:
            self.client.get_collection(self.collection_name)

        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE,
                ),
            )

        # LangChain Vector Store
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def delete_collection(self):
        try:
            self.client.delete_collection(
                collection_name=self.collection_name
            )
        except Exception:
            pass

    def recreate_collection(self):
        self.delete_collection()

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE,
            ),
        )

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )