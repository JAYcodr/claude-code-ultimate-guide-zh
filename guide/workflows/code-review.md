<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "代码评审（Claude Code 功能）"
description: "面向团队和企业计划的多智能体 PR 评审自动化 — 设置、触发器、REVIEW.md 配置和成本管理"
tags: [feature, teams, enterprise, github, code-review]
---

# 代码评审

> **可用性**：研究预览版 — 仅限团队和企业计划。免费/专业计划不可用，也不适用于启用零数据保留（ZDR）的组织。
> **发布日期**：2026 年 3 月 9 日

Claude Code 的代码评审功能对每个 GitHub Pull Request 运行多智能体评审。一组专用智能体在完整代码库的上下文中检查 diff，每个关注不同类别的问题（逻辑错误、安全漏洞、边缘情况、回归），随后进行验证步骤过滤误报。

发现问题会在找到问题的具体行上以内联 PR 评论形式发布，并标记严重性。评审不会批准或阻止 PR，因此现有的评审工作流保持完整。

---

## 工作原理

1. 触发器触发（PR 打开、push 或手动 `@claude review` 评论）
2. 多个智能体在 Anthropic 基础设施上并行分析 diff 和周围代码
3. 每个智能体针对不同类别的问题
4. 验证步骤对照实际代码行为检查候选问题，移除误报
5. 结果去重，按严重性排序，作为内联 PR 评论发布
6. 如果没有问题，Claude 发布一条简短确认评论

评审平均 **20 分钟完成**，规模随 PR 大小和复杂度增加。

### 严重性级别

| 标记 | 严重性 | 含义 |
|:-------|:---------|:--------|
| 🔴 | Normal | 应该合并前修复的 bug |
| 🟡 | Nit | 次要问题，值得修复但不阻塞 |
| 🟣 | Pre-existing | 代码库中非本 PR 引入的 bug |

每个发现都包含一个可折叠的扩展推理部分，解释 Claude 标记问题的原因以及如何验证问题。

---

## 设置

管理员为组织启用一次代码评审，选择要包含的仓库。

### 1. 打开管理员设置

转到 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 找到 **Code Review** 部分。需要对 Claude 组织和 GitHub 组织都有管理员访问权限，以及在 GitHub 组织安装 GitHub Apps 的权限。

### 2. 点击设置

这开始 GitHub App 安装流程。

### 3. 安装 Claude GitHub App

按照提示在 GitHub 组织上安装 Claude GitHub App。App 请求：

- **Contents**：读和写
- **Issues**：读和写
- **Pull requests**：读和写

代码评审使用读取权限访问 contents，写权限访问 pull requests。此权限集也支持 [GitHub Actions](./github-actions.md)（如果以后启用）。

### 4. 选择仓库

选择要启用的仓库。如果仓库缺失，确保在安装过程中授予了 GitHub App 访问权限。以后可以从管理员设置表格添加更多仓库。

### 5. 为每个仓库设置评审触发器

对于每个仓库，选择何时运行评审：

| 触发器 | 何时运行 | 成本配置 |
|---------|-------------|--------------|
| **PR 创建后一次** | PR 打开或标记 ready 时一次 | 最低 |
| **每次 push 后** | PR 分支每次 push | 最高（乘以 push 次数） |
| **手动** | 仅当有人评论 `@claude review` | 可控 |

`@claude review` 评论后，该 PR 的后续 push 会自动触发评审，不管配置的触发器是什么。

**手动模式**适用于高流量仓库，在那里你想选择特定的 PR 进行评审，或者只在 PR 准备好评审时才开始评审。

---

## 手动触发

在任何打开的、非草稿的 PR 上评论 `@claude review` 立即开始评审。要求：

- 顶层 PR 评论（不是内联 diff 评论）
- 评论开头是 `@claude review`
- 对仓库有 owner、member 或 collaborator 访问权限

如果评审已在运行，请求会排队直到进行中的评审完成。

---

## 配置评审

两个文件控制 Claude 标记什么。两者都在默认正确性检查之上叠加。

### CLAUDE.md

Claude 读取目录层次结构中的所有 `CLAUDE.md` 文件。新引入的违规被标记为 nit 级别发现。双向的：如果 PR 使 `CLAUDE.md` 声明过时，Claude 会标记文档也需要更新。

用于也适用于交互式 Claude Code 会话的指导。

### REVIEW.md

在**仓库根目录**添加 `REVIEW.md` 用于仅评审规则。自动发现，无需配置。

```markdown
# 代码评审指南

## 始终检查
- 新 API 端点有相应的集成测试
- 数据库迁移向后兼容
- 错误消息不向用户暴露内部细节

## 风格
- 优先使用 early return 而非嵌套条件
- 使用结构化日志，而非日志调用中的 f-string 插值

## 跳过
- `src/gen/` 下的生成文件
- `*.lock` 文件中仅格式更改
- `db/migrations/` 中的迁移文件
```

用于会污染 `CLAUDE.md`（对常规会话）的规则（linter 约定、跳过列表、特定团队模式）。

---

## 定价

代码评审按 token 使用量计费，**与你计划包含的使用量分开**（通过[额外使用量](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)）。

- 平均成本：**每次评审 $15-25**，随 PR 大小、代码库复杂度和需要验证的问题数量缩放
- "每次 push 后" 会将成本乘以 push 次数
- 设置月度消费上限：[claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) → 为 "Claude Code Review" 服务配置限制
- 监控消费：[claude.ai/analytics/code-review](https://claude.ai/analytics/code-review)（每日 PR 数量、每周消费、按仓库细分）

---

## 交叉参考

对于手动代码评审工作流（CLI，无需团队/企业计划）：
- [多智能体代码评审工作流](#split-role-sub-agents) — 通过 CLI 的 DIY 智能体团队
- [GitHub Actions 集成](./github-actions.md) — 自定义 CI/CD 自动化（相对于此托管服务的自托管替代方案）
- GitLab CI/CD — GitLab 管道的自托管 Claude 集成
- 代码评审插件 — 推送前的按需本地评审（可在插件市场获取）

---

## 已知限制（研究预览版）

- 仅限团队和企业 — 免费/专业计划不可用
- 不适用于启用零数据保留（ZDR）的组织
- 托管服务仅限 GitHub（GitLab 通过 CI/CD 集成支持，非此功能）
- 大仓库首次激活时全仓库索引延迟
- Anthropic 内部统计：>1000 行的 PR 平均发现 ~7.5 个问题，<1% 误报率 — 自行报告，未经独立验证