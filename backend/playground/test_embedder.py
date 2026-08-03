from app.loaders.loader_factory import LoaderFactory
from app.processors.chunk_manager import ChunkManager
from app.embeddings.embedding_factory import EmbeddingFactory

def test_embedder(file_path: str):
    # Load
    loader = LoaderFactory.get_loader(file_path)
    documents = loader.load(file_path)

    # Process
    chunks = ChunkManager.process_documents(documents)

    print(f"Generated Chunks: {len(chunks)}")

    # Create embedder
    embedder = EmbeddingFactory.get_embedder()

    # Embed first 3 chunks
    vectors = embedder.embed_documents(chunks[:3])

    print(f"\nGenerated Vectors: {len(vectors)}")
    print(f"Vector Dimension : {len(vectors[0])}")

    print("\nFirst 10 values of vector 1:")
    print(vectors[0][:10])


if __name__ == "__main__":
    file = "data/uploads/IDPL_Employee_Handbook_2026_Bhavnagar.pdf"
    test_embedder(file)