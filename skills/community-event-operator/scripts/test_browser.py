import json
import urllib.request
import ssl

API_KEY = "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd"
ENDPOINT = "https://zenmux.ai/api/vertex-ai"

request_body = {
    "contents": [{
        "parts": [{"text": "Generate an image: A minimalist philosopher illustration"}]
    }]
}

print("尝试模拟浏览器请求...")

try:
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(request_body).encode("utf-8"),
        method="POST"
    )
    
    # 完整的浏览器请求头
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    req.add_header("Accept", "application/json, text/plain, */*")
    req.add_header("Accept-Language", "en-US,en;q=0.9")
    req.add_header("Accept-Encoding", "gzip, deflate, br")
    req.add_header("Origin", "https://zenmux.ai")
    req.add_header("Referer", "https://zenmux.ai/")
    req.add_header("Connection", "keep-alive")
    
    ctx = ssl.create_default_context()
    
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"✅ 成功!")
        print(json.dumps(result, indent=2)[:1500])
        
except urllib.error.HTTPError as e:
    print(f"❌ HTTP {e.code}")
    print(f"Headers: {dict(e.headers)}")
    print(f"Body: {e.read().decode('utf-8')[:500]}")
except Exception as e:
    print(f"❌ 错误: {e}")
