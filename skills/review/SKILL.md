---
name: prd-review
description: Use when a product manager wants to check a PRD for completeness, missing sections, or logical issues. Accepts a Feishu link or local file. Add --global flag to also check for conflicts with related historical documents.
---

# PRD Review

Review a PRD document for completeness and correctness. Two modes:

- **Default**: Section-by-section completeness check
- `--global`: Also search for logical conflicts with related documents in the knowledge base

## Invocation

```
review [飞书链接 or local file]
review [飞书链接 or local file] --global
```

## Step 1: Read the Document

**If Feishu link:** Use `docx_v1_document_rawContent` to read the document content.
- For wiki links: first use `wiki_v2_space_getNode` to resolve the actual document token.

**If local file:** Read the file directly.

## Step 2: Completeness Check (Always)

Check each section against the standard PRD template. Output format:

```
✅ [section name]：完整
⚠️ [section name]：[specific missing content]
❌ [section name]：未填写
```

Sections to check:
1. **文档信息** — roles filled in? (placeholders are OK, but warn if completely missing)
2. **变更说明** — at least one entry?
3. **一、业务背景与价值点** — background AND value points both present?
4. **二、目标与范围** — goals listed? Out-of-scope explicitly stated?
5. **三、目标用户** — user type and scenario described?
6. **四、流程** — at least one end-to-end flow described?
7. **五、产品/交互逻辑** — each requirement point has 生效版本? Interaction rules specific enough?
8. **六、异常流程** — covers: network timeout, empty data, insufficient permissions, concurrent operations?
9. **七、验收标准** — each item testable and measurable? No vague language like "works correctly"?
10. **八、数据与埋点** — events and metrics defined? (or explicitly says "无")
11. **九、遗留问题** — unresolved items listed?

After the checklist, output a summary:
```
--- 总结 ---
完整：X 节
有缺漏：X 节
未填写：X 节

[1-3 sentence overall assessment and priority recommendations]
```

## Step 3: Global Check (Only with --global)

### 3.1 收集必要信息

如果用户未在命令中提供以下信息，依次询问：

1. **本地 PRD 文件名**（如未通过 local file 方式调用）
2. **知识库参考文档链接**：请用户提供目标飞书知识库中任意一篇文档的链接

收到链接后，调用 `wiki_v2_space_getNode` 解析出 `space_id`，无需告知用户。

### 3.2 提炼关键词

从 PRD 的"五、产品/交互逻辑"中逐一提取每个需求点的核心关键词（业务实体、动作、状态、角色等），每个需求点 1-3 个关键词组合。

### 3.3 搜索相关文档

对每组关键词调用 `wiki_v1_node_search`（带 `space_id`），合并所有搜索结果，去重后**取排名靠前、语义最相关的 3 篇文档**。

若搜索结果少于 3 篇，取全部结果。

### 3.4 读取并审阅

逐一调用 `docx_v1_document_rawContent` 读取这 3 篇文档，然后与 PRD 进行对比审阅，检查：

- **逻辑一致性**：相同业务实体的状态、规则、权限定义是否一致
- **逻辑冲突**：是否存在与 PRD 直接矛盾的业务规则或流程描述
- **逻辑完整性**：相关文档中涉及的场景、边界条件，PRD 是否有遗漏

### 3.5 输出格式

```
--- 全局检查（参考文档：[doc1标题]、[doc2标题]、[doc3标题]）---

⚠️ 逻辑冲突
- [冲突描述]（来源：[文档标题]）

⚠️ 逻辑遗漏
- [遗漏场景描述]（来源：[文档标题]）

✅ 逻辑一致
- [一致的关键规则描述]（来源：[文档标题]）
```

若无冲突或遗漏：`✅ 全局检查：未发现逻辑冲突或明显遗漏`

## Notes

- Be objective — do not make business judgments on behalf of the PM
- Only flag clear issues — do not penalize stylistic differences
- If a section uses `⚠️ 存疑` markers, note them but do not count as missing
- 只读取最相关的 3 篇文档，控制 token 消耗
