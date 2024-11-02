"""Testing Synchronous and Asynchronous Extraction"""

import os
import sys
import time
import unittest

import Levenshtein
from dotenv import load_dotenv

from tests.test_data import EXTRACT_JSON_TEST_DATA, EXTRACT_RESUME_TEST_DATA

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
        self.api_key = os.environ.get("CAMBIO_API_KEY")
        if not self.api_key:
            raise ValueError("CAMBIO_API_KEY is not set")
        self.ap = AnyParser(self.api_key)

    def test_pdf_sync_extract(self):
        """Synchronous PDF Extraction"""
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
        """Asynchronous PDF Extraction and Fetch"""
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
        """Synchronous Word Extraction"""
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
        """Asynchronous Word Extraction and Fetch"""
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

    def test_pptx_sync_extract(self):
        """Synchronous Powerpoint Extraction"""
        working_file = "./examples/sample_data/test_odf.pptx"
        correct_output_file = "./tests/outputs/correct_pptx_output.txt"

        # extract
        markdown, elapsed_time = self.ap.extract(working_file)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_pptx_async_extract_and_fetch(self):
        """Asynchronous Powerpoint Extraction and Fetch"""
        working_file = "./examples/sample_data/test_odf.pptx"
        correct_output_file = "./tests/outputs/correct_pptx_output.txt"

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

    def test_image_sync_extract(self):
        """Synchronous Image Extraction"""
        working_file = "./examples/sample_data/test3.png"
        correct_output_file = "./tests/outputs/correct_png_output.txt"

        # extract
        markdown, elapsed_time = self.ap.extract(working_file)
        self.assertFalse(markdown.startswith("Error:"), markdown)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_image_async_extract_and_fetch(self):
        """Asynchronous Image Extraction and Fetch"""
        working_file = "./examples/sample_data/test3.png"
        correct_output_file = "./tests/outputs/correct_png_output.txt"

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

    def test_sync_extract_key_value(self):
        """Synchronous JSON Extraction with subtests for different file formats"""
        for data in EXTRACT_JSON_TEST_DATA:
            with self.subTest(working_file=data["working_file"]):
                # extract
                key_value_result, elapsed_time = self.ap.extract_key_value(
                    data["working_file"], data["extract_instruction"]
                )

                # assertions
                self.assertEqual(key_value_result, data["correct_output"])
                self.assertIn("Time Elapsed", elapsed_time)

    def test_async_extract_key_value_and_fetch(self):
        """Asynchronous JSON Extraction with subtests for different file formats"""
        for data in EXTRACT_JSON_TEST_DATA:
            with self.subTest(working_file=data["working_file"]):
                # extract
                file_id = self.ap.async_extract_key_value(
                    data["working_file"], data["extract_instruction"]
                )
                self.assertFalse(file_id.startswith("Error:"), file_id)
                # fetch
                key_value_result = self.ap.async_fetch(file_id=file_id)
                # assertions
                self.assertEqual(key_value_result, data["correct_output"])
                # wait 1 s between requests
                time.sleep(1)

    def test_sync_extract_resume_key_value(self):
        """Synchronous Resume Extraction with subtests for different file formats"""
        for data in EXTRACT_RESUME_TEST_DATA:
            for extract_type in data["correct_output"]:
                with self.subTest(
                    working_file=data["working_file"], extract_type=extract_type
                ):
                    # extract
                    key_value_result, elapsed_time = self.ap.extract_resume_key_value(
                        data["working_file"], extract_type=extract_type
                    )
                    print("\n\n Key Value Result: ")
                    print(key_value_result)
                    print("\n\n Correct Output: ")
                    print(data["correct_output"][extract_type])

                    # TODO: update with proper value checking
                    # get levenshtein distance from string of correct output vs. key value result
                    percentage = compare_markdown(
                        str(key_value_result), str(data["correct_output"][extract_type])
                    )

                    self.assertGreaterEqual(
                        percentage,
                        80,
                        f"Output similarity too low: {percentage:.2f}%",
                    )

                    self.assertIn("Time Elapsed", elapsed_time)
                    # wait 1 s between requests
                    time.sleep(1)

    def test_async_extract_resume_key_value_and_fetch(self):
        """Asynchronous Resume Extraction and Fetch"""
        for data in EXTRACT_RESUME_TEST_DATA:
            for extract_type in data["correct_output"]:
                with self.subTest(
                    working_file=data["working_file"], extract_type=extract_type
                ):
                    # extract
                    file_id = self.ap.async_extract_resume_key_value(
                        data["working_file"], extract_type=extract_type
                    )
                    self.assertFalse(file_id.startswith("Error:"), file_id)
                    # fetch
                    extract_resume_result = self.ap.async_fetch(file_id=file_id)
                    # TODO: update with proper value checking
                    # get levenshtein distance from string of correct output vs. key value result
                    percentage = compare_markdown(
                        str(extract_resume_result),
                        str(data["correct_output"][extract_type]),
                    )

                    self.assertGreaterEqual(
                        percentage,
                        80,
                        f"Output similarity too low: {percentage:.2f}%",
                    )
                    # wait 1 s between requests
                    time.sleep(1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
