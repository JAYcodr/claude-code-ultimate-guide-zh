---
name: autoresearch
description: 自主改进循环——扫描代码库指标、搭建实验文件、运行 agent 驱动的迭代直至指标改善
argument-hint: "[--scaffold <loop-name>] [--run <loop-name>] [--status]"
effort: high
disable-model-invocation: true
---

# 自主优化——自主改进循环

扫描代码库质量指标，提出改进循环，运行自主 agent 迭代。灵感来自 [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — 从 ML 研究适配到代码质量。

**概念**：agent 提出代码更改，运行测量，如果指标改善则保留更改，否则通过 `git reset` 还原，重复直到手动停止。

**时间**：扫描约 30 秒 | 每次迭代：取决于范围 | 循环：持续运行直到你停止

---

## 模式 1：扫描（默认）

测量当前状态，检测现有循环，提出下一步操作。

### 使用说明

运行以下指标并显示带优先级的建议表。

**步骤 1：测量代码库指标**

适配 grep 模式到你的项目约定。以下是 TypeScript 默认值——为你的栈调整。

```bash
# M1：函数声明（偏好箭头函数）
M1=$(grep -r "export function " src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M2：接口声明（偏好类型别名）
M2=$(grep -r "export interface " src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M3：ESLint 禁用
M3=$(grep -r "eslint-disable" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M4：类型转换为 any
M4=$(grep -r " as any" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M5：TODO 注释
M5=$(grep -r "// TODO" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')
```

**步骤 2：检测现有循环**

```bash
for dir in scripts/autoresearch/loop-*/; do
  [ -d "$dir" ] || continue
  LOOP_NAME=$(basename "$dir")
  # 检查循环是否有结果
  if [[ -f "$dir/results.tsv" ]]; then
    ITERS=$(wc -l < "$dir/results.tsv" | tr -d ' ')
    BEST=$(sort -t$'\t' -k2 -n "$dir/results.tsv" | head -1 | cut -f2)
    echo "ACTIVE:$LOOP_NAME:iterations=$ITERS:best=$BEST"
  else
    echo "SCAFFOLDED:$LOOP_NAME"
  fi
done
```

**步骤 3：显示**

```
自主优化扫描 — {日期}

代码库指标：

| # | 循环                | 指标            | 当前 | 目标 | 优先级 | 风险 |
|---|-------------------|-------------------|---------|--------|----------|------|
| A | loop-remove-as-any| `as any` 强制类型转换  | {M4}    | 0      | P1       | 低  |
| B | loop-eslint-disable| eslint-disable   | {M3}    | 0      | P2       | 中  |
| C | loop-export-fn    | export function   | {M1}    | 0      | P1       | 低  |
| D | loop-interface-type| export interface | {M2}    | 0      | P1       | 低  |
| E | loop-todo-comments| TODO 注释     | {M5}    | 0      | P3       | 低  |

现有循环：{检测到的循环或"暂无"}

建议的下一步（P1，低风险）：
  /autonomize --scaffold loop-remove-as-any
  然后编写 program.md，创建工作树，运行循环。
```

---

## 模式 2：`--scaffold <loop-name>`

生成循环的 3 个机械文件。**不生成 `program.md`**——你自己编写以编码项目特定的约束。

### 使用说明

在 `scripts/autoresearch/{loop-name}/` 下创建以下文件：

**`measure.sh`**——评估工具（单一指标，返回整数）：

```bash
#!/usr/bin/env bash
# measure.sh — {loop-name}
# 返回整数。方向：越小越好（除非目标是覆盖率/分数）。
set -euo pipefail
grep -r "模式" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' '
```

**`direction.txt`**——改进方向：

```
lower
```

（对于测试覆盖率或质量分数等指标，使用 `higher`。）

**`files.txt`**——agent 应操作的范围：

```
src/
```

创建文件后，显示：

```
循环已搭建：scripts/autoresearch/{loop-name}/

  measure.sh  : {模式} 在 {范围} 中 → 今日 {N} 处
  direction   : lower（越少越好）
  files.txt   : src/

当前指标：{N}（目标：0）

下一步：
  1. 编写 program.md — agent 行为、约束、能做什么不能做什么
     参考：scripts/autoresearch/loop-remove-as-any/program.md
  2. 创建工作树：/worktree feature/autoresearch-{loop-name}
  3. cd 进入工作树
  4. bash scripts/autoresearch/runner.sh {loop-name} 0 15
```

---

## 模式 3：`--run <loop-name>`

执行自主循环。agent 持续运行——满意时手动停止。

### 使用说明

**验证前置条件：**

```bash
[ -f "scripts/autoresearch/{loop-name}/measure.sh" ] || { echo "错误：缺少 measure.sh。先运行 --scaffold。"; exit 1; }
[ -f "scripts/autoresearch/{loop-name}/program.md" ] || { echo "错误：缺少 program.md。请先编写——它编码了你的约束。"; exit 1; }
```

**运行循环：**

开始前完整阅读 `scripts/autoresearch/{loop-name}/program.md`。然后进入以下循环——重复直到停止：

```
循环迭代 #{N}

1. 当前指标：bash scripts/autoresearch/{loop-name}/measure.sh
2. 读取 program.md 约束
3. 对 files.txt 中的文件提出一个有针对性的更改
4. 应用更改
5. 重新测量：bash scripts/autoresearch/{loop-name}/measure.sh
6. 评估：
   - direction=lower 且 new < previous → 保留（git add -p && git commit -m "autonomize：{描述}"）
   - 否则 → 还原（git checkout -- .）
7. 记录到 results.tsv：{时间戳}\t{指标}\t{状态}\t{描述}
8. 继续迭代 #{N+1}
```

**停止标准**（来自 program.md）：
- 指标达到目标（例如 0）
- 没有更多机械更改可用
- 用户手动停止

**显示每次迭代：**

```
[迭代 #{N}] 指标：{之前} → {之后} | {保留/还原} | {更改描述}
```

---

## 模式 4：`--status`

显示项目中所有循环的状态。

### 使用说明

```bash
for dir in scripts/autoresearch/loop-*/; do
  [ -d "$dir" ] || continue
  NAME=$(basename "$dir")
  CURRENT=$(bash "$dir/measure.sh" 2>/dev/null || echo "?")
  ITERS=$([ -f "$dir/results.tsv" ] && wc -l < "$dir/results.tsv" | tr -d ' ' || echo "0")
  KEPT=$([ -f "$dir/results.tsv" ] && grep -c "KEPT" "$dir/results.tsv" || echo "0")
  echo "$NAME | current：$CURRENT | iters：$ITERS | kept：$KEPT"
done
```

显示：

```
自主优化状态

| 循环                | 当前 | 迭代次数 | 保留次数 | 状态       |
|---------------------|---------|------------|------|-----------|
| loop-remove-as-any  | {N}     | {N}        | {N}  | 活动      |
| loop-export-fn      | {N}     | 0          | 0    | 已搭建    |
```

---

## 编写 `program.md`——最重要的文件

`program.md` 是 agent 的行为契约。请自己编写——切勿自动生成。它必须针对你的特定代码库编码 agent 能做什么不能做什么。

**最小结构：**

```markdown
# 程序：{loop-name}

## 目标
将 `{指标}` 在 `src/` 中减少到 0。每次迭代做一个机械更改。

## 测量
bash scripts/autoresearch/{loop-name}/measure.sh
越小越好。目标：0。

## 你可以做的
- 将 `export function X(` 替换为 `export const X = (`
- 保持函数签名完全相同

## 你不能做的
- 修改测试文件
- 更改函数签名
- 触碰 src/ 以外的文件
- 每次迭代做多个更改

## 何时停止
- 指标 = 0
- 没有更多机械替换可做
```

---

## 模式（背景）

此命令实现了来自 [karpathy/autoresearch](https://github.com/karpathy/autoresearch) 的 **autoresearch loop** 模式：

| ML 研究（karpathy） | 代码质量（此命令） |
|------------------------|----------------------------|
| 修改 `train.py` | 修改 `src/` 文件 |
| 测量 `val_bpb` | 测量 grep 计数 |
| 5 分钟 GPU 预算 | 每次迭代一个原子更改 |
| 如果 val_bpb 改善则保留 | 如果计数减少则保留 |
| 否则 `git reset` | 否则 `git checkout -- .` |
| `program.md` = agent 技能 | `program.md` = agent 技能 |

关键洞见：固定的客观指标 + git 作为回滚机制 = 安全的自主迭代。agent 永远不需要人类每更改一次就批准，因为每次不好的更改都会自动还原。

---

## 用法

**扫描并提出循环：**
```
/autonomize
```

**为特定循环搭建文件：**
```
/autonomize --scaffold loop-remove-as-any
```

**运行自主循环（编写 program.md 后）：**
```
/autonomize --run loop-remove-as-any
```

**检查所有循环状态：**
```
/autonomize --status
```

$ARGUMENTS
