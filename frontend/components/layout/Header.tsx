"use client";

import { Sparkles } from "lucide-react";

export default function Header() {
  return (
    <header className="shrink-0">
      <div className="flex items-center gap-2 font-mono-jb text-[11px] uppercase tracking-[0.28em] text-primary">
        <Sparkles className="h-3.5 w-3.5" />
        <span>AI Document Intelligence</span>
      </div>

      <h1 className="mt-2 text-2xl font-newsreader tracking-tight text-[#F5F5F5]">
        RAG Assistant{" "}
        <span className="font-mono-jb text-[12px] tracking-widest">
          v0.1
        </span>
      </h1>

      <p className="mt-1 font-mono-jb text-sm text-muted-foreground">
        retrieval · augmented · answers
      </p>
    </header>
  );
}