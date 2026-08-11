"use client";

import {
  Database,
  Boxes,
  Cpu,
} from "lucide-react";

import { useWorkspace } from "@/hooks/useWorkspace";

export default function KnowledgeStats() {
  const { uploadedFile } = useWorkspace();

  if (!uploadedFile) return null;

  const stats = [
    {
      icon: Boxes,
      label: "Chunks",
      value: uploadedFile.chunks_indexed,
    },
    {
      icon: Cpu,
      label: "Embeddings",
      value: "Gemini",
    },
    {
      icon: Database,
      label: "Vector Store",
      value: "Qdrant",
    },
  ];

  return (
    <div>
      <div className="mb-4 text-[11px] uppercase tracking-[0.24em] text-muted-foreground">
        Knowledge Statistics
      </div>

      <div className="space-y-3">
        {stats.map((item) => (
          <div
            key={item.label}
            className="
              flex
              items-center
              justify-between
              rounded-2xl
              border
              border-white/5
              bg-white/[0.03]
              px-4
              py-3
              transition-all
              duration-300
              hover:border-primary/20
              hover:bg-primary/5
            "
          >
            <div className="flex items-center gap-3">
              <item.icon className="h-4 w-4 text-primary" />

              <span className="text-sm text-muted-foreground">
                {item.label}
              </span>
            </div>

            <span className="font-medium">
              {item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}