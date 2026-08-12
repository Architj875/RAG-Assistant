"use client";

import type { Dispatch, SetStateAction } from "react";

import Sidebar from "./Sidebar";
import MainPanel from "./MainPanel";

import { ChatMessage } from "@/types/api";

interface WorkspaceProps {
  messages: ChatMessage[];
  setMessages: Dispatch<
    SetStateAction<ChatMessage[]>
  >;
}

export default function Workspace({
  messages,
  setMessages,
}: WorkspaceProps) {
  return (
    <div className="grid h-full min-h-0 grid-cols-[400px_minmax(0,1fr)] gap-8">

      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <div className="min-h-0">
        <Sidebar />
      </div>

      {/* =====================================================
          CHAT
      ====================================================== */}

      <div className="min-h-0 min-w-0">
        <MainPanel
          messages={messages}
          setMessages={setMessages}
        />
      </div>

    </div>
  );
}