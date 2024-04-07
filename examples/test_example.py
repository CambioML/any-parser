import os
import sys

from dotenv import load_dotenv

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from open_parser import OpenParser  # noqa: E402

if __name__ == "__main__":
    load_dotenv()

    example_apikey = os.getenv("CAMBIO_API_KEY")

    example_local_file = "./sample_data/test2.pdf"

    op = OpenParser(example_apikey)

    print("file/document extraction test:")
    content_result = op.extract(example_local_file)
    print(type(content_result))
    print(content_result)

    print("information extraction test:")
    example_prompt = "Return table under Investor Metrics in JSON format with year as the key and the column as subkeys."
    qa_result = op.parse(example_local_file, example_prompt, mode="basic")
    print(type(qa_result))
    print(qa_result)
