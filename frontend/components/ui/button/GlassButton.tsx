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
        "group relative overflow-hidden",
        "rounded-2xl",
        "px-5 py-3",
        "text-sm font-medium",
        "transition-all duration-300",

        variant === "primary" && [
          "border border-primary/20",
          "bg-primary/10",
          "text-primary",
          "hover:border-primary/40",
          "hover:bg-primary/15",
          "hover:shadow-[0_0_30px_rgba(34,197,94,0.25)]",
        ],

        variant === "outline" && [
          "border border-white/10",
          "bg-white/[0.04]",
          "text-foreground",
          "hover:border-primary/20",
          "hover:bg-white/[0.06]",
        ],

        variant === "ghost" && [
          "text-muted-foreground",
          "hover:bg-white/[0.05]",
          "hover:text-foreground",
        ],

        className
      )}
      {...props}
    >
      {/* hover shine */}
      <div
        className="
          absolute
          inset-0
          -translate-x-full
          bg-gradient-to-r
          from-transparent
          via-white/10
          to-transparent
          transition-transform
          duration-700
          group-hover:translate-x-full
        "
      />

      <span className="relative z-10 flex items-center gap-2">
        {children}
      </span>
    </Button>
  );
}