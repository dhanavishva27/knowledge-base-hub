def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):
    words = text.split()

    if not words:
        return []

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        chunks.append({
            "chunk_index": chunk_index,
            "content": chunk
        })

        chunk_index += 1

        start += chunk_size - overlap

    return chunks