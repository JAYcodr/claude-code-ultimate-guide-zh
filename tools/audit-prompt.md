# 审计你的 Claude Code 配置

> 一个自包含的提示词，可一站式审计你的 Claude Code 配置 — 项目记忆、规则健康度、技能、代理/命令、安全性、MCP、工作流命令和新鲜度。

**作者**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | 创始工程师 [@Méthode Aristote](https://methode-aristote.fr)

**参考**: [The Ultimate Claude Code 指南](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. 功能概述

此提示词将 Claude 转变为 **审计编排器**，涵盖 8 个加权维度（总计 100 分）。它先快速运行 bash 清单，然后将每个领域委托给已安装的专用技能或命令，否则回退到内联检查。

| 审计内容 | 方式 |
|---|---|
| 内存和上下文（CLAUDE.md、规则、token 预算） | 若已安装则委托给 `/token-audit`，否则 bash 估算 |
| 规则健康度（`.claude/rules/`、`paths:` 有效性） | 若已安装则委托给 `/eval-rules`，否则 bash 扫描 |
| 技能质量（frontmatter、effort、allowed-tools） | 若已安装则委托给 `/eval-skills`，否则快速检查 |
| 代理/命令质量（16 项标准，A-F 等级） | 若已安装则委托给 `/audit-agents-skills`，否则检查 |
| 安全态势（权限、钩子、沙箱） | 若已安装则委托给 `/security-check`，否则 bash 检查 |
| MCP 生态（服务器、数据库风险、版本安全） | 内联 bash（无需专用技能） |
| 工作流命令（/investigate, /qa, /canary…） | 内联 bash 扫描 |
| 新鲜度与最佳实践（过时引用、缓存缺陷） | 内联 bash + 模式检查 |

**本提示词不做的事情**：不替代它所委托的深度工具。若要获取特定维度的完整细节，请直接使用 `/security-audit`、`/token-audit`、`/eval-rules`。

**时间**：若已安装所有审计技能约 5-8 分钟，回退模式下约 3-4 分钟。

**重要提示**：未经你明确批准，Claude 不会做出任何更改。

---

## 2. 适用人群

| 级别 | 你将获得 |
|-------|-----------------|
| **初学者** | 发现你缺少什么并获取入门模板 |
| **中级用户** | 识别优化机会和进阶模式 |
| **高级用户** | 验证你的配置并打磨边缘情况 |

**先决条件**：
- 已安装可正常使用的 Claude Code
- 待分析的项目目录（或仅全局配置）
- Bash shell（macOS/Linux 原生，Windows 使用 WSL）

**可选**（获得更丰富结果）：安装 `/token-audit`、`/eval-rules`、`/eval-skills`、`/audit-agents-skills`、`/security-check`。安装命令见第 8 节。

---

## 3. 使用方法

### 步骤 1：复制提示词

复制下方[第 4 节](#4-提示词)中代码块内的所有内容。

### 步骤 2：运行 Claude Code

```bash
cd your-project-directory
claude
```

### 步骤 3：粘贴并执行

粘贴提示词后按回车。若要同时审计全局 `~/.claude/` 配置，请在粘贴后附加 `--include-global`。

### 步骤 4：查看结果

Claude 将呈现 8 维度的评分卡，并在做出任何更改前请求你的确认。

### 平台说明

| 平台 | 全局配置路径 |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. 提示词

````markdown
# 审计我的 Claude Code 配置 — v5.0

## 范围检测

检查用户是否在提示词后附加了 `--include-global`。
- **默认（仅项目）**：审计当前目录下的 `.` + `.claude/`。
- **包含 `--include-global`**：同时审计 `~/.claude/` 和 `~/.claude.json`。

据此设置 SCOPE。所有下方的 bash 代码块均会注明每个范围适用的路径。

## 指令

不要修改任何文件。不要做任何更改。仅审计和报告。

使用高效的 bash 命令进行发现。仅在需要评分时才读取文件内容。

---

## 阶段 1 — 清单（30 秒，仅 bash）

运行以下单个代码块以一次性收集所有结构数据：

```bash
bash -c '
echo "=== SCOPE ==="
SCOPE="project"
[[ "$*" == *"--include-global"* ]] && SCOPE="project+global"
echo "Audit scope: $SCOPE"
CURRENT_DIR=$(pwd)

echo ""
echo "=== CONFIG FILES ==="
# Project
for f in ./CLAUDE.md ./.claude/CLAUDE.md ./.claude/settings.json ./.claude/settings.local.json; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f"
done
# Global (always check for context, even in project-only scope)
[ -f ~/.claude/CLAUDE.md ] && echo "✅ ~/.claude/CLAUDE.md (global)" || echo "❌ ~/.claude/CLAUDE.md (global)"
[ -f ~/.claude.json ] && echo "✅ ~/.claude.json (MCP config)" || echo "❌ ~/.claude.json"

echo ""
echo "=== FOLDER STRUCTURE ==="
for d in agents commands skills hooks rules styles; do
  if [ -d "./.claude/$d" ]; then
    count=$(find "./.claude/$d" -maxdepth 2 -type f | wc -l | tr -d " ")
    echo "✅ .claude/$d/ ($count files)"
  else
    echo "❌ .claude/$d/"
  fi
done

echo ""
echo "=== TECH STACK ==="
[ -f package.json ] && grep -o '"name": *"[^"]*"' package.json | head -1 | sed "s/\"name\": /nodejs: /"
[ -f pyproject.toml ] && grep "^name" pyproject.toml | head -1 | sed "s/name/python:/"
[ -f requirements.txt ] && echo "python: requirements.txt"
[ -f go.mod ] && head -1 go.mod | sed "s/module /go: /"
[ -f Cargo.toml ] && grep "^name" Cargo.toml | head -1 | sed "s/name/rust:/"
[ -f composer.json ] && echo "php: detected"
[ -f Gemfile ] && echo "ruby: detected"

echo ""
echo "=== MCP SERVERS ==="
if command -v jq &>/dev/null && [ -f ~/.claude.json ]; then
  MCP=$(jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null)
  [ -n "$MCP" ] && echo "$MCP" | sed "s/^/  /" || echo "  (none for this project)"
  DB_MCP=$(echo "$MCP" | grep -iE "postgres|neon|supabase|mysql|database" || true)
  [ -n "$DB_MCP" ] && echo "  ⚠️  DB MCPs detected: $DB_MCP (verify not production)"
else
  echo "  (jq not installed or ~/.claude.json absent)"
fi

echo ""
echo "=== RULES INVENTORY ==="
RULES_DIR="./.claude/rules"
if [ -d "$RULES_DIR" ]; then
  count=$(find "$RULES_DIR" -name "*.md" | wc -l | tr -d " ")
  size=$(find "$RULES_DIR" -name "*.md" | xargs wc -c 2>/dev/null | tail -1 | awk "{print \$1}")
  echo "  $count rules files, ~$size total chars"
  echo "  Top 3 by size:"
  find "$RULES_DIR" -name "*.md" | xargs wc -c 2>/dev/null | sort -rn | head -4 | grep -v "total" | awk "{print \"    \" \$0}"
  with_paths=$(grep -rl "^paths:" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
  always_on=$(( count - with_paths ))
  echo "  path-scoped: $with_paths | always-on: $always_on"
else
  echo "  No .claude/rules/ directory"
fi

echo ""
echo "=== AUDIT SKILLS AVAILABLE ==="
for skill in token-audit eval-rules eval-skills audit-agents-skills; do
  found=false
  [ -f "$HOME/.claude/skills/$skill/SKILL.md" ] && found=true
  [ -f ".claude/skills/$skill/SKILL.md" ] && found=true
  $found && echo "  ✅ /$skill" || echo "  ❌ /$skill (fallback mode)"
done
for cmd in security-check security-audit; do
  found=false
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd (fallback mode)"
done

echo ""
echo "=== CACHE BUG INDICATORS ==="
grep -rl "disableSkillShellExecution\|--resume" .claude/ ~/.claude/ 2>/dev/null | head -3 | sed "s/^/  /" || echo "  No cache bug workarounds found"
' "$@"
```

保存此完整输出。用于下方所有维度的评分。

---

## 阶段 2 — 维度审计

对每个维度进行评分。对于有委托技能的维度，检查该技能是否可用（依据阶段 1 输出）。如果 ✅：调用该技能并使用其输出进行评分。如果 ❌：运行内联回退 bash 并应用简化启发式规则。

### 维度 1 — 内存与上下文（20 分）

**完整审计**（如果 `/token-audit` 可用）：
调用：`/token-audit`
使用 Token Audit 输出：
- 固定上下文 <20K tokens → 18-20 分
- 20-40K tokens → 12-17 分
- 40-60K tokens → 6-11 分
- >60K tokens → 0-5 分。如果缺少 CLAUDE.md 扣 2 分，缺少全局 CLAUDE.md 扣 3 分。

**回退**（如果未安装 `/token-audit`）：

```bash
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c || echo 0)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
TOTAL=$(( (GLOBAL + PROJECT + RULES) / 4 + 7500 ))
echo "Estimated fixed context: ~$TOTAL tokens (~$(( TOTAL * 100 / 200000 ))% of 200K window)"
```

回退评分（最高 14 分）：
- 全局 CLAUDE.md 存在且非空：3 分
- 项目 CLAUDE.md 存在：3 分
- 规则数量合理（<15 个文件）：2 分
- Token 估算 <20K：6 分 | 20-40K：3 分 | >40K：0 分

### 维度 2 — 规则健康度（10 分）

**完整审计**（如果 `/eval-rules` 可用）：
调用：`/eval-rules`
取所有规则文件的平均分（每个 12 分）。按比例映射到 10 分。

**回退**（如果未安装 `/eval-rules`）：

```bash
RULES_DIR=".claude/rules"
[ -d "$RULES_DIR" ] || { echo "No rules dir"; exit 0; }
total=$(find "$RULES_DIR" -name "*.md" | wc -l | tr -d " ")
with_front=$(grep -rl "^---" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
with_paths=$(grep -rl "^paths:" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
valid_patterns=0
for f in "$RULES_DIR"/*.md; do
  pattern=$(grep -A1 "^paths:" "$f" 2>/dev/null | grep "^\s*-" | head -1 | sed "s/.*- //;s/['\"]//g")
  [ -n "$pattern" ] && ls $pattern 2>/dev/null | head -1 | grep -q . && valid_patterns=$(( valid_patterns + 1 ))
done
echo "Total: $total | With frontmatter: $with_front | With paths: $with_paths | Valid patterns: $valid_patterns"
```

回退评分（最高 8 分）：
- 规则目录存在：1 分
- 所有文件都有 YAML frontmatter：2 分
- 至少一半有 `paths:` 字段：3 分
- 无文件超过 150 行（使用 `wc -l` 检查）：2 分

### 维度 3 — 技能质量（10 分）

**完整审计**（如果 `/eval-skills` 可用）：
调用：`/eval-skills`
取所有技能文件的平均分（每个 14 分）。按比例映射到 10 分。

**回退**（如果未安装 `/eval-skills`）：

```bash
SKILLS_DIR=".claude/skills"
[ -d "$SKILLS_DIR" ] || { echo "No skills dir (0 pts)"; exit 0; }
total=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d " ")
with_effort=$(grep -rl "^effort:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
with_tools=$(grep -rl "^allowed-tools:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
with_desc=$(grep -rl "^description:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
echo "Skills: $total | effort field: $with_effort | allowed-tools: $with_tools | description: $with_desc"
```

回退评分（最高 8 分）：
- 技能目录存在：1 分
- 所有 SKILL.md 都有 `description:` 字段：2 分
- 所有 SKILL.md 都有 `effort:` 字段：3 分
- 所有 SKILL.md 都有 `allowed-tools:` 字段：2 分

### 维度 4 — 代理/命令质量（10 分）

**完整审计**（如果 `/audit-agents-skills` 可用）：
调用：`/audit-agents-skills`
取其报告中的总体得分（score/100）。乘以 0.10 得到 10 分制下的得分。

**回退**（如果未安装 `/audit-agents-skills`）：

```bash
agents=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l | tr -d " ")
commands=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l | tr -d " ")
skills=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d " ")
with_front=$(find .claude/agents .claude/commands .claude/skills -name "*.md" 2>/dev/null | xargs grep -l "^---" 2>/dev/null | wc -l | tr -d " ")
with_desc=$(find .claude/agents .claude/commands .claude/skills -name "*.md" 2>/dev/null | xargs grep -l "^description:" 2>/dev/null | wc -l | tr -d " ")
# Check argument-hint on legacy commands still using $ARGUMENTS
uses_args=$(find .claude/commands -name "*.md" 2>/dev/null | xargs grep -l '\$ARGUMENTS' 2>/dev/null | wc -l | tr -d " ")
with_hint=$(find .claude/commands -name "*.md" 2>/dev/null | xargs grep -l 'argument-hint' 2>/dev/null | wc -l | tr -d " ")
echo "Agents: $agents | Commands: $commands | Skills: $skills | With frontmatter: $with_front | With description: $with_desc"
echo "Commands using \$ARGUMENTS: $uses_args | With argument-hint: $with_hint"
```

回退评分（最高 8 分）：
- 存在代理、命令或技能：2 分
- 全部都有 YAML frontmatter：2 分
- 全部都有 `description:` 字段：2 分
- 所有使用 `$ARGUMENTS` 的旧版命令都包含 `argument-hint:`：2 分

### 维度 5 — 安全态势（20 分）

**完整审计**（如果 `/security-check` 可用）：
调用：`/security-check`
将其发现映射到 20 分：
- 无严重发现：18-20 分
- 1-2 个中等发现：12-17 分
- 3+ 个发现或任一严重发现：0-11 分

**回退**（如果未安装 `/security-check`）：

```bash
# permissions.deny check
echo "=== Permissions Deny ==="
for setting in ".claude/settings.json" "~/.claude/settings.json"; do
  [ -f "$setting" ] && {
    echo "File: $setting"
    grep -E "\.env|\.pem|credentials|secrets" "$setting" 2>/dev/null && echo "  ✅ Sensitive patterns found" || echo "  ❌ No .env/.pem/credentials blocked"
    grep -i "sandbox\|failIfUnavailable" "$setting" 2>/dev/null | head -3 | sed "s/^/  /"
  }
done

echo ""
echo "=== Hooks ==="
if [ -d ".claude/hooks" ]; then
  hooks=$(ls .claude/hooks/*.sh 2>/dev/null | wc -l | tr -d " ")
  pretool=$(grep -rl "PreToolUse" .claude/hooks/ 2>/dev/null | wc -l | tr -d " ")
  echo "  Hooks: $hooks | PreToolUse: $pretool"
else
  echo "  ❌ No hooks directory"
fi

echo ""
echo "=== Dangerous Patterns ==="
# Check for hardcoded tokens/keys in config
grep -rn "sk-\|ghp_\|xox[baprs]-\|AKIA" .claude/ CLAUDE.md 2>/dev/null | grep -v "example\|sample\|template" | head -5 || echo "  No obvious secrets found"
```

回退评分（最高 17 分）：
- `.env*` 已在 `permissions.deny` 中阻止：4 分
- `*.pem` 和 `credentials*` 也已阻止：3 分
- 至少存在一个 `PreToolUse` 钩子：4 分
- 已配置沙箱（`failIfUnavailable`）：3 分
- 配置中无硬编码密钥：3 分

### 维度 6 — MCP 生态（10 分）

仅内联 bash（该维度无专用技能）：

```bash
CURRENT_DIR=$(pwd)
echo "=== MCP Servers for this project ==="
if command -v jq &>/dev/null && [ -f ~/.claude.json ]; then
  jq -r --arg p "$CURRENT_DIR" '
    .projects[$p].mcpServers // {} | to_entries[] |
    "\(.key): \(.value.command // .value.url // "configured")"
  ' ~/.claude.json 2>/dev/null || echo "  No project-specific MCPs"

  echo ""
  echo "=== DB MCP Risk ==="
  jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null \
    | grep -iE "postgres|neon|supabase|mysql|database|mongo" \
    | sed "s/^/  ⚠️  /" || echo "  No DB MCPs found"

  echo ""
  echo "=== Guide MCP ==="
  jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null \
    | grep -iE "claude-code-ultimate-guide|ccguide" \
    | sed "s/^/  ✅ /" || echo "  ❌ Guide MCP not installed"
else
  echo "  (install jq for MCP analysis)"
fi
```

评分（最高 10 分）：
- 至少配置了 1 个 MCP：3 分
- 存在文档 MCP（Context7 或类似）：2 分
- 无数据库 MCP，或数据库 MCP 明确限定于开发/测试环境：3 分
- 已安装指南 MCP：2 分

### 维度 7 — 工作流命令（10 分）

```bash
echo "=== Core Workflow Skills/Commands ==="
for cmd in investigate qa canary land-and-deploy review-pr; do
  found=false
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd"
done

echo ""
echo "=== Additional Debug/Deploy Skills/Commands ==="
for cmd in ship commit release-notes diagnose; do
  found=false
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd"
done
```

评分：每个核心命令（`/investigate`、`/qa`、`/canary`、`/land-and-deploy`、`/review-pr`）2 分。最高 10 分。

### 维度 8 — 新鲜度与最佳实践（10 分）

```bash
echo "=== Deprecated Model References ==="
grep -rn "claude-3-haiku\|gpt-3.5\|claude-2\b\|claude-instant\|claude-3-5-sonnet\b" \
  .claude/ CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null | grep -v ".git" | head -8 \
  || echo "  No deprecated model names found"

echo ""
echo "=== Config Freshness ==="
git log --oneline -1 --format="  Last commit: %ar (%h)" 2>/dev/null || echo "  (not a git repo)"

echo ""
echo "=== Cache Bug Workarounds ==="
# Bug 2 HIGH: --resume causes 87-118K token re-announcement
grep -rn "disableSkillShellExecution" ~/.claude/settings.json .claude/settings.json 2>/dev/null \
  | sed "s/^/  /" || echo "  disableSkillShellExecution: not set"

echo ""
echo "=== argument-hint Coverage (legacy commands) ==="
missing=0
for f in $(find .claude/commands -name "*.md" 2>/dev/null); do
  grep -q '\$ARGUMENTS' "$f" && ! grep -q "argument-hint" "$f" && {
    echo "  ⚠️  Missing argument-hint: $f"
    missing=$(( missing + 1 ))
  }
done
[ $missing -eq 0 ] && echo "  ✅ All commands using \$ARGUMENTS have argument-hint (skills use effort: field instead)"

echo ""
echo "=== Hook Profiles (env vars) ==="
grep -rn "CLAUDE_HOOK_PROFILE\|HOOK_PROFILE" .claude/ CLAUDE.md 2>/dev/null | head -3 | sed "s/^/  /" || echo "  No hook profiles configured"
```

评分（最高 10 分）：
- 无已弃用的模型名称：3 分
- 最近 90 天内有 Git 活动（或非 git 仓库）：2 分
- `disableSkillShellExecution: false` 或未使用 `--resume` 模式：3 分
- 所有使用 `$ARGUMENTS` 的命令都包含 `argument-hint:`：2 分

---

## 阶段 3 — 统一报告

按以下精确结构生成报告：

### 执行摘要

列出：
- **总分**：X/100
- **成熟度等级**：入门（<40） | 成长（40-59） | 稳健（60-79） | 优化（80+）
- **检测到的技术栈**：[来自阶段 1]
- **前 3 快速制胜**：最高 ROI 的缺口，每个可在 <15 分钟内修复
- **前 3 严重缺口**：最严重缺失项

### 维度评分卡

| # | 维度 | 得分 | 满分 | 状态 | 关键发现 |
|---|-----------|-------|-----|--------|-------------|
| 1 | 内存与上下文 | X | 20 | ✅/⚠️/❌ | 一行发现 |
| 2 | 规则健康度 | X | 10 | ✅/⚠️/❌ | 一行发现 |
| 3 | 技能质量 | X | 10 | ✅/⚠️/❌ | 一行发现 |
| 4 | 代理/命令质量 | X | 10 | ✅/⚠️/❌ | 一行发现 |
| 5 | 安全态势 | X | 20 | ✅/⚠️/❌ | 一行发现 |
| 6 | MCP 生态 | X | 10 | ✅/⚠️/❌ | 一行发现 |
| 7 | 工作流命令 | X | 10 | ✅/⚠️/❌ | 一行发现 |
| 8 | 新鲜度与最佳实践 | X | 10 | ✅/⚠️/❌ | 一行发现 |
| | **总计** | **X** | **100** | | |

状态阈值：✅ ≥80% 满分，⚠️ 50-79%，❌ <50%。

### 详细发现

按维度分组。对每个缺口（❌ 或 ⚠️）：

```
**[维度 N — 名称]**
缺口：[缺失或不佳的部分]
影响：[缺少它会导致什么损坏或降级]
修复：[具体操作及文件路径]
```

### 技术栈专属模板

最多提议 3 个模板，选择检测到的技术栈中影响最大的缺口。仅包含文件路径 + 初始内容。不要重复已有内容。

### 深化审计

列出未安装的审计技能及其能解锁的功能：

```
未安装的技能 — 安装以进行更深入的分析：

# token-audit（维度 1 — 增加规则分类、钩子开销分析）
mkdir -p ~/.claude/skills/token-audit
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/token-audit/SKILL.md \
  > ~/.claude/skills/token-audit/SKILL.md

# eval-rules（维度 2 — 增加 glob 验证、交互式审查）
mkdir -p ~/.claude/skills/eval-rules
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/eval-rules/SKILL.md \
  > ~/.claude/skills/eval-rules/SKILL.md

# eval-skills（维度 3 — 增加每项技能 14 分评分）
mkdir -p ~/.claude/skills/eval-skills
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/eval-skills/SKILL.md \
  > ~/.claude/skills/eval-skills/SKILL.md

# audit-agents-skills（维度 4 — 增加 A-F 等级、比较分析）
mkdir -p ~/.claude/skills/audit-agents-skills
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/audit-agents-skills/SKILL.md \
  > ~/.claude/skills/audit-agents-skills/SKILL.md

# security-check（维度 5 — 针对威胁数据库、55 个 CVE、24 种技术进行扫描）
mkdir -p ~/.claude/skills/security-check
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/security-check/SKILL.md \
  > ~/.claude/skills/security-check/SKILL.md

# 维度 1 的替代方案 — context-evaluator.ai
# 零安装 LLM 原生审计：17 个 AI 评估器用于 CLAUDE.md/AGENTS.md，
# 自动 .patch 修复。通过更深入的规则分析补充 /token-audit。
# 访问：https://context-evaluator.ai
```

---

## 阶段 4 — 确认请求

在呈现报告后，询问：

"是否实施前 3 项快速制胜？回复：
- **yes** → 我将全部实施
- **high** → 仅严重缺口（维度 5，以及维度 1 如果为 ❌）
- **1, 3** → 按编号指定发现中的具体项
- **none** → 保留报告，不做更改"

在采取任何操作前等待用户明确回复。
````

---

## 5. 预期结果

### 执行摘要示例

```
## 执行摘要

总分：52/100 — 成长

检测到的技术栈：TypeScript + Next.js + Prisma

前 3 快速制胜：
- 为 .env* 添加 permissions.deny（15 分钟）→ 修复维度 5 的严重缺口
- 安装 /investigate 和 /qa 命令（5 分钟）→ 维度 7 加 4 分
- 为 3 条始终启用的规则添加 paths: frontmatter（20 分钟）→ 减少固定上下文约 3K tokens

前 3 严重缺口：
1. ❌ 安全 — 无 permissions.deny，无 PreToolUse 钩子（0/20）
2. ⚠️ 内存 — 缺少项目 CLAUDE.md，全局为 22K tokens（8/20）
3. ❌ 工作流 — 3/5 核心命令缺失（4/10）
```

### 维度评分卡示例

| # | 维度 | 得分 | 满分 | 状态 | 关键发现 |
|---|-----------|-------|-----|--------|-------------|
| 1 | 内存与上下文 | 8 | 20 | ⚠️ | 22K 固定 tokens，无项目 CLAUDE.md |
| 2 | 规则健康度 | 7 | 10 | ⚠️ | 4 条规则，均无 paths: 字段 |
| 3 | 技能质量 | 8 | 10 | ✅ | 3 个技能，均有 effort + allowed-tools |
| 4 | 代理/命令质量 | 6 | 10 | ⚠️ | 8 个命令，2 个缺少 argument-hint |
| 5 | 安全态势 | 0 | 20 | ❌ | 无拒绝规则，无钩子 |
| 6 | MCP 生态 | 7 | 10 | ✅ | Context7 + Sequential 已配置 |
| 7 | 工作流命令 | 4 | 10 | ⚠️ | /investigate ✅ /qa ❌ /canary ❌ |
| 8 | 新鲜度与最佳实践 | 12 | 10 | — | 已达上限 |
| | **总计** | **52** | **100** | ⚠️ | |

---

## 6. 理解结果

### 术语表

| 术语 | 定义 |
|------|------------|
| **记忆文件** | 跨会话为 Claude 提供持久上下文的 CLAUDE.md 文件 |
| **上下文预算** | 任何任务开始前的总常驻 token 成本。阈值：绿色 <20K，黄色 20-40K，红色 >40K |
| **规则（自动加载）** | 每次会话启动时加载的 `.claude/rules/*.md` 文件。带有 `paths:` 的文件仅在读取匹配文件时加载 |
| **paths: frontmatter** | 规则 YAML 中将规则限定到特定文件模式的字段 — 减少常驻开销 |
| **评估技能** | 审计一个领域的专用技能：`eval-skills`、`eval-rules`、`token-audit`、`audit-agents-skills` |
| **单一事实来源** | 约定只文档化一次并通过 `@path` 引用的模式 |
| **工具 SEO** | 编写代理/命令描述使 Claude 自动选择正确工具 |
| **MCP 服务器** | 模型上下文协议 — 扩展 Claude 能力的外部工具。配置按项目存储在 `~/.claude.json` 中 |
| **钩子配置文件** | 钩子的 minimal/standard/strict 安全级别，通过环境变量切换（v3.38.0 新增） |
| **PreToolUse** | 在 Claude 执行工具之前触发的钩子 — 用于安全检查和审批门控 |
| **effort: 字段** | 技能 frontmatter 中 low/medium/high 复杂度的信号 — Claude 用于分配思考预算 |
| **argument-hint** | Frontmatter 字段，在使用 `$ARGUMENTS` 的命令的斜杠命令菜单中显示占位文本 |
| **威胁数据库** | `examples/skills/update-threat-db/threat-db.yaml` — 55 个 CVE、24 种攻击技术、最小安全版本 |
| **缓存缺陷 #40524** | 缺陷 2（高）：`--resume` 导致完整上下文重新声明（每次恢复重建 87-118K tokens） |
| **范围漂移** | PR 更改了计划意图之外的文件。通过比较 `~/.claude/plans/` 与 `git diff --stat` 检测 |
| **修复优先启发式** | 审查模式：自动修复机械性问题，安全/设计决策需人工判断 |
| **LLM 输出信任边界** | 针对 AI 生成的值在未经格式验证时写入数据库的审查类别 |
| **managed-settings.d/** | 企业级政策目录，用于覆盖用户设置的管理规则（v2.1.83 新增） |
| **Routines** | 云端托管定时任务，3 种触发类型：定时、API、GitHub 事件（2026 年 4 月发布） |
| **上下文区域** | <70% 最佳，75% 自动压缩触发，85% 建议移交 |
| **沙箱** | 操作系统级隔离（Docker 容器或原生进程级）。在 settings.json 中配置 |
| **铁律** | 调试原则：没有根因调查就没有修复。参见 `/investigate` |

### 分数阈值

| 分数 | 等级 | 含义 |
|-------|------|----------------|
| 80-100 | 优化 | 配置稳固。关注新鲜度和边缘情况 |
| 60-79 | 稳健 | 基础良好。填补 ⚠️ 维度 |
| 40-59 | 成长 | 核心部分存在但有若干缺口。遵循快速制胜 |
| <40 | 入门 | 从维度 5（安全）和维度 1（内存）开始 |

### 状态图标

| 图标 | 含义 |
|------|---------|
| ✅ | ≥80% 该维度满分 |
| ⚠️ | 50-79% 该维度满分 |
| ❌ | <50% 该维度满分 |

---

## 7. 常见问题

### "审计技能未安装"

**原因**：专用技能是可选的，默认并非全局可用。

**后果**：提示词对该维度以回退模式运行。分数上限较低（某些维度为 8 分而非 10 分）。结果仍可操作，只是不够详细。

**修复**：使用报告中"深化审计"部分的安装命令。每个技能约需 1 分钟安装，可立即改善未来的审计。

### "Claude 未找到我的文件"

**原因**：工作目录错误或平台路径差异。

**修复**：
- 确保在项目根目录运行 `claude`
- 在 Windows 上，路径使用 `%USERPROFILE%\.claude\` 而非 `~/.claude/`

### "分数似乎不对"

**原因**：回退模式评分已简化 — 无法验证 glob 有效性、运行 14 分技能检查或针对威胁数据库进行扫描。

**修复**：安装相关的审计技能（参见"深化审计"）。重新运行以获得准确的维度分数。

### "推荐太多"

**原因**：首次审计一个没有 Claude Code 配置的项目。

**修复**：使用执行摘要中的快速制胜。先实施那三项。重新审计。逐步构建。

### "Claude 未经询问就做了更改"

**原因**：阶段 4 的确认未被执行或被跳过。

**修复**：确保复制了包含阶段 4 的完整提示词。在粘贴前使用计划模式（`Shift+Tab` 两次）以获得额外安全性。

---

## 8. 相关资源

**补充审计工具**（深入特定维度）：

| 工具 | 维度 | 安装 |
|------|-----------|---------|
| `/token-audit` | 内存与上下文 | `mkdir -p ~/.claude/skills/token-audit && curl -sL .../examples/skills/token-audit/SKILL.md > ...` |
| `/eval-rules` | 规则健康度 | 同上 |
| `/eval-skills` | 技能质量 | 同上 |
| `/audit-agents-skills` | 代理/命令 | 同上 |
| `/security-check` | 安全态势（快速，约 30 秒） | `mkdir -p ~/.claude/skills/security-check && curl -sL ...` |
| `/security-audit` | 安全态势（完整，2-5 分钟，满分 /100） | 同上 |
| [`tools/context-audit-prompt.md`](context-audit-prompt.md) | 深入上下文工程 | 自包含提示词，无需安装 |
| [`tools/onboarding-prompt.md`](onboarding-prompt.md) | 从零开始设置 | 自包含提示词，无需安装 |
| [context-evaluator.ai](https://context-evaluator.ai) | 内存与上下文（替代方案）— LLM 原生、17 个评估器、自动 `.patch` | 零安装网页工具 |

**参考文档**：
- [The Ultimate Claude Code 指南](../guide/ultimate-guide.md) — 完整参考
- [速查表](../guide/cheatsheet.md) — 快速日常参考
- [安全加固](../guide/security/security-hardening.md) — 生产安全模式
- [上下文工程](../guide/core/architecture.md) — token 预算策略
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code) — Anthropic 文档

**用于 CI/CD 集成**（JSON 输出、批处理模式）：[`examples/scripts/audit-scan.sh`](../examples/scripts/audit-scan.sh)

---

*版本 5.2（指南 v3.41.0+）| v5.2：针对 CC 2.1.3 技能-命令统一更新了技能检测 — 维度 4/7/8 的 bash 现在同时检查 `.claude/skills/` 和 `.claude/commands/`；security-check 安装路径已修正为标准 SKILL.md。v5.1：新增 context-evaluator.ai。v5.0：从清单重构为编排器，具备 8 个加权维度。*
