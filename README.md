# Cortexa

Enterprise Knowledge Intelligence Platform

## Overview

Cortexa is a Retrieval-Augmented Generation (RAG) platform designed to transform static documents into an intelligent knowledge base. Users can upload multiple PDF documents and interact with them using natural language queries. The system retrieves relevant information from the uploaded documents and generates context-aware answers with source citations.

The platform combines semantic search, vector databases, modern language models, and a responsive web interface to provide accurate document-grounded responses.

## Key Features

* Multi-document PDF ingestion
* Semantic search using vector embeddings
* Retrieval-Augmented Generation (RAG)
* Source-aware question answering
* Document-grounded responses
* Multi-file knowledge base
* FastAPI backend architecture
* React-based frontend interface
* ChromaDB vector storage
* Gemini 2.5 Flash integration
* Hallucination-reduction prompt engineering

## Architecture

User Query

↓

React Frontend

↓

FastAPI Backend

↓

Retriever

↓

ChromaDB Vector Store

↓

Relevant Document Chunks

↓

Gemini 2.5 Flash

↓

Answer + Source Citations

## Technology Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Axios

### Backend

* FastAPI
* Python

### AI and RAG

* LangChain
* ChromaDB
* HuggingFace Embeddings
* Gemini 2.5 Flash

### Embedding Model

* sentence-transformers/all-MiniLM-L6-v2

## Project Workflow

### Document Upload

Users upload one or more PDF documents through the web interface.

### Document Processing

The uploaded documents are processed using PyPDFLoader and split into smaller chunks using RecursiveCharacterTextSplitter.

### Embedding Generation

Each chunk is converted into vector embeddings using HuggingFace sentence transformers.

### Vector Storage

Embeddings are stored in ChromaDB for efficient semantic retrieval.

### Question Answering

When a user submits a query:

1. Relevant chunks are retrieved from ChromaDB.
2. Context is constructed from retrieved chunks.
3. Gemini generates an answer using only the retrieved information.
4. Sources are returned alongside the response.

## Example Use Cases

* Research paper analysis
* Resume intelligence systems
* Enterprise document search
* Knowledge management
* Academic document querying
* Internal company documentation assistants

## API Endpoints

### Upload Document

POST /upload

Uploads and indexes PDF documents into the vector database.

### Ask Question

POST /ask

Returns document-grounded answers and source citations.

## Project Structure

Cortexa

backend/

* main.py
* rag.py
* ingest.py
* vector_store.py
* requirements.txt

frontend/

* src/
* components/
* services/

chroma_db/

data/

README.md

## Running Locally

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

## Current Capabilities

* Multiple PDF document support
* Semantic document retrieval
* Context-aware responses
* Source citations
* Persistent vector database
* Full-stack architecture

## Future Improvements

* User authentication
* Document-level filtering
* Chat history and memory
* Hybrid search
* DOCX and TXT support
* Cloud deployment
* Multi-user support
* Advanced citation viewer

## Author

Kunal Bansal

Integrated B.Tech + M.Tech (Computer Science and Engineering)

Artificial Intelligence and Robotics Specialization

Gautam Buddha University

## License

This project is intended for educational, research, and portfolio purposes.

