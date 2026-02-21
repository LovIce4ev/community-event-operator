# Skill 编写最佳实践

本文档整合了 Claude Skills 的核心编写原则和最佳实践。

## 目录

- [核心原则](#核心原则)
- [命名规范](#命名规范)
- [Description 编写指南](#description-编写指南)
- [渐进式披露](#渐进式披露)
- [工作流设计](#工作流设计)
- [脚本最佳实践](#脚本最佳实践)
- [反模式清单](#反模式清单)
- [质量检查清单](#质量检查清单)

---

## 核心原则

### 1. 简洁至上

上下文窗口是公共资源。每个 token 都要问自己：
- "Claude 真的需要这个解释吗？"
- "我能假设 Claude 已经知道这个吗？"
- "这段内容值得占用 token 吗？"

**好的示例:**
```markdown
## 提取 PDF 文本

使用 pdfplumber 提取文本：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**差的示例:**
```markdown
## 提取 PDF 文本

PDF（便携式文档格式）是一种常见的文件格式...
（冗长的背景介绍）
```

### 2. 自由度匹配

根据任务的脆弱性和可变性匹配指令的具体程度。

| 自由度 | 适用场景 | 示例 |
|--------|----------|------|
| **高** | 多种方法都可行 | 代码审查流程 |
| **中** | 有首选模式但允许变化 | 带参数的脚本 |
| **低** | 操作脆弱、一致性关键 | 数据库迁移 |

---

## 命名规范

使用一致的命名模式，推荐使用 **动名词形式** (verb + -ing)。

**好的命名示例:**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**避免:**
- 模糊名称: `helper`, `utils`, `tools`
- 过于通用: `documents`, `data`, `files`

---

## Description 编写指南

`description` 字段用于 Skill 发现，必须包含：
1. **做什么** - Skill 的功能
2. **什么时候用** - 触发场景和关键词

### 关键规则

**始终使用第三人称:**
- ✅ "处理 Excel 文件并生成报告"
- ❌ "我可以帮你处理 Excel 文件"

### 好的示例

```yaml
# PDF 处理
description: 从 PDF 文件中提取文本和表格，填写表单，合并文档。当处理 PDF 文件或用户提到 PDF、表单、文档提取时使用。

# Excel 分析
description: 分析 Excel 电子表格，创建数据透视表，生成图表。当分析 Excel 文件、电子表格、表格数据或 .xlsx 文件时使用。
```

---

## 渐进式披露

SKILL.md 作为概览，指向详细材料。三级加载系统：

1. **元数据** (name + description) - 始终在上下文 (~100词)
2. **SKILL.md body** - 触发时加载 (<500行)
3. **Bundled resources** - 按需加载 (无限制)

### 避免深层嵌套引用

**差的示例 (太深):**
```
SKILL.md → advanced.md → details.md → 实际信息
```

**好的示例 (一层深度):**
```
SKILL.md → advanced.md (完整信息)
         → reference.md (完整信息)
         → examples.md (完整信息)
```

---

## 工作流设计

### 复杂任务使用工作流

将复杂操作分解为清晰的顺序步骤，提供检查清单：

```markdown
## PDF 表单填写工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1: 分析表单
- [ ] 步骤 2: 创建字段映射
- [ ] 步骤 3: 验证映射
- [ ] 步骤 4: 填写表单
- [ ] 步骤 5: 验证输出
```
```

### 实现反馈循环

**常见模式**: 运行验证器 → 修复错误 → 重复

```markdown
## 文档编辑流程

1. 编辑 `word/document.xml`
2. **立即验证**: `python scripts/validate.py`
3. 如果验证失败，修复问题后再次验证
4. **只有验证通过后才继续**
```

---

## 脚本最佳实践

### 解决问题，不要推卸

脚本应处理错误条件，而不是推给 Claude。

**好的示例:**
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件 {path} 未找到，创建默认文件")
        return ''
```

### 避免魔法数字

配置参数应有文档说明：

```python
# HTTP 请求通常在 30 秒内完成
REQUEST_TIMEOUT = 30

# 三次重试平衡可靠性和速度
MAX_RETRIES = 3
```

---

## 反模式清单

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| Windows 路径 | `scripts\helper.py` 在 Unix 上出错 | 使用 `scripts/helper.py` |
| 选项过多 | 列出所有可能选项 | 提供默认选项 + 备选方案 |
| 术语不一致 | 混用"端点"、"URL"、"路由" | 选择一个术语并坚持使用 |
| 深层嵌套引用 | A.md → B.md → C.md | 保持一层深度 |

---

## 质量检查清单

分享 Skill 前，验证以下项目：

### 核心质量
- [ ] Description 具体且包含关键词
- [ ] SKILL.md body 少于 500 行
- [ ] 额外详情放在单独文件中（如需要）
- [ ] 全文术语一致
- [ ] 示例具体，非抽象
- [ ] 文件引用保持一层深度

### 代码和脚本
- [ ] 脚本解决问题而非推给 Claude
- [ ] 错误处理明确且有帮助
- [ ] 无"魔法数字"
- [ ] 关键操作有验证/确认步骤
- [ ] 质量关键任务包含反馈循环

### 测试
- [ ] 设计至少三个测试提问
- [ ] 包含正常请求、边缘情况、不应触发的请求
- [ ] 用真实使用场景测试