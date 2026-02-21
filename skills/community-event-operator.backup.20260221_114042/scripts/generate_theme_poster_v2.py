import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "../assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "../outputs")

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

# 创建主题海报 - 修正版
img = Image.new('RGB', (1024, 1448), color = (45, 42, 58))
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype(FONTS["zh"]["title"], 80)
font_sub = ImageFont.truetype(FONTS["zh"]["info"], 36)
font_body = ImageFont.truetype(FONTS["zh"]["info"], 28)
font_big = ImageFont.truetype(FONTS["zh"]["title"], 48)
font_en = ImageFont.truetype(FONTS["en"]["info"], 24)
font_series = ImageFont.truetype(FONTS["zh"]["info"], 32)

white = (255, 255, 255)
gold = (212, 175, 95)
light_gray = (200, 195, 185)

# 顶部金色线条
draw.rectangle((80, 60, 944, 62), fill=gold)

# 系列标识 - 用英文避免乱码
series_text = "CMI CO-LEARNING · SESSION 07"
draw.text((80, 90), series_text, font=font_en, fill=gold)

# 主标题 - 分开显示避免拥挤
draw.text((80, 160), "反启蒙英雄", font=font_title, fill=white)
draw.text((80, 260), "卢梭", font=font_title, fill=gold)

# 副标题/主题
draw.text((80, 380), "个人主义平民社会系列", font=font_sub, fill=light_gray)

# 装饰分隔线
draw.rectangle((80, 460, 350, 462), fill=gold)

# 日期 - 修正为2月22日
draw.text((80, 500), "02.22", font=font_big, fill=white)
draw.text((240, 520), "周日晚上7点", font=font_sub, fill=light_gray)

# 地点
draw.text((80, 590), "清迈客栈 CMI空间", font=font_body, fill=white)

# 核心信息（底部区域）
info_y = 1120
draw.text((80, info_y), "· 系列第7场，继续深入", font=font_body, fill=light_gray)
draw.text((80, info_y + 45), "· 一起读懂卢梭的反启蒙思想", font=font_body, fill=light_gray)
draw.text((80, info_y + 90), "· 逃离信息茧房", font=font_body, fill=light_gray)

# 人数/费用（右下角）
draw.text((750, 1240), "限20人", font=font_sub, fill=gold)
draw.text((750, 1290), "免费参与", font=font_body, fill=white)

# 底部口号
draw.text((350, 1370), "别鸽，周日见！", font=font_sub, fill=gold)

# 底部装饰线
draw.rectangle((80, 1420, 944, 1422), fill=gold)

# Logo
logo_path = os.path.join(ASSETS_DIR, "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((140, 140))
    img.paste(logo, (860, 80), mask=logo)

output_path = os.path.join(OUTPUTS_DIR, "cmi_study_07_theme_v2.png")
img.save(output_path)
print(f"Saved: {output_path}")
