# CMI 社区活动运营助手 (Community Event Operator)

当用户需要为 CMI 社区策划活动时，帮助生成活动海报 Prompt、各渠道宣传文案，并提供打包交付能力。

## 触发条件

当用户有以下需求时激活此技能：
- "帮我做个活动海报"
- "写个活动推文"
- "生成宣传文案"
- "要做活动了，帮我想想怎么宣传"
- "给我个海报 Prompt"

## 工作流程

### 第一步：信息收集

向用户询问以下必要信息：
- **活动标题**：活动的核心名称
- **活动类型**：户外/咖啡/工作坊/聚餐/其他
- **时间**：具体日期和时段
- **地点**：具体地址或集合点
- **费用**：免费/人均 XX 元
- **人数限制**：最多多少人
- **活动亮点/流程**：2-3 句话描述吸引人的地方
- **目标渠道**：微信公众号 / 小红书 / 社群（可多选）

### 第二步：生成海报 Prompt

根据 `visual-guidelines.md` 生成英文 Prompt 供 AI 绘图工具使用。

Prompt 结构：
```
[Subject: {根据活动提取的主题场景}]
Style: [Flat illustration style / Risograph print style / Clean minimal vector art], vibrant and healing color palette.
Composition: Wide angle, plenty of negative space and clean solid backgrounds at the top/bottom for adding text later. No text, no letters, no words in the image. High quality, masterpiece.
```

### 第三步：生成渠道文案

根据 `tone-dna.yaml` 的人设和 `channel-templates.md` 的模板，为选定的渠道生成文案。

**文案原则**：
- 使用短句、半口语化
- 真诚直接，不卖弄专业
- 植入关键词：走起、别鸽、周末见、逃离城市、私藏路线
- 善用 emoji，但不要滥用（每段不超过 2 个）

### 第四步：打包交付

告诉用户所有物料已准备完毕，包括：
1. 海报底图 Prompt（供绘图工具使用）
2. 各渠道宣传文案
3. 排版要求（Logo + 二维码位置）

**重要规则：生成海报后的交付**
- 每次生成完海报，必须**直接发送原图文件**给用户
- 不要只发送预览截图或文字描述
- 使用 `message` 工具的 `media` 参数发送原图
- 原图保存在 `outputs/` 目录中

---

## 资源文件

| 文件 | 说明 |
|------|------|
| `assets/logo.png` | CMI 社区 Logo |
| `assets/wechat_qr.png` | 微信报名二维码（需用户自行添加） |
| `assets/JiangCheng-600W.ttf` | 主标题字体（江城黑体 600W） |
| `assets/JiangCheng-300W.ttf` | 副标题字体（江城黑体 300W） |
| `assets/Delight-Bold.ttf` | 英文主标题字体 |
| `assets/Delight-Regular.ttf` | 英文副标题字体 |
| `scripts/package_assets.py` | 自动打包脚本 |
| `scripts/send_to_feishu.py` | 飞书推送脚本 |
| `scripts/test_pil.py` | 基础海报布局测试 |
| `scripts/test_layout_v3.py` | 侧边栏布局版本 |
| `scripts/test_layout_v4.py` | 底部双栏布局版本 |

## 海报自动生成

skill 包含基于 PIL 的海报自动排版脚本，可以直接生成带文字布局的海报预览：

```bash
cd ~/openclaw-workspace/skills/community-event-operator

# 生成基础布局
python3 scripts/test_pil.py

# 生成侧边栏布局 (v3)
python3 scripts/test_layout_v3.py

# 生成底部双栏布局 (v4)
python3 scripts/test_layout_v4.py
```

生成的预览图会保存在 `outputs/` 目录中。这些脚本使用 CMI 标准字体，按照视觉规范自动排版活动信息。

## 字体规范

- **主标题**：江城黑体 600W
- **副标题及信息**：江城黑体 300W
- **英文主标题**：Delight-Bold
- **英文副标题**：Delight-Regular
