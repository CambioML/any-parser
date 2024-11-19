"""Synchronous parser implementation."""

import json
import time
from typing import Any, Dict, Optional, Tuple

import requests

from any_parser.base_parser import BaseParser

TIMEOUT = 60


class SyncParser(BaseParser):
    def _setup_endpoints(self) -> None:
        self._sync_parse_url = f"{self._base_url}/parse"
        self._sync_extract_pii = f"{self._base_url}/extract_pii"
        self._sync_extract_tables = f"{self._base_url}/extract_tables"
        self._sync_extract_key_value = f"{self._base_url}/extract_key_value"
        self._sync_extract_resume_key_value = (
            f"{self._base_url}/extract_resume_key_value"
        )
        self._sync_parse_with_ocr = f"{self._base_url}/parse_with_ocr"

    def get_sync_response(
        self,
        url_endpoint: str,
        file_content: str,
        file_type: str,
        extract_args: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[requests.Response], str]:
        payload = {
            "file_content": file_content,
            "file_type": file_type,
        }
        if extract_args:
            payload["extract_args"] = extract_args  # type: ignore

        start_time = time.time()
        response = requests.post(
            url_endpoint,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )
        end_time = time.time()

        if response.status_code != 200:
            return None, f"Error: {response.status_code} {response.text}"

        return response, f"{end_time - start_time:.2f} seconds"
