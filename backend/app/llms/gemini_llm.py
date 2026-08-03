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
    def invoke(self, prompt: str) -> str:

        response = self.llm.invoke(prompt)

        if isinstance(response.content, str):
            return response.content

        if isinstance(response.content, list):
            return "\n".join(
                block.get("text", "")
                for block in response.content
                if isinstance(block, dict)
            )
        return str(response.content)