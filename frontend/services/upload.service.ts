import api from "@/lib/api";
import { APIResponse, UploadData  } from "@/types/api";

export async function uploadDocument(
    file: File
): Promise<APIResponse<UploadData>> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<APIResponse<UploadData>>(
        "/upload/",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
}