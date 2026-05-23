<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "变更日志片段：每个 PR 强制文档化"

description: "三层强制模式，确保每个 PR 在编写时文档化，而不是在发布时"
tags: [workflow, changelog, automation, ci, git]
---

# 变更日志片段：每个 PR 强制文档化

三层强制模式，确保每个 PR 在编写时文档化，而不是在发布时。

---

## 问题

单一的 `CHANGELOG.md` 文件在活跃团队中会出问题。三个开放的功能分支都修改同一个文件意味着每次合并都有冲突。有人解决冲突、删掉一行，发布说明在发布前就错了。

更深层的问题是时机。"在发布时文档化"听起来合理，直到你在 PR #840 合并三周后盯着它，试图为用户重建变更。提交说 `fix session handling`。开发者在不同 timezone。上下文没了。

没有 CI 门禁的强制执行意味着变更日志变成追着人跑的任务。每次发布前，在时间压力下，有人得追着人从 git log 填补空白。

解决方案：每个 PR 一个 YAML 片段，在实现时编写，由 CI 验证，在发布时自动组装。

---

## 三层架构

系统之所以有效，是因为强制发生在三个独立层级。每个层级捕获不同的失败模式。

### 第 1 层：CLAUDE.md 工作流规则

第一层是在每个会话加载到 Claude Code 上下文的规则。它编码整个片段工作流，以便在要求创建 PR 时 Claude 可以自主完成。

```markdown
# git-workflow.md（通过 CLAUDE.md 加载）

## 变更日志片段 — 每个 PR 前必填

创建 PR 前，始终生成变更日志片段。

### 步骤

1. **从 git diff 推断** — 分析 `git diff main...HEAD` 确定：
   - `type`：feat | fix | perf | refactor | security | docs | chore
   - `scope`：受影响的功能区域（auth、sessions、api 等）
   - `title`：一行用户面向摘要（< 80 字符）

2. **创建片段** — 运行 `pnpm changelog:add` 或直接写入：
   ```
   changelog/fragments/{PR_NUMBER}-{slug}.yml
   ```

3. **验证** — 运行 `pnpm changelog:validate changelog/fragments/{file}.yml`

4. **与 PR 一起提交** — 将片段包含在同一分支中

### 片段 schema

```yaml
pr: 886                    # 必须匹配文件名前缀
type: fix                  # feat|fix|perf|refactor|security|docs|chore
scope: "visiochat"
title: "Fix empty chat after SSE race condition"   # < 80 字符
description: |             # 可选 — 解释用户影响，而非实现
  SSE workplan fires before AI stream completes, causing ChatWrapper
  to mount with 0 messages.
breaking: false
migration: false           # 如果 PR 添加数据库迁移设为 true
```

### 绕过

对没有用户影响的 PR 添加标签 `skip-changelog`（CI 配置、依赖更新、发布提交）。
```

这条规则使 Claude Code 成为强制执行的参与者，而不仅仅是一个编码工具。当开发者说"创建 PR"时，Claude 从 diff 推断片段内容并在打开 PR 前创建它。

### 第 2 层：UserPromptSubmit 钩子（行为检测）

第二层在实际行动之前拦截意图。当开发者输入表示 PR 创建意图的内容时，钩子检查是否提到了变更日志片段。

```bash
# .claude/hooks/smart-suggest.sh（节选 — 第 0 层强制）

# 检测到 PR 创建意图
if echo "$PROMPT_LC" | grep -qE '(create.*pr|open.*pr|make.*pr|pull.?request|push.*pr)'; then
    # 未提到片段 → 先重定向到创建步骤
    if ! echo "$PROMPT_LC" | grep -qE '(changelog|fragment|skip-changelog)'; then
        suggest "pnpm changelog:add" \
            "REQUIRED before merge — creates changelog/fragments/{PR}-{slug}.yml"
    else
        # 已提到 → 正常建议 PR 命令
        suggest "/pr" "PR creation with structured description"
    fi
fi
```

钩子是 `UserPromptSubmit`：非阻塞，每个提示最多一个建议，匹配时静默。它在 Claude Code 处理提示之前运行，所以开发者在 Claude 开始做任何事情之前在行内看到提醒。

条件逻辑（`if X without Y`）是关键模式。不是全面阻塞 — 它适应上下文。如果开发者已经提到片段，他们得到正常建议。如果没有，他们得到强制提醒。

**带三层架构的完整钩子**：见 [`examples/hooks/bash/smart-suggest.sh`](../../examples/hooks/bash/smart-suggest.sh)

### 第 3 层：CI 强制执行（GitHub Actions）

第三层是硬门禁。两个独立作业在每个针对 main 分支的 PR 上运行。

