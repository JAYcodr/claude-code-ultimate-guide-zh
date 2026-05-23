---
name: session-save
description: 保存当前会话状态——决策、修改的文件、当前状态和后续步骤——到交接文件中以便后续恢复。
effort: low
disable-model-invocation: true
---

# /session-save

将当前会话捕获到结构化的交接文件中，以便你（或其他实例）能在完整上下文中恢复。在 `.claude/sessions/` 中创建带时间戳的 Markdown 文件。

## 何时使用

- 在结束未完成的会话前
- 在切换到不同任务前
- 在上下文达到 75%+ 前（以保留重要部分）
- 在长任务的自然里程碑处（每个阶段完成后）
- 交接给另一个 Claude 实例

## 使用说明

生成具有以下结构的交接文档：

---

## 会话交接 — [时间戳]

### 正在做什么
[一段：目标、方法、当前进展]

### 本会话修改的文件
[列出创建、编辑或删除的每个文件——附带更改性质]

```
path/to/file.ts      — [改了啥、为什么]
path/to/other.ts     — [改了啥、为什么]
```

### 关键决策
[架构选择、接受的权衡、被拒绝的方法及其原因]

- **决策**：[决定了什么]
  - **理由**：[为什么]
  - **被拒绝的替代方案**：[还考虑了哪些]

### 当前状态
[当前进展——哪些在运行、哪些有问题、哪些进行中]

- 正常运行：[...]
- 进行中：[...]
- 已知问题：[...]

### 后续步骤（按顺序）
[确切的下一个操作——具体到新上下文无需重读所有内容即可接手]

1. [第一个操作] — `path/to/file.ts` — [做什么]
2. [第二个操作] — [...]
3. [...]

### 需重新加载的上下文
[必须以完整理解恢复的文件——保持短列表]

- `path/to/key-file.ts` — [为什么重要]
- `CLAUDE.md` — 项目规则

### 阻塞项 / 未解决问题
[需要决策或外部输入才能继续的任何未解决事项]

- [ ] [问题或阻塞项] — [谁/什么可以解决]

---

## 实现

将交接保存到 `.claude/sessions/handoff-[YYYY-MM-DD-HHMM].md`。然后输出文件路径，让用户知道在哪找到它。

## 恢复模式

从交接恢复：

```
/session-resume .claude/sessions/handoff-YYYY-MM-DD-HHMM.md
```

或手动：读取交接文件，然后在继续前读取"需重新加载的上下文"中列出的文件。

## 示例

### 示例 1：功能中期保存

```
/session-save
```

Claude 捕获：
- 正在重构认证中间件（文件：`src/middleware/auth.ts`、`src/middleware/jwt.ts`）
- 决策：从 session token 切换到 JWT（理由：跨服务扩展性更好）
- 状态：JWT 验证可用，刷新逻辑进行中
- 下一步：在 `src/services/auth.service.ts` 中实现 `refreshToken()`，然后更新测试

### 示例 2：上下文压力保存

当上下文达到 70% 时，在 `/compact` 前运行 `/session-save`，保留压缩可能丢失的决策上下文。

## 说明

- "需重新加载的上下文"最多 5 个文件——目标是快速恢复，而非全面重读
- "后续步骤"应具体到冷启动的 Claude 可以在不提问的情况下执行步骤 1
- 不要在交接中保存工具输出或代码片段——改为引用文件路径

---

**另见**：
- [Session Teleportation](/guide/ultimate-guide.md#916-session-teleportation) — 更广泛的会话管理模式
- [Instinct-Based Learning](/guide/ultimate-guide.md#924-instinct-based-continuous-learning) — 关闭前从会话中提取的内容
