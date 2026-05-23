<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "任务管理工作流"
description: "使用 Tasks API 和 TodoWrite 进行多会话任务协调，适用于复杂项目"
tags: [workflow, guide, agents]
---

# 任务管理工作流

**版本**：Claude Code v2.1.16+
**前置要求**：理解多会话工作流，基本 CLI 熟练度
**时间**：15-30 分钟学习，适用于所有复杂项目

## 概述

任务管理在 v2.1.16 中引入 **Tasks API** 后有了显著演进，作为原始 **TodoWrite** 工具的补充。本工作流教你何时使用每个系统，以及如何利用多会话任务协调来处理复杂项目。

**何时使用此工作流：**
- 跨越多个编码会话的项目
- 多智能体协调场景
- 带依赖的复杂任务层次结构
- 需要在上下文压缩或会话中断后恢复工作

**何时不使用：**
- 单会话的直接实现
- 快速修复或探索性编码
- 可在 <10 分钟内完成的任务

---

## 系统对比快速参考

| 功能 | TodoWrite（遗留） | Tasks API（v2.1.16+） |
|---------|-------------------|---------------------|
| **持久化** | 仅会话内存 | 磁盘存储（`~/.claude/tasks/`） |
| **多会话** | ❌ 会话结束时丢失 | ✅ 跨会话存活 |
| **依赖** | ❌ 手动排序 | ✅ 任务阻塞（A 阻塞 B） |
| **协调** | 单智能体 | ✅ 多智能体广播 |
| **状态跟踪** | pending/in_progress/completed | pending/in_progress/completed |
| **何时使用** | 简单单会话待办 | 复杂多会话项目 |

**迁移开关**（v2.1.19+）：
```bash
# 使用旧系统（TodoWrite）
CLAUDE_CODE_ENABLE_TASKS=false claude

# 使用新系统（Tasks API）— 自 v2.1.19 起默认
claude
```

---

## 工作流阶段 1：任务规划

**目标**：将复杂工作分解为可跟踪、可执行的单元

### 步骤 1：分析范围

在创建任务之前，理解你要构建的内容：

```bash
# 发现模式
claude
> "Analyze this codebase for implementing JWT authentication:
  - Glob for existing auth patterns
  - Grep for security-related code
  - Identify integration points"
```

### 步骤 2：设计任务层次结构

将工作分解为带依赖的逻辑阶段：

**示例：认证系统**
```
Authentication System (parent)
├── 1. Login endpoint (no dependencies)
├── 2. Token refresh (depends on #1)
├── 3. Logout endpoint (depends on #1)
└── 4. Integration tests (depends on #1, #2, #3)
```

### 步骤 3：创建任务结构

使用 `TaskCreate` 将你的计划具体化：

```bash
# 会话 1：规划阶段
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

# 在 Claude 会话中：
> "Create a task hierarchy for JWT authentication:

  Parent task: 'Implement JWT authentication system'
  - Description: Add JWT-based auth with refresh tokens and secure storage

  Child tasks:
  1. 'Create login endpoint' (no dependencies)
  2. 'Implement token refresh logic' (depends on task 1)
  3. 'Create logout endpoint' (depends on task 1)
  4. 'Write integration tests' (depends on tasks 1, 2, 3)

  Use TaskCreate with proper metadata."
```

**Claude 的预期输出：**
```json
{
  "tasks": [
    {
      "id": "task-auth-parent",
      "title": "Implement JWT authentication system",
      "status": "pending",
      "children": ["task-login", "task-refresh", "task-logout", "task-tests"]
    },
    {
      "id": "task-login",
      "title": "Create login endpoint",
      "status": "pending",
      "dependencies": [],
      "metadata": {"priority": "high", "estimated_duration": "2h"}
    },
    {
      "id": "task-refresh",
      "title": "Implement token refresh logic",
      "status": "pending",
      "dependencies": ["task-login"],
      "metadata": {"priority": "high", "estimated_duration": "1h"}
    }
    // ... other tasks
  ]
}
```

---

## 工作流阶段 2：任务执行

**目标**：系统地执行任务并跟踪进度

### 执行模式

```
TaskList → TaskGet（下一个 pending）→ 执行 → TaskUpdate → 验证 → 重复
```

### 步骤 1：发现下一个任务

