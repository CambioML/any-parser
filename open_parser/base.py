import json

import requests

CAMBIO_UPLOAD_URL = (
    "https://qreije6m7l.execute-api.us-west-2.amazonaws.com/v1/cambio_api/upload"
)
CAMBIO_EXTRACT_URL = (
    "https://qreije6m7l.execute-api.us-west-2.amazonaws.com/v1/cambio_api/extract"
)
CAMBIO_PARSE_URL = (
    "https://qreije6m7l.execute-api.us-west-2.amazonaws.com/v1/cambio_api/parse"
)


class OpenParser:
    def __init__(self, apiKey) -> None:
        self._uploadurl = CAMBIO_UPLOAD_URL
        self._extracturl = CAMBIO_EXTRACT_URL
        self._parseurl = CAMBIO_PARSE_URL
        self._request_header = {"x-api-key": apiKey}

    def setAPIKey(self, apiKey):
        self._request_header = {"x-api-key": apiKey}

    def extract(self, file_path):
        user_id, job_id, s3_key = self._request_and_upload_by_apiKey(file_path)
        result = self._request_file_extraction(user_id, job_id, s3_key)
        return json.loads(result)["result"]

    def parse(self, file_path, prompt, mode="advanced"):
        user_id, job_id, s3_key = self._request_and_upload_by_apiKey(file_path)
        result = self._request_info_extraction(user_id, job_id, s3_key, mode, prompt)
        return json.loads(result)["result"]

    def _error_handler(self, response):
        if response.status_code == 403:
            raise Exception("Invalid API Key")
        elif response.status_code == 429:
            raise Exception("API Key limit exceeded")
        else:
            raise Exception(f"Error: {response.status_code} {response.text}")

    def _request_and_upload_by_apiKey(self, file_path):
        params = {"fileName": file_path}
        response = requests.get(
            self._uploadurl, headers=self._request_header, params=params
        )

        if response.status_code == 200:
            url_info = response.json()["presignedUrl"]
            uid = response.json()["userId"]
            jid = response.json()["jobId"]
            with open(file_path, "rb") as file_to_upload:
                files = {"file": (file_path, file_to_upload)}
                upload_response = requests.post(
                    url_info["url"], data=url_info["fields"], files=files
                )
            print(f"Upload response: {upload_response.status_code}")
            return uid, jid, url_info["fields"]["key"]

        self._error_handler(response)

    def _request_file_extraction(self, user_id, job_id, s3_key):
        payload = {
            "userId": user_id,
            "jobId": job_id,
            "fileKey": s3_key,
        }
        response = requests.post(
            self._extracturl, headers=self._request_header, json=payload
        )

        if response.status_code == 200:
            print("Extraction success.")
            return response.text

        self._error_handler(response)

    def _request_info_extraction(self, user_id, job_id, s3_key, mode, prompt=""):
        if mode not in ["advanced", "basic"]:
            raise ValueError("Invalid mode. Choose either 'advanced' or 'basic'.")
        payload = {
            "userId": user_id,
            "jobId": job_id,
            "fileKey": s3_key,
            "user_prompt": prompt,
            "use_textract": "True" if mode == "advanced" else "False",
        }
        response = requests.post(
            self._parseurl, headers=self._request_header, json=payload
        )

        if response.status_code == 200:
            print("Extraction success.")
            return response.text

        self._error_handler(response)
