import os
import uuid
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# HuggingFace embeddings – free, local, no API key
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Import config variables
from config import CHROMA_DIR, TOP_K, EMBEDDING_MODEL

# MMR tuning – can be moved to config later
MMR_FETCH_K = 20
MMR_LAMBDA = 0.5


class VectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Persistent ChromaDB client
        self._client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self._collection = self._client.get_or_create_collection(
            name="cortexa_docs",
            metadata={"hnsw:space": "cosine"}
        )

        # HuggingFace embeddings (downloaded once, ~400 MB)
        self._embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

        self._initialized = True

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add chunks to the vector store."""
        if not documents:
            return []

        ids = []
        texts = []
        metadatas = []

        for doc in documents:
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            texts.append(doc.page_content)

            source = doc.metadata.get("source", "")
            filename = os.path.basename(source) if source else "unknown"
            page = doc.metadata.get("page", 0)

            metadatas.append({
                "filename": filename,
                "source": source,
                "page": page,
                "chunk_id": chunk_id,
                **{k: v for k, v in doc.metadata.items() if k not in ["source", "page"]}
            })

        # Generate embeddings in batch
        embeddings = self._embedding_model.embed_documents(texts)

        self._collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )

        return ids

    def delete_document(self, filename: str) -> int:
        """Delete all chunks for a given filename."""
        results = self._collection.get(where={"filename": filename})
        ids = results["ids"]
        if ids:
            self._collection.delete(ids=ids)
        return len(ids)

    def search(self, query: str, k: int = TOP_K,
               filter_metadata: Optional[Dict[str, Any]] = None,
               use_mmr: bool = True) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks, optionally with MMR reranking."""
        query_embedding = self._embedding_model.embed_query(query)
        fetch_k = MMR_FETCH_K if use_mmr else k

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=fetch_k,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"]
        )

        if not results["ids"] or not results["ids"][0]:
            return []

        chunks = []
        for i in range(len(results["ids"][0])):
            chunks.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        if use_mmr and len(chunks) > k:
            chunks = self._mmr_rerank(query_embedding, chunks, k, MMR_LAMBDA)

        return chunks[:k]

    def _mmr_rerank(self, query_embedding: List[float], chunks: List[Dict],
                    k: int, lambda_param: float) -> List[Dict]:
        """Maximum Marginal Relevance reranking."""
        texts = [c["text"] for c in chunks]
        embeds = self._embedding_model.embed_documents(texts)

        query_emb = np.array(query_embedding).reshape(1, -1)
        sim_query = cosine_similarity(query_emb, embeds)[0]   # relevance
        sim_matrix = cosine_similarity(embeds)                # pairwise similarity

        selected = []
        remaining = list(range(len(chunks)))

        # First pick the most relevant chunk
        first = np.argmax(sim_query)
        selected.append(first)
        remaining.remove(first)

        # Then pick chunks that balance relevance and diversity
        for _ in range(1, min(k, len(chunks))):
            mmr_scores = []
            for idx in remaining:
                relevance = sim_query[idx]
                redundancy = max(sim_matrix[idx][sel] for sel in selected)
                mmr = lambda_param * relevance - (1 - lambda_param) * redundancy
                mmr_scores.append(mmr)
            best_idx = remaining[np.argmax(mmr_scores)]
            selected.append(best_idx)
            remaining.remove(best_idx)

        return [chunks[i] for i in selected]

    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """Return aggregated metadata for each indexed file."""
        all_metadatas = self._collection.get(include=["metadatas"])
        if not all_metadatas["metadatas"]:
            return []

        doc_map = {}
        for meta in all_metadatas["metadatas"]:
            fname = meta.get("filename")
            if not fname:
                continue
            if fname not in doc_map:
                doc_map[fname] = {"pages": set(), "chunks": 0}
            doc_map[fname]["pages"].add(meta.get("page", 0))
            doc_map[fname]["chunks"] += 1

        result = []
        for fname, data in doc_map.items():
            result.append({
                "filename": fname,
                "pages": len(data["pages"]),
                "chunks": data["chunks"],
            })
        return result


# Global instance (singleton)
_vector_store = VectorStore()


# Public functions – used by main.py and rag.py
def add_documents(documents: List[Document]) -> None:
    _vector_store.add_documents(documents)


def delete_document_vectors(filename: str) -> int:
    return _vector_store.delete_document(filename)


def search_documents(query: str, k: int = TOP_K,
                     filter_metadata: Optional[Dict] = None,
                     use_mmr: bool = True) -> List[Dict]:
    return _vector_store.search(query, k, filter_metadata, use_mmr)


def get_all_documents_metadata() -> List[Dict]:
    return _vector_store.get_all_metadata()