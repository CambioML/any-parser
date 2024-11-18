"""Asynchronous parser implementation."""

import base64
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Optional

import requests

from any_parser.base_parser import BaseParser, ProcessType
from any_parser.utils import upload_file_to_presigned_url

TIMEOUT = 60


class AsyncParser(BaseParser):
    def _setup_endpoints(self) -> None:
        self._async_upload_url = f"{self._base_url}/async/upload"
        self._async_fetch_url = f"{self._base_url}/async/fetch"

    def _async_process_file(
        self,
        file_path: Optional[str],
        file_content: Optional[str],
        file_type: Optional[str],
    ):
        file_path, file_type, error = self._process_file(
            file_path, file_content, file_type
        )
        if error:
            return None, None, error

        if not file_path:
            temp_file = NamedTemporaryFile(delete=False, suffix=file_type)
            file_path = temp_file.name
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(file_content))  # type: ignore

        return file_path, file_type, None

    def send_async_request(
        self,
        process_type: ProcessType,
        file_path: str,
        extract_args: Optional[Dict] = None,
    ) -> str:
        """Extract full content from a file asynchronously.

        Args:
            url_endpoint (str): The URL endpoint for the API.
            file_path (str): The path to the file to be parsed.
            process_type (ProcessType): The type of processing to be done.
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
        return upload_file_to_presigned_url(file_path, response)
