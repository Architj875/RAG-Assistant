"use client";

import { useState } from "react";
import { toast } from "sonner";

import AppShell from "@/components/layout/AppShell";
import Container from "@/components/layout/Container";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import MainPanel from "@/components/layout/MainPanel";
import WorkspaceToolbar from "@/components/layout/WorkspaceToolbar";
import SettingsDialog from "@/components/settings/SettingsDialog";

import { useWorkspace } from "@/hooks/useWorkspace";
import { ChatMessage } from "@/types/api";

import { refreshKnowledgeBase } from "@/services/knowledge.service";

export default function Home() {
  const {
    uploadedFile,
    isReady,
    setUploadedFile,
  } = useWorkspace();

  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [showSettings, setShowSettings] =
    useState(false);

  const [isRefreshing, setIsRefreshing] =
    useState(false);

  // ============================================================
  // CLEAR CHAT
  // ============================================================

  function handleClearChat() {
    setMessages([]);

    toast.success("Chat cleared");
  }

  // ============================================================
  // REFRESH KNOWLEDGE BASE
  // ============================================================

  async function handleRefresh() {
    if (!uploadedFile) {
      toast.error(
        "No document is currently uploaded."
      );

      return;
    }

    if (isRefreshing) {
      return;
    }

    try {
      setIsRefreshing(true);

      toast.loading(
        "Refreshing knowledge base...",
        {
          id: "knowledge-refresh",
        }
      );

      const response =
        await refreshKnowledgeBase();

      if (
        !response.success ||
        !response.data
      ) {
        throw new Error(
          response.error ??
            "Failed to refresh knowledge base."
        );
      }

      // Update workspace with the
      // latest backend information.
      setUploadedFile(response.data);

      // The knowledge base has been rebuilt,
      // so clear answers generated from the
      // previous index.
      setMessages([]);

      toast.success(
        "Knowledge base refreshed successfully.",
        {
          id: "knowledge-refresh",
        }
      );
    } catch (error) {
      console.error(
        "Knowledge base refresh failed:",
        error
      );

      toast.error(
        error instanceof Error
          ? error.message
          : "Failed to refresh knowledge base.",
        {
          id: "knowledge-refresh",
        }
      );
    } finally {
      setIsRefreshing(false);
    }
  }

  // ============================================================
  // SETTINGS
  // ============================================================

  function handleSettings() {
    setShowSettings(
      (previous) => !previous
    );
  }

  function handleCloseSettings() {
    setShowSettings(false);
  }

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <AppShell>
      <Container>
        <div className="flex h-full min-h-0 flex-col">

          {/* =====================================================
              TOP ROW: HEADER + TOOLBAR
          ====================================================== */}

          <div
            className="
              grid
              shrink-0
              grid-cols-[400px_minmax(0,1fr)]
              gap-8
            "
          >

            {/* Header */}

            <div>
              <Header />
            </div>

            {/* Toolbar */}

            <div
              className="
                relative
                z-20
                self-start
                h-fit
                w-full
                rounded-3xl
                border
                border-white/[0.10]
                bg-white/[0.035]
                px-5
                py-2
                shadow-[0_8px_30px_rgba(0,0,0,0.22)]
                backdrop-blur-3xl
                transition-all
                duration-300
                ease-out
                hover:border-primary/30
                hover:bg-white/[0.055]
                hover:shadow-[0_12px_40px_rgba(34,197,94,0.10)]
              "
            >
              <WorkspaceToolbar
                filename={
                  uploadedFile?.filename ??
                  "No document"
                }
                isReady={
                  isReady && !isRefreshing
                }
                onRefresh={
                  handleRefresh
                }
                onClear={
                  handleClearChat
                }
                onSettings={
                  handleSettings
                }
              />
            </div>
          </div>

          {/* =====================================================
              MAIN WORKSPACE
          ====================================================== */}

          <div
            className="
              mt-6
              grid
              min-h-0
              flex-1
              grid-cols-[400px_minmax(0,1fr)]
              gap-8
            "
          >

            {/* Sidebar */}

            <div className="min-h-0">
              <Sidebar />
            </div>

            {/* Chat */}

            <div className="min-h-0 min-w-0">
              <MainPanel
                messages={messages}
                setMessages={setMessages}
              />
            </div>
          </div>

          {/* =====================================================
              SETTINGS DIALOG
          ====================================================== */}

          <SettingsDialog
            open={showSettings}
            onClose={handleCloseSettings}
            embeddingModel={
              uploadedFile?.embedding_model
            }
            vectorStore={
              uploadedFile?.vector_store
            }
          />

        </div>
      </Container>
    </AppShell>
  );
}