from pathlib import Path

from app.services.document_service import DocumentService
from app.utils.logger import logger


class KnowledgeService:
    """
    Manages the lifecycle of the active knowledge base.
    """

    def __init__(
        self,
        document_service: DocumentService,
    ):
        self.document_service = document_service
        self.upload_directory = Path("data/uploads")

    # ============================================================
    # COMPLETE RESET
    # ============================================================

    def reset(self):
        """
        Completely removes the current knowledge base.

        This removes:
        - Qdrant vectors
        - Uploaded documents
        """

        logger.info("Resetting knowledge base...")

        # ----------------------------------
        # Delete vectors
        # ----------------------------------

        self.document_service.delete_collection()

        # ----------------------------------
        # Delete uploaded files
        # ----------------------------------

        self.clear_uploaded_files()

        logger.info(
            "Knowledge base reset completed."
        )

    # ============================================================
    # REFRESH / REBUILD
    # ============================================================

    def clear_vector_store(self):
        """
        Clears the current vector store without
        deleting the uploaded document.

        Used when refreshing/re-indexing the
        current document.
        """

        logger.info(
            "Clearing vector store for refresh..."
        )

        # ----------------------------------
        # Delete vectors only
        # ----------------------------------

        self.document_service.delete_collection()

        logger.info(
            "Vector store cleared. Uploaded "
            "document preserved."
        )

    # ============================================================
    # FILE MANAGEMENT
    # ============================================================

    def clear_uploaded_files(self):
        """
        Deletes every uploaded file.
        """

        if not self.upload_directory.exists():
            return

        deleted = 0

        for file in self.upload_directory.iterdir():
            if file.is_file():
                file.unlink()
                deleted += 1

        logger.info(
            "Deleted %d uploaded file(s).",
            deleted,
        )