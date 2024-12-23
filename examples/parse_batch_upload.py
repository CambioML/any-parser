"""Batch API Folder Processing Upload Example"""

import json
import os
from datetime import datetime

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
responses = ap.batches.create(WORKING_FOLDER)

# Save responses to JSONL file with timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file = f"./sample_data_{timestamp}.jsonl"

with open(output_file, "w") as f:
    for response in responses:
        f.write(json.dumps(response.model_dump()) + "\n")

print(f"Upload responses saved to: {output_file}")
