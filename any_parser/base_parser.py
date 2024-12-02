"""Base parser implementation."""


class BaseParser:
    def __init__(self, api_key: str, base_url: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": self._api_key,
        }
