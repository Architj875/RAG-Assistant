import { ReactNode } from "react";

import { cn } from "@/lib/utils";
import GlassCard from "@/components/ui/card/GlassCard";

interface Props {
  children: ReactNode;
  className?: string;
}

export default function UploadCard({
  children,
  className,
}: Props) {
  return (
    <GlassCard
      className={cn(
        "flex h-full min-h-0 flex-col overflow-hidden rounded-3xl border border-primary/10 bg-card/60 p-8 backdrop-blur-xl",
        className
      )}
    >
      {children}
    </GlassCard>
  );
}