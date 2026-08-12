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
    <div className="flex min-h-full flex-col items-center justify-center px-6 py-10 text-center">

      {/* AI Icon */}
      <div
        className="
          relative
          flex
          h-20
          w-20
          items-center
          justify-center
          rounded-[28px]
          border
          border-primary/15
          bg-primary/[0.07]
          shadow-[0_0_45px_rgba(34,197,94,0.10)]
        "
      >
        <div
          className="
            absolute
            inset-2
            rounded-[20px]
            border
            border-primary/10
            bg-white/[0.025]
          "
        />

        <Sparkles className="relative z-10 h-8 w-8 text-primary" />
      </div>

      {/* Heading */}
      <h2 className="mt-6 text-xl font-semibold tracking-tight text-foreground">
        Start a Conversation
      </h2>

      {/* Description */}
      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-muted-foreground">
        Ask questions about your uploaded document and get answers
        grounded in your knowledge base.
      </p>

      {/* Suggestions */}
      <div className="mt-7 grid w-full max-w-[820px] gap-3 sm:grid-cols-3">
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
                border-white/[0.08]
                bg-white/[0.025]
                p-4
                text-left
                transition-all
                duration-300
                hover:-translate-y-0.5
                hover:border-primary/20
                hover:bg-primary/[0.05]
                hover:shadow-[0_0_30px_rgba(34,197,94,0.08)]
                focus:outline-none
                focus:ring-1
                focus:ring-primary/30
              "
            >
              <div
                className="
                  flex
                  h-9
                  w-9
                  items-center
                  justify-center
                  rounded-xl
                  border
                  border-white/[0.08]
                  bg-white/[0.035]
                  transition-all
                  duration-300
                  group-hover:border-primary/20
                  group-hover:bg-primary/10
                "
              >
                <Icon className="h-4 w-4 text-primary transition-transform duration-300 group-hover:scale-110" />
              </div>

              <p className="mt-3 text-sm font-medium text-foreground">
                {suggestion.label}
              </p>

              <p className="mt-1 text-xs text-muted-foreground">
                Ask the assistant
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}