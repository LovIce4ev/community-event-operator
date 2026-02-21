#!/usr/bin/env python3
"""
推送至飞书的脚本 - 用于将打包完成的文案推送到用户的飞书群或单人聊天
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

# ---------------------------------------------------------
# 配置区
# ---------------------------------------------------------
# 请在此处填入您的飞书群自定义机器人的 Webhook URL
# 获取方式：在飞书群设置 -> 群机器人 -> 添加自定义机器人 -> 复制 webhook 地址
FEISHU_WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL", "YOUR_FEISHU_WEBHOOK_HERE")
# ---------------------------------------------------------

def send_to_feishu(event_title: str, copy_text: str):
    if FEISHU_WEBHOOK_URL == "YOUR_FEISHU_WEBHOOK_HERE":
        print("⚠️ 警告：检测到飞书 Webhook 尚未配置。")
        print("请在 scripts/send_to_feishu.py 文件中，或者通过环境变量 FEISHU_WEBHOOK_URL 设置地址。")
        print("跳过飞书推送...")
        return

    print(f"🚀 正在将活动【{event_title}】的文案推送到飞书...")
    
    # 构造飞书支持的富文本消息(富文本卡片格式体验更好，这里先用最简单的 text)
    # 也可以使用 post 富文本，方便分渠道显示。
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content_text = f"📢 新活动物料已生成完毕！\n【{event_title}】\n"
    content_text += f"打包时间: {current_time}\n"
    content_text += f"------------------------\n"
    content_text += f"{copy_text}\n"
    content_text += f"------------------------\n"
    content_text += f"[提示] 活动海报底图和完整文案已在本地 outputs 文件夹中打包，请查收。"

    data = {
        "msg_type": "text",
        "content": {
            "text": content_text
        }
    }
    
    json_data = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(FEISHU_WEBHOOK_URL, data=json_data, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("code") == 0:
                print("✅ 成功推送到飞书！")
            else:
                print(f"❌ 飞书推送失败: {result.get('msg')}")
                print(f"完整响应: {json.dumps(result, indent=2)}")
    except urllib.error.URLError as e:
        print(f"❌ 网络请求失败: {e.reason}")
        if hasattr(e, 'read'):
            try:
                print(f"错误详情: {e.read().decode('utf-8')}")
            except:
                pass
    except Exception as e:
        print(f"❌ 发生未知错误: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python send_to_feishu.py \"活动标题\" \"完整文案长字符串\"")
        sys.exit(1)
        
    title = sys.argv[1]
    text = sys.argv[2]
    
    send_to_feishu(title, text)
