---
title: "Claude Code 工作流"
description: "使用 Claude Code 的常见开发模式指南"
tags: [workflow, guide, reference]
---

# Claude Code 工作流

常见开发模式指南，配套 Claude Code 使用说明。

---

## 🔍 搜索与探索

### [搜索工具精通](./search-tools-mastery.md) ⭐ 新增

**组合 rg、grepai、Serena 和 ast-grep，掌握代码搜索**

何时用哪个工具、如何组合使用效率最高，包含真实工作流：
- 探索陌生代码库
- 大规模重构
- 安全审计
- 框架迁移
- 性能优化

**核心内容**：
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

**何时使用**：多步骤功能、架构变更、不确定方案

### [使用 Claude 进行 TDD](./tdd-with-claude.md)

测试驱动开发：先写测试，后实现。

**何时使用**：关键功能、回归预防、API 设计

### [规范优先开发](./spec-first.md)

代码前先写规范，明确需求。

**何时使用**：团队协作、复杂功能、文档先行

### [迭代优化](./iterative-refinement.md)

多轮优化循环改进代码。

**何时使用**：质量改进、性能优化、代码清理

### [脚手架项目](./skeleton-projects.md) ⭐ 新增

用已有的、经过实战检验的仓库作新项目的脚手架。

**何时使用**：新项目启动、团队模式标准化、快速原型

### [团队 AI 指令](./team-ai-instructions.md)

多开发者、多工具团队的 CLAUDE.md 管理方案：基于配置文件的模块组装。

**何时使用**：5 人以上团队、多个 AI 工具、混合操作系统

### [变更日志片段](./changelog-fragments.md) ⭐ 新增

**三层强制系统，确保每个 PR 都有文档：CLAUDE.md 规则 + UserPromptSubmit 钩子 + CI 门禁**

消除 `CHANGELOG.md` 合并冲突、实现时捕获上下文、数据库迁移绝不静默部署。包含可复用的 `UserPromptSubmit` 钩子模式，可强制任何必选工作流步骤。

**核心内容**：
- CLAUDE.md 工作流规则，Claude 自主创建片段
- 三层优先级 `UserPromptSubmit` 钩子（强制、发现、上下文）
- 条件建议模式："有 PR 意图但未提片段"
- 带独立迁移检查的 CI 强制执行

### [RPI：研究 → 计划 → 实现](./rpi.md) ⭐ 新增

**三阶段功能开发，阶段之间有明确验证门禁**

三阶段构建功能：先研究可行性、再计划实现、最后写代码。每阶段产出具体产物（RESEARCH.md → PLAN.md → 代码）。每个门禁需要明确 GO 才能进入下阶段。

**何时使用**：可行性不明的功能、工作量超过一天、未知技术领域、发现错误假设代价高昂

### [GitHub Actions 工作流](./github-actions.md) ⭐ 新增

**5 个生产就绪模式，自动化 PR 评审、问题分类、质量门禁**

通过官方 `claude-code-action` 将 Claude 直接接入 GitHub 工作流。两种模式：交互式（`@claude` 提及）和完全自动化（push/定时）。

**核心内容**：
- `/install-github-app` 快速设置（30 秒）
- 模式 1：`@claude` 提及触发 PR 评审
- 模式 2：每次 push 自动评审
- 模式 3：问题分类和标签
- 模式 4：敏感路径安全评审
- 模式 5：定时仓库健康检查
- 成本控制、并发、fork 安全

**何时使用**：想要 AI 驱动代码评审、无需管理基础设施的团队

---

### [认知模式切换](./gstack-workflow.md) ⭐ 新增

交付周期中切换专家角色：战略产品门禁、架构评审、多疑代码评审、自动化发布、本地浏览器 QA 和回顾。

**何时使用**：交付周期中需要在产品方向、工程严谨、评审、发布之间明确分离

---

## 🎨 设计与内容

### [设计转代码](./design-to-code.md)

设计模型（Figma、线框图）转可用代码。

**何时使用**：前端开发、UI 实现、设计系统

### [OG 图片生成](./og-image-generation.md)

用 Satori 和 resvg 构建时动态生成社交预览图。

