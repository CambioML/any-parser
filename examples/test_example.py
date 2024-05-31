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

    op = AnyParser(example_apikey)

    print("file/document extraction test:")
    content_result = op.extract(example_local_file)
    print(type(content_result))
    print(content_result)

    print("information extraction test:")
    qa_result = op.parse(example_local_file)
    print(type(qa_result))
    print(qa_result)

    print("instruction extraction test:")
    example_prompt = "Return table under Investor Metrics in JSON format with year as the key and the column as subkeys."
    instruction_result = op.instruct(example_local_file, prompt=example_prompt)
    print(type(instruction_result))
    print(instruction_result)
