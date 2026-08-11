import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type BadgeProps =
  HTMLAttributes<HTMLDivElement>;

export default function Badge({
  className,
  children,
  ...props
}: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center gap-2 rounded-full px-3 py-1",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}