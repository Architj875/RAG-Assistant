from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    DocumentProcessingError,
    RAGPipelineError,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RAGPipelineError)
    async def rag_pipeline_exception_handler(
        _: Request,
        exc: RAGPipelineError,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": str(exc),
            },
        )

    @app.exception_handler(DocumentProcessingError)
    async def document_processing_exception_handler(
        _: Request,
        exc: DocumentProcessingError,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": str(exc),
            },
        )