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
    <div className="shrink-0 border-t border-white/10 bg-black/10 px-6 py-5 backdrop-blur-xl">
      <div className="mx-auto w-full max-w-4xl">
        <ChatInput
          loading={loading}
          onSend={onSend}
        />

        <p className="mt-2 text-center text-[11px] text-muted-foreground">
          AI responses are generated from your uploaded knowledge base.
        </p>
      </div>
    </div>
  );
}