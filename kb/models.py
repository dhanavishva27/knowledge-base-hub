from django.db import models


class URLDocument(models.Model):
    url = models.URLField(max_length=2048, unique=True)
    status_code = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=500, blank=True)
    raw_html = models.TextField(blank=True)
    clean_text = models.TextField(blank=True)

    scraped_at = models.DateTimeField(null=True, blank=True)

    content_hash = models.CharField(
        max_length=64,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
class DocumentChunk(models.Model):
    document = models.ForeignKey(
        URLDocument,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    chunk_index = models.IntegerField()

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.document.url} - Chunk {self.chunk_index}"