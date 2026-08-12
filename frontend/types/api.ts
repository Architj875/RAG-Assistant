// ----------------------------
// Chat
// ----------------------------

export interface ChatRequest {
    question: string;
}

export interface Source {
    filename: string;
    page: number | null;
}

export interface ChatData {
    answer: string;
    sources: Source[];
}

// ----------------------------
// Upload
// ----------------------------

export interface UploadData {
    filename: string;
    chunks_indexed: number;
    embedding_model: string;
    vector_store: string;
    message: string;
}

// ----------------------------
// Generic API Response
// ----------------------------

export interface APIResponse<T> {
    success: boolean;
    data: T | null;
    error: string | null;
}

// ----------------------------
// Chat History
// ----------------------------

export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
    sources?: Source[]
}