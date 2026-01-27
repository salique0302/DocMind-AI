from langchain_chroma import Chroma
from embeddings.local_embedding import LocalEmbedding
from answer_generation import generate_answer

PERSIST_DIR = "chroma_store"


def query_rag(query: str, k: int = 3):
    embedding = LocalEmbedding()

    db = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding
    )

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    # Extract text for LLM
    contexts = [doc.page_content for doc in docs]

    answer = generate_answer(query, contexts)

    print("\n📚 Retrieved Sources:")
    for i, doc in enumerate(docs, 1):
        print(f"[{i}] {doc.metadata.get('source')}")

    print("\n🤖 Answer:")
    print(answer)


if __name__ == "__main__":
    query_rag("How much did Microsoft pay to acquire GitHub?")
