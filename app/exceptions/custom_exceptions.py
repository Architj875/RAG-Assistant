class RAGPipelineError(Exception):
    """Raised when the RAG pipeline fails."""
    pass

class DocumentProcessingError(Exception):
    """Raised when document ingestion fails."""
    pass