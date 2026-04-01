# AI PRD Toolkit

A Claude Code skill set for product managers. Explores requirements through guided conversation, generates structured PRD documents with Mermaid flowcharts, and integrates with Feishu (Lark).

---

## Install

### Step 1: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 2: Clone and install this toolkit

```bash
git clone https://github.com/whn0914/prd-toolkit
cd prd-toolkit
bash install.sh
```

Then in Claude Code, run:

```
/reload-plugins
/clear
```

---

## Usage

### Step 1: Explore requirements with brainstorm

```
/prd:brainstorm
```

Start a structured multi-turn conversation. Claude asks one question at a time, accepts Axure/Figma prototype screenshots (`Cmd+V`), draws Mermaid flowcharts for confirmation, and saves rolling checkpoints to `projects/.drafts/`. Supports single requirements and multi-requirement version bundles.

When exploration is complete, Claude prompts you to run `/prd:generate`.

### Step 2: Generate the final PRD

```
/prd:generate
/prd:generate [功能名]
```

Reads the draft produced by brainstorm, presents a summary for your confirmation, generates the complete PRD to `projects/`, and runs an automated quality review. If issues are found, they are fixed or flagged with `⚠️ 存疑` for your review.

---

### Normalize an existing document

```
/prd:normalize [飞书链接 or local file]
```

Reads the original, restructures it to the standard template (including Mermaid flowcharts), saves as a new file. The original is never modified.

### Review a document

```
/prd:review [飞书链接 or local file]
/prd:review [飞书链接 or local file] --global
```

- Default: per-section completeness check with ✅/⚠️/❌ output
- `--global`: also checks for logical consistency, conflicts, and completeness against the Feishu knowledge base

**How `--global` works:**

1. Claude extracts keywords from each requirement point in the PRD
2. Searches the target Feishu wiki space using those keywords (`wiki:wiki:readonly` permission required)
3. Reads the top 3 most relevant documents
4. Compares against the PRD and reports: logic conflicts, missing scenarios, and confirmed consistencies

**`--global` requires two inputs (Claude will ask if not provided):**

- The local PRD file path
- Any wiki page link from the target knowledge base — Claude uses it to automatically determine the wiki space

No manual `space_id` configuration needed.

### Merge multiple PRDs

```
/prd:merge projects/A.md projects/B.md
/prd:merge projects/A.md https://xxx.feishu.cn/wiki/xxx
/prd:merge projects/A.md projects/B.md --output merged.md
```

Combines two or more PRDs (local files or Feishu links) into a single structured document with Mermaid flowcharts. Conflicts are automatically annotated with ⚠️ for PM review.

### Generate PRD from Axure prototype

```
/prd:axure-to-prd path/to/file.rp
```

Parses an Axure `.rp` source file directly — no Axure app required. Extracts page labels, annotations, and interaction notes from the binary file, generates Mermaid flowcharts from the sitemap and page structure, then produces a complete PRD saved to `projects/`. Works with Axure 9 and later.

**What gets extracted:**
- Page/folder names → 目标与范围、流程（+ Mermaid）
- UI control labels and field names → 产品/交互逻辑
- Inline annotations and design notes → 交互逻辑、异常流程
- Calculation rules and constraints → 业务背景、验收标准

Image-only shapes are marked as `[原型含图，需 PM 补充描述]` for manual follow-up.

---

## Draft files

During brainstorm, Claude maintains working drafts in `projects/.drafts/`:

```
projects/.drafts/
  [功能名]-draft.md    ← current confirmed state (read by prd-generate)
  [功能名]-log.md      ← append-only change history (human reference only)
```

Drafts are never auto-deleted — you can return to brainstorm at any time to continue refining.

---

## Feishu Integration (Optional)

`/prd:normalize`, `/prd:review`, `/prd:merge`, `/prd:axure-to-prd`, and `/prd:generate` with Feishu upload require the Feishu MCP:

```bash
claude mcp add feishu-mcp -- npx -y feishu-mcp@latest
```

After adding, run `/mcp` in Claude Code to complete authorization.

For `/prd:review --global`, grant `wiki:wiki:readonly` in Feishu Open Platform.

---

## Customization

Both config files live in `.ai-config/` and are loaded automatically:

| File | Purpose | Editable |
|------|---------|----------|
| `.ai-config/prd-template.md` | PRD section structure and required fields | Team lead only |
| `.ai-config/ai-guidelines.md` | AI behavior rules (ask style, checkpoint, Mermaid, review criteria) | PM can modify |

---

## Repository structure

```
├── skills/
│   ├── brainstorm/         # prd-brainstorm: multi-turn requirement exploration
│   │   └── SKILL.md
│   ├── generate/           # prd-generate: draft → final PRD + review
│   │   ├── SKILL.md
│   │   └── prd-reviewer-prompt.md
│   ├── normalize/          # prd-normalize: restructure existing docs
│   │   └── SKILL.md
│   ├── review/             # prd-review: completeness & conflict check
│   │   └── SKILL.md
│   ├── merge/              # prd-merge: combine multiple PRDs
│   │   └── SKILL.md
│   └── axure-to-prd/       # prd-axure-to-prd: parse .rp file → PRD
│       ├── SKILL.md
│       └── parse_axure.py
├── .ai-config/
│   ├── prd-template.md
│   └── ai-guidelines.md
├── install.sh
└── README.md
```
