# 🌊 OpenParse

OpenParse provides an API to accurately extract your unstructured data (e.g. PDF, images, charts) into structured format.

## :seedling: Set up your OpenParser API key

OpenParse is still in private beta. If you are interested in testing our document models, please reach out at info@cambioml.com for a FREE API key.


To set up your API key `CAMBIO_API_KEY`, you will need to :

1. create a `.env` file in your root folder;
2. add the following one line to your `.env file:
    ```
    CAMBIO_API_KEY=17b************************
    ```

## :computer: Installation

```
conda create -n openparse python=3.10 -y
conda activate openparse
pip3 install open_parser
```

## :bashfile usage
To use OpenParse via `curl` requests, you can run the following bash command from the root folder of this repository:
```
bash parse.sh <your apiKey> <file path> <prompt for parse (optional, default="")>
```

For example, to extract a table from a PDF file, you can run the following command:
```
bash parse.sh gl**************************************  /path/to/your/file.pdf "Return the table in a JSON format with
 each box's key and value."
```

## :scroll:  Examples

OpenParse can extract text, numbers and symbols from PDF, images, etc. Check out each notebook below to run OpenParse within 10 lines of code!

### [Prompt to Extract Key-values into JSON from W2 (PDF)](https://github.com/CambioML/open-parser/blob/main/examples/prompt_to_extract_table_from_pdf_to_json.ipynb)
Do you want to extract key-values from a W2 PDF into JSON format? Check out this notebook (3-min read)!

### [Extract a Table from an Image into Markdown Format](https://github.com/CambioML/open-parser/blob/main/examples/extract_table_from_image_to_markdown.ipynb)
Are you a financial analyst who need to extract ACCURATE number from a table in an image or a PDF. Check out this notebook (3-min read)!