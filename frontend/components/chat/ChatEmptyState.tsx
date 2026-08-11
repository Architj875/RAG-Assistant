"use client";

import {
  FileText,
  List,
  MessageCircleQuestion,
  Sparkles,
} from "lucide-react";

interface Props {
  onSuggestionClick: (question: string) => void;
}

const suggestions = [
  {
    label: "Summarize this document",
    icon: FileText,
  },
  {
    label: "What are the key points?",
    icon: List,
  },
  {
    label: "What should I know from this?",
    icon: MessageCircleQuestion,
  },
];

export default function ChatEmptyState({
  onSuggestionClick,
}: Props) {
  return (
    <div className="flex min-h-full items-center justify-center px-6 py-10">
      <div className="w-full max-w-2xl text-center">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-primary/20 bg-primary/10 shadow-[0_0_40px_rgba(34,197,94,0.08)]">
          <Sparkles className="h-7 w-7 text-primary" />
        </div>

        <h2 className="text-2xl font-semibold tracking-tight">
          Start a Conversation
        </h2>

        <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-muted-foreground">
          Ask questions about your uploaded document and get answers
          grounded in your knowledge base.
        </p>

        <div className="mt-8 grid gap-3 sm:grid-cols-3">
          {suggestions.map((suggestion) => {
            const Icon = suggestion.icon;

            return (
              <button
                key={suggestion.label}
                type="button"
                onClick={() =>
                  onSuggestionClick(suggestion.label)
                }
                className="
                  group
                  rounded-2xl
                  border
                  border-white/10
                  bg-white/[0.03]
                  p-4
                  text-left
                  transition-all
                  duration-300
                  hover:-translate-y-0.5
                  hover:border-primary/20
                  hover:bg-primary/[0.05]
                  hover:shadow-[0_0_30px_rgba(34,197,94,0.08)]
                "
              >
                <Icon className="h-4 w-4 text-primary transition-transform duration-300 group-hover:scale-110" />

                <p className="mt-3 text-sm font-medium">
                  {suggestion.label}
                </p>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}