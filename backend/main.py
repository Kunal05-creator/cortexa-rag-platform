from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from rag import ask_question
from ingest import load_pdf
from vector_store import add_documents

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


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Cortexa API Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    try:

        os.makedirs("../data", exist_ok=True)

        file_path = f"../data/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"\nUploading: {file.filename}")

        chunks = load_pdf(file_path)

        print(f"Total chunks: {len(chunks)}")

        print("\n===== FIRST 5 CHUNKS =====")

        for i, chunk in enumerate(chunks[:5]):
            print(f"\nCHUNK {i+1}")
            print("PAGE:", chunk.metadata.get("page"))
            print(chunk.page_content[:300])

        print("\n==========================")

        add_documents(chunks)

        return {
            "message": f"{file.filename} uploaded and indexed successfully"
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

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )