#!/usr/bin/env python3
"""
自动打包交发件脚本 - 用于将零散的文案和生成的图片汇聚归档
"""

import os
import sys
import shutil
import re
from datetime import datetime

def safe_filename(name):
    # 去除不能用于文件名的特殊字符
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def package_assets(event_title, copy_text):
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    outputs_dir = os.path.abspath(os.path.join(base_dir, "outputs"))
    
    # 构建当前活动的归档文件夹名 (加个今天月日作为前缀)
    date_prefix = datetime.now().strftime("%m%d")
    folder_name = safe_filename(f"{date_prefix}-{event_title}")
    target_dir = os.path.join(outputs_dir, folder_name)
    
    # 创建目标文件夹
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. 写入文案到文本文件
    copy_path = os.path.join(target_dir, "宣传文案.txt")
    with open(copy_path, "w", encoding="utf-8") as f:
        f.write(copy_text)
        
    print(f"✅ 文案已打包至: {copy_path}")
    
    # 2. 检查并复制生成的图片
    generated_poster = os.path.join(base_dir, "assets", "generated_poster.png")
    if os.path.exists(generated_poster):
        poster_target = os.path.join(target_dir, "活动海报底图.png")
        shutil.copy2(generated_poster, poster_target)
        print(f"✅ 海报底图已打包至: {poster_target}")
    
    # 3. 顺便发一份常用 logo 给用户方便排版
    logo_file = os.path.join(base_dir, "assets", "logo.png")
    qr_file = os.path.join(base_dir, "assets", "wechat_qr.png")
    
    if os.path.exists(logo_file):
        shutil.copy2(logo_file, os.path.join(target_dir, "品牌Logo.png"))
    if os.path.exists(qr_file):
        shutil.copy2(qr_file, os.path.join(target_dir, "引流二维码.png"))
        
    print("\n📦 全部打包完成！")
    print(f"📁 归档文件夹路径: {target_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python package_assets.py \"活动标题\" \"完整文案长字符串\"")
        sys.exit(1)
        
    title = sys.argv[1]
    text = sys.argv[2]
    
    package_assets(title, text)
