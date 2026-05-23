---
name: ci-status
description: 显示当前分支的流水线状态 — GitLab CI 或 GitHub Actions
argument-hint: "[可选 pr_number]"
allowed-tools: [Bash]
model: haiku
effort: low
disable-model-invocation: true
---

# /ci:status — 流水线状态

快速查看当前分支的 CI 流水线快照。

## 流程

```bash
# 1. 当前分支
BRANCH=$(git branch --show-current)
echo "分支：$BRANCH"

# 2. 最近提交
git log -3 --oneline
```

## GitLab CI

```bash
# 使用 glab CLI（推荐）
if command -v glab &>/dev/null; then
  glab ci status --branch "$BRANCH"
else
  # 回退：显示 URL
  REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
  if [ -n "$REMOTE" ]; then
    WEB_URL=$(echo "$REMOTE" | sed 's/git@gitlab\.com:/https:\/\/gitlab.com\//' | sed 's/\.git$//')
    echo "流水线：$WEB_URL/-/pipelines?ref=$BRANCH"
  fi
fi

# 如提供了 MR 编号
if [ -n "$ARGUMENTS" ] && command -v glab &>/dev/null; then
  glab mr view "$ARGUMENTS"
fi
```

## GitHub Actions

```bash
# 使用 gh CLI（推荐）
if command -v gh &>/dev/null; then
  gh run list --branch "$BRANCH" --limit 5
else
  # 回退：显示 URL
  REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
  if [ -n "$REMOTE" ]; then
    WEB_URL=$(echo "$REMOTE" | sed 's/git@github\.com:/https:\/\/github.com\//' | sed 's/\.git$//')
    echo "Actions：$WEB_URL/actions?query=branch%3A$BRANCH"
  fi
fi

# 如提供了 PR 编号
if [ -n "$ARGUMENTS" ] && command -v gh &>/dev/null; then
  gh pr checks "$ARGUMENTS"
fi
```

## 预期输出

```
分支：feat/add-payment-retry

最近提交：
  a1b2c3d feat(payments): add retry logic with exponential backoff
  e4f5g6h test(payments): add Vitest coverage on retry scenarios
  i7j8k9l chore: update pnpm lockfile

流水线：running
  ✅ lint          30s
  ✅ typecheck     45s
  ⏳ test          running...
  ⏸️  deploy        waiting

URL：https://gitlab.com/org/my-app/-/pipelines?ref=feat/add-payment-retry
```

## 用法

```
/ci:status
/ci:status 42    # MR 或 PR 编号 42
```

Target: $ARGUMENTS
