"""AnyParser RT: Real-time parser for any data format."""

import base64
import json
import time
import uuid
from pathlib import Path

import requests

from any_parser.async_parser import AsyncParser
from any_parser.constants import ProcessType
from any_parser.sync_parser import SyncParser
from any_parser.utils import validate_file_inputs

PUBLIC_SHARED_BASE_URL = "https://public-api.cambio-ai.com"
TIMEOUT = 60


def handle_file_processing(func):
    """
    Decorator to handle common file processing logic for parsing
    and extraction operations.

    This decorator manages file input validation and processing, supporting
    either direct file content or file path inputs. It performs base64 encoding
    of file contents when a file path is provided.

    Args:
        func: The decorated function that performs the actual parsing or
        extraction.

    Parameters for decorated functions:
        file_path (str, optional): Path to the file to be processed. If
            provided, the file will be read and encoded in base64.
        file_content (str, optional): Base64-encoded content of the file. If
            provided, file_path will be ignored.
        file_type (str, optional): The file extension/type (e.g., 'pdf').
            If not provided and file_path is given, it will be inferred from
            the file extension.
        *args, **kwargs: Additional arguments passed to the decorated function.

    Returns:
        tuple: A tuple containing (error_message, result), where:
            - error_message (str): Error message if processing fails, empty
                string on success
            - result (str): Empty string if error occurs, otherwise the
                processed result from func

    Usage:
        @handle_file_processing
        def parse(self, file_path=None, file_content=None, file_type=None):
            # Implementation
            pass

    Note:
        Either file_path or file_content must be provided, but not both.
        If file_path is provided, the file content will be read and encoded in
        base64, and file_type will be inferred from the file extension.
        If file_content is provided, file_type will be validated, and a
        temporary file path will be generated for generating presigned url(for
        async parsing and extraction)
    """

    def wrapper(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        *args,
        **kwargs,
    ):
        # pylint: disable=too-many-arguments
        # Validate inputs
        is_valid, error_message = validate_file_inputs(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
        )

        if not is_valid:
            return error_message, ""

        # Encode the file content in base64 if file_path is provided
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    file_content = base64.b64encode(file.read()).decode("utf-8")
                    file_type = Path(file_path).suffix.lower().lstrip(".")
            except Exception as e:
                return f"Error: {e}", ""
        else:
            # generate a random file path for genrating presigned url
            file_path = f"/tmp/{uuid.uuid4()}.{file_type}"

        return func(
            self,
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
            *args,
            **kwargs,
        )

    return wrapper


class AnyParser:
    """Real-time parser for processing various data formats.

    Provides both synchronous and asynchronous methods for parsing and
    extracting information from different types of files.
    """

    def __init__(self, api_key: str, base_url: str = PUBLIC_SHARED_BASE_URL) -> None:
        """Initialize AnyParser with API credentials.

        Args:
            api_key: Authentication key for API access
            base_url: API endpoint URL, defaults to public endpoint
        """
        self._sync_parser = SyncParser(api_key, base_url)
        self._async_parser = AsyncParser(api_key, base_url)

    @handle_file_processing
    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extract full content from a file synchronously.

        Args:
            file_path: Path to input file
            file_content: Base64 encoded file content
            file_type: File format extension
            extract_args: Additional extraction parameters

        Returns:
            tuple: (result, timing_info) or (error_message, "")
        """
        response, info = self._sync_parser.get_sync_response(
            self._sync_parser._sync_parse_url,
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=extract_args,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = "\n".join(
                response_data["markdown"]
            )  # Using direct extraction instead of extract_key
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    @handle_file_processing
    def extract_pii(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
    ):
        """
        Extract PII data from a file synchronously.
        """
        response, info = self._sync_parser.get_sync_response(
            self._sync_parser._sync_extract_pii,
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=None,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["pii_extraction"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    @handle_file_processing
    def extract_tables(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
    ):
        """Extract tables from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        response, info = self._sync_parser.get_sync_response(
            self._sync_parser._sync_extract_tables,
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=None,
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = "\n".join(response_data["markdown"])
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    @handle_file_processing
    def extract_key_value(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_instruction=None,
    ):
        """Extract key-value pairs from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
            extract_instruction (Dict): A dictionary containing the keys to be
                extracted, with their values as the description of those keys.
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        response, info = self._sync_parser.get_sync_response(
            self._sync_parser._sync_extract_key_value,
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args={"extract_instruction": extract_instruction},
        )

        if response is None:
            return info, ""

        try:
            response_data = response.json()
            result = response_data["json"]
            return result, f"Time Elapsed: {info}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response: {response.text}", ""

    @handle_file_processing
    def extract_resume_key_value(
        self, file_path=None, file_content=None, file_type=None
    ):
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
                    - "pii": Personally Identifiable Information - includes
                        only name, email, and phone
        """
        response, info = self._sync_parser.get_sync_response(
            self._sync_parser._sync_extract_resume_key_value,
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

    # Example of decorated methods:
    @handle_file_processing
    def async_parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extract full content from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            extract_args=extract_args,
        )

    @handle_file_processing
    def async_parse_with_layout(
        self, file_path=None, file_content=None, file_type=None
    ):
        """Extract content from a file asynchronously with layout analysis."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE_WITH_LAYOUT,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
        )

    @handle_file_processing
    def async_parse_with_ocr(self, file_path=None, file_content=None, file_type=None):
        """Extract full content from a file asynchronously with OCR."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE_WITH_OCR,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
        )

    @handle_file_processing
    def async_extract_pii(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extract PII from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_PII,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            extract_args=extract_args,
        )

    @handle_file_processing
    def async_extract_tables(self, file_path=None, file_content=None, file_type=None):
        """Extract tables from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_TABLES,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
        )

    @handle_file_processing
    def async_extract_key_value(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_instruction=None,
    ):
        """Extract key-value pairs from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_KEY_VALUE,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            extract_args={"extract_instruction": extract_instruction},
        )

    @handle_file_processing
    def async_extract_resume_key_value(
        self, file_path=None, file_content=None, file_type=None
    ):
        """Extract resume key-value pairs from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_RESUME_KEY_VALUE,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
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
            sync (bool, optional): Whether to wait for the results
                synchronously.
            sync_timeout (int, optional): Maximum time to wait for results in
                seconds. Defaults to 60.
            sync_interval (int, optional): Time interval between polling
                attempts in seconds. Defaults to 5.

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
                    self._async_parser._async_fetch_url,
                    headers=self._async_parser._headers,
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
                self._async_parser._async_fetch_url,
                headers=self._async_parser._headers,
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
            return ""
        return f"Error: {response.status_code} {response.text}"
