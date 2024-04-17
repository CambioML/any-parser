#!/bin/bash
source open_parser_base.sh

# Check if number of arguments is not equal to 3
if [ "$#" -lt 2 ]; then
    echo "Error: Missing arguments
    Usage: $0 <apiKey> <file_path> <prompt (optional, default="")>"
    exit 1
fi

apiKey="$1"
file_path="$2"
prompt="$3"
textract=false

echo "Parsing $file_path..."

upload
parse

echo "$result"