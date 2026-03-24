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
review [飞书链接 or local file] --global --space=[wiki_space_id]
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

After the completeness check, determine the wiki space to search:

### Resolve `space_id` (priority order)

1. **Inline flag**: If `--space=[value]` is provided, use that value directly.
2. **Config file**: Check for `.ai-config/feishu-config.json` in the current working directory. If it contains `"wiki_space_id"`, use that value.
3. **Auto-detect from document**: If the document was a wiki link, the `wiki_v2_space_getNode` response includes a `space_id` field — use it.
4. **No filter**: If none of the above apply, call `wiki_v1_node_search` without `space_id` (searches all accessible wiki spaces — may return unrelated results).

### How PMs find their `space_id`

Open any page in the target knowledge base. The URL looks like:
```
https://xxx.feishu.cn/wiki/ZLIgw7SqNix1fRknuvXcWLSjnWe
```
Call `wiki_v2_space_getNode` with `token=ZLIgw7SqNix1fRknuvXcWLSjnWe` — the response contains `space_id`.
Alternatively, the PM can find it in Feishu → 知识库 → 设置 → 基本信息.

### Search and analyze

1. Call `wiki_v1_node_search` with the resolved `space_id` (if any) and the document's core topic as query
2. Find up to 10 semantically related documents
3. Read the most relevant ones using `docx_v1_document_rawContent`
4. Check for:
   - **Logic conflicts**: business rules, state transitions, permission definitions that contradict this document
   - **Missing scenarios**: situations covered in related docs but absent here

Output format for global issues:

```
--- 全局检查（知识库：[space_id or 全部]）---

⚠️ 逻辑冲突
- [conflict description] （来源：[document name]）

⚠️ 遗漏场景
- [scenario description] （来源：[document name]）
```

If no conflicts or gaps found: `✅ 全局检查：未发现逻辑冲突或明显遗漏`

## Notes

- Be objective — do not make business judgments on behalf of the PM
- Only flag clear issues — do not penalize stylistic differences
- If a section uses `⚠️ 存疑` markers, note them but do not count as missing
- Max 10 related documents read during global check
