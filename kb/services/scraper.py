import requests

from bs4 import BeautifulSoup


def scrape_url(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/153.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            allow_redirects=True
        )

        status_code = response.status_code
        raw_html = response.text

        # ------------------------------------------------
        # HTTP ERROR
        # ------------------------------------------------

        if not 200 <= status_code < 300:

            return {
                "success": False,
                "status_code": status_code,
                "title": "",
                "raw_html": raw_html,
                "clean_text": "",
                "error": (
                    f"HTTP {status_code}"
                ),
            }

        # ------------------------------------------------
        # PARSE SUCCESSFUL PAGE
        # ------------------------------------------------

        soup = BeautifulSoup(
            raw_html,
            "html.parser"
        )

        title = ""

        if soup.title:

            title = soup.title.get_text(
                strip=True
            )

        # Remove unnecessary elements
        for element in soup(
            ["script", "style", "noscript"]
        ):

            element.decompose()

        clean_text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Make sure there is actually content
        if not clean_text:

            return {
                "success": False,
                "status_code": status_code,
                "title": title,
                "raw_html": raw_html,
                "clean_text": "",
                "error": "No readable text found",
            }

        return {
            "success": True,
            "status_code": status_code,
            "title": title,
            "raw_html": raw_html,
            "clean_text": clean_text,
            "error": None,
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "status_code": None,
            "title": "",
            "raw_html": "",
            "clean_text": "",
            "error": str(error),
        }