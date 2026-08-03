from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.api.schemas import APIResponse, ChatData, ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post(
    "/",
    response_model=APIResponse,
    summary="Ask a question",
    description="Answers a user's question using the Retrieval-Augmented Generation (RAG) pipeline based on the indexed documents.",
)
def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    answer = chat_service.ask(request.question)

    return APIResponse(
        success=True,
        data=ChatData(
            answer=answer,
        ),
        error=None,
    )