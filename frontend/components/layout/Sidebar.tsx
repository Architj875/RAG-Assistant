"use client";

import UploadForm from "../knowledge/UploadForm";
import KnowledgeCard from "../knowledge/KnowledgeCard";
import KnowledgeStats from "../knowledge/knowledgeStats";
import KnowledgeActions from "../knowledge/knowledgeActions";

import GlassCard from "../ui/card/GlassCard";

import { useWorkspace } from "@/hooks/useWorkspace";

export default function Sidebar() {
  const { uploadedFile } = useWorkspace();

  return (
    <GlassCard className="h-full">
      <div className="flex h-full min-h-0 flex-col p-6">

        {/* Upload / Current Document */}
        {!uploadedFile ? (
          <UploadForm />
        ) : (
          <KnowledgeCard />
        )}

        {/* Statistics */}
        {uploadedFile && (
          <div className="mt-6">
            <KnowledgeStats />
          </div>
        )}

        {/* Push actions to bottom */}
        <div className="flex-1" />

        {/* Actions */}
        <KnowledgeActions />

      </div>
    </GlassCard>
  );
}