import json
import urllib.request
import ssl

API_KEY = "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd"
ENDPOINT = "https://zenmux.ai/api/vertex-ai"

# Google Vertex AI 标准请求格式
request_body = {
    "contents": [{
        "role": "user",
        "parts": [{
            "text": "Generate an image: A minimalist flat illustration of Jean-Jacques Rousseau, warm tones, no text"
        }]
    }],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 2048,
        "candidateCount": 1
    }
}

# 尝试不同的认证方式
auth_methods = [
    ("Bearer Token", {"Authorization": f"Bearer {API_KEY}"}),
    ("X-API-Key", {"x-api-key": API_KEY}),
    ("API-Key", {"api-key": API_KEY}),
    ("X-Google-Api-Key", {"x-goog-api-key": API_KEY}),
]

for name, headers in auth_methods:
    print(f"\n{'='*50}")
    print(f"尝试: {name}")
    print(f"Headers: {headers}")
    
    try:
        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(request_body).encode("utf-8"),
            method="POST"
        )
        
        req.add_header("Content-Type", "application/json")
        for k, v in headers.items():
            req.add_header(k, v)
        
        # 禁用 SSL 验证（测试用）
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"✅ 成功!")
            print(json.dumps(result, indent=2)[:1000])
            break
            
    except urllib.error.HTTPError as e:
        error = e.read().decode('utf-8')
        print(f"❌ HTTP {e.code}: {error[:300]}")
    except Exception as e:
        print(f"❌ 错误: {e}")

print("\n" + "="*50)
