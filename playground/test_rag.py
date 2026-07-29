from app.rag.rag_pipeline import RAGPipeline


def test_rag():

    print("Initializing RAG Pipeline...\n")

    rag = RAGPipeline()

    print("RAG Pipeline Ready!\n")

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit" :
            print("\nGoodbye!")
            break

        print("\nThinking...\n")

        answer = rag.ask(question)

        print("=" * 80)
        print(answer)
        print("=" * 80)

if __name__ == "__main__":
    test_rag()