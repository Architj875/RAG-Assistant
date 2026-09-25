import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    # ==================================================
    # Google / LLM
    # ==================================================

    GOOGLE_API_KEY = os.getenv(
        "GOOGLE_API_KEY"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME"
    )

    # ==================================================
    # Embeddings
    # ==================================================

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL"
    )

    # ==================================================
    # Chunking
    # ==================================================

    CHUNK_SIZE = int(
        os.getenv(
            "CHUNK_SIZE",
            700,
        )
    )

    CHUNK_OVERLAP = int(
        os.getenv(
            "CHUNK_OVERLAP",
            120,
        )
    )

    # ==================================================
    # Retrieval
    # ==================================================

    # Final number of chunks sent to the LLM
    TOP_K = int(
        os.getenv(
            "TOP_K",
            5,
        )
    )

    # Number of candidates retrieved from Qdrant
    # before deduplication / selection
    RETRIEVAL_CANDIDATES = int(
        os.getenv(
            "RETRIEVAL_CANDIDATES",
            30,
        )
    )

    # Minimum similarity score.
    #
    # Keep this at 0 initially because similarity scores
    # can vary depending on the embedding model and query.
    MIN_SIMILARITY_SCORE = float(
        os.getenv(
            "MIN_SIMILARITY_SCORE",
            0.0,
        )
    )

    # ==================================================
    # Qdrant
    # ==================================================

    QDRANT_COLLECTION_NAME = os.getenv(
        "QDRANT_COLLECTION_NAME",
        "knowledge_base",
    )

    QDRANT_DB_PATH = os.getenv(
        "QDRANT_DB_PATH",
        "./qdrant_db",
    )


settings = Settings()