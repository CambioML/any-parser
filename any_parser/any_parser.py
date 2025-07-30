"""AnyParser: Real-time parser for any data format."""

import base64
import time
import uuid
from collections.abc import Iterable
from io import StringIO
from pathlib import Path
from .terminal_ui import TerminalParserUI


from any_parser.async_parser import AsyncParser
from any_parser.batch_parser import BatchParser
from any_parser.constants import (
    PUBLIC_BATCH_BASE_URL,
    PUBLIC_SHARED_BASE_URL,
    ProcessType,
)
from any_parser.sync_parser import (
    ExtractKeyValueSyncParser,
    ExtractPIISyncParser,
    ExtractTablesSyncParser,
    ParseProSyncParser,
    ParseSyncParser,
    ParseTextractSyncParser,
)
from any_parser.utils import validate_file_inputs


def handle_file_processing(func):
    """
    Decorator to handle file input validation and processing.

    Supports both file path and base64 file content inputs. When a file path
    is provided, reads and base64-encodes the file content automatically.

    Args:
        func: The decorated function that performs parsing or extraction.

    Decorated function parameters:
        file_path (str, optional): Path to the file to process.
        file_content (str, optional): Base64-encoded file content.
        file_type (str, optional): File extension (e.g., 'pdf'). Auto-detected from file_path.

    Returns:
        tuple: (result, timing_info) on success, (error_message, "") on failure.

    Note:
        Either file_path or file_content must be provided, but not both.
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

    def __init__(
        self,
        api_key: str,
        base_url: str = PUBLIC_SHARED_BASE_URL,
        batch_url: str = PUBLIC_BATCH_BASE_URL,
    ) -> None:
        """Initialize AnyParser with API credentials.

        Args:
            api_key: Authentication key for API access
            base_url: API endpoint URL, defaults to public endpoint
            batch_url: Batch API endpoint URL, defaults to public batch endpoint
        """
        self._async_parser = AsyncParser(api_key, base_url)
        self._sync_parse = ParseSyncParser(api_key, base_url)
        self._sync_parse_pro = ParseProSyncParser(api_key, base_url)
        self._sync_parse_textract = ParseTextractSyncParser(api_key, base_url)
        self._sync_extract_key_value = ExtractKeyValueSyncParser(api_key, base_url)
        self._sync_extract_pii = ExtractPIISyncParser(api_key, base_url)
        self._sync_extract_tables = ExtractTablesSyncParser(api_key, base_url)
        self.batches = BatchParser(api_key, batch_url)

    @handle_file_processing
    def parse(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
        show_ui=False  # New optional parameter
    ):
        """Extract full content from a file synchronously with optional terminal UI.

        Args:
            file_path: Path to input file
            file_content: Base64 encoded file content
            file_type: File format extension
            extract_args: Additional extraction parameters
            show_ui: Whether to display formatted output in terminal (default: False)

        Returns:
            tuple: (result, timing_info) or (error_message, "")
        """
        result, timing = self._sync_parse.parse(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
            extract_args=extract_args
        )
        
        if show_ui:
            TerminalParserUI().display(result)
        
        return result, timing
    
    @handle_file_processing
    def parse_pro(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extract full content from a file synchronously using pro model with multi-language support.

        Args:
            file_path: Path to input file
            file_content: Base64 encoded file content
            file_type: File format extension
            extract_args: Additional extraction parameters

        Returns:
            tuple: (result, timing_info) or (error_message, "")
        """
        return self._sync_parse_pro.parse(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
            extract_args=extract_args,
        )

    @handle_file_processing
    def parse_textract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_tables=False,
    ):
        """Extract content from a file synchronously using AWS Textract.

        Args:
            file_path: Path to input file
            file_content: Base64 encoded file content
            file_type: File format extension
            extract_tables: Whether to extract tables

        Returns:
            tuple: (result, timing_info) or (error_message, "")
        """
        extract_args = {"extract_tables": extract_tables} if extract_tables else None
        return self._sync_parse_textract.parse(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
            extract_args=extract_args,
        )

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
        return self._sync_extract_pii.extract(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
        )

    @staticmethod
    def flatten_to_string(item):
        """
        Flatten any iterable object to a string.
        """

        if isinstance(item, str):
            return item

        # if item is a dict, flatten all keys and values
        if isinstance(item, dict):
            parts = []
            for k, v in item.items():
                parts.append(AnyParser.flatten_to_string(k))
                parts.append(AnyParser.flatten_to_string(v))
            return "".join(parts)

        # item is other iterable objects
        if isinstance(item, Iterable):
            parts = []
            for sub_item in item:
                parts.append(AnyParser.flatten_to_string(sub_item))
            return "".join(parts)

        # item is not iterable objects
        return str(item)

    @handle_file_processing
    def extract_tables(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        return_type="html",
    ):
        """Extract tables from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
            return_type (str): 'html' or 'csv'
        Returns:
            tuple(str, str)
        """
        extracted_result, time_elapsed = self._sync_extract_tables.extract(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
        )

        # Handle the new result format where tables are in a dict with 'markdown' key
        if isinstance(extracted_result, dict) and "markdown" in extracted_result:
            extracted_html = extracted_result["markdown"]
        else:
            extracted_html = extracted_result

        # Convert list of HTML strings to a single HTML string
        if isinstance(extracted_html, list):
            extracted_html = AnyParser.flatten_to_string(extracted_html)

        if return_type.lower() == "csv":
            try:
                import pandas as pd
            except ImportError:
                raise ImportError("Please install pandas to use CSV return_type")

            # Ensure we have a string for pandas
            if isinstance(extracted_html, list):
                extracted_html = "".join(str(item) for item in extracted_html)

            # Wrap the HTML tables in a proper HTML structure for pandas
            html_content = f"<html><body>{extracted_html}</body></html>"

            try:
                df_list = pd.read_html(StringIO(html_content))
                combined_df = pd.concat(df_list, ignore_index=True)
                csv_output = combined_df.to_csv(index=False)
                return csv_output, time_elapsed
            except ValueError as e:
                if "No tables found" in str(e):
                    # Return the raw HTML if pandas can't parse it
                    return extracted_html, time_elapsed
                else:
                    raise e

        return extracted_html, time_elapsed

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
            file_content (str): Base64 encoded file content.
            file_type (str): File format extension.
            extract_instruction (Dict or List): A dictionary containing the keys to be
                extracted, with their values as the description of those keys.
                Or a list of dictionaries with 'key' and 'description' fields.
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        # Convert extract_instruction to the correct API format\
        if not file_type:
            file_type = file_path.split(".")[-1] if "." in file_path else ""
        formatted_instruction = None
        if extract_instruction:
            if isinstance(extract_instruction, dict):
                # Convert dict format to list of key-description pairs
                formatted_instruction = [
                    {"key": key, "description": description}
                    for key, description in extract_instruction.items()
                ]
            elif isinstance(extract_instruction, list):
                # Already in correct format
                formatted_instruction = extract_instruction
            else:
                raise ValueError("extract_instruction must be a dict or list")

        return self._sync_extract_key_value.extract(
            file_path=file_path,
            file_content=file_content,
            file_type=file_type,
            extract_args={"extract_instruction": formatted_instruction},
        )

    # Async methods
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
    def async_parse_pro(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_args=None,
    ):
        """Extract full content from a file asynchronously using pro model."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE_PRO,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=extract_args,
        )

    @handle_file_processing
    def async_parse_textract(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_tables=False,
    ):
        """Extract content from a file asynchronously using AWS Textract."""
        extract_args = {"extract_tables": extract_tables} if extract_tables else None
        return self._async_parser.send_async_request(
            process_type=ProcessType.PARSE_TEXTRACT,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args=extract_args,
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
            file_type=file_type,  # type: ignore
            extract_args=None,
        )

    @handle_file_processing
    def async_extract_tables(self, file_path=None, file_content=None, file_type=None):
        """Extract tables from a file asynchronously."""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_TABLES,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
        )

    @handle_file_processing
    def async_extract_key_value(
        self,
        file_path=None,
        file_content=None,
        file_type=None,
        extract_instruction=None,
    ):
        """Extract key-value pairs from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
            file_content (str): Base64 encoded file content.
            file_type (str): File format extension.
            extract_instruction (Dict or List): A dictionary containing the keys to be
                extracted, with their values as the description of those keys.
                Or a list of dictionaries with 'key' and 'description' fields.

        Returns:
            tuple: (job_id, timing_info) or (error_message, "")
        """
        if not file_type:
            file_type = file_path.split(".")[-1] if "." in file_path else ""
        return self._async_parser.send_async_request(
            process_type=ProcessType.EXTRACT_KEY_VALUE,
            file_path=file_path,  # type: ignore
            file_content=file_content,  # type: ignore
            file_type=file_type,  # type: ignore
            extract_args={"extract_instruction": extract_instruction},
        )

    def get_job_status(self, job_id: str):
        """Get the status of an async job.

        Args:
            job_id (str): The ID of the job to check.

        Returns:
            Dict: Job status information including status, result, and error if any.
        """
        return self._async_parser.get_job_status(job_id)

    def async_fetch(
        self,
        file_id: str,
        sync_timeout: int = 180,
        sync_interval: int = 3,
    ) -> str:
        """Fetches extraction results asynchronously.

        Note: This method is kept for backwards compatibility. For new implementations,
        use get_job_status() with the job_id returned from async methods.

        Args:
            file_id (str): The ID of the job to fetch results for.
            sync_timeout (int, optional): Maximum time to wait for results in
                seconds. Defaults to 180.
            sync_interval (int, optional): Time interval between polling
                attempts in seconds. Defaults to 3.

        Returns:
            str: The extracted results as a markdown string, or error message if failed.
        """
        start_time = time.time()
        while time.time() < start_time + sync_timeout:
            try:
                job_status = self.get_job_status(file_id)

                if job_status.get("status") == "completed":
                    # Handle presigned URL if present
                    presigned_url = job_status.get("result_url")
                    if presigned_url:
                        try:
                            import requests

                            presigned_resp = requests.get(presigned_url)
                            presigned_resp.raise_for_status()
                            result_json = presigned_resp.json()
                            if "markdown" in result_json:
                                return result_json["markdown"]
                            elif "result" in result_json:
                                return str(result_json["result"])
                            else:
                                return str(result_json)
                        except Exception:
                            # Fall back to inline result if presigned URL fails
                            pass

                    # Handle inline result
                    result = job_status.get("result", {})
                    if "markdown" in result:
                        return result["markdown"]
                    elif "result" in result:
                        return str(result["result"])
                    else:
                        return str(result)
                elif job_status.get("status") == "failed":
                    error_msg = job_status.get("error_message") or job_status.get(
                        "error", "Job failed"
                    )
                    return f"Error: {error_msg}"
                elif job_status.get("status") in ["pending", "processing"]:
                    print("Waiting for response...")
                    time.sleep(sync_interval)
                    continue
                else:
                    return f"Unknown status: {job_status.get('status')}"

            except Exception as e:
                return f"Error fetching results: {e}"

        return f"Timeout: Job did not complete within {sync_timeout} seconds"
