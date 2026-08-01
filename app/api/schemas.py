from typing import Any

from pydantic import BaseModel


# ----------------------------
# Chat Schemas
# ----------------------------

class ChatRequest(BaseModel):
    question: str


class ChatData(BaseModel):
    answer: str


# ----------------------------
# Upload Schemas
# ----------------------------

class UploadData(BaseModel):
    filename: str
    chunks_indexed: int
    message: str


# ----------------------------
# Common API Responses
# ----------------------------

class APIResponse(BaseModel):
    success: bool
    data: Any | None = None
    error: str | None = None