from app.loaders.loader_factory import LoaderFactory
from app.processors.chunk_manager import ChunkManager
from app.vectorstores.base_vectorstore import BaseVectorStore
from app.utils.logger import logger


class DocumentService:
    """
    Handles document loading, cleaning, chunking,
    and indexing into the vector store.
    """

    def __init__(
        self,
        vector_store: BaseVectorStore,
    ):
        self.vector_store = vector_store

    def ingest_document(
        self,
        file_path: str,
    ):
        try:
            logger.info(
                "Starting document ingestion: %s",
                file_path,
            )

            # ----------------------------------
            # Load document
            # ----------------------------------

            loader = LoaderFactory.get_loader(
                file_path
            )

            documents = loader.load(
                file_path
            )

            logger.info(
                "Loaded %d document(s)",
                len(documents),
            )

            # ----------------------------------
            # Clean + chunk document
            # ----------------------------------

            chunks = ChunkManager.process_documents(
                documents
            )

            logger.info(
                "Generated %d chunks",
                len(chunks),
            )

            # ----------------------------------
            # DEBUG: Inspect chunks from
            # relevant pages
            # ----------------------------------

            if chunks:

                logger.info(
                    "========== CHUNK SAMPLES =========="
                )

                for chunk in chunks:

                    page = chunk.metadata.get(
                        "page",
                        -1,
                    )

                    if page in [30, 31]:

                        logger.info(
                            "\n"
                            "--- CHUNK %s | PAGE %s ---\n"
                            "%s",
                            chunk.metadata.get(
                                "chunk_id",
                                "unknown",
                            ),
                            page,
                            chunk.page_content,
                        )

                logger.info(
                    "========== END CHUNK SAMPLES =========="
                )

            # ----------------------------------
            # DEBUG: First chunk
            # ----------------------------------

            if chunks:

                logger.info(
                    "========== FIRST CHUNK =========="
                )

                logger.info(
                    "%s",
                    chunks[0].page_content[:1500],
                )

                logger.info(
                    "Metadata: %s",
                    chunks[0].metadata,
                )

                logger.info(
                    "========== END FIRST CHUNK =========="
                )

            # ----------------------------------
            # Index chunks into Qdrant
            # ----------------------------------

            self.vector_store.add_documents(
                chunks
            )

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