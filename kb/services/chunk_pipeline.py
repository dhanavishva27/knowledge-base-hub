from kb.models import URLDocument, DocumentChunk

from .chunker import chunk_text


def create_chunks_for_documents():

    # Only process successfully scraped documents
    documents = (
        URLDocument.objects
        .filter(
            status_code__gte=200,
            status_code__lt=300
        )
        .exclude(
            clean_text=""
        )
    )

    total_chunks = 0

    for document in documents:

        # Remove previous chunks
        document.chunks.all().delete()

        chunks = chunk_text(
            document.clean_text
        )

        for chunk in chunks:

            DocumentChunk.objects.create(
                document=document,
                chunk_index=chunk["chunk_index"],
                content=chunk["content"]
            )

            total_chunks += 1

    return total_chunks