import requests
import json

GOOGLE_API_KEY = "AIzaSyByPHoEpVjgzo4vl-S5_qz5Mo8q3OwnFUA"

url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={GOOGLE_API_KEY}"

headers = {
    'Content-Type': 'application/json'
}

data = {
    "instances": [
        {"prompt": "A beautiful sunset over the mountains"}
    ],
    "parameters": {
        "sampleCount": 1
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
