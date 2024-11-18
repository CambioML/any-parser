"""AnyParser RT: Real-time parser for any data format."""

import base64
import json
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests

from any_parser.async_parser import AsyncParser
from any_parser.base_parser import ProcessType
from any_parser.sync_parser import SyncParser
from any_parser.utils import validate_parser_inputs

PUBLIC_SHARED_BASE_URL = "https://public-api.cambio-ai.com"
TIMEOUT = 60


def handle_parsing(func):
    """Decorator to handle common file processing logic."""

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
        is_valid, error_message = validate_parser_inputs(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
        )

        if not is_valid:
            return error_message, ""

        # Encode the file content in base64 if file_path is provided
        if file_content is None:
            assert file_path is not None  # Type narrowing for mypy
            try:
                with open(file_path, "rb") as file:
                    file_content = base64.b64encode(file.read()).decode("utf-8")
                    file_type = Path(file_path).suffix.lower().lstrip(".")
            except Exception as e:
                return f"Error: {e}", ""

        return func(
            self,
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
            *args,
            **kwargs,
        )

    return wrapper


def handle_async_parsing(func):
    """Decorator to handle common async file processing logic."""

    def wrapper(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        *args,
        **kwargs,
    ):
        # Validate inputs
        is_valid, error_message = validate_parser_inputs(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
        )

        if not is_valid:
            return error_message

        # Dump the file content into a NamedTemporaryFile if file_path
        # is not provided
        if file_path:
            file_type = Path(file_path).suffix.lower().lstrip(".")
        else:
            file_path = NamedTemporaryFile(delete=False, suffix=f".{file_type}").name
            print(file_path)
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(file_content))  # type: ignore

        # Call the actual function with processed arguments
        return func(self, file_path=file_path, *args, **kwargs)

    return wrapper


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
        self._sync_parser = SyncParser(api_key, base_url)
        self._async_parser = AsyncParser(api_key, base_url)

    @handle_parsing
    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extract full content from a file in real-time."""
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

    @handle_parsing
    def extract_pii(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
    ):
        """Extract PII from a file in real-time."""
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

    @handle_parsing
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

    @handle_parsing
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

    @handle_parsing
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
    @handle_async_parsing
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
            extract_args=extract_args,
        )

    @handle_async_parsing
    def async_parse_with_layout(
        self, file_path=None, file_content=None, file_type=None
    ):
        """Extract content from a file asynchronously with layout analysis."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE_WITH_LAYOUT,
            file_path=file_path,  # type: ignore
        )

    @handle_async_parsing
    def async_parse_with_ocr(self, file_path=None, file_content=None, file_type=None):
        """Extract full content from a file asynchronously with OCR."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE_WITH_OCR,
            file_path=file_path,  # type: ignore
        )

    @handle_async_parsing
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
            extract_args=extract_args,
        )

    @handle_async_parsing
    def async_extract_tables(self, file_path=None, file_content=None, file_type=None):
        """Extract tables from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_TABLES,
            file_path=file_path,  # type: ignore
        )

    @handle_async_parsing
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
            extract_args={"extract_instruction": extract_instruction},
        )

    @handle_async_parsing
    def async_extract_resume_key_value(
        self, file_path=None, file_content=None, file_type=None
    ):
        """Extract resume key-value pairs from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_RESUME_KEY_VALUE,
            file_path=file_path,  # type: ignore
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
