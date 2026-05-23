<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "Claude Code 工作流"
description: "使用 Claude Code 的常见开发模式分步指南"
tags: [workflow, guide, reference]
---

# Claude Code 工作流

使用 Claude Code 的常见开发模式分步指南。

---

## 🔍 搜索与探索

### [搜索工具精通](./search-tools-mastery.md) ⭐ 新增

**通过组合 rg、grepai、Serena 和 ast-grep 掌握代码搜索艺术**

学习何时使用每个工具、如何组合使用以获得最大效率，以及包括以下内容的真实工作流：
- 探索未知代码库
- 大规模重构
- 安全审计
- 框架迁移
- 性能优化

**关键主题**：
- 快速决策矩阵
- 完整功能对比
- 5 个组合工作流
- 性能基准
- 常见陷阱
- 工具选择速查表

---

## 🎯 开发工作流

### [计划驱动开发](./plan-driven.md)

执行前先用计划模式结构化复杂任务。

**何时使用**：多步骤功能、架构变更、方案不确定

### [使用 Claude 进行 TDD](./tdd-with-claude.md)

测试驱动开发工作流：先写测试，后实现。

**何时使用**：关键功能、回归预防、API 设计

### [规范优先开发](./spec-first.md)

代码前先写规范，以获得更清晰的需求。

**何时使用**：团队协作、复杂功能、文档先行项目

### [迭代优化](./iterative-refinement.md)

通过多个优化循环改进代码。

**何时使用**：质量改进、性能优化、代码清理

### [脚手架项目](./skeleton-projects.md) ⭐ 新增

使用已有的、经过实战检验的仓库作为新项目的脚手架。

**何时使用**：启动新项目、标准化团队模式、从可靠基础快速原型

### [团队 AI 指令](./team-ai-instructions.md)

通过基于配置文件的模块组装跨多开发者、多工具团队扩展 CLAUDE.md。

**何时使用**：5 人以上团队、多个 AI 工具（Claude Code + Cursor/Windsurf）、混合操作系统

### [变更日志片段](./changelog-fragments.md) ⭐ 新增

**通过三层系统强制每个 PR 文档化：CLAUDE.md 规则 + UserPromptSubmit 钩子 + CI 门禁**

消除 `CHANGELOG.md` 上的合并冲突，在实现时捕获上下文，确保数据库迁移永远不会被静默部署。包括一个可复用的 `UserPromptSubmit` 钩子模式，用于强制任何必选工作流步骤。

**关键主题**：
- 用于自主创建片段的 CLAUDE.md 工作流规则
- 三层优先级的 `UserPromptSubmit` 钩子（强制、发现、上下文）
- 条件建议模式："如果有 PR 意图但未提及片段"
- 带独立迁移检查作业的 CI 强制执行

### [RPI：研究 → 计划 → 实现](./rpi.md) ⭐ 新增

**三阶段功能开发，各阶段之间有明确的验证门禁**

以三个锁定阶段构建功能：先研究可行性，再计划实现，最后写代码。每个阶段产生一个具体产物（RESEARCH.md → PLAN.md → 代码）。每个门禁需要明确的 GO 才能进入下一阶段。

**何时使用**：可行性不明确的功能、工作量超过一天、不熟悉的技术领域，或在任何发现错误假设代价高昂的地方

### [GitHub Actions 工作流](./github-actions.md) ⭐ 新增

**5 个可用于生产环境的模式，用于自动化 PR 评审、问题分类和质量门禁**

通过官方 `claude-code-action` 将 Claude 直接连接到你的 GitHub 工作流。两种模式：交互式（`@claude` 提及）和完全自动化（push/定时触发）。

**关键主题**：
- 通过 `/install-github-app` 设置（30 秒快速开始）
- 模式 1：通过 `@claude` 提及按需 PR 评审
- 模式 2：每次 push 时自动评审
- 模式 3：问题分类和标签
- 模式 4：敏感路径的安全聚焦评审
- 模式 5：定时每周仓库健康检查
- 成本控制、并发、fork 安全

**何时使用**：任何想要 AI 驱动的代码评审而无需管理基础设施的团队

---

### [认知模式切换](./gstack-workflow.md) ⭐ 新增

在交付周期中切换专家角色：战略产品门禁、架构评审、多疑代码评审、自动化发布、本地浏览器 QA 和回顾。

**何时使用**：交付周期中需要在产品方向、工程严谨、评审和发布之间有明确分离，而不是一个通用助手处理所有阶段

---

## 🎨 设计与内容

### [设计转代码](./design-to-code.md)

将设计模型（Figma、线框图）转换为可用代码。

**何时使用**：前端开发、UI 实现、设计系统工作

