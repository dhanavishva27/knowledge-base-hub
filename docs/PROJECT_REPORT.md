# Knowledge Base Hub — Project Report

## 1. Introduction

Knowledge Base Hub is an AI-powered web application designed to convert a collection of web URLs into a searchable knowledge base.

The system combines web scraping, document processing, semantic embeddings, vector similarity search, Retrieval-Augmented Generation, and a local Large Language Model.

The application is implemented using Django and Django REST Framework, with SQLite for application storage, FAISS for vector search, Sentence Transformers for embeddings, and Ollama for local LLM inference.

## 2. Problem Statement

Information about organizations, executives, products, and other entities can be distributed across many web pages.

A normal keyword search may fail when a user's wording differs from the wording used by the source document.

The project addresses this by converting documents and questions into semantic vector representations and retrieving information based on similarity of meaning.

## 3. Objectives

- Accept URL collections through CSV/XLSX files.
- Scrape and store web content.
- Clean and process scraped HTML.
- Divide content into searchable chunks.
- Generate semantic embeddings.
- Build a FAISS vector index.
- Retrieve relevant information using natural-language questions.
- Use RAG to provide context to a local LLM.
- Return answers with source information.
- Provide REST APIs and a web interface.

## 4. Proposed System

The proposed system consists of an ingestion pipeline and a query pipeline.

### Ingestion

```text
CSV/XLSX
   ↓
URL Extraction
   ↓
SQLite
   ↓
Scraping
   ↓
Clean Text
   ↓
Chunking
   ↓
Embeddings
   ↓
FAISS
```

### Query

```text
Question
   ↓
Question Embedding
   ↓
FAISS Retrieval
   ↓
Relevant Chunks
   ↓
RAG Context
   ↓
Ollama
   ↓
Answer + Sources
```

## 5. Technology Stack

| Technology | Role |
|---|---|
| Python | Core programming language |
| Django | Web application |
| Django REST Framework | REST APIs |
| SQLite | Persistent application data |
| Requests | HTTP scraping |
| BeautifulSoup | HTML parsing |
| OpenPyXL | XLSX processing |
| Sentence Transformers | Embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| FAISS | Vector similarity search |
| Ollama | Local LLM runtime |
| Llama 3.2 3B | Generative model |
| HTML/CSS/JavaScript | Frontend |
| Git/GitHub | Version control |

## 6. Data Model

### URLDocument

Stores source and scraped document information:

- URL
- HTTP status
- title
- raw HTML
- clean text
- scraping timestamp
- timestamps for record management

### DocumentChunk

Stores smaller searchable pieces of each successful document:

- source document
- chunk index
- chunk content
- creation timestamp

## 7. Web Scraping

The scraper uses Requests with a browser-like User-Agent and follows redirects.

BeautifulSoup parses returned HTML.

Script, style, and noscript elements are removed before converting the page into clean text.

HTTP failures are retained as status information and are not indexed as valid content.

## 8. Chunking Strategy

The current implementation uses:

```text
Chunk size = 500 words
Overlap = 50 words
```

Overlap helps preserve context between adjacent chunks.

## 9. Embedding Strategy

The application uses the pretrained:

```text
all-MiniLM-L6-v2
```

model.

Each chunk is represented as a 384-dimensional normalized vector.

No model training or fine-tuning is performed.

## 10. Vector Search

FAISS is used to perform similarity search.

The system stores:

1. Vector index
2. Mapping from FAISS index positions to `DocumentChunk` IDs

When a query arrives, its embedding is compared with the stored vectors and the most relevant chunks are retrieved.

## 11. RAG Implementation

RAG means Retrieval-Augmented Generation.

The project first retrieves relevant chunks and then passes them to the LLM as context.

The LLM is instructed to use only the supplied context and to report when the requested information is not available.

This avoids requiring model retraining whenever the knowledge base changes.

## 12. Local LLM

Ollama is used to run:

```text
llama3.2:3b
```

locally.

The application sends a prompt containing:

- instructions
- retrieved context
- user question

The generated answer is returned to the application.

## 13. REST API

The system provides:

```text
GET /api/urls/
GET /api/search/?q=<question>
```

The first exposes harvested URL data.

The second executes the semantic retrieval and RAG pipeline.

## 14. User Interface

The frontend provides:

### Search Page

Users can enter natural-language questions and receive:

- generated answer
- source URLs
- page titles
- similarity information

### Upload Page

Users can upload CSV/XLSX URL lists and trigger ingestion.

## 15. Results

The completed system demonstrates an end-to-end workflow:

```text
URL File
   ↓
Web Content
   ↓
Structured Storage
   ↓
Semantic Index
   ↓
Natural-Language Search
   ↓
Retrieved Evidence
   ↓
LLM Answer
```

The semantic search component was tested using a leadership-related question and successfully retrieved the relevant Apple leadership content among the top results.

## 16. Limitations

- Some websites return 403/404 or other HTTP failures.
- JavaScript-rendered content may not be available through simple HTTP requests.
- The current vector index is rebuilt rather than incrementally updated.
- Ollama and the model must be available locally.
- SQLite is intended for this assignment/local environment rather than high-concurrency production use.

## 17. Future Enhancements

- Incremental indexing
- Scheduled crawling
- Background workers
- Playwright-based browser scraping
- Hybrid search
- Reranking
- PostgreSQL
- Authentication
- Docker deployment
- Cloud deployment
- Monitoring
- Automated retrieval evaluation
- Conversation history
- Streaming responses

## 18. Conclusion

Knowledge Base Hub demonstrates how web data can be transformed into a searchable AI knowledge base.

The project combines traditional backend development with modern AI techniques:

```text
Web Scraping
+
Data Storage
+
Chunking
+
Embeddings
+
Vector Search
+
RAG
+
Local LLM
+
REST API
+
Web UI
```

The final application provides a practical foundation for building domain-specific knowledge assistants without requiring model fine-tuning for every new document.
