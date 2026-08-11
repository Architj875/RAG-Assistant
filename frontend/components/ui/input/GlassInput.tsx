import { ComponentProps } from "react";

import Input from "./Input";
import { cn } from "@/lib/utils";

type Props = ComponentProps<typeof Input>;

export default function GlassInput({
  className,
  ...props
}: Props) {
  return (
    <Input
      className={cn(
        "rounded-2xl",
        "border border-white/10",
        "bg-white/[0.04]",
        "backdrop-blur-xl",
        "transition-all duration-300",
        "placeholder:text-muted-foreground",
        "focus:border-primary/30",
        "focus:bg-white/[0.06]",
        "focus:outline-none",
        "focus:ring-0",
        "focus:shadow-[0_0_30px_rgba(34,197,94,0.08)]",
        className
      )}
      {...props}
    />
  );
}