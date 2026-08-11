"use client";

import { MessageSquare } from "lucide-react";

export default function ChatHeader() {
  return (
    <div className="border-b border-white/10 px-8 py-6">
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary/10">
          <MessageSquare className="h-5 w-5 text-primary" />
        </div>

        <div>
          <h2 className="text-xl font-semibold">
            AI Chat
          </h2>

          <p className="text-sm text-muted-foreground">
            Ask questions about your uploaded documents.
          </p>
        </div>
      </div>
    </div>
  );
}