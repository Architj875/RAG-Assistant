"use client";

import { useRef, useState } from "react";
import { toast } from "sonner";

import { uploadDocument } from "@/services/upload.service";
import { useWorkspace } from "@/hooks/useWorkspace";

import UploadDropzone from "./UploadDropzone";

export default function UploadForm() {
  const inputRef = useRef<HTMLInputElement>(null);

  const {
    setUploadedFile,
    setIsUploading,
    setUploadStage,
    setIsReady,
  } = useWorkspace();

  const [progress, setProgress] = useState(0);

  async function handleUpload(file: File) {
    setIsUploading(true);
    setIsReady(false);
    setUploadStage("Uploading...");
    setProgress(20);

    try {
      const response = await uploadDocument(file);

      if (!response.success || !response.data) {
        throw new Error(
          response.error ?? "Upload failed."
      );
      }

      setProgress(100);

      setUploadedFile(response.data);

      setUploadStage("Ready");

      setIsReady(true);

      toast.success("Knowledge base updated");
      setTimeout(() => {
        setProgress(0);
      }, 1200);
    }
    catch (err) {
      toast.error(
        err instanceof Error
          ? err.message
          : "Upload failed"
      );
    } finally {
      setIsUploading(false);
    }
  }

  function handleFileChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = e.target.files?.[0];

    if (!file) return;

    handleUpload(file);

    e.target.value = "";
  }

  return (
    <>
      <UploadDropzone
        progress={progress}
        onChooseFile={() =>
          inputRef.current?.click()
        }
        onFileDrop={handleUpload}
      />

      <input
        ref={inputRef}
        hidden
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={handleFileChange}
      />
    </>
  );
}