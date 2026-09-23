import json
import os

from kb.models import DocumentChunk

from .embeddings import generate_embeddings
from .vector_store import FAISSVectorStore


INDEX_DIR = "faiss_index"

INDEX_FILE = os.path.join(
    INDEX_DIR,
    "index.faiss"
)

MAPPING_FILE = os.path.join(
    INDEX_DIR,
    "mapping.json"
)


def build_vector_index():

    chunks = list(
        DocumentChunk.objects
        .exclude(content="")
        .order_by("id")
    )

    if not chunks:
        raise ValueError(
            "No document chunks found."
        )

    texts = [
        chunk.content
        for chunk in chunks
    ]

    print(
        f"Generating embeddings for {len(texts)} chunks..."
    )

    embeddings = generate_embeddings(texts)

    store = FAISSVectorStore(
        dimension=embeddings.shape[1]
    )

    store.add_embeddings(embeddings)

    os.makedirs(
        INDEX_DIR,
        exist_ok=True
    )

    store.save(INDEX_FILE)

    mapping = {
        str(index): chunk.id
        for index, chunk in enumerate(chunks)
    }

    with open(
        MAPPING_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            mapping,
            file,
            indent=2
        )

    return {
        "chunks": len(chunks),
        "dimension": embeddings.shape[1]
    }