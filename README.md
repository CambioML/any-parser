# 🌊 AnyParser

AnyParser provides an API to accurately extract your unstructured data (e.g. PDF, images, charts) into structured format.

## :seedling: Set up your AnyParser API key

AnyParser is still in private beta. If you are interested in testing our document models, please reach out at info@cambioml.com for a FREE testing API key.


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

## bashfile usage
To use AnyParser via `curl` requests, you can run the following bash command from the root folder of this repository:
```
bash parse.sh <your apiKey> <file path> <prompt for parse (optional, default="")>
```

For example, to extract a table from a PDF file, you can run the following command:
```
bash parse.sh gl**************************************  /path/to/your/file.pdf "Return the table in a JSON format with each box's key and value."
```

## :scroll:  Examples

AnyParser can extract text, numbers and symbols from PDF, images, etc. Check out each notebook below to run AnyParser within 10 lines of code!

### [Extract a Table from PDF into Excel](https://github.com/CambioML/any-parser/blob/main/demo/pdf_to_html_to_excel.ipynb)
Do you want to extract a complicated table from a financial report (PDF) into Excel spread sheet? Check out this notebook (3-min read)!

### [Extract a Table from an Image into Markdown Format](https://github.com/CambioML/any-parser/blob/main/examples/extract_table_from_image_to_markdown.ipynb)
Are you a financial analyst who need to extract ACCURATE number from a table in an image or a PDF. Check out this notebook (3-min read)!
