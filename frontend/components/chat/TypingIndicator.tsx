"use client";

export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-4">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-primary/20 bg-primary/10">
        <span className="h-2 w-2 animate-pulse rounded-full bg-primary" />
      </div>

      <div className="flex items-center gap-1 rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-4">
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.3s]" />
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.15s]" />
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground" />
      </div>
    </div>
  );
}