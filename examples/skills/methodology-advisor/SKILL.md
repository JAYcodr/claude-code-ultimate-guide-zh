---
name: methodology-advisor
description: 分析你的代码库并提出 3 个有针对性的问题，以推荐合适的 AI 辅助开发方法论栈
effort: medium
---

# 方法论顾问

分析此项目并推荐最佳的 AI 辅助开发方法论栈。先从代码库中读取能读到的信息，然后仅询问无法推断的内容。

**时间**：2-4 分钟 | **输出**：推荐栈 + 上下文快速开始

---

## 阶段 1 — 静默代码库分析

静默运行以下读取。暂时不输出结果——仅在内部构建认知。

### 1.1 项目身份

```bash
# 配置文件
cat CLAUDE.md 2>/dev/null || cat claude.md 2>/dev/null
cat package.json 2>/dev/null | grep -E '"name"|"description"|"scripts"' | head -10
cat Cargo.toml 2>/dev/null | grep -E '^name|^description' | head -5
cat pyproject.toml 2>/dev/null | grep -E '^name|^description' | head -5
cat go.mod 2>/dev/null | head -3
```

### 1.2 团队规模

```bash
# 过去 90 天的唯一贡献者
git log --since="90 days ago" --format="%ae" 2>/dev/null | sort -u | wc -l
# 总提交数
git log --oneline 2>/dev/null | wc -l
```

### 1.3 测试成熟度

```bash
# 测试文件是否存在？
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" -o -name "test_*.py" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l
# 测试框架线索
grep -rn --include="*.json" --include="*.toml" --include="*.yaml" \
  -l "jest\|vitest\|pytest\|rspec\|mocha\|cypress\|playwright" \
  2>/dev/null | grep -v node_modules | head -5
# CI 配置
ls .github/workflows/*.yml 2>/dev/null | wc -l
ls .gitlab-ci.yml .circleci/config.yml 2>/dev/null | wc -l
```

### 1.4 规范和文档信号

```bash
# 规范文件
find . -name "*.spec.md" -o -name "SPEC*.md" -o -name "spec.md" -o -name "DESIGN*.md" \
  -o -name "ADR*.md" -o -name "RFC*.md" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -10
# OpenAPI / 契约文件
find . -name "openapi*.yaml" -o -name "openapi*.json" -o -name "swagger*.yaml" \
  -o -name "*.proto" \
  2>/dev/null | grep -v node_modules | head -5
# BDD 特性文件
find . -name "*.feature" 2>/dev/null | grep -v node_modules | wc -l
```

### 1.5 代码库大小和结构

```bash
# 文件数（粗略）
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" \
  -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.rb" \) \
  2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l
# 服务/包（monorepo 信号）
ls packages/ apps/ services/ 2>/dev/null | head -10
```

### 1.6 AI 和 LLM 信号

```bash
# 代码中的 LLM API 使用
grep -rn --include="*.ts" --include="*.py" --include="*.js" \
  -l "anthropic\|openai\|groq\|mistral\|langchain\|llm\|ChatCompletion\|claude" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -5
# 评估框架线索
find . -name "evals*" -o -name "*eval*" -type d 2>/dev/null | grep -v node_modules | head -5
```

---

## 阶段 2 — 评分 8 个栈

根据你的发现，对每个栈评 0-10 分（基于适配信号）：

| 栈 | 提升评分的关键信号 |
|-------|----------------------------------|
| **solo-mvp** | 1 个贡献者、文件少、无 CI、绿地方案 |
| **team-greenfield** | 2-10 贡献者、新项目、无遗留文件 |
| **microservices** | `packages/`、`services/`、OpenAPI 文件、`.proto` |
| **brownfield-saas** | 提交数高、文件数多、测试文件少 |
| **enterprise-gov** | 10+ 贡献者、CI、ADR 文件、`AGENTS.md` |
| **llm-native** | LLM 导入、eval 目录、AI 产品信号 |
| **power-solo** | 1 个贡献者、提交频率高、迭代式提交 |
| **plan-moderate** | 混合信号、CLAUDE.md 存在、中等规模 |

