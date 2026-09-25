import { ComponentProps } from "react";

import { cn } from "@/lib/utils";

import Card from "./Card";
import GlassGlow from "./GlassGlow";

type GlassCardProps = ComponentProps<typeof Card>;

export default function GlassCard({
  className,
  children,
  ...props
}: GlassCardProps) {
  return (
    <Card
      className={cn(
        "group relative flex h-full min-h-0 min-w-0 flex-col overflow-hidden",
        "rounded-3xl",
        "border border-border",
        "bg-card/80",
        "backdrop-blur-3xl",
        "shadow-[0_10px_50px_rgba(15,23,42,0.08)]",
        "transition-all duration-300 ease-out",
        "hover:-translate-y-1",
        "hover:border-primary/30",
        "hover:shadow-[0_20px_70px_rgba(34,197,94,0.10)]",
        className
      )}
      {...props}
    >
      <GlassGlow />

      <div className="relative z-10 flex min-h-0 flex-1 flex-col">
        {children}
      </div>
    </Card>
  );
}