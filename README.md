# RAG Assistant

> AI document intelligence for your own knowledge base

A modern Retrieval-Augmented Generation (RAG) system for turning uploaded documents into an interactive, queryable knowledge workspace.

This project combines a Python FastAPI backend with a Next.js frontend and includes both:

- Standard RAG retrieval for grounded question answering
- ReAct agent mode for multi-step, tool-driven reasoning workflows

It is built to work with mixed document types and is designed to be generic enough for real-world document ingestion use cases, not just a single file format or fixed workflow.

## Overview

RAG Assistant helps users turn scattered files into a usable retrieval layer for AI-powered search and Q&A. Users can upload documents, process them into smaller chunks, embed them into a vector database, and ask natural-language questions grounded in the indexed content.

The application supports:

- document upload for multiple file types
- preprocessing and chunking for retrieval
- embeddings and semantic similarity search with Qdrant
- grounded answer generation using Gemini
- optional ReAct agent execution for more advanced workflows
- a clean web interface for document interaction and chat

This repository is intended as a practical, extensible foundation for document intelligence applications, research experiments, and real-world product workflows.

## Key Features

- Generic document ingestion for PDF, DOCX, TXT, MD, HTML, CSV, and similar content
- Modular loaders, processors, and vectorstore integrations
- Semantic retrieval using embeddings + vector search
- Chunking and deduplication pipeline
- Prompt assembly for grounded answers
- Google Gemini LLM integration
- ReAct-style agent mode for multi-step reasoning
- FastAPI backend APIs for file handling and chat
- Next.js frontend with modern UI and theme support
- Light/dark mode styling with a clean app shell
- Evaluation and playground scripts for experimentation and retrieval tuning

## Architecture

```text
User request
   |
   v
Frontend (Next.js)
   |
   v
FastAPI Backend
   |
   +--> Document ingestion / preprocessing
   |
   +--> Embedding generation
   |
   +--> Vector storage (Qdrant)
   |
   +--> Retrieval + reranking / filtering
   |
   +--> Prompt building
   |
   +--> Gemini LLM / ReAct agent
   |
   v
Response to user
```

## Tech Stack

### Backend

- Python
- FastAPI
- Qdrant
- Google Gemini
- Hugging Face embeddings
- Python dotenv
- Pydantic models

### Frontend

- Next.js
- React
- Tailwind CSS
- TypeScript
- Lucide icons
- Theme-aware UI system

## Project Structure

```text
RAG-Assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── config/
│   │   ├── embeddings/
│   │   ├── exceptions/
│   │   ├── llms/
│   │   ├── loaders/
│   │   ├── middleware/
│   │   ├── processors/
│   │   ├── rag/
│   │   ├── services/
│   │   ├── utils/
│   │   └── vectorstores/
│   ├── data/
│   ├── evaluation/
│   ├── logs/
│   ├── playground/
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── context/
│   ├── hooks/
│   ├── lib/
│   ├── services/
│   ├── types/
│   ├── package.json
│   └── README.md
├── qdrant_db/
├── test_documents/
├── main.py
├── .gitignore
├── README.md
└── .env.example
```

## Requirements

### Python

- Python 3.10+

### Node.js

- Node.js 18+
- npm / pnpm / yarn

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Architj875/RAG-Assistant.git
cd RAG-Assistant
```

### 2. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Frontend setup

```bash
cd frontend
npm install
```

### 4. Environment variables

Create a `.env` file in the backend project root with values similar to:

```env
GOOGLE_API_KEY=your_google_api_key
MODEL_NAME=gemini-2.5-flash
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
CHUNK_SIZE=700
CHUNK_OVERLAP=120
TOP_K=5
RETRIEVAL_CANDIDATES=30
MIN_SIMILARITY_SCORE=0.0
QDRANT_COLLECTION_NAME=knowledge_base
QDRANT_DB_PATH=./qdrant_db
```

> Keep secrets out of Git using your ignore rules and do not commit `.env` files.

## Run the Application

### Start the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

The backend API will be available at:

- http://localhost:8000

### Start the frontend

```bash
cd frontend
npm run dev
```

The frontend app will run at:

- http://localhost:3000

## Usage

### Upload a document

Use the frontend upload area or the backend API to upload a file into the system.

### Ask a question

After ingestion, you can:

- ask a direct RAG question
- switch to ReAct agent mode
- retrieve grounded answers from indexed content

### Retrieval flow

1. document is loaded
2. text is cleaned and chunked
3. embeddings are created
4. chunks are stored in Qdrant
5. query is transformed into embeddings
6. similar chunks are retrieved
7. relevant context is passed into Gemini or the agent
8. final answer is returned to the user

## ReAct Agent Implementation

The project includes a working ReAct agent execution path for situations where a multi-step reasoning flow is useful. This is implemented as part of the app architecture and can be switched on from the frontend chat interface. It helps when a task benefits from:

- stepwise reasoning
- intermediate tool usage
- structured tool-driven retrieval
- more advanced decision-making during answer generation

## Evaluation and Research

The project includes evaluation and experimentation folders for:

- retrieval benchmarking
- chunk quality checks
- reranker comparisons
- embedding and retrieval audits
- document pipeline experiments

These are useful for iterative tuning and understanding how retrieval quality changes across document types and chunking strategies.

## Final Repository Cleanup Review

The project has been cleaned up to keep the repository focused on reusable product code rather than local experimentation artifacts.

Current repository hygiene includes:

- single project-level README for the repo
- ignored local secrets and environment variables
- ignored generated outputs and vector database contents
- ignored scratch evaluation and playground artifacts
- preserved source code for the actual app and retriever pipeline

This keeps the repository clean, shareable, and easier to maintain while preserving the work needed for experimentation and iteration.

## Roadmap

Planned improvements include:

- stronger reranking strategies
- better retrieval selection logic
- more document formats and preprocessing support
- improved frontend UX polish
- production-ready deployment setup
- monitoring and evaluation dashboards
- authentication and user management

## License

This project is currently intended for learning, research, and internal development use.

## Contact

For project-related questions or collaboration, contact the project owner or maintainers through the repository.
