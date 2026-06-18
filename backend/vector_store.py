from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

DB_PATH = "../chroma_db"
COLLECTION_NAME = "cortexa"


def get_vectorstore():

    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vectorstore


def add_documents(documents):

    vectorstore = get_vectorstore()

    vectorstore.add_documents(documents)

    print("\n==============================")
    print("DOCUMENTS ADDED")
    print("==============================")
    print(f"New Chunks: {len(documents)}")
    print(
        f"Total Chunks: {vectorstore._collection.count()}"
    )
    print("==============================\n")

    return vectorstore


def load_vectorstore():

    vectorstore = get_vectorstore()

    print(
        f"\nLoaded Vector Store | Total Chunks: {vectorstore._collection.count()}"
    )

    return vectorstore