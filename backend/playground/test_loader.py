from pathlib import Path

from app.loaders.loader_factory import LoaderFactory


def test_file(file_path: str):
    loader = LoaderFactory.get_loader(file_path)

    documents = loader.load(file_path)

    # Debug Information
    print("\n===== DEBUG INFORMATION =====")
    print(f"Type of documents: {type(documents)}")
    print(f"Type of first document: {type(documents[0])}")

    doc = documents[0]

    print(f"Content Length: {len(doc.page_content)}")
    print(f"First 300 Characters (repr):\n{repr(doc.page_content[:300])}")

    print("\n=============================\n")

    print("=" * 60)
    print(f"File: {Path(file_path).name}")
    print(f"Documents Loaded: {len(documents)}")
    print("=" * 60)

    for index, document in enumerate(documents[:3], start=1):  # print only the first 3 documents for brevity
        print(f"\nDocument {index}")
        print("=" * 40)

        print("Metadata:")
        print(document.metadata)

        print("\nContent Preview:")
        print(repr(document.page_content[:300]))
        print("-" * 40)


if __name__ == "__main__":
    file = "data/uploads/IDPL_Employee_Handbook_2026_Bhavnagar.pdf"
    test_file(file)