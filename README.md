# DocMind- A Retrieval-Augmented Generation System 

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)**
system with a strong emphasis on **reliability, modularity, and
Scalable design principles**.

The system cleanly separates **ingestion**, **retrieval**, and **answer
generation**, uses **local embeddings** to avoid fragile API
dependencies, and integrates a cloud LLM **only for answer generation**.

The goal of this project is not just functional correctness, but to
demonstrate **real-world system design thinking**, including
architectural trade-offs, failure modes, and scalability considerations.

## Key Features

-   🔹 Local embeddings using sentence-transformers (no embedding API
    dependency)
-   🔹 ChromaDB for persistent vector storage and fast similarity search
-   🔹 Semantic retrieval using cosine similarity and HNSW indexing
-   🔹 LLM-based answer generation via Gemini (isolated, pluggable
    layer)
-   🔹 Graceful degradation when the LLM is unavailable
-   🔹 Production-oriented project structure and dependency management

## Architecture Overview

    User Query
       ↓
    Local Embedding (MiniLM)
       ↓
    ChromaDB Vector Search
       ↓
    Top-k Relevant Chunks
       ↓
    Gemini LLM (Answer Generation)
       ↓
    Final Answer

### Design Principles

-   **Local-first retrieval** for reliability and reproducibility
-   **LLM isolation** to avoid coupling ingestion and retrieval to API
    failures
-   **Pluggable components** (embeddings, vector store, LLM can be
    swapped)
-   **Explicit trade-offs** instead of hidden assumptions

## Project Structure

    RAG_begins/
    │
    ├── embeddings/
    │   ├── __init__.py
    │   └── local_embedding.py        # Local sentence-transformer embeddings
    │
    ├── docs/
    │   ├── Tesla.txt
    │   ├── Microsoft.txt
    │   └── ...                       # Source documents for ingestion
    │
    ├── ingestion_pipeline.py         # Document loading, chunking, embedding, indexing
    ├── retrieval_pipeline.py         # Semantic retrieval + answer generation
    ├── answer_generation.py          # Gemini-based LLM generation
    │
    ├── requirements.txt              # Project dependencies
    ├── .gitignore                    # Ignored files (env, vector DB, cache)
    └── README.md                     # Project documentation

## Installation

### 1. Create a virtual environment

    python3 -m venv venv
    source venv/bin/activate

### 2. Install dependencies

    pip install -r requirements.txt

## Configuration

### Gemini API Key (Answer Generation Only)

Set the Gemini API key as an environment variable:

    export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

> Note: Retrieval works independently of the LLM. If the API key is
> missing or invalid, the system can still retrieve relevant documents.

## Usage

### 1. Ingest Documents

Loads documents, splits them into chunks, generates local embeddings,
and stores them in ChromaDB.

    python3 ingestion_pipeline.py

### 2. Query the System

Runs semantic retrieval and generates an answer using Gemini.

    python3 retrieval_pipeline.py

## Embedding Model

-   **Model**: `sentence-transformers/all-MiniLM-L6-v2`
-   **Embedding Dimension**: 384
-   **Execution**: Fully local (CPU)

### Why this model?

-   Lightweight (\~90 MB)
-   Fast inference
-   Strong semantic retrieval quality
-   Widely used in production RAG systems

## Vector Store

-   **Database**: ChromaDB
-   **Index Type**: HNSW
-   **Similarity Metric**: Cosine similarity
-   **Persistence**: Local disk (excluded from version control)

Vector indices are generated during ingestion and intentionally not
committed to Git.

## LLM for Answer Generation

-   **Model**: Gemini 1.5 Flash
-   **Purpose**: Answer generation only

### Reasoning

-   Embeddings and retrieval require high reliability
-   LLM APIs are inherently less predictable
-   Isolating the LLM improves overall system robustness

The LLM layer is designed to be **replaceable** (e.g., local LLMs or
other APIs).

## Reliability and Failure Handling

### Guaranteed Behavior

-   Local embeddings always function
-   Vector search is deterministic
-   Retrieval does not depend on external APIs

### Non-Guaranteed Behavior

-   LLM availability
-   Network reliability
-   API rate limits

These constraints reflect real-world production systems and are
intentionally isolated.

## Scalability Considerations

  -----------------------------------------------------------------------
  Component                          Current Capability
  ---------------------------------- ------------------------------------
  Local embeddings                   Up to hundreds of thousands of
                                     chunks (CPU)

  ChromaDB                           Efficient retrieval up to \~1M
                                     vectors (single node)

  Concurrency                        Single-process (scalable with
                                     async/multi-worker setup)
  -----------------------------------------------------------------------

### Future Scaling Paths

-   GPU-backed embeddings
-   Distributed vector databases
-   Hybrid retrieval (BM25 + vector search)
-   Async APIs for high concurrency

## Design Decisions and Trade-offs

### Why Local Embeddings?

-   Avoid API quota and rate-limit issues
-   Deterministic ingestion
-   Lower long-term cost
-   Easier debugging and reproducibility

### Why Not Hugging Face Free Inference?

-   Unreliable availability
-   Endpoint deprecations
-   No SLA guarantees

### Why Gemini Only for Generation?

-   High-quality language generation
-   Reduced operational complexity
-   Clear separation of concerns

## Disclaimer

This project is intended as a **learning and demonstration system**.\
While the architecture mirrors production-grade patterns, it is **not
deployed as a live service**.

## Author Notes

This project reflects **real-world engineering decisions**, including
failed approaches, architectural pivots, and reliability trade-offs.

The focus is on **clarity, correctness, and evolvability**, rather than
premature scaling.

## License

MIT License
