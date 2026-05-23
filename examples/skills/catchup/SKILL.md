---
name: catchup
description: 通过总结近期工作和项目状态，在 /clear 后恢复上下文
argument-hint: "[branch] [--since <date>]"
effort: low
disable-model-invocation: true
---

# 上下文恢复

在 `/clear` 后恢复上下文 — 总结近期工作和项目状态。

## 目的

使用 `/clear` 清除上下文后，用此命令快速重建对以下内容的了解：
- 最近修改了什么
- 当前项目状态
- 未完成的 TODO 和问题
- 从哪里继续工作

## 使用说明

### 步骤 1：Git 历史分析

```bash
# 最近提交（最后 10 条）
git log --oneline -10

# 最后 5 次提交中修改的文件
git diff --stat HEAD~5 2>/dev/null || git diff --stat $(git rev-list --max-parents=0 HEAD)

# 当前分支和状态
git branch --show-current
git status --short
```

### 步骤 2：近期更改总结

```bash
# 今天的更改
git log --oneline --since="midnight" --author="$(git config user.name)" 2>/dev/null

# 未提交的工作
git diff --name-only
git diff --cached --name-only
```

### 步骤 3：TODO/FIXME 扫描

```bash
# 查找最近修改文件中的待办标记
git diff --name-only HEAD~5 2>/dev/null | head -20 | xargs grep -n "TODO\|FIXME\|XXX\|HACK" 2>/dev/null | head -30
```

### 步骤 4：项目状态检查

```bash
# 检查常用状态指示器
[ -f "package.json" ] && echo "📦 Node 项目：$(jq -r '.name // "unnamed"' package.json)"
[ -f "Cargo.toml" ] && echo "🦀 Rust 项目：$(grep '^name' Cargo.toml | head -1)"
[ -f "pyproject.toml" ] && echo "🐍 Python 项目"
[ -f "go.mod" ] && echo "🐹 Go 项目：$(head -1 go.mod | cut -d' ' -f2)"

# 活跃分支用途（从分支名推断）
BRANCH=$(git branch --show-current)
echo "🌿 分支：$BRANCH"
```

## 输出格式

提供结构化的摘要：

---

### 📍 上下文已恢复

**项目**：[来自 package.json/Cargo.toml 等的项目名]
**分支**：[当前分支]
**最近活动**：[最后提交时间]

### 🔄 近期工作（最后 5 次提交）

1. [提交信息 1] - [涉及的文件]
2. [提交信息 2] - [涉及的文件]
...

### 📝 未提交的更改

- [修改文件列表及简要说明]

### ⚠️ 未完成的 TODO

- [文件:行] TODO：[描述]
- [文件:行] FIXME：[描述]

### 🎯 建议的下一步

基于近期活动：
1. [根据模式推断的最可能下一步]
2. [备选关注方向]

---

## 使用示例

**长时间中断后：**
```
/catchup
```
→ 完整的上下文恢复

**快速状态检查：**
```
/catchup --brief
```
→ 仅提交和未提交的更改

**关注特定领域：**
```
/catchup auth
```
→ 仅筛选与 auth 相关的更改

## 提示

1. **在 `/clear` 前记录**：在清除上下文前，在提交信息或 CLAUDE.md 中写一条简短笔记
2. **与 Memory Bank 结合**：配合 `.claude/memory/` 文件实现持久状态
3. **分支命名**：使用描述性分支名（如 `feat/user-auth`）帮助上下文恢复

$ARGUMENTS
