"use client";

import {
  RefreshCw,
  Trash2,
} from "lucide-react";

import GlassButton from "@/components/ui/button/GlassButton";
import { useWorkspace } from "@/hooks/useWorkspace";

export default function KnowledgeActions() {
  const {
    setUploadedFile,
    setIsReady,
    setUploadStage,
  } = useWorkspace();

  function handleReplace() {
    // We'll connect this to UploadForm later
    console.log("Replace document");
  }

  function handleRemove() {
    setUploadedFile(null);
    setIsReady(false);
    setUploadStage("Ready");
  }

  return (
    <div className="space-y-3 border-t border-white/10 pt-6">
      <GlassButton
        onClick={handleReplace}
        className="w-full justify-center"
      >
        <RefreshCw className="mr-2 h-4 w-4" />
        Replace Document
      </GlassButton>

      <GlassButton
        variant="outline"
        onClick={handleRemove}
        className="w-full justify-center"
      >
        <Trash2 className="mr-2 h-4 w-4" />
        Remove Document
      </GlassButton>
    </div>
  );
}