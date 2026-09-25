"use client";

import { FormEvent, useState } from "react";
import { ArrowUp } from "lucide-react";

interface Props {
  loading: boolean;
  onSend: (question: string) => void;
}

export default function ChatInput({
  loading,
  onSend,
}: Props) {
  const [value, setValue] = useState("");

  function submitMessage() {
    const question = value.trim();

    if (!question || loading) return;

    onSend(question);
    setValue("");
  }

  function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    submitMessage();
  }

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      submitMessage();
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="relative w-full"
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
          min-h-14
          w-full
          resize-none
          rounded-2xl
          border
          border-border
          bg-secondary/40
          py-4
          pl-5
          pr-16
          text-sm
          leading-6
          text-foreground
          outline-none
          backdrop-blur-xl
          transition-all
          duration-300
          placeholder:text-muted-foreground
          focus:border-primary/30
          focus:bg-secondary/80
          focus:shadow-[0_0_30px_rgba(34,197,94,0.08)]
          disabled:cursor-not-allowed
          disabled:opacity-50
        "
      />

      <button
        type="submit"
        disabled={loading || !value.trim()}
        aria-label="Send message"
        className="
          absolute
          right-2
          top-[calc(50%-5px)]
          flex
          h-10
          w-10
          -translate-y-1/2
          items-center
          justify-center
          rounded-xl
          border
          border-primary/20
          bg-primary/10
          p-0
          text-primary
          transition-all
          duration-300
          hover:border-primary/40
          hover:bg-primary/15
          hover:shadow-[0_0_20px_rgba(34,197,94,0.18)]
          disabled:pointer-events-none
          disabled:opacity-40
        "
      >
        <ArrowUp className="h-4 w-4 shrink-0" />
      </button>
    </form>
  );
}