// ============================================================
// CHAT
// ============================================================

export interface ChatRequest {
  question: string;
  mode?: "rag" | "react";
}

export interface Source {
  citation_id: number;
  filename: string;
  file_type?: string | null;
  location_kind?: string | null;
  location_label?: string | null;
  page: number | null;
  page_label: string | null;
}

export interface ChatData {
  answer: string;
  sources: Source[];
}


// ============================================================
// UPLOAD
// ============================================================

export interface UploadData {
  filename: string;
  chunks_indexed: number;
  embedding_model: string;
  vector_store: string;
  message: string;
}


// ============================================================
// GENERIC API RESPONSE
// ============================================================

export interface APIResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
}


// ============================================================
// CHAT HISTORY
// ============================================================

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}