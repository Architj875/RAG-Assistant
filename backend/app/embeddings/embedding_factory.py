from app.embeddings.base_embedder import BaseEmbedder
from app.embeddings.bge_embedder import BGEEmbedder

class EmbeddingFactory:
    """Factory class for creating embedding models"""

    @staticmethod
    def get_embedder(
        model_type: str = "bge",
    ) -> BaseEmbedder:

        if model_type.lower() == "bge" :
            return BGEEmbedder()

        raise ValueError(f"Unsupported embedding model: {model_type}")