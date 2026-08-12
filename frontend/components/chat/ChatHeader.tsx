"use client";

import { MessageSquare } from "lucide-react";

export default function ChatHeader() {
  return (
    <div className="border-b border-white/10 px-7 py-5">
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary/10">
          <MessageSquare className="h-[19px] w-[19px] text-primary" />
        </div>

        <div>
          <h2 className="text-xl font-semibold tracking-tight">
            AI Chat
          </h2>

          <p className="mt-0.5 text-sm text-muted-foreground">
            Ask questions about your uploaded documents.
          </p>
        </div>
      </div>
    </div>
  );
}