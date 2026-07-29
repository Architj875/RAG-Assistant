from app.llms.gemini_llm import GeminiLLM

class LLMFactory:

    @staticmethod
    def get_llm(llm_type: str = "gemini"):

        if llm_type.lower() == "gemini":
            return GeminiLLM()

        raise ValueError(
            f"Unsupported LLM: {llm_type}"
        )