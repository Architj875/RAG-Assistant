"use client";

import { useState } from "react";
import { askQuestion } from "@/services/chat.service";

export default function ChatBox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  async function handleAsk() {
    if (!question.trim()) return;

    try {
      const response = await askQuestion({
        question,
      });

      if (response.success && response.data) {
        setAnswer(response.data.answer);
      } else {
        setAnswer(response.error ?? "Unable to generate an answer.");
      }
    } catch (error) {
      console.error(error);
      setAnswer("Something went wrong.");
    }
  }

  return (
    <div className="mt-8 w-full rounded-lg border p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-semibold">
        Ask a Question
      </h2>

      <textarea
        className="w-full rounded border p-3"
        rows={3}
        placeholder="Ask anything about your uploaded document..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        onClick={handleAsk}
        className="mt-4 rounded bg-black px-4 py-2 text-white hover:bg-gray-800"
      >
        Send
      </button>

      {answer && (
        <div className="mt-6 rounded-lg bg-white p-4 shadow">
    <h3 className="mb-2 text-lg font-semibold text-gray-900">
        Answer
    </h3>

    <p className="whitespace-pre-wrap text-gray-800">
        {answer}
    </p>
</div>
      )}
    </div>
  );
}