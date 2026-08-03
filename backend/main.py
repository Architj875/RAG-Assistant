from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.api.exception_handlers import register_exception_handlers
from app.middleware.logging_middleware import logging_middleware

app = FastAPI(
    title="RAG Assistant API",
    version="1.0.0",
    description="""
A production-ready Retrieval-Augmented Generation (RAG) API built with FastAPI.

## Features

- Upload PDF, DOCX, TXT, CSV, HTML and Markdown documents
- Automatic chunking and embedding generation
- Qdrant vector database
- Semantic document retrieval
- Gemini-powered question answering
- RESTful API

Built by Archit Joshi.
""",
    contact={
        "name": "Archit Joshi",
        "email": "architj875@email.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all custom exception handlers
register_exception_handlers(app)

# Register all API routes
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the RAG Assistant API!"
    }