```bash
# 会话 2：开始实现
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show all pending tasks"
```

**输出：**
```
Tasks for 'auth-system-v2':
✅ task-login: Create login endpoint [completed]
⏳ task-refresh: Implement token refresh logic [pending, blocked by: none]
⏳ task-logout: Create logout endpoint [pending, blocked by: none]
⏳ task-tests: Write integration tests [pending, blocked by: task-refresh, task-logout]
```

### 步骤 2：获取任务详情

```bash
> "TaskGet task-refresh to see full requirements"
```

**输出：**
```json
{
  "id": "task-refresh",
  "title": "Implement token refresh logic",
  "description": "Create endpoint POST /auth/refresh that validates refresh token and issues new access token",
  "status": "pending",
  "dependencies": ["task-login"],
  "metadata": {
    "priority": "high",
    "estimated_duration": "1h",
    "files": ["src/auth/refresh.ts", "src/middleware/auth.ts"]
  }
}
```

### 步骤 3：执行并更新

```bash
> "Mark task-refresh as in_progress, then implement the token refresh endpoint according to requirements"

# Claude 执行：TaskUpdate task-refresh status=in_progress
# Claude 实现功能...
# 完成后：

> "Mark task-refresh as completed"
# Claude 执行：TaskUpdate task-refresh status=completed
```

### 步骤 4：验证

```bash
> "Run tests for token refresh functionality"

# 如果测试通过：
# ✅ Task remains completed

# 如果测试失败：
> "TaskUpdate task-refresh status=in_progress, add error details to metadata and fix issues"
```

---

## 工作流阶段 3：会话管理

**目标**：跨会话和上下文边界无缝恢复工作

### 持久化机制

**存储位置**：`~/.claude/tasks/<task-list-id>/`

任务存活于：
- 会话终止
- 上下文压缩（`/compact`）
- 系统重启
- 多天中断

#### ⚠️ 字段可见性限制

**TaskList 仅返回**：`id`、`subject`、`status`、`owner`、`blockedBy`

**TaskList 输出中缺少**：
- `description`（需要对每个任务执行 TaskGet）
- `metadata`（自定义字段如 priority、estimates）
- `activeForm`（进度微调文本）

**工作流调整**：

```bash
# 不要：假设可以扫描所有描述
TaskList  # 仅显示 subject

# 应该：有选择地获取
TaskList                    # 获取概览（存在哪些任务、状态）
TaskGet(task-auth-login)    # 获取特定任务的完整详情
TaskGet(task-auth-tests)    # 获取下一个任务的详情
```

**这在以下情况重要**：
- 具有详细任务描述的复杂项目（每个任务 >50 词）
- 需要共享上下文可见性的多智能体协调
- 需要快速扫描所有任务笔记以决定恢复点

**成本意识**：
- TaskList = 1 次 API 调用
- 获取 N 个任务的描述 = 1 + N 次调用
- 对于 20 个任务，如果需要所有描述，则开销是 20 倍

**缓解**：
- 使用 `subject` 字段存储关键信息（TaskList 可见）
- 保持 `description` 简洁（最多 50-100 词）
- 在 markdown 文件中存储详细计划（`docs/plan-*.md`）

### 恢复模式

```bash
# 几天后，不同终端会话
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show current state"

# 输出准确显示你离开的位置：
# ✅ task-login [completed]
# ✅ task-refresh [completed]
# ⏳ task-logout [pending]
# ⏳ task-tests [pending, blocked by: task-logout]

> "Continue with next pending task that isn't blocked"
```

### 多终端协调

**用例**：运行多个 Claude 实例处理同一项目

```bash
# 终端 1：前端工作
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "Work on task-logout endpoint"

# 终端 2：测试编写（同时）
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "TaskList - check what's completed so I can write tests"

# 两个终端都能看到实时状态更新
```

**⚠️ 警告**：使用仓库特定的任务列表 ID 以避免跨项目污染：
```bash
# ❌ 不好：在多个仓库中使用通用 ID
export CLAUDE_CODE_TASK_LIST_ID="my-project"

# ✅ 好：带上下文的仓库特定 ID
export CLAUDE_CODE_TASK_LIST_ID="mycompany-api-auth-refactor"
```

---

## 集成：TDD + 任务管理

