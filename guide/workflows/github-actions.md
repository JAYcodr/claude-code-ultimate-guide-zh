<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "GitHub Actions 工作流与 Claude Code"
description: "使用 claude-code-action 自动化 PR 评审、问题分类和质量门禁的生产就绪模式"
tags: [workflow, ci-cd, github-actions, automation]
---

# GitHub Actions 工作流与 Claude Code

> **可信度**：第 1 层 — 官方 Anthropic action（`anthropics/claude-code-action`，6.2k stars，v1.0）。

把 Claude 直接接入 GitHub 工作流，自动化代码评审、问题分类和质量门禁。两种触发模式：`@claude` 提及（人工发起）和预定/事件自动化（完全自主）。

---

## 目录

1. [TL;DR](#tldr)
2. [两种模式](#两种模式)
3. [设置](#设置)
4. [模式 1：@claude 提及的 PR 代码评审](#模式-1claude-提及的-pr-代码评审)
5. [模式 2：Push 时自动 PR 评审](#模式-2push-时自动-pr-评审)
6. [模式 3：问题分类和标签](#模式-3问题分类和标签)
7. [模式 4：安全聚焦评审](#模式-4安全聚焦评审)
8. [模式 5：预定仓库维护](#模式-5预定仓库维护)
9. [认证替代方案](#认证替代方案)
10. [成本控制](#成本控制)
11. [安全检查清单](#安全检查清单)
12. [另见](#另见)

---

## TL;DR

```yaml
# 最小工作示例 — 粘贴到 .github/workflows/claude.yml
name: Claude Code Review
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

在任意 PR 上评论 `@claude review this PR` → Claude 读取 diff 并发布评审。

---

## 两种模式

| 模式 | 触发器 | 用例 |
|-------|---------|------|
| **交互式** | PR/issue 评论中的 `@claude` 提及 | 按需评审、问题、修复 |
| **自动化** | Push、PR 打开、定时、标签 | 持续质量门禁、分类 |

两者使用相同的 action — 区别在于 `on:` 块以及是否包含 `if:` 条件。

---

## 设置

### 快速开始（30 秒）

在你的 Claude Code 终端中，在任何连接到 GitHub 仓库的项目内：

```
/install-github-app
```

这指导你创建 GitHub App、将 `ANTHROPIC_API_KEY` 添加到仓库 secrets，并生成基础 `claude.yml` 工作流。

### 手动设置

1. 将 `ANTHROPIC_API_KEY` 添加到你的 GitHub 仓库 secrets
2. 创建 `.github/workflows/claude.yml`（见下面的模式）
3. 授予工作流权限：`contents: write`、`pull-requests: write`、`issues: write`

---

## 模式 1：@claude 提及的 PR 代码评审

人工发起。开发者评论 `@claude review this PR`，Claude 在行内响应。

```yaml
# .github/workflows/claude-review.yml
name: Claude Interactive Review
on:
  issue_comment:
    types: [created, edited]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: |
      contains(github.event.comment.body, '@claude') ||
      contains(github.event.review_comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_env: |
            GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

**使用示例：**
- `@claude review this PR` — 完整 diff 分析带建议
- `@claude is this change backwards compatible?` — 针对性问题
- `@claude fix the failing test in src/auth.test.ts` — Claude 打开带有修复的跟进 PR

---

## 模式 2：Push 时自动 PR 评审

每个 PR 在打开或更新时立即获得评审。无需提及。

```yaml
# .github/workflows/claude-auto-review.yml
name: Claude Auto PR Review
on:
  pull_request:
    types: [opened, synchronize]
    # 可选：仅在特定路径触发
    # paths:
    #   - 'src/**'
    #   - '!**/*.md'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this pull request. Focus on:
            - Logic errors and edge cases
            - Security issues (injection, auth, secrets)
            - Performance regressions
            - Missing error handling

            Format your response as:
            ## Summary
            One paragraph describing the change.

            ## Issues Found
            Numbered list, severity (Critical/Major/Minor), file:line reference.

            ## Suggestions
            Optional improvements.

            Keep it under 400 words. Be direct.
```

**提示**：添加 `paths:` 以避免在仅文档 PR 上触发，或 `if: github.event.pull_request.draft == false` 跳过草稿。

---

## 模式 3：问题分类和标签

Claude 读取新问题、分配标签并发布结构化分类评论。

```yaml
# .github/workflows/claude-triage.yml
name: Issue Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Triage this GitHub issue:

            1. Assign one label from: bug, enhancement, question, documentation, performance, security
            2. Assign a priority label: priority:critical, priority:high, priority:medium, priority:low
            3. Post a comment with:
               - Issue type classification
               - Which component is likely affected (based on the issue description)
               - Next step recommendation for the reporter (reproduce steps needed? version info missing?)

            Be brief. One sentence per point.
```

---

## 模式 4：安全聚焦评审

专门针对触摸敏感路径（auth、payments、config）的 PR 运行。

```yaml
# .github/workflows/claude-security.yml
name: Security Review
on:
  pull_request:
    paths:
      - 'src/auth/**'
      - 'src/payments/**'
      - '**/config/**'
      - '**/.env*'
      - '**/secrets/**'

jobs:
  security-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a security-focused review of this PR. Check for:

            - Injection vulnerabilities (SQL, command, LDAP)
            - Authentication and authorization bypasses
            - Secrets or credentials in code or comments
            - Insecure direct object references
            - Missing input validation
            - Unsafe deserialization
            - OWASP Top 10 patterns

            Rate overall risk: Low / Medium / High / Critical.
            If High or Critical, add the label 'security-review-required'.
            List each finding with: file:line, vulnerability type, and recommended fix.
```

---

## 模式 5：预定仓库维护

每周健康检查 — 无需任何人工触发运行。

```yaml
# .github/workflows/claude-maintenance.yml
name: Weekly Repo Health Check
on:
  schedule:
    - cron: '0 9 * * 1'  # 每周一 UTC 9am
  workflow_dispatch:       # 也允许手动触发

jobs:
  maintenance:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a weekly repository health check:

            1. Scan package.json (or equivalent) for outdated major dependencies
            2. Check for TODO/FIXME comments older than 30 days in src/
            3. Identify any test files without corresponding implementation files
            4. List any documentation files that reference deleted or renamed files

            Open a GitHub issue titled "Weekly Health Check - [date]" with your findings.
            If nothing requires attention, post a comment "Health check passed — no issues found."
```

---

## 认证替代方案

上述示例直接使用 `ANTHROPIC_API_KEY`。对于使用云提供商的团队：

**Amazon Bedrock：**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: 'true'
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_REGION: us-east-1
    ANTHROPIC_MODEL: 'anthropic.claude-3-5-sonnet-20241022-v2:0'
```

**Google Vertex AI：**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_vertex: 'true'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
    CLOUD_ML_REGION: us-east5
    ANTHROPIC_MODEL: 'claude-3-5-sonnet-v2@20241022'
```

云提供商受益于数据驻留合规性，可以利用现有 IAM 策略而不是管理单独的 API 密钥。

---

## 成本控制

自动化工作流在无人工介入的情况下运行 — 设置明确限制。

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    # 限制每次工作流运行的消费
    claude_args: '--max-budget-usd 0.50'
    # 分类用 Haiku，评审用 Sonnet — 不要默认用 Opus
    prompt: |
      ...
```

**按模式的预算指导：**

| 模式 | 模型 | 约每次成本 |
|---------|-------|--------------------|
| PR 评审（中等 PR）| Sonnet | $0.05–0.15 |
| 问题分类 | Haiku | $0.01–0.03 |
| 安全评审（大 PR）| Sonnet | $0.10–0.25 |
| 预定维护 | Sonnet | $0.05–0.20 |

用 `ccusage` 或 Anthropic Console 使用仪表板监控实际消费。

**防止成本失控：**
- 使用 `paths:` 过滤器避免在不相关的变更上触发
- 添加 `if: github.event.pull_request.draft == false` 跳过草稿 PR
- 设置 `concurrency:` 防止在同一 PR 上并行运行

```yaml
jobs:
  claude-review:
    concurrency:
      group: claude-${{ github.event.pull_request.number }}
      cancel-in-progress: true
```

---

## 安全检查清单

部署到团队仓库前：

- [ ] `ANTHROPIC_API_KEY` 存储为 GitHub secret，绝不在工作流 YAML 中
- [ ] 工作流权限最小化 — 除非需要写权限，否则使用 `contents: read`
- [ ] 对于公共仓库：添加 `if: github.event.pull_request.head.repo.full_name == github.repository` 防止 fork PR 触发 API 调用
- [ ] 审查工作流公开发布的内容 — Claude 的评论对所有贡献者可见
- [ ] 谨慎使用 `pull_request_target` — 它即使从 fork 运行也以写权限运行

**公共仓库 fork 安全模式：**
```yaml
jobs:
  claude:
    # 仅在同一仓库的 PR 上运行，而非 fork
    if: github.event.pull_request.head.repo.full_name == github.repository
```

---

## 另见

- [第 9.3 节 CI/CD 集成](#93-cicd-集成) — 无头模式、Unix 管道、`--output-format json`
- [生产安全](../security/production-safety.md) — 自动化智能体的护栏
- [安全加固](../security/security-hardening.md) — MCP 和 webhook 安全
- [官方 action 文档](https://github.com/anthropics/claude-code-action) — 解决方案指南、迁移、云提供商
- [社区工作流蓝图](https://github.com/alirezarezvani/claude-code-github-workflow) — 高级团队的 8 个工作流 + 4 个自主智能体