# Knowledge Base Hub — Architecture

## 1. Overview

Knowledge Base Hub is a Django-based knowledge retrieval application. It accepts URLs through CSV/XLSX files, scrapes the pages, stores the harvested content in SQLite, chunks the text, generates embeddings, indexes them with FAISS, retrieves relevant chunks for natural-language questions, and uses a local Ollama LLM to generate answers.

## 2. End-to-End Architecture

```text
CSV / XLSX
    |
    v
URL Extraction
    |
    v
SQLite (URLDocument)
    |
    v
Web Scraping
Requests + BeautifulSoup
    |
    v
Raw HTML + Clean Text
    |
    v
Document Chunking
500 words / 50-word overlap
    |
    v
Sentence Transformer
all-MiniLM-L6-v2
    |
    v
384-D Embeddings
    |
    v
FAISS Vector Index
    |
    v
Semantic Retrieval
    |
    v
Relevant Chunks
    |
    v
RAG Context
    |
    v
Ollama / Llama 3.2:3b
    |
    v
Answer + Sources
    |
    +------> Web UI
    |
    +------> REST API
```

## 3. Main Components

### Django
Provides the web application, URL routing, templates, database integration, and request handling.

### Django REST Framework
Provides the REST API endpoints.

### SQLite
Stores URL records, scraping results, and document chunks.

### Requests + BeautifulSoup
Requests downloads HTML pages. BeautifulSoup parses HTML and extracts readable text.

### Chunking
Clean text is divided into 500-word chunks with 50 words of overlap.

### Sentence Transformers
`all-MiniLM-L6-v2` converts text into 384-dimensional normalized embeddings.

### FAISS
FAISS stores and searches the embedding vectors using similarity search.

### Ollama
Runs the local Llama 3.2 3B model.

### RAG
Retrieves relevant document chunks before asking the LLM to generate an answer.

## 4. Data Flow

### Ingestion

```text
Upload File
    ↓
Read URL Column
    ↓
Create/Update URLDocument Records
    ↓
Scrape URLs
    ↓
Store HTTP Status, Title, Raw HTML, Clean Text
    ↓
Create DocumentChunk Records
    ↓
Generate Embeddings
    ↓
Build FAISS Index
    ↓
Save Vector-to-Chunk Mapping
```

### Search

```text
User Question
    ↓
Generate Question Embedding
    ↓
FAISS Similarity Search
    ↓
Retrieve DocumentChunk Records
    ↓
Build Context
    ↓
Send Context + Question to Ollama
    ↓
Return Answer + Sources
```

## 5. Important Design Decision

SQLite and FAISS have different responsibilities.

SQLite is the application database and stores the actual document information.

FAISS stores vector representations used for fast semantic similarity search.

The FAISS mapping file connects a vector position to a `DocumentChunk` database ID.

## 6. Project Services

| Module | Responsibility |
|---|---|
| `scraper.py` | Downloads and parses URLs |
| `chunker.py` | Splits text into chunks |
| `chunk_pipeline.py` | Stores chunks in SQLite |
| `embeddings.py` | Generates embeddings |
| `vector_store.py` | FAISS abstraction |
| `indexer.py` | Builds and saves FAISS index |
| `search.py` | Semantic retrieval |
| `llm.py` | Ollama communication |
| `rag.py` | Retrieval + generation |
| `ingestion.py` | Coordinates ingestion |

## 7. Error Flow

HTTP failures such as 403 and 404 are recorded as failed ingestion results. Failed pages are not treated as valid searchable knowledge.

If no usable chunks exist, vector indexing is skipped.

The search endpoint returns an error response if retrieval or LLM generation fails.

## 8. Scalability Considerations

The current implementation is designed for an academic/local project. Future production improvements could include:

- PostgreSQL
- Background jobs with Celery
- Incremental FAISS indexing
- Scheduled crawling
- Redis
- Playwright for JavaScript-heavy pages
- Authentication
- Containerization
- Monitoring
