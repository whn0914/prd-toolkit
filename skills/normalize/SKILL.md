---
name: prd-normalize
description: Use when a product manager provides a Feishu document link or local file path and wants to restructure it into the standard PRD format. Reads the original document, reorganizes content, and creates a new file without modifying the original.
---

# PRD Normalize

Read an existing PRD (Feishu link or local file), reorganize it according to the standard template, and save as a new document. The original is never modified.

## Invocation

```
规范化 [飞书链接]
规范化 [local/file/path.md]
normalize [feishu link or file path]
```

## Rules

- **Read only** the original — never write back to it
- Preserve all useful information — do not omit or reinterpret content
- If content doesn't clearly belong to a section, put it in 遗留问题 and note the original location
- If the original has images you cannot read, mark the position: `[原文档含截图，需 PM 补充描述]`
- Do not invent content — only reorganize what exists
- Fill 变更说明 version 1.0.0 with today's date and a one-line summary of the document topic
- Leave 产品经理/UI/开发/测试/蓝湖/发布版本 as placeholders if not present in source

## Workflow

### Step 1: Read the Source

**If Feishu link:** Use the Feishu MCP tool `docx_v1_document_rawContent` to read the document.
- Extract the document token from the URL (the string after `/docx/` or `/wiki/`)
- For wiki links: first call `wiki_v2_space_getNode` to get the actual document token

**If local file:** Read the file directly.

### Step 2: Analyze and Map

Scan all content in the original and map each piece to a PRD section:
1. 业务背景与价值点
2. 目标与范围
3. 目标用户
4. 流程
5. 产品/交互逻辑
6. 异常流程与边界条件
7. 验收标准
8. 数据与埋点
9. 遗留问题

Note any content that doesn't fit cleanly into a section.

### Step 3: Generate Restructured Document

Follow this template exactly:

```markdown
# [Document Title]

## 文档信息

| 角色 | 姓名 |
|------|------|
| 产品经理 | [from source, or leave blank] |
| UI | [from source, or leave blank] |
| 开发 | [from source, or leave blank] |
| 测试 | [from source, or leave blank] |

**原型蓝湖：**（待填写）
**蓝湖设计稿：**（待填写）
**发布版本：**（待填写）

---

## 变更说明

| 版本 | 变更人 | 变更日期 | 变更内容 |
|------|-------|---------|---------｜
| 1.0.0 | | [TODAY] | 规范化整理原文档 |

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

### Step 4: Save

Save to `projects/[original-title]-规范版.md`.

### Step 5: Confirm

Tell the PM:
- Output file path
- How many sections were filled vs left empty
- Any content that could not be mapped (placed in 遗留问题)
- Any image placeholders added

## Optional: Upload to Feishu

If the PM says "上传到飞书" or "import to Feishu" after normalizing, use `docx_builtin_import` to upload the generated markdown file to Feishu.
