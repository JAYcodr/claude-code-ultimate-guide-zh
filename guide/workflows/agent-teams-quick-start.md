---
title: "智能体团队快速入门指南"
description: "5 分钟设置指南，包含智能体团队的复制粘贴模式"
tags: [workflow, agents, tutorial]
---

# 智能体团队快速入门指南

> **在你项目中使用智能体团队的实用指南**
> **阅读时间**：8-10 分钟 | **完整文档**：[智能体团队](./agent-teams.md)（30 分钟概述）

## 这是什么？

你知道智能体团队存在。你读过理论。但**你实际上什么时候应该在项目中使用它们？**

本指南提供：
- ✅ **5 分钟设置**（环境 → 首次测试）
- ✅ **4 个复制粘贴模式**用于真实项目（Guide + RTK）
- ✅ **决策矩阵**（何时用，何时不用）
- ✅ **指标**用于衡量 ROI
- ✅ **红旗**避免浪费

**如果你想理论**：阅读[智能体团队完整文档](./agent-teams.md)。

---

## 目录

1. [5 分钟设置](#1-5-分钟设置)
2. [项目模式](#2-项目模式)
   - 2.1 [Claude Code 指南 - 发布前审查](#21-claude-code-指南---发布前审查)
   - 2.2 [Claude Code 指南 - Landing 同步](#22-claude-code-指南---landing-同步)
   - 2.3 [Claude Code 指南 - 多文件文档更新](#23-claude-code-指南---多文件文档更新)
   - 2.4 [RTK - 安全 PR 审查](#24-rtk---安全-pr-审查)
3. [决策矩阵：何时使用](#3-决策矩阵何时使用)
4. [最小工作流模板](#4-最小工作流模板)
5. [成功指标](#5-成功指标)
6. [限制与红旗](#6-限制与红旗)

---

## 1. 5 分钟设置

### 步骤 1：前置条件检查

```bash
# 检查 Claude Code 版本（需要 v2.1.32+）
claude --version

# 检查模型可用性
claude
> /model opus
# 应显示："Model changed to opus (claude-opus-4-6-20250624)"
```

**最低要求**：
- Claude Code v2.1.32+
- Opus 4.6 模型
- Git 仓库（智能体团队使用 git 进行协调）

### 步骤 2：启用功能

```bash
# 设置环境变量（添加到 ~/.bashrc 或 ~/.zshrc 以持久化）
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 启动 Claude Code
claude
```

### 步骤 3：验证

```
> Are agent teams enabled?
```

**预期响应**：
```
Yes, agent teams are enabled in this session. I can create teams
of agents to work in parallel on complex tasks using:
- Multi-agent coordination
- Git-based task claiming
- Autonomous team coordination
```

**如果已禁用**：检查环境变量是否设置（`echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`）。

### 步骤 4：首次测试（2 个智能体）

```
> Create a simple test team to analyze this README:
> - Agent 1: Check structure (sections, TOC, badges)
> - Agent 2: Check content quality (clarity, examples, completeness)
```

**发生了什么**：
1. Claude 生成 2 个智能体（你会看到"Creating team..."消息）
2. 智能体并行工作（你可能看到"Idle"消息——这是正常的）
3. Claude 呈现合并发现（收敛 + 独特洞察）

**导航**：
- `Shift+Down`：循环切换队友输出（进程中模式）
- 主视图：合并汇总

**时长**：简单 2 智能体任务 1-2 分钟。

---

## 2. 项目模式

### 2.1 Claude Code 指南 - 发布前审查

**用例**：版本升级前的系统性审计，发现一致性问题（链接断开、计数不同步、版本错误）

**触发**：每次执行 `/release` 命令前

**时长**：3-5 分钟

**团队组成**：
```
Team: pre-release-audit (3 agents)
├─ accuracy-auditor → 验证声明、统计、版本、外部链接
├─ consistency-checker → 检查模板数量、评估数量、指南行数是否跨文件匹配
└─ breaking-checker → 识别与上一版本的 Breaking Changes
```

**复制粘贴提示**：
```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

**ROI**：发现的 bug 示例：
- LinkedIn URL 损坏（今天的真实审计中发现）
- guide/landing 之间不同步（模板计数）
- 多个文件中版本号错误
- 外部链接断开

**何时跳过**：简单的拼写错误修复（无版本/计数/链接更改）。

**真实示例**（2026-02-08 测试）：
```
Findings:
- Accuracy: 1 critical (LinkedIn URL malformed), 3 warnings (external links to verify)
- Consistency: 2 criticals (template count mismatch README vs landing, line numbers outdated in reference.yaml)
- Breaking: 0 breaking changes detected vs v3.23.0 (clean release)

Convergence: 2 agents flagged template count issue (high confidence)
Time: 4 min 12 sec
Verdict: ✅ High value, found 3 criticals that would've shipped
```

---

### 2.2 Claude Code 指南 - Landing 同步

**用例**：验证 guide/landing 同步（版本、计数、内容），无需运行手动脚本

**触发**：重大指南修改后（版本升级、模板添加、FAQ 更改）

**时长**：2-3 分钟

**团队组成**：
```
Team: landing-sync (2 agents)
├─ guide-scanner → 提取版本、模板计数、评估计数、指南行数、FAQ 内容
└─ landing-scanner → 与 index.html、examples.html 比较，检查同步状态
```

**复制粘贴提示**：
```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md), FAQ entries from README.md
> - Landing scanner: Check /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/index.html and examples.html for version in footer+FAQ, template count in badges, eval count, guide lines approximation (~9800+)
>
> Report: Synced ✅ / Mismatches with line numbers
```

**ROI**：
- 零不同步发送到生产环境
- 避免手动执行 `./scripts/check-landing-sync.sh`
- 比脚本更快（2 分钟 vs 运行脚本 + 修复 5 分钟）

**何时跳过**：纯代码更改（不影响文档/计数）。

**成功标准**：
```
✅ All synced: Version, template count, eval count match
⚠️ Mismatch: Specific line numbers in index.html to fix
```

---

### 2.3 Claude Code 指南 - 多文件文档更新

**用例**：跨多个文件（ultimate-guide.md、reference.yaml、README.md）添加新功能文档，确保交叉引用一致性

**触发**：新功能部分（>50 行）、Breaking Changes、架构更新

**时长**：5-8 分钟

**团队组成**：
```
Team: doc-update (3 agents)
├─ content-writer → 在 ultimate-guide.md 中编写主要部分，包含示例
├─ index-updater → 更新 TOC、reference.yaml 条目、README 导航
└─ consistency-checker → 验证交叉引用、行号、锚点是否正常工作
```

**复制粘贴提示**：
```
> Update documentation for new "[FEATURE NAME]" feature:
> - Content Scope: Write section [X.Y] in guide/ultimate-guide.md with:
>   - Overview (what/why/when)
>   - 2-3 concrete examples
>   - Best practices + gotchas
>   - Links to related sections
>   Context: guide/ultimate-guide.md section [X.Y] only
> - Index Scope: Update:
>   - guide/ultimate-guide.md TOC (add section [X.Y])
>   - machine-readable/reference.yaml (add entry with line numbers)
>   - README.md navigation (add link if major feature)
>   Context: Index files only (TOC, reference.yaml, README.md)
> - Consistency Scope: Verify:
>   - All cross-references resolve correctly
>   - Line numbers in reference.yaml match actual content
>   - Anchors in README point to correct sections
>   - No broken internal links
>   Context: All modified files for cross-reference validation
```

**ROI**：
- 零链接断开（consistency-checker 捕获全部）
- 比顺序快 60%（写 → 索引 → 验证）
- 并行工作减少等待时间

**何时跳过**：单文件编辑（<50 行），无需交叉引用。

**真实示例**（智能体团队部分添加）：
```
Task: Add "Agent Teams" as section 9.20 (300 lines)
Files touched: 3 (ultimate-guide.md, reference.yaml, README.md)

Sequential estimate: 12-15 min (write → index → verify)
Agent Teams: 7 min 30 sec (3 agents parallel)
Savings: 40% time + zero manual cross-ref checks
```

---

### 2.4 RTK - 安全 PR 审查

**用例**：审查外部贡献者的 PR 安全问题（注入、令牌泄漏）、Rust 惯用法和性能

**触发**：非核心贡献者打开的 PR，PR 触及敏感代码（认证、外部命令、正则）

**时长**：5-8 分钟

**团队组成**：
```
Team: security-pr-review (3 agents)
├─ rust-expert → 检查所有权模式、错误处理（anyhow/thiserror）、惯用代码
├─ security-auditor → 扫描注入风险、令牌泄漏、输入清理
└─ perf-analyzer → 审查内存分配、异步模式、编译正则
```

**复制粘贴提示**：
```
> Review PR #[NUMBER] with scope-focused analysis:
> - Rust Scope: Check:
>   - Ownership patterns (prefer &str over String, minimize clones)
>   - Error handling (anyhow::Result with .context(), no unwrap outside tests)
>   - Idiomatic code (impl after type, #[cfg(test)] mod tests)
>   - Clippy compliance (zero warnings)
>   Context: All modified .rs files
> - Security Scope: Scan for:
>   - Command injection (shell escapes, argument sanitization)
>   - Token/credential leaks (hardcoded secrets, logs, error messages)
>   - Input sanitization (path traversal, regex DoS)
>   - File operations (path validation, permissions)
>   Context: Input handling, auth, file I/O code
> - Performance Scope: Review:
>   - Unnecessary allocations (String::from vs &str)
>   - Async patterns (spawn_blocking for CPU-bound work)
>   - Compiled regex (lazy_static! for hot paths)
>   - Algorithm complexity (O(n) vs O(n²))
>   Context: Hot paths, loops, async functions
```

**ROI**：
- 盲点检测：Security + Rust + Perf = 单个审查者会遗漏的区域
- 一致的审查质量（不依赖于审查者情绪/专注度）
- 比顺序快（3 个智能体并行 vs 3 轮审查）

**何时跳过**：来自可信贡献者的内部 PR，简单更改（仅文档、注释、测试）。

**成功标准**：
```
✅ Convergence: 2+ agents flag same critical issue (high confidence)
✅ Unique insights: Each agent finds domain-specific issues (Rust/Security/Perf)
❌ False positives: <20% of findings are invalid
```

**真实示例**（假设的外部 PR）：
```
PR: Add new git filter command
Agents findings:
- Rust: 3 issues (unwrap in production code, missing .context(), non-idiomatic error handling)
- Security: 2 criticals (shell injection via user input, token leak in error message)
- Perf: 1 issue (regex compiled on every call, not lazy_static)

Convergence: Security + Rust both flagged missing input sanitization (high confidence)
Time: 6 min 40 sec
Verdict: ✅ Critical security issues caught, PR requires revision
```

---

## 3. 决策矩阵：何时使用

| 情况 | 智能体团队？ | 原因 |
|-----------|---------------|--------|
| **发布前审查（指南）** | ✅ 是 | 多层审计（准确性 + 一致性 + Breaking）需要并行视角 |
| **简单拼写错误修复** | ❌ 否 | 大材小用，1 个智能体 = 10 秒，3 个智能体 = 成本浪费 |
| **外部 PR（RTK）** | ✅ 是 | Security + Rust + Perf = 盲点检测，高风险审查 |
| **多文件文档更新（指南）** | ✅ 是 | Content + Index + Consistency = 零链接断开，并行工作 |
| **Landing 同步检查** | ⚠️ 可能 | 如果怀疑不同步使用智能体团队，否则 `./scripts/check-landing-sync.sh` 更快 |
| **CHANGELOG 更新** | ❌ 否 | 顺序任务（线性写作），无并行化收益 |
| **单文件编辑（RTK）** | ❌ 否 | 无需协调，顺序即可 |
| **小型 README 调整（<50 行）** | ❌ 否 | 无交叉引用，无复杂性，单个智能体更快 |
| **架构设计** | ✅ 是 | 多视角（前端、后端、基础设施、安全）揭示盲点 |
| **Bug 调查** | ⚠️ 可能 | 简单 bug → 否，复杂多组件故障 → 是 |

### 经验法则

**使用智能体团队当**：
- ✅ 你自然会想"我应该检查 X、Y 和 Z"
- ✅ 高风险（生产发布、外部贡献者、安全敏感）
- ✅ 需要多范围分析（Rust 范围 + 安全范围 + 性能范围）
- ✅ 跨文件一致性重要（链接、计数、版本同步）
- ✅ 并行工作可能（独立任务，无顺序依赖）

**不要使用智能体团队当**：
- ❌ 简单任务（<5 个文件，<100 行，1 个领域）
- ❌ 顺序工作流（B 取决于 A 结果）
- ❌ 预算紧张（3x tokens，为高价值任务保留）
- ❌ 写密集型（许多编辑相同文件 = 合并冲突）

---

## 4. 最小工作流模板

### Bash 模板（可重用）

```bash
# 1. 设置（每会话一次）
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 2. 启动 Claude
claude

# 3. 创建团队（提示模板）
> Create a team to [TASK]:
> - Agent 1 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 2 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 3 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
>
> [FILES/DIRECTORIES TO ANALYZE]

# 4. 观察（可选）
# Shift+Down 循环切换队友输出（进程中模式）

# 5. 汇总
# Claude 自动呈现合并发现

# 6. 行动
# 修复关键发现，跳过次要发现
```

### 示例提示（可直接复制）

#### 发布前指南审计

```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

#### 安全 PR 审查（RTK）

```
> Review PR #42 with scope-focused analysis:
> - Rust Scope: Check ownership patterns, error handling (anyhow/thiserror), idiomatic code in modified files (context: src/**/*.rs)
> - Security Scope: Scan for injection risks, token leaks, input sanitization (context: auth, input handling code)
> - Performance Scope: Review allocations, async patterns, compiled regex (context: hot paths, loops)
```

#### 多文件文档更新

```
> Update documentation for new "Agent Teams Quick Start" feature:
> - Content Scope: Write guide/workflows/agent-teams-quick-start.md with overview, 4 patterns, decision matrix, metrics
> - Index Scope: Update guide/ultimate-guide.md (add reference section 9.20), machine-readable/reference.yaml (add entry), CHANGELOG.md (add "Added" entry)
> - Consistency Scope: Verify all cross-refs work, line numbers match, no broken links (context: all modified files)
```

#### Landing 同步验证

```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md)
> - Landing scanner: Check /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/index.html and examples.html for version, counts, guide lines approximation
```

---

## 5. 成功指标

### 如何衡量智能体团队 ROI

| 指标 | 目标 | 如何衡量 |
|--------|--------|----------------|
| **收敛率** | >50% | 2+ 智能体标记的发现 / 总发现。收敛 = 高置信度。 |
| **独特洞察** | 每个智能体 ≥1 | 每个智能体必须在其领域找到至少 1 个独特问题。如果智能体找到 0 个独特 = 浪费 tokens。 |
| **误报率** | <20% | 无效发现 / 总发现。太多误报 = 提示质量差。 |
| **时间节省** | 60-70% | 比较智能体团队时间 vs 顺序（估计 3 个任务 3 倍单智能体时间）。 |
| **Bug 捕获率** | >80% | 智能体发现的关键 bug / 发售后发现的总 bug。高 = 有效预防。 |

### 真实示例：发布前审查测试（2026-02-08）

```
Task: Pre-release audit for v3.23.1
Agents: 3 (accuracy-auditor, consistency-checker, breaking-checker)
Duration: 4 min 12 sec

Findings (raw): 45 total
├─ Accuracy: 12 (1 critical: LinkedIn URL malformed, 11 warnings)
├─ Consistency: 18 (2 criticals: template count desync, line numbers outdated)
└─ Breaking: 15 (0 breaking changes, 15 informational notes)

Findings (deduplicated): ~30 unique issues

Convergence analysis:
├─ High confidence (2-3 agents): 4 issues
│   ├─ Template count mismatch (consistency + accuracy)
│   ├─ Line numbers outdated (consistency + accuracy)
│   ├─ External link verification needed (accuracy + breaking)
│   └─ Version sync across files (all 3 agents)
└─ Unique insights:
    ├─ Accuracy: LinkedIn URL corruption (only this agent caught it)
    ├─ Consistency: TOC structure deviation (only this agent)
    └─ Breaking: Changelog format improvement suggestion (only this agent)

Metrics:
├─ Convergence rate: 4/30 = 13% (lower than target, but 4 criticals flagged by multiple agents = high confidence on what matters)
├─ Unique insights: 3/3 agents = 100% (each agent found unique issues in their domain)
├─ False positive rate: 2/30 = 6.6% (below 20% target ✅)
├─ Time saving: 4 min vs estimated 12 min sequential = 66% savings ✅
├─ Bug catch rate: 3 critical bugs caught that would've shipped = prevented production issues ✅

Verdict: ✅ High value for pre-release audits
```

### 如何跟踪你的指标

**每个智能体团队任务后**：

1. **计数发现**：记录每个智能体的原始发现，然后去重
2. **标记收敛**：哪些问题被 2+ 智能体标记？
3. **检查独特洞察**：每个智能体是否找到至少 1 个领域特定问题？
4. **验证误报**：有多少发现是无效/噪音？
5. **时间对比**：智能体团队时长 vs 估计顺序时间
6. **发售后验证**：智能体团队是否捕获了会发货的关键 bug？

**保持日志**（项目文档中的 Markdown 表格）：

```markdown
| Date | Task | Agents | Duration | Findings | Convergence | Unique | False+ | Time Saved | Bugs Caught |
|------|------|--------|----------|----------|-------------|--------|--------|------------|-------------|
| 2026-02-08 | Pre-release v3.23.1 | 3 | 4m12s | 30 | 13% (4 critical) | 3/3 | 6.6% | 66% | 3 |
```

**如果指标不达标，调整提示**：
- 低收敛（<30%）→ 范围太窄，更多重叠上下文边界
- 无独特洞察→ 范围太相似，多样化分析角度
- 高误报（>20%）→ 提示太模糊，添加具体标准

---

## 6. 限制与红旗

### 智能体团队不能做什么

| 限制 | 含义 | 缓解 |
|------------|---------------|-----------|
| **3x tokens** | 每个智能体 = 独立模型调用 = 3x 成本 | 为高风险任务保留（发布前、安全 PR，不是拼写错误修复） |
| **空闲spam** | 智能体在协调期间显示"Idle"消息 | 正常行为，不是 bug，忽略 spam |
| **实验性** | 研究预览 = 不保证稳定性 | 预期有 bug，不要依赖智能体团队进行生产关键工作流 |
| **协调开销** | 最多 3-5 个智能体，不是 10（协调复杂性增长） | 坚持 2-4 个智能体，避免"10 个智能体团队"提示 |
| **上下文隔离** | 智能体看不到彼此的发现（独立工作） | Claude 汇总发现，但智能体不能在任务中途相互构建工作 |

### 红旗：何时不使用

❌ **简单任务**（<5 个文件，<100 行，1 个领域）
- 示例：修复 README.md 中的拼写错误
- 为什么避免：10 秒任务的 3x tokens = 浪费

❌ **顺序工作流**（B 取决于 A 结果）
- 示例：实现功能 → 写测试 → 部署
- 为什么避免：智能体并行工作，不能处理依赖

❌ **预算紧张**（3x tokens，优化成本）
- 示例：API 额度有限的个人项目
- 为什么避免：智能体团队是高风险任务的奢侈品，不是日常工作流

❌ **写密集型**（许多编辑相同文件）
- 示例：重构整个代码库结构
- 为什么避免：合并冲突，协调开销，智能体互相踩踏

❌ **低风险审查**（内部 PR、可信贡献者、简单更改）
- 示例：团队成员修复小 bug
- 为什么避免：大材小用，单智能体审查更快更便宜

### 尽管有成本但应该使用的情况

✅ **高风险**（生产发布、安全敏感、外部贡献者）
✅ **多领域**（Rust + Security + Performance = 盲点）
✅ **并行友好**（独立任务，无顺序依赖）
✅ **一致性关键**（跨文件同步、计数、版本）
✅ **学习机会**（理解盲点，改进提示）

---

## 总结：快速参考

### 设置（一次 5 分钟）

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
> Are agent teams enabled?  # Verify
```

### 何时使用（决策规则）

**是如果**：
- 高风险 + 多领域 + 并行友好

**否如果**：
- 简单任务 + 顺序 + 预算紧张

### 模式（4 个可直接使用）

1. **发布前审查**（指南）→ 准确性 + 一致性 + Breaking
2. **Landing 同步**（指南）→ 指南扫描器 + Landing 扫描器
3. **多文件文档更新**（指南）→ Content + Index + Consistency
4. **安全 PR 审查**（RTK）→ Rust + Security + Performance

### 指标（跟踪 ROI）

- 收敛：>50%（2+ 智能体的发现）
- 独特洞察：每个智能体 ≥1
- 误报：<20%
- 时间节省：60-70%
- Bug 捕获：>80%

### 红旗（避免浪费）

- ❌ 简单任务（<5 个文件）
- ❌ 顺序工作流
- ❌ 预算紧张
- ❌ 写密集型（合并冲突）

---

## 下一步

1. **尝试首次测试**（5 分钟设置 + 简单 2 智能体任务）
2. **从你的项目选择一个模式**（指南或 RTK）
3. **衡量指标**（收敛、独特洞察、时间节省）
4. **根据结果调整提示**
5. **阅读完整文档**了解高级模式：[智能体团队](./agent-teams.md)

**有问题？** 查看[完整文档](./agent-teams.md)了解：
- 架构深入解析（git 协调如何工作）
- 高级用例（15+ 生产场景）
- 故障排查（常见问题 + 解决方案）
- 最佳实践（团队规模、提示设计、冲突解决）