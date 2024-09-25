"""Testing Syncrhonous Extraction"""

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

# synchronous extract job (both extraction and result fetching, 60s timeout)
md_output, total_time = ap.extract(FILE_PATH)
print(md_output)
print(total_time)
