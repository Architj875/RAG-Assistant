"use client";

import { useRef } from "react";
import {
  FileText,
  RefreshCw,
  Trash2,
} from "lucide-react";

import { useWorkspace } from "@/hooks/useWorkspace";

import GlassButton from "@/components/ui/button/GlassButton";
import KnowledgeStats from "@/components/knowledge/knowledgeStats";
import UploadForm from "@/components/knowledge/UploadForm";

export default function Sidebar() {
  const {
    uploadedFile,
    isReady,
    isUploading,
    clearWorkspace,
  } = useWorkspace();

  const inputRef = useRef<HTMLInputElement | null>(null);

  const hasDocument = Boolean(uploadedFile);

  return (
    <aside
      className="
        relative
        flex
        h-full
        min-h-0
        flex-col
        overflow-hidden
        rounded-3xl
        border
        border-border
        bg-card/80
        p-5
        backdrop-blur-3xl
        shadow-[0_10px_40px_rgba(15,23,42,0.06)]
        transition-all
        duration-300
        ease-out
        hover:-translate-y-1
        hover:border-primary/25
        hover:bg-secondary/80
        hover:shadow-[0_18px_60px_rgba(34,197,94,0.10)]
      "
    >
      <div
        className="
          pointer-events-none
          absolute
          inset-0
          rounded-3xl
          bg-[radial-gradient(circle_at_18%_8%,rgba(255,255,255,0.02),transparent_35%)]
        "
      />

      <div className="relative z-10 flex h-full min-h-0 flex-col">
        <div className="shrink-0">
          {hasDocument && !isUploading && (
            <div
              className="
                group/document
                rounded-3xl
                border
                border-border
                bg-secondary/70
                p-5
                shadow-[0_10px_30px_rgba(15,23,42,0.04)]
                backdrop-blur-xl
                transition-all
                duration-300
                ease-out
                hover:-translate-y-0.5
                hover:border-primary/25
                hover:bg-secondary/80
                hover:shadow-[0_12px_40px_rgba(34,197,94,0.08)]
              "
            >
              <div className="flex items-start gap-4">
                <div
                  className="
                    flex
                    h-12
                    w-12
                    shrink-0
                    items-center
                    justify-center
                    rounded-2xl
                    border
                    border-primary/10
                    bg-primary/10
                    transition-all
                    duration-300
                    group-hover/document:border-primary/20
                    group-hover/document:bg-primary/[0.14]
                    group-hover/document:shadow-[0_0_24px_rgba(34,197,94,0.10)]
                  "
                >
                  <FileText
                    className="
                      h-6
                      w-6
                      text-primary
                      transition-transform
                      duration-300
                      group-hover/document:scale-105
                    "
                  />
                </div>

                <div className="min-w-0 flex-1">
                  <p
                    className="
                      text-[10px]
                      uppercase
                      tracking-[0.2em]
                      text-muted-foreground
                    "
                  >
                    Current document
                  </p>

                  <p
                    className="
                      mt-2
                      truncate
                      text-base
                      font-semibold
                      text-foreground
                    "
                    title={uploadedFile?.filename}
                  >
                    {uploadedFile?.filename}
                  </p>

                  <p
                    className="
                      mt-1
                      text-xs
                      leading-5
                      text-muted-foreground
                    "
                  >
                    Indexed successfully and ready for retrieval.
                  </p>

                  <div
                    className="
                      mt-3
                      inline-flex
                      items-center
                      gap-2
                      rounded-full
                      border
                      border-primary/20
                      bg-primary/10
                      px-3
                      py-1
                      text-[11px]
                      text-primary
                      transition-all
                      duration-300
                      group-hover/document:border-primary/30
                      group-hover/document:bg-primary/[0.14]
                    "
                  >
                    <span
                      className={`
                        h-1.5
                        w-1.5
                        rounded-full
                        ${
                          isReady
                            ? "bg-primary shadow-[0_0_8px_rgba(34,197,94,0.7)]"
                            : "bg-muted-foreground/50"
                        }
                      `}
                    />

                    {isReady ? "Ready" : "Processing"}
                  </div>
                </div>
              </div>
            </div>
          )}

          <UploadForm
            inputRef={inputRef}
            showDropzone={!hasDocument || isUploading}
          />
        </div>

        <div className="mt-5 shrink-0">
          <KnowledgeStats
            documentCount={hasDocument ? 1 : 0}
            chunkCount={uploadedFile?.chunks_indexed ?? 0}
            embeddingModel={uploadedFile?.embedding_model ?? "—"}
            vectorStore={uploadedFile?.vector_store ?? "—"}
          />
        </div>

        {hasDocument && !isUploading && (
          <div
            className="
              mt-5
              shrink-0
              border-t
              border-border
              pt-4
            "
          >
            <div className="space-y-2.5">
              <GlassButton
                type="button"
                variant="primary"
                className="
                  w-full
                  justify-center
                  py-2.5
                  hover:-translate-y-0.5
                  hover:border-primary/40
                  hover:bg-primary/[0.14]
                  hover:shadow-[0_0_28px_rgba(34,197,94,0.14)]
                "
                onClick={() => {
                  inputRef.current?.click();
                }}
              >
                <RefreshCw className="h-4 w-4" />
                Replace Document
              </GlassButton>

              <GlassButton
                type="button"
                variant="outline"
                className="
                  w-full
                  justify-center
                  py-2.5
                  hover:-translate-y-0.5
                  hover:border-red-400/30
                  hover:bg-red-400/[0.06]
                  hover:text-red-300
                  hover:shadow-[0_0_24px_rgba(248,113,113,0.10)]
                "
                onClick={() => {
                  clearWorkspace();
                }}
              >
                <Trash2 className="h-4 w-4" />
                Remove Document
              </GlassButton>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}