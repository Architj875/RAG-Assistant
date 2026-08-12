from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import (
    get_upload_service,
    get_knowledge_service,
)

from app.api.schemas import (
    APIResponse,
    UploadData,
)

from app.exceptions.custom_exceptions import (
    DocumentProcessingError,
)

from app.services.upload_service import UploadService
from app.services.knowledge_service import KnowledgeService


router = APIRouter()


UPLOAD_DIRECTORY = Path("data/uploads")
UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@router.post(
    "/",
    response_model=APIResponse,
    summary="Upload a document",
    description=(
        "Uploads a document, replaces the current "
        "knowledge base, generates embeddings, "
        "and indexes the document."
    ),
)
def upload_document(
    file: UploadFile = File(...),
    upload_service: UploadService = Depends(
        get_upload_service
    ),
    knowledge_service: KnowledgeService = Depends(
        get_knowledge_service
    ),
):
    try:
        # ----------------------------------
        # Reset previous knowledge base
        # ----------------------------------

        knowledge_service.reset()

        # ----------------------------------
        # Save uploaded file
        # ----------------------------------

        file_path = UPLOAD_DIRECTORY / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # ----------------------------------
        # Index document
        # ----------------------------------

        total_chunks = upload_service.upload(
            str(file_path)
        )

        return APIResponse(
            success=True,
            data=UploadData(
                filename=file.filename,
                chunks_indexed=total_chunks,
                embedding_model="BAAI/bge-base-en-v1.5",
                vector_store="Qdrant",
                message=(
                    "Knowledge base updated successfully."
                ),
            ),
            error=None,
        )

    except Exception:
        raise DocumentProcessingError(
            "Failed to process document."
        )


# ============================================================
# REFRESH CURRENT KNOWLEDGE BASE
# ============================================================

@router.post(
    "/refresh/",
    response_model=APIResponse,
    summary="Refresh the current knowledge base",
    description=(
        "Re-processes the currently uploaded document, "
        "re-generates embeddings, and re-indexes it "
        "into Qdrant."
    ),
)
def refresh_knowledge_base(
    upload_service: UploadService = Depends(
        get_upload_service
    ),
    knowledge_service: KnowledgeService = Depends(
        get_knowledge_service
    ),
):
    try:
        # ----------------------------------
        # Find current uploaded document
        # ----------------------------------

        files = [
            file
            for file in UPLOAD_DIRECTORY.iterdir()
            if file.is_file()
        ]

        if not files:
            return APIResponse(
                success=False,
                data=None,
                error=(
                    "No document is currently uploaded."
                ),
            )

        # ----------------------------------
        # Current document
        # ----------------------------------

        file_path = files[0]

        # ----------------------------------
        # Clear vector store only
        # Keep uploaded document
        # ----------------------------------

        knowledge_service.clear_vector_store()

        # ----------------------------------
        # Re-index current document
        # ----------------------------------

        total_chunks = upload_service.upload(
            str(file_path)
        )

        # ----------------------------------
        # Return updated information
        # ----------------------------------

        return APIResponse(
            success=True,
            data=UploadData(
                filename=file_path.name,
                chunks_indexed=total_chunks,
                embedding_model="BAAI/bge-base-en-v1.5",
                vector_store="Qdrant",
                message=(
                    "Knowledge base refreshed successfully."
                ),
            ),
            error=None,
        )

    except Exception:
        raise DocumentProcessingError(
            "Failed to refresh knowledge base."
        )