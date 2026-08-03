from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import get_upload_service
from app.api.schemas import APIResponse, UploadData
from app.exceptions.custom_exceptions import DocumentProcessingError
from app.services.upload_service import UploadService

router = APIRouter()

UPLOAD_DIRECTORY = Path("data/uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.post(
    "/",
    response_model=APIResponse,
    summary="Upload a document",
    description="Uploads a document, splits it into chunks, generates embeddings, and stores them in Qdrant.",
)
def upload_document(
    file: UploadFile = File(...),
    upload_service: UploadService = Depends(get_upload_service),
):
    try:
        file_path = UPLOAD_DIRECTORY / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        total_chunks = upload_service.upload(str(file_path))

        return APIResponse(
            success=True,
            data=UploadData(
                filename=file.filename,
                chunks_indexed=total_chunks,
                message="Document uploaded successfully.",
            ),
            error=None,
        )

    except Exception:
        raise DocumentProcessingError("Failed to process document.")