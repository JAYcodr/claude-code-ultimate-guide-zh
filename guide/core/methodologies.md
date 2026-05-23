---
title: "开发方法论参考"
description: "15 种结构化 AI 辅助开发方法论的快速参考，包括 TDD、SDD 和 BDD"
tags: [reference, tdd, design-patterns, workflows]
---

# 开发方法论参考

> **可信度**：第二层 — 经多个生产报告和官方文档验证。
>
> **最后更新**：2026 年 2 月

这是 2025-2026 年 AI 辅助开发领域涌现的 15 种结构化开发方法论的快速参考。实践工作流请参见 [workflows/](../workflows/)。

---

## 目录

1. [决策树](#决策树你需要什么)
2. [15 种方法论](#15-种方法论)
3. [SDD 工具参考](#sdd-工具参考)
4. [编写有效规约](#编写有效规约)
5. [组合模式](#组合模式)
6. [来源](#来源)

---

## 决策树：你需要什么？

```
┌─ "我要高质量的代码"          ──→ workflows/tdd-with-claude.md
│
├─ "我要先写规约再写代码"      ──→ workflows/spec-first.md
│
├─ "我需要规划架构"            ──→ workflows/plan-driven.md
│
├─ "我在迭代某个东西"          ──→ workflows/iterative-refinement.md
│
└─ "我需要方法论理论"          ──→ 继续往下读
```

---

## 方法论地图

每种方法论在两个维度上的位置：**规约优先 vs 代码优先**（Y 轴）和**精益/独立 vs 企业/治理**（X 轴）。

```
                      规约 / 计划优先
                            ▲
  ── 精益 · 规约 ──         │          ── 治理 · 规约 ──
                            │
  [文档驱动]  [SDD]          │    [BDD]  [ATDD]   [需求驱动]
  [GSD]  [计划优先]          │ [CDD] [ADR驱动] [DDD] [BMAD]
                            │
  精益 ─────────────────────┼────────────────────────────────► 企业
                            │
  ── 精益 · 代码 ──         │          ── 治理 · 代码 ──
                            │
  [上下文工程] [TDD]        │       [多智能体]
  [提示工程] [迭代]         │       [评估驱动]      [FDD]
  [Ralph 循环]              │           [JiTTesting]
                            │
                        代码 / 涌现
```

**如何阅读：**

- **左上** — 规约优先 · 精益：`SDD`、`文档驱动`、`计划优先`。独立开发者和小团队脱离"代码优先"的自然入口。
- **右上** — 规约优先 · 治理：`BMAD`、`需求驱动`、`ATDD`、`DDD`。真正的治理，但设置成本高。ROI 由项目复杂度和需求稳定性驱动，而非仅人头数。
- **左下** — 代码优先 · 精益：Claude Code 的自然领地。`TDD` + `Ralph 循环` + `迭代` = 核心独立工作流。
- **右下** — 代码优先 · 规模化：`多智能体`、`评估驱动`、`JiTTesting`（Meta，1 亿+ 行代码）。高产量团队的新兴模式。
- **轴线上** — `计划优先`、`CDD`、`ADR 驱动`、`GSD`：适应任何上下文的混合方法。

---

## 15 种方法论

按 6 层金字塔组织，从上到下从策略编排到优化技术。

### 第 1 层：策略编排

| 名称 | 是什么 | 最适合 | Claude 适配度 |
|------|--------|-------|-------------|
| **BMAD** | 多智能体治理，以宪法为护栏 | 高复杂度项目，需求稳定、需合规或治理 | ⭐⭐ 小众但强大 |
| **GSD** | 元提示 6 阶段工作流，每任务新上下文 | 独立开发者、Claude Code CLI | ⭐⭐ 类似本指南中的模式 |

**BMAD（Breakthrough Method for Agile AI-Driven Development）** 颠覆了传统范式：文档成为真实来源，而非代码。使用专业智能体（分析师、PM、架构师、开发者、QA）配合严格治理进行编排。*注意：BMAD 的基于角色的智能体命名反映了他们的方法论；请参见 §9.17 智能体反模式了解范围聚焦的替代方案。*

- **关键概念**：Constitution.md 作为策略护栏
- **何时使用**：需要治理的复杂企业项目
- **何时避免**：MVP、快速原型、需求演进中的项目——BMAD 在规约中途变更时很脆弱

**GSD（Get Shit Done）** 通过系统化的 6 阶段工作流（初始化 → 讨论 → 计划 → 执行 → 验证 → 完成）解决上下文腐烂问题，每任务使用全新的 200K token 上下文。核心概念（多智能体编排、全新上下文管理）与 Ralph 循环、Gas Town 和 BMAD 等现有模式显著重叠。详细对比请参见[资源评估](../../docs/resource-evaluations/gsd-evaluation.md)。

> **新兴**：[Ralph Inferno](https://github.com/sandstream/ralph-inferno) 实现了自主多角色工作流（分析师→PM→UX→架构师→业务），支持基于 VM 的执行和自纠错 E2E 循环。实验性，但对"大规模氛围编码"有兴趣。

---

### 基础训练：计划优先工作流

> **"计划做好了，代码自然就好了。"**
> — Boris Cherny，Claude Code 创始人

**不只是一个功能（`/plan` 命令）——这是一个系统性的训练。**

> **上下文工程**：Thoughtworks 在其技术雷达（2025 年 11 月）中将这种更广泛的方法称为"上下文工程"——在推理过程中向 LLM 提供信息的系统性设计[^thoughtworks2025]。三种核心技术：上下文设置（最小系统提示、少量示例）、长周期任务的上下文管理（摘要、外部记忆、子智能体架构）、以及动态信息检索（JIT 上下文加载）。Claude Code 中的相关模式：AGENTS.md、MCP Context7、计划模式。

[^thoughtworks2025]: Thoughtworks 技术雷达第 33 卷，2025 年 11 月。[PDF](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/11/tr_technology_radar_vol_33_en.pdf)。另请参见：[宏观趋势博客文章](https://www.thoughtworks.com/insights/blog/technology-strategy/macro-trends-tech-industry-november-2025)。

**心智模型**：

规划对于复杂任务来说不是可选项。这决定了：
- ❌ 8 次"试 → 修 → 重试 → 再修"的迭代
- ✅ 1 次"规划 → 验证 → 干净执行"的迭代

**何时先计划**：

| 任务复杂度 | 先计划？ | 为什么 |
|-----------|---------|------|
| 修改 >3 个文件 | ✅ 是 | 跨文件依赖需要架构 |
| 变更 >50 行 | ✅ 是 | 足够的复杂度可能出错 |
| 架构变更 | ✅ 是 | 需要影响分析 |
| 不熟悉的代码库 | ✅ 是 | 在行动前需要探索 |
| 拼写错误/明显修复 | ❌ 否 | 规划开销 > 任务时间 |
| 单行更改 | ❌ 否 | 直接做就行 |

**计划优先如何工作**：

1. **探索阶段**（通过 `Shift+Tab` 的计划模式）：
   - Claude 读取文件、探索架构
   - 不允许编辑 → 强制先思考再行动
   - 提出方案，附带权衡

2. **验证阶段**（你审查）：
   - 计划暴露假设和差距
   - 现在纠正方向比写了 100 行代码后再纠正容易得多
   - 计划成为执行的契约

3. **执行阶段**（通过 `Shift+Tab` 切换回正常模式）：
   - 计划 → 代码成为机械性的翻译
   - 更少意外、更干净的实现
   - 尽管"起步"看起来更慢，总体反而更快

**Boris Cherny 工作流**：

> "我运行很多会话，从计划模式开始，一旦计划看起来正确就切换到执行。关键的升级是验证——给 Claude 一种测试和确认自己输出的方式。"

**相对于"直接开始编码"的优势**：

- **更少的修正迭代**：计划在问题变成代码之前就捕获它们
- **更好的架构**：被迫先思考结构
- **更清晰的沟通**：计划成为与团队/Claude 共享的理解
- **更低的成本**：一次干净的迭代 < 多次混乱的迭代（即使计划阶段消耗 token）

**与 CLAUDE.md 的集成**：

在你的 CLAUDE.md 中记录团队的计划优先触发条件：
```markdown
## 规划策略
- 始终先规划：API 变更、数据库迁移、新功能
- 可选规划：<10 行的 bug 修复、测试补充
- 绝不能跳过：影响 >2 个模块的变更
```

**另请参见**：[计划模式文档](#23-计划模式)了解 `/plan` 命令使用方法。

> **高级模式**：关于基于迭代注解的计划驱动开发方法，请参见[自定义 Markdown 计划（Boris Tane 模式）](../workflows/plan-driven.md#advanced-custom-markdown-plans-boris-tane-pattern)。

---

### 第 2 层：规约与架构

| 名称 | 是什么 | 最适合 | Claude 适配度 |
|------|--------|-------|-------------|
| **SDD** | 先规约后代码 | API、契约 | ⭐⭐⭐ 核心模式 |
| **文档驱动** | 文档 = 真实来源 | 跨团队对齐 | ⭐⭐⭐ CLAUDE.md 原生 |
| **需求驱动** | 丰富的制品上下文（20+ 制品） | 复杂需求 | ⭐⭐ 设置成本高 |
| **DDD** | 领域语言优先 | 业务逻辑 | ⭐⭐ 设计时 |

**SDD（Spec-Driven Development）** — 代码之前先写规约。一次结构良好的迭代等于 8 次无结构的迭代。CLAUDE.md 就是你的规约文件。

**文档驱动开发（Doc-Driven Development）** — 在 git 中版本化的活文档成为单一真实来源。规约变更触发实现。

**需求驱动开发（Requirements-Driven Development）** — 使用 CLAUDE.md 作为全面的实现指南，包含 20+ 个结构化制品。

**DDD（Domain-Driven Design）** — 通过以下方式使软件与业务语言对齐：
- 通用语言：代码中的共享词汇
- 有界上下文：隔离的领域边界
- 领域提炼：核心 vs 支撑 vs 通用领域

---

### 第 3 层：行为与验收

| 名称 | 是什么 | 最适合 | Claude 适配度 |
|------|--------|-------|-------------|
| **BDD** | Given-When-Then 场景 | 利益相关者协作 | ⭐⭐⭐ 测试和规约 |
| **ATDD** | 验收标准优先 | 合规、受监管 | ⭐⭐ 流程重 |
| **CDD** | API 契约作为接口 | 微服务 | ⭐⭐⭐ OpenAPI 原生 |

**BDD（Behavior-Driven Development）** — 超越测试：一个协作过程。
1. 发现：让开发者和业务专家参与
2. 形式化：编写 Given-When-Then 示例
3. 自动化：转换为可执行测试（Gherkin/Cucumber）

```gherkin
Feature: 订单管理
  Scenario: 无库存时不能购买
    Given 产品库存为 0
    When 客户尝试购买
    Then 系统拒绝并显示错误消息
```

**ATDD（Acceptance Test-Driven Development）** — 编码之前先定义验收标准，协作进行（"三剑客"：业务、开发、测试）。

在智能体开发中，ATDD 特别有效，因为智能体需要明确的成功条件。工作流可以清晰地映射到智能体任务：

1. **用 Gherkin 定义验收标准**（人类可读、机器可执行）
2. **智能体根据场景编写失败的测试**（不是实现）
3. **智能体进行实现**直到测试通过

```gherkin
Feature: 密码重置
  Scenario: 用户通过邮件重置
    Given 已注册用户，邮箱为 "user@example.com"
    When 他们请求密码重置
    Then 他们在 60 秒内收到重置邮件
    And 重置链接在 24 小时后过期
```

这个 Gherkin 场景是意图和实现之间的契约。智能体无法误解范围，因为在写一行代码之前就已经定义了"完成"。

> **应用到智能体**：在实现之前将 Gherkin 文件传给 Claude Code。"为这个功能文件编写失败的测试，然后实现直到测试通过。"场景编写者角色（人类或智能体）在执行开始前强制明确范围。

**CDD（Contract-Driven Development）** — API 契约（OpenAPI 规约）作为团队之间的可执行接口。模式：契约即测试、契约即桩。

**JiTTesting（Just-in-Time Testing）** — 在 PR 提交时即时生成测试，设计为失败，合并后丢弃。无维护成本、无测试套件增长。

TDD/BDD/ATDD 都假设开发者控制代码编写的速度。智能体开发打破了这一假设：一个智能体每小时可以生成 200 行代码，快于任何人类测试编写工作流的跟进速度。JiTTest 是针对这种不匹配的工业级响应。

机制：在 PR 时，LLM 推断 diff 的意图，生成代码突变（故意破坏的变体），编写捕获这些突变的测试，运行基于规则的集成和 LLM 评估器来过滤误报，仅向工程师呈现真正的回归。测试永远不进入代码库。

Meta 在大规模部署了这一点（1 亿+ 行代码）：捕获回归的能力比传统强化测试提升 4 倍，人类审查负载减少 70%，41 个候选审查中阻止了 4 个严重生产故障。

目前尚无开源实现。你可以近似实现：在合并任何智能体生成的 PR 之前，提示 Claude"为这个 diff 可能引入的回归生成测试——我会在本地运行，PR 合并后丢弃。"这种临时框架使测试生成聚焦于实际更改的内容，而非通用覆盖率。

> **参考**：[Meta 的即时回归测试生成](https://arxiv.org/abs/2601.22832) — Harman，2026。

---

### 第 4 层：功能交付

| 名称 | 是什么 | 最适合 | Claude 适配度 |
|------|--------|-------|-------------|
| **FDD** | 逐功能交付 | 功能团队，并行交付 | ⭐⭐ 结构 |
| **上下文工程** | 上下文作为一等设计要素 | 长时间会话 | ⭐⭐⭐ 基础 |

**FDD（Feature-Driven Development）** — 五个流程：
1. 开发整体模型
2. 构建功能列表
3. 按功能规划
4. 按功能设计
5. 按功能构建

严格迭代：每个功能最长 2 周。

**上下文工程（Context Engineering）** — 将上下文视为设计要素：
- 渐进式披露：让智能体逐步发现
- 记忆管理：对话 vs 持久记忆
- 动态刷新：在响应前重写 TODO 列表

---

### 第 5 层：实现

| 名称 | 是什么 | 最适合 | Claude 适配度 |
|------|--------|-------|-------------|
| **TDD** | 红-绿-重构 | 高质量代码 | ⭐⭐⭐ 核心工作流 |
| **评估驱动** | 对 LLM 输出进行评估 | AI 产品 | ⭐⭐⭐ 智能体 |
| **多智能体** | 编排子智能体 | 复杂任务 | ⭐⭐⭐ Task 工具 |

**TDD（Test-Driven Development）** — 经典循环：
1. **红**：编写会失败的测试
2. **绿**：编写最少代码使其通过
3. **重构**：清理代码，测试保持绿色

使用 Claude 时：要明确。"编写尚不存在的**会失败的**测试。"

> **验证循环** — 一个用于自主迭代的正式化模式（比 TDD 更广泛）：
>
> **核心原则**：给 Claude 一种验证自己输出的机制。
>
> ```
> 代码生成 → 验证工具 → 反馈循环 → 改进
> ```
>
> **为什么有效**（Boris Cherny）：*"能'看到'自己做了什么事的智能体产出更好的结果。"*
>
> **按领域的验证机制**：
>
> | 领域 | 验证工具 | Claude "看到"什么 |
> |------|---------|-----------------|
> | **前端** | 浏览器预览（实时重载） | 视觉渲染、布局、交互 |
> | **后端** | 测试（单元/集成） | 通过/失败状态、错误消息 |
> | **类型** | TypeScript 编译器 | 类型错误、不兼容 |
> | **风格** | 代码检查（ESLint、Prettier） | 风格违规、格式问题 |
> | **性能** | 分析器、基准测试 | 执行时间、内存使用 |
> | **无障碍** | axe-core、屏幕阅读器 | WCAG 违规、导航问题 |
> | **安全** | 静态分析器（Semgrep） | 漏洞模式 |
> | **UX** | 用户测试、录制 | 可用性问题、困惑点 |
>
> **TDD 作为典型示例**：
> 1. Claude 为该功能编写测试
> 2. Claude 迭代代码直到测试通过
> 3. 持续直到满足明确的完成标准
>
> **官方指导**：*"告诉 Claude 一直进行到所有测试通过。通常需要几次迭代。"* — [Anthropic 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices)
>
> **实现模式**：
> - **钩子**：每次编辑后 PostToolUse 钩子运行验证
> - **浏览器扩展**：Chrome 中的 Claude 看到渲染输出
> - **测试监视器**：Jest/Vitest 监视模式提供即时反馈
> - **CI/CD 门禁**：GitHub Actions 运行完整验证套件
> - **双 Claude 验证**：一个 Claude 编码，另一个审查
>
> **反模式**：无反馈的盲目迭代。没有验证机制，Claude 无法收敛到正确的解决方案——它只能猜测。

关于这防止的实现侧故障模式，请参见 TDD 工作流中的[验证差距](../workflows/tdd-with-claude.md#the-verification-gap)。

**评估驱动开发（Eval-Driven Development）** — 面向 LLM 的 TDD。通过评估测试智能体行为：
- 基于代码的：`output == golden_answer`
- 基于 LLM 的：另一个 Claude 评估
- 人工评分：参考，较慢

> **评估框架**——端到端运行评估的基础设施：提供指令和工具、并发运行任务、记录步骤、评分输出和汇总结果。
>
> 请参见 Anthropic 的全面指南：[AI 智能体评估揭秘](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**多智能体编排（Multi-Agent Orchestration）** — 从单一助手到编排团队：
```
元智能体（编排器）
├── 分析师（需求）
├── 架构师（设计）
├── 开发者（代码）
└── 审查者（验证）
```

### ADR 驱动开发

**模式**：编写纯英文 ADR → 提供给 implement-adr 技能 → 在原生环境中执行

架构决策记录（ADR）与 Claude Code 技能的结合创建了一种工作流，其中架构决策直接驱动实现。

**工作流步骤**：
1. 以 ADR 格式**记录决策**（上下文、决策、后果）
2. **创建实现技能**（通用的或专门的 `implement-adr`）
3. **将 ADR 作为提示词**提供给技能，附带明确的验收标准
4. **Claude 执行**基于 ADR 中的架构指导

**ADR 模板示例**：
```
# ADR-001：数据库迁移策略

## 上下文
遗留 MySQL 模式需要迁移到 PostgreSQL 以获得更好的 JSON 支持。

## 决策
使用增量双写模式配合功能标志。

## 后果
- 正面：零停机迁移
- 负面：过渡期间临时代码复杂度
```

**实现工作流**：
```bash
# 1. 编写 ADR（纯英文）
vim docs/adr/001-database-migration.md

# 2. 提供给实现技能
/implement-adr docs/adr/001-database-migration.md

# 3. Claude 根据 ADR 指导执行
# → 创建迁移脚本
# → 更新 ORM 配置
# → 添加功能标志
# → 实现双写逻辑
```

**优势**：
- ✅ **文档驱动**：架构和代码保持同步
- ✅ **原生执行**：无需外部框架
- ✅ **可追溯的决策**：从决策到实现的清晰审计记录
- ✅ **团队对齐**：ADR 向人类和 AI 传达意图

**来源**：[Gur Sannikov 嵌入式工程工作流](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

### 第 6 层：优化

| 名称 | 是什么 | 最适合 | Claude 适配度 |
|------|--------|-------|-------------|
| **迭代循环** | 自主优化 | 优化 | ⭐⭐⭐ 核心 |
| **新上下文** | 每任务重置，状态在文件中 | 长时间自主会话 | ⭐⭐⭐ 高级用户 |
| **提示工程** | 技术基础 | 一切 | ⭐⭐⭐ 先决条件 |

**迭代优化循环** — 自主收敛：
1. 执行提示
2. 观察结果
3. 如果结果 ≠ "完成" → 优化并重复

**提示工程（Prompt Engineering）** — 所有 Claude 使用的基础：
- 零样本思维链："一步步思考"
- 少样本学习：2-3 个预期模式的示例
- 结构化提示：用于组织的 XML 标签
- 位置很重要：对于长文档，将问题放在末尾

**新上下文模式（Ralph 循环）** — 通过每任务生成全新的智能体实例来解决上下文腐烂问题。状态持久化在 git + 进度文件中，而非聊天历史。适合长时间自主会话（迁移、夜间运行）。参见[终极指南 - 新上下文模式](#fresh-context-pattern-ralph-loop)了解实现。

---

## SDD 工具参考

已有三种工具专门用于形式化规约驱动开发：

| 工具 | 使用场景 | 官方文档 | Claude 集成 |
|------|---------|---------|-------------|
| **Spec Kit** | 新建项目、治理 | [github.blog/spec-kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | `/speckit.constitution`、`/speckit.specify`、`/speckit.plan` |
| **OpenSpec** | 现有项目、变更 | [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | `/openspec:proposal`、`/openspec:apply`、`/openspec:archive` |
| **Specmatic** | API 契约测试 | [specmatic.io](https://specmatic.io) | 提供 MCP 智能体 |
| **Spec-to-Code Factory** | 新建项目、配套执行 | [github.com/SylvainChabaud/spec-to-code-factory](https://github.com/SylvainChabaud/spec-to-code-factory) | 多智能体参考实现（BREAK→MODEL→ACT→DEBRIEF） |

### Spec Kit（新建项目）

5 阶段工作流：
1. 章程：`/speckit.constitution` → 护栏
2. 规约：`/speckit.specify` → 需求
3. 计划：`/speckit.plan` → 架构
4. 任务：`/speckit.tasks` → 分解
5. 实现：`/speckit.implement` → 代码

### OpenSpec（现有项目）

双文件夹架构：
```
openspec/
├── specs/      ← 当前事实（稳定）
└── changes/    ← 提案（临时）
```

工作流：提案 → 审查 → 应用 → 归档

### Specmatic（API 契约）

- **契约即测试**：从 OpenAPI 规约自动生成数千个测试
- **契约即桩**：用于并行开发的模拟服务器
- **向后兼容**：检测破坏性变更

---

## 编写有效规约

> 基于对 2,500+ 个智能体配置文件的元分析。
> 来源：[Addy Osmani](https://addyosmani.com/blog/good-spec/)

### 六个必要组件

| 组件 | 包含什么 | 示例 |
|------|---------|------|
| **命令** | 带标志的可执行命令 | `npm test -- --coverage` |
| **测试** | 框架、覆盖率、位置 | `vitest, 80%, tests/` |
| **项目结构** | 明确的目录 | `src/`、`lib/`、`tests/` |
| **代码风格** | 一个示例胜过段落 | 展示一个真实的函数 |
| **Git 工作流** | 分支、提交、PR 格式 | `feat/name`、常规提交 |
| **边界** | 权限层级 | 见下方 |

### 权限层级

| 层级 | 符号 | 用途 |
|------|------|------|
| 始终做 | ✅ | 安全操作，无需批准（lint、format） |
| 先问 | ⚠️ | 高影响变更（删除、发布） |
| 绝不做 | 🚫 | 硬边界（提交密钥、force push 主分支） |

### 指令的诅咒

> ⚠️ 研究表明**指令越多 = 每条指令的遵守程度越低**。
>
> 解决方案：每任务只提供相关的规约部分，而不是整个文档。

### 单体 vs 模块化规约

| 项目规模 | 方法 |
|---------|------|
| 小（<10 个文件） | 单个规约文件 |
| 中（10-50 个文件） | 分节规约，每任务提供相关部分 |
| 大（50+ 个文件） | 按领域的子智能体路由 |

---

## 组合模式

按场景推荐的组合：

| 场景 | 推荐组合 | 备注 |
|------|---------|------|
| 单 MVP | SDD + TDD | 最少开销，质量聚焦 |
| 5-10 人团队，新建项目 | Spec Kit + TDD + BDD | 治理 + 质量 + 协作 |
| 微服务 | CDD + Specmatic | 契约优先，并行开发 |
| 现有 SaaS（100+ 功能） | OpenSpec + BDD | 变更追踪，无规约漂移 |
| 高复杂度 / 合规 | BMAD + Spec Kit + Specmatic | 完整治理 + 契约 |
| LLM 原生产品 | 评估驱动 + 多智能体 | 自改进系统 |

---

## 快速参考表

| 方法论 | 层级 | 主要关注点 | 最佳上下文 | 学习曲线 |
|---------|------|-----------|-----------|---------|
| BMAD | 编排 | 治理 | 高复杂度、需求稳定 | 高 |
| SDD | 规约 | 契约 | 任何 | 中 |
| 文档驱动 | 规约 | 对齐 | 任何 | 低 |
| 需求驱动 | 规约 | 上下文 | 复杂需求、多制品 | 中 |
| DDD | 规约 | 领域 | 复杂业务领域 | 非常高 |
| BDD | 行为 | 协作 | 多角色利益相关者参与 | 中 |
| ATDD | 行为 | 合规 | 受监管、明确验收标准 | 中 |
| CDD | 行为 | API | 服务边界、并行团队 | 中 |
| FDD | 交付 | 功能 | 功能团队、并行交付 | 中 |
| 上下文工程 | 交付 | AI 会话 | 任何 | 低 |
| TDD | 实现 | 质量 | 任何 | 低 |
| 评估驱动 | 实现 | AI 输出 | 任何 | 中 |
| 多智能体 | 实现 | 复杂度 | 任何 | 中 |
| 迭代 | 优化 | 优化 | 任何 | 低 |
| 提示工程 | 优化 | 基础 | 任何 | 非常低 |

---

## 来源

### 官方文档（第一层）

- Anthropic：[Claude Code 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices)
- Anthropic：[AI 智能体的有效上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic：[AI 智能体评估揭秘](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- GitHub：[规约驱动开发工具包](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- Microsoft：[使用 Spec Kit 进行规约驱动开发](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)

### 方法论参考（第二层）

**SDD 与规约优先**
- Addy Osmani：[如何为 AI 智能体编写好的规约](https://addyosmani.com/blog/good-spec/)
- Addy Osmani：[2026 年我的 AI 编码工作流](https://addyosmani.com/blog/ai-coding-workflow/) — 端到端工作流：规约优先、上下文打包、TDD、git 检查点
- Martin Fowler：[SDD 工具分析](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- InfoQ：[规约驱动开发](https://www.infoq.com/articles/spec-driven-development/)
- Kinde：[超越 TDD——为什么 SDD 是下一步](https://kinde.com/learn/ai-for-software-engineering/best-practice/beyond-tdd-why-spec-driven-development-is-the-next-step/)
- Tessl.io：[使用 Claude Code 进行规约驱动开发](https://tessl.io/blog/spec-driven-dev-with-claude-code/)

**BMAD**
- GMO Recruit：[BMAD 方法](https://recruit.group.gmo/engineer/jisedai/blog/the-bmad-method-a-framework-for-spec-oriented-ai-driven-development/)
- Benny Cheung：[BMAD - 在 AI 开发中重获控制](https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev)
- GitHub：[BMAD-AT-CLAUDE](https://github.com/24601/BMAD-AT-CLAUDE)

**与 AI 配合 TDD**
- Steve Kinney：[使用 Claude 进行 TDD](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)
- Nathan Fox：[驯服 GenAI 智能体](https://www.nathanfox.net/p/taming-genai-agents-like-claude-code)
- Alex Op：[自定义 TDD 工作流 Claude Code](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)

**BDD 与 DDD**
- Alex Soyes：[BDD 行为驱动开发](https://alexsoyes.com/bdd-behavior-driven-development/)
- Alex Soyes：[DDD 领域驱动设计](https://alexsoyes.com/ddd-domain-driven-design/)
- Inflectra：[行为驱动开发](https://www.inflectra.com/Ideas/Topic/Behavior-Driven-Development.aspx)

**上下文工程**
- Intuition Labs：[什么是上下文工程](https://intuitionlabs.ai/articles/what-is-context-engineering)
- Manus.im：[AI 智能体的上下文工程](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

**评估驱动与多智能体**
- Fireworks AI：[使用 Claude Code 进行评估驱动开发](https://fireworks.ai/blog/eval-driven-development-with-claude-code)
- Brandon Casci：[使用 Claude Code 智能体变身开发团队](https://www.brandoncasci.com/2025/09/21/how-to-transform-yourself-into-a-dev-team-using-claude-codes-ai-agents.html)
- The Unwind AI：[Claude Code 的多智能体编排](https://www.theunwindai.com/p/claude-code-s-hidden-multi-agent-orchestration-now-open-source)

### 工具文档（第一层）

- OpenSpec：[github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- Spec Kit：[github.com/github/spec-kit](https://github.com/github/spec-kit)
- Specmatic：[specmatic.io](https://specmatic.io)
- Specmatic 文章：[使用 GitHub Spec Kit 和 Specmatic MCP 进行规约驱动开发](https://specmatic.io/article/spec-driven-development-api-design-first-with-github-spec-kit-and-specmatic-mcp/)

### 附加参考

- Talent500：[Claude Code TDD 指南](https://talent500.com/blog/claude-code-test-driven-development-guide/)
- Testlio：[验收测试驱动开发](https://testlio.com/blog/what-is-acceptance-test-driven-development/)
- Monday.com：[功能驱动开发](https://monday.com/blog/rnd/feature-driven-development-fdd/)
- Paddo.dev：[Ralph Wiggum 自主循环](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)
- Walturn：[Claude 的提示工程](https://www.walturn.com/insights/mastering-prompt-engineering-for-claude)
- AWS：[在 Bedrock 上使用 Claude 进行提示工程](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)

---

## 另请参见

- [workflows/tdd-with-claude.md](../workflows/tdd-with-claude.md) — 实践 TDD 指南
- [workflows/spec-first.md](../workflows/spec-first.md) — 规约优先开发
- [workflows/plan-driven.md](../workflows/plan-driven.md) — 使用 /plan 模式
- [workflows/iterative-refinement.md](../workflows/iterative-refinement.md) — 迭代优化循环
- [ultimate-guide.md#912](../ultimate-guide.md) — 第 9.12 节摘要


