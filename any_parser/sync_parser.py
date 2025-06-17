"""Synchronous parser implementation."""

import json
import time
from typing import Any, Dict, Optional, Tuple

import requests

from any_parser.base_parser import BaseParser

TIMEOUT = 60


class BaseSyncParser(BaseParser):

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
            payload.update(extract_args)

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

    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Converts the given file to markdown."""
        raise NotImplementedError

    def extract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extracts information from the given file."""
        raise NotImplementedError


class ParseSyncParser(BaseSyncParser):
    """Parse parser implementation."""

    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_parse",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=extract_args,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["markdown"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""


class ParseProSyncParser(BaseSyncParser):
    """Parse Pro parser implementation for multi-language support."""

    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_parse_pro",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=extract_args,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["markdown"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""


class ParseTextractSyncParser(BaseSyncParser):
    """Parse Textract parser implementation."""

    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        # Add extract_tables parameter if provided in extract_args
        payload_args = {}
        if extract_args and "extract_tables" in extract_args:
            payload_args["extract_tables"] = extract_args["extract_tables"]
            
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_parse_textract",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=payload_args,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["markdown"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""


class ExtractPIISyncParser(BaseSyncParser):
    """Extract PII parser implementation."""

    def extract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_extract_pii",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=None,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["result"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""


class ExtractTablesSyncParser(BaseSyncParser):
    """Extract tables parser implementation."""

    def extract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_extract_tables",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args={"extract_tables" : True},
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["markdown"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""


class ExtractKeyValueSyncParser(BaseSyncParser):
    """Extract key-value parser implementation."""

    def extract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        # Handle the key-value extraction payload structure
        payload_args = {}
        if extract_args and "extract_instruction" in extract_args:
            payload_args["extract_input_key_description_pairs"] = extract_args["extract_instruction"]
            
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_extract_key_value",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=payload_args,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["result"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""


class ExtractResumeKeyValueSyncParser(BaseSyncParser):
    """Extract resume key-value parser implementation."""

    def extract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        response, info = self.get_sync_response(
            f"{self._base_url}/anyparser/sync_extract_resume_key_value",
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=None,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["extraction_result"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""
