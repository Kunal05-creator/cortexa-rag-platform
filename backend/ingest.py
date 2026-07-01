from pathlib import Path

import fitz  # PyMuPDF
import pdfplumber
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 250


def _load_with_pymupdf(pdf_path: str):
    """
    Primary PDF parser using PyMuPDF.
    """
    documents = []

    pdf = fitz.open(pdf_path)

    try:
        total_pages = len(pdf)

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text")

            if text:
                text = text.strip()

            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(Path(pdf_path).resolve()),
                        "page": page_number,
                        "total_pages": total_pages,
                        "parser": "pymupdf",
                    },
                )
            )

    finally:
        pdf.close()

    return documents


def _load_with_pdfplumber(pdf_path: str):
    """
    Fallback parser if PyMuPDF fails.
    """
    documents = []

    with pdfplumber.open(pdf_path) as pdf:

        total_pages = len(pdf.pages)

        for page_number, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()

            if text:
                text = text.strip()

            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(Path(pdf_path).resolve()),
                        "page": page_number,
                        "total_pages": total_pages,
                        "parser": "pdfplumber",
                    },
                )
            )

    return documents


def load_pdf(pdf_path):
    """
    Compatible with previous implementation.

    Returns:
        List[Document]
    """

    pdf_path = str(pdf_path)

    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    documents = []

    try:
        documents = _load_with_pymupdf(pdf_path)

        if not documents:
            raise ValueError("PyMuPDF extracted no text.")

        print("\nPDF parsed using PyMuPDF")

    except Exception as e:
        print(f"\nPyMuPDF failed: {e}")
        print("Switching to pdfplumber...")

        documents = _load_with_pdfplumber(pdf_path)

        if not documents:
            raise ValueError("No readable text found in PDF.")

        print("PDF parsed using pdfplumber")

    print(f"\nLoaded {len(documents)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks
