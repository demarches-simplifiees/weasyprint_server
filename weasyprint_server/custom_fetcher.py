from urllib.error import URLError
from weasyprint.urls import default_url_fetcher
from .logger import LOGGER


def custom_url_fetcher(url, timeout=10, ssl_context=None):
    try:
        result = default_url_fetcher(url, timeout, ssl_context)
    except URLError as e:
        LOGGER.warning("asset missing", exc_info=e, extra={"context": {"url": url}})
        # Ugly hack:
        # the caller swallows all `Exception`
        # but raise an AttributeError if the result is None
        result = None
    return result
