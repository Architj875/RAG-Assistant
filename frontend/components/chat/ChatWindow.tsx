"use client";

import { useEffect, useRef, useState } from "react";

import { askQuestion } from "@/services/chat.service";
import { ChatMessage } from "@/types/api";
import { useWorkspace } from "@/hooks/useWorkspace";

import GlassCard from "@/components/ui/card/GlassCard";

import ChatHeader from "./ChatHeader";
import MessageArea from "./MessageArea";
import ChatComposer from "./ChatComposer";

interface ChatWindowProps {
  messages: ChatMessage[];
  setMessages: React.Dispatch<
    React.SetStateAction<ChatMessage[]>
  >;
}

export default function ChatWindow({
  messages,
  setMessages,
}: ChatWindowProps) {
  const { isReady } = useWorkspace();

  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<"rag" | "react">("rag");

  const messagesEndRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading]);

  async function handleSend(question: string) {
    const userMessage: ChatMessage = {
      role: "user",
      content: question,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setLoading(true);

    try {
      const response = await askQuestion({
        question,
        mode,
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content:
          response.data?.answer ??
          "Unable to generate an answer.",
        sources:
          response.data?.sources ?? [],
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Something went wrong while generating the answer.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <GlassCard className="h-full">
      <div className="flex h-full min-h-0 flex-col">
        <ChatHeader
          mode={mode}
          setMode={setMode}
        />

        <MessageArea
          isReady={isReady}
          loading={loading}
          messages={messages}
          messagesEndRef={messagesEndRef}
          onSuggestionClick={handleSend}
        />

        <ChatComposer
          loading={loading}
          onSend={handleSend}
        />
      </div>
    </GlassCard>
  );
}