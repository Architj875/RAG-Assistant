"use client";

import { MessageSquare } from "lucide-react";

interface ChatHeaderProps {
  mode: "rag" | "react";
  setMode: (value: "rag" | "react") => void;
}

export default function ChatHeader({
  mode,
  setMode,
}: ChatHeaderProps) {
  return (
    <div className="border-b border-border px-7 py-5">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary/10">
            <MessageSquare className="h-4.75 w-4.75 text-primary" />
          </div>

          <div>
            <h2 className="text-xl font-semibold tracking-tight text-foreground">
              AI Chat
            </h2>

            <p className="mt-0.5 text-sm text-muted-foreground">
              Ask questions about your uploaded documents.
            </p>
          </div>
        </div>

        <div className="flex rounded-full border border-border bg-secondary/70 p-1">
          <button
            type="button"
            onClick={() => setMode("rag")}
            className={`rounded-full px-3 py-1.5 text-xs font-medium transition ${
              mode === "rag"
                ? "bg-[#5aa973] text-primary-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Standard RAG
          </button>

          <button
            type="button"
            onClick={() => setMode("react")}
            className={`rounded-full px-3 py-1.5 text-xs font-medium transition ${
              mode === "react"
                ? "bg-[#5aa973] text-primary-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            ReAct Agent
          </button>
        </div>
      </div>
    </div>
  );
}