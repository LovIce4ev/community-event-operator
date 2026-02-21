#!/usr/bin/env python3
import os
import json
import urllib.request

# 测试 Nano Banana Pro API
API_KEY = "AIzaSyAzz0qYljbNgo-_IC0oZsE_FXPShQHsIpM"

# 尝试几个可能的 endpoint
ENDPOINTS = [
    "https://api.nano-banana.com/v1/images/generations",
    "https://api.nano-banana.com/v1/generate",
    "https://nano-banana.com/api/v1/generate",
    "https://api.replicate.com/v1/predictions",  # 可能是 replicate 托管
]

prompt = "A minimalist flat illustration of Jean-Jacques Rousseau silhouette, warm amber and sepia tones, soft vintage atmosphere, clean negative space at top and bottom for text, no text in image, artistic style"

print("🔍 测试 Nano Banana Pro API 连接...")
print(f"API Key: {API_KEY[:20]}...")
print()

for endpoint in ENDPOINTS:
    print(f"尝试: {endpoint}")
    try:
        data = {
            "prompt": prompt,
            "n": 1,
            "size": "1024x1448"
        }
        
        req = urllib.request.Request(
            endpoint, 
            data=json.dumps(data).encode("utf-8"), 
            method="POST",
            timeout=30
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"✅ 成功! 响应: {json.dumps(result, indent=2)[:500]}")
            break
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {error_body[:200]}")
    except Exception as e:
        print(f"❌ 错误: {str(e)[:100]}")
    print()

print("测试完成")
