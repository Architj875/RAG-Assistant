from app.services.document_service import DocumentService


def test_qdrant(file_path: str):

    service = DocumentService()

    total_chunks = service.ingest_document(file_path)

    print(f"Successfully indexed {total_chunks} chunks.")


if __name__ == "__main__":
    file = "data/uploads/IDPL_Employee_Handbook_2026_Bhavnagar.pdf"

    test_qdrant(file)