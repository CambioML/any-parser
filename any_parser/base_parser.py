"""Base parser implementation."""

import base64
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

from any_parser.utils import validate_parser_inputs


class ProcessType(Enum):
    EXTRACT_PII = "extract_pii"
    EXTRACT_TABLES = "extract_tables"
    EXTRACT_KEY_VALUE = "extract_key_value"
    EXTRACT_RESUME_KEY_VALUE = "extract_resume_key_value"
    PARSE = "parse"
    PARSE_WITH_OCR = "parse_with_ocr"
    PARSE_WITH_LAYOUT = "parse_with_layout"


class BaseParser:
    def __init__(self, api_key: str, base_url: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": self._api_key,
        }
        self._setup_endpoints()

    def _setup_endpoints(self) -> None:
        """Setup API endpoints - to be implemented by child classes."""
        raise NotImplementedError

    def _process_file(
        self,
        file_path: Optional[str],
        file_content: Optional[str],
        file_type: Optional[str],
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Common file processing logic."""
        # Validate inputs
        is_valid, error_message = validate_parser_inputs(
            file_path=file_path, file_content=file_content, file_type=file_type
        )

        if not is_valid:
            return None, None, error_message

        if file_content is None and file_path is not None:
            try:
                with open(file_path, "rb") as file:
                    file_read = file.read()
                    file_content = base64.b64encode(file_read).decode("utf-8")
                    file_type = Path(file_path).suffix.lower().lstrip(".")
            except Exception as e:
                return None, None, f"Error: {e}"

        return file_content, file_type, None
