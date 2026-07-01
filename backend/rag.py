from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Any, Optional
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

from config import TOP_K, LLM_MODEL, GOOGLE_API_KEY
from vector_store import search_documents

load_dotenv()

MODEL_NAME = LLM_MODEL
TOP_K_RETRIEVAL = TOP_K   # e.g., 15

# ------------------------------------------------------------------
# Helpers (unchanged)
# ------------------------------------------------------------------
def remove_duplicates(documents: List[Document]) -> List[Document]:
    unique = []
    seen = set()
    for doc in documents:
        key = (doc.metadata.get("source", ""), doc.metadata.get("page", 0), doc.page_content[:300])
        if key not in seen:
            seen.add(key)
            unique.append(doc)
    return unique

def format_context_with_numbers(documents: List[Document]) -> tuple:
    context_parts = []
    sources = []
    for idx, doc in enumerate(documents, start=1):
        source = Path(doc.metadata.get("source", "Unknown")).name
        page = doc.metadata.get("page", 0) + 1
        context_parts.append(f"""
[Document {idx}]
Source: {source}
Page: {page}
Content:
{doc.page_content}
""")
        sources.append({
            "source": source,
            "page": page,
            "chunk_number": idx,
        })
    return "\n".join(context_parts), sources

def collect_sources_from_citations(answer: str, all_sources: List[Dict]) -> List[Dict]:
    pattern = r'\[(\d+)\]'
    cited_numbers = set(map(int, re.findall(pattern, answer)))
    if not cited_numbers:
        return all_sources
    cited_sources = [src for src in all_sources if src["chunk_number"] in cited_numbers]
    return cited_sources if cited_sources else all_sources

def debug_documents(documents: List[Document]) -> None:
    print("\n==============================")
    print("RETRIEVED DOCUMENTS")
    print("==============================")
    for i, doc in enumerate(documents, start=1):
        print(f"\nDOC {i}")
        print("SOURCE:", Path(doc.metadata.get("source", "Unknown")).name)
        print("PAGE:", doc.metadata.get("page", 0) + 1)
        print("CONTENT:")
        print(doc.page_content[:600])
    print("\n==============================\n")

# ------------------------------------------------------------------
# Retrieval with list‑support (unchanged)
# ------------------------------------------------------------------
def retrieve_documents(question: str, document_filters: Optional[List[str]] = None) -> List[Document]:
    filter_meta = None
    if document_filters:
        filter_meta = {"filename": {"$in": document_filters}}

    chunks = search_documents(
        query=question,
        k=TOP_K_RETRIEVAL,
        filter_metadata=filter_meta,
        use_mmr=True
    )
    docs = [Document(page_content=chunk["text"], metadata=chunk["metadata"]) for chunk in chunks]

    list_keywords = ["chapter", "chapters", "table of contents", "contents", "list of", "authors", "members", "steps", "sections"]
    if any(kw in question.lower() for kw in list_keywords):
        print("\n--- Detected list question, performing exhaustive retrieval ---")
        extra_chunks = search_documents(
            query=question,
            k=30,
            filter_metadata=filter_meta,
            use_mmr=False
        )
        for chunk in extra_chunks:
            if "chapter" in chunk["text"].lower() or "contents" in chunk["text"].lower():
                docs.append(Document(page_content=chunk["text"], metadata=chunk["metadata"]))
            if chunk["metadata"].get("page", 999) <= 10 and "chapter" in question.lower():
                docs.append(Document(page_content=chunk["text"], metadata=chunk["metadata"]))

    docs = remove_duplicates(docs)
    return docs

# ------------------------------------------------------------------
# Main ask_question with improved prompt for "name" queries
# ------------------------------------------------------------------
def ask_question(question: str, document_filters: Optional[List[str]] = None) -> Dict[str, Any]:
    docs = retrieve_documents(question, document_filters)

    if not docs:
        return {
            "answer": "I could not find any relevant information in the uploaded documents.",
            "sources": []
        }

    debug_documents(docs)
    context, all_sources = format_context_with_numbers(docs)

    print("\n========== CONTEXT ==========\n")
    print(context[:6000])
    print("\n=============================\n")

    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0.2,
        google_api_key=GOOGLE_API_KEY
    )

    # Improved prompt with explicit instructions for name/list queries
    prompt = f"""
You are Cortexa, an Enterprise Knowledge Intelligence Assistant.

Answer the user's question based **only** on the provided document chunks.
When you use information from a specific chunk, cite it using [1], [2], etc.

Guidelines:
- If the question asks for **names** or **titles** (e.g., "name of the projects", "list the authors"), provide **only the names/titles** – do not include descriptions or extra details.
- For list questions, extract the complete list from the context.
- If information is missing, say so clearly.
- If the answer is not present at all, reply exactly: "I could not find that information in the uploaded documents."

Example:
Question: "Name the projects from the resume."
Expected answer: "Project A [1], Project B [2], Project C [3]."

==========================
DOCUMENT CONTEXT
==========================

{context}

==========================
USER QUESTION
==========================

{question}
"""

    response = llm.invoke(prompt)
    answer = response.content if hasattr(response, "content") else str(response)

    if not answer.strip():
        answer = "I could not find that information in the uploaded documents."

    cited_sources = collect_sources_from_citations(answer, all_sources)

    if "I could not find" in answer:
        cited_sources = []

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")
    print(answer)
    print("==============================\n")
    print("\n==============================")
    print("SOURCES (cited)")
    print("==============================")
    for src in cited_sources:
        print(f"{src['source']} | Page {src['page']} (chunk {src['chunk_number']})")
    print("==============================\n")

    return {
        "answer": answer,
        "sources": cited_sources
    }