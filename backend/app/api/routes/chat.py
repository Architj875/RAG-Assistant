from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.api.schemas import APIResponse, ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post(
    "/",
    response_model=APIResponse,
    summary="Ask a question",
    description="Answers a user's question using either the standard RAG pipeline or the ReAct agent.",
)
def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    if request.mode == "react":
        chat_data = chat_service.ask_react(request.question)
    else:
        chat_data = chat_service.ask(request.question)

    return APIResponse(
        success=True,
        data=chat_data,
        error=None,
    )