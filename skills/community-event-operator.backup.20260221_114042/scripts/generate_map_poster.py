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

# 创建地图海报
img = Image.new('RGB', (1024, 1448), color = (250, 248, 245))
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype(FONTS["zh"]["title"], 68)
font_sub = ImageFont.truetype(FONTS["zh"]["info"], 32)
font_body = ImageFont.truetype(FONTS["zh"]["info"], 26)
font_big = ImageFont.truetype(FONTS["zh"]["title"], 36)
font_small = ImageFont.truetype(FONTS["zh"]["info"], 22)

text_color = (50, 50, 50)
accent_color = (180, 70, 50)
map_bg = (230, 228, 220)

# 标题区域
draw.text((80, 60), "CMI共学 #07", font=font_title, fill=text_color)
draw.text((80, 140), "反启蒙英雄卢梭", font=font_sub, fill=accent_color)
draw.text((600, 80), "周日 2/23 晚7点", font=font_sub, fill=text_color)

# 地图区域（模拟地图框）
map_box = (80, 220, 944, 700)
draw.rectangle(map_box, fill=map_bg, outline=accent_color, width=2)

# 地图标题
draw.text((450, 240), "活 动 地 点", font=font_sub, fill=text_color)

# 绘制简化的地图示意
# 主路
draw.rectangle((200, 350, 824, 380), fill=(200, 195, 185))
draw.text((480, 355), "主路", font=font_small, fill=(120, 115, 105))

# 小巷
draw.rectangle((450, 300, 470, 550), fill=(210, 205, 195))
draw.text((400, 420), "巷", font=font_small, fill=(120, 115, 105))

# 地标点
draw.ellipse((420, 380, 500, 460), fill=accent_color)
draw.text((435, 405), "CMI", font=font_small, fill=(255, 255, 255))

# 周边地标
draw.text((250, 320), "🏛️ 寺庙", font=font_body, fill=text_color)
draw.text((700, 400), "☕ 咖啡店", font=font_body, fill=text_color)
draw.text((300, 520), "🍜 餐厅", font=font_body, fill=text_color)
draw.text((650, 300), "🛒 7-11", font=font_body, fill=text_color)

# 地址信息框
info_y = 750
draw.text((80, info_y), "📍 清迈客栈 CMI空间", font=font_big, fill=accent_color)
draw.text((80, info_y + 50), "具体地址：清迈古城内 [详细地址]", font=font_body, fill=text_color)

# 交通指引
transport_y = 860
draw.text((80, transport_y), "🚗 交通指引", font=font_sub, fill=text_color)
draw.text((80, transport_y + 45), "• 双条车：告诉司机去「清迈客栈」或古城内", font=font_body, fill=text_color)
draw.text((80, transport_y + 80), "• 摩托车/自行车：古城内可停车", font=font_body, fill=text_color)
draw.text((80, transport_y + 115), "• 步行：从塔佩门步行约15分钟", font=font_body, fill=text_color)

# 联系信息
draw.text((80, 1050), "📞 联系：Andreas [手机号]", font=font_body, fill=text_color)
draw.text((80, 1090), "💬 进群了解更多详情", font=font_body, fill=text_color)

# 底部二维码区域
draw.rectangle((700, 1000, 944, 1200), fill=(240, 240, 240), outline=(200, 200, 200))
draw.text((740, 1080), "扫码报名", font=font_body, fill=text_color)

# Logo
logo_path = os.path.join(ASSETS_DIR, "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((120, 120))
    img.paste(logo, (850, 60), mask=logo)

# 底部强调
draw.text((350, 1280), "限20人 · 免费参与", font=font_sub, fill=accent_color)
draw.text((300, 1330), "别鸽，周日晚上7点见！", font=font_big, fill=text_color)

output_path = os.path.join(OUTPUTS_DIR, "cmi_study_07_map.png")
img.save(output_path)
print(f"Saved map poster: {output_path}")
