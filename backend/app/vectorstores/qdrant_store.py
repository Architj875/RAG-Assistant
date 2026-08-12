from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config.settings import settings
from app.embeddings.embedding_factory import EmbeddingFactory
from app.vectorstores.base_vectorstore import BaseVectorStore


class QdrantStore(BaseVectorStore):
    def __init__(self):
        self.collection_name = (
            settings.QDRANT_COLLECTION_NAME
        )

        self.db_path = settings.QDRANT_DB_PATH

        # Embedding model
        self.embedding = (
            EmbeddingFactory.get_embedder().embedding_model
        )

        # Local Qdrant database
        self.client = QdrantClient(
            path=self.db_path
        )

        self._initialize_collection()

    # ----------------------------------
    # Private Helpers
    # ----------------------------------

    def _collection_config(self):
        """
        Shared configuration for the Qdrant collection.
        """

        return VectorParams(
            size=768,
            distance=Distance.COSINE,
        )

    def _initialize_collection(self):
        """
        Create the collection if it doesn't exist.
        """

        try:
            self.client.get_collection(
                self.collection_name
            )

        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=self._collection_config(),
            )

        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """
        Initialize the LangChain vector store wrapper.
        """

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )

    # ----------------------------------
    # BaseVectorStore API
    # ----------------------------------

    def add_documents(self, documents):
        self.vector_store.add_documents(
            documents
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ):
        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def delete_collection(self):
        """
        Delete the active collection and recreate
        an empty collection.
        """

        try:
            self.client.delete_collection(
                collection_name=self.collection_name
            )
        except Exception:
            # Collection may not exist yet.
            pass

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=self._collection_config(),
        )

        self._initialize_vector_store()