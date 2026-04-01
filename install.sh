#!/usr/bin/env bash
# AI PRD Toolkit 安装脚本
# 用法：bash install.sh

set -e

SKILLS_DIR="${HOME}/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "安装 AI PRD Toolkit skills..."

mkdir -p "${SKILLS_DIR}/prd-brainstorm"
mkdir -p "${SKILLS_DIR}/prd-generate"
mkdir -p "${SKILLS_DIR}/prd-normalize"
mkdir -p "${SKILLS_DIR}/prd-review"
mkdir -p "${SKILLS_DIR}/prd-merge"
mkdir -p "${SKILLS_DIR}/prd-axure-to-prd"

cp "${SCRIPT_DIR}/skills/brainstorm/SKILL.md" "${SKILLS_DIR}/prd-brainstorm/SKILL.md"
cp "${SCRIPT_DIR}/skills/generate/SKILL.md" "${SKILLS_DIR}/prd-generate/SKILL.md"
cp "${SCRIPT_DIR}/skills/generate/prd-reviewer-prompt.md" "${SKILLS_DIR}/prd-generate/prd-reviewer-prompt.md"
cp "${SCRIPT_DIR}/skills/normalize/SKILL.md" "${SKILLS_DIR}/prd-normalize/SKILL.md"
cp "${SCRIPT_DIR}/skills/review/SKILL.md" "${SKILLS_DIR}/prd-review/SKILL.md"
cp "${SCRIPT_DIR}/skills/merge/SKILL.md" "${SKILLS_DIR}/prd-merge/SKILL.md"
cp "${SCRIPT_DIR}/skills/axure-to-prd/SKILL.md" "${SKILLS_DIR}/prd-axure-to-prd/SKILL.md"
cp "${SCRIPT_DIR}/skills/axure-to-prd/parse_axure.py" "${SKILLS_DIR}/prd-axure-to-prd/parse_axure.py"

echo "✅ 安装完成！"
echo ""
echo "在 Claude Code 中执行 /reload-plugins，然后 /clear 开始使用："
echo "  prd-brainstorm    — 多轮需求探讨，产出草稿"
echo "  prd-generate      — 从草稿生成正式 PRD"
echo "  prd-normalize     — 规范化已有文档"
echo "  prd-review        — 完整性检查"
echo "  prd-merge         — 合并多个 PRD"
echo "  prd-axure-to-prd  — 解析 Axure .rp 文件生成 PRD"
