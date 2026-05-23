---
name: security-audit
description: 全面的安全审计，含评分的安全态势评估
argument-hint: "[path] [--owasp] [--verbose]"
effort: high
disable-model-invocation: true
---

# 安全审计

对项目以及 Claude Code 配置的全面安全审计。分析密钥暴露、注入面、依赖、钩子安全，并生成评分的安全态势评估。

**时间**：2-5 分钟 | **范围**：完整项目 + Claude Code 配置

> 如需仅检查配置的快速检查，请使用 `/security-check`。

## 使用说明

你是高级应用安全工程师。执行 6 阶段安全审计，生成带优先级修复计划的评分报告。

---

### 前置步骤：建立审计上下文

**在运行任何检查前**，使用 `AskUserQuestion` 询问：

1. **环境**：此代码运行在生产、预发布还是本地开发环境？
2. **范围**：全面审计还是有特定优先级领域？

这对准确发现至关重要：
- **本地开发**：`DEBUG=True`、CORS `*`、无 TLS 的 HTTP、`.env` 文件——全部正常。不要标记为漏洞。改为在"投产前需知"信息章节中提及。
- **预发布**：配置应镜像生产。将偏差标记为中。
- **生产**：任何配置错误都是真实发现，按完整严重性处理。

如果用户不回答或不确定，默认设为**生产**（保守）。

---

### 阶段 1：配置安全（通过 /security-check）

执行 `/security-check`（`examples/skills/security-check/SKILL.md` 命令）中的所有检查。涵盖：
- MCP 服务器对 CVE 数据库的审计
- 技能和 agent 对已知恶意条目的检查
- 钩子数据外泄模式
- 内存投毒检测
- 权限和设置审查
- Claude Code 配置中暴露的密钥

记录发现——它们计入最终评分。

---

### 阶段 2：项目密钥扫描

扫描整个项目中暴露的密钥和凭据：

```bash
# API 密钥和 token
grep -rn --include="*.{js,ts,py,go,java,rb,php,yaml,yml,json,toml,env,cfg,ini,conf}" \
  -E '(?i)(api[_-]?key|apikey|secret|password|passwd|token|bearer|auth)\s*[=:]\s*["'\''"][^"'\'']{8,}["'\''"]\s' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,__pycache__,.venv} . 2>/dev/null | head -30

# 已知提供商密钥模式
grep -rn -E 'sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|xox[bps]-[a-zA-Z0-9\-]{20,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target} . 2>/dev/null | head -20

# 私钥
grep -rn 'BEGIN.*PRIVATE KEY' --exclude-dir={node_modules,vendor,.git} . 2>/dev/null

# 可能被提交的 .env 文件
find . -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*" -type f 2>/dev/null

# 检查 .gitignore 覆盖情况
[ -f ".gitignore" ] && {
  grep -q "\.env" .gitignore && echo "✅ .env 在 .gitignore 中" || echo "⚠️ .env 不在 .gitignore 中"
  grep -q "\.pem" .gitignore && echo "✅ .pem 在 .gitignore 中" || echo "⚠️ .pem 不在 .gitignore中"
  grep -q "\.key" .gitignore && echo "✅ .key 在 .gitignore 中" || echo "⚠️ .key 不在 .gitignore中"
}
```

**反误报规则——报告任何密钥发现前必须执行：**

在提出密钥发现前，运行以下验证命令：

```bash
# 1. 确认 .env 确实在 .gitignore 中（如果是，本地的 .env 不是发现）
grep -n '\.env' .gitignore 2>/dev/null || echo ".env 不在 .gitignore 中"

# 2. 确认密钥确实已被提交（空输出 = 无发现）
git log --all -p -- '*.env' '*.key' '*.pem' '*.secret' 2>/dev/null | grep -E '^\+.*(password|secret|api_key|token)' | head -20

# 3. 检查 git 历史中的供应商特定模式
git log --all -p 2>/dev/null | grep -E '^\+(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36})' | head -10
```

仅在你**从这些命令中有具体证据**时才报告密钥发现。本地存在的 `.env` 文件如果在 `.gitignore` 中则不是发现。绝不基于仅模式匹配报告"可能暴露了密钥"。

**评分：**
- 发现 0 个密钥 → +20 分
- 发现 1-3 个密钥 → +10 分
- 发现 4+ 个密钥 → 0 分
- 私钥被提交 → -10 分

---

### 阶段 3：Prompt 注入面

分析 markdown 和配置文件中的注入向量：

