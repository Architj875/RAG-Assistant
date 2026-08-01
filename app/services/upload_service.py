from app.services.document_service import DocumentService
from app.utils.logger import logger

class UploadService:

    def __init__(self, document_service: DocumentService):
        self.document_service = document_service

    def upload(self, file_path: str):
        try:
            logger.info("Starting upload processing: %s", file_path)

            chunks = self.document_service.ingest_document(file_path)

            logger.info(
                "Upload completed successfully. Indexed %d chunks",
                chunks
            )

            return chunks
        
        except Exception:
            logger.exception("Upload processing failed")
            raise