---

## 阶段 3 — 仅询问无法推断的内容

静默分析后，用 2-3 行向用户呈现初步情况，然后精确地提出 3 个问题。不多不少。

格式：

```
从你的代码库我能看出：[2-3 个具体观察]。
推荐之前，有 3 个问题：

1. [痛点问题——从下方选择最相关的]
2. [部署频率——如果无法从 CI/CD 信号推断]
3. [投入意愿——你愿意投入多少前期工作量？]
```

**问题库——根据你的发现选择最相关的 3 个：**

- 痛点："目前最拖慢你的是什么——回归、需求不明确、会话间的上下文腐烂、还是没有可追溯性？"
- 痛点："当 Claude 生成大量代码时，你最担心什么——质量、偏离规范、还是无法追踪已构建的内容？"
- 部署："你多久发布一次生产版本——每天多次、每周、还是更长的发布周期？"
- 部署："这是一个有真实用户的产品、一个原型、还是一个内部工具？"
- 治理："你愿意投入多少前期设置——不投入（直接开始）、30 分钟、还是半天？"
- 治理："开发团队之外的人（PM、QA、合规）是否需要验证构建的内容？"
- AI 产品："你的产品是否直接向最终用户暴露 AI 生成的输出？"
- 规模："多个服务或团队是否需要在实现前就 API 契约达成一致？"

---

## 阶段 4 — 推荐

按以下结构输出推荐：

---

### 你的栈：[栈名称] [图标]

**为什么适合你的项目：**
- [阶段 1 的发现] → [解释选择了此栈]
- [阶段 1 的发现] → [解释选择了此栈]
- [问题 N 的答案] → [解释选择了此栈]

**包含的方法论：** `[方法 A]` + `[方法 B]`（+ `[方法 C]` 如适用）

**实际效果：**
[2-3 句话描述此项目的具体工作流，使用实际找到的文件名或路径。]

**你的项目的快速开始：**
1. [基于实际项目上下文的具体第一步]
2. [第二步]
3. [第三步]

**开始前请注意：**
- [一个此栈的诚实权衡或局限]
- [根据你的发现需要留意的一个事项]

**深入了解：** https://cc.bruniaux.com/methodologies/ — 交互式测验和完整栈对比
**方法论完全指南：** https://cc.bruniaux.com/guide/methodologies/

---

## 栈参考（内部）

用此将评分映射到快速启动语言：

**solo-mvp**（SDD + TDD）：在 CLAUDE.md 中编写功能规范 → `"为此规范编写会失败的测试，然后实现直到变绿。"`

**team-greenfield**（Spec Kit + TDD + BDD）：`/speckit.constitution` → 与 PM 一起编写 Given/When/Then 场景 → TDD 每个场景。

**microservices**（CDD + Specmatic + TDD）：先编写 OpenAPI 规范 → Specmatic 用于契约测试 → TDD 实现。

**brownfield-saas**（OpenSpec + BDD + JiTTesting）：OpenSpec 捕获当前状态 → BDD 用于更改的行为 → 合并前：`"生成能捕获此 diff 中回归的测试。"`

**enterprise-gov**（BMAD + Spec Kit + Specmatic）：`constitution.md` → agent 角色定义 → Spec Kit 需求 → Specmatic 契约执行。

**llm-native**（Eval 驱动 + 多 Agent）：定义评估标准（准确性、安全性、格式）→ 构建评估工具 → 迭代直到评估通过。

**power-solo**（TDD + Ralph Loop + 迭代）：紧密的测试循环 → 通过 git stash + 进度文件实现每次任务新上下文 → `"持续迭代直到所有测试通过且 lint 干净。"`

**plan-moderate**（Plan-First + SDD + 上下文工程）：每个复杂任务以规划模式开始（Shift+Tab）→ 验证 → 在 CLAUDE.md 中编写规范 → 通过渐进式上下文加载执行。
