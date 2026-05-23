---
name: audit-codebase
description: 代码库健康审计，7 个类别评分并生成改进计划
argument-hint: "[path] [--focus security|performance|quality]"
effort: medium
disable-model-invocation: true
---

# 代码库健康审计

在 7 个健康类别上给你的代码库评分，识别薄弱环节，并生成按优先级排序的改进计划。每个类别按 1-10 分评分，附带具体且可操作的发现。

**时间**：3-8 分钟（取决于代码库大小）| **范围**：完整项目

## 使用说明

你是高级工程顾问，负责执行代码库健康评估。在所有 7 个类别上分析项目（如果 `$ARGUMENTS` 指定了类别则分析子集），对每个类别评分，并生成改进计划。

如果 `$ARGUMENTS` 包含类别名称（如"secrets security tests"），仅审计这些类别。否则，审计全部 7 个。

---

### 类别 1：密钥（权重：15%）

扫描代码中硬编码的凭据、API 密钥和敏感数据。

```bash
# 代码中的 API 密钥和 token
grep -rn --include="*.{js,ts,py,go,java,rb,php,yaml,yml,json,toml,env,cfg,ini,conf}" \
  -E '(?i)(api[_-]?key|apikey|secret[_-]?key|password|passwd|token|bearer)\s*[=:]\s*["'\''"][^"'\'']{8,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,__pycache__,.venv} . 2>/dev/null | head -20

# 已知提供商模式
grep -rn -E 'sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|xox[bps]-[a-zA-Z0-9\-]{20,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target} . 2>/dev/null | head -10

# 已提交的 .env 文件
find . -name ".env*" -not -name ".env.example" -not -path "*/node_modules/*" -not -path "*/.git/*" -type f 2>/dev/null

# .gitignore 覆盖情况
[ -f ".gitignore" ] && {
  for pattern in ".env" "*.pem" "*.key" "*.p12"; do
    grep -q "$pattern" .gitignore 2>/dev/null && echo "OK：$pattern 在 .gitignore 中" || echo "缺失：$pattern 不在 .gitignore 中"
  done
}
```

**评分：**
- 10：零密钥，.gitignore 覆盖所有敏感模式，.env.example 存在
- 7-9：代码中无密钥，.gitignore 有少量缺口
- 4-6：发现 1-3 个潜在密钥（可能是误报），或 .env 被提交
- 1-3：代码中有多个密钥，私钥被提交，无 .gitignore 保护

---

### 类别 2：安全（权重：15%）

检查 OWASP 风格的漏洞和不安全模式。

