"use client";

import {
  CheckCircle2,
  FileText,
} from "lucide-react";

import { useWorkspace } from "@/hooks/useWorkspace";

import GlassCard from "@/components/ui/card/GlassCard";
import GlassBadge from "@/components/ui/badge/GlassBadge";

export default function KnowledgeCard() {
  const { uploadedFile } = useWorkspace();

  if (!uploadedFile) return null;

  return (
    <GlassCard className="p-5">
      <div className="flex items-start gap-4">

        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
          <FileText className="h-7 w-7 text-primary" />
        </div>

        <div className="min-w-0 flex-1">

          <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">
            Current Document
          </p>

          <h3 className="mt-2 truncate text-lg font-semibold">
            {uploadedFile.filename}
          </h3>

          <p className="mt-1 text-sm text-muted-foreground">
            Indexed successfully and ready for retrieval.
          </p>

          <div className="mt-4">
            <GlassBadge>
              <CheckCircle2 className="h-3.5 w-3.5" />
              Ready
            </GlassBadge>
          </div>

        </div>

      </div>
    </GlassCard>
  );
}