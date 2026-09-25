"use client";

import {
  BrainCircuit,
  Database,
  Sparkles,
  X,
} from "lucide-react";

import ThemeSwitcher from "./ThemeSwitcher";

interface SettingsDialogProps {
  open: boolean;
  onClose: () => void;
  embeddingModel?: string;
  vectorStore?: string;
}

export default function SettingsDialog({
  open,
  onClose,
  embeddingModel,
  vectorStore,
}: SettingsDialogProps) {
  if (!open) {
    return null;
  }

  return (
    <div
      className="
        fixed
        inset-0
        z-100
        flex
        items-center
        justify-center
        bg-black/50
        p-6
        backdrop-blur-sm
      "
      onMouseDown={(event) => {
        if (
          event.target ===
          event.currentTarget
        ) {
          onClose();
        }
      }}
    >
      <div
        className="
          relative
          w-full
          max-w-md
          overflow-hidden
          rounded-3xl
          border
          border-border
          bg-card/95
          shadow-[0_20px_60px_rgba(20,30,24,0.10)]
          backdrop-blur-3xl
        "
      >
        <div
          className="
            pointer-events-none
            absolute
            inset-0
            bg-[radial-gradient(circle_at_20%_0%,rgba(34,197,94,0.08),transparent_35%)]
          "
        />

        <div className="relative z-10">
          <div
            className="
              flex
              items-start
              justify-between
              border-b
              border-border
              px-6
              py-5
            "
          >
            <div>
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />

                <h2 className="text-base font-semibold text-foreground">
                  Settings
                </h2>
              </div>

              <p className="mt-1 text-xs text-muted-foreground">
                Configure your RAG workspace.
              </p>
            </div>

            <button
              type="button"
              onClick={onClose}
              aria-label="Close settings"
              className="
                flex
                h-8
                w-8
                items-center
                justify-center
                rounded-xl
                text-muted-foreground
                transition-all
                duration-200
                hover:bg-secondary/80
                hover:text-foreground
              "
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="space-y-5 px-6 py-5">
            <section>
              <div className="mb-2.5">
                <p className="text-xs font-medium text-foreground">
                  Appearance
                </p>

                <p className="mt-0.5 text-[11px] text-muted-foreground">
                  Choose how the application looks.
                </p>
              </div>

              <ThemeSwitcher />
            </section>

            <div className="h-px bg-border" />

            <section>
              <div className="mb-3">
                <p className="text-xs font-medium text-foreground">
                  RAG Configuration
                </p>

                <p className="mt-0.5 text-[11px] text-muted-foreground">
                  Current retrieval and AI configuration.
                </p>
              </div>

              <div className="space-y-2.5">
                <div
                  className="
                    flex
                    items-center
                    gap-3
                    rounded-2xl
                    border
                    border-border
                    bg-secondary/70
                    px-4
                    py-3
                  "
                >
                  <div
                    className="
                      flex
                      h-8
                      w-8
                      shrink-0
                      items-center
                      justify-center
                      rounded-xl
                      bg-primary/8
                    "
                  >
                    <BrainCircuit className="h-4 w-4 text-primary" />
                  </div>

                  <div className="min-w-0">
                    <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
                      AI Model
                    </p>

                    <p className="mt-0.5 text-sm text-foreground">
                      Gemini
                    </p>
                  </div>
                </div>

                <div
                  className="
                    flex
                    items-center
                    gap-3
                    rounded-2xl
                    border
                    border-border
                    bg-secondary/70
                    px-4
                    py-3
                  "
                >
                  <div
                    className="
                      flex
                      h-8
                      w-8
                      shrink-0
                      items-center
                      justify-center
                      rounded-xl
                      bg-primary/8
                    "
                  >
                    <Sparkles className="h-4 w-4 text-primary" />
                  </div>

                  <div className="min-w-0">
                    <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
                      Embeddings
                    </p>

                    <p
                      className="
                        mt-0.5
                        truncate
                        text-sm
                        text-foreground
                      "
                    >
                      {embeddingModel ?? "—"}
                    </p>
                  </div>
                </div>

                <div
                  className="
                    flex
                    items-center
                    gap-3
                    rounded-2xl
                    border
                    border-border
                    bg-secondary/70
                    px-4
                    py-3
                  "
                >
                  <div
                    className="
                      flex
                      h-8
                      w-8
                      shrink-0
                      items-center
                      justify-center
                      rounded-xl
                      bg-primary/8
                    "
                  >
                    <Database className="h-4 w-4 text-primary" />
                  </div>

                  <div>
                    <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
                      Vector Store
                    </p>

                    <p className="mt-0.5 text-sm text-foreground">
                      {vectorStore ?? "—"}
                    </p>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <div
            className="
              border-t
              border-border
              px-6
              py-4
            "
          >
            <p className="text-center text-[10px] text-muted-foreground">
              RAG Assistant · v0.1
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}