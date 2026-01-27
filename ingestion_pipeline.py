import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma

from embeddings.local_embedding import LocalEmbedding

DOCS_DIR = "docs"
PERSIST_DIR = "chroma_store"


def load_documents():
    documents = []

    print("📄 Loading documents...")
    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(DOCS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={"source": path}
            )
        )

    print(f"📄 Loaded {len(documents)} documents")
    return documents


def ingest():
    documents = load_documents()

    print("✂️ Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"🧩 Created {len(chunks)} chunks")

    print("🧠 Creating local embeddings...")
    embedding = LocalEmbedding()

    print("💾 Storing vectors in ChromaDB...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=PERSIST_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print("✅ Ingestion completed successfully")


if __name__ == "__main__":
    ingest()
