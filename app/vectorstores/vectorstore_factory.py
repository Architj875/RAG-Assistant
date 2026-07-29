from app.vectorstores.qdrant_store import QdrantStore

class VectorStoreFactory:

    @staticmethod
    def get_vector_store(store_type: str = "qdrant"):
        """
        Returns an instance of the requested vector store.
        """

        if store_type.lower() == "qdrant" :
            return QdrantStore()

        raise ValueError(
            f"Unsupported vector store: {store_type}"
        )