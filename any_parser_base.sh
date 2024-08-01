UPLOAD_URL="https://jnrsqrod4j.execute-api.us-west-2.amazonaws.com/v1/cambio_api/upload"
EXTRACT_URL="https://jnrsqrod4j.execute-api.us-west-2.amazonaws.com/v1/cambio_api/extract"

uid="null"
jid="null"
s3_key="null"

result=""

upload() {
    local response=$(curl -s -X GET \
        -H "x-api-key: $apiKey" \
        "$UPLOAD_URL?fileName=$file_path")

    local url_info=$(echo "$response" | jq -r '.presignedUrl')
    local tmp_url=$(echo "$url_info" | jq -r '.url')
    local tmp_data=$(echo "$url_info" | jq -r '.fields')
    s3_key=$(echo "$tmp_data" | jq -r '.key')
    jid=$(echo "$response" | jq -r '.jobId')
    uid=$(echo "$response" | jq -r '.userId')

    if [ "$uid" = "null" ] || [ "$uid" == "null" ]; then
        exit 1
    fi
    if [ "$jid" = "null" ] || [ "$jid" == "null" ]; then
        exit 1
    fi
    if [ "$s3_key" = "null" ] || [ "$s3_key" == "null" ]; then
        exit 1
    fi

    local aws_access_key_id=$(echo "$tmp_data" | jq -r '."AWSAccessKeyId"')
    local x_amz_security_token=$(echo "$tmp_data" | jq -r '."x-amz-security-token"')
    local policy=$(echo "$tmp_data" | jq -r '."policy"')
    local signature=$(echo "$tmp_data" | jq -r '."signature"')
    local x_amz_meta_jobid=$(echo "$tmp_data" | jq -r '."x-amz-meta-jobid"')
    local x_amz_meta_userid=$(echo "$tmp_data" | jq -r '."x-amz-meta-userid"')
    local x_amz_meta_filename=$(echo "$tmp_data" | jq -r '."x-amz-meta-filename"')
    local x_amz_meta_jobtype=$(echo "$tmp_data" | jq -r '."x-amz-meta-jobtype"')
    local x_amz_meta_user_prompt=$(echo "$tmp_data" | jq -r '."x-amz-meta-user_prompt"')

    local status=$(curl -s -X POST \
        -F "key=$s3_key" \
        -F "AWSAccessKeyId=$aws_access_key_id" \
        -F "x-amz-security-token=$x_amz_security_token" \
        -F "policy=$policy" \
        -F "signature=$signature" \
        -F "x-amz-meta-jobid=$x_amz_meta_jobid" \
        -F "x-amz-meta-userid=$x_amz_meta_userid" \
        -F "x-amz-meta-filename=$x_amz_meta_filename" \
        -F "x-amz-meta-jobtype=$x_amz_meta_jobtype" \
        -F "x-amz-meta-user_prompt=$x_amz_meta_user_prompt" \
        -F "file=@$file_path" \
        "$tmp_url")
}

extract() {
    local payload='{
        "userId": "'"$uid"'",
        "jobId": "'"$jid"'",
        "fileKey": "'"$s3_key"'"
    }'

    local response=$(curl -s -X POST \
                    -H "x-api-key: $apiKey" \
                    -d "$payload" \
                    "$EXTRACT_URL")

    result=$(echo "$response" | jq -r '.result')
}

