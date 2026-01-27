# DocMind-AI
RAG pipeline for converting enterprise documents into a persistent, queryable vector knowledge base.
# RAG (Retrieval-Augmented Generation) System

A modular and scalable **Retrieval-Augmented Generation (RAG)** system for document ingestion, vector storage, and context-aware question answering using Large Language Models.

---

## 🚀 Features

- **Scalable Document Ingestion**
  - Batched document loading and processing
  - Controlled embedding generation to avoid memory bottlenecks
- **Semantic Chunking**
  - Configurable chunk size and overlap
  - Designed to preserve meaning and retrieval quality
- **Vector Storage**
  - Persistent vector storage using ChromaDB
- **RAG Pipeline**
  - Context-aware question answering using LLMs
- **Modular Architecture**
  - Clear separation between ingestion and retrieval pipelines
  - Easily extensible and debuggable

---

## 📁 Project Structure

RAG/
├── src/
│ ├── ingestion_pipeline.py # End-to-end ingestion workflow
│ ├── retrieval_pipeline.py # RAG retrieval and QA pipeline
│ ├── data_loader.py # Document loading logic
│ ├── data_chunking.py # Text chunking logic
│ ├── data_embedding.py # Embedding generation logic
│ ├── data_vectorstore.py # Vector store abstraction
│
├── data/ # Input documents directory
├── chroma_db/ # Vector database (auto-generated)
├── requirements.txt # Python dependencies
└── .env # Environment variables (create this)


## 🛠️ Setup

### 1. Clone the Repository

bash-
git clone <your-repo-url>
cd RAG
2. Create a Virtual Environment
bash
Copy code
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Environment Variables
Create a .env file in the root directory:

env
Copy code
# HuggingFace API Token (for embeddings)
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# LLM Provider API Key
LLM_API_KEY=your_llm_api_key_here
📖 Usage
Ingestion Pipeline
Use the ingestion pipeline to process documents and store embeddings in the vector database.

python
Copy code
from src.ingestion_pipeline import IngestionPipeline
from src.data_loader import DataLoader
from src.data_chunking import DataChunking
from src.data_embedding import EmbeddingModel
from src.data_vectorstore import DataVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

data_loader = DataLoader(
    data_path="./data",
    max_chars_per_batch=100_000
)

data_chunking = DataChunking(
    chunk_size=1000,
    chunk_overlap=200
)

embedding_model = EmbeddingModel(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

vectorstore = DataVectorStore(
    embedding_model=embedding_model,
    collection_name="rag_collection",
    persist_directory="./chroma_db",
    batch_size=50
)

pipeline = IngestionPipeline(
    data_loader=data_loader,
    data_chunking=data_chunking,
    vectorstore=vectorstore
)

stats = pipeline.ingest(verbose=True)
print(f"Ingested {stats['chunks_stored']} chunks")
Retrieval Pipeline
Query the RAG system using the retrieval pipeline.

python
Copy code
from src.retrieval_pipeline import DataRetrieval
from src.data_embedding import EmbeddingModel
from src.data_vectorstore import DataVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

embedding_model = EmbeddingModel(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

vectorstore = DataVectorStore(
    embedding_model=embedding_model,
    collection_name="rag_collection",
    persist_directory="./chroma_db"
)

retrieval = DataRetrieval(
    vectorstore=vectorstore,
    model_name="llama-3.1-8b-instant",
    top_k=5
)

result = retrieval.query("What is Retrieval-Augmented Generation?")
print(result["answer"])

answer = retrieval.get_answer("Explain vector databases")
print(answer)

queries = [
    "What is RAG?",
    "Why are embeddings important?",
    "How does chunking affect retrieval?"
]

results = retrieval.batch_query(queries, verbose=True)
🔧 Components
DataLoader
Batched document loading

Encoding-safe text reading

Designed for large document collections

DataChunking
Configurable chunk size and overlap

Optimized for semantic continuity

DataEmbedding
Embedding generation abstraction

Easily swappable embedding models

DataVectorStore
ChromaDB-backed vector storage

Persistent storage

Similarity search

IngestionPipeline
End-to-end ingestion orchestration

Isolated pipeline stages

Progress and statistics tracking

DataRetrieval
Query embedding

Vector similarity search

LLM-based answer generation

⚙️ Configuration
Chunking Parameters
chunk_size – Size of each text chunk (default: 1000)

chunk_overlap – Overlap between chunks (default: 200)

Embedding Model
Default: sentence-transformers/all-MiniLM-L6-v2

Can be replaced by changing EmbeddingModel

LLM Model
Default: llama-3.1-8b-instant

Can be swapped based on provider support

Vector Store
Collection name: rag_collection

Persist directory: ./chroma_db

📊 Performance
Controlled embedding batching to reduce memory usage

Streaming document ingestion

Persistent vector storage to avoid reprocessing

Scales to large document collections

🐛 Troubleshooting
Dependency Issues
bash
Copy code
pip install -r requirements.txt
API Key Issues
bash
Copy code
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('HUGGINGFACEHUB_API_TOKEN'))"
Vector Store Issues
If ChromaDB becomes inconsistent:

bash
Copy code
rm -rf chroma_db/
Re-run the ingestion pipeline after cleanup.

🚧 END