**何时使用**：Astro 项目、保持社交预览准确

### [PDF 生成](./pdf-generation.md)

用 Quarto/Typst 和 Claude Code 生成专业 PDF。

**何时使用**：报告、文档、白皮书、技术文档

### [演讲准备管道](./talk-pipeline.md) ⭐ 新增

6 阶段技能管道：原材料 → 结构化演讲 → Kimi 生成幻灯片。

**何时使用**：会议演讲、meetup 演示、内部技术分享——从文章、转录稿或笔记

### [TTS 设置](./tts-setup.md)

Claude Code 文字转语音配置（Agent Vibes 集成）。

**何时使用**：音频反馈、无障碍、免手编码

---

## 🔬 代码探索

### [探索工作流](./exploration-workflow.md)

系统探索和理解陌生代码库。

**何时使用**：新项目、遗留代码、文档缺失

**相关**：[搜索工具精通](./search-tools-mastery.md) 的高级多工具探索策略

---

## 多智能体与高级

### [智能体团队](./agent-teams.md)

编排多个专用智能体并行处理复杂任务。

**何时使用**：并行、专业知识、独立验证受益的任务

### [智能体团队快速入门](./agent-teams-quick-start.md)

30 分钟搭建第一个智能体团队。

**何时使用**：多智能体模式新手、想先试试水

### [双实例计划](./dual-instance-planning.md)

Opus 计划 + Sonnet 执行，双 Claude Code 实例协作。

**何时使用**：需要深度推理的复杂功能架构、成本敏感的执行

### [事件驱动智能体](./event-driven-agents.md)

通过钩子事件而非直接编排协调智能体。

**何时使用**：响应式工作流、钩子触发自动化、松耦合管道

### [计划管道](./plan-pipeline.md)

完整端到端计划管道：/plan-start、/plan-validate、/plan-execute 串联。

**何时使用**：重要功能、编码前值得计划严谨性

### [任务管理](./task-management.md)

跨会话任务跟踪，用 TodoWrite、Tasks API 和上下文持久化。

**何时使用**：长周期任务、团队协调、复杂待办

---

## 快速选择

| 情况 | 推荐工作流 |
|----------------|---------------------|
| **代码库新手** | [探索工作流](./exploration-workflow.md) + [搜索工具精通](./search-tools-mastery.md) |
| **复杂功能** | [计划驱动](./plan-driven.md) 或 [规范优先](./spec-first.md) |
| **需要可靠性** | [TDD](./tdd-with-claude.md) |
| **大规模重构** | [搜索工具精通](./search-tools-mastery.md) |
| **UI 实现** | [设计转代码](./design-to-code.md) |
| **代码质量** | [迭代优化](./iterative-refinement.md) |
| **新项目** | [脚手架项目](./skeleton-projects.md) |
| **团队 AI 指令** | [团队 AI 指令](./team-ai-instructions.md) |
| **强制文档** | [变更日志片段](./changelog-fragments.md) |
| **多日功能** | [RPI](./rpi.md) |
| **生成文档** | [PDF 生成](./pdf-generation.md) |
| **社交预览** | [OG 图片生成](./og-image-generation.md) |
| **准备演讲** | [演讲准备管道](./talk-pipeline.md) |
| **音频反馈** | [TTS 设置](./tts-setup.md) |
| **多智能体** | [智能体团队](./agent-teams.md) |
| **首个团队** | [快速入门](./agent-teams-quick-start.md) |
| **成本优化** | [双实例计划](./dual-instance-planning.md) |
| **钩子自动化** | [事件驱动智能体](./event-driven-agents.md) |
| **完整计划** | [计划管道](./plan-pipeline.md) |
| **跨会话跟踪** | [任务管理](./task-management.md) |
| **战略门禁** | [认知模式切换](./gstack-workflow.md) |
| **浏览器自动化** | [认知模式切换](./gstack-workflow.md) |

---

## 贡献

有新工作流想法？在主仓库开 issue 或 PR。

**工作流模板结构**：
1. 标题和目的
2. 何时使用
3. 先决条件
4. 分步指南
5. 真实示例
6. 常见陷阱
7. 相关工作流

---

**最后更新**：2026 年 3 月