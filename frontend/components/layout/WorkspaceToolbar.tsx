"use client";

import {
  FileText,
  RefreshCw,
  Settings,
  Sparkles,
  Trash2,
} from "lucide-react";

interface WorkspaceToolbarProps {
  filename?: string;
  isReady?: boolean;
  onRefresh?: () => void;
  onClear?: () => void;
  onSettings?: () => void;
}

export default function WorkspaceToolbar({
  filename = "No document",
  isReady = false,
  onRefresh,
  onClear,
  onSettings,
}: WorkspaceToolbarProps) {
  return (
    <div className="w-full">
      <div
        className="
          flex w-full items-center justify-between
          rounded-2xl
          border border-white/[0.08]
          bg-white/[0.025]
          px-3 py-2
          backdrop-blur-xl
          shadow-[0_8px_30px_rgba(0,0,0,0.16)]
          transition-all duration-300
          hover:border-primary/15
        "
      >
        {/* Left information */}
        <div className="flex min-w-0 items-center">
          {/* Document */}
          <div className="flex min-w-0 items-center gap-2.5 px-2">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-white/[0.05]">
              <FileText className="h-4 w-4 text-primary" />
            </div>

            <div className="min-w-0 max-w-[220px]">
              <p className="truncate text-xs font-medium text-foreground">
                {filename}
              </p>

              <p className="text-[10px] text-muted-foreground">
                Current document
              </p>
            </div>
          </div>

          <div className="mx-2 h-6 w-px bg-white/[0.08]" />

          {/* Model */}
          <div className="flex items-center gap-2 px-2.5">
            <Sparkles className="h-3.5 w-3.5 text-primary" />

            <div>
              <p className="text-xs font-medium text-foreground">
                Gemini
              </p>

              <p className="text-[10px] text-muted-foreground">
                AI model
              </p>
            </div>
          </div>

          <div className="mx-2 h-6 w-px bg-white/[0.08]" />

          {/* Status */}
          <div className="flex items-center gap-2 px-2.5">
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                isReady
                  ? "bg-primary shadow-[0_0_8px_rgba(34,197,94,0.7)]"
                  : "bg-muted-foreground/40"
              }`}
            />

            <span className="text-xs text-muted-foreground">
              {isReady ? "Ready" : "Waiting"}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex shrink-0 items-center gap-1">
          {/* Refresh */}
          <button
            type="button"
            onClick={onRefresh}
            aria-label="Refresh knowledge base"
            className="
              flex h-8 w-8 items-center justify-center
              rounded-xl
              text-muted-foreground
              transition-all duration-300
              hover:bg-primary/10
              hover:text-primary
              hover:shadow-[0_0_16px_rgba(34,197,94,0.10)]
            "
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </button>

          {/* Clear */}
          <button
            type="button"
            onClick={onClear}
            aria-label="Clear chat"
            className="
              flex h-8 w-8 items-center justify-center
              rounded-xl
              text-muted-foreground
              transition-all duration-300
              hover:bg-red-500/10
              hover:text-red-400
            "
          >
            <Trash2 className="h-3.5 w-3.5" />
          </button>

          {/* Settings */}
          <button
            type="button"
            onClick={onSettings}
            aria-label="Settings"
            className="
              flex h-8 w-8 items-center justify-center
              rounded-xl
              text-muted-foreground
              transition-all duration-300
              hover:bg-primary/10
              hover:text-primary
              hover:shadow-[0_0_18px_rgba(34,197,94,0.12)]
            "
          >
            <Settings className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}