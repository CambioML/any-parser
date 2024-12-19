"""Batch API Folder Processing Upload Example"""

import os

from dotenv import load_dotenv

from any_parser import AnyParser

# Load environment variables
load_dotenv(override=True)

# Get API key and create parser
api_key = os.environ.get("CAMBIO_API_KEY")
if not api_key:
    raise ValueError("CAMBIO_API_KEY is not set")
ap = AnyParser(api_key)

# Upload folder for batch processing
WORKING_FOLDER = "./sample_data"
response = ap.batches.create(WORKING_FOLDER)

print(f"Upload response saved to: {response}")
