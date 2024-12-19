"""Test batch API folder fetch response"""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

from any_parser import AnyParser

# Load environment variables
load_dotenv(override=True)

MAX_WORKER = 10

# Get API key and create parser
api_key = os.environ.get("CAMBIO_API_KEY")
if not api_key:
    raise ValueError("CAMBIO_API_KEY is not set")
ap = AnyParser(api_key)

# Read responses from JSONL file
# Change to your real output json from parse_batch_upload.py
response_file = "./sample_data_20241219190049.jsonl"
with open(response_file, "r") as f:
    responses = [json.loads(line) for line in f]


def process_response(response):
    """Process a single response by retrieving markdown content"""
    request_id = response["requestId"]
    try:
        markdown = ap.batches.retrieve(request_id)
        if markdown:
            response["result"] = [markdown.result[0] if markdown.result else ""]
            response["requestStatus"] = "COMPLETED"
            response["completionTime"] = markdown.completionTime
    except Exception as e:
        print(f"Error processing {request_id}: {str(e)}")
        response["error"] = [str(e)]
    return response


# Process responses concurrently
with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
    future_to_response = {
        executor.submit(process_response, response): response for response in responses
    }

    updated_responses = []
    for future in as_completed(future_to_response):
        updated_response = future.result()
        updated_responses.append(updated_response)

# Write all updated responses back to file
with open(response_file, "w") as f:
    for response in updated_responses:
        f.write(json.dumps(response) + "\n")

print(f"Updated all responses in {response_file} with markdown content")
