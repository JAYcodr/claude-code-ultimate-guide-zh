---
name: pr
description: 分析更改、检测范围问题并创建结构良好的 PR
argument-hint: "[--base <branch>] [--draft]"
effort: medium
disable-model-invocation: true
---

# 创建 Pull Request

分析更改、检测范围问题并创建符合项目约定的结构良好的 PR。

## 流程

1. **分析更改**：根据文件、提交和目录计算复杂度评分
2. **检测范围问题**：如果 PR 过大或混合了不相关的更改则发出警告
3. **建议拆分**：如需要，按范围分组提交并提出单独的 PR
4. **收集信息**：询问类型、目标分支、草稿状态、标签
5. **生成内容**：创建 TLDR + 描述 + 清单
6. **创建 PR**：执行 `gh pr create` 并正确格式化
7. **提醒跟进**：显示 PR 后清单（SonarQube、Claude Review）

## 复杂度评分

计算 PR 复杂度以检测是否需要拆分：

| 标准 | 权重 | 描述 |
|-----------|--------|-------------|
| 代码文件 | x2 | `*.ts, *.tsx`（不含测试） |
| 测试文件 | x0.5 | `*.test.ts, *.spec.ts` |
| 配置文件 | x1 | `*.json, *.yml, *.md` |
| 目录数 | x3 | 不同的 `src/*` 目录 |
| 提交数 | x1 | 提交数量 |

**阈值**：0-15 ✅ 正常 | 16-25 ⚠️ 较大 | 26+ 🔴 建议拆分

## 范围一致性

| 模式 | 裁决 |
|---------|---------|
| 单一范围 | ✅ 正常 |
| 相关范围（sessions + calendar） | ✅ 正常 |
| 不相关范围（payments + auth） | 🔴 拆分 |
| feat + fix 同一范围 | ✅ 正常 |
| feat + fix 不同范围 | 🔴 拆分 |

## 拆分建议格式

建议拆分时显示：

```
🔴 范围过大（评分：32）

按范围分组提交：
├── payments（5 个提交，8 个文件）
│   ├── feat(payments): add Stripe checkout
│   └── fix(payments): handle currency
│
└── notifications（3 个提交，6 个文件）
    └── feat(notifications): add email templates

💡 建议：
1. PR #1：feature/payments-stripe → payments 提交
2. PR #2：feature/notifications → notifications 提交

选项：
[A] 继续用一个 PR（不推荐）
[B] 拆分（半自动——提供 git 命令）
[C] 查看文件详情
```

**半自动拆分**提供复制粘贴命令：
```bash
git checkout develop
git checkout -b feature/payments-stripe
git cherry-pick abc1234 def5678
git push -u origin feature/payments-stripe
```

## 要问的问题

1. **类型**：feature | fix | tech | docs | security
2. **目标分支**：显示最近分支（develop、main 等）
3. **草稿**：是（WIP）| 否（准备审查）
4. **标签**：基于类型 + 可选（breaking-change、security）

## PR 标题格式

```
<类型>(<范围>): <描述>
```

示例：
- `feat(payments): add Stripe checkout integration`
- `fix(sessions): resolve timezone calculation bug`

## PR 主体模板

```markdown
## TLDR
<!-- 最多 2 行 - 执行摘要 -->

---

## 类型
{功能 | 修复 | 技术 | 文档 | 安全}

## 描述
{上下文和改动}

## 技术改动
{主要修改清单}

## 测试
- [ ] 单元测试已添加/通过
- [ ] 手动测试已完成

## 清单
- [ ] 代码遵循约定
- [ ] 没有遗留的 console.log
- [ ] 类型正确（`pnpm typecheck`）

---

🤖 由 [Claude Code](https://claude.com/claude-code) 生成

Co-Authored-By: Claude <noreply@anthropic.com>
```

## 可用标签

| 标签 | 颜色 | 何时使用 |
|-------|-------|----------|
| `feature` | 🟢 | 新功能 |
| `fix` | 🔴 | Bug 修复 |
| `tech` | 🔵 | 重构、技术债务 |
| `docs` | 📘 | 仅文档 |
| `security` | 🟣 | 安全修复 |
| `breaking-change` | ⚫ | 破坏性更改 |
| `WIP` | 🟡 | 进行中（草稿） |

## 要执行的命令

```bash
# 1. 获取基分支（通常是 develop）
BASE_BRANCH="develop"

# 2. 计算复杂度评分
CODE=$(git diff --name-only $BASE_BRANCH..HEAD | grep -E '\.(ts|tsx)$' | grep -v test | wc -l)
TESTS=$(git diff --name-only $BASE_BRANCH..HEAD | grep -E '\.test\.|\.spec\.' | wc -l)
DIRS=$(git diff --name-only $BASE_BRANCH..HEAD | cut -d'/' -f1-2 | sort -u | wc -l)
COMMITS=$(git rev-list --count $BASE_BRANCH..HEAD)
SCORE=$((CODE * 2 + TESTS / 2 + DIRS * 3 + COMMITS))

# 3. 从提交中获取范围
git log --oneline $BASE_BRANCH..HEAD --format="%s" | sed -n 's/^\w*(\([^)]*\))).*/\1/p' | sort | uniq -c

# 4. 供选择的最近分支
git branch --sort=-committerdate --format='%(refname:short)' | head -5

# 5. 创建 PR
gh pr create \
  --title "<类型>(<范围>): <描述>" \
  --body "$BODY" \
  --base $BASE_BRANCH \
  --label "<标签>" \
  --draft  # 如果是 WIP
```

## PR 后输出

创建 PR 后，始终显示：

```
✅ PR 已创建：https://github.com/org/repo/pull/XXX

📋 后续自动步骤：
   • SonarQube 将分析代码质量（bug、漏洞、代码异味）
   • Claude Code Review 将提供 AI 反馈

⏳ 请注意在接下来几分钟内关注这些分析。
   如果检测到问题，在请求人工审查前修复它们。
```

## 边缘用例

| 情况 | 行为 |
|-----------|----------|
| 提交中无范围 | 按目录分析 |
| 非 Conventional Commit | 警告 + 手动询问类型 |
| 无提交（与基分支相同） | 错误："无更改" |
| 单个提交 | 使用提交消息作为标题 |
| Merge 提交 | 忽略（`--no-merges`） |

## 用法

```
/pr
/pr --base main
/pr --draft
```

Target：$ARGUMENTS（可选：--base、--draft）
