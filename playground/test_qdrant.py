from app.loaders.loader_factory import LoaderFactory
from app.processors.chunk_manager import ChunkManager
from app.vectorstores.vectorstore_factory import VectorStoreFactory


def test_qdrant(file_path: str):

    print("Loading document...")

    loader = LoaderFactory.get_loader(file_path)
    documents = loader.load(file_path)

    print(f"Loaded {len(documents)} documents")

    print("\nProcessing document...")

    chunks = ChunkManager.process_documents(documents)

    print(f"Generated {len(chunks)} chunks")

    print("\nCreating Qdrant store...")

    vector_store = VectorStoreFactory.get_vector_store()

    print("\nResetting collection...")

    vector_store.recreate_collection()

    print("Adding documents to Qdrant...")

    vector_store.add_documents(chunks)

    print("Documents indexed successfully!")

    print("\nSearching...")

    results = vector_store.similarity_search(
        query="What is the notice period?",
        k=3,
    )

    print("\nTop Results:\n")

    for index, doc in enumerate(results, start=1):
        print(f"Result {index}")
        print("=" * 50)
        print(doc.page_content[:500])

        print("\nMetadata:")
        print(doc.metadata)
        print()


if __name__ == "__main__":
    file = "data/uploads/IDPL_Employee_Handbook_2026_Bhavnagar.pdf"
    test_qdrant(file)