"""Testing Synchronous and Asynchronous Extraction"""

import os
import sys
import unittest

import Levenshtein

sys.path.append(".")


from any_parser import AnyParser


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
        self.ap = AnyParser(self.api_key)

    def test_sync_extract(self):
        """Synchronous Extraction"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/correct_output.txt"

        markdown, elapsed_time = self.ap.extract(working_file)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )
        self.assertIn("Time Elapsed", elapsed_time)

    def test_async_extract_and_fetch(self):
        """Asynchronous Extraction and Fetch"""
        working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        correct_output_file = "./tests/correct_output.txt"

        file_id = self.ap.async_extract(working_file)
        self.assertNotIn(
            "error", file_id.lower(), "Error occurred during async extraction"
        )

        markdown = self.ap.async_fetch(file_id=file_id)
        correct_output = get_ground_truth(correct_output_file)
        percentage = compare_markdown(markdown, correct_output)

        self.assertGreaterEqual(
            percentage, 90, f"Output similarity too low: {percentage:.2f}%"
        )


if __name__ == "__main__":
    unittest.main()
