# Knowledge Base Hub from CSV URLs

## 1. Introduction

The Knowledge Base Hub is a web-based knowledge retrieval system that collects information from URLs provided through a CSV or Excel file and makes that information searchable using natural language.

The system follows a Retrieval-Augmented Generation (RAG) approach. Web pages are scraped, cleaned, divided into smaller chunks, converted into numerical embeddings, and stored in a FAISS vector index. When a user asks a question, the system retrieves the most relevant content and provides it as context to a locally running Large Language Model (LLM).

The application is developed using Django and Django REST Framework, with SQLite for application data storage, FAISS for vector search, Sentence Transformers for embeddings, and Ollama for local LLM-based answer generation.

## 2. Objectives

- Allow users to upload CSV or Excel files containing URLs.
- Extract URLs automatically from uploaded files.
- Scrape and store web page content.
- Store raw HTML, cleaned text, HTTP status, title, and timestamps.
- Divide large web documents into smaller searchable chunks.
- Generate embeddings for document chunks.
- Store embeddings in a FAISS vector index.
- Provide semantic search using natural-language questions.
- Use a local LLM to generate answers from retrieved information.
- Provide REST APIs for accessing stored URLs and search results.
- Provide a simple web interface for uploading URLs and asking questions.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Web application framework |
| Django REST Framework | REST API development |
| SQLite | Database for URLs and scraped content |
| Requests | Sending HTTP requests to websites |
| BeautifulSoup | HTML parsing and text extraction |
| Sentence Transformers | Generating text embeddings |
| all-MiniLM-L6-v2 | Pre-trained embedding model |
| FAISS | Vector storage and similarity search |
| Ollama | Running the local LLM |
| Llama 3.2 3B | Local language model |
| HTML/CSS/JavaScript | Frontend interface |
| Git/GitHub | Version control and project hosting |

## 4. System Architecture

```text
CSV / XLSX File
      |
      v
URL Extraction
      |
      v
SQLite Database
      |
      v
Web Scraping
      |
      v
Raw HTML + Clean Text
      |
      v
Document Chunking
      |
      v
Sentence Transformer
      |
      v
Embeddings
      |
      v
FAISS Vector Index
      |
      v
User Natural-Language Query
      |
      v
Query Embedding
      |
      v
FAISS Semantic Search
      |
      v
Relevant Document Chunks
      |
      v
RAG Context
      |
      v
Local LLM (Ollama)
      |
      v
Generated Answer + Sources
```

### 4.1 Data Storage

SQLite stores the original application data and scraped content.

The `URLDocument` model stores URL, HTTP status code, page title, raw HTML, cleaned text, scraping timestamp, content hash, and creation/update timestamps.

The `DocumentChunk` model stores smaller sections of cleaned documents and maintains a relationship with the original URL document.

### 4.2 Vector Search

Documents are divided into chunks. Each chunk is converted into a 384-dimensional vector using the `all-MiniLM-L6-v2` Sentence Transformer model.

FAISS uses these vectors to perform similarity search. A JSON mapping connects FAISS vector positions to database chunk IDs.

### 4.3 Retrieval-Augmented Generation

1. The user enters a natural-language question.
2. The question is converted into an embedding.
3. FAISS searches for similar document chunks.
4. The top relevant chunks are retrieved.
5. Retrieved chunks are combined into context.
6. The context and question are sent to the local LLM.
7. The LLM generates an answer using the supplied context.
8. Source URLs and similarity scores are returned.

## 5. Implementation

### 5.1 URL Upload

The application supports `.csv` and `.xlsx` files.

During upload:

1. The file format is validated.
2. The URL column is identified.
3. URLs are extracted.
4. Duplicate URLs are avoided using the database's unique URL constraint.
5. New URLs are stored in SQLite.
6. The ingestion pipeline is triggered.

### 5.2 Web Scraping

The scraper uses Python `requests` and BeautifulSoup.

For each URL, the system sends an HTTP request, records the status code, stores the raw HTML, extracts the page title, removes script/style/noscript elements, converts the remaining HTML into readable text, and stores the cleaned text.

Failed requests are recorded instead of stopping the complete ingestion process.

### 5.3 Document Chunking

Large documents are divided into smaller chunks before embedding.

Current configuration:
- Chunk size: 500 words
- Overlap: 50 words

The overlap helps preserve context between neighboring chunks.

### 5.4 Embedding Generation

The project uses the pre-trained `all-MiniLM-L6-v2` model from Sentence Transformers.

The embedding process does not train or fine-tune the model. The pre-trained model converts text into numerical representations that capture semantic meaning.

Each chunk produces a 384-dimensional vector.

### 5.5 FAISS Indexing

The generated embeddings are stored in a FAISS index.

A separate JSON mapping file connects each FAISS vector position to its corresponding database chunk ID.

The application searches FAISS, obtains matching vector positions, converts them to database chunk IDs, and retrieves the original chunk information from SQLite.

### 5.6 Semantic Search

The user's question is converted into an embedding and compared against stored document embeddings.

Example:

```text
Question:
"Who is the CEO of Apple?"
        |
        v
Query Embedding
        |
        v
FAISS Similarity Search
        |
        v
Relevant Apple Leadership Chunk
        |
        v
RAG Context
```

This allows the system to retrieve relevant information even when the wording of the query and document are not exactly the same.

### 5.7 Local LLM

Ollama is used to run `llama3.2:3b` locally.

