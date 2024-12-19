"""Testing Synchronous and Asynchronous Extraction"""

import base64
import os
import sys
import time
import unittest
from pathlib import Path

import Levenshtein
from dotenv import load_dotenv

from tests.test_data import EXTRACT_JSON_TEST_DATA

sys.path.append(".")
load_dotenv(override=True)
from any_parser import AnyParser  # noqa: E402


# helper functions
def get_ground_truth(file_path: str) -> str:
    """Get the ground truth from the file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def compare_markdown(generated_output: str, correct_output: str) -> float:
    """
    Compare the generated markdown to the correct markdown using
    Levenshtein Distance.
    """
    distance = Levenshtein.distance(generated_output, correct_output)

    max_len = max(len(generated_output), len(correct_output))
    similarity_percentage = ((max_len - distance) / max_len) * 100

    return similarity_percentage


class TestAnyParser(unittest.TestCase):
    """Testing Any Parser"""

    def setUp(self):
        self.api_key = os.environ.get("CAMBIO_API_KEY")
        if not self.api_key:
            raise ValueError("CAMBIO_API_KEY is not set")
        self.ap = AnyParser(self.api_key)

    def test_pdf_sync_parse(self):
        """Synchronous PDF Parse"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/outputs/correct_pdf_output.txt"

        # extract
        markdown_list, elapsed_time = self.ap.parse(file_path=working_file)
        markdown = "\n".join(markdown_list)
        print(markdown)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_pdf_sync_parse_with_file_content(self):
        """Synchronous PDF Parse with file content"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/outputs/correct_pdf_output.txt"

        with open(working_file, "rb") as file:
            file_content = base64.b64encode(file.read()).decode("utf-8")
            file_type = Path(working_file).suffix.lower().lstrip(".")

        # extract
        markdown_list, elapsed_time = self.ap.parse(
            file_content=file_content, file_type=file_type
        )
        markdown = "\n".join(markdown_list)

        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_pdf_async_parse_and_fetch(self):
        """Asynchronous PDF Parse and Fetch"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/outputs/correct_pdf_output.txt"

        # extract
        file_id = self.ap.async_parse(file_path=working_file)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown_list = self.ap.async_fetch(file_id=file_id)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )

    def test_pdf_async_parse_and_fetch_with_file_content(self):
        """Asynchronous PDF Parse and Fetch with file content"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/outputs/correct_pdf_output.txt"

        with open(working_file, "rb") as file:
            file_content = base64.b64encode(file.read()).decode("utf-8")
            file_type = Path(working_file).suffix.lower().lstrip(".")

        # extract
        file_id = self.ap.async_parse(file_content=file_content, file_type=file_type)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown_list = self.ap.async_fetch(file_id=file_id)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )

    def test_docx_sync_extract(self):
        """Synchronous Word Extraction"""
        working_file = "./examples/sample_data/test_odf.docx"
        correct_output_file = "./tests/outputs/correct_docx_output.txt"

        # extract
        markdown_list, elapsed_time = self.ap.parse(file_path=working_file)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_docx_async_parse_and_fetch(self):
        """Asynchronous Word Parse and Fetch"""
        working_file = "./examples/sample_data/test_odf.docx"
        correct_output_file = "./tests/outputs/correct_docx_output.txt"

        # extract
        file_id = self.ap.async_parse(file_path=working_file)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown_list = self.ap.async_fetch(file_id=file_id)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )

    def test_pptx_sync_extract(self):
        """Synchronous Powerpoint Extraction"""
        working_file = "./examples/sample_data/test_odf.pptx"
        correct_output_file = "./tests/outputs/correct_pptx_output.txt"

        # extract
        markdown_list, elapsed_time = self.ap.parse(file_path=working_file)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_pptx_async_parse_and_fetch(self):
        """Asynchronous Powerpoint Parse and Fetch"""
        working_file = "./examples/sample_data/test_odf.pptx"
        correct_output_file = "./tests/outputs/correct_pptx_output.txt"

        # extract
        file_id = self.ap.async_parse(file_path=working_file)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown_list = self.ap.async_fetch(file_id=file_id)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )

    def test_image_sync_extract(self):
        """Synchronous Image Extraction"""
        working_file = "./examples/sample_data/test3.png"
        correct_output_file = "./tests/outputs/correct_png_output.txt"

        # extract
        markdown_list, elapsed_time = self.ap.parse(file_path=working_file)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_image_async_parse_and_fetch(self):
        """Asynchronous Image Parse and Fetch"""
        working_file = "./examples/sample_data/test3.png"
        correct_output_file = "./tests/outputs/correct_png_output.txt"

        # extract
        file_id = self.ap.async_parse(file_path=working_file)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown_list = self.ap.async_fetch(file_id=file_id)
        markdown = "\n".join(markdown_list)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )

    def test_sync_extract_key_value(self):
        """
        Synchronous JSON Extraction with subtests for different file formats
        """
        for data in EXTRACT_JSON_TEST_DATA:
            with self.subTest(working_file=data["working_file"]):
                # extract
                key_value_result, elapsed_time = self.ap.extract_key_value(
                    file_path=data["working_file"],
                    extract_instruction=data["extract_instruction"],
                )

                # assertions
                self.assertEqual(key_value_result, data["correct_output"])
                self.assertIn("Time Elapsed", elapsed_time)

    def test_async_extract_key_value_and_fetch(self):
        """
        Asynchronous JSON Extraction with subtests for different file formats
        """
        for data in EXTRACT_JSON_TEST_DATA:
            with self.subTest(working_file=data["working_file"]):
                # extract
                file_id = self.ap.async_extract_key_value(
                    file_path=data["working_file"],
                    extract_instruction=data["extract_instruction"],
                )
                self.assertFalse(file_id.startswith("Error:"), file_id)
                # fetch
                key_value_result = self.ap.async_fetch(file_id=file_id)
                # assertions
                self.assertEqual(key_value_result, data["correct_output"])
                # wait 1 s between requests
                time.sleep(1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