将测试驱动开发与任务跟踪结合，实现系统化的测试覆盖。

### 模式：测试优先任务执行

```bash
export CLAUDE_CODE_TASK_LIST_ID="tdd-feature-x"
claude

# 使用测试优先方法创建任务
> "Create task hierarchy for feature X:

  For each feature component:
  1. Task: 'Write failing tests for [component]'
  2. Task: 'Implement [component] to pass tests' (depends on #1)
  3. Task: 'Refactor [component]' (depends on #2)

  Use TDD red-green-refactor cycle per task."
```

### 示例：带 TDD 的登录功能

```bash
# 阶段 1：Red（失败测试）
TaskCreate: {
  title: "Write failing tests for login endpoint",
  description: "Test cases: valid credentials, invalid password, user not found, rate limiting",
  status: "pending"
}

# 执行测试编写
> "Implement task-login-tests, ensure all tests fail initially"

# 阶段 2：Green（最小实现）
TaskCreate: {
  title: "Implement login endpoint (minimal)",
  description: "Make tests pass with simplest possible implementation",
  dependencies: ["task-login-tests"],
  status: "pending"
}

# 阶段 3：Refactor
TaskCreate: {
  title: "Refactor login endpoint",
  description: "Optimize, remove duplication, improve readability",
  dependencies: ["task-login-impl"],
  status: "pending"
}
```

