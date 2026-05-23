<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "脚手架项目工作流"
description: "使用已有的、经过实战检验的仓库作为新项目的脚手架"
tags: [workflow, architecture, template]
---

# 脚手架项目工作流

使用已有的、经过实战检验的仓库作为新项目的脚手架，而不是从零开始。

---

## 何时使用

- **启动使用已知技术栈的新项目**
- **跨多个服务标准化团队模式**
- **快速原型**，架构决策已经做出
- **通过可用的参考入职**新团队成员

**不要在以下情况使用**：探索未知技术（改用 [Vibe Coding](#98-vibe-coding-skeleton-projects)），或需求对现有模板来说太独特。

---

## 先决条件

- Claude Code 已安装并配置
- 访问参考仓库的 Git 权限
- 清楚了解目标项目需求

---

## 分步指南

### 阶段 1：找到并评估脚手架

不要从零构建。找到匹配你目标架构的现有仓库。

**步骤 1：搜索候选**

```bash
# 让 Claude 帮助找到参考仓库
claude -p "I need a skeleton for a Next.js 15 app with:
- App Router
- Prisma ORM with PostgreSQL
- tRPC for type-safe API
- Tailwind CSS
- Jest + Playwright testing

Search GitHub for well-maintained starter templates.
Evaluate the top 3 by: last commit date, stars, dependency freshness, test coverage."
```

**步骤 2：克隆并审计**

```bash
git clone <candidate-repo> skeleton-eval
cd skeleton-eval
claude
```

```markdown
User: Audit this repository as a potential skeleton for our project:
1. List all dependencies and their versions (flag outdated ones)
2. Assess code quality: patterns, consistency, test coverage
3. Identify what we'd keep vs. what we'd remove
4. Flag any security concerns (vulnerable deps, exposed secrets)
5. Rate overall suitability (1-5) with specific justification
```

**步骤 3：用子智能体评估**（用于彻底分析）

```markdown
User: Run a multi-perspective evaluation of this skeleton:

Agent 1 (Security): Check for vulnerabilities, hardcoded secrets, unsafe patterns
Agent 2 (Architecture): Assess modularity, separation of concerns, scalability
Agent 3 (DX): Evaluate developer experience - setup time, documentation, tooling

Synthesize findings into a go/no-go recommendation.
```

### 阶段 2：分叉并定制

**步骤 4：从脚手架创建你的项目**

```bash
# 从脚手架创建新仓库
mkdir my-project
cp -r skeleton-eval/. my-project/
cd my-project
rm -rf .git
git init
```

**步骤 5：用 Claude 剥离和适配**

```markdown
User: Customize this skeleton for our project "Acme Dashboard":

1. Remove: example routes, demo data, sample tests
2. Keep: config structure, auth setup, database schema pattern, CI pipeline
3. Update: package.json (name, description, version 0.1.0)
4. Add: our CLAUDE.md with project conventions
5. Verify: `pnpm install && pnpm build && pnpm test` all pass after changes

Important: Don't break the working skeleton. Each removal should be followed
by a build check.
```

### 阶段 3：从脚手架扩展到 MVP

**步骤 6：构建第一个真实功能**

```markdown
User: Using the patterns established in this skeleton, implement our first feature:
User Authentication (login + registration + password reset)

Follow the skeleton's existing patterns for:
- Route structure (match the example routes pattern)
- Service layer (match the existing service pattern)
- Test structure (match the example test pattern)
- Error handling (match the existing error pattern)

Create a task plan before starting implementation.
```

**步骤 7：验证脚手架完整性**

```markdown
User: Now that we have one real feature, verify the skeleton still works:
1. Run full test suite
2. Check that the CI pipeline passes
3. Verify no skeleton patterns were broken
4. Confirm new code follows skeleton conventions consistently
```

### 阶段 4：文档化和迭代

**步骤 8：在 CLAUDE.md 中记录决策**

```markdown
User: Update CLAUDE.md with:
1. Which skeleton we started from (repo URL, commit hash)
2. What we kept and why
3. What we removed and why
4. Any pattern deviations from the original skeleton
5. Conventions we've added on top
```

---

## 脚手架扩展时间线

```
Skeleton (Day 1)     →    MVP (Week 1)      →    Production (Month 1)
──────────────────────────────────────────────────────────────────────
1 example route      →    5 real routes      →    20+ routes
1 example test       →    30 tests           →    200+ tests
Basic config         →    Env-based config   →    Multi-env + secrets
SQLite/local DB       →    Docker PostgreSQL   →    Managed DB + migrations
No CI                 →    Basic CI            →    Full CI/CD pipeline
README only           →    CLAUDE.md + ADRs     →    Full documentation
```

---

## 真实世界示例：从脚手架到微服务

```bash
# 1. 克隆可靠脚手架
git clone https://github.com/example/express-prisma-starter skeleton
cd skeleton && claude

# 2. 审计（2 分钟）
User: "Audit this skeleton. Is it suitable for a billing microservice?"
# Claude: Reports deps, patterns, suitability score

# 3. 定制（5 分钟）
User: "Strip examples, rename to billing-service, add our CLAUDE.md"
# Claude: Removes demo code, updates config, adds project context

# 4. 第一个功能（30 分钟）
User: "Implement invoice creation endpoint following skeleton patterns"
# Claude: Creates route, service, repo, tests matching skeleton conventions

# 5. 验证（2 分钟）
User: "Run all tests, verify build, check skeleton patterns preserved"
# Claude: All green, patterns consistent
```

---

## 常见陷阱

| 陷阱 | 症状 | 修复 |
|---------|---------|-----|
| 脚手架太复杂 | 花在剥离上的时间比构建多 | 选择更简单的脚手架，或自己构建最小的 |
| 依赖过时 | 安装时安全警告 | 在克隆前检查最后提交日期（< 6 个月理想） |
| 破坏脚手架模式 | 新代码偏离脚手架约定 | 将脚手架模式添加到 CLAUDE.md 作为约束 |
| 保留死代码 | 未使用的示例代码弄乱项目 | 在阶段 2 彻底剥离，每次移除后验证构建 |
| 无文档 | 忘记为什么选择脚手架 | 立即在 CLAUDE.md 中文档化（阶段 4） |

---

## 相关工作流

- **[Vibe Coding](#98-vibe-coding-skeleton-projects)**：在选择脚手架前探索
- **[计划驱动开发](./plan-driven.md)**：执行前先计划脚手架定制
- **[使用 Claude 进行 TDD](./tdd-with-claude.md)**：脚手架功能的测试先行扩展
- **[排列框架](#919-permutation-frameworks)**：在承诺之前测试多个脚手架变体

---

**最后更新**：2026 年 1 月