#!/bin/bash
source any_parser_base.sh

if [ "$#" -lt 3 ]; then
    echo "Error: Missing arguments
    Usage: $0 <api_key> <job type: extract | parse | instruct> <file path> <prompt for parse (optional, default="")> <parse mode (optional, default=basic): basic | advanced>"
    exit 1
fi

apiKey="$1"
func="$2"
file_path="$3"

if [ "$func" == "extract" ]; then
    upload
    extract
elif [ "$func" == "parse" ]; then
    prompt="$4"
    mode="$5"
    if [ -z "$mode" ] || [ "$mode" == "" ] || [ "$mode" == "advanced" ]; then
        textract="True"
    else
        textract="False"
    fi
    upload
    parse
elif [ "$func" == "instruct" ]; then
    prompt="$4"
    mode="$5"
    if [ -z "$mode" ] || [ "$mode" == "" ] || [ "$mode" == "advanced" ]; then
        textract="True"
    else
        textract="False"
    fi
    upload
    instruct
fi

echo "$result"
