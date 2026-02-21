#!/usr/bin/env python3
"""
Zenmux 海报生成脚本 - Google Vertex AI 格式
"""

import os
import sys
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# Zenmux / Google Vertex AI 配置
API_KEY = "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd"
ENDPOINT = "https://zenmux.ai/api/vertex-ai"

# 路径配置
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

FONTS = {
    "zh": {
        "title": os.path.join(ASSETS_DIR, "JiangCheng-600W.ttf"),
        "info": os.path.join(ASSETS_DIR, "JiangCheng-300W.ttf")
    }
}

LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
BASE_IMAGE_PATH = os.path.join(ASSETS_DIR, "generated_base.png")
FINAL_IMAGE_PATH = os.path.join(OUTPUTS_DIR, "cmi_poster_ai.png")


def generate_image(prompt):
    """使用 Zenmux (Google Vertex AI 格式) 生成图片"""
    print("🎨 调用 Zenmux AI 生成底图...")
    print(f"Prompt: {prompt[:60]}...")
    
    # Google Vertex AI 格式
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "temperature": 0.7
        }
    }
    
    try:
        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(data).encode("utf-8"),
            method="POST"
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"✅ 成功! 响应预览: {json.dumps(result, indent=2)[:500]}")
            return True
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


if __name__ == "__main__":
    prompt = "A minimalist flat illustration of Jean-Jacques Rousseau silhouette, warm amber and sepia tones, vintage atmosphere, clean negative space, no text"
    generate_image(prompt)
