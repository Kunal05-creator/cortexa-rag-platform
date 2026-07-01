from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def ask_question(question):

    vectorstore = Chroma(
        persist_directory="../chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    )

    prompt = f"""
Answer the question using only the provided context.

If the answer is not present in the context, say:
"I could not find that information in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    sources = []

    for doc in docs:

        source_info = {
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", 0) + 1
        }

        if source_info not in sources:
            sources.append(source_info)

    return {
        "answer": response.content,
        "sources": sources
    }