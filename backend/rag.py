from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from vector_store import load_vectorstore

load_dotenv()


def ask_question(question):

    # Load Vector Store
    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 8
        }
    )

    docs = retriever.invoke(question)

    # Remove duplicate chunks
    unique_docs = []
    seen = set()

    for doc in docs:

        key = (
            doc.metadata.get("source", ""),
            doc.metadata.get("page", 0),
            doc.page_content[:200]
        )

        if key not in seen:
            seen.add(key)
            unique_docs.append(doc)

    docs = unique_docs

    # Special handling for metadata questions
    metadata_keywords = [
        "title",
        "author",
        "name",
        "candidate",
        "student",
        "guide",
        "supervisor",
        "university",
        "college",
        "thesis",
        "dissertation",
        "abstract"
    ]

    if any(keyword in question.lower() for keyword in metadata_keywords):

        extra_docs = vectorstore.similarity_search(
            question,
            k=25
        )

        first_page_docs = [
            doc for doc in extra_docs
            if doc.metadata.get("page", 999) <= 3
        ]

        docs.extend(first_page_docs)

        unique_docs = []
        seen = set()

        for doc in docs:

            key = (
                doc.metadata.get("source", ""),
                doc.metadata.get("page", 0),
                doc.page_content[:200]
            )

            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)

        docs = unique_docs

    print("\n==============================")
    print("RETRIEVED DOCUMENTS")
    print("==============================")

    for i, doc in enumerate(docs):
        print(f"\nDOC {i+1}")
        print("SOURCE:", doc.metadata.get("source"))
        print("PAGE:", doc.metadata.get("page"))
        print("CONTENT PREVIEW:")
        print(doc.page_content[:500])

    print("\n==============================\n")

    context = "\n\n".join(
        [
            f"PAGE {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in docs
        ]
    )

    print("\n========== CONTEXT ==========")
    print(context[:5000])
    print("\n=============================\n")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    )

    prompt = f"""
You are Cortexa, an Enterprise Knowledge Intelligence Assistant.

Answer ONLY from the provided document context.

Rules:
1. Do not make up information.
2. Answer clearly if the information exists.
3. Use information from any uploaded document.
4. If the answer is not present, respond exactly with:

I could not find that information in the uploaded documents.

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