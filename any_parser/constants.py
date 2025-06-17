from enum import Enum

# Default URLs for AnyParser
PUBLIC_SHARED_BASE_URL = "https://anyparser.cambioml.com/api/v1"
PUBLIC_BATCH_BASE_URL = "http://batch-api.cambioml.com" # TODO: Fix Later
TIMEOUT = 180

class ProcessType(Enum):
    EXTRACT_PII = "extract_pii"
    EXTRACT_TABLES = "extract_tables"
    EXTRACT_KEY_VALUE = "extract_key_value"
    PARSE = "parse"
    PARSE_PRO = "parse_pro"
    PARSE_TEXTRACT = "parse_textract"

