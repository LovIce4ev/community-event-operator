import json
import urllib.request

API_KEY = "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd"
ENDPOINT = "https://zenmux.ai/api/vertex-ai"

# 尝试不同的请求格式
formats = [
    # 格式1: Vertex AI with x-api-key header
    {
        "headers": {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        },
        "data": {
            "contents": [{"parts": [{"text": "Generate an image: A minimalist illustration of a philosopher"}]}]
        }
    },
    # 格式2: OpenAI compatible with api-key header  
    {
        "headers": {
            "Content-Type": "application/json", 
            "api-key": API_KEY
        },
        "data": {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "Generate image: minimalist philosopher illustration"}]
        }
    },
    # 格式3: POST to /v1/images/generations on same domain
    {
        "url": "https://zenmux.ai/v1/images/generations",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        "data": {
            "prompt": "minimalist philosopher illustration",
            "n": 1
        }
    }
]

for i, fmt in enumerate(formats, 1):
    url = fmt.get("url", ENDPOINT)
    print(f"\n尝试格式 {i}: {url}")
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(fmt["data"]).encode("utf-8"),
            method="POST"
        )
        for k, v in fmt["headers"].items():
            req.add_header(k, v)
        
        with urllib.request.urlopen(req) as resp:
            print(f"✅ 成功! {resp.read()[:200]}")
            break
    except Exception as e:
        print(f"❌ {e}")