**完整工作流参考**：参见 [TDD with Claude](tdd-with-claude.md#task-management-integration)

---

## 集成：计划驱动 + 任务管理

将战略计划转换为可执行的任务层次结构。

### 模式：计划到任务转换

```bash
# 步骤 1：进入计划模式
claude
> [Press Shift+Tab to enter Plan Mode]

# 步骤 2：创建架构计划
> "Design architecture for microservices migration:
  - Identify service boundaries
  - Plan data migration strategy
  - Design API contracts"

# 步骤 3：退出计划模式并创建任务
> "Convert this plan into a task hierarchy using TaskCreate"
```

### 示例：微服务迁移

**计划输出：**
```
Phase 1: Analysis (Week 1)
- Map monolith dependencies
- Identify bounded contexts
- Design service boundaries

Phase 2: Infrastructure (Week 2)
- Set up service templates
- Configure API gateway
- Establish monitoring

Phase 3: Migration (Week 3-6)
- Extract user service
- Extract order service
- Migrate database schemas
```

**任务转换：**
```bash
TaskCreate: {
  title: "Microservices migration",
  children: [
    {
      title: "Phase 1: Analysis",
      children: [
        {title: "Map monolith dependencies", priority: "critical"},
        {title: "Identify bounded contexts", dependencies: ["map-deps"]},
        {title: "Design service boundaries", dependencies: ["bounded-contexts"]}
      ]
    },
    {
      title: "Phase 2: Infrastructure",
      dependencies: ["phase-1"],
      children: [
        {title: "Set up service templates"},
        {title: "Configure API gateway", dependencies: ["templates"]},
        {title: "Establish monitoring"}
      ]
    }
    // ... Phase 3
  ]
}
```

**完整工作流参考**：参见 [Plan-Driven Development](plan-driven.md#task-hierarchy-design)

---

## TodoWrite 迁移指南

###何时迁移

**继续使用 TodoWrite 如果：**
- ✅ 所有工作在单个会话中完成
- ✅ 不需要多智能体协调
- ✅ 简单线性任务列表（无依赖）
- ✅ 使用 Claude Code < v2.1.16

**迁移到 Tasks API 如果：**
- ✅ 工作跨越多个会话
- ✅ 需要跨天/周的任务持久化
- ✅ 复杂依赖图
- ✅ 多终端协作
- ✅ 希望在上下文压缩后恢复

### 迁移步骤

#### 步骤 1：识别 TodoWrite 使用情况

```bash
# 在你的 CLAUDE.md 或工作流中找到现有的 TodoWrite 使用
grep -r "TodoWrite" .claude/
```

#### 步骤 2：将 TodoWrite 列表转换为 Tasks

**之前（TodoWrite）：**
```markdown
- [ ] Implement user authentication
- [ ] Add password hashing
- [ ] Create session management
- [ ] Write tests
```

**之后（Tasks API）：**
```bash
export CLAUDE_CODE_TASK_LIST_ID="user-auth-2026"
claude

> "Create tasks:
  1. 'Implement user authentication' (parent)
     - Child: 'Add password hashing'
     - Child: 'Create session management' (depends on hashing)
     - Child: 'Write tests' (depends on auth, hashing, sessions)"
```

#### 步骤 3：更新 CLAUDE.md 说明

**之前：**
```markdown
For complex tasks:
- Use TodoWrite to create task list
- Execute tasks sequentially
```

**之后：**
```markdown
For complex tasks:
- Set CLAUDE_CODE_TASK_LIST_ID=<project-name>
- Use TaskCreate for hierarchical planning
- Execute with TaskUpdate status tracking
- Resume with TaskList in new sessions
```

#### 步骤 4：测试迁移

```bash
# 创建测试任务列表
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "Create 3 test tasks with dependencies, mark one completed, then exit"

# 在新会话中重新启动
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "TaskList - verify tasks persisted correctly"

# 预期：看到所有 3 个任务及其正确状态
```

---

## 模式与反模式

### ✅ 好模式

#### 1. 层级任务分解

```bash
Project (parent)
└── Feature A (child of project)
    ├── Component A1 (child of Feature A)
    │   ├── Implementation (leaf task)
    │   └── Tests (leaf task, depends on Implementation)
    └── Component A2
        └── ...
```

**为什么有效**：反映自然项目结构，使依赖关系明确

#### 2. 依赖优先排序

```bash
# 创建任务时始终定义依赖
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["run-tests", "code-review", "backup-database"],
  metadata: {blocking_reason: "Safety checks required"}
}
```

**为什么有效**：防止过早执行，强制执行质量门禁

#### 3. 粒度状态更新

```bash
# 不好：大型任务在没有中间更新的情况下标记为完成
TaskCreate: {title: "Build entire auth system"}
# ... 几小时后 ...
TaskUpdate: {id: "auth-system", status: "completed"}

# 好：随着工作进展频繁更新状态
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "25%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "50%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "75%"}
TaskUpdate: {id: "auth-system", status: "completed"}
```

**为什么有效**：提供可见性，支持上下文感知恢复

#### 4. 元数据丰富的任务

```bash
TaskCreate: {
  title: "Optimize database queries",
  description: "Reduce query time for user dashboard from 2s to <200ms",
  metadata: {
    priority: "high",
    estimated_duration: "3h",
    related_files: ["src/db/queries.ts", "src/db/indexes.sql"],
    performance_baseline: "2000ms",
    performance_target: "200ms",
    related_issue: "https://github.com/org/repo/issues/123"
  }
}
```

**为什么有效**：丰富的上下文恢复，更易于委托，更好的文档

### ❌ 反模式

#### 1. 单体任务（>10 步）

```bash
# ❌ 不好：任务太大，难以跟踪进度
TaskCreate: {
  title: "Implement entire payment system",
  description: "Stripe integration, webhooks, refunds, disputes, reporting, admin UI, ..."
}

# ✅ 好：分解为阶段
TaskCreate: {
  title: "Payment system - Phase 1: Core integration",
  children: [
    {title: "Stripe SDK setup"},
    {title: "Payment intent creation"},
    {title: "Webhook handling"}
  ]
}
```

#### 2. 缺少依赖

```bash
# ❌ 不好：任务可以按错误顺序执行
TaskCreate: {title: "Deploy to production"} # No dependencies
TaskCreate: {title: "Write tests"} # No dependencies

# ✅ 好：显式排序
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["write-tests", "run-tests", "code-review"]
}
```

#### 3. 无上下文的孤立任务

```bash
# ❌ 不好：将来的你不会记得这是什么意思
TaskCreate: {
  title: "Fix the bug",
  description: "That one from yesterday"
}

# ✅ 好：自包含的上下文
TaskCreate: {
  title: "Fix login timeout on Safari",
  description: "Users on Safari 17.2+ experience session timeout after 5min. Expected: 30min timeout. Root cause: cookie SameSite=Strict not supported.",
  metadata: {
    browser: "Safari 17.2+",
    error_message: "Session expired",
    related_commit: "a1b2c3d",
    slack_thread: "https://slack.com/archives/C123/p456"
  }
}
```

#### 4. 状态不匹配

```bash
# ❌ 不好：任务标记为完成但测试失败
TaskUpdate: {id: "login-feature", status: "completed"}
# 测试运行后发现：3 个失败

# ✅ 好：完成前验证
> "Run tests for login feature"
# 如果测试通过：
TaskUpdate: {id: "login-feature", status: "completed", metadata: {test_results: "pass"}}
# 如果测试失败：
TaskUpdate: {id: "login-feature", status: "in_progress", metadata: {test_results: "3 failures", error_log: "..."}}
```

---

## 故障排查

### Q：任务跨会话不持久化

**症状**：`TaskList` 在重启 Claude 后显示为空

**解决方案**：
```bash
# 确保启动前设置了 CLAUDE_CODE_TASK_LIST_ID
export CLAUDE_CODE_TASK_LIST_ID="your-project-name"
claude

# 验证存储目录存在
ls ~/.claude/tasks/your-project-name/
```

### Q：多个项目共享任务列表

**症状**：在项目 B 上工作时看到项目 A 的任务

**原因**：在不同仓库中使用相同的任务列表 ID

**解决方案**：
```bash
# 使用带上下文的仓库特定 ID
cd ~/projects/api
export CLAUDE_CODE_TASK_LIST_ID="api-v2-migration"
claude

cd ~/projects/frontend
export CLAUDE_CODE_TASK_LIST_ID="frontend-redesign"
claude
```

### Q：仍在使用 TodoWrite 而不是 Tasks API

**症状**：即使设置了任务列表 ID，任务也不持久化

**原因**：`CLAUDE_CODE_ENABLE_TASKS=false` 在环境中设置

**解决方案**：
```bash
# 检查环境
env | grep CLAUDE_CODE_ENABLE_TASKS

# 如果存在则取消设置
unset CLAUDE_CODE_ENABLE_TASKS

# 或显式启用（v2.1.19+ 默认启用）
export CLAUDE_CODE_ENABLE_TASKS=true
```

### Q：任务依赖未强制执行

**症状**：Claude 在依赖完成前执行被阻塞的任务

**原因**：TaskCreate 中依赖定义不正确

**解决方案**：
```bash
# 确保依赖使用正确的任务 ID
TaskCreate: {
  title: "Task B",
  dependencies: ["task-a-id"], # ✅ 使用实际任务 ID
  # 不是 dependencies: ["Task A"] # ❌ 任务标题不起作用
}

# 验证依赖：
TaskGet task-b-id
# 应显示："blockedBy": ["task-a-id"]
```

---

## 高级：自定义任务元数据

使用特定领域元数据扩展任务以增强工作流。

### 元数据约定

**性能优化任务：**
```json
{
  "metadata": {
    "type": "performance",
    "baseline_metric": "2000ms",
    "target_metric": "200ms",
    "profiling_tool": "Chrome DevTools",
    "measurement_location": "dashboard load time"
  }
}
```

**安全任务：**
```json
{
  "metadata": {
    "type": "security",
    "severity": "critical",
    "cve_id": "CVE-2024-1234",
    "affected_versions": "< 2.1.0",
    "mitigation": "Update package X to v3.0+"
  }
}
```

**Bug 修复任务：**
```json
{
  "metadata": {
    "type": "bugfix",
    "issue_url": "https://github.com/org/repo/issues/456",
    "reported_by": "user@example.com",
    "reproduction_steps": "1. Login 2. Navigate to dashboard 3. Click export",
    "error_message": "TypeError: Cannot read property 'map' of undefined"
  }
}
```

### 按元数据查询

```bash
# 按类型过滤任务（需要脚本，非内置）
TaskList | jq '.tasks[] | select(.metadata.type == "security")'

# 查找高优先级 pending 任务
TaskList | jq '.tasks[] | select(.metadata.priority == "high" and .status == "pending")'
```

---

## 会话生命周期协议

每个智能体会话都遵循相同的十步序列，从启动到提交。明确定义这些步骤（而不是让它们含蓄）正是使会话在中断后能够可靠恢复的原因。Anthropic 自己的工程团队直接观察到了这一点：在一个游戏编辑器实验中裸 Claude 运行失败了一半，而相同工作负载包装在结构化会话工具中则成功完成（来源：[Anthropic 工程博客](https://www.anthropic.com/engineering/harness-design-long-running-apps)）。

| 步骤 | 操作 | 产物 |
|------|--------|----------|
| START | 读取项目说明 | `AGENTS.md` 或 `CLAUDE.md` |
| INIT | 运行环境引导 | `init.sh` / `npm install && npm run check` |
| READ | 加载上一会话状态 | `progress.md` |
| SELECT | 选择一个功能，设置状态为 active | `feature_list.json` |
| EXECUTE | 仅实现该功能 | 源文件 |
| VERIFY | 运行三层验证（lint、测试、e2e） | 退出码 |
| WRAP UP | 记录完成和证据 | `progress.md`、`feature_list.json` |
| CLEANUP | 移除临时文件，验证仓库干净重启 | 仓库状态 |
| COMMIT | 在 git 中标记会话边界 | Git 历史 |
| HANDOFF | 编写或更新交接说明 | `claudedocs/handoffs/` |

### 连续性产物：`progress.md`

`progress.md` 是让 READ 步骤在几秒钟内完成而非几分钟的文件。它位于项目根目录，保持在 50 行以下，是为下一个智能体会话编写的，不是为人工审查者写的。这个区别很重要。交接文档（WRAP UP 和 HANDOFF 步骤）按设计是冗长的：它告诉人工审查者发生了什么、为什么做出决定以及要注意什么。`progress.md` 做的是更窄的事情。它记录活动功能 ID、上一次提交哈希、任何当前阻塞器以及智能体下一步应该采取的单一操作。无散文，无叙事。

```markdown
# Session Progress

last_updated: 2026-05-04
active_feature: feat-002
last_commit: a3f92c1
session_count: 3

## Status
- feat-001: passing (verified 2026-05-01)
- feat-002: active (in progress)
- feat-003: not_started

## Next action
Finish chunking implementation, then run: npm test -- --grep 'chunking'

## Blockers
None
```

下一会话在 READ 步骤中读取这个，获取 `active_feature: feat-002`，检查上一次提交哈希以在 git 历史中定向，然后直接进入下一个操作。无需冷启动简报。

### 这如何与交接三部曲组合

本工作流前面文档化的交接三部曲模式（创建、恢复、更新）和 `progress.md` 服务于阅读相同会话边界的不同受众。`progress.md` 给智能体一个机器可读的起点。交接文档给人工审查者关于发生了什么以及为什么的叙事账户。两者都不能替代对方，两者在同一步骤（WRAP UP）更新，这使它们保持同步而无需额外开销。

### COMMIT 步骤作为会话边界

在 COMMIT 步骤的提交不仅仅是一个 VCS 操作。它是对仓库处于可重启状态的断言。规则与交接三部曲相同：只在功能完成并验证后才提交。在未完成状态下留下的半实现功能意味着下一会话从破损环境开始，INIT 步骤的 `npm run check` 将立即失败，在任何新工作开始之前浮现问题。这个失败是信息性的，但通过持有提交直到 VERIFY 步骤干净通过来防止它更好。

关于跳过 VERIFY 步骤时发生的失败模式，请参见 [tdd-with-claude.md](tdd-with-claude.md#the-verification-gap) 中的验证差距。

---

## 相关工作流

- **[TDD with Claude](tdd-with-claude.md)** — 带任务跟踪的测试优先开发
- **[Plan-Driven Development](plan-driven.md)** — 战略规划到任务层次结构
- **[Iterative Refinement](iterative-refinement.md)** — 带任务的增量改进
- **[Exploration Workflow](exploration-workflow.md)** — 任务创建前的发现阶段

---

## 参考

**工具文档**：参见[终极指南第 5.X 节](#task-management-system)

**来源：**
- 官方：[Claude Code CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- 官方：[System Prompts - TaskCreate](https://github.com/Piebald-AI/claude-code-system-prompts)
- 社区：[paddo.dev - From Beads to Tasks](https://paddo.dev/blog/from-beads-to-tasks/)
- 社区：[llbbl.blog - Two Changes in Claude Code](https://llbbl.blog/2026/01/25/two-changes-in-claude-code.html)

**版本跟踪**：本工作流记录 Claude Code v2.1.16+（发布于 2026-01-22）。在 [claude-code-releases.yaml](../../machine-readable/claude-code-releases.yaml) 中验证最新更改。