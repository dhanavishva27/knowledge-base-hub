# Scripts

The main processing scripts are implemented inside `kb/services/`.

## Scraping

`scraper.py`

Downloads URLs and extracts:

- HTTP status
- Page title
- Raw HTML
- Clean text

## Chunking

`chunker.py`

Splits clean text into 500-word chunks with 50-word overlap.

## Chunk Pipeline

`chunk_pipeline.py`

Creates and stores `DocumentChunk` records in SQLite.

## Embeddings

`embeddings.py`

Uses `all-MiniLM-L6-v2` to generate 384-dimensional embeddings.

## Vector Indexing

`indexer.py`

Creates the FAISS vector index and maintains the mapping between FAISS vector positions and database chunk IDs.

## Semantic Search

`search.py`

Converts a user question into an embedding and retrieves the most relevant chunks from FAISS.

## LLM

`llm.py`

Communicates with the local Ollama Llama 3.2 3B model.

## RAG

`rag.py`

Combines semantic retrieval with LLM generation.

## Ingestion Pipeline

`ingestion.py`

Coordinates:

```text
Scraping
   ↓
Chunking
   ↓
Embedding
   ↓
FAISS Indexing
