# 🌊 AnyParser

AnyParser provides an API to accurately extract your unstructured data (e.g. PDF, images, charts) into structured format.

## :seedling: Set up your AnyParser API key

You can generate your keys at the [Playground Account Page](https://www.cambioml.com/account) with up to 2 keys and 100 total free pages per account.

> ⚠️ **Note:** The free API is limited to 10 pages/call.

If you're interested in more AnyParser usage and applications, please reach out at info@cambioml.com for details.


To set up your API key `CAMBIO_API_KEY`, you will need to :

1. create a `.env` file in your root folder;
2. add the following one line to your `.env file:
    ```
    CAMBIO_API_KEY=0cam************************
    ```

## :computer: Installation

```
conda create -n any-parse python=3.10 -y
conda activate any-parse
pip3 install any-parser
```

If you want to run pdf_to_markdown.ipynb, install the following:
- Mac:
    ```
    brew install poppler
    ```
- Linux:
    ```
    sudo apt update
    sudo apt install poppler-utils
    ```
- Windows:
    ```
    choco install poppler
    ```

## :scroll:  Examples

AnyParser can extract text, numbers and symbols from PDF, images, etc. Check out each notebook below to run AnyParser within 10 lines of code!

### [Extract all text and layout from PDF into Markdown Format](https://github.com/CambioML/any-parser/blob/main/examples/pdf_to_markdown.ipynb)
Are you an AI engineer who need to ACCURATELY extract both the text and its layout (e.g. table of content or markdown headers hierarchy) from a PDF. Check out this notebook demo (3-min read)!

### [Extract a Table from an Image into Markdown Format](https://github.com/CambioML/any-parser/blob/main/examples/extract_table_from_image_to_markdown.ipynb)
Are you a financial analyst who need to extract ACCURATE number from a table in an image or a PDF. Check out this notebook (3-min read)!

### [Extract all tables and from PDF into HTML, JSON, and CSV Format](https://github.com/CambioML/any-parser/blob/main/examples/extract_tables_from_pdf.ipynb)
Are you an AI engineer who need to ACCURATELY extract tables from a PDF? Check out this notebook demo (3-min read)!