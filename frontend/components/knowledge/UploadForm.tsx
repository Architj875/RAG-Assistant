"use client";

import type { RefObject } from "react";
import { useState } from "react";
import { toast } from "sonner";

import { uploadDocument } from "@/services/upload.service";
import { useWorkspace } from "@/hooks/useWorkspace";

import UploadDropzone from "./UploadDropzone";

interface UploadFormProps {
  inputRef: RefObject<HTMLInputElement | null>;
  showDropzone?: boolean;
}

export default function UploadForm({
  inputRef,
  showDropzone = true,
}: UploadFormProps) {
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
    } catch (err) {
      toast.error(
        err instanceof Error
          ? err.message
          : "Upload failed"
      );

      setProgress(0);
    } finally {
      setIsUploading(false);
    }
  }

  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    void handleUpload(file);

    // Allows selecting the same file again later.
    event.target.value = "";
  }

  return (
    <>
      {showDropzone && (
        <UploadDropzone
          progress={progress}
          onChooseFile={() =>
            inputRef.current?.click()
          }
          onFileDrop={handleUpload}
        />
      )}

      <input
        ref={inputRef}
        hidden
        type="file"
        accept=".pdf,.docx,.txt,.csv,.md,.html"
        onChange={handleFileChange}
      />
    </>
  );
}