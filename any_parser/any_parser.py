"""AnyParser RT: Real-time parser for any data format."""

import base64
import json
import time
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple

import requests

from any_parser.utils import check_file_type_and_path, upload_file_to_presigned_url

PUBLIC_SHARED_BASE_URL = "https://3urw2x5zhi.execute-api.us-west-2.amazonaws.com/v1/"
TIMEOUT = 60


class ProcessType(Enum):
    EXTRACT_PII = "extract_pii"
    EXTRACT_TABLES = "extract_tables"
    EXTRACT_KEY_VALUE = "extract_key_value"
    EXTRACT_RESUME_KEY_VALUE = "extract_resume_key_value"
    PARSE = "file"
    PARSE_WITH_OCR = "parse_with_ocr"
    PARSE_WITH_LAYOUT = "parse_with_layout"


class AnyParser:
    """AnyParser RT: Real-time parser for any data format."""

    def __init__(self, api_key: str, base_url: str = PUBLIC_SHARED_BASE_URL) -> None:
        """Initialize the AnyParser RT object.

        Args:
            api_key (str): The API key for the AnyParser
            url (str): The URL of the AnyParser RT API.

        Returns:
            None
        """
        self._sync_parse_url = f"{base_url}/parse"
        self._sync_extract_pii = f"{base_url}/extract_pii"
        self._sync_extract_tables = f"{base_url}/extract_tables"
        self._sync_extract_key_value = f"{base_url}/extract_key_value"
        self._sync_extract_resume_key_value = f"{base_url}/extract_resume_key_value"
        self._sync_parse_with_ocr = f"{base_url}/parse_with_ocr"
        self._async_upload_url = f"{base_url}/async/upload"
        self._async_fetch_url = f"{base_url}/async/fetch"
        self._api_key = api_key
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": self._api_key,
        }

    def _get_sync_response(
        self, url_endpoint: str, file_path: str, extract_args: Optional[Dict] = None
    ) -> Tuple[requests.Response | None, str]:
        """Extract full content from a file in real-time.

        Args:
            url_endpoint (str): The URL endpoint for the API.
            file_path (str): The path to the file to be parsed.
            extract_args (Optional[Dict]): Additional extraction arguments.

        Returns:
            tuple(requests.Response | None, str): The response object and the
            time taken. If the file is invalid or the API request fails,
            returns None and an error message.
        """

        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)
        if error:
            return None, error

        # Encode the file content in base64
        with open(file_path, "rb") as file:
            encoded_file = base64.b64encode(file.read()).decode("utf-8")

        # Create the JSON payload
        payload = {
            "file_content": encoded_file,
            "file_type": file_extension,
        }

        if extract_args is not None and isinstance(extract_args, dict):
            payload["extract_args"] = extract_args

        # Send the POST request
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

    def _send_async_request(
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
        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)
        if error:
            return error

        file_name = Path(file_path).name

        # Create the JSON payload
        payload = {
            "file_name": file_name,
            "process_type": process_type.value,
        }

        if extract_args is not None and isinstance(extract_args, dict):
            payload["extract_args"] = extract_args

        # Send the POST request
        response = requests.post(
            self._async_upload_url,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )

        # If response successful, upload the file
        return upload_file_to_presigned_url(file_path, response)

    def parse(
        self,
        file_path: str,
        extract_args: Optional[Dict] = None,
    ) -> Tuple[str, str]:
        """Extract full content from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
            extract_args (Optional[Dict]): Additional extraction arguments added
                to the prompt.

        Returns:
            tuple(str, str): The extracted data and the time taken.
        """

        response, info = self._get_sync_response(
            self._sync_parse_url,
            file_path,
            extract_args=extract_args,
        )
        if response is None:
            return info, ""

        try:
            response_data = response.json()
            response_list = []
            for text in response_data["markdown"]:
                response_list.append(text)
            markdown_text = "\n".join(response_list)
            return (
                markdown_text,
                f"Time Elapsed: {info}",
            )
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    def extract_pii(
        self,
        file_path: str,
    ) -> Tuple[str, str]:
        """Extract personally identifiable information (PII) from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        response, info = self._get_sync_response(
            self._sync_extract_pii,
            file_path,
            extract_args=None,
        )
        if response is None:
            return info, ""

        try:
            response_data = response.json()
            return (
                response_data["pii_extraction"],
                f"Time Elapsed: {info}",
            )
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""
        
    def extract_tables(
        self,
        file_path: str,
    ) -> Tuple[str, str]:
        """Extract tables from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        response, info = self._get_sync_response(
            self._sync_extract_tables,
            file_path,
            extract_args=None,
        )
        if response is None:
            return info, ""

        try:
            response_data = response.json()
            response_list = []
            for text in response_data["markdown"]:
                response_list.append(text)
            markdown_text = "\n".join(response_list)
            return (
                markdown_text,
                f"Time Elapsed: {info}",
            )
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    def extract_key_value(
        self,
        file_path: str,
        extract_instruction: Dict,
    ) -> Tuple[str, str]:
        """Extract key-value pairs from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
            extract_instruction (Dict): A dictionary containing the keys to be
                extracted, with their values as the description of those keys.
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        response, info = self._get_sync_response(
            self._sync_extract_key_value,
            file_path,
            extract_args={"extract_instruction": extract_instruction},
        )
        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["json"]
            return (
                result,
                f"Time Elapsed: {info}",
            )
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    def extract_resume_key_value(
        self,
        file_path: str,
    ) -> Tuple[str, str]:
        """Extract resume in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            tuple(str, str): The extracted data and the time taken.
                extracted data includes:
                    - "education": Education
                    - "work_experience": Work Experience
                    - "personal_info": Personal Information
                    - "skills": Skills
                    - "certifications": Certifications
                    - "projects": Projects
                    - "pii": Personally Identifiable Information - includes only name, email, and phone
        """
        response, info = self._get_sync_response(
            self._sync_extract_resume_key_value,
            file_path,
            extract_args=None,
        )
        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["extraction_result"]
            return (
                result,
                f"Time Elapsed: {info}",
            )
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    def async_parse(
        self,
        file_path: str,
        extract_args: Optional[Dict] = None,
    ) -> str:
        """Extract full content from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
            extract_args (Optional[Dict]): Additional extraction arguments added to prompt
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.PARSE,
            file_path,
            extract_args=extract_args,
        )

    def async_parse_with_layout(self, file_path: str) -> str:
        """Extract full content from a file asynchronously.

        Compared with `async_extract`, this method will first analyze the layout of the file.
        Then it will process text, tables, and images separately;
        and return the combined result in markdown format.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.PARSE_WITH_LAYOUT,
            file_path,
            extract_args=None,
        )

    def async_parse_with_ocr(self, file_path: str) -> str:
        """Extract full content from a file asynchronously.

        Compared with `async_extract`, this method will first perform OCR on the file.
        Then it will process text, tables, and images separately;
        and return the combined result in markdown format.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.PARSE_WITH_OCR,
            file_path,
            extract_args=None,
        )

    def async_extract_pii(self, file_path: str) -> str:
        """Extract personally identifiable information (PII) from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.EXTRACT_PII,
            file_path,
            extract_args=None,
        )
    
    def async_extract_tables(self, file_path: str) -> str:
        """Extract tables from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.EXTRACT_TABLES,
            file_path,
            extract_args=None,
        )

    def async_extract_key_value(
        self,
        file_path: str,
        extract_instruction: Dict,
    ) -> str:
        """Extract key-value pairs from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
            extract_instruction (Dict): A dictionary containing the keys to be
                extracted, with their values as the description of those keys.
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.EXTRACT_KEY_VALUE,
            file_path,
            extract_args={"extract_instruction": extract_instruction},
        )

    def async_extract_resume_key_value(
        self,
        file_path: str,
    ) -> str:
        """Extract key-value pairs from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            str: The file id of the uploaded file.
        """
        return self._send_async_request(
            ProcessType.EXTRACT_RESUME_KEY_VALUE,
            file_path,
            extract_args=None,
        )

    def async_fetch(
        self,
        file_id: str,
        sync: bool = True,
        sync_timeout: int = 60,
        sync_interval: int = 5,
    ) -> str:
        """Fetches extraction results asynchronously.

        Args:
            file_id (str): The ID of the file to fetch results for.
            sync (bool, optional): Whether to wait for the results synchronously.
            sync_timeout (int, optional): Maximum time to wait for results in seconds. Defaults to 60.
            sync_interval (int, optional): Time interval between polling attempts in seconds. Defaults to 5.

        Returns:
            str: The extracted results as a markdown string.
            None: If the extraction is still in progress (when sync is False).
        """

        response = None
        # Create the JSON payload
        payload = {"file_id": file_id}
        if sync:
            start_time = time.time()
            while time.time() < start_time + sync_timeout:
                response = requests.post(
                    self._async_fetch_url,
                    headers=self._headers,
                    data=json.dumps(payload),
                    timeout=TIMEOUT,
                )
                if response.status_code == 202:
                    print("Waiting for response...")
                    time.sleep(sync_interval)
                    continue
                break
        else:
            response = requests.post(
                self._async_fetch_url,
                headers=self._headers,
                data=json.dumps(payload),
                timeout=TIMEOUT,
            )

        if response is None:
            return "Error: timeout, no response received"
        if response.status_code == 200:
            result = response.json()
            if "json" in result:
                return result["json"]
            elif "resume_extraction" in result:
                return result["resume_extraction"]
            elif "pii_extraction" in result:
                return result["pii_extraction"]
            elif "markdown" in result:
                markdown_list = result["markdown"]
                return "\n".join(markdown_list)
            return f"Error: Invalid response format\n {result}"
        if response.status_code == 202:
            return None
        return f"Error: {response.status_code} {response.text}"
