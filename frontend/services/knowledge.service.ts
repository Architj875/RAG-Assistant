import api from "@/lib/api";
import {
  APIResponse,
  UploadData,
} from "@/types/api";

export async function refreshKnowledgeBase(): Promise<
  APIResponse<UploadData>
> {
  const response =
    await api.post<APIResponse<UploadData>>(
      "/upload/refresh/"
    );

  return response.data;
}