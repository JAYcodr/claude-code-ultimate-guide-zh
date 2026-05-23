---
name: ci-all
description: "完整 CI 流程：在本地运行测试、类型检查、推送分支，并返回流水线 URL。打开 PR 前所需的唯一命令。"
argument-hint: "[--skip-tests | --e2e]"
allowed-tools: [Bash]
model: haiku
effort: medium
disable-model-invocation: true
---

# /ci:all — PR 前的完整 CI

按顺序执行所有步骤：本地测试 → 类型检查 → 推送 → 流水线 URL。

一条 `/ci:all` 替代：手动测试 + git push + 复制流水线 URL。

## 栈检测

```bash
if [ -f "uv.lock" ]; then STACK="python"
elif [ -f "pnpm-lock.yaml" ]; then STACK="node"
elif [ -f "package-lock.json" ]; then STACK="node-npm"
elif [ -f "Cargo.toml" ]; then STACK="rust"
fi
```

## 步骤 1 — 本地测试（阻塞）

**Python（uv/pytest）：**
```bash
uv run pytest --tb=short -q
# 失败 → 停止并打印失败测试
```

**Node（pnpm/vitest）：**
```bash
pnpm vitest run
pnpm tsc --noEmit
# 失败 → 停止
```

**Rust：**
```bash
cargo test --quiet 2>&1
```

如果传入 `--skip-tests` → 跳到步骤 2。

## 步骤 2 — 推送 + 流水线

```bash
BRANCH=$(git branch --show-current)

# 检查是否有待推送的提交
AHEAD=$(git rev-list --count origin/$BRANCH..HEAD 2>/dev/null || echo "1")
if [ "$AHEAD" = "0" ]; then
  echo "分支已在 origin 上为最新。"
else
  git push origin "$BRANCH"
fi
```

## 步骤 3 — 流水线 URL

### GitLab CI

```bash
REMOTE=$(git remote get-url origin)
WEB_URL=$(echo "$REMOTE" | sed 's/git@gitlab\.com:/https:\/\/gitlab.com\//' | sed 's/\.git$//')
echo "流水线：$WEB_URL/-/pipelines?ref=$BRANCH"

# 可选：通过 glab CLI 查看实时状态
if command -v glab &>/dev/null; then
  sleep 3
  glab ci status --branch "$BRANCH" 2>/dev/null || true
fi
```

### GitHub Actions

```bash
REMOTE=$(git remote get-url origin)
WEB_URL=$(echo "$REMOTE" | sed 's/git@github\.com:/https:\/\/github.com\//' | sed 's/\.git$//')
echo "Actions：$WEB_URL/actions?query=branch%3A$BRANCH"

# 可选：通过 gh CLI 查看实时状态
if command -v gh &>/dev/null; then
  sleep 5
  gh run list --branch "$BRANCH" --limit 3 2>/dev/null || true
fi
```

## 预期输出

```
CI — my-app (Node/Vitest)
──────────────────────────

① 本地测试
  ✅ 47 passed in 8.2s

② 类型检查
  ✅ 无错误

③ 推送
  ✅ origin/feat/my-feature

④ 流水线
  🔗 https://gitlab.com/org/my-app/-/pipelines?ref=feat/my-feature

下一步：用 /pr 或在 GitLab/GitHub 上打开 PR。
```

测试失败时：
```
CI — my-api (Python/pytest)
────────────────────────────

① 本地测试
  ❌ 2 个失败

  FAILED tests/test_orders.py::TestOrderService::test_refund_validation
  AssertionError: expected 400, got 500

→ 修复测试后再推送。流水线未触发。
```

## 用法

```
/ci:all
/ci:all --skip-tests    # 不重新运行测试直接推送
/ci:all --e2e           # 包含 E2E 测试（如已配置）
```

Target: $ARGUMENTS
