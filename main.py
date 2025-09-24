import os
from dotenv import load_dotenv
from any_parser import AnyParser

# Load environment variables
load_dotenv(override=True)

# Get the API key from the environment
example_apikey = os.getenv("CAMBIO_API_KEY")

# Create an AnyParser instance
ap = AnyParser(api_key=example_apikey)

# Extract content with beautiful terminal UI display
markdown, total_time = ap.parse(
    file_path="./data/qa.pdf",
    show_ui=True  # This enables the formatted terminal display
)

# The results will automatically display in a nice format

# Timing
print("\nProcessing Time (seconds):", total_time)