"use client";

import { ChatMessage as ChatMessageType } from "@/types/api";

import ChatMessage from "./ChatMessage";

interface Props {
  messages: ChatMessageType[];
}

export default function MessageList({
  messages,
}: Props) {
  return (
    <div className="space-y-6">
      {messages.map((message, index) => (
        <ChatMessage
          key={`${message.role}-${index}`}
          message={message}
        />
      ))}
    </div>
  );
}