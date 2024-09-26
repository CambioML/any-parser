"""Testing Synchronous and Asynchronous Extraction"""

import os
import random
import sys
import time
import unittest

from any_parser import AnyParser

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")


class TestAnyParser(unittest.TestCase):
    """Testing Any Parser"""

    @classmethod
    def setUpClass(cls):
        # Add a random delay between 0 and 10 seconds at the start of each test suite
        time.sleep(random.uniform(0, 20))

    def setUp(self):
        # get secret API key
        self.api_key = os.environ.get("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY environment variable is not set")
        self.file_path = "./examples/sample_data/stoxx_index_guide_0003.pdf"
        # create instance of AnyParser
        self.ap = AnyParser(self.api_key)

    def test_sync_extract(self):
        """Synchronous Extraction"""
        # Add a delay before making the API call
        time.sleep(random.uniform(1, 5))
        md_output, total_time = self.ap.extract(self.file_path)

        # check for specific content in the markdown
        self.assertFalse(md_output.startswith("Error:"), total_time)
        self.assertTrue(
            md_output.startswith("STOXX INDEX METHODOLOGY GUIDE"),
            "Extraction failed",
        )

        # returning time elapsed indicates success
        self.assertTrue(total_time.startswith("Time Elapsed:"))

    def test_async_extract_and_fetch(self):
        """Asynchronous Extraction and Fetch"""

        # check for error in sending extraction request
        # Add a delay before making the API call
        time.sleep(random.uniform(1, 5))
        file_id = self.ap.async_extract(self.file_path)
        self.assertFalse(file_id.startswith("Error:"), file_id)
        self.assertFalse(file_id.startswith("Request error:"), file_id)
        self.assertFalse(file_id.startswith("Upload error:"), file_id)

        # check for specific content in extraction result
        # Add another delay before fetching
        time.sleep(random.uniform(1, 5))
        md = self.ap.async_fetch(file_id=file_id)
        self.assertFalse(md.startswith("Error:"), md)
        self.assertTrue(
            md.startswith("STOXX INDEX METHODOLOGY GUIDE"),
            "Expected content not found at the start of the fetched result",
        )


if __name__ == "__main__":
    unittest.main()