### [OG 图片生成](./og-image-generation.md)

使用 Satori 和 resvg 在构建时动态生成社交预览图片。

**何时使用**：Astro 项目、保持社交预览准确而无需维护静态 PNG

### [PDF 生成](./pdf-generation.md)

使用 Quarto/Typst 和 Claude Code 生成专业 PDF。

**何时使用**：报告、文档、白皮书、技术文档

### [演讲准备管道](./talk-pipeline.md) ⭐ 新增

6 阶段技能管道：原材料 → 结构化演讲 → 通过 Kimi 生成 AI 幻灯片。

**何时使用**：会议演讲、meetup 演示、内部技术演讲——从文章、转录稿或笔记

### [TTS 设置](./tts-setup.md)

配置 Claude Code 响应的文字转语音（Agent Vibes 集成）。

**何时使用**：音频反馈、无障碍、免手动编码

---

## 🔬 代码探索

### [探索工作流](./exploration-workflow.md)

系统地探索和理解陌生的代码库。

**何时使用**：新项目、遗留代码、文档缺失

**相关**：高级多工具探索策略见 [搜索工具精通](./search-tools-mastery.md)。

---

## 多智能体与高级

### [智能体团队](./agent-teams.md)

编排多个专用智能体并行处理复杂任务。

**何时使用**：从并行、专业知识或独立验证中受益的任务

### [智能体团队快速入门](./agent-teams-quick-start.md)

在 30 分钟内设置第一个智能体团队的快速指南。

**何时使用**：多智能体模式新手、想在投入完整设置之前先尝试

### [双实例计划](./dual-instance-planning.md)

在两个协调的 Claude Code 实例中运行 Opus 进行计划，Sonnet 进行执行。

**何时使用**：需要深度推理的复杂功能架构、成本有效的执行

### [事件驱动智能体](./event-driven-agents.md)

通过钩子事件而非直接编排来协调智能体。

**何时使用**：响应式工作流、钩子触发的自动化、松耦合智能体管道

### [计划管道](./plan-pipeline.md)

完整的端到端计划管道：/plan-start、/plan-validate、/plan-execute 作为连贯工作流。

**何时使用**：任何在写代码前计划严谨性有回报的重要功能

### [任务管理](./task-management.md)

使用 TodoWrite、Tasks API 和跨会话上下文持久化的多会话任务跟踪。

**何时使用**：跨多个会话的长期运行任务、团队协调、复杂待办事项

---

## 快速选择指南

| 你的情况 | 推荐工作流 |
|----------------|---------------------|
| **代码库新手** | [探索工作流](./exploration-workflow.md) + [搜索工具精通](./search-tools-mastery.md) |
| **复杂功能** | [计划驱动](./plan-driven.md) 或 [规范优先](./spec-first.md) |
| **需要可靠性** | [使用 Claude 进行 TDD](./tdd-with-claude.md) |
| **大规模重构** | [搜索工具精通](./search-tools-mastery.md) |
| **UI 实现** | [设计转代码](./design-to-code.md) |
| **代码质量** | [迭代优化](./iterative-refinement.md) |
| **从模板开始新项目** | [脚手架项目](./skeleton-projects.md) |
| **团队 AI 指令** | [团队 AI 指令](./team-ai-instructions.md) |
| **强制必选工作流步骤** | [变更日志片段](./changelog-fragments.md) |
| **可行性不明确、多日功能** | [RPI：研究 → 计划 → 实现](./rpi.md) |
| **文档** | [PDF 生成](./pdf-generation.md) |
| **社交预览** | [OG 图片生成](./og-image-generation.md) |
| **从原材料准备会议演讲** | [演讲准备管道](./talk-pipeline.md) |
| **音频反馈** | [TTS 设置](./tts-setup.md) |
| **多智能体任务** | [智能体团队](./agent-teams.md) |
| **第一个智能体团队** | [智能体团队快速入门](./agent-teams-quick-start.md) |
| **成本优化计划** | [双实例计划](./dual-instance-planning.md) |
| **钩子驱动自动化** | [事件驱动智能体](./event-driven-agents.md) |
| **完整计划工作流** | [计划管道](./plan-pipeline.md) |
| **多会话跟踪** | [任务管理](./task-management.md) |
| **编码前的战略门禁** | [认知模式切换](./gstack-workflow.md) |
| **非 MCP 浏览器自动化** | [认知模式切换](./gstack-workflow.md) |

---

## 贡献

有新工作流想法？在主仓库开 issue 或 PR。

**工作流模板结构**：
1. 标题和目的
2. 何时使用
3. 先决条件
4. 分步指南
5. 真实世界示例
6. 常见陷阱
7. 相关工作流

---

**最后更新**：2026 年 3 月