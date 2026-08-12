"use client";

import { FileText } from "lucide-react";

import { Source } from "@/types/api";

interface Props {
  source: Source;
}

export default function SourceCard({
  source,
}: Props) {
  return (
    <div
      className="
        group
        flex
        min-w-0
        items-center
        gap-3
        rounded-xl
        border
        border-white/[0.06]
        bg-white/[0.025]
        px-3
        py-2.5
        transition-all
        duration-300
        hover:border-primary/15
        hover:bg-primary/[0.04]
      "
    >
      {/* File icon */}
      <div
        className="
          flex
          h-8
          w-8
          shrink-0
          items-center
          justify-center
          rounded-lg
          border
          border-white/[0.06]
          bg-white/[0.04]
          transition-all
          duration-300
          group-hover:border-primary/20
          group-hover:bg-primary/10
        "
      >
        <FileText className="h-4 w-4 text-primary" />
      </div>

      {/* Source information */}
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium">
          {source.filename}
        </p>

        <p className="mt-0.5 text-xs text-muted-foreground">
          {source.page !== null
            ? `Page ${source.page}`
            : "Document source"}
        </p>
      </div>
    </div>
  );
}