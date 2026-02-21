#!/usr/bin/env python3
"""
CMI共学海报生成脚本 - 参考图风格版
严格按照 reference_poster.webp 的排版布局
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai.types import HttpOptions

# Zenmux 配置
ZENMUX_API_KEY = "sk-ai-v1-70d6bc6a5281bff6802214468c45a6325a9a3a93c4f33c34063e9bfc59a170dd"
ZENMUX_ENDPOINT = "https://zenmux.ai/api/vertex-ai"

client = genai.Client(
    api_key=ZENMUX_API_KEY,
    vertexai=True,
    http_options=HttpOptions(base_url=ZENMUX_ENDPOINT, api_version="v1")
)

# 路径配置
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
REFERENCE_PATH = os.path.join(ASSETS_DIR, "reference_poster.webp")

FONTS = {
    "zh": {
        "big": os.path.join(ASSETS_DIR, "JiangCheng-600W.ttf"),
        "info": os.path.join(ASSETS_DIR, "JiangCheng-300W.ttf")
    }
}

LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
OUTPUT_PATH = os.path.join(OUTPUTS_DIR, "cmi_study_poster.png")

def generate_base_image(event_title, theme):
    """生成底图 - 参考图风格"""
    print("🎨 生成AI底图...")
    
    prompt = f"""A classical Greek marble statue in dramatic lighting against pure black background, 
    {theme}, academic and philosophical atmosphere, 
    clean composition with the statue centered, high contrast, museum quality photography,
    no text, no letters, masterpiece"""
    
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt
        )
        
        # 保存生成的图片
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    with open(os.path.join(ASSETS_DIR, "generated_base.png"), "wb") as f:
                        f.write(image_data)
                    print("✅ 底图生成成功")
                    return True
        return False
    except Exception as e:
        print(f"⚠️ 生成失败: {e}")
        return False

def create_poster(event_data):
    """创建海报 - 严格参考图排版"""
    print("🖨️ 开始排版...")
    
    # 创建黑色背景
    img = Image.new('RGB', (1024, 1448), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 字体
    font_big = ImageFont.truetype(FONTS["zh"]["big"], 120)  # 左侧大标题
    font_title = ImageFont.truetype(FONTS["zh"]["big"], 80)  # 右上角标题
    font_sub = ImageFont.truetype(FONTS["zh"]["info"], 36)  # 副标题
    font_side = ImageFont.truetype(FONTS["zh"]["info"], 28)  # 侧边竖排
    font_info = ImageFont.truetype(FONTS["zh"]["info"], 32)  # 右下角信息
    
    white = (255, 255, 255)
    gold = (255, 200, 100)
    
    # 1. 左侧竖排大标题 (从上到下：个人主义与平民社会)
    left_title = event_data.get("series", "个人主义与平民社会")
    y_pos = 80
    for char in left_title:
        draw.text((50, y_pos), char, font=font_big, fill=white)
        y_pos += 130
    
    # 2. 右上角 CMI共学会 + 编号
    session_num = event_data.get("session", "07")
    draw.text((400, 60), f"CMI共学会{session_num}", font=font_title, fill=white)
    
    # 3. 右上角副标题 (反启蒙英雄)
    subtitle = event_data.get("subtitle", "反启蒙英雄")
    hero = event_data.get("hero", "卢梭")
    draw.text((650, 160), f"{subtitle}", font=font_sub, fill=white)
    draw.text((850, 220), f"{hero}", font=font_title, fill=white)
    
    # 4. 中间贴底图（如果有）
    base_path = os.path.join(ASSETS_DIR, "generated_base.png")
    if os.path.exists(base_path):
        base_img = Image.open(base_path).convert("RGBA")
        # 缩放并居中
        base_img.thumbnail((700, 1000))
        x_offset = (1024 - base_img.width) // 2
        y_offset = 300
        img.paste(base_img, (x_offset, y_offset), mask=base_img)
    
    # 5. 右侧竖排 (线上线下同步参与)
    side_text = event_data.get("side_text", "线上线下同步参与")
    y_side = 400
    for char in side_text:
        draw.text((950, y_side), char, font=font_side, fill=white)
        y_side += 40
    
    # 6. 右下角信息块
    info_x = 550
    info_y = 1050
    
    # 日期时间
    time_str = event_data.get("time_display", "2月22日晚七点")
    draw.text((info_x, info_y), time_str, font=font_info, fill=white)
    
    # 亮点列表（固定4句）
    highlights = event_data.get("highlights", [
        "最硬核的内容",
        "最温情的讨论", 
        "每周日晚七点",
        "你的精神港湾"
    ])
    
    y_info = info_y + 60
    for h in highlights[:4]:
        draw.text((info_x, y_info), h, font=font_info, fill=white)
        y_info += 50
    
    # 7. 右下角 Logo
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo.thumbnail((120, 120))
        img.paste(logo, (880, 1280), mask=logo)
    
    # 保存
    img.save(OUTPUT_PATH)
    print(f"✅ 海报已保存: {OUTPUT_PATH}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_study_poster.py <活动JSON文件>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        event_data = json.load(f)
    
    print(f"📦 生成 CMI共学海报: {event_data.get('title')}")
    
    # 生成底图
    theme = event_data.get("theme", "philosophical contemplation")
    generate_base_image(event_data.get('title'), theme)
    
    # 创建海报
    create_poster(event_data)
    
    print("\n🎉 完成！")
