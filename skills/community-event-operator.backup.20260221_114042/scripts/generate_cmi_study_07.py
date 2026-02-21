import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "../assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "../outputs")

FONTS = {
    "zh": {
        "title": os.path.join(ASSETS_DIR, "JiangCheng-600W.ttf"),
        "info": os.path.join(ASSETS_DIR, "JiangCheng-300W.ttf")
    }
}

event_data = {
  "title": "CMI共学 #07 | 反启蒙英雄卢梭",
  "subtitle": "个人主义平民社会系列",
  "time": "2025-02-23 19:00",
  "location": "清迈客栈 CMI空间",
  "fee": "免费",
  "limit": "20人",
  "highlights": [
    "系列第7场，继续深入",
    "一起读懂卢梭的反启蒙",
    "逃离信息茧房"
  ]
}

img = Image.new('RGB', (1024, 1448), color = (245, 245, 240))
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype(FONTS["zh"]["title"], 72)
font_sub = ImageFont.truetype(FONTS["zh"]["info"], 36)
font_body = ImageFont.truetype(FONTS["zh"]["info"], 28)
font_bottom = ImageFont.truetype(FONTS["zh"]["title"], 32)
font_big = ImageFont.truetype(FONTS["zh"]["title"], 40)

text_color = (40, 40, 40)
accent_color = (200, 80, 60)

# 顶部标题
title = event_data["title"]
title_bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
title_x = max(50, (1024 - title_w) // 2)
draw.text((title_x, 100), title, font=font_title, fill=text_color)

# 副标题
subtitle = event_data["subtitle"]
sub_bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
sub_w = sub_bbox[2] - sub_bbox[0]
sub_x = max(50, (1024 - sub_w) // 2)
draw.text((sub_x, 200), subtitle, font=font_sub, fill=accent_color)

# 日期和人数右上
date_str = "周日 2月23日"
limit_str = f"限{event_data['limit']}"
draw.text((750, 120), date_str, font=font_sub, fill=text_color)
draw.text((750, 170), limit_str, font=font_body, fill=text_color)

# 左侧竖排文字
side_text = "CMI共学·个人主义系列"
side_img = Image.new('RGBA', (800, 60), (255, 255, 255, 0))
side_draw = ImageDraw.Draw(side_img)
side_draw.text((10, 10), side_text, font=font_sub, fill=accent_color)
side_rotated = side_img.rotate(90, expand=True)
img.paste(side_rotated, (40, 280), mask=side_rotated)

# 核心亮点（左下）
y_info = 1220
for h in event_data["highlights"][:2]:
    draw.text((80, y_info), f"• {h}", font=font_bottom, fill=text_color)
    y_info += 50

# 右下角信息
def right_align_text(draw, x_right, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((x_right - w, y), text, font=font, fill=fill)

info_y = 1180
right_align_text(draw, 960, info_y, f"时间: 周日晚上7点", font_big, text_color)
right_align_text(draw, 960, info_y + 55, f"地点: {event_data['location']}", font_big, text_color)
right_align_text(draw, 960, info_y + 110, f"费用: {event_data['fee']}", font_big, text_color)

# Logo
logo_path = os.path.join(ASSETS_DIR, "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((150, 150))
    img.paste(logo, (50, 50), mask=logo)

output_path = os.path.join(OUTPUTS_DIR, "cmi_study_07_preview.png")
img.save(output_path)
print(f"Saved: {output_path}")
