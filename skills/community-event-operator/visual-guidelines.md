# 海报生成视觉规范与 Prompt 模板

当用户需要生成海报 (或要求提供给 DALL-E/Midjourney 等绘画工具的 Prompt) 时，必须生成一段英文为主、夹带必要说明的提示词，并严格遵守以下视觉红线。

## 视觉DNA (Visual DNA)
- **核心色调**: 治愈系自然色 (如森绿、暖阳黄、日落橘、克莱因蓝) 或 具有现代感的极简黑白灰结构。
- **风格限定**: 避免过度写实或油腻的商业风。推荐使用：
  - `Flat illustration style` (扁平插画风)
  - `Risograph print style` (孔版印刷风 - 颗粒感/复古)
  - `Clean minimal vector art` (干净极简矢量图)
- **构图要求**: 必须为文字预留大量的留白空间 (`negative space for typography`)。

## 交付 Prompt 的组装公式

Agent 输出的海报 Prompt 应包含以下两段：

### 1. 绘图 Prompt (供 AI 生成底图)
> 请复制以下 Prompt 至绘图工具：
```
[Subject: 根据活动提取的主题，如 "A group of friends hiking on a mountain trail", "People sitting in a circle having coffee and chatting"]
Style: [从上方风格限定选一个, 如 Flat illustration style], vibrant and healing color palette.
Composition: Wide angle, plenty of negative space and clean solid backgrounds at the top/bottom for adding text later. No text, no letters, no words in the image. High quality, masterpiece.
```

### 2. 人工排版组装要求 (供用户操作)
> 底图生成后，请在 Canva 或 Figma 等排版工具中完成组装：
> 1. 打上活动核心标题：【 这里填入活动标题 】
> 2. 写上时间地点：【 这里填入时间地点 】
> 3. **强制物料**: 贴上社区 Logo (`assets/logo.png`) 以及 微信报名二维码 (`assets/wechat_qr.png`)。
