"""Testing Aynchronous Extraction"""

import sys

from any_parser import AnyParser

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

# define API key and file path
API_KEY = "U1xoe4F7qQ9MGJkiMFtR240r3r2iF6NQaAMUEYYc"
FILE_PATH = "./sample_data/stoxx_index_guide_0003.pdf"

# create instance of AnyParser
ap = AnyParser(API_KEY)

# asynchronous extract job (extraction and result fetching are separate)
file_id = ap.async_extract(FILE_PATH)

# fetch results (5s polling)
md = ap.async_fetch(file_id=file_id)
print(md)
