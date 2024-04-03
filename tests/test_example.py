from open_parser import OpenParser

if __name__ == "__main__":

    example_apikey = "1PW5Li5aif4wuv9bG5f1KaEJkJEnxrmF95esi4FM"
    example_local_file = "./schedule.pdf"

    op = OpenParser(example_apikey)

    print("file content extraction test:")
    content_result = op.extract(example_local_file)
    print(type(content_result))
    print(content_result)

    print("file information QA test:")
    example_prompt = "This is a test, simply return filename and 'test'"
    qa_result = op.parse(example_local_file, example_prompt)
    print(type(qa_result))
    print(qa_result)
