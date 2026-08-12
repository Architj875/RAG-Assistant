"use client";

import {
  FileText,
  Boxes,
  Cpu,
  Database,
} from "lucide-react";

interface KnowledgeStatsProps {
  documentCount: number;
  chunkCount: number;
  embeddingModel: string;
  vectorStore: string;
}

export default function KnowledgeStats({
  documentCount,
  chunkCount,
  embeddingModel,
  vectorStore,
}: KnowledgeStatsProps) {
  const stats = [
    {
      label: "Documents",
      value: documentCount,
      icon: FileText,
    },
    {
      label: "Chunks",
      value: chunkCount,
      icon: Boxes,
    },
    {
      label: "Embeddings",
      value: embeddingModel,
      icon: Cpu,
    },
    {
      label: "Vector Store",
      value: vectorStore,
      icon: Database,
    },
  ];

  return (
    <section className="shrink-0">
      <div className="mb-3 flex items-center gap-2 px-1">
        <Database className="h-3.5 w-3.5 text-primary" />

        <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-muted-foreground">
          Knowledge Statistics
        </p>
      </div>

      <div className="grid grid-cols-2 gap-2.5">
        {stats.map((stat) => {
          const Icon = stat.icon;

          return (
            <div
              key={stat.label}
              className="
                group/stat
                rounded-2xl
                border border-white/[0.08]
                bg-white/[0.025]
                p-3
                backdrop-blur-xl
                transition-all duration-300
                hover:-translate-y-0.5
                hover:border-primary/20
                hover:bg-white/[0.045]
                hover:shadow-[0_8px_25px_rgba(34,197,94,0.08)]
              "
            >
              <div
                className="
                  flex h-8 w-8 items-center justify-center
                  rounded-xl
                  border border-white/[0.08]
                  bg-white/[0.035]
                  transition-all duration-300
                  group-hover/stat:border-primary/20
                  group-hover/stat:bg-primary/[0.08]
                "
              >
                <Icon className="h-4 w-4 text-primary" />
              </div>

              <p
                className="mt-3 truncate text-base font-semibold text-foreground"
                title={String(stat.value)}
              >
                {stat.value}
              </p>

              <p className="mt-0.5 text-[10px] text-muted-foreground">
                {stat.label}
              </p>
            </div>
          );
        })}
      </div>
    </section>
  );
}