```bash
# SQL 注入模式
grep -rn --include="*.{js,ts,py,java,go,rb,php}" \
  -E '(query|execute|exec)\s*\(\s*[`"'\''"].*\+|\$\{|%s|\.format\(' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,test,__test__} . 2>/dev/null | head -15

# eval/exec 使用
grep -rn -E '\b(eval|exec|execSync|Function\(|setTimeout\([^,]*[+`]|setInterval\([^,]*[+`])' \
  --include="*.{js,ts,py}" --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -10

# 不安全反序列化
grep -rn -E '(pickle\.loads|yaml\.load\(|JSON\.parse\(.*user|unserialize\()' \
  --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -10

# 路由/端点缺少输入验证
grep -rn -E '(app\.(get|post|put|delete|patch)|router\.(get|post|put|delete))' \
  --include="*.{js,ts}" --exclude-dir={node_modules,.git,dist} . 2>/dev/null | wc -l
```

**评分：**
- 10：无注入模式、无 eval/exec、所有端点有输入验证、CSP 头部
- 7-9：小问题（非面向用户代码中有 1-2 处 eval 使用）
- 4-6：一些注入模式、多个端点缺少验证
- 1-3：存在 SQL 注入风险、eval 使用用户输入、无输入消毒

---

### 类别 3：依赖（权重：15%）

审计包健康、已知 CVE 和更新程度。

```bash
# Node.js 审计
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities' 2>/dev/null
[ -f "package.json" ] && npx npm-check 2>/dev/null | tail -20

# Python
[ -f "requirements.txt" ] && pip-audit -r requirements.txt 2>/dev/null | tail -20
[ -f "pyproject.toml" ] && pip-audit 2>/dev/null | tail -20

# Rust
[ -f "Cargo.toml" ] && cargo audit 2>/dev/null | tail -20

# Go
[ -f "go.mod" ] && govulncheck ./... 2>/dev/null | tail -20

# 锁定文件存在性
for lockfile in package-lock.json yarn.lock pnpm-lock.yaml Cargo.lock go.sum poetry.lock; do
  [ -f "$lockfile" ] && echo "OK：$lockfile 存在"
done
[ ! -f "package-lock.json" ] && [ ! -f "yarn.lock" ] && [ ! -f "pnpm-lock.yaml" ] && [ -f "package.json" ] && echo "缺失：Node.js 项目无锁定文件"
```

**评分：**
- 10：零 CVE、锁定文件存在、所有依赖不超过 6 个月
- 7-9：无严重/高危 CVE、少量过时包
- 4-6：1-3 个高危 CVE，或 >50% 依赖过时一年以上
- 1-3：严重 CVE、无锁定文件、依赖已废弃

---

### 类别 4：结构（权重：10%）

评估文件组织、命名约定和模块边界。

```bash
# 每个顶级目录的文件数
for dir in */; do
  [ -d "$dir" ] && [ "$dir" != "node_modules/" ] && [ "$dir" != ".git/" ] && [ "$dir" != "vendor/" ] && \
    echo "$dir：$(find "$dir" -type f -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l) 个文件"
done

# 深度嵌套文件（复杂度指标）
find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -mindepth 6 2>/dev/null | head -10

# 混合命名约定
find . -type f -name "*_*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -5
find . -type f -name "*-*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -5

# 循环依赖指示器（JS/TS 项目）
[ -f "package.json" ] && npx madge --circular --extensions ts,js src/ 2>/dev/null | head -20
```

**评分：**
- 10：清晰的模块边界、一致的命名、无循环依赖、扁平层次
- 7-9：结构良好，有少量不一致
- 4-6：混合约定、一些循环依赖、模块边界不清晰
- 1-3：无清晰结构、文件嵌套过深、循环依赖普遍

---

### 类别 5：测试（权重：15%）

评估测试覆盖率、测试质量和测试实践。

```bash
# 测试文件数 vs 源文件数
TEST_COUNT=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -path "*/test/*" -o -path "*/__tests__/*" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
SRC_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.java" \) \
  -not -name "*.test.*" -not -name "*.spec.*" -not -name "test_*" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" 2>/dev/null | wc -l)
echo "测试文件：$TEST_COUNT | 源文件：$SRC_COUNT | 比例：$(echo "scale=2; $TEST_COUNT / ($SRC_COUNT + 1)" | bc)"

# 覆盖率配置存在性
for cfg in jest.config.* vitest.config.* .nycrc .coveragerc pytest.ini setup.cfg; do
  [ -f "$cfg" ] && echo "OK：$cfg 存在"
done

# 覆盖率报告（如可用）
[ -d "coverage" ] && [ -f "coverage/coverage-summary.json" ] && cat coverage/coverage-summary.json | jq '.total' 2>/dev/null

# 快照测试数（潜在维护负担）
find . -name "*.snap" -not -path "*/node_modules/*" 2>/dev/null | wc -l
```

**评分：**
- 10：测试比例 >0.8、覆盖率 >80%、CI 运行测试、无陈旧快照
- 7-9：测试比例 >0.5、覆盖率 >60%、覆盖率配置存在
- 4-6：存在一些测试但缺口明显、无覆盖率跟踪
- 1-3：测试比例 <0.2 或完全没有测试

---

### 类别 6：导入（权重：10%）

检查未使用的导入、循环依赖和类型覆盖率。

```bash
# 未使用的导入（TypeScript/JavaScript）
[ -f "tsconfig.json" ] && npx tsc --noEmit 2>&1 | grep -c "declared but" 2>/dev/null
[ -f "tsconfig.json" ] && npx tsc --noEmit 2>&1 | grep "declared but" | head -10

# TypeScript 严格模式
[ -f "tsconfig.json" ] && grep -E '"strict"|"noImplicitAny"|"strictNullChecks"' tsconfig.json 2>/dev/null

# Python 未使用的导入
[ -f "pyproject.toml" ] || [ -f "setup.py" ] && python -m pyflakes . 2>/dev/null | grep "imported but unused" | head -10

# 通配符导入（代码异味）
grep -rn 'import \*' --include="*.{py,ts,js}" --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

**评分：**
- 10：零未使用导入、TypeScript 严格模式、无通配符导入
- 7-9：<5 个未使用导入、启用严格模式但有少量缺口
- 4-6：5-20 个未使用导入、无严格模式、一些通配符导入
- 1-3：>20 个未使用导入、通配符导入普遍、无类型检查

---

### 类别 7：AI 模式（权重：20%）

评估 Claude Code 配置成熟度和 AI 辅助开发就绪度。

```bash
# CLAUDE.md 存在性和质量
[ -f "CLAUDE.md" ] && echo "OK：CLAUDE.md 存在（$(wc -l < CLAUDE.md) 行）" || echo "缺失：无 CLAUDE.md"
[ -f ".claude/settings.json" ] && echo "OK：.claude/settings.json 存在" || echo "缺失：无 .claude/settings.json"

# 自定义命令
COMMANDS=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l)
echo "自定义命令：$COMMANDS"

# 钩子
HOOKS_CFG=$(grep -c "hooks" .claude/settings.json 2>/dev/null || echo "0")
echo "钩子配置数：$HOOKS_CFG"

# 规则文件
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | wc -l)
echo "规则文件数：$RULES"

# Agents
AGENTS=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
echo "Agent 定义数：$AGENTS"

# Skills
SKILLS=$(find .claude/skills -name "*.md" 2>/dev/null | wc -l)
echo "技能数：$SKILLS"

# .gitignore 中 AI 相关模式
grep -q "claude" .gitignore 2>/dev/null && echo "OK：.gitignore 包含 Claude 模式" || echo "信息：.gitignore 不含 Claude 模式"
```

**评分：**
- 10：CLAUDE.md 含约定、配置了钩子、自定义命令、规则、agent
- 7-9：CLAUDE.md 存在且含项目上下文、一些命令或规则
- 4-6：基本的 CLAUDE.md、无钩子或命令
- 1-3：无 CLAUDE.md 或 CLAUDE.md 为空

---

## 评分与报告

### 总体评分计算

```
总体 =（密钥 × 0.15）+（安全 × 0.15）+（依赖 × 0.15）+
      （结构 × 0.10）+（测试 × 0.15）+（导入 × 0.10）+
      （AI 模式 × 0.20）
```

保留一位小数。

### 输出格式

```markdown
## 代码库健康审计

**项目**：[目录名]
**日期**：[时间戳]
**审计类别**：[全部 7 个或筛选子集]

### 总体评分：[X.X] / 10

| 类别 | 评分 | 权重 | 加权分 | 关键发现 |
|----------|-------|--------|----------|-------------|
| 密钥 | X/10 | 15% | X.XX | [一行摘要] |
| 安全 | X/10 | 15% | X.XX | [一行摘要] |
| 依赖 | X/10 | 15% | X.XX | [一行摘要] |
| 结构 | X/10 | 10% | X.XX | [一行摘要] |
| 测试 | X/10 | 15% | X.XX | [一行摘要] |
| 导入 | X/10 | 10% | X.XX | [一行摘要] |
| AI 模式 | X/10 | 20% | X.XX | [一行摘要] |
| **总体** | | **100%** | **X.XX** | |

### 详细发现

#### 🔴 关键（立即修复）
- [发现及 file:line 引用和具体修复方案]

#### 🟡 警告（本周修复）
- [发现及上下文和建议方法]

#### 🟢 信息（值得改进）
- [观察及可选建议]

### 改进计划

[根据总体评分显示相应层级]

#### 第 1 层：基础（当前评分 <5，目标：5）
优先消除关键风险。

| 优先级 | 操作 | 类别 | 影响 | 工作量 |
|----------|--------|----------|--------|--------|
| 1 | [具体操作] | [类别] | [分数提升] | [时间估计] |
| 2 | [具体操作] | [类别] | [分数提升] | [时间估计] |
| ... | | | | |

#### 第 2 层：稳固（当前评分 5-7，目标：8）
在基础上构建可靠实践。

| 优先级 | 操作 | 类别 | 影响 | 工作量 |
|----------|--------|----------|--------|--------|
| 1 | [具体操作] | [类别] | [分数提升] | [时间估计] |
| ... | | | | |

#### 第 3 层：优秀（当前评分 8+，目标：10）
打磨优化以实现最大团队效率。

| 优先级 | 操作 | 类别 | 影响 | 工作量 |
|----------|--------|----------|--------|--------|
| 1 | [具体操作] | [类别] | [分数提升] | [时间估计] |
| ... | | | | |

### 速胜（<30 分钟）
1. [工作量最小但提升分数的操作]
2. [...]
3. [...]
```

### 严重程度分布

约 70% 的发现应是可自动化的（脚本、linter、CI 检查可检测）。标记剩余 30% 需要人工判断，并解释为何自动化工具有限。

---

**来源**：
- Variant Systems codebase analyzer 插件（variantsystems.io，2026 年 2 月）：7 类别分析框架
- OWASP Top 10（2021）：安全类别模式
- Claude Code Security Hardening Guide：AI 模式类别基线

$ARGUMENTS
