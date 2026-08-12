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
      className={`flex gap-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {/* Assistant avatar */}
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-primary/20 bg-primary/10 shadow-[0_0_18px_rgba(34,197,94,0.08)]">
          <Bot className="h-4 w-4 text-primary" />
        </div>
      )}

      <div
        className={`min-w-0 max-w-[80%] ${
          isUser
            ? "rounded-2xl rounded-br-md border border-primary/15 bg-primary/[0.08] px-5 py-4"
            : "rounded-2xl border border-white/[0.06] bg-white/[0.025] px-5 py-4"
        }`}
      >
        {/* Message */}
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
            prose-p:my-2

            prose-strong:text-foreground

            prose-li:text-foreground
            prose-li:my-1

            prose-a:text-primary
            prose-a:no-underline
            hover:prose-a:underline

            prose-code:text-primary

            prose-pre:overflow-x-auto
            prose-pre:border
            prose-pre:border-white/10
            prose-pre:bg-black/30
            prose-pre:rounded-xl

            prose-blockquote:border-primary/30
            prose-blockquote:text-muted-foreground
          "
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Sources */}
        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (
            <div className="mt-6 border-t border-white/[0.06] pt-4">
              <p className="mb-3 text-[10px] font-medium uppercase tracking-[0.2em] text-muted-foreground">
                Sources
              </p>

              <div className="space-y-2">
                {message.sources.map((source, index) => (
                  <SourceCard
                    key={`${source.filename}-${source.page}-${index}`}
                    source={source}
                  />
                ))}
              </div>
            </div>
          )}
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04]">
          <User className="h-4 w-4 text-muted-foreground" />
        </div>
      )}
    </div>
  );
}