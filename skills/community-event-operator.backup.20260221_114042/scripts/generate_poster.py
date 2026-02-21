#!/usr/bin/env python3
"""
高级海报生成脚本 (A+B+C 三段式合成架构)
支持：AI 识图写 Prompt -> Nano Banana Pro 生成底图 -> Pillow 精准文字坐标排版
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# 配置区
# ---------------------------------------------------------
# 阶段 A：提取画图 Prompt 的大模型 API 配置 (例如 OpenAI, 豆包, 通义等)
LLM_API_KEY = os.environ.get("LLM_API_KEY", "YOUR_API_KEY")
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")

# 阶段 B：Nano Banana Pro 生图 API 配置
NB_API_KEY = os.environ.get("NANO_BANANA_API_KEY", "YOUR_NB_API_KEY")
NB_ENDPOINT = os.environ.get("NB_ENDPOINT", "https://api.example.com/v1/images/generations")
NB_MODEL = os.environ.get("NB_MODEL", "nano-banana-pro")

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
QR_PATH = os.path.join(ASSETS_DIR, "wechat_qr.png")

BASE_IMAGE_PATH = os.path.join(ASSETS_DIR, "generated_base.png")
FINAL_IMAGE_PATH = os.path.join(OUTPUTS_DIR, "final_poster_with_text.png")
# ---------------------------------------------------------

def stage_a_generate_prompt(event_data):
    """阶段 A: 调用 LLM 根据活动信息(和参考图)写出生图提示词"""
    print("🧠 [阶段 A] 正在调用大模型构思海报画面...")
    
    # 抽取核心信息供生图参考
    title = event_data.get("title", "精彩活动")
    highlights = ", ".join(event_data.get("highlights", []))
    
    system_prompt = """你是一个顶级的海报插画设计师指导。
