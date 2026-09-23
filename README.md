# Knowledge Base Hub

A web-based knowledge management and question-answering system that collects information from URLs provided through CSV/XLSX files, stores the scraped content, converts the content into semantic vector representations, and allows users to search the knowledge base using natural-language questions.

The application uses Retrieval-Augmented Generation (RAG) with a local LLM through Ollama to generate answers from retrieved knowledge-base content.

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [How the System Works](#how-the-system-works)
- [Database Design](#database-design)
- [RAG Pipeline](#rag-pipeline)
- [REST API](#rest-api)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Using the Application](#using-the-application)
- [Example Workflow](#example-workflow)
- [Error Handling and Limitations](#error-handling-and-limitations)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)

## Project Overview

Knowledge Base Hub is an end-to-end application that combines web scraping, document processing, vector search, and generative AI.

Users provide a collection of URLs through a CSV or Excel file. The application processes those URLs, extracts useful text, stores the collected information, divides documents into smaller chunks, generates embeddings, and indexes the embeddings using FAISS.

When a user asks a question, the application searches the vector index for semantically relevant content. The retrieved content is then passed to a local LLM running through Ollama. The LLM generates a natural-language answer using the retrieved context.

### High-Level Flow

```text
CSV / XLSX
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
Semantic Search
    |
    v
Relevant Context
    |
    v
Ollama / Llama 3.2
    |
    v
Generated Answer
    |
    v
Web UI / REST API
```

## Problem Statement

Information available across multiple websites can be difficult to search and understand efficiently.

Traditional keyword search mainly looks for matching words. It may fail when the user asks a question using different words from those used in the source document.

Knowledge Base Hub addresses this by collecting information from user-provided URLs, processing the content, generating semantic embeddings, retrieving relevant chunks, and using an LLM to formulate a natural-language answer.

## Objectives

- Build a URL-based knowledge ingestion system.
- Support both CSV and XLSX input files.
- Scrape and process web content.
- Store scraped information in a relational database.
- Split large documents into smaller chunks.
- Generate semantic embeddings.
- Perform vector similarity search.
- Implement Retrieval-Augmented Generation.
- Use a local LLM instead of requiring a paid external LLM API.
- Provide REST APIs for accessing the knowledge base.
- Build a simple user-friendly web interface.
- Display source URLs along with generated answers.

## Key Features

### 1. CSV/XLSX Upload

Users can upload `.csv` or `.xlsx` files. The input file must contain a column named `URL`.

Example:

```text
URL
https://www.apple.com/in/leadership/
https://www.oracle.com/in/corporate/executives/
```

Duplicate URLs are not inserted because the URL field is unique.

### 2. Web Scraping

The application uses Requests and BeautifulSoup to collect:

- HTTP status code
- Page title
- Raw HTML
- Clean text

JavaScript, CSS, and `noscript` elements are removed before extracting readable text.

### 3. SQLite Storage

SQLite stores:

- URL
- HTTP status
- title
- raw HTML
- clean text
- scraping timestamp
- document chunks

### 4. Document Chunking

Large web pages are divided into smaller pieces.

Current configuration:

```text
Chunk size: 500 words
Overlap: 50 words
```

Example:

```text
Chunk 1: words 1 - 500
Chunk 2: words 451 - 950
Chunk 3: words 901 - 1400
```

### 5. Semantic Embeddings

The project uses:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers.

Each chunk is converted into a 384-dimensional vector.

### 6. FAISS Vector Search

FAISS is used for similarity search. The project uses an inner-product index with normalized embeddings.

A mapping file connects FAISS vector positions to database chunk IDs.

### 7. Local LLM

The project uses Ollama to run a local language model.

Current model:

```text
llama3.2:3b
```

The model receives the retrieved document context and the user's question.

### 8. Retrieval-Augmented Generation

The RAG process is:

```text
User Question
      |
      v
Question Embedding
      |
      v
FAISS Similarity Search
      |
      v
Relevant Document Chunks
      |
      v
Context Construction
      |
      v
Local LLM
      |
      v
Final Answer
```

### 9. Source Display

Search results include:

- Source URL
- Page title
- Similarity score

### 10. REST API

The application provides:

```text
GET /api/urls/
GET /api/search/?q=...
```

## System Architecture

```text
                         +------------------+
                         |   CSV / XLSX     |
                         |    URL File      |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |  URL Extraction  |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |      SQLite      |
                         |   URLDocument    |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |   Web Scraper    |
                         | Requests + BS4   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |   Clean Text     |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Chunking      |
                         | 500 words /      |
                         | 50 overlap       |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |   Embeddings     |
                         | MiniLM-L6-v2     |
                         | 384 dimensions   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |      FAISS       |
                         |  Vector Index    |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Semantic Search  |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Relevant Context |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Ollama / Llama   |
                         |     3.2:3b       |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Generated Answer |
                         +------------------+
```

## Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Django |
| REST Framework | Django REST Framework |
| Database | SQLite |
| Web Scraping | Requests |
| HTML Parsing | BeautifulSoup |
| Excel Processing | OpenPyXL |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| LLM Runtime | Ollama |
| LLM Model | Llama 3.2 3B |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git / GitHub |

## Project Structure

```text
knowledge-base-hub/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── data/
│   └── Leadership_URL.xlsx
│
├── kb/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_documentchunk.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chunk_pipeline.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── indexer.py
│   │   ├── ingestion.py
│   │   ├── llm.py
│   │   ├── rag.py
│   │   ├── scraper.py
│   │   ├── search.py
│   │   └── vector_store.py
│   │
│   ├── templates/
│   │   └── kb/
│   │       ├── home.html
│   │       └── upload.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

Runtime files such as the SQLite database, virtual environment, Python cache files, and FAISS index are excluded from Git where appropriate.

## How the System Works

### Step 1: Upload URLs

The user opens:

```text
http://127.0.0.1:8000/upload/
```

and uploads a CSV or XLSX file.

The application checks the file type and searches for a `URL` column. Each non-empty URL is stored as a `URLDocument`.

### Step 2: Scraping

The ingestion pipeline sends an HTTP request to every stored URL.

For successful responses, it extracts:

```text
Title
Raw HTML
Clean Text
HTTP Status Code
```

Unsuccessful HTTP responses such as 403 or 404 are recorded but are not indexed as usable knowledge content.

### Step 3: Cleaning

BeautifulSoup parses the HTML and removes elements such as:

```text
<script>
<style>
<noscript>
```

The remaining HTML is converted into plain text.

### Step 4: Chunking

The cleaned document is divided into overlapping chunks. Each chunk receives an index and is stored in the `DocumentChunk` table.

### Step 5: Embedding Generation

Each chunk is passed to:

```text
SentenceTransformer("all-MiniLM-L6-v2")
```

The model converts the text into a 384-value vector. The embeddings are normalized before being inserted into FAISS.

### Step 6: Building the FAISS Index

The application creates a FAISS index using the embedding dimension. It also creates a mapping between FAISS vector positions and database chunk IDs.

## Database Design

### URLDocument

| Field | Purpose |
|---|---|
| `url` | Source URL |
| `status_code` | HTTP response status |
| `title` | Web page title |
| `raw_html` | Original HTML response |
| `clean_text` | Extracted readable text |
| `scraped_at` | Last scraping time |
| `content_hash` | Field available for future change detection |
| `created_at` | Record creation time |
| `updated_at` | Record update time |

### DocumentChunk

| Field | Purpose |
|---|---|
| `document` | Related URLDocument |
| `chunk_index` | Position of the chunk |
| `content` | Chunk text |
| `created_at` | Chunk creation time |

Relationship:

```text
URLDocument
     |
     +---- DocumentChunk
     |
     +---- DocumentChunk
     |
     +---- DocumentChunk
```

## RAG Pipeline

RAG stands for Retrieval-Augmented Generation.

Instead of asking the LLM to answer using only its pretrained knowledge, the application first retrieves relevant information from the project's knowledge base.

```text
User Question
      |
      v
Generate Query Embedding
      |
      v
FAISS Similarity Search
      |
      v
Top Relevant Chunks
      |
      v
Build Context
      |
      v
Ollama / Llama 3.2
      |
      v
Generated Answer
```

The LLM is instructed to answer using only the provided context and to say when the answer is not found in the knowledge base.

### Does the Project Train the LLM?

No.

The project does not fine-tune or train Llama 3.2. It uses a pretrained model and supplies relevant information at inference time through RAG.

The embedding model is also used as a pretrained model.

## REST API

### Get All URLs

```http
GET /api/urls/
```

Example:

```text
http://127.0.0.1:8000/api/urls/
```

Returns URL information including:

- URL
- HTTP status
- title
- raw HTML
- clean text
- metadata

### Search Knowledge Base

```http
GET /api/search/?q=<question>
```

Example:

```text
http://127.0.0.1:8000/api/search/?q=Who%20is%20the%20CEO%20of%20Apple?
```

Processing:

```text
GET Request
    |
    v
Question
    |
    v
Embedding
    |
    v
FAISS Search
    |
    v
Top Relevant Chunks
    |
    v
LLM Context
    |
    v
Generated Answer
```

Example response structure:

```json
{
  "answer": "The answer generated from the retrieved knowledge base context.",
  "sources": [
    {
      "url": "https://example.com",
      "title": "Example",
      "score": 0.66
    }
  ]
}
```

## Installation

### Prerequisites

Install:

- Python 3.12 or compatible
- Git
- Ollama

### Clone the Repository

```bash
git clone https://github.com/dhanavishva27/knowledge-base-hub.git
cd knowledge-base-hub
```

### Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Database Setup

```powershell
python manage.py migrate
```

### Start Ollama

Install Ollama and make sure it is running.

Pull the model:

```powershell
ollama pull llama3.2:3b
```

Optional verification:

```powershell
ollama run llama3.2:3b
```

### Run Django

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Using the Application

### Upload Data

1. Open the Upload page.
2. Select a `.csv` or `.xlsx` file.
3. Ensure the file contains a `URL` column.
4. Submit the file.
5. URLs are stored in SQLite.
6. The ingestion pipeline scrapes the URLs.
7. Successful content is chunked.
8. Embeddings are generated.
9. FAISS is built from the available chunks.

### Search

Open:

```text
http://127.0.0.1:8000/
```

Enter a natural-language question, for example:

```text
Who is the CEO of Apple?
```

The application:

1. Converts the question into an embedding.
2. Searches FAISS.
3. Retrieves relevant chunks.
4. Builds the LLM context.
5. Sends the context and question to Ollama.
6. Generates an answer.
7. Displays the answer and sources.

## Example End-to-End Workflow

```text
User uploads Leadership_URL.xlsx
              |
              v
Application extracts URLs
              |
              v
URLs stored in SQLite
              |
              v
URLs scraped
              |
              v
HTML converted to clean text
              |
              v
Text split into chunks
              |
              v
Chunks converted to 384-D embeddings
              |
              v
Embeddings indexed in FAISS
              |
              v
User asks:
"Who is the CEO of Apple?"
              |
              v
Question converted to embedding
              |
              v
FAISS retrieves relevant chunks
              |
              v
Retrieved chunks become LLM context
              |
              v
Ollama / Llama 3.2 generates answer
              |
              v
Answer + Sources displayed
```

## Why Use FAISS?

Traditional SQL keyword search depends mainly on matching words.

Semantic search instead compares vector representations of meaning.

For example, a user can ask:

```text
Who leads Apple?
```

even if the source page uses terminology such as:

```text
Apple Leadership
```

This allows the system to retrieve semantically related content rather than relying only on exact keyword matches.

## Why Use Sentence Transformers?

The system needs to convert text into numerical representations that preserve semantic meaning.

Sentence Transformers provides pretrained models for this purpose.

`all-MiniLM-L6-v2` is used because it is relatively small and fast while producing useful sentence-level embeddings.

## Why Use RAG?

An LLM does not automatically know the contents of the URLs collected by this application.

RAG connects the LLM to the project's own knowledge base:

```text
LLM
+
Retrieved Knowledge
=
Context-Aware Answer
```

The project therefore does not need to retrain the LLM every time new documents are added.

## Error Handling

### Invalid Upload

Only `.csv` and `.xlsx` files are accepted.

### Missing URL Column

If the file does not contain a `URL` column, the upload is rejected with an error message.

### HTTP Errors

Websites can return:

```text
403 Forbidden
404 Not Found
500 Server Error
```

These responses are recorded rather than treated as successful knowledge content.

### Empty Pages

If a successful HTTP response contains no readable text, it is not treated as usable knowledge content.

### LLM/Search Errors

Errors during retrieval or local LLM generation are returned by the search API instead of silently producing an invalid answer.

## Current Limitations

### Dynamic Websites

Some websites generate content using JavaScript. A simple HTTP request may not receive all browser-rendered content.

A future version could use Playwright for such pages.

### Access Restrictions

Some websites may reject automated requests. The application records such failures rather than attempting to bypass access controls.

### FAISS Rebuilding

The current indexing pipeline rebuilds the FAISS index from available chunks. For very large datasets, incremental indexing would be more efficient.

### Local LLM Requirements

Ollama and the selected model must be available on the machine running the application.

### SQLite Scalability

SQLite is suitable for this assignment and local development. A production system with many concurrent users could use PostgreSQL.

## Future Improvements

- Incremental vector indexing
- Background scraping using Celery
- Scheduled URL refresh
- URL content change detection
- Better HTML/document parsing
- JavaScript rendering with Playwright
- Hybrid keyword + semantic search
- Retrieval reranking
- Metadata-aware retrieval
- PostgreSQL integration
- Authentication and authorization
- User-specific knowledge bases
- Docker deployment
- Cloud deployment
- Monitoring and logging
- Automated retrieval evaluation
- Conversation history
- Streaming LLM responses

## Learning Outcomes

This project demonstrates practical understanding of:

- Django application development
- Django REST Framework
- REST API design
- Web scraping
- HTML parsing
- Data ingestion pipelines
- SQLite
- Document chunking
- NLP
- Sentence embeddings
- Vector search
- FAISS
- Semantic search
- Retrieval-Augmented Generation
- Local LLM deployment
- Ollama
- Frontend-backend integration
- Git and GitHub

## Main Service Modules

| File | Responsibility |
|---|---|
| `scraper.py` | Downloads and parses web pages |
| `chunker.py` | Splits clean text into overlapping chunks |
| `chunk_pipeline.py` | Creates database chunks |
| `embeddings.py` | Generates Sentence Transformer embeddings |
| `vector_store.py` | Provides FAISS storage/search abstraction |
| `indexer.py` | Builds and saves the FAISS index and mapping |
| `search.py` | Performs semantic retrieval |
| `llm.py` | Communicates with Ollama |
| `rag.py` | Connects retrieval with generation |
| `ingestion.py` | Coordinates scraping, chunking, and indexing |

## Development Commands

Check Django configuration:

```powershell
python manage.py check
```

Create migrations:

```powershell
python manage.py makemigrations
```

Apply migrations:

```powershell
python manage.py migrate
```

Run the development server:

```powershell
python manage.py runserver
```

Open the Django shell:

```powershell
python manage.py shell
```

## Screenshots and Demonstration

Recommended screenshots for the project submission:

1. Home/Search page
2. URL upload page
3. Successful ingestion result
4. Search query
5. Generated RAG answer
6. Retrieved source documents
7. `/api/urls/` response
8. `/api/search/` response
9. Django Admin page

Suggested demo sequence:

```text
Open application
    ↓
Upload URL file
    ↓
Show ingestion result
    ↓
Enter natural-language question
    ↓
Show generated answer
    ↓
Show sources
    ↓
Open REST API
```

## GitHub Repository

Repository:

https://github.com/dhanavishva27/knowledge-base-hub

Typical Git workflow:

```powershell
git status
git add .
git commit -m "Describe the change"
git push
```

## Conclusion

Knowledge Base Hub demonstrates an end-to-end AI-powered knowledge retrieval system by combining:

```text
Django
   +
Web Scraping
   +
SQLite
   +
Document Processing
   +
Sentence Embeddings
   +
FAISS
   +
Semantic Search
   +
RAG
   +
Ollama
   +
REST API
   +
Web UI
```

The system transforms a collection of web URLs into a searchable knowledge base and allows users to ask natural-language questions about the collected information.

