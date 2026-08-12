import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --------------------------
    # Google
    # --------------------------

    GOOGLE_API_KEY = os.getenv(
        "GOOGLE_API_KEY"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL"
    )

    # --------------------------
    # Chunking
    # --------------------------

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", 500)
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", 100)
    )

    TOP_K = int(
        os.getenv("TOP_K", 5)
    )

    # --------------------------
    # Qdrant
    # --------------------------

    QDRANT_COLLECTION_NAME = os.getenv(
        "QDRANT_COLLECTION_NAME",
        "knowledge_base",
    )

    QDRANT_DB_PATH = os.getenv(
        "QDRANT_DB_PATH",
        "./qdrant_db",
    )


settings = Settings()