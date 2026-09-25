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

  function handleClearChat() {
    setMessages([]);
    toast.success("Chat cleared");
  }

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

      setUploadedFile(response.data);
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

  function handleSettings() {
    setShowSettings(
      (previous) => !previous
    );
  }

  function handleCloseSettings() {
    setShowSettings(false);
  }

  return (
    <AppShell>
      <Container>
        <div className="flex h-full min-h-0 flex-col">
          <div
            className="
              grid
              shrink-0
              grid-cols-[400px_minmax(0,1fr)]
              gap-8
            "
          >
            <div>
              <Header />
            </div>

            <div
              className="
                relative
                z-20
                self-start
                h-fit
                w-full
                rounded-3xl
                border
                border-border
                bg-card/80
                px-5
                py-2
                shadow-[0_8px_30px_rgba(15,23,42,0.08)]
                backdrop-blur-3xl
                transition-all
                duration-300
                ease-out
                hover:border-primary/30
                hover:bg-secondary/80
                hover:shadow-[0_12px_40px_rgba(34,197,94,0.08)]
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
            <div className="min-h-0">
              <Sidebar />
            </div>

            <div className="min-h-0 min-w-0">
              <MainPanel
                messages={messages}
                setMessages={setMessages}
              />
            </div>
          </div>

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