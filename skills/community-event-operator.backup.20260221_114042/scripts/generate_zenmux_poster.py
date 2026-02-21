#!/usr/bin/env python3
"""
高级海报生成脚本 - Zenmux AI 版本
支持：AI 生图 (Zenmux) -> Pillow 文字排版
"""

import os
import sys
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# 配置区 - Zenmux API
# ---------------------------------------------------------
ZENMUX_API_KEY = os.environ.get("ZENMUX_API_KEY", "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd")
ZENMUX_ENDPOINT = os.environ.get("ZENMUX_ENDPOINT", "https://zenmux.ai/api/v1")

# 基础路径配置
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

FONTS = {
    "zh": {
        "title": os.path.join(ASSETS_DIR, "JiangCheng-600W.ttf"),
        "info": os.path.join(ASSETS_DIR, "JiangCheng-300W.ttf")
    },
    "en": {
        "title": os.path.join(ASSETS_DIR, "Delight-Bold.ttf"),
        "info": os.path.join(ASSETS_DIR, "Delight-Regular.ttf")
    }
}

LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
BASE_IMAGE_PATH = os.path.join(ASSETS_DIR, "generated_base.png")
FINAL_IMAGE_PATH = os.path.join(OUTPUTS_DIR, "final_poster_with_text.png")
# ---------------------------------------------------------

def generate_image_with_zenmux(prompt, output_path):
    """使用 Zenmux API 生成图片"""
    print(f"🎨 正在调用 Zenmux AI 生成底图...")
    print(f"Prompt: {prompt[:80]}...")
    
    # Zenmux 使用 OpenAI 兼容格式，尝试 /v1/images/generations
    data = {
        "model": "dall-e-3",  # 或其他模型
        "prompt": prompt,
        "n": 1,
        "size": "1024x1792"  # 竖版比例
    }
    
    # 尝试不同端点
    endpoints = [
        "https://zenmux.ai/api/vertex-ai",  # 用户提供的端点
        f"{ZENMUX_ENDPOINT}/images/generations",
        f"{ZENMUX_ENDPOINT}/chat/completions",
    ]
    
    for endpoint in endpoints:
        print(f"尝试端点: {endpoint}")
        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(data).encode("utf-8"),
                method="POST"
            )
            req.add_header("Content-Type", "application/json")
            req.add_header("Authorization", f"Bearer {ZENMUX_API_KEY}")
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                print(f"✅ 成功! 响应: {json.dumps(result, indent=2)[:300]}")
                return True
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP {e.code}: {error_body[:200]}")
        except Exception as e:
            print(f"❌ 错误: {str(e)[:100]}")
    
    return False


def add_text_overlay(event_data, base_image_path, output_path):
    """在底图上添加文字"""
    print("🖨️ 开始文字排版...")
    
    if not os.path.exists(base_image_path):
        print("❌ 找不到底图")
        return False
        
    try:
        img = Image.open(base_image_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        # 字体设置
        font_title = ImageFont.truetype(FONTS["zh"]["title"], 72)
        font_sub = ImageFont.truetype(FONTS["zh"]["info"], 36)
        font_body = ImageFont.truetype(FONTS["zh"]["info"], 28)
        font_big = ImageFont.truetype(FONTS["zh"]["title"], 42)
        
        # 文字颜色（根据背景调整）
        text_color = (255, 255, 255, 255)  # 白色
        gold = (212, 175, 95, 255)
        
        # 获取活动信息
        title = event_data.get("title", "CMI活动")
        highlights = event_data.get("highlights", [])
        
        # 添加暗色遮罩让文字更清晰
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 100))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 标题居中
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        title_x = max(50, (1024 - title_w) // 2)
        draw.text((title_x, 80), title, font=font_title, fill=text_color)
        
        # 副标题
        if highlights:
            sub = highlights[0][:20]
            draw.text((80, 180), sub, font=font_sub, fill=gold)
        
        # 日期和地点
        date_str = event_data.get('time', '').split()[0] if ' ' in event_data.get('time', '') else event_data.get('time', '')
        draw.text((750, 120), date_str, font=font_sub, fill=text_color)
        draw.text((750, 170), event_data.get('location', ''), font=font_body, fill=text_color)
        
        # 底部信息
        info_y = 1200
        for i, h in enumerate(highlights[:2]):
            draw.text((80, info_y + i*50), f"• {h[:25]}", font=font_body, fill=text_color)
        
        # 费用和人数
        draw.text((800, 1240), f"限{event_data.get('limit', '20')}人", font=font_sub, fill=gold)
        draw.text((800, 1290), event_data.get('fee', '免费'), font=font_body, fill=text_color)
        
        # 添加 Logo
        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo.thumbnail((150, 150))
            img.paste(logo, (50, 50), mask=logo)
        
        # 保存
        img.convert("RGB").save(output_path)
        print(f"✅ 海报合成完成: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 排版错误: {e}")
        return False


# ---------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_zenmux_poster.py <活动JSON文件>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    with open(json_path, 'r', encoding='utf-8') as f:
        event_data = json.load(f)
    
    print(f"📦 开始为「{event_data.get('title')}」生成海报...")
    print()
    
    # 生成 Prompt
    prompt = f"A minimalist flat illustration for {event_data.get('title')}, {', '.join(event_data.get('highlights', [])[:2])}, warm tones, clean negative space at top and bottom, no text, artistic style"
    
    # 阶段 1: 生成底图
    success = generate_image_with_zenmux(prompt, BASE_IMAGE_PATH)
    
    if success:
        # 阶段 2: 添加文字
        add_text_overlay(event_data, BASE_IMAGE_PATH, FINAL_IMAGE_PATH)
        print(f"\n🎉 完成！海报保存在: {FINAL_IMAGE_PATH}")
    else:
        print("\n❌ 底图生成失败")
