from .request_handler import RequestHandler


class BaseClient:
    """
    Shared HTTP + auth + retry layer.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._handler = RequestHandler()

    def _get(self, url: str, retries: int = 3, delay: int = 10):
        response = self._handler.get_response(url, retries=retries, delay=delay)

        if response.status_code != 200:
            raise RuntimeError(f"Request failed: {url} ({response.status_code})")

        return response.json()

    def _auth_get(self, url: str, api_key: str, retries: int = 3, delay: int = 10):
        response = self._handler.get_response_auth(
            url, api_key, retries=retries, delay=delay
        )

        if response.status_code != 200:
            raise RuntimeError(f"Request failed: {url} ({response.status_code})")

        return response.json()


class AuthMixin:
    """
    Append auth to end of url
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _auth_url(self, url: str) -> str:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}api_key={self.api_key}"
