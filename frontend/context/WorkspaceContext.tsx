"use client";

import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type { UploadData } from "@/types/api";

interface WorkspaceContextValue {
  // Global Workspace State
  uploadedFile: UploadData | null;
  isReady: boolean;
  isUploading: boolean;
  uploadStage: string;

  // Actions
  setUploadedFile: (
    file: UploadData | null
  ) => void;

  setIsReady: (
    ready: boolean
  ) => void;

  setIsUploading: (
    uploading: boolean
  ) => void;

  setUploadStage: (
    stage: string
  ) => void;

  clearWorkspace: () => void;
}

const WorkspaceContext =
  createContext<WorkspaceContextValue | undefined>(
    undefined
  );

interface WorkspaceProviderProps {
  children: ReactNode;
}

export function WorkspaceProvider({
  children,
}: WorkspaceProviderProps) {
  const [uploadedFile, setUploadedFile] =
    useState<UploadData | null>(null);

  const [isReady, setIsReady] =
    useState(false);

  const [isUploading, setIsUploading] =
    useState(false);

  const [uploadStage, setUploadStage] =
    useState("Ready");

  function clearWorkspace() {
    setUploadedFile(null);
    setIsReady(false);
    setIsUploading(false);
    setUploadStage("Ready");
  }

  const value = useMemo(
    () => ({
      uploadedFile,
      isReady,
      isUploading,
      uploadStage,

      setUploadedFile,
      setIsReady,
      setIsUploading,
      setUploadStage,

      clearWorkspace,
    }),
    [
      uploadedFile,
      isReady,
      isUploading,
      uploadStage,
    ]
  );

  return (
    <WorkspaceContext.Provider value={value}>
      {children}
    </WorkspaceContext.Provider>
  );
}

export function useWorkspace() {
  const context =
    useContext(WorkspaceContext);

  if (!context) {
    throw new Error(
      "useWorkspace must be used within a WorkspaceProvider."
    );
  }

  return context;
}