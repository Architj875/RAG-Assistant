import { ComponentProps } from "react";

import { cn } from "@/lib/utils";

import Button from "./Button";

type Props = ComponentProps<typeof Button> & {
  variant?: "primary" | "outline" | "ghost";
};

export default function GlassButton({
  className,
  variant = "primary",
  children,
  ...props
}: Props) {
  return (
    <Button
      className={cn(
        // Base
        "group/button relative overflow-hidden",
        "rounded-2xl",
        "px-5 py-3",
        "text-sm font-medium",
        "transition-all duration-300 ease-out",

        // Primary
        variant === "primary" && [
          "border border-primary/20",
          "bg-primary/10",
          "text-primary",
          "hover:-translate-y-0.5",
          "hover:border-primary/40",
          "hover:bg-primary/15",
          "hover:shadow-[0_0_30px_rgba(34,197,94,0.20)]",
        ],

        // Outline
        variant === "outline" && [
          "border border-white/10",
          "bg-white/[0.035]",
          "text-foreground",
          "hover:-translate-y-0.5",
          "hover:border-white/20",
          "hover:bg-white/[0.055]",
        ],

        // Ghost
        variant === "ghost" && [
          "text-muted-foreground",
          "hover:bg-white/[0.05]",
          "hover:text-foreground",
        ],

        className
      )}
      {...props}
    >
      {/* Button-only reflection */}
      <div
        className="
          pointer-events-none
          absolute
          inset-0
          -translate-x-full
          bg-gradient-to-r
          from-transparent
          via-white/[0.08]
          to-transparent
          transition-transform
          duration-700
          group-hover/button:translate-x-full
        "
      />

      <span className="relative z-10 flex items-center justify-center gap-2">
        {children}
      </span>
    </Button>
  );
}