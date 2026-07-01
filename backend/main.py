from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from rag import ask_question
from ingest import load_pdf
from vector_store import (
    add_documents,
    delete_document_vectors,
)

app = FastAPI(
    title="Cortexa API",
    description="Enterprise Knowledge Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "../data"


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "app": "Cortexa",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Cortexa API",
        "version": "1.0.0"
    }


@app.get("/documents")
def get_documents():

    os.makedirs(DATA_PATH, exist_ok=True)

    documents = []

    for file in sorted(os.listdir(DATA_PATH)):

        if file.lower().endswith(".pdf"):

            file_path = os.path.join(DATA_PATH, file)

            documents.append({
                "name": file,
                "size_mb": round(
                    os.path.getsize(file_path) / 1024 / 1024,
                    2
                )
            })

    return {
        "count": len(documents),
        "documents": documents
    }

@app.delete("/documents/{filename}")
def delete_document(filename: str):

    file_path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    deleted_chunks = delete_document_vectors(filename)

    os.remove(file_path)

    return {
        "success": True,
        "message": f"{filename} deleted successfully.",
        "deleted_chunks": deleted_chunks
    }


@app.post("/upload")
async def upload_pdf(files: list[UploadFile] = File(...)):

    try:

        os.makedirs(DATA_PATH, exist_ok=True)

        uploaded = []

        for file in files:

            file_path = os.path.join(
                DATA_PATH,
                file.filename
            )

            if os.path.exists(file_path):
                print(f"{file.filename} already exists")
                continue

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            print(f"\nUploading: {file.filename}")

            chunks = load_pdf(file_path)

            print(f"Chunks Created: {len(chunks)}")

            add_documents(chunks)

            uploaded.append(file.filename)

        return {
            "success": True,
            "documents": uploaded,
            "message": f"{len(uploaded)} document(s) uploaded successfully."
        }

    except Exception as e:

        print("\nUPLOAD ERROR")
        print(type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post("/ask")
def ask(query: Query):

    try:

        result = ask_question(query.question)

        return {
            "question": query.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        print("\nASK ERROR")
        print(type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )