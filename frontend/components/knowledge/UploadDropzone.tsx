"use client";

import { useState } from "react";
import {
  UploadCloud,
  FileText,
} from "lucide-react";

import GlassButton from "@/components/ui/button/GlassButton";
import GlassCard from "@/components/ui/card/GlassCard";

interface Props {
  progress: number;
  onChooseFile: () => void;
  onFileDrop: (file: File) => void;
}

export default function UploadDropzone({
  progress,
  onChooseFile,
  onFileDrop,
}: Props) {
  const [dragging, setDragging] =
    useState(false);

  function handleDrop(
    e: React.DragEvent<HTMLDivElement>
  ) {
    e.preventDefault();

    setDragging(false);

    const file = e.dataTransfer.files?.[0];

    if (file) {
      onFileDrop(file);
    }
  }

  return (
    <GlassCard
      className={`
        border-2
        border-dashed
        transition-all
        duration-300
        ${
          dragging
            ? "border-primary bg-primary/5"
            : "border-white/10"
        }
      `}
    >
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() =>
          setDragging(false)
        }
        onDrop={handleDrop}
        className="flex flex-col items-center justify-center p-8 text-center"
      >
        <div className="mb-6 rounded-full bg-primary/10 p-5">
          <UploadCloud className="h-10 w-10 text-primary" />
        </div>

        <h3 className="text-xl font-semibold">
          Upload Knowledge Base
        </h3>

        <p className="mt-2 max-w-xs text-sm text-muted-foreground">
          Drag & drop your PDF, DOCX or TXT
          file here.
        </p>

        <GlassButton
          onClick={onChooseFile}
          className="mt-6"
        >
          <FileText className="mr-2 h-4 w-4" />
          Browse Files
        </GlassButton>

        {progress > 0 && (
          <div className="mt-6 w-full">
            <div className="h-2 overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full rounded-full bg-primary transition-all duration-500"
                style={{
                  width: `${progress}%`,
                }}
              />
            </div>

            <p className="mt-2 text-xs text-muted-foreground">
              {progress}% uploaded
            </p>
          </div>
        )}
      </div>
    </GlassCard>
  );
}