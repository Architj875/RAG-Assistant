from app.llms.llm_factory import LLMFactory

def test_llm():
    print("Initializing LLM...")

    llm = LLMFactory.get_llm()
    print("LLM initialized successfully!")
    question = "Explain Retrieval-Augmented Generation in simple terms."
    print(f"\nQuestion:\n{question}")
    print("\nGenerating response...\n")
    answer = llm.invoke(question)

    print("Response:\n")
    print(answer)

if __name__ == "__main__":
    test_llm() 