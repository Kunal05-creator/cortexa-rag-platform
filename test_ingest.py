from ingest import load_pdf

chunks = load_pdf("../data/KunalBansal_Resume.pdf")

print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")

print(chunks[0].page_content[:500])