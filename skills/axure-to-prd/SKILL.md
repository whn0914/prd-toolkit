---
name: prd-axure-to-prd
description: Use when a product manager provides an Axure .rp source file path and wants to generate a structured PRD from the prototype. Parses the binary .rp format, extracts page labels, annotations, and interaction notes, then produces a standard PRD document.
---

# Axure to PRD

Parse an Axure `.rp` prototype source file, extract all text content, and produce a complete PRD following the standard template. No Axure app required — works directly from the binary file.

## Invocation

```
/prd:axure-to-prd [path/to/file.rp]
```

## How Axure .rp Files Work

Axure RP source files use a proprietary binary format (magic bytes: `ac ef 09 00`). Content blocks are compressed with raw DEFLATE inside a gzip wrapper. Each block contains a mix of binary framing and UTF-8 text — page labels, shape names, annotation notes, and interaction descriptions.

The parser in `parse_axure.py` handles this automatically.

## Workflow

### Step 1: Parse the .rp File

Run the bundled parser. The skill file is in the same directory as this SKILL.md:

```bash
python3 "$(dirname "$0")/parse_axure.py" "/path/to/file.rp"
```

Use the Bash tool to execute this. Capture the JSON output — it contains:
- `sitemap`: top-level page/folder names
- `pages[].labels`: short UI labels and control names
- `pages[].notes`: longer annotation text and design specs
- `notes`: all annotation strings deduplicated

If the file path contains spaces, quote it.

### Step 2: Analyze Content

From the parsed output, identify:

| Source field | Maps to PRD section |
|---|---|
| Sitemap names | 目标与范围、流程（页面清单）|
| Page labels (UI controls, field names) | 产品/交互逻辑 |
| Short annotations (规则、限制说明) | 产品/交互逻辑、异常流程 |
| Long annotations (背景说明、计算规则) | 业务背景、产品/交互逻辑 |
| Error/limit descriptions | 异常流程与边界条件 |
| Acceptance-style notes | 验收标准 |

### Step 3: Ask One Clarifying Question (if needed)

If the parsed content is missing an obvious section (e.g., no business background found), ask the PM **one question only** before generating:

> "原型里没有找到背景说明，这个需求的核心目的是什么？"

If content is sufficient, skip directly to Step 4.

### Step 4: Generate the PRD

Fill the standard template. Content rules:
- **Do not invent** — only use what was extracted or stated by the PM
- Annotation notes → use verbatim or lightly paraphrased
- UI labels → group logically under 产品/交互逻辑
- If a section has no source content, leave it with a placeholder `（原型未涉及，需 PM 补充）`
- Add `[原型含图，需 PM 补充描述]` where visual layout matters but cannot be inferred

**Mermaid 生成规则：**
- **「四、流程」**：根据 sitemap 页面顺序和页面间跳转关系，生成 `flowchart TD` 流程图
- **「五、产品/交互逻辑」**：页面内存在多状态、条件分支时，插入对应 Mermaid 图
- 无法确定跳转关系时，标注 `（原型跳转逻辑不明确，需 PM 确认）`

```markdown
# [功能名称]

## 文档信息

| 角色 | 姓名 |
|------|------|
| 产品经理 | |
| UI | |
| 开发 | |
| 测试 | |

**原型蓝湖：**（待填写）
**蓝湖设计稿：**（待填写）
**发布版本：**（待填写）

---

## 变更说明

| 版本 | 变更人 | 变更日期 | 变更内容 |
|------|-------|---------|---------｜
| 1.0.0 | | [TODAY] | 基于 Axure 原型自动生成 |

---

## 一、业务背景与价值点
...

## 二、目标与范围
...

## 三、目标用户
...

## 四、流程
...

## 五、产品/交互逻辑
...

## 六、异常流程与边界条件

| 场景 | 触发条件 | 系统处理方式 |
|------|---------|------------|
| | | |

## 七、验收标准

- [ ] ...

## 八、数据与埋点需求
...

## 九、遗留问题

| 问题 | 负责人 | 截止日期 |
|------|-------|---------|
| | | |
```

### Step 5: Save

Save to `projects/[功能名称].md`.

### Step 6: Confirm

Tell the PM:
- Output file path
- Sections filled vs left as placeholders
- Any content that couldn't be mapped (placed in 遗留问题)

Then offer:
> "内容已从原型中提取并生成 PRD。如需进一步完善，可以运行 `/prd:review` 做质量检查，或直接告诉我需要补充的内容。确认后可以上传到飞书。"

## Optional: Upload to Feishu

If the PM says "上传到飞书" or "import to Feishu", use `docx_builtin_import` to upload the generated markdown file to Feishu.

## Parser Limitations

- **No visual layout** — spatial relationships between elements are lost; only text content is extracted
- **Image widgets** — image-only shapes have no text; annotate as `[原型含图，需 PM 补充描述]`
- **Master pages** — content from Axure masters may appear duplicated across pages; deduplicate during Step 2
- **Very large files** (>5 MB) — parsing may be slow; this is normal
