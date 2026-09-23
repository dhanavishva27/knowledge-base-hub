from django.utils import timezone

from kb.models import URLDocument

from .scraper import scrape_url
from .chunk_pipeline import create_chunks_for_documents
from .indexer import build_vector_index


def scrape_all_documents():

    documents = URLDocument.objects.all()

    results = []

    for document in documents:

        result = scrape_url(
            document.url
        )

        document.status_code = (
            result["status_code"]
        )

        document.title = (
            result["title"]
        )

        document.raw_html = (
            result["raw_html"]
        )

        document.clean_text = (
            result["clean_text"]
        )

        document.scraped_at = (
            timezone.now()
        )

        document.save()

        # If scraping failed, remove old chunks
        if not result["success"]:

            document.chunks.all().delete()

        results.append({
            "url": document.url,
            "success": result["success"],
            "status_code": result["status_code"],
            "title": result["title"],
            "error": result["error"],
        })

    return results


def run_ingestion_pipeline():

    # 1. Scrape
    scrape_results = scrape_all_documents()

    # 2. Chunk only successful documents
    total_chunks = create_chunks_for_documents()

    # 3. Rebuild FAISS
    index_result = None

    if total_chunks > 0:

        index_result = build_vector_index()

    return {
        "scrape_results": scrape_results,
        "total_chunks": total_chunks,
        "index_result": index_result,
    }