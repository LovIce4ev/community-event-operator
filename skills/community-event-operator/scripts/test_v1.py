import json
import urllib.request

API_KEY = "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd"

# 测试 /api/v1 的各种路径
endpoints = [
    "https://zenmux.ai/api/v1/chat/completions",
    "https://zenmux.ai/api/v1/images/generations", 
    "https://zenmux.ai/api/v1/models",
]

for url in endpoints:
    print(f"\n测试: {url}")
    
    # OpenAI 格式
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Generate an image: minimalist philosopher"}]
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            method="POST"
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"✅ 成功! {resp.read()[:200]}")
            break
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read()[:200]}")
    except Exception as e:
        print(f"❌ {e}")
