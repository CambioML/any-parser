"""Batch parser implementation."""

from typing import List, Optional

import requests
from pydantic import BaseModel, Field

from any_parser.base_parser import BaseParser

TIMEOUT = 60


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

    def create(self, file_path: str) -> UploadResponse:
        """Upload a single file for batch processing.

        Args:
            file_path: Path to the file to upload

        Returns:
            FileUploadResponse object containing upload details
        """
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                self._file_upload_url,
                headers=self._headers,
                files=files,
                timeout=TIMEOUT,
            )
            print(response.json())

            if response.status_code != 200:
                raise Exception(f"Upload failed: {response.text}")

            data = response.json()
            return UploadResponse(
                fileName=data["fileName"],
                requestId=data["requestId"],
                requestStatus=data["requestStatus"],
            )

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
