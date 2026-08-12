from typing import Any

from pydantic import BaseModel


# ----------------------------
# Chat Schemas
# ----------------------------

class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    filename: str
    page: int | None = None


class ChatData(BaseModel):
    answer: str
    sources: list[Source]


# ----------------------------
# Upload Schemas
# ----------------------------

class UploadData(BaseModel):
    filename: str
    chunks_indexed: int
    embedding_model: str
    vector_store: str
    message: str


# ----------------------------
# Common API Responses
# ----------------------------

class APIResponse(BaseModel):
    success: bool
    data: Any | None = None
    error: str | None = None