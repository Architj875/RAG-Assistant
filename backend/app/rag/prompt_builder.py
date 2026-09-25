from langchain_core.documents import Document


class PromptBuilder:

    @staticmethod
    def build(
        documents: list[Document],
        question: str,
        query_type: str = "factual",
    ) -> str:

        # ==================================================
        # BUILD DOCUMENT CONTEXT
        # ==================================================

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = document.metadata

            page = metadata.get(
                "page"
            )

            source = metadata.get(
                "source",
                "Unknown source",
            )

            filename = source.split("/")[-1]

            chunk_id = metadata.get(
                "chunk_id",
                "Unknown",
            )

            citation_id = metadata.get(
                "citation_id"
            )

            context_parts.append(
                f"""
--- Document Chunk {index} ---

Citation ID: [{citation_id}]

Source: {filename}
Page: {page if page is not None else "Unknown"}
Chunk ID: {chunk_id}

{document.page_content}
""".strip()
            )

        context = "\n\n".join(
            context_parts
        )

        # ==================================================
        # QUERY-SPECIFIC INSTRUCTIONS
        # ==================================================

        if query_type == "document_summary":

            task_instruction = """
The user is asking for a broad summary.

Summarize the important information that is actually
supported by the retrieved document context.

Organize the answer into logical sections or bullet
points when useful.

Do not assume that the retrieved chunks represent the
entire document.

Only summarize information that is present in the
provided context.
"""

        elif query_type == "section_summary":

            task_instruction = """
The user is asking for a summary related to a specific
topic.

Identify the relevant information about that topic
from the retrieved context.

Combine related information across multiple chunks
when appropriate.

Stay focused on the requested topic.

Do not introduce information that is not supported by
the retrieved context.
"""

        else:

            task_instruction = """
The user is asking a factual or specific question.

Answer directly when the requested information is
clearly supported by the document context.

If the question is ambiguous, identify the different
plausible meanings that are actually represented in the
retrieved context instead of silently choosing one.

If the document provides related information but does
not provide the exact detail requested, explain that
limitation and provide the related information that is
supported.
"""

        # ==================================================
        # FINAL PROMPT
        # ==================================================

        prompt = f"""
You are a document-grounded question-answering assistant.

You answer questions using ONLY the information contained
in the DOCUMENT CONTEXT below.

The documents can be ANY type of document.

They may contain policies, manuals, reports, contracts,
technical documentation, specifications, employee
handbooks, research documents, guides, or other content.

Do not assume a particular document type.

==================================================
QUERY TYPE
==================================================

{query_type}

==================================================
TASK
==================================================

{task_instruction}

==================================================
CRITICAL DOCUMENT-GROUNDING RULES
==================================================

1. Use ONLY the provided document context.

2. Do NOT use outside knowledge.

3. Do NOT invent information.

4. Do NOT assume that a value or rule exists merely
because it would normally make sense.

5. Do NOT silently convert one unit or time period into
another unless the document explicitly provides the
necessary relationship.

6. Do NOT turn an annual entitlement into a monthly,
weekly, or daily entitlement unless the document
supports that interpretation.

7. Do NOT infer missing limits, quantities, dates,
conditions, permissions, or requirements.

8. If the user asks for information that is NOT stated
in the document, clearly say that the document does not
specify that information.

9. If related information is available but the exact
requested detail is not specified, explain that clearly.

10. Do not contradict the document context.

11. Keep answers concise unless multiple categories
require explanation.

==================================================
CITATIONS
==================================================

Every factual claim based on the retrieved documents
should include a citation.

Use ONLY the Citation IDs provided in the context.

Use exactly this format:

[1]
[2]
[3]

Example:

Employees earn 1 EL for every 20 working days. [1]

Another example:

Sick Leave is 7 days per year. [2]

If a statement is supported by multiple chunks:

The policy contains several leave categories. [1] [2]

IMPORTANT:

- Never invent a citation number.
- Only use citation IDs present in the context.
- Put citations immediately after the claim they support.
- Do not create a separate Sources section.
- Do not list citations at the end of the entire answer.
- Do not cite unsupported information.

==================================================
DOCUMENT CONTEXT
==================================================

{context}

==================================================
USER QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
""".strip()

        return prompt