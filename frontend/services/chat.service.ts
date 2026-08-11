import api from "@/lib/api";
import { APIResponse, ChatData, ChatRequest } from "@/types/api";

export async function askQuestion(
  payload: ChatRequest
): Promise<APIResponse<ChatData>> {
  const response = await api.post<APIResponse<ChatData>>(
    "/chat/",
    payload
  );

  return response.data;
}