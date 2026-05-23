---
title: "Claude Code 终极指南"
description: "从零到高手的 Claude Code 完全自学指南"
tags: [guide, reference, workflows, agents, hooks, mcp, security]

---

# Claude Code 终极指南

> 一份完整的 Claude Code 自学指南——从零基础到熟练用户。

**作者**: Florian BRUNIAUX | 创始工程师 [@Méthode Aristote](https://methode-aristote.fr)

**写作工具**: Claude (Anthropic)

**阅读时间**: ~30-40 小时（全文）| ~15 分钟（仅快速入门）

**最后更新**: 2026 年 1 月

**版本**: 3.41.0

---

## 开始之前

**本指南并非 Anthropic 官方文档。** 它是基于我对 Claude Code 数月的探索整理而成的社区资源。

**你能找到的：**
- 对我有效的模式
- 可能不适用于你工作流的观察
- 作为粗略近似值的时间和百分比估计

**你找不到的：**
- 定论（这个工具还太新）
- 经过基准测试的性能声明
- 任何技术对你一定有效的保证

**批判性使用。多试验。分享对你有用的东西。**

> **⚠️ 注意（2026 年 1 月）**：如果你最近听说过 **ClawdBot**，那是**另一个工具**。ClawdBot 是一个可通过即时通讯应用（Telegram、WhatsApp 等）访问的自托管聊天助手，面向个人自动化和智能家居场景。Claude Code 是一个面向开发者的 CLI 工具（终端/IDE 集成），专注于软件开发生成式工作流。两者都使用 Claude 模型，但服务于不同的用户群体和使用场景。

---

## TL;DR — 5 分钟摘要

如果你只有 5 分钟，以下是你需要知道的内容：

### 常用命令
```bash
claude                    # 启动 Claude Code
/help                     # 显示所有命令
/powerup                  # 互动课程：CLAUDE.md、/rewind、记忆、effort 模式
/status                   # 检查上下文用量
/compact                  # 上下文超过 70% 时压缩
/clear                    # 全新开始
/plan                     # 安全的只读模式
Ctrl+C                    # 取消操作
```

### 工作流
```
描述 → Claude 分析 → 审查 Diff → 接受/拒绝 → 验证
```

### 上下文管理（关键！）
| 上下文占比 | 操作 |
|-----------|------|
| 0-50% | 自由工作 |
| 50-70% | 开始精打细算 |
| 70-90% | 立即 `/compact` |
| 90%+ | 必须 `/clear` |

*以上阈值基于我的经验。你的最佳工作流可能因任务复杂度和工作风格而异。*

### 记忆层级
```
~/.claude/CLAUDE.md       → 全局（所有项目）
/project/CLAUDE.md        → 项目（提交到 git）
/project/.claude/         → 个人（不提交）
```

### 高级功能
| 功能 | 作用 |
|------|------|
| **智能体（Agents）** | 专为特定任务定制的 AI 角色 |
| **技能（Skills）** | 可复用的知识模块 |
| **钩子（Hooks）** | 事件触发的自动化脚本 |
| **MCP 服务器** | 外部工具（Serena、Context7、Playwright...） |
| **插件（Plugins）** | 社区创建的扩展包 |

### 黄金法则
1. **始终审查 diff**，然后再接受变更
2. **在上下文变得紧张前使用 `/compact`**
3. **请求要具体**（WHAT、WHERE、HOW、VERIFY）
4. **复杂/高风险任务先用计划模式**
5. **为每个项目创建 CLAUDE.md**

### 快速决策树
```
简单任务 → 直接问 Claude
复杂任务 → 用 TodoWrite 规划
有风险 → 先进入计划模式
重复性任务 → 创建智能体或命令
上下文满了 → /compact 或 /clear
```

**现在阅读第 1 节完整快速入门，或跳转到你需要的任何章节。**

---

## 按你的情况选择路线

本指南共 11 章，22,000+ 行。你不需要全部读完——以下根据你的情况推荐：

| 你的身份 | 读这些 | 跳过这些 | 时间 |
|---------|--------|---------|------|
| **开发者，刚入门** | Ch.1 → Ch.2 → Ch.3 | Ch.9、Ch.11、附录 | 3h |
| **开发者，有基础** | Ch.2.6 → Ch.4 → Ch.5 → Ch.7 | Ch.1，Ch.10 仅作参考 | 4h |
| **高级用户 / 资深** | Ch.9（进阶）→ Ch.4-8 | Ch.1 快速入门 | 2h |
| **技术负责人 / EM** | Ch.3.5 → Ch.9.17 → Ch.9.20 → Ch.11 | Ch.5-6 细节 | 1h30 |
| **只需要参考** | Ch.10.5 速查表 | 其他所有内容 | 5 min |

---

## ROI 最高的 5 个章节

如果你只有时间看 5 个章节：

1. **[2.6 心智模型](ultimate-guide/02-core-concepts.md#26-mental-model)** — 理解 Claude Code 的思考方式（20 分钟）
2. **[3.1 CLAUDE.md](ultimate-guide/03-memory-settings.md#31-memory-files-claudemd)** — 跨会话持久的记忆（30 分钟）
3. **[9.1 三位一体](ultimate-guide/09-advanced-patterns.md#91-the-trinity)** — 智能体化工作的核心模式（20 分钟）
4. **[7.4 安全钩子](ultimate-guide/07-hooks.md#74-security-hooks)** — 自动化你忘不掉的护栏（30 分钟）
5. **[10.5 速查表](ultimate-guide/10-reference.md#105-cheatsheet)** — 日常参考，收藏它（5 分钟）

---

## 目录

- [1. 快速入门（第 1 天）](ultimate-guide/01-quick-start.md) `🟢 入门` `⏱ 45 分钟`
  - [1.1 安装](ultimate-guide/01-quick-start.md#11-installation)
  - [1.2 第一个工作流](ultimate-guide/01-quick-start.md#12-first-workflow)
  - [1.3 常用命令](ultimate-guide/01-quick-start.md#13-essential-commands)
  - [1.4 权限模式](ultimate-guide/01-quick-start.md#14-permission-modes)
  - [1.5 效率清单](ultimate-guide/01-quick-start.md#15-productivity-checklist)
  - [1.6 从其他 AI 编程工具迁移](ultimate-guide/01-quick-start.md#16-migrating-from-other-ai-coding-tools)
  - [1.7 信任校准](ultimate-guide/01-quick-start.md#17-trust-calibration-when-and-how-much-to-verify)
  - [1.8 初学者的八个误区](ultimate-guide/01-quick-start.md#18-eight-beginner-mistakes-and-how-to-avoid-them)
- [2. 核心概念](ultimate-guide/02-core-concepts.md) `🟡 进阶` `⏱ 60 分钟`
  - [2.1 交互循环](ultimate-guide/02-core-concepts.md#21-the-interaction-loop)
  - [2.2 上下文管理](ultimate-guide/02-core-concepts.md#22-context-management)
  - [2.3 计划模式](ultimate-guide/02-core-concepts.md#23-plan-mode)（含 [Ultraplan](#ultraplan)、[OpusPlan](#opusplan-mode)）
  - [2.4 回退](ultimate-guide/02-core-concepts.md#24-rewind)
  - [2.5 模型选择与思考指南](ultimate-guide/02-core-concepts.md#25-model-selection--thinking-guide)
  - [2.6 心智模型](ultimate-guide/02-core-concepts.md#26-mental-model)
  - [2.7 配置决策指南](ultimate-guide/02-core-concepts.md#27-configuration-decision-guide)
  - [2.8 XML 标签结构化提示](ultimate-guide/02-core-concepts.md#28-structured-prompting-with-xml-tags)
  - [2.9 语义锚点](ultimate-guide/02-core-concepts.md#29-semantic-anchors)
  - [2.10 数据流与隐私](ultimate-guide/02-core-concepts.md#210-data-flow--privacy)
  - [2.11 底层机制](ultimate-guide/02-core-concepts.md#211-under-the-hood)
- [3. 记忆与设置](ultimate-guide/03-memory-settings.md) `🟢 入门` `⏱ 30 分钟`
  - [3.1 记忆文件（CLAUDE.md）](ultimate-guide/03-memory-settings.md#31-memory-files-claudemd)
  - [3.2 .claude/ 文件夹结构](ultimate-guide/03-memory-settings.md#32-the-claude-folder-structure)
  - [3.3 设置与权限](ultimate-guide/03-memory-settings.md#33-settings--permissions)
  - [3.4 优先规则](ultimate-guide/03-memory-settings.md#34-precedence-rules)
  - [3.5 团队规模化配置](ultimate-guide/03-memory-settings.md#35-team-configuration-at-scale)
- [4. 智能体](ultimate-guide/04-agents.md) `🟡 进阶` `⏱ 45 分钟`
  - [4.1 什么是智能体](ultimate-guide/04-agents.md#41-what-are-agents)
  - [4.2 创建自定义智能体](ultimate-guide/04-agents.md#42-creating-custom-agents)
  - [4.3 智能体模板](ultimate-guide/04-agents.md#43-agent-template)
  - [4.4 最佳实践](ultimate-guide/04-agents.md#44-best-practices)
  - [4.5 智能体记忆](ultimate-guide/04-agents.md#45-agent-memory)
  - [4.6 智能体示例](ultimate-guide/04-agents.md#46-agent-examples)
  - [4.7 进阶智能体模式](ultimate-guide/04-agents.md#47-advanced-agent-patterns)
- [5. 技能](ultimate-guide/05-skills.md) `🟡 进阶` `⏱ 30 分钟`
  - [5.1 理解技能](ultimate-guide/05-skills.md#51-understanding-skills)
  - [5.2 创建技能](ultimate-guide/05-skills.md#52-creating-skills)
  - [5.3 技能模板](ultimate-guide/05-skills.md#53-skill-template)
  - [5.4 技能示例](ultimate-guide/05-skills.md#54-skill-examples)
- [6. 命令](ultimate-guide/06-commands.md) `🟡 进阶` `⏱ 30 分钟`
  - [6.1 斜杠命令](ultimate-guide/06-commands.md#61-slash-commands)
  - [6.2 创建自定义命令](ultimate-guide/06-commands.md#62-creating-custom-commands)
  - [6.3 命令模板](ultimate-guide/06-commands.md#63-command-template)
  - [6.4 命令示例](ultimate-guide/06-commands.md#64-command-examples)
- [7. 钩子](ultimate-guide/07-hooks.md) `🟡 进阶` `⏱ 45 分钟`
  - [7.1 事件系统](ultimate-guide/07-hooks.md#71-the-event-system)
  - [7.2 创建钩子](ultimate-guide/07-hooks.md#72-creating-hooks)
  - [7.3 钩子模板](ultimate-guide/07-hooks.md#73-hook-templates)
  - [7.4 安全钩子](ultimate-guide/07-hooks.md#74-security-hooks)
  - [7.5 钩子示例](ultimate-guide/07-hooks.md#75-hook-examples)
- [8. MCP 服务器](ultimate-guide/08-mcp-servers.md) `🟡 进阶` `⏱ 40 分钟`
  - [8.1 什么是 MCP](ultimate-guide/08-mcp-servers.md#81-what-is-mcp)
  - [8.2 可用服务器](ultimate-guide/08-mcp-servers.md#82-available-servers)
  - [8.3 配置](ultimate-guide/08-mcp-servers.md#83-configuration)
  - [8.4 服务器选择指南](ultimate-guide/08-mcp-servers.md#84-server-selection-guide)
  - [8.5 插件系统](ultimate-guide/08-mcp-servers.md#85-plugin-system)
  - [8.6 MCP 安全](ultimate-guide/08-mcp-servers.md#86-mcp-security)
- [9. 进阶模式](ultimate-guide/09-advanced-patterns.md) `🔴 高级` `⏱ 3 小时`
  - [9.1 三位一体](ultimate-guide/09-advanced-patterns.md#91-the-trinity)
  - [9.2 组合模式](ultimate-guide/09-advanced-patterns.md#92-composition-patterns)
  - [9.3 CI/CD 集成](ultimate-guide/09-advanced-patterns.md#93-cicd-integration)
  - [9.4 IDE 集成](ultimate-guide/09-advanced-patterns.md#94-ide-integration)
  - [9.5 紧密反馈循环](ultimate-guide/09-advanced-patterns.md#95-tight-feedback-loops)
  - [9.6 Todo 作为指令镜像](ultimate-guide/09-advanced-patterns.md#96-todo-as-instruction-mirrors)
  - [9.7 输出风格](ultimate-guide/09-advanced-patterns.md#97-output-styles)
  - [9.8 Vibe Coding 与骨架项目](ultimate-guide/09-advanced-patterns.md#98-vibe-coding--skeleton-projects)
  - [9.9 批量操作模式](ultimate-guide/09-advanced-patterns.md#99-batch-operations-pattern)
  - [9.10 持续改进心态](ultimate-guide/09-advanced-patterns.md#910-continuous-improvement-mindset)
  - [9.11 常见陷阱与最佳实践](ultimate-guide/09-advanced-patterns.md#911-common-pitfalls--best-practices)
  - [9.12 Git 最佳实践与工作流](ultimate-guide/09-advanced-patterns.md#912-git-best-practices--workflows)
  - [9.13 成本优化策略](ultimate-guide/09-advanced-patterns.md#913-cost-optimization-strategies)
  - [9.14 开发方法论](ultimate-guide/09-advanced-patterns.md#914-development-methodologies)
  - [9.15 命名提示模式](ultimate-guide/09-advanced-patterns.md#915-named-prompting-patterns)
  - [9.16 会话传送](ultimate-guide/09-advanced-patterns.md#916-session-teleportation)
  - [9.17 扩展模式：多实例工作流](ultimate-guide/09-advanced-patterns.md#917-scaling-patterns-multi-instance-workflows)
  - [9.18 面向智能体生产力的代码库设计](ultimate-guide/09-advanced-patterns.md#918-codebase-design-for-agent-productivity)
  - [9.19 排列组合框架](ultimate-guide/09-advanced-patterns.md#919-permutation-frameworks)
  - [9.20 智能体团队（多智能体协调）](ultimate-guide/09-advanced-patterns.md#920-agent-teams-multi-agent-coordination)
  - [9.21 遗留代码库现代化](ultimate-guide/09-advanced-patterns.md#921-legacy-codebase-modernization)
  - [9.22 远程控制（移动端访问）](ultimate-guide/09-advanced-patterns.md#922-remote-control-mobile-access)
  - [9.23 配置生命周期与更新循环](ultimate-guide/09-advanced-patterns.md#923-configuration-lifecycle--the-update-loop)
  - [9.24 基于直觉的持续学习](ultimate-guide/09-advanced-patterns.md#924-instinct-based-continuous-learning)
  - [9.25 Harness 工程](ultimate-guide/09-advanced-patterns.md#925-harness-engineering)
- [10. 参考](ultimate-guide/10-reference.md) `🟢 全等级` `⏱ 按需查阅`
  - [10.1 命令表](ultimate-guide/10-reference.md#101-commands-table)
  - [10.2 键盘快捷键](ultimate-guide/10-reference.md#102-keyboard-shortcuts)
  - [10.3 配置参考](ultimate-guide/10-reference.md#103-configuration-reference)
  - [10.4 故障排查](ultimate-guide/10-reference.md#104-troubleshooting)
  - [10.5 速查表](ultimate-guide/10-reference.md#105-cheatsheet)
  - [10.6 日常工作流与清单](ultimate-guide/10-reference.md#106-daily-workflow--checklists)
- [11. AI 生态：互补工具](ultimate-guide/11-ai-ecosystem.md) `🟡 进阶` `⏱ 20 分钟`
  - [11.1 为什么互补性很重要](ultimate-guide/11-ai-ecosystem.md#111-why-complementarity-matters)
  - [11.2 工具矩阵](ultimate-guide/11-ai-ecosystem.md#112-tool-matrix)
  - [11.3 实用工作流](ultimate-guide/11-ai-ecosystem.md#113-practical-workflows)
  - [11.4 集成模式](ultimate-guide/11-ai-ecosystem.md#114-integration-patterns)
  - [面向非开发者：Claude Cowork](ultimate-guide/11-ai-ecosystem.md#for-non-developers-claude-cowork)
- [附录：模板合集](ultimate-guide/10-reference.md#appendix-templates-collection)
  - [附录 A：文件位置参考](ultimate-guide/10-reference.md#appendix-a-file-locations-reference)
  - [附录 B：FAQ](ultimate-guide/10-reference.md#appendix-b-faq)

---

> 💡 本指南按章节拆分为独立文件，方便导航。以上每个链接打开对应的章节。