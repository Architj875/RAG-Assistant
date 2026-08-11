"use client";

import {
  AlertCircle,
  CheckCircle2,
  LoaderCircle,
} from "lucide-react";

interface UploadStatusProps {
  selectedFile: File | null;
  isUploading: boolean;
  error: string | null;
  uploadStage: string;
}

export default function UploadStatus({
  selectedFile,
  isUploading,
  error,
  uploadStage,
}: UploadStatusProps) {
  function renderBadge() {
    if (error) {
      return (
        <div className="flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm text-red-400">
          <AlertCircle className="h-4 w-4" />
          Failed
        </div>
      );
    }

    if (isUploading) {
      return (
        <div className="flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-4 py-2 text-sm text-primary">
          <LoaderCircle className="h-4 w-4 animate-spin" />
          Uploading
        </div>
      );
    }

    if (selectedFile) {
      return (
        <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
          <CheckCircle2 className="h-4 w-4" />
          Indexed
        </div>
      );
    }

    return (
      <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
        <CheckCircle2 className="h-4 w-4" />
        Ready
      </div>
    );
  }

  return (
    <div className="mt-8 flex items-center justify-between border-t border-border/50 pt-6">
      <div>
        <p className="text-sm font-medium">
          {uploadStage}
        </p>

        <p className="mt-1 text-sm text-muted-foreground">
          PDF • DOCX • TXT • CSV
        </p>
      </div>

      {renderBadge()}
    </div>
  );
}