---
name: security
description: 针对 OWASP Top 10 漏洞的快速安全评估
argument-hint: "[path] [--depth quick|full]"
effort: medium
disable-model-invocation: true
---

# 安全快速审计

针对 OWASP Top 10 漏洞的快速安全评估。

## 目的

执行快速安全扫描，识别常见漏洞：
- 硬编码的密钥和凭据
- SQL 注入风险
- XSS 漏洞
- 不安全的依赖
- 认证/授权问题

## 使用说明

### 步骤 1：密钥扫描

```bash
# 常见密钥模式
grep -rn --include="*.{js,ts,py,go,java,rb,php,env}" \
  -E "(password|secret|api_key|apikey|token|auth|credential).*[=:].*['\"][^'\"]{8,}['\"]" \
  --exclude-dir={node_modules,vendor,.git,dist,build} . 2>/dev/null | head -20

# 可能被提交的 .env 文件
find . -name ".env*" -not -path "*/node_modules/*" -type f 2>/dev/null

# 检查密钥是否在 gitignore 中
[ -f ".gitignore" ] && grep -q "\.env" .gitignore && echo "✅ .env 在 .gitignore 中" || echo "⚠️ .env 不在 .gitignore 中"
```

### 步骤 2：注入漏洞

```bash
# SQL 注入模式（使用字符串拼接的原始查询）
grep -rn --include="*.{js,ts,py,go,java,php}" \
  -E "(query|execute|raw|sql).*\+.*\$|f['\"].*SELECT|\.format\(.*SELECT" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -15

# 命令注入模式
grep -rn --include="*.{js,ts,py,go,rb,php}" \
  -E "(exec|spawn|system|shell_exec|popen)\s*\(" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -15
```

### 步骤 3：XSS 模式

```bash
# 危险的 innerHTML/dangerouslySetInnerHTML 使用
grep -rn --include="*.{js,ts,jsx,tsx,vue}" \
  -E "(innerHTML|dangerouslySetInnerHTML|v-html)" \
  --exclude-dir={node_modules,.git,dist} . 2>/dev/null | head -15

# HTML 上下文中未转义的模板字面量
grep -rn --include="*.{js,ts,jsx,tsx}" \
  -E "\`.*\$\{.*\}.*<" \
  --exclude-dir={node_modules,.git,dist} . 2>/dev/null | head -10
```

### 步骤 4：依赖检查

```bash
# 检查 npm 包中的已知漏洞
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '{vulnerabilities: .metadata.vulnerabilities}' 2>/dev/null

# 检查有安全问题的过时包
[ -f "package.json" ] && npm outdated --json 2>/dev/null | jq 'to_entries | map(select(.value.current != .value.latest)) | length' 2>/dev/null
```

### 步骤 5：认证和会话问题

```bash
# 硬编码的 JWT 密钥
grep -rn --include="*.{js,ts,py,go}" \
  -E "(jwt|JWT).*secret.*[=:].*['\"].{8,}['\"]" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null

# 缺少 CSRF 保护模式
grep -rn --include="*.{js,ts,py}" \
  -E "(POST|PUT|DELETE|PATCH).*fetch|axios\.(post|put|delete|patch)" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

## 输出格式

---

### 🛡️ 安全审计报告

**扫描日期**：[时间戳]
**范围**：[扫描的目录]

### 🔴 严重问题

| 问题 | 位置 | 描述 |
|-------|----------|-------------|
| [类型] | [file:line] | [简要描述] |

### 🟠 高严重性

| 问题 | 位置 | 建议 |
|-------|----------|----------------|
| [类型] | [file:line] | [修复建议] |

### 🟡 中严重性

| 问题 | 位置 | 说明 |
|-------|----------|------|
| [类型] | [file:line] | [上下文] |

### 📊 总结

- **严重**：X 个
- **高**：X 个
- **中**：X 个
- **依赖**：X 个漏洞

### 🔧 快速修复

1. [最高优先级的修复及命令/代码]
2. [第二优先级]
3. [第三优先级]

---

## 严重性级别

| 级别 | 示例 | 操作 |
|-------|----------|--------|
| 🔴 严重 | 硬编码的生产密钥、SQL 注入 | 立即修复 |
| 🟠 高 | 缺少认证、XSS 向量 | 部署前修复 |
| 🟡 中 | 过时的依赖、缺少 CSRF | 计划修复 |
| 🟢 低 | 最佳实践违规 | 跟踪改进 |

## 用法

**完整审计：**
```
/security
```

**关注特定领域：**
```
/security auth
/security deps
/security injection
```

**特定文件/目录：**
```
/security src/api/
```

## 说明

- 此扫描为启发式快速扫描，非全面安全审计
- 生产系统请配合专用工具使用（Snyk、SonarQube、OWASP ZAP）
- 可能存在误报——请手动验证发现
- 参见 `examples/hooks/security-hooks.sh` 了解自动化的提交前安全检查

$ARGUMENTS
