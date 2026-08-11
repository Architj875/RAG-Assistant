"use client";

import { FileText } from "lucide-react";

interface Props {
  filename: string;
}

export default function DocumentPreview({
  filename,
}: Props) {
  return (
    <div className="rounded-2xl border border-border/50 bg-background/30 p-5">
      <div className="flex items-start gap-4">
        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10">
          <FileText className="h-6 w-6 text-primary" />
        </div>

        <div className="min-w-0 flex-1">
          <p
            title={filename}
            className="truncate text-base font-semibold"
          >
            {filename}
          </p>

          <p className="mt-1 text-sm text-muted-foreground">
            Ready to answer questions from this document.
          </p>
        </div>
      </div>
    </div>
  );
}