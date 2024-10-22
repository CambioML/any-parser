EXTRACT_JSON_TEST_DATA = [
    {
        "working_file": "./examples/sample_data/test1.pdf",
        "extract_instruction": {
            "social_security_number": "the social security number of the employee",
            "ein": "the employer identification number",
            "first_name": "the first name of the employee",
            "last_name": "the last name of the employee",
        },
        "correct_output": [
            [
                {
                    "social_security_number": "758-58-5787",
                    "ein": "78-8778788",
                    "first_name": "Jesan",
                    "last_name": "Rahaman",
                }
            ]
        ],
    },
    {
        "working_file": "./examples/sample_data/test_w2.pptx",
        "extract_instruction": {
            "social_security_number": "the social security number of the employee",
            "ein": "the employer identification number",
            "first_name": "the first name of the employee",
            "last_name": "the last name of the employee",
        },
        "correct_output": [
            [
                {
                    "social_security_number": "758-58-5787",
                    "ein": "78-8778788",
                    "first_name": "Jesan",
                    "last_name": "Rahaman",
                }
            ]
        ],
    },
    {
        "working_file": "./examples/sample_data/test_w2.docx",
        "extract_instruction": {
            "social_security_number": "the social security number of the employee",
            "ein": "the employer identification number",
            "first_name": "the first name of the employee",
            "last_name": "the last name of the employee",
        },
        "correct_output": [
            [
                {
                    "social_security_number": "758-58-5787",
                    "ein": "78-8778788",
                    "first_name": "Jesan",
                    "last_name": "Rahaman",
                }
            ]
        ],
    },
    {
        "working_file": "./examples/sample_data/test_w2.png",
        "extract_instruction": {
            "social_security_number": "the social security number of the employee",
            "ein": "the employer identification number",
            "first_name": "the first name of the employee",
            "last_name": "the last name of the employee",
        },
        "correct_output": [
            [
                {
                    "social_security_number": "758-58-5787",
                    "ein": "78-8778788",
                    "first_name": "Jesan",
                    "last_name": "Rahaman",
                }
            ]
        ],
    },
]

EXTRACT_RESUME_TEST_DATA = [
    {
        "working_file": "./examples/sample_data/test_resume.pdf",
        "correct_output": {
            "personal_info": {
                "name": "John Doe",
                "phone_number": "+1-123-456-7890",
                "address": "123 Main St, Anytown, USA",
                "email_address": "johndoe@example.com",
                "linkedin_url": "linkedin.com/in/johndoe",
                "github_url": "github.com/johndoe",
                "summary": "Experienced software developer with a passion for creating innovative solutions and a strong focus on full-stack development. Skilled in a variety of programming languages and frameworks, with a proven track record of delivering high-quality software in fast-paced environments.",
            },
            "education": [
                {
                    "organization": "University of Anytown",
                    "degree": "Bachelor of Science",
                    "major": "Computer Science",
                    "start_date": "2013-08-01",
                    "end_date": "2017-05-01",
                    "courses": [
                        "Data Structures",
                        "Algorithms",
                        "Web Development",
                        "Cloud Computing",
                        "Databases",
                    ],
                    "achievements": ["GPA: 3.8/4.0"],
                }
            ],
            "work_experience": [
                {
                    "job_title": "Senior Software Engineer",
                    "company_name": "Tech Solutions Corp",
                    "location": "Anytown, USA",
                    "start_date": "2022-01-01",
                    "end_date": "Present",
                    "job_type": None,
                    "summary": "Led a team of developers to design and implement scalable microservices architecture.",
                    "bullet_points": [
                        "Led a team of 5 developers to design and implement a scalable microservices architecture using Node.js and AWS Lambda.",
                        "Improved application performance by 30% through code optimization and database tuning.",
                        "Developed and deployed CI/CD pipelines using GitHub Actions and AWS CodePipeline.",
                        "Collaborated with product managers to define technical requirements and timelines for new features.",
                    ],
                },
                {
                    "job_title": "Full-Stack Developer",
                    "company_name": "Innovative Web Agency",
                    "location": "Somecity, USA",
                    "start_date": "2019-08-01",
                    "end_date": "2021-12-31",
                    "job_type": None,
                    "summary": "Built responsive web applications for a variety of clients.",
                    "bullet_points": [
                        "Built responsive web applications using React, TypeScript, and Tailwind CSS for a variety of clients.",
                        "Integrated third-party APIs (Stripe, Twilio) to enhance application functionality.",
                        "Maintained and updated legacy systems written in PHP and MySQL.",
                        "Spearheaded the migration of on-premise infrastructure to AWS, reducing hosting costs by 40%.",
                    ],
                },
            ],
            "skills": {
                "Programming Languages": [
                    "JavaScript",
                    "Typescript",
                    "Python",
                    "Java",
                    "SQL",
                ],
                "Tools": [
                    "Git",
                    "Github",
                    "Gitlab",
                    "Jira",
                    "Jenkins",
                ],
                "Other": [
                    "AWS",
                    "Docker",
                    "Kubernetes",
                    "Terraform",
                ],
            },
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect – Associate",
                    "description": "Certification demonstrating knowledge of AWS solutions architecture.",
                },
                {
                    "name": "Certified Kubernetes Administrator (CKA)",
                    "description": "Certification for Kubernetes administration skills.",
                },
                {
                    "name": "Google Cloud Professional DevOps Engineer",
                    "description": "Certification validating proficiency in Google Cloud DevOps practices.",
                },
            ],
            "projects": [
                {
                    "organization": None,
                    "project_name": "Project Management App",
                    "location": None,
                    "start_date": "2019-08-01",
                    "end_date": "2021-12-01",
                    "descriptions": [
                        "A React-based project management tool that allows teams to track tasks, set deadlines, and collaborate in real-time.",
                        "Integrated with Firebase for authentication and Firestore for real-time data sync.",
                    ],
                },
                {
                    "organization": None,
                    "project_name": "E-Commerce Platform",
                    "location": None,
                    "start_date": "2019-08-01",
                    "end_date": "2018-12-01",
                    "descriptions": [
                        "Built a fully functional e-commerce platform using Node.js, Express, and MongoDB.",
                        "Includes user authentication, product search and filtering, and an admin dashboard for order management.",
                    ],
                },
            ],
        },
    },
]
