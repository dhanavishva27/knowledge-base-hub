# Knowledge Base Hub — API Documentation

## Base URL

Local development:

```text
http://127.0.0.1:8000
```

## 1. Get URL Documents

### Endpoint

```http
GET /api/urls/
```

### Purpose

Returns stored URL records and their scraped information.

### Example

```text
http://127.0.0.1:8000/api/urls/
```

### Response Structure

```json
[
  {
    "url": "https://example.com",
    "http_status": 200,
    "title": "Example",
    "raw_html": "<html>...</html>",
    "clean_text": "Example page content...",
    "metadata": {
      "scraped_at": "2026-09-23T10:00:00Z",
      "created_at": "2026-09-23T09:00:00Z",
      "updated_at": "2026-09-23T10:00:00Z"
    }
  }
]
```

## 2. Search Knowledge Base

### Endpoint

```http
GET /api/search/?q=<question>
```

### Example

```text
http://127.0.0.1:8000/api/search/?q=Who%20is%20the%20CEO%20of%20Apple?
```

### Processing

```text
Question
   ↓
Sentence Embedding
   ↓
FAISS Search
   ↓
Top Relevant Chunks
   ↓
Context Construction
   ↓
Ollama LLM
   ↓
Answer + Sources
```

### Example Response

```json
{
  "answer": "Answer generated from the retrieved knowledge base context.",
  "sources": [
    {
      "url": "https://example.com",
      "title": "Example",
      "score": 0.66
    }
  ]
}
```

### Missing Query

Request:

```text
GET /api/search/
```

Response status:

```text
400 Bad Request
```

Example:

```json
{
  "error": "Please provide a search query using ?q="
}
```

### Server/Processing Error

If retrieval or generation fails, the API returns:

```text
500 Internal Server Error
```

Example:

```json
{
  "error": "Search failed: ..."
}
```

## 3. Upload Page

The upload interface is available at:

```http
GET/POST /upload/
```

It accepts:

- CSV
- XLSX

The file must contain a `URL` column.

Successful upload triggers the ingestion pipeline.

## 4. Home Page

```http
GET /
```

Provides the natural-language search interface.

## 5. Admin

```http
GET /admin/
```

Provides Django Admin access for managing stored URL documents.

## 6. API Design Notes

The APIs are implemented using Django REST Framework's `@api_view`.

The `/api/urls/` endpoint exposes stored document information.

The `/api/search/` endpoint connects the semantic retrieval layer with the RAG generation layer.
