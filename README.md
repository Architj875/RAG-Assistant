# 🤖 RAG Assistant

A modern and modular Retrieval-Augmented Generation (RAG) application built with Python, LangChain, Qdrant, Google Gemini, and Hugging Face embeddings. This project demonstrates how to ingest documents, retrieve relevant context semantically, and generate grounded answers using LLMs.

## ✨ Overview

RAG Assistant is designed to help you build AI applications that can answer questions from your own documents. The system combines:

- document ingestion from multiple formats
- text cleaning and chunking
- embedding generation
- semantic search over a vector database
- retrieval-augmented answer generation with an LLM

The architecture is modular and scalable, making it suitable for experimentation, learning, and future production enhancements.

---

## 🚀 Features

- 📄 Multi-format document loading
  - PDF
  - DOCX
  - TXT
  - Markdown
  - HTML
  - CSV

- 🧹 Document preprocessing and cleaning
- ✂️ Recursive text chunking
- 🧠 Hugging Face embeddings using BAAI/bge-base-en-v1.5
- 🗂️ Qdrant vector database integration
- 🤖 Google Gemini LLM support
- 🔍 Semantic similarity search
- 💬 Retrieval-Augmented Generation (RAG)
- 🏗️ Modular architecture using factory-based abstractions

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| LLM | Google Gemini |
| Embeddings | Hugging Face BAAI/bge-base-en-v1.5 |
| Framework | LangChain |
| Vector Database | Qdrant |
| Configuration | Python dotenv |
| Logging | Python logging |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
RAG-Assistant/
├── app/
│   ├── api/
│   ├── config/
│   ├── embeddings/
│   ├── llms/
│   ├── loaders/
│   ├── processors/
│   ├── rag/
│   ├── services/
│   ├── utils/
│   └── vectorstores/
├── data/
├── logs/
├── playground/
├── qdrant_db/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Architj875/RAG-Assistant.git
cd RAG-Assistant
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
MODEL_NAME=gemini-2.5-flash
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
COLLECTION_NAME=employee_handbook
QDRANT_PATH=./qdrant_db
CHUNK_SIZE=500
CHUNK_OVERLAP=100
TOP_K=5
```

---

## ▶️ Running the Project

You can test the project using the scripts in the playground folder:

```bash
python playground/test_loader.py
python playground/test_embedder.py
python playground/test_qdrant.py
python playground/test_llm.py
python playground/test_rag.py
```

---

## 🏛️ Architecture

```text
User Question
    │
    ▼
Similarity Search
    │
    ▼
Qdrant Vector Store
    │
    ▼
Relevant Chunks
    │
    ▼
Prompt Builder
    │
    ▼
Google Gemini
    │
    ▼
Final Answer
```

---

## 📌 Current Progress

### ✅ Phase 1 — RAG Engine

- [x] Modular project structure
- [x] Multi-format document loaders
- [x] Document cleaning
- [x] Recursive text chunking
- [x] Embedding generation
- [x] Qdrant integration
- [x] Semantic retrieval
- [x] Prompt builder
- [x] Gemini integration
- [x] End-to-end RAG pipeline

### 🚧 Upcoming Features

- FastAPI backend
- REST APIs
- File upload API
- Chat API
- Next.js frontend
- Chat interface
- Authentication
- Docker support
- Deployment
- CI/CD pipeline

---

## 📚 Learning Objectives

This project is being developed to explore and understand:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Vector databases
- Embedding models
- Semantic search
- FastAPI
- Clean architecture
- Software design patterns
- Full-stack AI application development

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Archit Joshi**

- GitHub: https://github.com/Architj875
- LinkedIn: https://www.linkedin.com/in/architdotjoshi/
