<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "演讲准备管道：从想法到带 AI 的幻灯片"
description: "6 阶段技能管道，将原材料转化为带 AI 生成幻灯片的完整会议演讲"
tags: [workflow, skills, pipeline, presentation, ai-handoff]
---

# 演讲准备管道：从想法到带 AI 的幻灯片

> **可信度**：第 2 层 — 在真实会议演讲（DevWithAI Lyon，2026 年）上生产验证。

将原始文章、转录稿或笔记转化为完整的会议演讲——包括用于 AI 生成幻灯片的 Kimi 就绪提示词。六个阶段，两种模式，一个人工介入检查点。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用](#何时使用)
3. [先决条件](#先决条件)
4. [管道概述](#管道概述)
5. [分阶段指南](#分阶段指南)
6. [Kimi 交接](#kimi-交接)
7. [人工介入检查点](#人工介入检查点)
8. [管道适配](#管道适配)
9. [真实世界示例](#真实世界示例)
10. [常见陷阱](#常见陷阱)
11. [展示的设计模式](#展示的设计模式)
12. [另见](#另见)

---

## TL;DR

```
源材料（文章 / 转录稿 / 笔记）
        │
        ▼
[阶段 1] 提取 ─────────────── {slug}-summary.md
        │
        ├──────────────────────────────────────┐
        │                                      │
        ▼ (--rex only)                         ▼
[阶段 2] 研究                    [阶段 3] 概念
  git-archaeology.md              concepts.md
  changelog-analysis.md           concepts-enriched.md
  timeline.md                       │
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
              [阶段 4] 定位
                angles.md
                titre.md
                descriptions.md
                feedback-draft.md
                       │
                  [检查点]
             用户选择角度 + 标题
                       │
                       ▼
              [阶段 5] 脚本
                pitch.md
                slides.md
                kimi-prompt.md ──► 复制粘贴到 Kimi.com
                       │
                       ▼
             [阶段 6] 修订
              revision-sheets.md
```

两种模式：**REX**（带真实世界证明的演讲 — git 历史、指标）和 **Concept**（基于想法/论文 — 跳过阶段 2）。

---

## 何时使用

此管道适合当你有演讲要准备且有：

- **有 REX 讲**：你构建了一些东西，发布了，有真实指标 — 想把它变成结构化会议演讲
- **有概念要发展**：你有一篇文章、笔记或想法想变成结构化演示

适合的格式：
- 会议演讲（20-45 分钟）
- Meetup 演示（15-30 分钟）
- 内部技术演讲
- 工作坊开场

不适合： recurring 会议的幻灯片更新、10 分钟以下的短闪电演讲，或没有任何现有材料可处理的情况。

---

## 先决条件

**必需**：
- 已安装技能的 Claude Code（见 [examples/skills/talk-pipeline/](../../examples/skills/talk-pipeline/)）
- 源材料：`.mdx` 文章、`.md` 转录稿、笔记或混合
- 演讲元数据：slug、活动名称、日期、时长、受众描述

**仅限 REX 模式**：
- 要分析的 git 仓库访问权限
- 可选：如果不同于仓库根目录的 `CHANGELOG.md` 路径

**用于 Kimi 幻灯片生成（阶段 5 输出）**：
- [kimi.com](https://kimi.com) 的免费账户（无需 API — 只需复制粘贴）

**可选但推荐**：
- 项目根中的 `talks/` 目录用于输出文件
- 1-2 个可用的可信同伴用于反馈草稿（阶段 4）

---

## 管道概述

### 每种模式的输出文件

| 文件 | 阶段 | REX | Concept |
|------|-------|-----|---------|
| `{slug}-summary.md` | 1 | ✓ | ✓ |
| `{slug}-git-archaeology.md` | 2 | ✓ | — |
| `{slug}-changelog-analysis.md` | 2 | ✓ | — |
| `{slug}-timeline.md` | 2 | ✓ | — |
| `{slug}-concepts.md` | 3 | ✓ | ✓ |
| `{slug}-concepts-enriched.md` | 3 | ✓（如果有仓库）| — |
| `{slug}-angles.md` | 4 | ✓ | ✓ |
| `{slug}-titre.md` | 4 | ✓ | ✓ |
| `{slug}-descriptions.md` | 4 | ✓ | ✓ |
| `{slug}-feedback-draft.md` | 4 | ✓ | ✓ |
| `{slug}-pitch.md` | 5 | ✓ | ✓ |
| `{slug}-slides.md` | 5 | ✓ | ✓ |
| `{slug}-kimi-prompt.md` | 5 | ✓ | ✓ |
| `{slug}-revision-sheets.md` | 6 | ✓ | ✓ |

REX 模式：13-14 个文件。Concept 模式：10 个文件。

### 命名约定

所有输出遵循 `talks/{YYYY}-{slug}-{stage-label}.md`。2026 年 slug `devwithai` 的示例：

```
talks/2026-devwithai-summary.md
talks/2026-devwithai-git-archaeology.md
talks/2026-devwithai-concepts.md
talks/2026-devwithai-angles.md
...
```

---

## 分阶段指南

### 阶段 1：提取

**做什么**：读取源材料并产生结构化摘要 — 叙事弧线、关键指标、主要主题、差距。

| | |
|--|--|
| **输入** | 源文件 + 元数据（slug、活动、日期、时长、受众、模式）|
| **输出** | `{slug}-summary.md` |
| **使用的工具** | Read、Write、AskUserQuestion |
| **模式** | REX + Concept |

**关键规则**：
- 基于信号自动检测源类型（REX vs Concept）（日期、指标、"I shipped" vs "I think"）
- 提取每个可测量指标及其来源 — 不编造数字
- 明确标记差距而非隐藏

**调用**：
```
/talk-stage1-extract
```

或通过编排器：
```
/talk-pipeline --stage=extract --slug=my-talk --event="Conf 2026" --date=2026-06-15 --duration=30 --audience="senior devs"
```

**移动前审查**：
- 叙事弧线连贯（不是泛泛的："这个演讲是关于 AI..."）
- 所有指标有明确来源
- 差距已列出（即使只是"无重大差距"）
- 类型检测正确（REX / Concept / 混合）

---

### 阶段 2：研究（仅限 REX 模式）

**做什么**：Git 考古 — 提取速度指标、交叉引用 CHANGELOG、构建由 git 验证的事实时间线（不是估算）。

| | |
|--|--|
| **输入** | `{slug}-summary.md` + 仓库路径 |
| **输出** | `git-archaeology.md`、`changelog-analysis.md`、`timeline.md` |
| **使用的工具** | Bash（只读 git 命令）、Read、Write |
| **模式** | 仅限 REX — **在 Concept 模式中自动跳过** |

**关键规则**：
- 仅使用只读 git 命令 — 绝不修改仓库
- 在 git 中找不到的日期标记为"未验证" — 绝不估算
- 来源之间的矛盾被标记，不静默解决

**使用的 Git 命令**（仅读）：
```bash
git log --pretty=format:"%Y-%m" | sort | uniq -c   # 按月速度
git shortlog -sn --no-merges                         # 贡献者
git tag --sort=version:refname                       # 发布
git log --merges --oneline | wc -l                   # 合并的 PR
```

**移动前审查**：
- 时间线覆盖摘要中的完整时间段
- 无估算日期 — 全部验证
- 速度峰值有上下文注释

---

### 阶段 3：概念

**做什么**：构建材料中所有概念的有编号、有评分的目录。每个概念获得演讲潜力评分（HIGH / MEDIUM / LOW）。

| | |
|--|--|
| **输入** | `{slug}-summary.md` + `{slug}-timeline.md`（可选）|
| **输出** | `{slug}-concepts.md`、如果仓库可用则加 `{slug}-concepts-enriched.md` |
| **使用的工具** | Read、Write |
| **模式** | REX + Concept |

**评分标准**：
- **HIGH**：可演示、反直觉、有验证数字、30 秒内可操作
- **MEDIUM**：有用但可预期、缺少证明或数字
- **LOW**：太抽象、过度覆盖、难以在幻灯片上说明

**评分纪律**：最多 30% HIGH — 选择性是重点。

**移动前审查**：
- 识别 15+ 个概念（带仓库访问权限的 REX 为 20+）
- 评分已校准（不全 HIGH，不全 LOW）
- 每个概念有 1-2 句具体描述

---

### 阶段 4：定位 + 检查点

**做什么**：生成战略角度、标题、描述和同行反馈草稿。然后**停止并等待**你的角度 + 标题选择。

| | |
|--|--|
| **输入** | `{slug}-summary.md` + `{slug}-concepts.md` + 活动约束 |
| **输出** | `angles.md`、`titre.md`、`descriptions.md`、`feedback-draft.md` |
| **使用的工具** | Read、Write、AskUserQuestion |
| **模式** | REX + Concept |

**生成的内容**：
- **3-4 个角度**：每个带 force、弱点、受众契合度、评分（/5）和 verdict
- **推荐**：一个带结构化理由的明确选择
- **每个角度 3-5 个标题**
- **描述短**（约 100 词摘要）+ **描述长**（约 250 词 CFP）
- **反馈草稿**：用于同行验证的随时可发送消息（3 种格式：Slack DM、email、LinkedIn 帖子）

**检查点显示**（阶段 5 前的强制项）：

```
---
检查点：角度 + 标题选择

我生成了 4 个文件：
- talks/{YYYY}-{slug}-angles.md    → 分析的 {n} 个角度
- talks/{YYYY}-{slug}-titre.md     → {n} 个标题选项
- talks/{YYYY}-{slug}-descriptions.md
- talks/{YYYY}-{slug}-feedback-draft.md

在启动脚本（阶段 5）之前，我需要你的选择：

1. 你保留哪个角度？（推荐：角度 {X} — {名称}）
2. 你更喜欢哪个标题？（推荐："{标题}"）

你也可以修改、混合或提出其他内容。
---
```

**阶段 5 不能在没有明确用户确认的情况下开始。**

**确认前审查**：
- 你已阅读反馈草稿，可选发送给同行
- 推荐角度可以在没有重复的情况下支撑完整时长
- 标题具体（无术语、无点击诱饵）

---

### 阶段 5：脚本

**做什么**：以 5 幕结构构建完整演讲，带演讲者笔记、幻灯片规范和 Kimi 提示词。

| | |
|--|--|
| **输入** | summary + concepts + timeline（可选）+ **已验证角度 + 标题** |
| **输出** | `{slug}-pitch.md`、`{slug}-slides.md`、`{slug}-kimi-prompt.md` |
| **使用的工具** | Read、Write |
| **模式** | REX + Concept |

**三个交付物**：

1. **`pitch.md`**：带演讲者笔记的 5 幕叙事、计时、关键时刻。你说的 — 不是从幻灯片读的。

2. **`slides.md`**：逐幻灯片规范：标题、视觉描述、关键文本（≤30 词）、演讲者笔记、时长、幕数。随时可交给设计师或传递给 Kimi。

3. **`kimi-prompt.md`**：[kimi.com](https://kimi.com) 的完整提示词 — 包括设计系统、颜色调色板、排版规范、完整幻灯片内容和截图占位符。复制粘贴就绪。

**每幻灯片一个想法规则**：如果幻灯片需要"和"来描述它，将其拆分。

**移动前审查**：
- 计时检查：总计 ≤ 时长 + 10% buffer
- 演讲者笔记朗读自然（大声测试这个）
- Kimi 提示词没有 `{PLACEHOLDER}` 未填写

---

### 阶段 6：修订

**做什么**：产生演讲期间和之后的修订表 — 按幕快速导航、主概念表、Q&A 速查表、术语表。

| | |
|--|--|
| **输入** | `pitch.md` + `slides.md` + `concepts.md` |
| **输出** | `{slug}-revision-sheets.md` |
| **使用的工具** | Read、Write |
| **模式** | REX + Concept |

**修订表包含**：
- **导航**按幕带锚链接
- **每幕分解**：关键概念 + 指标 + 轶事 + 可能 Q&A
- **主表**：概念 → 1-2 句定义 → 可共享 URL
- **Q&A 速查表**：6-10 个可能问题带简短答案（≤20 秒）
- **指标块**：所有数字在一处
- **外部资源**：演讲中提到的链接
- **术语表**：技术术语，最多 10 词每个

**目的**：有人问问题 → 找到章节 → 5 秒内共享 URL。

---

## Kimi 交接

阶段 5 生成 `{slug}-kimi-prompt.md` — [kimi.com](https://kimi.com) 的完整提示词。

**用它做什么**：
1. 打开生成的文件
2. 验证没有 `{PLACEHOLDER}` 剩余（搜索文件）
3. 去 [kimi.com](https://kimi.com) — 免费账户，无需 API
4. 开始新对话
5. 复制粘贴整个提示词
6. Kimi 生成演示（PowerPoint 或 PDF）

**与 Kimi 迭代**：
- 首次生成后，对照 `slides.md` 规范审查幻灯片
- 添加跟进消息用于个别调整："幻灯片 7：让数字更大，删除项目符号列表"
- 对于截图：导出后在 `SCREENSHOT AREA` 占位符处手动替换

**嵌入模板的设计系统**：
- 暗色主题（#0a0a0a 背景）
- 橙色强调（#f97316）用于关键数字和 CTA
- Inter/SF Pro 排版
- 每幻灯片最多 30 词，数字作为主角
- WCAG AA 对比度（投影仪安全）

**为什么是 Kimi？** 在撰写时，Kimi 从详细提示词生成高质量会议演示优于大多数替代方案。模板是 Kimi 调优的，但设计系统和幻灯片结构适用于任何 AI 演示工具。

---

## 人工介入检查点

管道有两个人工检查点：

### 检查点 1：阶段 1 元数据收集

如果演讲元数据（slug、活动、日期、时长、受众、模式）未预先提供，阶段 1 使用 `AskUserQuestion` 在继续之前收集它们。这避免生成你会丢弃的摘要。

### 检查点 2：阶段 4 — 角度 + 标题选择（强制）

这是管道的关键门禁。阶段 5 不能在没有明确人工选择的情况下开始。

**为什么重要**：角度和标题决定接下来的一切 — 5 幕结构、哪些概念浮现、Kimi 提示词语气。在这里自动化选择会产生通用演讲。这一决定必须是你的。

**在检查点做什么**：
1. 阅读 `angles.md` — 不要跳过它，推荐可能对你的上下文错误
2. 可选将 `feedback-draft.md` 发送给可信同行（需要 10 分钟，节省 2 小时返工）
3. 回复你的选择（可以是推荐、修改或完全不同）

---

## 管道适配

### 闪电演讲（10-15 分钟）

- 保留阶段 1、3、4、5 — 即使在 REX 模式也跳过阶段 2
- 阶段 3：限制 8-10 个概念（无情过滤为仅 HIGH）
- 阶段 4：最多生成 2 个角度
- 阶段 5：目标约 8-10 张幻灯片，约 2 分钟/幻灯片
- 跳过阶段 6（短格式不需要）

### 45 分钟演讲

- 完整管道，所有阶段
- 阶段 3：目标 25-35 个概念（给你足够填充 5 个坚实幕的内容）
- 阶段 5：20-25 张幻灯片，允许 3 分钟/幻灯片平均
- 阶段 6 变得关键（Q&A 持续 10-15 分钟）

### 工作坊（90+ 分钟）

- 运行管道到阶段 4
- 阶段 5：用活动规范替换 slides.md（练习、计时、分组）
- Kimi 提示词部分变为可选（对工作坊材料相关性较低）

### 没有 git 仓库可用（无代码的 REX）

- 如果你有来自其他来源的指标（分析、仪表板、事件报告）使用 `--rex` 模式
- 阶段 2：用那些来源的手动数据收集替换 git 命令
- 在 sourcing 上更严格 — "未验证"指标在演讲中不能存活

---

## 真实世界示例

**演讲**："Dev with AI" REX — 我们如何用 AI 工具在 7 个月内发布了一个复杂项目

**模式**：REX
**活动**：DevWithAI Lyon，2026 年 2 月
**时长**：30 分钟
**源材料**：12,000 词的 `.mdx` 文章

**生成的文件（16 个总计）**：

```
talks/2026-devwithai-summary.md              （阶段 1）
talks/2026-devwithai-git-archaeology.md      （阶段 2）
talks/2026-devwithai-changelog-analysis.md   （阶段 2）
talks/2026-devwithai-timeline.md             （阶段 2）
talks/2026-devwithai-concepts.md             （阶段 3）
talks/2026-devwithai-concepts-enriched.md    （阶段 3）
talks/2026-devwithai-angles.md               （阶段 4）
talks/2026-devwithai-titre.md                （阶段 4）
talks/2026-devwithai-descriptions.md         （阶段 4）
talks/2026-devwithai-feedback-draft.md       （阶段 4）
talks/2026-devwithai-pitch.md                （阶段 5）
talks/2026-devwithai-slides.md               （阶段 5）
talks/2026-devwithai-kimi-prompt.md          （阶段 5）
talks/2026-devwithai-revision-sheets.md      （阶段 6）
```

**阶段 2 暴露的关键指标**：
- 7 个月内 1,200 次提交（用 `git log` 验证）
- 3 个主要贡献者
- 特定迁移后流量减少 97%（来自 CHANGELOG v1.1.0）
- 第 4 个月速度峰值（正常节奏的 2 倍）

**选择的角度**（从 3 个生成）："构建者之旅" — REX 角度，展示用 AI 工具构建数月的真实体验，而非功能演示

**Kimi 输出**：暗色主题幻灯片组，20 张，以数字为主角的设计，约 90 秒生成

---

## 常见陷阱

### 没有来源的指标

阶段 1 提取指标但不验证。阶段 2 验证。如果你在 Concept 模式，演讲中提到的任何指标必须在摘要中明确 sourcing — 或删除。观众会问"那个数字从哪里来的？""我查过了"不是答案。

### 幻灯片过载

Kimi 提示词强制每幻灯片 30 词，但你可能在阶段 5 写的 pitch.md 漂移到项目符号列表。测试每幻灯片一个想法规则：如果你需要"和"来描述幻灯片内容，拆分它。

### 跳过检查点

在没有验证角度 + 标题的情况下运行阶段 5 会为错误的演讲产生技术正确的脚本。阶段 4 的推荐是好的起点，不是最终答案 — 你的受众知识很重要。

### 反馈草稿发送太晚

反馈草稿在阶段 4 生成，在脚本存在之前。这是故意的 — 在角度/标题阶段的同行反馈是可操作的。完成脚本上的反馈大多产生后悔。

### 通用演讲者笔记

`pitch.md` 中的演讲者笔记应该读作自然语音。如果你发现自己写"在这张幻灯片上，我们讨论..."，重写为你实际对房间说的内容。Kimi 提示词复制这些笔记 — 它们需要会话式。

---

## 展示的设计模式

此管道从 Claude Code 角度有趣，因为它在一个连贯系统中展示了几个高级模式。

### 带基于文件的状态的技能链接

每个阶段写入下个阶段读取的文件。状态通过文件系统在技能调用之间持久化 — 无内存耦合。你可以在阶段 2 一周后运行阶段 3 而不丢失上下文。

```
阶段 1 → 写入 {slug}-summary.md
阶段 2 → 读取 {slug}-summary.md → 写入 3 个新文件
阶段 3 → 读取 summary + timeline → 写入 2 个新文件
...
```

### 工具权限范围

阶段 2 是唯一需要 Bash 的阶段（用于 git 命令）。其他每个阶段仅 Read + Write。这是故意的 — 每阶段最小占用意味着更少的错误面。

```yaml
# 仅阶段 2
allowed-tools:
  - Write
  - Read
  - Bash
```

### 人工介入门禁

阶段 4 使用 `AskUserQuestion` 呈现检查点 — 不是作为便利，而是作为结构要求。技能不会在没有明确人工响应的情况下继续到阶段 5。这是"Claude 提议，人工决定"的模式。

### AI 到 AI 交接

阶段 5 为第二个 AI 系统（Kimi）生成提示词。Claude 不直接生成幻灯片 — 它生成另一个 AI 执行的规范。这个模式让你组合优势：Claude 用于结构化叙事推理，Kimi 用于视觉演示生成。

```
Claude（阶段 5）→ kimi-prompt.md → Kimi.com → slides.pptx
```

### 带条件阶段跳过的两种执行模式

`--rex` / `--concept` 标志控制哪些阶段运行。阶段 2 在 Concept 模式中自动跳过。编排器（`/talk-pipeline`）处理路由 — 单独阶段技能是模式无关的。

---

## 另见

- **技能模板**：[`examples/skills/talk-pipeline/`](../../examples/skills/talk-pipeline/)
- **PDF 生成工作流**：[`guide/workflows/pdf-generation.md`](./pdf-generation.md) — 从演讲内容生成讲义
- **规范优先工作流**：[`guide/workflows/spec-first.md`](./spec-first.md) — 与 Claude 结构化工作的互补模式
- **技能结构参考**：[`examples/skills/skill-creator/SKILL.md`](../../examples/skills/skill-creator/SKILL.md)

---

**最后更新**：2026 年 2 月