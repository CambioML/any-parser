"""Asynchronous parser implementation."""

import json
import time
from typing import Dict, Optional

import requests

from any_parser.base_parser import BaseParser
from any_parser.constants import ProcessType

TIMEOUT = 180


class AsyncParser(BaseParser):
    def __init__(self, api_key: str, base_url: str) -> None:
        super().__init__(api_key, base_url)

    def send_async_request(
        self,
        process_type: ProcessType,
        file_path: str,
        file_content: str,
        file_type: str = None,
        extract_args: Optional[Dict] = None,
    ) -> str:
        """Submit an async processing job and return the job ID.

        Args:
            process_type (ProcessType): The type of processing to be done.
            file_path (str): The path to the file to be parsed (used for job identification).
            file_content (str): The content of the file to be parsed.
            file_type (str): The type of the file to be parsed.
            extract_args (Optional[Dict]): Additional extraction arguments.

        Returns:
            str: The job_id of the submitted job.
        """

        # Determine the endpoint based on process type
        endpoint_map = {
            ProcessType.PARSE: "/anyparser/async_parse",
            ProcessType.PARSE_PRO: "/anyparser/async_parse_pro",
            ProcessType.PARSE_TEXTRACT: "/anyparser/async_parse_textract",
            ProcessType.EXTRACT_PII: "/anyparser/async_extract_pii",
            ProcessType.EXTRACT_TABLES: "/anyparser/async_extract_tables",
            ProcessType.EXTRACT_KEY_VALUE: "/anyparser/async_extract_key_value",
        }

        endpoint = endpoint_map.get(process_type)
        if not endpoint:
            raise ValueError(f"Unsupported process type: {process_type}")

        # Get file type from file path
        file_type = file_path.split(".")[-1] if "." in file_path else ""

        # Create the payload
        payload = {
            "file_content": file_content,
            "file_type": file_type,
        }

        if extract_args:
            if process_type == ProcessType.EXTRACT_KEY_VALUE:
                input_keys = list(extract_args["extract_instruction"].keys())
                input_descriptions = list(extract_args["extract_instruction"].values())
                extract_instruction = [
                    {"key": key, "description": description}
                    for key, description in zip(input_keys, input_descriptions)
                ]
                payload["extract_input_key_description_pairs"] = extract_instruction
            elif process_type == ProcessType.EXTRACT_TABLES:
                payload["extract_tables"] = True
            else:
                payload.update(extract_args)

        # Send the POST request
        response = requests.post(
            f"{self._base_url}{endpoint}",
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        response_data = response.json()
        return response_data["job_id"]

    def get_job_status(self, job_id: str) -> Dict:
        """Get the status of an async job.

        Args:
            job_id (str): The ID of the job to check.

        Returns:
            Dict: Job status information including status, result, and error if any.
        """
        response = requests.get(
            f"{self._base_url}/anyparser/job_status/{job_id}",
            headers=self._headers,
            timeout=TIMEOUT,
        )

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        return response.json()

    def handle_async_response(self, response) -> str:
        """Handle async response for backwards compatibility."""
        if response is None:
            return "Error: timeout, no response received"
        if response.status_code == 202:
            return ""
        if response.status_code == 200:
            try:
                response_data = response.json()

                # Handle different response formats
                if "markdown" in response_data:
                    return response_data["markdown"]
                elif "result" in response_data:
                    return response_data["result"]
                elif "error" in response_data:
                    return f"Error: {response_data['error']}"
                else:
                    return str(response_data)

            except json.JSONDecodeError:
                return f"Error: Invalid JSON response: {response.text}"

        return f"Error: {response.status_code} {response.text}"
