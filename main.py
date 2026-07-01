from pathlib import Path
import shutil
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ingest import load_pdf
from rag import ask_question
from vector_store import add_documents


app = FastAPI(
    title="Cortexa API",
    description="Enterprise Knowledge Intelligence Platform",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("../data")
DATA_DIR.mkdir(exist_ok=True)


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Cortexa API Running"
    }


@app.get("/documents")
def list_documents():

    docs = []

    for pdf in DATA_DIR.glob("*.pdf"):

        docs.append(
            {
                "name": pdf.name,
                "size_mb": round(pdf.stat().st_size / (1024 * 1024), 2)
            }
        )

    return {
        "count": len(docs),
        "documents": docs
    }


@app.post("/upload")
async def upload_pdfs(
    files: list[UploadFile] = File(...)
):

    uploaded = []

    for file in files:

        path = DATA_DIR / file.filename

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks = load_pdf(str(path))

        add_documents(chunks)

        uploaded.append(file.filename)

    return {
        "message": f"{len(uploaded)} document(s) indexed successfully.",
        "documents": uploaded
    }


@app.delete("/documents/{filename}")
def delete_document(filename: str):

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    os.remove(file_path)

    return {
        "message": f"{filename} deleted."
    }


@app.post("/ask")
def ask(query: Query):

    result = ask_question(query.question)

    return {
        "question": query.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }