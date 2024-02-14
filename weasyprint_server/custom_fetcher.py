from urllib.error import URLError
from weasyprint.urls import default_url_fetcher


def custom_url_fetcher(url, timeout=10, ssl_context=None):
    try:
        result = default_url_fetcher(url, timeout, ssl_context)
    except URLError:
        # Ugly hack:
        # the caller swallows all `Exception`
        # but raise an AttributeError if the result is None
        result = None
    return result