The LLM receives the user's question, retrieved document context, and instructions to use only the supplied context. The prompt also instructs the model not to invent information when the answer cannot be found in the knowledge base.

### 5.8 Web Interface

The frontend provides:
- URL file upload
- Natural-language search
- Loading indication
- Generated answer display
- Source URL display
- Similarity scores
- Responsive layout

## 6. API Documentation

### 6.1 Search API

**Endpoint:**

```text
GET /api/search/?q=<question>
```

Example:

```text
/api/search/?q=Who%20is%20the%20CEO%20of%20Apple?
```

The API performs semantic retrieval, sends retrieved context to the local LLM, and returns the generated answer with source information.

Example response structure:

```json
{
  "answer": "Answer generated from the retrieved knowledge base.",
  "sources": [
    {
      "url": "https://example.com",
      "title": "Example Page",
      "score": 0.66
    }
  ]
}
```

### 6.2 URLs API

**Endpoint:**

```text
GET /api/urls/
```

This endpoint returns stored URL information including URL, HTTP status, page title, raw HTML, clean text, and metadata.

Example structure:

```json
[
  {
    "url": "https://example.com",
    "http_status": 200,
    "title": "Example Page",
    "raw_html": "...",
    "clean_text": "...",
    "metadata": {
      "scraped_at": "...",
      "created_at": "...",
      "updated_at": "..."
    }
  }
]
```

## 7. Difficulties Encountered

### 7.1 Website Access Restrictions

Some websites returned HTTP `403 Forbidden` responses because access to automated requests was restricted. Other URLs returned `404 Not Found` when the requested page was unavailable. The application records these HTTP statuses instead of treating them as application crashes.

### 7.2 Dynamic Web Content

Some modern websites depend on JavaScript to load content dynamically. A basic `requests` and BeautifulSoup scraper may not capture content that is generated only after browser-side JavaScript execution.

### 7.3 Different Website Structures

Different websites use different HTML structures. A universal scraper cannot assume that information will always be located in the same HTML elements. The implementation removes common non-content elements such as scripts and styles before extracting readable text.

### 7.4 Vector Search Integration

FAISS stores vectors rather than original document information. Therefore, an additional mapping between FAISS vector indexes and database chunk IDs was required.

### 7.5 Local LLM Integration

Running a language model locally requires system resources. Ollama was used to simplify local model execution and avoid depending on a paid external LLM API.

### 7.6 Keeping the Search Index Updated

When scraped content changes, the corresponding chunks and embeddings also need to be regenerated. The ingestion pipeline recreates chunks and rebuilds the vector index from the current database content.

## 8. Other Observations

- SQLite and FAISS serve different purposes: SQLite stores application data and scraped content, while FAISS performs vector similarity search.
- `all-MiniLM-L6-v2` provides a lightweight embedding solution suitable for a small knowledge base.
- The embedding model and LLM are pre-trained models; this project does not perform model fine-tuning.
- Semantic search allows users to ask questions using natural language instead of requiring exact keyword matches.
- The RAG prompt instructs the LLM to use retrieved context and avoid inventing information.
- REST APIs allow backend functionality to be accessed independently of the frontend.
- The current implementation is suitable for a small-to-medium prototype knowledge base.
- Websites with strong bot protection or client-side rendering may require additional scraping techniques.

## 9. Future Enhancements

### 9.1 JavaScript-Rendered Website Support

Integrate browser automation tools such as Playwright or Selenium to retrieve content from websites that depend heavily on JavaScript.

### 9.2 Scheduled Scraping

Add scheduled jobs to automatically re-scrape stored URLs at regular intervals and keep the knowledge base up to date.

### 9.3 Incremental Indexing

Instead of rebuilding the complete FAISS index after every ingestion, update only documents whose content has changed.

### 9.4 Improved Chunking

Implement semantic, heading-based, or sentence-aware chunking to improve retrieval quality.

### 9.5 Metadata Filtering

Allow users to filter results by company, website, document type, date, or other metadata.

### 9.6 Structured Person Information

Improve extraction of person-related information such as name, designation, company, biography, department, and leadership role.

### 9.7 Authentication and Authorization

Add user authentication and role-based access control for administrators and normal users.

### 9.8 Production Vector Database

For a much larger knowledge base, FAISS can be replaced or complemented with a production-oriented vector database such as Milvus.

### 9.9 Improved LLM Support

Add support for larger or more capable local models when sufficient hardware resources are available.

### 9.10 Search Quality Evaluation

Introduce evaluation metrics such as retrieval precision, recall, and answer quality to measure and improve the RAG system.

### 9.11 Content Change Detection

Use content hashes to detect whether a webpage has changed before re-processing and generating new embeddings.

### 9.12 Cloud Deployment

Deploy the application to a cloud environment so that it can be accessed remotely and used by multiple users.

## 10. Conclusion

The Knowledge Base Hub demonstrates an end-to-end implementation of a web-based Retrieval-Augmented Generation system.

The project combines web scraping, structured data storage, document processing, embeddings, vector similarity search, REST APIs, and a local LLM into a single application.

The system can accept URLs through CSV or Excel files, collect and process their content, index the information for semantic search, and answer natural-language questions using retrieved knowledge.

The project also demonstrates how RAG can be implemented without training a language model from scratch. Instead, pre-trained embedding and language models are combined with an external knowledge base to provide context-aware responses.

The current implementation provides a working foundation that can be extended with better web scraping, scheduled ingestion, incremental indexing, structured information extraction, authentication, evaluation, and cloud deployment.
