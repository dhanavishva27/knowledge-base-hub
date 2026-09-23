import json

from kb.models import DocumentChunk

from .embeddings import generate_embeddings
from .vector_store import FAISSVectorStore
from .indexer import INDEX_FILE, MAPPING_FILE


def search_documents(query, top_k=5):

    # Load FAISS index
    store = FAISSVectorStore.load(
        INDEX_FILE
    )

    # Convert the user's question into an embedding
    query_embedding = generate_embeddings(
        [query]
    )

    # Search FAISS
    scores, indices = store.search(
        query_embedding,
        top_k=top_k
    )

    # Load FAISS → database ID mapping
    with open(
        MAPPING_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

    results = []

    for score, index in zip(
        scores[0],
        indices[0]
    ):

        # FAISS returns -1 when there is no result
        if index == -1:
            continue

        chunk_id = mapping.get(
            str(index)
        )

        if chunk_id is None:
            continue

        try:
            chunk = DocumentChunk.objects.get(
                id=chunk_id
            )
        except DocumentChunk.DoesNotExist:
            continue

        results.append({
            "score": float(score),
            "chunk_id": chunk.id,
            "document_id": chunk.document.id,
            "url": chunk.document.url,
            "title": chunk.document.title,
            "content": chunk.content,
        })

    return results