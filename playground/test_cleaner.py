from pathlib import Path

from app.loaders.loader_factory import LoaderFactory
from app.processors.cleaner import TextCleaner

def test_cleaner(file_path: str):
    # Load documents
    loader = LoaderFactory.get_loader(file_path)
    documents = loader.load(file_path)

    # Clean documents
    cleaned_documents = TextCleaner.clean_documents(documents)

    print("=" * 60)
    print(f"File: {Path(file_path).name}")
    print("=" * 60)

    print(f"Original Documents : {len(documents)}")
    print(f"Cleaned Documents : {len(cleaned_documents)}")

    print("\n")

    original = documents[0]
    cleaned = cleaned_documents[0]

    print("=" * 60)
    print("ORIGINAL TEXT")
    print("=" * 60)
    print(repr(original.page_content[:500]))  # Print first 500 characters of original text

    print("\n")

    print("=" * 60)
    print("CLEANED TEXT")
    print("=" * 60)
    print(repr(cleaned.page_content[:500]))  # Print first 500 characters of cleaned text

    print("\n")

    print("=" * 60)
    print("METADATA")
    print("=" * 60)
    print(cleaned.metadata)

if __name__ == "__main__":
    file = "data/uploads/IDPL_Employee_Handbook_2026_Bhavnagar.pdf"
    test_cleaner(file)