from open_parser import OpenParser

if __name__ == "__main__":

    example_apikey = "1PW5Li5aif4wuv9bG5f1KaEJkJEnxrmF95esi4FM"
    example_local_file = "./schedule.pdf"

    op = OpenParser(example_apikey)
    result = op.extract_pdf_content(example_local_file)

    print(type(result))
    print(result)
