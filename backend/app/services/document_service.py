from app.loaders.loader_factory import LoaderFactory
from app.processors.chunk_manager import ChunkManager
from app.vectorstores.base_vectorstore import BaseVectorStore
from app.utils.logger import logger


class DocumentService:
    def __init__(self, vector_store: BaseVectorStore):
        self.vector_store = vector_store

    def ingest_document(self, file_path: str):
        try:
            logger.info(
                "Starting document ingestion: %s",
                file_path,
            )

            loader = LoaderFactory.get_loader(file_path)

            documents = loader.load(file_path)

            logger.info(
                "Loaded %d document(s)",
                len(documents),
            )

            chunks = ChunkManager.process_documents(
                documents
            )

            logger.info(
                "Generated %d chunks",
                len(chunks),
            )

            self.vector_store.add_documents(chunks)

            logger.info(
                "Successfully indexed %d chunks into Qdrant",
                len(chunks),
            )

            return len(chunks)

        except Exception:
            logger.exception(
                "Document ingestion failed"
            )
            raise

    # ----------------------------------
    # Knowledge Base Management
    # ----------------------------------

    def delete_collection(self):
        """
        Delete the current vector collection.
        """
        logger.info(
            "Deleting vector collection..."
        )

        self.vector_store.delete_collection()

        logger.info(
            "Vector collection deleted."
        )