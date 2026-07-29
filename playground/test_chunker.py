from pathlib import Path

from app.loaders.loader_factory import LoaderFactory
from app.processors.cleaner import TextCleaner
from app.processors.chunker import TextChunker

def test_chunker(file_path: str):
    # Load
    loader = LoaderFactory.get_loader(file_path)
    documents = loader.load(file_path)

    # Clean
    cleaned_documents = TextCleaner.clean_documents(documents)

    # Chunk
    chunks = TextChunker.recursive_chunk_documents(
        cleaned_documents,
        chunk_size=500,
        chunk_overlap=100
    )

    print("=" * 60)
    print(f"File: {Path(file_path).name}")
    print("=" * 60)

    print(f"Original Documents: {len(documents)}")
    print(f"Clean Documents: {len(cleaned_documents)}")
    print(f"Generated Chunks: {len(chunks)}")

    print("\n")

    # Display first 3 chunks
    for index, chunk in enumerate(chunks[:3], start=1):
        print("=" * 60)
        print(f"Chunk {index}")
        print("=" * 60)

        print("Metadata:")
        print(chunk.metadata)

        print("\nCharacters:")
        print(len(chunk.page_content))

        print("\nContent:")
        print(repr(chunk.page_content))

        print("\n")

if __name__ == "__main__":
    file = "data/uploads/IDPL_Employee_Handbook_2026_Bhavnagar.pdf"
    test_chunker(file)