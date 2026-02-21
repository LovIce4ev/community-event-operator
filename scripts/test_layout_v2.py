import os, json
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "../assets")

FONTS = {
    "zh": {
        "title": os.path.join(ASSETS_DIR, "主标题字体（江城黑体600W）.ttf"),
        "info": os.path.join(ASSETS_DIR, "副标题及信息字体（江城黑体300W）.ttf")
    },
    "en": {
        "title": os.path.join(ASSETS_DIR, "英文主标题字体（Delight-Bold）.ttf"),
        "info": os.path.join(ASSETS_DIR, "英文副标题及信息字体（Delight-Regular）.ttf")
    }
}

img = Image.new('RGB', (1024, 1448), color = (200, 200, 200))
draw = ImageDraw.Draw(img)

# Data for Chinese test
event_data = {
  "title": "金秋徒步露营派对",
  "time": "2023-10-24 14:00",
  "location": "京郊野鸭湖湿地国家公园",
  "fee": "199元/人",
  "limit": "50人",
  "highlights": ["结伴同行认识有趣的新朋友", "逃离城市呼吸自然", "专业领队带队安全无忧"]
}

lang_key = "zh"
font_title = ImageFont.truetype(FONTS[lang_key]["title"], 80)
font_sub = ImageFont.truetype(FONTS[lang_key]["info"], 40)
font_body = ImageFont.truetype(FONTS[lang_key]["info"], 30)
text_color = (0, 0, 0)

title = event_data["title"]
highlights = event_data["highlights"]

# --- A. 顶部区域 ---
title_bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
title_x = max(50, (1024 - title_w) // 2)
draw.text((title_x, 80), title, font=font_title, fill=text_color)

# --- F. 左侧侧边栏 (Moved to Top Left) ---
side_text = highlights[0][:15] if highlights else "社区专属活动"
side_img_w = 800
side_img_h = 100
txt_img = Image.new('RGBA', (side_img_w, side_img_h), (255, 255, 255, 0))
txt_draw = ImageDraw.Draw(txt_img)
sb_bbox = txt_draw.textbbox((0, 0), side_text, font=font_sub)
sb_w = sb_bbox[2] - sb_bbox[0]
sb_x = (side_img_w - sb_w) // 2
txt_draw.text((sb_x, 10), side_text, font=font_sub, fill=text_color)
txt_rotated = txt_img.rotate(90, expand=True)
paste_y = 230 # Start at Y=230
img.paste(txt_rotated, (40, paste_y), mask=txt_rotated)

# --- B. 上方左侧：两行核心亮点 (Moved to Bottom Left, replacing Bottom Title) ---
y_left_info = 1270
for h in highlights[:2]: 
    draw.text((100, y_left_info), f"• {h}", font=font_body, fill=text_color)
    y_left_info += 45
    
# --- C. 上方右侧：日期与限制 (Right Aligned) ---
date_str = event_data.get('time', '待定').split(" ")[0]
limit_str = f"人数: {event_data.get('limit', '不限')}"

def right_align_text(draw, x_right, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((x_right - w, y), text, font=font, fill=fill)

right_align_text(draw, 960, 210, date_str, font_sub, text_color)
right_align_text(draw, 960, 260, limit_str, font_body, text_color)

# --- E. 右下角细节区 (Right Aligned) ---
info_y = 1270
time_str = f"时间: {event_data.get('time', 'TBD')}"
loc_str = f"地点: {event_data.get('location', 'TBD')}"
fee_str = f"费用: {event_data.get('fee', 'Free')}"

right_align_text(draw, 960, info_y, time_str, font_body, text_color)
right_align_text(draw, 960, info_y + 40, loc_str, font_body, text_color)
right_align_text(draw, 960, info_y + 80, fee_str, font_body, text_color)

# --- D. 底部横向跨度 ---
# Removed per user markings!

img.save(os.path.join(BASE_DIR, "../outputs/preview_layout_v2.png"))
print("Saved preview_layout_v2.png")
