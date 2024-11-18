import json
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

import requests

SUPPORTED_FILE_EXTENSIONS = [
    "pdf",
    "doc",
    "docx",
    "ppt",
    "pptx",
    "jpg",
    "jpeg",
    "png",
    "gif",
]


class ValidationError(Enum):
    MISSING_INPUTS = "Either file_content or file_path must be provided"
    MISSING_FILE_TYPE = "file_type must be provided when using file_content"
    NOT_FOUND = "File does not exist: {}"
    UNSUPPORTED_FILE_TYPE = "Unsupported file type: {}. Supported file types: {}"
    FILE_EMPTY = "File is empty: {}"
    FILE_TOO_LARGE = "File size exceeds maximum limit of {} MB: {}"
    OTHER = "{}"


def validate_parser_inputs(
    file_path: Optional[str],
    file_content: Optional[str],
    file_type: Optional[str],
) -> Tuple[bool, str]:
    """Validate inputs for the parser.

    Args:
        file_content (Optional[str]): Base64 encoded file content
        file_path (Optional[str]): Path to the file
        file_type (Optional[str]): File extension/type

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        - is_valid: True if validation passes, False otherwise
        - error_message: "" if validation passes, error if validation fails
    """
    # Check if at least one input method is provided
    if file_content is None and file_path is None:
        return False, ValidationError.MISSING_INPUTS.value

    # Validate file_content path
    if file_content is not None and file_type is None:
        return False, ValidationError.MISSING_FILE_TYPE.value

    # Validate file path if provided
    if file_path is not None:
        path = Path(file_path)

        # Check if file exists
        if not path.is_file():
            return False, ValidationError.NOT_FOUND.value.format(file_path)

        # Check if file is empty
        if path.stat().st_size == 0:
            return False, ValidationError.FILE_EMPTY.value.format(file_path)

        # If file_type not provided, extract it from file_path
        if file_type is None:
            file_type = path.suffix.lower().lstrip(".")

    # Validate file type
    if file_type not in SUPPORTED_FILE_EXTENSIONS:
        supported_types = ", ".join(sorted(SUPPORTED_FILE_EXTENSIONS))
        return False, ValidationError.UNSUPPORTED_FILE_TYPE.value.format(
            file_type, supported_types
        )

    return True, ""


def upload_file_to_presigned_url(
    file_path: str, response: requests.Response, timeout: int = 10
) -> str:
    if response.status_code == 200:
        try:
            file_id = response.json().get("fileId")
            presigned_url = response.json().get("presignedUrl")
            with open(file_path, "rb") as file_to_upload:
                files = {"file": (file_path, file_to_upload)}
                upload_resp = requests.post(
                    presigned_url["url"],
                    data=presigned_url["fields"],
                    files=files,
                    timeout=timeout,
                )
                if upload_resp.status_code != 204:
                    return f"Error: {upload_resp.status_code} {upload_resp.text}"
            return file_id
        except json.JSONDecodeError:
            return "Error: Invalid JSON response"
    else:
        return f"Error: {response.status_code} {response.text}"
