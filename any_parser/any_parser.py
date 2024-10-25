"""AnyParser RT: Real-time parser for any data format."""

import base64
import json
import time
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple

import requests

from any_parser.utils import (
    ModelType,
    check_file_type_and_path,
    check_model,
    check_resume_extract_type,
    upload_file_to_presigned_url,
)

PUBLIC_SHARED_BASE_URL = "https://public-api.cambio-ai.com"
TIMEOUT = 60


class ProcessType(Enum):
    FILE = "file"
    TABLE = "table"
    FILE_REFINED = "file_refined"
    FILE_REFINED_QUICK = "file_refined_quick"


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
        self._sync_extract_url = f"{base_url}/extract"
        self._sync_json_url = f"{base_url}/json/extract"
        self._sync_resume_url = f"{base_url}/resume/extract"
        self._sync_refined_url = f"{base_url}/refined_parse"
        self._async_upload_url = f"{base_url}/async/upload"
        self._async_fetch_url = f"{base_url}/async/fetch"
        self._api_key = api_key
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": self._api_key,
        }

    def extract(
        self,
        file_path: str,
        model: ModelType = ModelType.BASE,
        extract_args: Optional[Dict] = None,
    ) -> Tuple[str, str]:
        """Extract full content from a file in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
            model (ModelType): The model to use for extraction. Can be
                `ModelType.BASE` or `ModelType.PRO`. Defaults to `ModelType.BASE`.
            extract_args (Optional[Dict]): Additional extraction arguments added
                to the prompt.

        Returns:
            tuple(str, str): The extracted data and the time taken.
        """

        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)

        if error:
            return error, None

        error = check_model(model)
        if error:
            return error, None

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

        if model == ModelType.BASE:
            url = self._sync_extract_url
        elif model == ModelType.PRO:
            url = self._sync_refined_url
            if model == ModelType.PRO:
                payload["quick_mode"] = True
        else:
            return "Error: Invalid model type", None

        # Send the POST request
        start_time = time.time()
        response = requests.post(
            url,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )
        end_time = time.time()

        # Check if the request was successful
        if response.status_code == 200:
            try:
                response_data = response.json()
                response_list = []
                for text in response_data["markdown"]:
                    response_list.append(text)
                markdown_text = "\n".join(response_list)
                return (
                    markdown_text,
                    f"Time Elapsed: {end_time - start_time:.2f} seconds",
                )
            except json.JSONDecodeError:
                return f"Error: Invalid JSON response: {response.text}", None
        else:
            return f"Error: {response.status_code} {response.text}", None

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
        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)
        if error:
            return error, None

        # Encode the file content in base64
        with open(file_path, "rb") as file:
            encoded_file = base64.b64encode(file.read()).decode("utf-8")

        # Create the JSON payload
        payload = {
            "file_content": encoded_file,
            "file_type": file_extension,
            "instruction_args": {"extract_instruction": extract_instruction},
        }

        # Send the POST request
        start_time = time.time()
        response = requests.post(
            self._sync_json_url,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )
        end_time = time.time()

        # Check if the request was successful
        if response.status_code == 200:
            try:
                response_data = response.json()
                result = response_data["json"]
                return (
                    result,
                    f"Time Elapsed: {end_time - start_time:.2f} seconds",
                )
            except json.JSONDecodeError:
                return f"Error: Invalid JSON response: {response.text}", None
        else:
            return f"Error: {response.status_code} {response.text}", None

    def resume_extract(
        self,
        file_path: str,
        extract_type: Dict,
    ) -> Tuple[str, str]:
        """Extract resume in real-time.

        Args:
            file_path (str): The path to the file to be parsed.
            extract_type (str): The type of extraction to be performed. It can be one of the following:
                - "education": Education
                - "work_experience": Work Experience
                - "personal_info": Personal Information
                - "skills": Skills
                - "certifications": Certifications
                - "projects": Projects
                - "pii": Personally Identifiable Information - includes only name, email, and phone
        Returns:
            tuple(str, str): The extracted data and the time taken.
        """
        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)
        if error:
            return error, None

        error = check_resume_extract_type(extract_type)
        if error:
            return error, None

        # Encode the file content in base64
        with open(file_path, "rb") as file:
            encoded_file = base64.b64encode(file.read()).decode("utf-8")

        # Create the JSON payload
        payload = {
            "file_content": encoded_file,
            "file_type": file_extension,
            "extract_type": extract_type,
        }

        # Send the POST request
        start_time = time.time()
        response = requests.post(
            self._sync_resume_url,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )
        end_time = time.time()

        # Check if the request was successful
        if response.status_code == 200:
            try:
                response_data = response.json()
                result = response_data["extraction_result"]
                if extract_type in result:
                    result = result[extract_type]
                return (
                    result,
                    f"Time Elapsed: {end_time - start_time:.2f} seconds",
                )
            except json.JSONDecodeError:
                return f"Error: Invalid JSON response: {response.text}", None
        else:
            return f"Error: {response.status_code} {response.text}", None

    def async_extract(
        self,
        file_path: str,
        model: ModelType = ModelType.BASE,
        extract_args: Optional[Dict] = None,
    ) -> str:
        """Extract full content from a file asynchronously.

        Args:
            file_path (str): The path to the file to be parsed.
            model (ModelType): The model to use for extraction. Can be
                `ModelType.BASE` or `ModelType.PRO`. Defaults to `ModelType.BASE`.
            extract_args (Optional[Dict]): Additional extraction arguments added to prompt
        Returns:
            str: The file id of the uploaded file.
        """
        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)

        if error:
            return error, None

        error = check_model(model)
        if error:
            return error, None

        file_name = Path(file_path).name

        if model == ModelType.BASE:
            process_type = ProcessType.FILE
        elif model == ModelType.PRO:
            process_type = ProcessType.FILE_REFINED_QUICK
        else:
            return "Error: Invalid model type", None

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
        file_extension = Path(file_path).suffix.lower().lstrip(".")

        # Check if the file exists and file_type
        error = check_file_type_and_path(file_path, file_extension)

        if error:
            return error, None

        file_name = Path(file_path).name

        # Create the JSON payload
        payload = {
            "file_name": file_name,
            "process_type": "json",
            "extract_args": {"extract_instruction": extract_instruction},
        }

        # Send the POST request
        response = requests.post(
            self._async_upload_url,
            headers=self._headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )

        # If response successful, upload the file
        return upload_file_to_presigned_url(file_path, response)

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
            elif "markdown" in result:
                markdown_list = result["markdown"]
                return "\n".join(markdown_list)
            return f"Error: Invalid response format\n {result}"
        if response.status_code == 202:
            return None
        return f"Error: {response.status_code} {response.text}"
