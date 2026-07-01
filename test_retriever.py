from rag import get_retriever

retriever = get_retriever()

docs = retriever.invoke(
    "What technical skills does Kunal have?"
)

print(docs[0].page_content)