from dataclasses import dataclass
from typing import Any

from langchain.agents import create_agent
from langchain.tools import tool

from app.config.settings import settings
from app.utils.logger import logger


@dataclass
class ReactAnswerResult:
    answer: str
    documents: list[Any]


class ReactAgentRAG:

    def __init__(
        self,
        vector_store,
        llm,
    ):
        self.vector_store = vector_store
        self.llm = llm

    def _format_docs(self, documents):
        if not documents:
            return "No relevant document chunks were found."

        parts = []

        for idx, doc in enumerate(documents, start=1):
            source = doc.metadata.get("source", "unknown")
            filename = source.split("/")[-1]
            page = doc.metadata.get("page", "unknown")
            text = doc.page_content.strip()

            parts.append(
                f"""
--- Context {idx} ---
Source: {filename}
Page: {page}

{text}
""".strip()
            )

        return "\n\n".join(parts)

    def _extract_text(self, content):
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            pieces = []
            for item in content:
                if isinstance(item, dict):
                    if "text" in item:
                        pieces.append(str(item["text"]))
                    elif "content" in item:
                        pieces.append(self._extract_text(item["content"]))
                elif hasattr(item, "text"):
                    pieces.append(str(item.text))
            return "\n".join(p for p in pieces if p)

        if isinstance(content, dict):
            for key in ("text", "content"):
                if key in content:
                    return self._extract_text(content[key])
            return str(content)

        return str(content)

    def _attach_citation_ids(self, docs):
        for idx, doc in enumerate(docs, start=1):
            doc.metadata["citation_id"] = idx

    def ask(self, question: str) -> ReactAnswerResult:
        logger.info("React agent question: %s", question)

        retrieved_documents = []

        @tool
        def retrieve_docs(query: str) -> str:
            """Retrieve the most relevant document chunks for a factual query."""
            docs = self.vector_store.similarity_search(
                query=query,
                k=settings.TOP_K,
            )
            self._attach_citation_ids(docs)
            retrieved_documents.extend(docs)
            logger.info("React tool retrieve_docs called with: %s", query)
            return self._format_docs(docs)

        @tool
        def retrieve_summary(query: str) -> str:
            """Retrieve a summary-oriented context for overview or policy-style questions."""
            docs = self.vector_store.summary_search(
                query=query,
                k=settings.TOP_K,
            )
            self._attach_citation_ids(docs)
            retrieved_documents.extend(docs)
            logger.info("React tool retrieve_summary called with: %s", query)
            return self._format_docs(docs)

        tools = [retrieve_docs, retrieve_summary]

        base_llm = getattr(self.llm, "llm", self.llm)

        agent = create_agent(
            model=base_llm,
            tools=tools,
            system_prompt="""
You are a document-grounded assistant.

Use the tools when the user asks for factual answers or needs evidence.
If the user is asking for a summary or overview, prefer retrieve_summary.
If the user asks a specific fact or rule, prefer retrieve_docs.
If the tool output is weak or incomplete, do one more search with a clearer query.
Answer using only the retrieved context.
If the context does not contain the answer, say so clearly.
Do not invent citations. The final answer should be clean prose.
When using information from retrieved context, cite it using the numbered reference format [1], [2], etc.
""",
        )

        result = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": question}
                ]
            }
        )

        messages = result.get("messages", [])
        if not messages:
            return ReactAnswerResult(
                answer="No response generated.",
                documents=retrieved_documents,
            )

        final_answer = self._extract_text(messages[-1].content)

        if retrieved_documents and "[1]" not in final_answer:
            final_answer = f"{final_answer} [1]"

        return ReactAnswerResult(
            answer=final_answer,
            documents=retrieved_documents,
        )