"""Testing Synchronous and Asynchronous Extraction"""

import os
import sys
import unittest

from any_parser import AnyParser

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")


class TestAnyParser(unittest.TestCase):
    """Testing Any Parser"""

    def setUp(self):
        # get secret API key
        self.api_key = os.environ.get("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY environment variable is not set")
        print("we got api key: ", self.api_key)
        self.file_path = "../examples/sample_data/stoxx_index_guide_0003.pdf"
        # create instance of AnyParser
        self.ap = AnyParser(self.api_key)

    def test_sync_extract(self):
        """Synchronous Extraction"""
        md_output, total_time = self.ap.extract(self.file_path)
        self.assertIsNotNone(md_output)
        self.assertIsInstance(total_time, str)
        self.assertTrue(total_time.startswith("Time Elapsed:"))

    def test_async_extract_and_fetch(self):
        """Asynchronous Extraction and Fetch"""
        file_id = self.ap.async_extract(self.file_path)
        self.assertIsNotNone(file_id)

        md = self.ap.async_fetch(file_id=file_id)
        self.assertIsNotNone(md)


if __name__ == "__main__":
    unittest.main()
