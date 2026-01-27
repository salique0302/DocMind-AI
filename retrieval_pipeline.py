from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from embeddings.gemini import GeminiEmbeddings

load_dotenv()

PERSIST_DIRECTORY = "db/chroma_db"


def load_vector_store():
    print("Loading Chroma vector store...")

    embedding_model = GeminiEmbeddings()

    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model,
        collection_metadata={"hnsw:space": "cosine"},
    )

    print("Vector store loaded successfully")
    return db


def run_query(query, k=5):
    db = load_vector_store()

    retriever = db.as_retriever(search_kwargs={"k": k})

    print(f"\nUser Query: {query}")
    print("\n--- Retrieved Context ---")

    relevant_docs = retriever.invoke(query)

    for i, doc in enumerate(relevant_docs, 1):
        print(f"\nDocument {i}:")
        print(f"Source: {doc.metadata.get('source')}")
        print(doc.page_content)
        print("-" * 60)


if __name__ == "__main__":
    query = "How much did Microsoft pay to acquire GitHub?"
    run_query(query)
