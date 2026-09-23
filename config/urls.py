from django.contrib import admin
from django.urls import path

from kb.views import (
    home,
    upload_csv,
    search_api,
    urls_api,
)


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "upload/",
        upload_csv,
        name="upload_csv"
    ),

    path(
        "api/search/",
        search_api,
        name="search_api"
    ),

    path(
        "api/urls/",
        urls_api,
        name="urls_api"
    ),

    path(
    "",
    home,
    name="home"
    ),
]