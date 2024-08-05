import os
import sys

from dotenv import load_dotenv

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from any_parser import AnyParser  # noqa: E402

if __name__ == "__main__":
    load_dotenv()

    example_apikey = os.getenv("CAMBIO_API_KEY")
    example_local_file = "./sample_data/test2.pdf"

    any_parser_instance = AnyParser(example_apikey)

    print("file/document extraction test:")
    content_result = any_parser_instance.extract(example_local_file)
    print(type(content_result))
    print(content_result)
