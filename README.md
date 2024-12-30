# 🌊 AnyParser
<p align="center">
  <a href="https://pypi.org/project/any-parser/"><img src="https://img.shields.io/pypi/v/any-parser.svg" alt="pypi_status" /></a>
  <a href="https://github.com/cambioml/any-parser/graphs/commit-activity"><img alt="Commit activity" src="https://img.shields.io/github/commit-activity/m/cambioml/any-parser?style=flat-square"/></a>
  <a href="https://join.slack.com/t/cambiomlworkspace/shared_invite/zt-1zes33rmt-20Rag043uvExUaUdvt5_xQ"><img src="https://badgen.net/badge/Join/Community/cyan?icon=slack" alt="Slack" /></a>
</p>

**AnyParser** provides an API to accurately extract unstructured data (e.g., PDFs, images, charts) into a structured format.

## :seedling: Set up your AnyParser API key

To get started, generate your API key from the [Sandbox Account Page](https://www.cambioml.com/account). Each account comes with **100 free pages**.

> ⚠️ **Note:** The free API is limited to 10 pages/call.

For more information or to inquire about larger usage plans, feel free to contact us at info@cambioml.com.

To set up your API key (`CAMBIO_API_KEY`), follow these steps:
1. Create a `.env` file in the root directory of your project.
2. Add the following line to the `.env` file:
```
CAMBIO_API_KEY=0cam************************
```


## :computer: Installation
### 1. Set Up a New Conda Environment and Install AnyParser
First, create and activate a new Conda environment, then install AnyParser:
```bash
conda create -n any-parse python=3.10 -y
conda activate any-parse
pip3 install any-parser
```
### 2. Create an AnyParser Instance Using Your API Key
Use your API key to create an instance of AnyParser. Make sure you’ve set up your .env file to store your API key securely:
```python
import os
from dotenv import load_dotenv
from any_parser import AnyParser

# Load environment variables
load_dotenv(override=True)

# Get the API key from the environment
example_apikey = os.getenv("CAMBIO_API_KEY")

# Create an AnyParser instance
ap = AnyParser(api_key=example_apikey)
```

### 3. Run Synchronous Extraction
To extract data synchronously and receive immediate results:
```python
# Extract content from the file and get the markdown output along with processing time
markdown, total_time = ap.parse(file_path="./data/test.pdf")
```

### 4. Run Asynchronous Extraction
For asynchronous extraction, send the file for processing and fetch results later:
```python
# Send the file to begin asynchronous extraction
file_id = ap.async_parse(file_path="./data/test.pdf")

# Fetch the extracted content using the file ID
markdown = ap.async_fetch(file_id=file_id)
```

### 5. Run Batch Extraction (Beta)
For batch extraction, send the file to begin processing and fetch results later:
```python
# Send the file to begin batch extraction
response = ap.batches.create(file_path="./data/test.pdf")
request_id = response.requestId

# Fetch the extracted content using the request ID
markdown = ap.batches.retrieve(request_id)
```

Batch API for folder input:
```python
# Send the folder to begin batch extraction
WORKING_FOLDER = "./sample_data"
# This will generate a jsonl with filename and requestID
response = ap.batches.create(WORKING_FOLDER)
```

Each response in the JSONL file contains:
- The filename
- A unique request ID
- Additional processing metadata
You can later use these request IDs to retrieve the extracted content for each file:

```python
# Fetch the extracted content using the request ID from the jsonl file
markdown = ap.batches.retrieve(request_id)
```
For more details about code implementation of batch API, refer to
[examples/parse_batch_upload.py](examples/parse_batch_upload.py)  and  [examples/parse_batch_fetch.py](examples/parse_batch_fetch.py) 

> ⚠️ **Note:** Batch extraction is currently in beta testing. Processing time may take up to 12 hours to complete.

## :scroll:  Examples
Check out these examples to see how you can utilize **AnyParser** to extract text, numbers, and symbols in fewer than 10 lines of code!

### [Extract all text and layout from PDF into Markdown Format](https://github.com/CambioML/any-parser/blob/rt-migration/examples/pdf_to_markdown.ipynb)
Are you an AI engineer looking to **accurately** extract both the text and layout (e.g., table of contents or Markdown headers hierarchy) from a PDF? Check out this [3-minute notebook demo](https://github.com/CambioML/any-parser/blob/rt-migration/examples/pdf_to_markdown.ipynb).

### [Extract a Table from an Image into Markdown Format](https://github.com/CambioML/any-parser/blob/rt-migration/examples/image_to_markdown.ipynb)
Are you a financial analyst needing to **accurately** extract numbers from a table within an image? Explore this [3-minute notebook example](https://github.com/CambioML/any-parser/blob/rt-migration/examples/image_to_markdown.ipynb).
