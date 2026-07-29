from langchain_core.documents import Document


class PromptBuilder:

    @staticmethod
    def build(documents: list[Document], question: str) -> str:

        context = "\n\n".join(
            doc.page_content for doc in documents
        )

        prompt = f"""
You are an intelligent assistant.

Answer teh user's question ONLY using the provided context.

If the answer is not available in the context, reply:

"I couldn't find that information in the provided documents."

Context:
---------
{context}
---------

Question:
{question}

Answer:
"""
        return prompt.strip()