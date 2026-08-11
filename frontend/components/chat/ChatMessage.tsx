"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Bot, User } from "lucide-react";

import { ChatMessage as ChatMessageType } from "@/types/api";

import SourceCard from "./SourceCard";

interface Props {
  message: ChatMessageType;
}

export default function ChatMessage({
  message,
}: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex gap-4 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-primary/20 bg-primary/10">
          <Bot className="h-4 w-4 text-primary" />
        </div>
      )}

      <div
        className={`min-w-0 max-w-[80%] ${
          isUser
            ? "rounded-2xl bg-primary/10 px-5 py-4"
            : ""
        }`}
      >
        <div
          className="
            prose
            prose-invert
            max-w-none
            text-sm
            leading-7
            prose-headings:font-semibold
            prose-headings:text-foreground
            prose-p:text-foreground
            prose-strong:text-foreground
            prose-li:text-foreground
            prose-a:text-primary
            prose-code:text-primary
            prose-pre:border
            prose-pre:border-white/10
            prose-pre:bg-black/30
          "
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (
            <div className="mt-5">
              <p className="mb-3 text-xs font-medium uppercase tracking-[0.18em] text-muted-foreground">
                Sources
              </p>

              <div className="space-y-2">
                {message.sources.map(
                  (source, index) => (
                    <SourceCard
                      key={`${source.filename}-${source.page}-${index}`}
                      source={source}
                    />
                  )
                )}
              </div>
            </div>
          )}
      </div>

      {isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04]">
          <User className="h-4 w-4 text-muted-foreground" />
        </div>
      )}
    </div>
  );
}