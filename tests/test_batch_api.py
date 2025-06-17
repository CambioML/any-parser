# """Testing Batch API Extraction"""

# import os
# import sys
# import unittest

# from dotenv import load_dotenv

# sys.path.append(".")
# load_dotenv(override=True)
# from any_parser import AnyParser  # noqa: E402


# class TestAnyParserBatchAPI(unittest.TestCase):
#     """Testing Any Parser Batch API"""

#     def setUp(self):
#         self.api_key = os.environ.get("CAMBIO_API_KEY")
#         if not self.api_key:
#             raise ValueError("CAMBIO_API_KEY is not set")
#         self.ap = AnyParser(self.api_key)

#     def test_batch_api_create(self):
#         """Batch API Create"""
#         working_file = "./examples/sample_data/stoxx_index_guide_0003.pdf"

#         response = self.ap.batches.create(working_file)

#         self.assertIsNotNone(response)
#         self.assertEqual(response.requestStatus, "UPLOADED")

#         request_id = response.requestId
#         status = self.ap.batches.retrieve(request_id)
#         self.assertEqual(status.requestStatus, "UPLOADED")

#         quota = self.ap.batches.get_usage()
#         self.assertGreaterEqual(quota.pageRemaining, 0)
