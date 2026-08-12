"use client";

import { Dispatch, SetStateAction } from "react";

import ChatWindow from "../chat/ChatWindow";

import { ChatMessage } from "@/types/api";

interface MainPanelProps {
  messages: ChatMessage[];
  setMessages: Dispatch<SetStateAction<ChatMessage[]>>;
}

export default function MainPanel({
  messages,
  setMessages,
}: MainPanelProps) {
  return (
    <div className="h-full min-h-0 min-w-0">
      <ChatWindow
        messages={messages}
        setMessages={setMessages}
      />
    </div>
  );
}