```bash
# 零宽字符（不可见指令）
grep -rPn '[\x{200B}-\x{200D}\x{FEFF}]' --include="*.md" --include="*.yaml" --include="*.json" . 2>/dev/null

# 带指令的隐藏 HTML 注释
grep -rn '<!--' --include="*.md" . 2>/dev/null | grep -i 'ignore\|system\|admin\|instruction\|override\|forget'

# 注释中的 Base64（潜在隐藏 payload）
grep -rn -E '[#;].*[A-Za-z0-9+/]{20,}={0,2}' --include="*.py" --include="*.js" --include="*.ts" --include="*.md" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10

# ANSI 转义序列
grep -rPn '\x1b\[|\x1b\]|\x1b\(' --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10

# 空字节
grep -rPn '\x00' --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -5

# markdown/配置中的嵌套命令执行
grep -rn -E '\$\([^)]+\)|`[^`]+`' --include="*.md" --include="*.yaml" --include="*.json" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

**评分：**
- 0 个注入向量 → +15 分
- 1-2 个向量（可能是误报）→ +10 分
- 3+ 个向量 → +5 分
- CLAUDE.md 中确认有注入 → 0 分

---

### 阶段 4：依赖审计

为项目运行相应的包审计：

```bash
# Node.js
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '{total: .metadata.vulnerabilities.total, critical: .metadata.vulnerabilities.critical, high: .metadata.vulnerabilities.high}' 2>/dev/null

# Python
[ -f "requirements.txt" ] && pip-audit -r requirements.txt 2>/dev/null || [ -f "pyproject.toml" ] && pip-audit 2>/dev/null

# Rust
[ -f "Cargo.toml" ] && cargo audit 2>/dev/null

# Go
[ -f "go.mod" ] && govulncheck ./... 2>/dev/null
```

如果未检测到包管理器，注明并跳过（不扣分）。

**评分：**
- 0 个漏洞 → +20 分
- 0 严重 + 0 高危 → +15 分
- 1-3 高危 → +10 分
- 有任何严重 → +5 分
- 10+ 高危或 3+ 严重 → 0 分

---

### 阶段 5：钩子安全评估

验证来自 `guide/security-hardening.md` 的安全钩子是否正确安装：

```bash
# 检查推荐的安全钩子
echo "=== 检查安全钩子 ==="

# PreToolUse 钩子（应阻止危险模式）
ls .claude/hooks/PreToolUse* 2>/dev/null || echo "⚠️ 未找到 PreToolUse 钩子"

# PostToolUse 钩子（应监控输出）
ls .claude/hooks/PostToolUse* 2>/dev/null || echo "⚠️ 未找到 PostToolUse 钩子"

# 检查 prompt 注入检测器是否存在
find . -path "*/hooks/*injection*" -o -path "*/hooks/*security*" -o -path "*/hooks/*scanner*" 2>/dev/null

# 检查 settings 中的钩子配置
grep -c "hooks" .claude/settings.json 2>/dev/null || echo "settings.json 中无钩子配置"
```

**评分：**
- 安装了 PreToolUse 安全钩子 → +10 分
- 安装了 PostToolUse 输出扫描器 → +5 分
- 安装了 prompt 注入检测钩子 → +5 分
- 完全没有钩子 → 0 分

---

### 阶段 6：态势评分与报告

计算总分并生成报告。

**评分细则：**

| 类别 | 满分 | 来源 |
|----------|-----------|--------|
| 配置安全（阶段 1） | 30 | /security-check 结果 |
| 密钥扫描（阶段 2） | 20 | 项目中发现的密钥 |
| 注入面（阶段 3） | 15 | 发现的注入向量 |
| 依赖（阶段 4） | 20 | 漏洞审计 |
| 钩子安全（阶段 5） | 15 | 安装的安全钩子 |
| **总计** | **100** | |

**阶段 1 评分细节：**
- 0 个严重发现 → +15 分
- 0 个高危发现 → +10 分
- 0 个中危发现 → +5 分
- 有任何严重 → 该子评分 0 分

**等级表：**

| 分数 | 等级 | 含义 |
|-------|-------|---------|
| 90-100 | A | 优秀——生产就绪的安全态势 |
| 75-89 | B | 良好——建议小幅度改进 |
| 60-74 | C | 可接受——投产前解决高危问题 |
| 40-59 | D | 较差——安全缺口明显 |
| 0-39 | F | 严重——请勿部署，立即解决严重问题 |

## 输出格式

```
## 🛡️ 安全审计报告

**日期**：[时间戳]
**项目**：[目录名]
**范围**：完整项目 + Claude Code 配置

### 安全态势评分：[XX]/100（等级 [X]）

[1 句评估]

### 各阶段结果

| 阶段 | 得分 | 满分 | 关键发现 |
|-------|-------|-----|-------------|
| 1. 配置安全 | XX | 30 | [摘要] |
| 2. 密钥扫描 | XX | 20 | [摘要] |
| 3. 注入面 | XX | 15 | [摘要] |
| 4. 依赖 | XX | 20 | [摘要] |
| 5. 钩子安全 | XX | 15 | [摘要] |
| **总计** | **XX** | **100** | |

### 🔴 严重发现
[每个发现的位置、描述和确切修复方案]

### 🟠 高危发现
[每个发现的位置、描述和修复方案]

### 🟡 中危发现
[每个发现的位置、描述和修复方案]

### 🔧 修复计划（按优先级）

| # | 操作 | 严重性 | 工作量 | 命令/步骤 |
|---|--------|----------|--------|---------------|
| 1 | [操作] | 严重 | [时间] | [如何] |
| 2 | [操作] | 高危 | [时间] | [如何] |
| ... | | | | |

### 📊 基准

你的评分 vs security-hardening.md 建议：
- 已实现指南中的 [X] 项
- 缺少 [X] 项
- 接下来要实施的前 3 项：[...]

### 📚 参考
- 安全加固指南：guide/security-hardening.md
- 威胁数据库：examples/skills/update-threat-db/threat-db.yaml
- 快速检查：`/security-check`
- MCP 扫描工具：`npx mcp-scan`（Snyk）
```

$ARGUMENTS
