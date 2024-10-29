import json
from enum import Enum
from pathlib import Path

import requests


class ModelType(Enum):
    BASE = "base"
    PRO = "pro"
    ADVANCED = "advanced"


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


def check_model(model: ModelType) -> None:
    if model not in {ModelType.BASE, ModelType.PRO, ModelType.ADVANCED}:
        valid_models = ", ".join(["`" + model.value + "`" for model in ModelType])
        return f"Invalid model type: {model}. Supported `model` types include {valid_models}."


def check_file_type_and_path(file_path, file_extension):
    # Check if the file exists
    if not Path(file_path).is_file():
        return f"Error: File does not exist: {file_path}"

    if file_extension not in SUPPORTED_FILE_EXTENSIONS:
        supported_types = ", ".join(SUPPORTED_FILE_EXTENSIONS)
        return f"Error: Unsupported file type: {file_extension}. Supported file types include {supported_types}."
