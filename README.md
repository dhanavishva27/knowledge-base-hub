# Knowledge Base Hub

A web-based knowledge management system that collects information from URLs provided through CSV/XLSX files, stores the scraped content, creates semantic vector representations, and allows users to search the knowledge base using natural-language questions.

The system uses Retrieval-Augmented Generation (RAG) with a local LLM to generate answers based only on the retrieved knowledge-base content.

---

## Features

- Upload URLs through CSV or XLSX files
- Automatically scrape web pages
- Store scraped content in SQLite
- Extract clean text from HTML
- Split documents into smaller chunks
- Generate semantic embeddings using Sentence Transformers
- Store embeddings in FAISS
- Perform semantic similarity search
- Generate answers using a local LLM through Ollama
- Display source URLs for generated answers
- REST APIs for URL data and search
- Django-based web interface
- Django Admin interface for managing documents

---

## Architecture

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
Web Scraper
(Requests + BeautifulSoup)
     |
     v
Clean Text
     |
     v
Document Chunking
     |
     v
Sentence Transformer
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
Ollama Local LLM
     |
     v
Generated Answer
     |
     v
Web UI / REST API

Technology Stack
Component	Technology
Backend	Django
REST API	Django REST Framework
Database	SQLite
Web Scraping	Requests, BeautifulSoup
Document Processing	Python
Embeddings	Sentence Transformers
Vector Database	FAISS
LLM	Ollama
LLM Model	Llama 3.2 3B
Frontend	HTML, CSS, JavaScript
Excel Processing	OpenPyXL
Version Control	Git / GitHub
Project Structure
knowledge-base-hub/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── kb/
│   ├── migrations/
│   ├── services/
│   │   ├── chunker.py
│   │   ├── chunk_pipeline.py
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
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
├── data/
│   └── Leadership_URL.xlsx
│
├── manage.py
├── requirements.txt
└── README.md
How the System Works
1. URL Upload

The user uploads a CSV or XLSX file containing a column named:

URL

Example:

URL
https://www.apple.com/in/leadership/
https://www.oracle.com/in/corporate/executives/

The application extracts the URLs and stores them in the SQLite database.

2. Web Scraping

The application sends an HTTP request to each URL.

The scraper collects:

HTTP status code
Page title
Raw HTML
Clean text

BeautifulSoup is used to remove elements such as:

JavaScript
CSS
No-script content

The remaining page content is converted into readable text.

3. Document Chunking

Large documents are divided into smaller pieces.

The current chunking strategy uses:

Chunk size: 500 words
Overlap: 50 words

The overlap helps preserve context between neighboring chunks.

For example:

Chunk 1:
words 1 → 500

Chunk 2:
words 451 → 950

Chunk 3:
words 901 → 1400
4. Embeddings

Each document chunk is converted into a numerical vector using:

all-MiniLM-L6-v2

The model produces:

384-dimensional vectors

These vectors represent the semantic meaning of the text.

Similar meanings produce vectors that are closer together in vector space.

5. FAISS

FAISS is used for efficient similarity search.

The application stores the chunk embeddings in a FAISS index.

When a user asks:

Who is the CEO of Apple?

the question is also converted into an embedding.

FAISS then finds the chunks whose embeddings are most similar to the question.

6. Retrieval-Augmented Generation

The retrieved chunks are provided to the local LLM as context.

The flow is:

User Question
      |
      v
Question Embedding
      |
      v
FAISS Similarity Search
      |
      v
Relevant Chunks
      |
      v
Context
      |
      v
Ollama / Llama 3.2
      |
      v
Final Answer

The LLM is instructed to answer using only the retrieved context.

This reduces the possibility of generating information that is not present in the knowledge base.

REST API
Get All URLs
GET /api/urls/

Returns stored URL information including:

URL
HTTP status
title
raw HTML
clean text
metadata
Search Knowledge Base
GET /api/search/?q=your question

Example:

/api/search/?q=Who is the CEO of Apple?

The API performs:

Question
→ Embedding
→ FAISS Search
→ Context Retrieval
→ LLM
→ Answer

The response contains the generated answer and source information.

Running the Project
1. Clone the repository
git clone https://github.com/dhanavishva27/knowledge-base-hub.git
cd knowledge-base-hub
2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Apply migrations
python manage.py migrate
5. Start Ollama

Make sure Ollama is installed and the required model is available:

ollama pull llama3.2:3b
6. Start Django
python manage.py runserver

Open:

http://127.0.0.1:8000/
Main Pages
Home
/

Provides the natural-language search interface.

Upload
/upload/

Allows users to upload CSV/XLSX files containing URLs.

API
/api/urls/
/api/search/?q=...
Database Models
URLDocument

Stores information about each scraped URL.

Important fields include:

url
status_code
title
raw_html
clean_text
scraped_at
created_at
updated_at
DocumentChunk

Stores chunks generated from successfully scraped documents.

Important fields:

document
chunk_index
content
created_at
Why RAG?

A normal LLM answers using knowledge learned during its training.

This project instead uses:

Knowledge Base
      +
Retrieval
      +
LLM

The retrieval system first finds relevant information from the stored documents.

The LLM then uses that information to formulate the final response.

This makes the application suitable for answering questions about the specific content collected into the knowledge base.

Current Limitations
Some websites may return HTTP errors such as 403 or 404.
JavaScript-heavy websites may not expose all content through a normal HTTP request.
FAISS indexes need to be rebuilt when indexed document content changes.
Ollama requires the local LLM to be installed and running.
The current system primarily performs text-based retrieval.
Future Improvements

Possible improvements include:

Background scraping jobs using Celery
Scheduled URL re-crawling
Better duplicate detection
Incremental FAISS indexing
Metadata-aware retrieval
Hybrid keyword + semantic search
Better document parsing
Authentication and user accounts
PostgreSQL for production deployment
Docker deployment
Cloud-based vector databases
More advanced reranking models
