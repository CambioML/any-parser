"""Testing Synchronous and Asynchronous Extraction"""

import os
import sys
import unittest

import Levenshtein
from dotenv import load_dotenv

sys.path.append(".")
load_dotenv(override=True)
from any_parser import AnyParser  # noqa: E402


# helper functions
def get_ground_truth(file_path: str) -> str:
    """Get the ground truth from the file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def compare_markdown(generated_output: str, correct_output: str) -> float:
    """Compare the generated markdown to the correct markdown using Levenshtein Distance."""
    distance = Levenshtein.distance(generated_output, correct_output)

    max_len = max(len(generated_output), len(correct_output))
    similarity_percentage = ((max_len - distance) / max_len) * 100

    return similarity_percentage


class TestAnyParser(unittest.TestCase):
    """Testing Any Parser"""

    def setUp(self):
        self.api_key = os.environ.get("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY is not set")
        self.ap = AnyParser(self.api_key)

    def test_pdf_sync_extract(self):
        """Synchronous Extraction"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/outputs/correct_pdf_output.txt"

        # extract
        markdown, elapsed_time = self.ap.extract(working_file)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_pdf_async_extract_and_fetch(self):
        """Asynchronous Extraction and Fetch"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/outputs/correct_pdf_output.txt"

        # extract
        file_id = self.ap.async_extract(working_file)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown = self.ap.async_fetch(file_id=file_id)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )

    def test_docx_sync_extract(self):
        """Synchronous Extraction"""
        working_file = "./examples/sample_data/test_odf.docx"
        correct_output_file = "./tests/outputs/correct_docx_output.txt"

        # extract
        markdown, elapsed_time = self.ap.extract(working_file)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_docx_async_extract_and_fetch(self):
        """Asynchronous Extraction and Fetch"""
        working_file = "./examples/sample_data/test_odf.docx"
        correct_output_file = "./tests/outputs/correct_docx_output.txt"

        # extract
        file_id = self.ap.async_extract(working_file)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        # fetch
        markdown = self.ap.async_fetch(file_id=file_id)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )


if __name__ == "__main__":
    unittest.main()
