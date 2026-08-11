import { ComponentProps } from "react";

import Badge from "./badge";
import { cn } from "@/lib/utils";

type Props =
  ComponentProps<typeof Badge>;

export default function GlassBadge({
  className,
  children,
  ...props
}: Props) {
  return (
    <Badge
      className={cn(
        "border border-primary/20",
        "bg-primary/10",
        "text-xs font-medium text-primary",
        "backdrop-blur-xl",
        className
      )}
      {...props}
    >
      {children}
    </Badge>
  );
}