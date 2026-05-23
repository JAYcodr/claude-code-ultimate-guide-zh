---
name: plan-pipeline
description: "编排完整的计划流水线：产品方向（ceo-review）→ 架构（eng-review）→ 实现计划（start）→ 验证（validate）→ 执行（execute）。可单独运行各阶段，也可让编排器协调完整流程。"
allowed-tools: "Read, Write, Bash, Task"
effort: high
---

# 计划流水线编排器

编排从计划到执行的完整流水线。可运行完整流水线或单个独立阶段。

## 阶段

| 阶段 | 技能 | 目的 |
|-------|-------|---------|
| 1 | `/plan-pipeline:ceo-review` | 质疑任务简报，锁定产品方向 |
| 2 | `/plan-pipeline:eng-review` | 锁定架构、图表和测试矩阵 |
| 3 | `/plan-pipeline:start` | 5 阶段计划：PRD、调研、ADR、任务清单 |
| 4 | `/plan-pipeline:validate` | 编写任何代码前的 2 层验证 |
| 5 | `/plan-pipeline:execute` | 工作树隔离、并行 agent、质量门、PR |

## 用法

```
/plan-pipeline                     # 完整流水线，询问上下文
/plan-pipeline --from=start        # 跳过门禁，从计划阶段开始
/plan-pipeline --from=validate     # 验证现有计划
/plan-pipeline --from=execute      # 执行已验证的计划
```

## 何时使用各阶段

**ceo-review** — 在方向未锁定的重大功能前使用。当需求具体时尤其有价值（具体性通常意味着压缩了解决方案空间）。

**eng-review** — 方向锁定后使用。涉及异步组件、外部依赖或多步流程的功能必需此阶段。

**start** — 涉及超过 2 个文件或包含架构决策的非平凡功能使用。

**validate** — 执行前始终执行。验证的成本与执行中才发现问题的成本相比微不足道。

**execute** — 验证确认所有问题已解决后执行。

## 工作流

1. **收集上下文** — 我们在构建什么，从哪个阶段开始？
2. **ceo-review** — 产品方向门禁（可用 `--from=eng-review` 或更后阶段跳过）
3. **eng-review** — 架构门禁（可用 `--from=start` 或更后阶段跳过）
4. **检查点** — 在计划前询问用户确认方向和架构
5. **start** — 运行 5 阶段计划，生成 `docs/plans/plan-{name}.md`
6. **检查点** — 在验证前呈现计划供审查
7. **validate** — 2 层验证（结构 + 专长 agent）
8. **execute** — 工作树隔离 → 并行 agent → 质量门 → PR

## 依赖图

```
   ceo-review
        |
   eng-review
        |
      start
        |
    validate
        |
    execute
```

## 说明

每个阶段将其输出写入磁盘后下一阶段开始。如果流水线被中断，使用 `--from=<阶段>` 并使用正确的阶段名恢复。所有决策记录在 `docs/plans/plan-{name}.md` 和 `docs/adr/` 下的对应 ADR 中。
