"use client";

import { FormEvent, useState } from "react";
import { ArrowUp } from "lucide-react";

import GlassButton from "@/components/ui/button/GlassButton";

interface Props {
  loading: boolean;
  onSend: (question: string) => void;
}

export default function ChatInput({
  loading,
  onSend,
}: Props) {
  const [value, setValue] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const question = value.trim();

    if (!question || loading) return;

    onSend(question);
    setValue("");
  }

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      const question = value.trim();

      if (!question || loading) return;

      onSend(question);
      setValue("");
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="relative"
    >
      <textarea
        value={value}
        onChange={(event) =>
          setValue(event.target.value)
        }
        onKeyDown={handleKeyDown}
        disabled={loading}
        rows={1}
        placeholder="Ask anything about your document..."
        className="
          min-h-[56px]
          w-full
          resize-none
          rounded-2xl
          border
          border-white/10
          bg-white/[0.04]
          py-4
          pl-5
          pr-16
          text-sm
          text-foreground
          outline-none
          backdrop-blur-xl
          transition-all
          duration-300
          placeholder:text-muted-foreground
          focus:border-primary/30
          focus:bg-white/[0.06]
          focus:shadow-[0_0_30px_rgba(34,197,94,0.08)]
          disabled:cursor-not-allowed
          disabled:opacity-50
        "
      />

      <GlassButton
        type="submit"
        disabled={
          loading || !value.trim()
        }
        className="
          absolute
          bottom-2
          right-2
          h-10
          w-10
          rounded-xl
          p-0
        "
        aria-label="Send message"
      >
        <ArrowUp className="h-4 w-4" />
      </GlassButton>
    </form>
  );
}