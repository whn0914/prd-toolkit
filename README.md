# AI PRD Toolkit

A Claude Code skill set for product managers. Generates, normalizes, reviews, and merges PRD documents through guided AI conversation, with optional Feishu (Lark) integration.

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

### Step 3: (Optional) Install Superpowers

The `prd-generate` skill works standalone. If you also have the [Superpowers](https://github.com/obra/superpowers-marketplace) plugin installed, its brainstorming capabilities will be available during generation.

---

## Usage

### Generate a new PRD

```
/prd:generate
```

Start a guided conversation. Claude asks one question at a time, accepts Axure/Figma prototype screenshots (`Cmd+V`), and generates a complete PRD saved to `projects/`.

### Normalize an existing document

```
/prd:normalize [飞书链接 or local file]
```

Reads the original, restructures it to the standard template, saves as a new file. The original is never modified.

### Review a document

```
/prd:review [飞书链接 or local file]
/prd:review [飞书链接 or local file] --global
/prd:review [飞书链接 or local file] --global --space=[wiki_space_id]
```

- Default: per-section completeness check with ✅/⚠️/❌ output
- `--global`: also checks for logical conflicts with related documents in the Feishu knowledge base
- `--space`: restrict knowledge base search to a specific wiki space

### Merge multiple PRDs

```
/prd:merge projects/A.md projects/B.md
/prd:merge projects/A.md https://xxx.feishu.cn/wiki/xxx
/prd:merge projects/A.md projects/B.md --output merged.md
```

Combines two or more PRDs (local files or Feishu links) into a single structured document. Conflicts are automatically annotated with ⚠️ for PM review.

### Generate PRD from Axure prototype

```
/prd:axure-to-prd path/to/file.rp
```

Parses an Axure `.rp` source file directly — no Axure app required. Extracts page labels, annotations, and interaction notes from the binary file, then generates a complete PRD saved to `projects/`. Works with Axure 9 and later.

**What gets extracted:**
- Page/folder names → 目标与范围、流程
- UI control labels and field names → 产品/交互逻辑
- Inline annotations and design notes → 交互逻辑、异常流程
- Calculation rules and constraints → 业务背景、验收标准

Image-only shapes are marked as `[原型含图，需 PM 补充描述]` for manual follow-up.

---

## Feishu Integration (Optional)

`/prd:normalize`, `/prd:review`, `/prd:merge`, and `/prd:axure-to-prd` with Feishu upload require the Feishu MCP:

```bash
claude mcp add feishu-mcp -- npx -y feishu-mcp@latest
```

After adding, run `/mcp` in Claude Code to complete authorization.

For `/prd:review --global`, grant `wiki:wiki:readonly` in Feishu Open Platform.

**Configure default wiki space** — create `.ai-config/feishu-config.json` in your workspace:

```json
{
  "wiki_space_id": "your_space_id_here"
}
```

To find your `space_id`: send any wiki page link to Claude and ask "帮我查一下这篇文章所在知识库的 space_id".

---

## Customization

Both config files live in `.ai-config/` and are loaded automatically:

| File | Purpose | Editable |
|------|---------|----------|
| `.ai-config/prd-template.md` | PRD section structure and required fields | Team lead only |
| `.ai-config/ai-guidelines.md` | AI behavior rules (ask style, review criteria) | PM can modify |

If these files exist in your working directory, they override the defaults.

---

## Repository structure

```
├── skills/
│   ├── generate/           # prd-generate: guided PRD creation
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
├── install.sh
└── README.md
```
