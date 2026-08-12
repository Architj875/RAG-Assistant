"use client";

import { RefObject } from "react";

import { ChatMessage } from "@/types/api";

import ChatEmptyState from "./ChatEmptyState";
import MessageList from "./MessageList";
import TypingIndicator from "./TypingIndicator";

interface Props {
  isReady: boolean;
  loading: boolean;
  messages: ChatMessage[];
  messagesEndRef: RefObject<HTMLDivElement | null>;
  onSuggestionClick: (question: string) => void;
}

export default function MessageArea({
  isReady,
  loading,
  messages,
  messagesEndRef,
  onSuggestionClick,
}: Props) {
  if (!isReady) {
    return (
      <div className="flex min-h-0 flex-1 items-center justify-center overflow-hidden px-6">
        <div className="max-w-md text-center">
          <p className="text-sm text-muted-foreground">
            Upload a document to start chatting with your knowledge base.
          </p>
        </div>
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="min-h-0 flex-1 overflow-y-auto">
        <ChatEmptyState
          onSuggestionClick={onSuggestionClick}
        />
      </div>
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto px-7 py-6">
      <div className="mx-auto w-full max-w-4xl">
        <MessageList messages={messages} />

        {loading && (
          <div className="mt-6">
            <TypingIndicator />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}