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
    <div className="flex min-w-0 items-center justify-between gap-4">
      <div className="flex min-w-0 items-center">
        <div className="flex min-w-0 items-center gap-2 px-2.5">
          <FileText className="h-4 w-4 shrink-0 text-primary" />

          <div className="min-w-0 max-w-[240px]">
            <p className="truncate text-xs font-medium text-foreground">
              {filename}
            </p>

            <p className="text-[10px] text-muted-foreground">
              Current document
            </p>
          </div>
        </div>

        <div className="mx-2 h-7 w-px bg-border" />

        <div className="flex items-center gap-2 px-2.5">
          <Sparkles className="h-4 w-4 text-primary" />

          <div>
            <p className="text-xs font-medium text-foreground">
              Gemini
            </p>

            <p className="text-[10px] text-muted-foreground">
              AI model
            </p>
          </div>
        </div>

        <div className="mx-2 h-7 w-px bg-border" />

        <div className="flex items-center gap-2 px-2.5">
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              isReady
                ? "bg-primary shadow-[0_0_10px_rgba(34,197,94,0.7)]"
                : "bg-muted-foreground/40"
            }`}
          />

          <span
            className={`text-xs ${
              isReady
                ? "text-primary"
                : "text-muted-foreground"
            }`}
          >
            {isReady ? "Ready" : "Waiting"}
          </span>
        </div>
      </div>

      <div className="flex shrink-0 items-center gap-1">
        <button
          type="button"
          onClick={onRefresh}
          aria-label="Refresh knowledge base"
          title="Refresh"
          className="
            flex h-9 w-9 items-center justify-center
            rounded-xl
            text-muted-foreground
            transition-all
            duration-300
            hover:bg-primary/10
            hover:text-primary
            hover:shadow-[0_0_18px_rgba(34,197,94,0.08)]
          "
        >
          <RefreshCw className="h-4 w-4" />
        </button>

        <button
          type="button"
          onClick={onClear}
          aria-label="Clear chat"
          title="Clear chat"
          className="
            flex h-9 w-9 items-center justify-center
            rounded-xl
            text-muted-foreground
            transition-all
            duration-300
            hover:bg-red-500/10
            hover:text-red-400
          "
        >
          <Trash2 className="h-4 w-4" />
        </button>

        <button
          type="button"
          onClick={onSettings}
          aria-label="Settings"
          title="Settings"
          className="
            flex h-9 w-9 items-center justify-center
            rounded-xl
            text-muted-foreground
            transition-all
            duration-300
            hover:bg-primary/10
            hover:text-primary
          "
        >
          <Settings className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}