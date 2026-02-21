import os
import requests
import json

GOOGLE_API_KEY = "AIzaSyByPHoEpVjgzo4vl-S5_qz5Mo8q3OwnFUA"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GOOGLE_API_KEY}"

headers = {
    'Content-Type': 'application/json'
}

data = {
    "contents": [{
        "parts": [{"text": "Hello world"}]
    }]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
