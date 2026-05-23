---
name: commit
description: 为暂存更改生成符合 Conventional Commit 规范的提交信息
argument-hint: "[--amend] [message]"
effort: low
disable-model-invocation: true
---

# Conventional Commit

为暂存更改生成符合 Conventional Commit 规范的提交信息。

## 使用说明

1. 运行 `git diff --cached` 查看暂存的更改
2. 分析更改的性质
3. 按以下格式生成提交信息

## 提交信息格式

```
<类型>(<范围>): <标题>

[可选正文]

[可选脚注]
```

### 类型
- `feat`：新功能
- `fix`：Bug 修复
- `docs`：仅文档
- `style`：格式调整、缺少分号等
- `refactor`：既不修复 bug 也不增加功能的代码更改
- `perf`：性能改进
- `test`：补充缺失的测试
- `chore`：维护任务

### 规则
- 标题：祈使句，无句号，最多 50 个字符
- 正文：解释做了什么和为什么，而非怎么做
- 脚注：破坏性变更、问题引用

## 示例

```
feat(auth): add password reset functionality

Implement password reset flow with email verification.
Users can now request a reset link and set new password.

Closes #123
```

```
fix(api): prevent race condition in order processing

Add mutex lock to ensure orders are processed sequentially.
This fixes duplicate charge issues reported by users.

Fixes #456
```

```
refactor(cart): extract pricing logic to separate module

No functional changes. Improves testability and
separates concerns for future discount feature.
```

## 执行

分析暂存的更改后，建议一条提交信息。在执行 `git commit -m "..."` 前要求确认。

$ARGUMENTS
