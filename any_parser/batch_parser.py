"""Batch parser implementation."""

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Union

import requests
from pydantic import BaseModel, Field

from any_parser.base_parser import BaseParser

TIMEOUT = 60
MAX_WORKERS = 10

logger = logging.getLogger(__name__)


class UploadResponse(BaseModel):
    fileName: str
    requestId: str
    requestStatus: str


class UsageResponse(BaseModel):
    pageLimit: int
    pageRemaining: int


class FileStatusResponse(BaseModel):
    fileName: str
    fileType: str
    requestId: str
    requestStatus: str
    uploadTime: str
    completionTime: Optional[str] = None
    result: Optional[List[str]] = Field(default_factory=list)
    error: Optional[List[str]] = Field(default_factory=list)


class BatchParser(BaseParser):
    def __init__(self, api_key: str, base_url: str) -> None:
        super().__init__(api_key, base_url)
        self._file_upload_url = f"{self._base_url}/files/"
        self._processing_status_url = f"{self._base_url}/files/" + "{request_id}"
        self._usage_url = f"{self._base_url}/users/current/usage"

        # remove "Content-Type" from headers
        self._headers.pop("Content-Type")

    def create(self, file_path: str) -> Union[UploadResponse, List[UploadResponse]]:
        """Upload a single file or folder for batch processing.

        Args:
            file_path: Path to the file or folder to upload

        Returns:
            If file: Single UploadResponse object containing upload details
            If folder: List of UploadResponse objects for each file
        """
        path = Path(file_path)
        if path.is_file():
            return self._upload_single_file(path)
        elif path.is_dir():
            return self._upload_folder(path)
        else:
            raise ValueError(f"Path {file_path} does not exist")

    def _upload_single_file(self, file_path: Path) -> UploadResponse:
        """Upload a single file for batch processing."""
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                self._file_upload_url,
                headers=self._headers,
                files=files,
                timeout=TIMEOUT,
            )

            if response.status_code != 200:
                raise Exception(f"Upload failed: {response.text}")

            data = response.json()
            return UploadResponse(
                fileName=data["fileName"],
                requestId=data["requestId"],
                requestStatus=data["requestStatus"],
            )

    def _upload_folder(self, folder_path: Path) -> List[UploadResponse]:
        """Upload all files in a folder for batch processing.

        Args:
            folder_path: Path to the folder containing files to upload

        Returns:
            List of UploadResponse objects for each uploaded file
        """
        # Get all files in folder and subfolders
        files = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                files.append(Path(root) / filename)

        # Upload files concurrently using thread pool
        responses = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_file = {
                executor.submit(self._upload_single_file, file_path): file_path
                for file_path in files
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    response = future.result()
                    responses.append(response)
                except Exception as e:
                    logger.error(f"Failed to upload {file_path}: {str(e)}")

        return responses

    def retrieve(self, request_id: str) -> FileStatusResponse:
        """Get the processing status of a file.

        Args:
            request_id: The ID of the file processing request

        Returns:
            FileProcessingStatus object containing status details
        """
        response = requests.get(
            self._processing_status_url.format(request_id=request_id),
            headers=self._headers,
            timeout=TIMEOUT,
        )

        if response.status_code != 200:
            raise Exception(f"Status check failed: {response.text}")

        data = response.json()
        return FileStatusResponse(**data)

    def get_usage(self) -> UsageResponse:
        """Get current usage information.

        Returns:
            UsageResponse object containing usage details
        """
        response = requests.get(
            self._usage_url,
            headers=self._headers,
            timeout=TIMEOUT,
        )

        if response.status_code != 200:
            raise Exception(f"Usage check failed: {response.text}")

        data = response.json()
        return UsageResponse(
            pageLimit=data["pageLimit"], pageRemaining=data["pageRemaining"]
        )
