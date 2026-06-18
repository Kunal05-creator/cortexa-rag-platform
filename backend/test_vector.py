from ingest import load_pdf
from vector_store import get_vectorstore

chunks = load_pdf("../data/KunalBansal_Resume.pdf")

vectorstore = get_vectorstore(chunks)

print("Vector Database Created Successfully")