**`check-fragment` 作业**：首先检查绕过标签（封闭列表），然后要求 `changelog/fragments/{PR_NUMBER}-*.yml` 存在并通过结构验证。

```yaml
- name: Check fragment exists and is valid
  env:
    PR_NUMBER: ${{ github.event.pull_request.number }}
    PR_LABELS: ${{ toJson(github.event.pull_request.labels.*.name) }}
  run: |
    SKIP_LABELS=("skip-changelog" "dependencies" "release" "chore: deps")
    for LABEL in "${SKIP_LABELS[@]}"; do
      if echo "$PR_LABELS" | grep -q "\"$LABEL\""; then
        echo "Bypass label detected — fragment not required"
        exit 0
      fi
    done

    FRAGMENT=$(ls "changelog/fragments/${PR_NUMBER}-"*.yml 2>/dev/null | head -1)
    if [ -z "$FRAGMENT" ]; then
      echo "Fragment missing. Run: pnpm changelog:add"
      exit 1
    fi

    pnpm tsx changelog/scripts/validate.ts "$FRAGMENT"
```

**`check-migration-flag` 作业**（独立运行，无绕过）：用 `git diff --name-only --diff-filter=A` 检测新的 SQL 迁移文件。如果存在迁移而片段中 `migration: false`，则失败。这个作业不能被标签绕过 — 添加了迁移的 `skip-changelog` PR 仍会触发检查。

两个作业设计为独立的。PR 可以绕过片段创建（通过标签）但仍会失败迁移检查。

---

## 发布时片段组装

片段在 PR 合并时积累在 `changelog/fragments/` 中。在发布时，一个命令将它们组装成版本化的 CHANGELOG 部分。

```bash
pnpm changelog:assemble --version 1.8.0 [--dry-run]
```

作用：
1. 读取所有 `changelog/fragments/*.yml`
2. 按固定顺序按 type 分组（feat、fix、perf、refactor、security、docs、chore）
3. 将 `breaking: true` 条目提取到专用的 `🔨 Breaking Changes` 部分
4. 用 `⚠️ Migration DB.` 内联标注 `migration: true` 条目
5. 替换 `CHANGELOG.md` 中的 `## [Next Release]` 占位符
6. 将片段存档到 `changelog/fragments/released/{version}/`

输出：
```markdown
## [1.8.0] - 2026-03-15

### 🔨 Breaking Changes
- **Remove legacy token format (#871)** — Tokens issued before v1.6.0 are invalid.

### ✨ New Features
- **Add real-time presence indicators (#892)**

### 🔧 Bug Fixes
- **Fix empty chat after SSE race condition (#886)** — SSE workplan fires before
  AI stream completes, causing ChatWrapper to mount with 0 messages.
```

---

## 为什么是 3 层，而不是 1 层

每层捕获不同的失败模式：

| 层级 | 捕获的失败 | 何时 |
|-------|---------------|------|
| CLAUDE.md 规则 | Claude 忘记工作流 | 每个会话 |
| UserPromptSubmit 钩子 | 开发者在不考虑时输入"创建 PR" | 预提示 |
| CI 门禁 | 片段被跳过或损坏 | 预合并 |

单一的 CI 门禁捕获问题太晚 — 开发者必须在 PR 打开后切换回上下文。钩子在意图时捕获。CLAUDE.md 规则意味着 Claude 在被赋予任务时自主处理它。

各层不冲突。它们相互加强。看到钩子建议的开发者会运行 `pnpm changelog:add`。Claude 会遵循 CLAUDE.md 规则并验证输出。CI 在合并前确认一切。

---

## 采用此模式

TypeScript 脚本（add、validate、assemble、audit）特定于 Méthode Aristote 堆栈。三层强制模式不是 — 它适用于任何片段格式、任何 CI 系统、任何组装器。

**最小可行设置：**

1. **定义你的片段 schema**（YAML、JSON，或任何适合你堆栈的格式）
2. **添加 CLAUDE.md 规则** 编码创建工作流以便 Claude 可以自主处理
3. **添加 `UserPromptSubmit` 钩子** 带有 `if PR-intent without fragment-mention → suggest` 模式
4. **添加 CI 作业** 在合并前检查片段存在

钩子模式泛化到任何必选工作流步骤。将"变更日志片段"替换为"ADR"、"迁移标志"、"测试覆盖率检查" — 条件检测逻辑相同。

---

## 相关

- 钩子示例：[`examples/hooks/bash/smart-suggest.sh`](../../examples/hooks/bash/smart-suggest.sh)
- 钩子文档：[UserPromptSubmit 钩子](../ultimate-guide.md)（搜索 "UserPromptSubmit"）
- 片段验证器和组装器脚本：在 Méthode Aristote 仓库可用