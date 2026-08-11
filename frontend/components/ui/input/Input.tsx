import {
  forwardRef,
  TextareaHTMLAttributes,
} from "react";

import { cn } from "@/lib/utils";

type InputProps =
  TextareaHTMLAttributes<HTMLTextAreaElement>;

const Input = forwardRef<
  HTMLTextAreaElement,
  InputProps
>(({ className, ...props }, ref) => {
  return (
    <textarea
      ref={ref}
      className={cn(
        "w-full",
        "rounded-2xl",
        "border border-border",
        "bg-background",
        "px-4 py-3",

        "resize-none",
        "outline-none",

        "transition-all duration-300",

        "focus:border-primary",
        "focus:ring-2",
        "focus:ring-primary/20",

        "disabled:cursor-not-allowed",
        "disabled:opacity-50",

        className
      )}
      {...props}
    />
  );
});

Input.displayName = "Input";

export default Input;