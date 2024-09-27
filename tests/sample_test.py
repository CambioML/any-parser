"""Testing Synchronous and Asynchronous Extraction"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(".")
from any_parser import AnyParser


class TestAnyParser(unittest.TestCase):
    """Testing Any Parser"""

    def setUp(self):
        # get secret API key
        self.api_key = os.environ.get("API_KEY")
        # TODO: remove
        # self.api_key = "U1xoe4F7qQ9MGJkiMFtR240r3r2iF6NQaAMUEYYc"
        self.file_path = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        # create instance of AnyParser
        self.ap = AnyParser(api_key=self.api_key)

    @patch("requests.post")
    def test_extract_success(self, mock_post):
        """Test successful real-time extraction."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "markdown": ["# Slide 1: Title", "Some text content"]
        }
        mock_post.return_value = mock_response

        result, elapsed_time = self.ap.extract(self.file_path)

        self.assertEqual(result, "# Slide 1: Title\nSome text content")
        self.assertIn("Time Elapsed", elapsed_time)

    @patch("pathlib.Path.is_file", return_value=True)
    def test_extract_unsupported_file_type(self, mock_is_file):
        """Test extraction with unsupported file type."""
        unsupported_file = "testfile.txt"
        result, elapsed_time = self.ap.extract(unsupported_file)

        self.assertEqual(
            result,
            (
                "Error: Unsupported file type: txt. Supported file types include "
                "pdf, doc, docx, ppt, pptx, jpg, jpeg, png, gif"
            ),
        )
        self.assertIsNone(elapsed_time)
        mock_is_file.assert_called()

    def test_extract_file_not_exist(self):
        """Test extraction with a non-existent file."""
        result, elapsed_time = self.ap.extract("nonexistent.docx")

        self.assertEqual(result, "Error: File does not exist: nonexistent.docx")
        self.assertIsNone(elapsed_time)

    @patch("requests.post")
    def test_extract_api_error(self, mock_post):
        """Test API error during real-time extraction."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        result, elapsed_time = self.ap.extract(self.file_path)

        self.assertEqual(result, "Error: 500 Internal Server Error")
        self.assertIsNone(elapsed_time)

    @patch("requests.post")
    @patch("pathlib.Path.is_file", return_value=True)
    def test_async_extract_success(self, mock_post, mock_is_file):
        """Test successful async file upload."""

        # Mock the initial async API response for presigned URL generation
        mock_response = MagicMock()
        mock_response.status_code = 200  # Correctly mock a 200 status code
        mock_response.json.return_value = {
            "fileId": "12345",
            "presignedUrl": {"url": "http://mockurl.com/upload", "fields": {}},
        }

        # Mock the presigned URL upload response (successful 204 status code)
        mock_upload_response = MagicMock()
        mock_upload_response.status_code = 204  # Simulating successful upload

        # Set side_effect for two calls:
        # 1. First call returns presigned URL and fileId
        # 2. Second call returns a successful 204 status after uploading
        mock_post.side_effect = [mock_response, mock_upload_response]

        # Call async_extract
        print("Before async_extract call")
        file_id = self.ap.async_extract(self.file_path)
        print("After async_extract call")

        # Debugging: Print the call arguments for each request
        print(f"Call args list: {mock_post.call_args_list}")

        # Assert that the correct file ID is returned
        self.assertEqual(file_id, "12345")

        # Check that both requests.post were called
        self.assertEqual(mock_post.call_count, 2)

        # Check if the second request is sent to the correct URL
        self.assertEqual(mock_post.call_args_list[1][0][0], "http://mockurl.com/upload")

    def test_async_extract_file_not_exist(self):
        """Test async extraction with a non-existent file."""
        result = self.ap.async_extract("nonexistent.docx")
        self.assertEqual(result, "Error: File does not exist: nonexistent.docx")

    @patch("requests.post")
    def test_async_fetch_in_progress(self, mock_post):
        """Test async fetch in progress."""
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_post.return_value = mock_response

        result = self.ap.async_fetch("12345", sync=False)

        self.assertIsNone(result)

    @patch("requests.post")
    def test_async_fetch_success(self, mock_post):
        """Test successful async fetch."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "markdown": ["# Slide 1: Title", "Some text content"]
        }
        mock_post.return_value = mock_response

        result = self.ap.async_fetch("12345")

        self.assertEqual(result, "# Slide 1: Title\nSome text content")

    @patch("requests.post")
    def test_async_fetch_timeout(self, mock_post):
        """Test async fetch timeout."""
        mock_post.return_value = None
        result = self.ap.async_fetch("12345")
        self.assertEqual(result, "Error: timeout, no response received")


if __name__ == "__main__":
    unittest.main()
