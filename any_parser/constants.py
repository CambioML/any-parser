from enum import Enum


class ProcessType(Enum):
    EXTRACT_PII = "extract_pii"
    EXTRACT_TABLES = "extract_tables"
    EXTRACT_KEY_VALUE = "extract_key_value"
    EXTRACT_RESUME_KEY_VALUE = "extract_resume_key_value"
    PARSE = "parse"
    PARSE_WITH_OCR = "parse_with_ocr"
    PARSE_WITH_LAYOUT = "parse_with_layout"
