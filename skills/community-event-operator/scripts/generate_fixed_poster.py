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

img = Image.new('RGB', (1024, 1448), color = (45, 42, 58))
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype(FONTS["zh"]["title"], 80)
font_sub = ImageFont.truetype(FONTS["zh"]["info"], 36)
font_body = ImageFont.truetype(FONTS["zh"]["info"], 28)
font_big = ImageFont.truetype(FONTS["zh"]["title"], 52)
font_small = ImageFont.truetype(FONTS["zh"]["info"], 26)

white = (255, 255, 255)
gold = (212, 175, 95)
light_gray = (180, 175, 165)

# 顶部线条
draw.rectangle((80, 60, 944, 62), fill=gold)

# 系列标识 - 只用中文，避免混排乱码
draw.text((80, 90), "CMI共学    系列第7场", font=font_small, fill=gold)

# 主标题
draw.text((80, 160), "反启蒙英雄", font=font_title, fill=white)
draw.text((80, 260), "卢梭", font=font_title, fill=gold)

# 副标题
draw.text((80, 380), "个人主义平民社会系列", font=font_sub, fill=light_gray)

# 分隔线
draw.rectangle((80, 460, 320, 462), fill=gold)

# 日期 - 修正为2月22日
draw.text((80, 500), "02.22", font=font_big, fill=white)
draw.text((220, 520), "周日晚上7点", font=font_sub, fill=light_gray)

# 地点 - 不用特殊图标，纯文字
draw.text((80, 590), "地点: 清迈客栈 CMI空间", font=font_body, fill=white)

# 核心信息
info_y = 1120
draw.text((80, info_y), "· 系列第7场，继续深入", font=font_body, fill=light_gray)
draw.text((80, info_y + 45), "· 一起读懂卢梭的反启蒙思想", font=font_body, fill=light_gray)
draw.text((80, info_y + 90), "· 逃离信息茧房", font=font_body, fill=light_gray)

# 人数/费用
draw.text((780, 1240), "限20人", font=font_sub, fill=gold)
draw.text((780, 1290), "免费", font=font_body, fill=white)

# 底部口号
draw.text((350, 1370), "别鸽，周日见！", font=font_sub, fill=gold)

# 底部线条
draw.rectangle((80, 1420, 944, 1422), fill=gold)

# Logo
logo_path = os.path.join(ASSETS_DIR, "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((130, 130))
    img.paste(logo, (870, 80), mask=logo)

output_path = os.path.join(OUTPUTS_DIR, "cmi_study_07_fixed.png")
img.save(output_path)
print(f"Saved: {output_path}")
