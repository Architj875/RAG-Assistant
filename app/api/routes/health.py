from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/",
    summary="Health Check",
    description="Returns the current health status of the RAG Assistant API.",
)
def health():
    return {
        "status": "healthy",
        "message": "RAG Assistant API is running"
    }