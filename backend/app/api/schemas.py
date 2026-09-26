from pydantic import BaseModel


# ============================================================
# CHAT
# ============================================================

class ChatRequest(BaseModel):
    question: str
    mode: str = "rag"


class Source(BaseModel):
    citation_id: int
    filename: str
    file_type: str | None = None
    location_kind: str | None = None
    location_label: str | None = None
    page: int | None = None
    page_label: str | None = None


class ChatData(BaseModel):
    answer: str
    sources: list[Source]


# ============================================================
# UPLOAD
# ============================================================

class UploadData(BaseModel):
    filename: str
    chunks_indexed: int
    embedding_model: str
    vector_store: str
    message: str


# ============================================================
# GENERIC API RESPONSE
# ============================================================

class APIResponse(BaseModel):
    success: bool
    data: object | None
    error: str | None