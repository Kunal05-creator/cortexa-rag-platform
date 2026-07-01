import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# Project paths
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # points to backend/
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
LOG_DIR = BASE_DIR / "logs"

# ------------------------------------------------------------------
# Model & retrieval settings
# ------------------------------------------------------------------
# Embedding model (can be any HuggingFace model)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# LLM model (Gemini, OpenAI, or any)
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# Retrieval
TOP_K = int(os.getenv("TOP_K", "8"))

# ------------------------------------------------------------------
# API keys (optional – only needed if using Gemini/OpenAI)
# ------------------------------------------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")   # can be empty if using HuggingFace

# ------------------------------------------------------------------
# Create directories if they don't exist
# ------------------------------------------------------------------
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)