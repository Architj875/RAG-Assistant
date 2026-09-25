from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings
from app.llms.base_llm import BaseLLM


class GeminiLLM(BaseLLM):

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    def _normalize_content(self, content):
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    if "text" in item:
                        parts.append(str(item["text"]))
                    elif "content" in item:
                        parts.append(self._normalize_content(item["content"]))
                elif hasattr(item, "text"):
                    parts.append(str(item.text))
            return "\n".join(p for p in parts if p)

        if isinstance(content, dict):
            for key in ("text", "content"):
                if key in content:
                    return self._normalize_content(content[key])
            return str(content)

        if hasattr(content, "text"):
            return str(content.text)

        return str(content)

    def invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return self._normalize_content(response.content)