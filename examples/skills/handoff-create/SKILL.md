---
name: handoff-create
description: 从当前会话生成结构化的交接文档。捕获范围、相关文件（含行号）、关键发现、已完成工作、当前状态、后续步骤和代码片段。在结束会话或将工作交接给其他 agent 前使用。
argument-hint: "[可选文件名]"
effort: low
disable-model-invocation: true
---

根据我们当前的对话生成结构化的交接文档，保存到 `claudedocs/handoffs/handoff_YYYYMMDD_HHMMSS.md`（如果提供了 `$ARGUMENTS[0]` 则使用提供的文件名）。

如果 `claudedocs/handoffs/` 目录不存在则创建。

## 文档结构

必须包含以下章节：

```markdown
# 交接 — [任务名称] — [YYYY-MM-DD HH:MM]

## 任务

[一句话：正在完成什么]

## 范围

[需要完成什么。明确说明边界 — 哪些在范围内、哪些明确不在范围内]

## 文件

[所有涉及到的或需要的文件。格式：`path/to/file:line`（涉及特定行时）]

- `src/auth/middleware.ts:45` — token 验证逻辑
- `tests/auth.spec.ts` — 此更改的测试套件
- `docs/api.md` — 实现后需要更新

## 发现

[到目前为止工作过程中的关键发现和洞见。下一位 agent 需要知道但不明显的线索]

- [发现 1]
- [发现 2]

## 已完成工作

[已完成的任务。仅追加 — 永不删除已有条目。包含 commit hash（如有）]

- [x] 任务 A 已完成（commit：abc1234）
- [x] 任务 B 已完成

## 状态

[当前状态：哪些已完成、哪些待办、测试状态、阻塞项]

## 下一步

[可操作的待办清单，按顺序排列]

1. [ ] 步骤 1
2. [ ] 步骤 2
3. [ ] 步骤 3

## 代码

[相关代码片段及上下文。重点关注接手的 agent 需要立即理解的部分]

\`\`\`typescript
// 关键实现细节
\`\`\`
```

## 规则

- 总字数控制在 600 字以内。接手的 agent 应在阅读后 30 秒内理解并继续工作。
- 所有文件引用使用 `path/to/file:line` 格式。行号很重要。
- "已完成工作"仅追加。永不删除已有条目。
- 不包含完整的 git diff 或完整文件内容。仅包含非显而易见的代码片段。

保存后，确认文件路径。
