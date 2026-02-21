#!/usr/bin/env python3
"""
极简海报生成器 - Minimal Poster Generator
生成纯黑背景 + 极窄边框的活动海报
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os
import sys
from pathlib import Path

def get_font(size):
    """获取支持中文的字体"""
    font_paths = [
        # 中文字体
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        # Windows
        "/Windows/Fonts/simhei.ttf",
        "/Windows/Fonts/simsun.ttc",
        "/Windows/Fonts/msyh.ttc",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    return ImageFont.load_default()

def generate_poster(event_data, output_dir="./output", include_qr=True):
    """
    生成极简风格活动海报
    """
    
    # 创建画布 1080x1920 (9:16 竖版)
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), color='#000000')
    draw = ImageDraw.Draw(img)
    
    # 极窄边框 (2px 白色)
    border_color = '#FFFFFF'
    border_width = 2
    margin = 60
    draw.rectangle(
        [margin, margin, width-margin, height-margin],
        outline=border_color,
        width=border_width
    )
    
    # 加载字体
    font_title = get_font(80)
    font_subtitle = get_font(50)
    font_info = get_font(40)
    font_desc = get_font(32)
    
    # 颜色
    text_color = '#FFFFFF'
    accent_color = '#FF6B6B'
    gray_color = '#AAAAAA'
    
    # 获取活动信息
    title = event_data.get('title', '活动')
    subtitle = event_data.get('subtitle', '')
    datetime = event_data.get('datetime', '')
    location = event_data.get('location', '')
    price = event_data.get('price', '')
    description = event_data.get('description', '')
    
    # 绘制标题
    y_pos = 250
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    x_pos = (width - title_width) // 2
    draw.text((x_pos, y_pos), title, font=font_title, fill=text_color)
    
    # 副标题
    if subtitle:
        y_pos += 120
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        x_pos = (width - subtitle_width) // 2
        draw.text((x_pos, y_pos), subtitle, font=font_subtitle, fill=gray_color)
    
    # 分隔线
    y_pos += 120
    draw.line([(150, y_pos), (width-150, y_pos)], fill='#333333', width=1)
    
    # 时间地点
    y_pos += 80
    info_lines = []
    if datetime:
        info_lines.append(f"📅 {datetime}")
    if location:
        info_lines.append(f"📍 {location}")
    
    for line in info_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_info)
        line_width = line_bbox[2] - line_bbox[0]
        x_pos = (width - line_width) // 2
        draw.text((x_pos, y_pos), line, font=font_info, fill=text_color)
        y_pos += 70
    
    # 价格
    if price:
        y_pos += 30
        price_text = f"💰 {price}"
        price_bbox = draw.textbbox((0, 0), price_text, font=font_info)
        price_width = price_bbox[2] - price_bbox[0]
        x_pos = (width - price_width) // 2
        draw.text((x_pos, y_pos), price_text, font=font_info, fill=accent_color)
    
    # 描述文字
    if description:
        y_pos += 100
        # 文本换行处理
        max_width = width - 200
        words = description
        lines = []
        current_line = ""
        
        for char in words:
            test_line = current_line + char
            try:
                test_bbox = draw.textbbox((0, 0), test_line, font=font_desc)
                if test_bbox[2] - test_bbox[0] > max_width and current_line:
                    lines.append(current_line)
                    current_line = char
                else:
                    current_line = test_line
            except:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        
        for line in lines[:5]:  # 最多5行
            try:
                line_bbox = draw.textbbox((0, 0), line, font=font_desc)
                line_width = line_bbox[2] - line_bbox[0]
                x_pos = (width - line_width) // 2
                draw.text((x_pos, y_pos), line, font=font_desc, fill='#CCCCCC')
            except:
                draw.text((100, y_pos), line, font=font_desc, fill='#CCCCCC')
            y_pos += 55
    
    # 底部装饰线
    y_pos = height - 280
    draw.line([(150, y_pos), (width-150, y_pos)], fill='#333333', width=1)
    
    # 底部信息
    y_pos += 50
    footer_lines = ["清迈客栈 | CMI社区", "扫码报名 · 现场参加"]
    for line in footer_lines:
        try:
            line_bbox = draw.textbbox((0, 0), line, font=font_desc)
            line_width = line_bbox[2] - line_bbox[0]
            x_pos = (width - line_width) // 2
            draw.text((x_pos, y_pos), line, font=font_desc, fill='#888888')
        except:
            draw.text((100, y_pos), line, font=font_desc, fill='#888888')
        y_pos += 50
    
    # 二维码占位符
    if include_qr:
        qr_size = 180
        qr_x = width - qr_size - 100
        qr_y = height - qr_size - 80
        draw.rectangle(
            [qr_x, qr_y, qr_x + qr_size, qr_y + qr_size],
            outline=text_color,
            width=2
        )
        qr_text = "扫码"
        try:
            qr_text_bbox = draw.textbbox((0, 0), qr_text, font=font_desc)
            qr_text_width = qr_text_bbox[2] - qr_text_bbox[0]
            draw.text((qr_x + (qr_size-qr_text_width)//2, qr_y + qr_size//2 - 15), 
                     qr_text, font=font_desc, fill=text_color)
        except:
            draw.text((qr_x + 60, qr_y + qr_size//2 - 15), qr_text, font=font_desc, fill=text_color)
    
    # 保存
    os.makedirs(output_dir, exist_ok=True)
    suffix = "_full" if include_qr else "_sns"
    output_path = os.path.join(output_dir, f"poster{suffix}.png")
    img.save(output_path, 'PNG')
    print(f"✅ 海报已生成: {output_path}")
    
    return output_path


if __name__ == "__main__":
    event_json = {
        "title": "清迈客栈即兴戏剧活动",
        "subtitle": "在即兴的世界里，遇见有趣的灵魂",
        "datetime": "2025年2月28日（周五）19:00-21:00",
        "location": "清迈客栈 1F",
        "price": "200 铢",
        "description": "在即兴的世界里，最好的台词从来不是'想'出来的，而是从搭档的眼神、呼吸和动作里'读'出来的。加入我们，一起探索即兴表演的乐趣！"
    }
    
    output_dir = "/data/openclaw-workspace/output"
    
    generate_poster(event_json, output_dir, include_qr=True)
    generate_poster(event_json, output_dir, include_qr=False)
    
    print("\n🎉 两张海报都已生成！")
    print(f"📁 查看目录: {output_dir}")