你的任务是根据用户的活动主题，写出一段纯英文的、用于给 DALL-E 或类似生图模型使用的绘画提示词 (Prompt)。
要求：
1. 只需要描述画面中心的主体元素、氛围、色彩。
2. 明确要求画面必须有大面积纯色留白(Negative Space) 供后续人工打字。
3. 绝对禁止在提示词中要求出现任何英文字母、数字和单词。
4. 结合提供的活动的主题构思合适的意象。
请直接输出一段2-3句话的英文字符串提示词，不要说多余的废话。"""

    user_content = f"活动主题：{title}\n核心亮点：{highlights}\n请为这个活动设计一张干净纯粹、顶部/侧部留白极大的插画风背景图提示词。"

    data = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.7
    }
    
    try:
        req = urllib.request.Request(LLM_ENDPOINT, data=json.dumps(data).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {LLM_API_KEY}")
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            generated_prompt = result["choices"][0]["message"]["content"].strip()
            print(f"✨ 构思完毕 Prompt: \n{generated_prompt}")
            return generated_prompt
    except Exception as e:
        print(f"⚠️ 大模型调用失败 ({e})，使用备用基础 Prompt。")
        return "Clean minimalist flat illustration vector art background, lots of negative space for text, vibrant colors, no text, no letters. Masterpiece."


def stage_b_generate_base_image(prompt):
    """阶段 B: 调用 Nano Banana Pro 生成底图并保存"""
    print("🎨 [阶段 B] 正在呼叫 Nano Banana Pro 绘制底图...")
    data = {
        "model": NB_MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "1024x1448"
    }
    
    try:
        req = urllib.request.Request(NB_ENDPOINT, data=json.dumps(data).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {NB_API_KEY}")
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            image_url = result.get("data", [{}])[0].get("url")
            
            if image_url:
                urllib.request.urlretrieve(image_url, BASE_IMAGE_PATH)
                print(f"🖼️ 底图绘制成功并下载至: {BASE_IMAGE_PATH}")
                return True
    except Exception as e:
        print(f"❌ 生图 API 调用失败: {e}")
        return False


def is_mostly_english(text):
    """简单检测文本是否主要由英文字符构成（基于是否包含汉字）"""
    if not text:
        return True
    
    import re
    if re.search(r'[\u4e00-\u9fff]', text):
        return False
    return True

def stage_c_add_text_overlay(event_data):
    """阶段 C: 使用 Pillow 零 Token 硬核排版 (带多语言双轨字体字典)"""
    print("🖨️ [阶段 C] 开始像素级精准文字排版...")
    
    if not os.path.exists(BASE_IMAGE_PATH):
        print("❌ 找不到生好的底图，无法排版。")
        return
        
    title = event_data.get("title", "Event Name")
    lang_key = "en" if is_mostly_english(title) else "zh"
    font_paths = FONTS[lang_key]
    
    title_font_path = font_paths["title"]
    info_font_path = font_paths["info"]
    
    if not os.path.exists(title_font_path) or not os.path.exists(info_font_path):
        print(f"⚠️ 找不到当前语言({lang_key})专属字体：\n{title_font_path}\n{info_font_path}\n请确保assets中存在对应文件！排版可能中止。")
        return
        
    try:
        img = Image.open(BASE_IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        font_title = ImageFont.truetype(title_font_path, 80)
        font_sub = ImageFont.truetype(info_font_path, 40)
        font_body = ImageFont.truetype(info_font_path, 30)
        
        font_bottom_left = ImageFont.truetype(title_font_path, 32) 
        font_bottom_right = ImageFont.truetype(title_font_path, 40)
        
        text_color = (255, 255, 255, 255)
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 80))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        title = event_data.get("title", "Event Name")
        highlights = event_data.get("highlights", [])
        
        # --- A. 顶部区域：居中跨度大标题 ---
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        title_x = max(50, (1024 - title_w) // 2)
        draw.text((title_x, 80), title, font=font_title, fill=text_color)
        
        # --- F. 原侧边栏文字：现变为主标题正下方的副标题 ---
        side_text = highlights[0] if highlights else ("ENVELOPING COMPOSITION" if lang_key == "en" else "社区专属活动")
        subtitle_bbox = draw.textbbox((0, 0), side_text, font=font_sub)
        subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = max(50, (1024 - subtitle_w) // 2)
        draw.text((subtitle_x, 190), side_text, font=font_sub, fill=text_color)
        
        # --- B. 左下角：两行核心亮点 ---
        y_left_info = 1250  
        for h in highlights[:2]: 
            draw.text((80, y_left_info), f"• {h}", font=font_bottom_left, fill=text_color)
            y_left_info += 50
            
        def right_align_text(draw, x_right, y, text, font, fill):
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            draw.text((x_right - w, y), text, font=font, fill=fill)
            
        # --- C. 上方右侧：日期与限制 ---
        date_str = event_data.get('time', '待定').split(" ")[0]
        limit_str = f"Limit: {event_data.get('limit', 'No limit')}" if lang_key == "en" else f"人数: {event_data.get('limit', '不限')}"
        
        right_align_text(draw, 960, 210, date_str, font_sub, text_color)
        right_align_text(draw, 960, 260, limit_str, font_body, text_color)
        
        # --- E. 右下角细节区 ---
        info_y = 1215
        time_prefix = "Time: " if lang_key == "en" else "时间: "
        loc_prefix = "Location: " if lang_key == "en" else "地点: "
        fee_prefix = "Fee: " if lang_key == "en" else "费用: "
        
        time_str = f"{time_prefix}{event_data.get('time', 'TBD')}"
        loc_str = f"{loc_prefix}{event_data.get('location', 'TBD')}"
        fee_str = f"{fee_prefix}{event_data.get('fee', 'Free')}"
        
        right_align_text(draw, 960, info_y, time_str, font_bottom_right, text_color)
        right_align_text(draw, 960, info_y + 55, loc_str, font_bottom_right, text_color)
        right_align_text(draw, 960, info_y + 110, fee_str, font_bottom_right, text_color)
        
        # 贴 Logo 和二维码
        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo.thumbnail((200, 200))
            img.paste(logo, (50, 50), mask=logo)
            
        if os.path.exists(QR_PATH):
            qr = Image.open(QR_PATH).convert("RGBA")
            qr.thumbnail((200, 200))
            img.paste(qr, (1024 - 250, 1448 - 250), mask=qr)
            
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        img.convert("RGB").save(FINAL_IMAGE_PATH)
        print(f"\n🎉 完美合成！带有文字、Logo和二维码的终极海报已生成: {FINAL_IMAGE_PATH}")
        
    except Exception as e:
        print(f"❌ 排版合成阶段发生错误: {e}")

# ---------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_poster.py <记录了活动核心要素的JSON文件路径>")
        sys.exit(1)
        
    json_path = sys.argv[1]
    
    if not os.path.exists(json_path):
        print(f"❌ 找不到包含活动数据的 JSON 文件: {json_path}")
        sys.exit(1)
        
    with open(json_path, 'r', encoding='utf-8') as f:
        event_data = json.load(f)
        
    print(f"📦 已读取活动数据，开始执行三段式终极海报生成...")
    
    # 执行三步走
    prompt = stage_a_generate_prompt(event_data)
    success = stage_b_generate_base_image(prompt)
    if success:
        stage_c_add_text_overlay(event_data)
