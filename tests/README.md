# Testing
Overview of running tests for AnyParser sdk. These should be run before submitting any pull request.

These tests are written using the unittest framework in Python. The tests are located in the `tests/test.py` file. Test data is located in the `tests/test_data.py` file.

## Setup
1. Install the required packages by running the following command:
```bash
poetry install
```
In the `dev.dependencies` section of the `pyproject.toml` file, you will see the packages that are installed.

2. Add a `.env` file in the `tests` folder with the following content:
```bash
CAMBIO_API_KEY=*************
```

## Pre-commit
This project uses pre-commit to run checks before committing code. To initialize `pre-commit` for this repo, run the following command:
```bash
pre-commit install
```

Now, with every commit, the checks will run automatically on the files added to the commit. The checks include:
- `black` for code formatting
- `flake8` for linting
- `isort` for import sorting
- running the unit tests in `tests/test.py`

If you want to run the checks manually, you can run the following command:
```bash
pre-commit run --all-files
```

## Running Tests Manually
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
