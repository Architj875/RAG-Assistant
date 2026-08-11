"use client";

import { Lock } from "lucide-react";

export default function ChatLocked() {
  return (
    <div className="flex h-[550px] flex-col items-center justify-center rounded-3xl border border-dashed border-border/50 text-center">
      <div className="mb-5 rounded-full border border-primary/20 bg-primary/10 p-4">
        <Lock className="h-8 w-8 text-primary" />
      </div>

      <h3 className="text-xl font-semibold">
        Chat Locked
      </h3>

      <p className="mt-3 max-w-md text-muted-foreground">
        Upload a document to unlock your AI
        assistant and begin asking
        questions.
      </p>
    </div>
  );
}