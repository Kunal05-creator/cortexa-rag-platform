# Cortexa

Enterprise Knowledge Intelligence Platform

## Overview

Cortexa is a Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents and interact with them using natural language questions. The system retrieves relevant document chunks from a vector database and generates context-aware responses using Google's Gemini 2.5 Flash model.

The project demonstrates the integration of FastAPI, LangChain, ChromaDB, HuggingFace Embeddings, and Generative AI to build an intelligent document question-answering system.

## Features

* PDF document upload and processing
* Semantic search using vector embeddings
* Retrieval-Augmented Generation (RAG)
* Context-aware question answering
* Source citation support
* FastAPI backend
* React frontend
* ChromaDB vector database
* Gemini 2.5 Flash integration

## Technology Stack

### Frontend

* React
* Vite
* Axios
* Tailwind CSS

### Backend

* FastAPI
* Python

### AI Components

* LangChain
* ChromaDB
* HuggingFace Embeddings
* Gemini 2.5 Flash

### Embedding Model

* sentence-transformers/all-MiniLM-L6-v2

## System Workflow

1. Upload a PDF document.
2. Extract text using PyPDFLoader.
3. Split text into chunks.
4. Generate vector embeddings.
5. Store embeddings in ChromaDB.
6. Retrieve relevant chunks based on user queries.
7. Generate answers using Gemini.
8. Return answers with source references.

## API Endpoints

### Upload PDF

POST /upload

Uploads a PDF file and indexes its content.

### Ask Question

POST /ask

Accepts a user query and returns a context-aware response with sources.

## Project Structure

backend/

* main.py
* rag.py
* ingest.py
* vector_store.py

frontend/

* src/
* components/
* services/

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Current Status

Implemented:

* PDF Upload
* Document Chunking
* Vector Embeddings
* ChromaDB Integration
* Semantic Retrieval
* Gemini-based Answer Generation
* Source Citations
* React Frontend

Planned Improvements:

* Improved Multi-Document Retrieval
* Authentication
* Chat History
* Document Filtering
* Cloud Deployment
* Hybrid Search

## Author

Kunal Bansal

Integrated B.Tech + M.Tech (Computer Science and Engineering)

Artificial Intelligence and Robotics Specialization

Gautam Buddha University
