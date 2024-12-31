EXTRACT_JSON_TEST_DATA = [
    {
        "working_file": "./examples/sample_data/test1.pdf",
        "extract_instruction": {
            "social_security_number": "the social security number of the employee",
            "ein": "the employer identification number",
            "first_name": "the first name of the employee",
            "last_name": "the last name of the employee",
        },
        "correct_output": {
            "social_security_number": ["758-58-5787"],
            "ein": ["78-8778788"],
            "first_name": ["Jesan"],
            "last_name": ["Rahaman"],
        },
    },
    # {
    #     "working_file": "./examples/sample_data/test_w2.pptx",
    #     "extract_instruction": {
    #         "social_security_number": "the social security number of the employee",
    #         "ein": "the employer identification number",
    #         "first_name": "the first name of the employee",
    #         "last_name": "the last name of the employee",
    #     },
    #     "correct_output": [
    #         {
    #             "social_security_number": ["758-58-5787"],
    #             "ein": ["78-8778788"],
    #             "first_name": ["Jesan"],
    #             "last_name": ["Rahaman"],
    #         }
    #     ],
    # },
    # {
    #     "working_file": "./examples/sample_data/test_w2.docx",
    #     "extract_instruction": {
    #         "social_security_number": "the social security number of the employee",
    #         "ein": "the employer identification number",
    #         "first_name": "the first name of the employee",
    #         "last_name": "the last name of the employee",
    #     },
    #     "correct_output": [
    #         {
    #             "social_security_number": ["758-58-5787"],
    #             "ein": ["78-8778788"],
    #             "first_name": ["Jesan"],
    #             "last_name": ["Rahaman"],
    #         }
    #     ],
    # },
    {
        "working_file": "./examples/sample_data/test_w2.png",
        "extract_instruction": {
            "social_security_number": "the social security number of the employee",
            "ein": "the employer identification number",
            "first_name": "the first name of the employee",
            "last_name": "the last name of the employee",
        },
        "correct_output": {
            "social_security_number": ["758-58-5787"],
            "ein": ["78-8778788"],
            "first_name": ["Jesan"],
            "last_name": ["Rahaman"],
        },
    },
]
