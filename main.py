from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil

from rag import ask_question
from ingest import load_pdf
from vector_store import get_vectorstore

app = FastAPI(
    title="Cortexa API",
    description="Enterprise Knowledge Intelligence Platform",
    version="1.0.0"
)


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Cortexa API Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"../data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = load_pdf(file_path)

    get_vectorstore(chunks)

    return {
        "message": f"{file.filename} uploaded and indexed successfully"
    }


@app.post("/ask")
def ask(query: Query):

    result = ask_question(query.question)

    return {
        "question": query.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }