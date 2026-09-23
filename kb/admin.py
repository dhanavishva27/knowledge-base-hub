from django.contrib import admin
from .models import URLDocument


@admin.register(URLDocument)
class URLDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'url',
        'status_code',
        'title',
        'scraped_at',
        'created_at',
    )

    search_fields = (
        'url',
        'title',
        'clean_text',
    )

    list_filter = (
        'status_code',
    )