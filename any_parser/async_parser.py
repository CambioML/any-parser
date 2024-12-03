"""Asynchronous parser implementation."""

import json
from pathlib import Path
from typing import Dict, Optional

import requests

from any_parser.base_parser import BaseParser
from any_parser.constants import ProcessType
from any_parser.utils import upload_file_to_presigned_url

TIMEOUT = 60


class BasePostProcessor:
    def __init__(self, successor=None) -> None:
        self.successor = successor

    def process(self, json_response: Dict) -> str:
        if self.successor:
            return self.successor.process(json_response)
        return f"Error: Invalid JSON response: {json_response}"


class ParsePostProcessor(BasePostProcessor):
    def process(self, json_response: Dict) -> str:
        if "markdown" in json_response:
            return json_response["markdown"]
        return super().process(json_response)


class KeyValuePostProcessor(BasePostProcessor):
    def process(self, json_response: Dict) -> str:
        if "json" in json_response:
            return json_response["json"]
        return super().process(json_response)


class ExtractPIIPostProcessor(BasePostProcessor):
    def process(self, json_response: Dict) -> str:
        if "pii_extraction" in json_response:
            return json_response["pii_extraction"]
        return super().process(json_response)


class ExtractResumeKeyValuePostProcessor(BasePostProcessor):

    def process(self, json_response: Dict) -> str:
        if "resume_extraction" in json_response:
            return json_response["resume_extraction"]
        return super().process(json_response)


class AsyncParser(BaseParser):
    def __init__(self, api_key: str, base_url: str) -> None:
        super().__init__(api_key, base_url)
        self._async_upload_url = f"{self._base_url}/async/upload"
        self._async_fetch_url = f"{self._base_url}/async/fetch"

    def send_async_request(
        self,
        process_type: ProcessType,
        file_path: str,
        file_content: str,
        extract_args: Optional[Dict] = None,
    ) -> str:
        """Extract full content from a file asynchronously.

        Args:
            process_type (ProcessType): The type of processing to be done.
            file_path (str): The path to the file to be parsed.
            file_content (str): The content of the file to be parsed.
            extract_args (Optional[Dict]): Additional extraction arguments.

        Returns:
            str: The file id of the uploaded file.
        """

        file_name = Path(file_path).name

        # Create the JSON payload
        payload = {
            "file_name": file_name,
            "process_type": process_type.value,
        }

        if extract_args is not None and isinstance(extract_args, dict):
            payload["extract_args"] = extract_args  # type: ignore

        # Send the POST request
        response = requests.post(
            self._async_upload_url,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )

        # If response successful, upload the file
        return upload_file_to_presigned_url(file_content, response)

    def handle_async_response(self, response) -> str:
        if response is None:
            return "Error: timeout, no response received"
        if response.status_code == 202:
            return ""
        if response.status_code == 200:
            extract_resume_processor = ExtractResumeKeyValuePostProcessor()
            key_value_processor = KeyValuePostProcessor(extract_resume_processor)
            extract_pii_processor = ExtractPIIPostProcessor(key_value_processor)
            handler = ParsePostProcessor(extract_pii_processor)
            try:
                return handler.process(response.json())
            except json.JSONDecodeError:
                return f"Error: Invalid JSON response: {response.text}"

        return f"Error: {response.status_code} {response.text}"
