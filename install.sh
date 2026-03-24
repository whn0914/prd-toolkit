#!/usr/bin/env bash
# AI PRD Toolkit 安装脚本
# 用法：bash install.sh

set -e

SKILLS_DIR="${HOME}/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "安装 AI PRD Toolkit skills..."

mkdir -p "${SKILLS_DIR}/prd-generate"
mkdir -p "${SKILLS_DIR}/prd-normalize"
mkdir -p "${SKILLS_DIR}/prd-review"
mkdir -p "${SKILLS_DIR}/prd-merge"

cp "${SCRIPT_DIR}/skills/generate/SKILL.md" "${SKILLS_DIR}/prd-generate/SKILL.md"
cp "${SCRIPT_DIR}/skills/generate/prd-reviewer-prompt.md" "${SKILLS_DIR}/prd-generate/prd-reviewer-prompt.md"
cp "${SCRIPT_DIR}/skills/normalize/SKILL.md" "${SKILLS_DIR}/prd-normalize/SKILL.md"
cp "${SCRIPT_DIR}/skills/review/SKILL.md" "${SKILLS_DIR}/prd-review/SKILL.md"
cp "${SCRIPT_DIR}/skills/merge/SKILL.md" "${SKILLS_DIR}/prd-merge/SKILL.md"

echo "✅ 安装完成！"
echo ""
echo "在 Claude Code 中执行 /reload-plugins，然后 /clear 开始使用："
echo "  prd-generate  — 生成新 PRD"
echo "  prd-normalize — 规范化已有文档"
echo "  prd-review    — 完整性检查"
echo "  prd-merge     — 合并多个 PRD"
