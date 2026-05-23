---
name: security-check
description: 对照已知威胁数据库快速检查配置安全
argument-hint: "[path]"
effort: low
disable-model-invocation: true
---

# 安全检查

对照已知威胁数据库快速检查配置安全。验证你的 Claude Code 设置中是否存在已知的恶意技能、有漏洞的 MCP、危险模式和暴露的密钥。

**时间**：约 30 秒 | **范围**：仅 Claude Code 配置

## 使用说明

你是安全分析师。对照绑定在 `examples/skills/update-threat-db/threat-db.yaml` 的威胁情报数据库检查用户的 Claude Code 配置。生成简洁、可操作的报告。

### 阶段 1：加载威胁数据库

读取本仓库中的 `examples/skills/update-threat-db/threat-db.yaml` 以加载：
- 已知的恶意作者和技能
- MCP 服务器的 CVE 数据库
- 钩子、agent 和配置的可疑模式

### 阶段 2：MCP 服务器审计

读取用户的 MCP 配置：

```bash
# 全局 MCP 配置
cat ~/.claude.json 2>/dev/null | jq '.mcpServers // empty'

# 项目 MCP 配置
cat .mcp.json 2>/dev/null
```

**对照 threat-db.yaml 检查：**
- [ ] 是否有 MCP 服务器匹配 CVE 条目？→ 严重
- [ ] 版本锁定：所有 MCP 服务器是否锁定到确切版本（非 `@latest`）？→ 高（如未锁定）
- [ ] MCP 参数中是否包含 `--dangerous-*` 标志？→ 严重
- [ ] 是否有 MCP 服务器不在安全列表中？→ 中（标记人工审查）

### 阶段 3：技能和 Agent 审计

```bash
# 列出已安装的技能
ls -la .claude/skills/ 2>/dev/null
ls -la ~/.claude/skills/ 2>/dev/null

# 列出 agent
ls -la .claude/agents/ 2>/dev/null
ls -la ~/.claude/agents/ 2>/dev/null

# 检查 agent 的 tools 字段
grep -r "^tools:" .claude/agents/ 2>/dev/null
grep -r "^tools:" ~/.claude/agents/ 2>/dev/null
```

**对照 threat-db.yaml 检查：**
- [ ] 技能/agent 名称匹配 `malicious_skills` 条目？→ 严重
- [ ] 技能/agent 作者匹配 `malicious_authors` 条目？→ 严重
- [ ] 任何 agent 仅有 `tools: Bash`？→ 高
- [ ] 任何 agent 工具访问权限过宽且描述模糊？→ 中

### 阶段 4：钩子安全

```bash
# 列出所有钩子
find .claude/hooks/ -type f 2>/dev/null
find ~/.claude/hooks/ -type f 2>/dev/null

# 扫描钩子中的可疑模式
grep -rn "curl\|wget\|nc \|ncat\|netcat\|base64\|eval\|exec\|/dev/tcp\|/dev/udp" .claude/hooks/ 2>/dev/null
grep -rn "curl\|wget\|nc \|ncat\|netcat\|base64\|eval\|exec\|/dev/tcp\|/dev/udp" ~/.claude/hooks/ 2>/dev/null

# 检查钩子中的凭据访问
grep -rn "ssh\|id_rsa\|id_ed25519\|\.env\|credentials\|secret\|password\|token\|api.key" .claude/hooks/ 2>/dev/null
grep -rn "ssh\|id_rsa\|id_ed25519\|\.env\|credentials\|secret\|password\|token\|api.key" ~/.claude/hooks/ 2>/dev/null
```

**对照 threat-db.yaml `suspicious_patterns.hooks` 检查：**
- [ ] 网络调用（`curl`、`wget`）→ 高
- [ ] 反向 shell 指示器（`nc`、`/dev/tcp`）→ 严重
- [ ] 凭据访问（`ssh`、`.env`、`password`）→ 严重
- [ ] Base64 编码 → 中（审查上下文）

### 阶段 5：内存投毒检查

```bash
# 检查配置中的可疑指令
grep -in "ignore\|forget\|override\|disregard\|you are now\|new role\|system prompt" \
  CLAUDE.md .claude/CLAUDE.md SOUL.md .claude/SOUL.md MEMORY.md .claude/MEMORY.md \
  ~/.claude/CLAUDE.md ~/.claude/MEMORY.md 2>/dev/null
```

- [ ] CLAUDE.md / SOUL.md / MEMORY.md 中存在 prompt 注入模式？→ 高
- [ ] 有指令要求禁用安全功能、跳过审查或授予过宽权限？→ 严重

### 阶段 6：权限和设置

```bash
# 检查设置
cat .claude/settings.json 2>/dev/null
cat ~/.claude/settings.json 2>/dev/null
```

- [ ] `permissions.deny` 存在并覆盖 `.env*`、`*.pem`、`*.key`、secrets？→ 中（如缺失）
- [ ] 没有通配符 `permissions.allow` 用于 Bash 或 Write？→ 高（如存在）
- [ ] 没有 `dangerouslySkipPermissions` 或类似标志？→ 严重（如存在）

### 阶段 7：配置中暴露的密钥

```bash
# 检查 .claude/ 目录中的密钥
grep -rn "sk-[a-zA-Z0-9]\{20,\}\|sk-ant-[a-zA-Z0-9]\{20,\}\|ghp_[a-zA-Z0-9]\{36\}\|AKIA[A-Z0-9]\{16\}" \
  .claude/ ~/.claude/ 2>/dev/null

# 检查私钥
grep -rn "BEGIN.*PRIVATE KEY" .claude/ ~/.claude/ 2>/dev/null
```

- [ ] 配置文件中存在 API 密钥或 token？→ 严重
- [ ] 配置中存在私钥？→ 严重

## 输出格式

```
## 🛡️ 安全检查报告

**日期**：[时间戳]
**范围**：Claude Code 配置

### 结果摘要

| 严重性 | 数量 | 状态 |
|----------|-------|--------|
| 🔴 严重 | X | [通过/未通过] |
| 🟠 高 | X | [通过/未通过] |
| 🟡 中 | X | [通过/未通过] |
| 🟢 低 | X | [通过/未通过] |

### 🔴 严重问题
[列出每个严重发现的位置和修复]

### 🟠 高优先级问题
[列出每个高优先级发现的位置和修复]

### 🟡 中优先级问题
[列出每个中优先级发现的位置和修复]

### ✅ 通过的检查
[列出通过的项——对建立信心很重要]

### 🔧 建议的操作（按优先级）
1. [最紧急的修复及确切命令]
2. [第二优先级]
3. [...]

### 📚 参考
- 完整安全指南：guide/security-hardening.md
- 威胁数据库：examples/skills/update-threat-db/threat-db.yaml
- MCP 扫描：`npx mcp-scan`（Snyk）
```

如果所有检查均通过，输出：

```
## 🛡️ 安全检查报告 — 全部通过 ✅

**日期**：[时间戳]
在您的 Claude Code 配置中未检测到已知威胁。

**对持续安全的建议：**
- 安装新技能或 MCP 服务器后重新运行 `/security-check`
- 运行 `/security-audit` 进行全面项目和配置审计
- 保持 Claude Code 更新（当前安全修复在 v2.1.34+）
```

$ARGUMENTS
