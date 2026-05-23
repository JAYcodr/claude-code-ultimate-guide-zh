---
name: ci-pipeline
description: 推送当前分支并返回流水线跟踪 URL（GitLab 或 GitHub Actions）
argument-hint: "[--force | --draft]"
allowed-tools: [Bash]
model: haiku
effort: low
disable-model-invocation: true
---

# /ci:pipeline — 推送并触发流水线

推送当前分支并返回流水线跟踪链接。

## 流程

```bash
BRANCH=$(git branch --show-current)

# 1. 安全检查
if echo "$BRANCH" | grep -qE "^(main|master|production)$"; then
  echo "❌ 不允许直接推送到 $BRANCH。请创建 feature/fix 分支。"
  exit 1
fi

# 2. 检查未提交的更改
UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
  echo "⚠️  有 $UNCOMMITTED 个未提交的文件："
  git status --short
  echo ""
  echo "请先用 /commit 或 git add + git commit 提交"
  exit 0
fi

# 3. 推送
echo "推送中 → origin/$BRANCH"
git push origin "$BRANCH" 2>&1
```

## 流水线 URL

### GitLab CI

```bash
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
WEB_URL=$(echo "$REMOTE" | sed 's/git@gitlab\.com:/https:\/\/gitlab.com\//' | sed 's/\.git$//')
echo ""
echo "✅ 推送成功"
echo "   流水线：$WEB_URL/-/pipelines?ref=$BRANCH"

# 通过 glab 查看实时状态（如已安装）
if command -v glab &>/dev/null; then
  sleep 3
  glab ci status --branch "$BRANCH" 2>/dev/null || true
fi
```

### GitHub Actions

```bash
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
WEB_URL=$(echo "$REMOTE" | sed 's/git@github\.com:/https:\/\/github.com\//' | sed 's/\.git$//')
echo ""
echo "✅ 推送成功"
echo "   Actions：$WEB_URL/actions?query=branch%3A$BRANCH"

# 通过 gh 查看实时状态（如已安装）
if command -v gh &>/dev/null; then
  sleep 5
  gh run list --branch "$BRANCH" --limit 3 2>/dev/null || true
fi
```

## 预期输出

```
推送中 → origin/feat/add-payment-retry

Enumerating objects: 12, done.
...

✅ 推送成功
   流水线：https://gitlab.com/org/my-app/-/pipelines?ref=feat/add-payment-retry

流水线状态（3 秒后）：
  ⏳ lint       running
  ⏸️  test       waiting
  ⏸️  deploy     waiting
```

## 用法

```
/ci:pipeline
```

Target: $ARGUMENTS
