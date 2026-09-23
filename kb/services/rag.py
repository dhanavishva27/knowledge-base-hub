from .search import search_documents
from .llm import generate_answer


def answer_question(question, top_k=3):

    # Step 1: Retrieve relevant chunks
    results = search_documents(
        question,
        top_k=top_k
    )

    if not results:
        return {
            "answer": "No relevant information was found.",
            "sources": []
        }

    # Step 2: Build context
    context_parts = []

    for result in results:

        context_parts.append(
            f"""
Source: {result['url']}
Title: {result['title']}

Content:
{result['content']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    # Step 3: Generate answer using LLM
    answer = generate_answer(
        question,
        context
    )

    # Step 4: Return answer + sources
    sources = [
        {
            "url": result["url"],
            "title": result["title"],
            "score": result["score"]
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources
    }