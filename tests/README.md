# Testing
Overview of running tests for AnyParser sdk. These should be run before submitting any pull request.

These tests are written using the unittest framework in Python. The tests are located in the `tests/test.py` file. Test data is located in the `tests/test_data.py` file.

## Setup
1. Install the required packages by running the following command:
```bash
pip install Levenshtein
```
2. Add a `.env` file in the `tests` folder with the following content:
```bash
API_KEY=*************
```

## Running Tests
1. Make sure you are in the project root folder.
2. Run the following command:
```bash
./run_tests.sh
```

If you just want to run an individual test within the test.py file, you can run the following command:
```bash
python -m unittest -k <test_name>
```

For example, if you want to run `test_pdf_sync_extract`, you can run the following command:
```bash
python -m unittest -k test_pdf_sync_extract
```
