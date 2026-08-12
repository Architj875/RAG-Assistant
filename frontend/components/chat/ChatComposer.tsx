"use client";

import ChatInput from "./ChatInput";

interface Props {
  loading: boolean;
  onSend: (question: string) => void;
}

export default function ChatComposer({
  loading,
  onSend,
}: Props) {
  return (
    <div className="px-5 pb-5 pt-3">
      <ChatInput
        loading={loading}
        onSend={onSend}
      />

      <p className="mt-2 text-center text-[11px] text-muted-foreground/70">
        AI responses are generated from your uploaded knowledge base.
      </p>
    </div>
  );
}