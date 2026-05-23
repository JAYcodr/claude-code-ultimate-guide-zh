---
name: scaffold
description: "交互式教练，通过 4-5 个问题确定你需要的是 agent、command、skill、hook 还是 rule——然后生成即用模板。用法：/scaffold（无参数——开始对话）"
effort: medium
disable-model-invocation: true
---

# Claude Code 搭建教练

交互式向导，为你的用例识别正确的 Claude Code 组件并生成即用模板。

**用法**：`/scaffold` — 无需参数。开始对话。

---

## 阶段 1 — 发现

以以下提示开始，等待用户回答后再询问其他内容：

> 你想自动化或构建什么？一句话就够了。

一旦有了大致概念，按顺序提出以下问题。如果前一个答案已回答某个问题则跳过。

### Q1 — 触发方式

> 这个如何触发？
>
> a) 我自己用命令运行（例如 `/something`）
> b) 当 Claude 执行某个操作时自动触发（写文件、运行 bash、结束会话……）
> c) 始终生效，每个会话都自动应用，我无需任何操作

- 如果 **b** → 可能是 **Hook** — 跳到 Q_hook
- 如果 **c** → 可能是 **Rule** — 跳到 Q_rule
- 如果 **a** → 继续 Q2

### Q2 — 领域专业知识

> 这需要深入的、项目特定的专业知识吗？
> 例如：了解你的 GraphQL schema、你的迁移约定、你的内部 API 模式、你的成本模型……

- 如果 **是，需要深入专业知识** → 可能是 **Agent** — 跳到 Q_agent
- 如果 **否，更像清单或步骤** → 继续 Q3

### Q3 — 复杂度

> 这涉及多少上下文和逻辑？
>
> a) 很多——多条规则、领域特定的示例、微妙的判断
> b) 直接——几个步骤、一个模板、一些 bash

- 如果 **a** → 可能是 **Skill**
- 如果 **b** → 可能是 **Command**

### Q4 — 复用范围

> 谁需要这个？
>
> a) 只有我
> b) 我整个团队
> c) 其他 agent 需要能自动调用它

- **c** → 加强为 **Agent**（需要有其他 agent 能读取的 `description:` 字段）
- **b** → 加强为 **Command** 或 **Skill**（共享配置）
- **a** → 可以作为简单的个人 **Command**

### Q5 — 输出类型

> 最终会发生什么？
>
> a) 报告或分析——Claude 读取并解释，不触碰文件
> b) 生成代码或文件
> c) 执行某个操作（commit、push、API 调用……）
> d) Claude 的行为永久改变（总是做 X、绝不做 Y）

- **a** → 只读 Agent（tools 中无 `Write` 或 `Bash`）
- **b/c** → 具有写权限的 Agent 或 Command/Skill
- **d** → Rule，或条件触发的 Hook

---

## 内部决策树（不显示——用于推理）

```
自动触发？
  ├─ Claude 操作时（Write、Bash、SessionEnd……）→ Hook
  └─ 始终活跃，无触发器 → Rule

手动触发？
  ├─ 需要深入领域专业知识？
  │   ├─ 是 + 其他 agent 可调用 → Agent
  │   └─ 是 + 仅手动使用 → Agent 或 Skill
  └─ 步骤/清单，无需特殊专业知识？
      ├─ 复杂、大量项目特定上下文 → Skill
      └─ 简单、只需几步 → Command

常见的混合情况：
  - Agent + Command → 专家 agent + 调用它的快捷命令
  - Rule + Hook → 永久行为 + 特定操作上的阻塞
  - Skill + Agent → 将分析委托给 agent 的技能
```

---

## 阶段 2 — 推荐

问题后，显示此结构：

```
## 诊断

你想实现：[一行总结用例]

## 推荐：[类型]

**为什么？**
[2-3 句：触发类型、复杂度级别、复用范围]

**它不是什么，以及为什么：**
- 不是 agent 因为 [简短理由]
- 不是 rule 因为 [简短理由]
[根据实际候选进行调整]

**混合情况？**[是 / 否]
[如果是：解释组合及先创建哪个文件]
```

---

## 阶段 3 — 搭建

询问："生成模板文件？"

如果同意，根据检测到的类型生成以下模板。

---

### Agent 模板

```markdown
---
name: [kebab-case-name]
description: "[此 agent 的作用一句话。何时调用。其他 agent 的触发示例。]"
model: sonnet
tools: Read, Grep, Glob[, Write, Bash — 仅当此 agent 必须修改文件或运行命令时添加]
---

# [Agent 名称]

[一段：此 agent 的用途、不是干什么的、以及何时应优先选择其他 agent。]

## 上下文

[此 agent 需要有效的技术栈、约定或领域知识。]

## 何时调用

- [具体触发条件 1]
- [具体触发条件 2]
- [具体触发条件 3]

## 协议

### 步骤 1 — 读取上下文

```bash
# 在推理前读取的内容
cat CLAUDE.md 2>/dev/null
```

### 步骤 2 — 分析

[要找什么。要检测的模式。要提出的红旗。]

### 步骤 3 — 输出

[确切的输出格式——用 markdown 代码块展示结构。]

## 红旗

| 模式 | 风险 |
|---------|------|
| [模式] | [影响] |

## 此 agent 不做的事

- [范围边界 1]
- [范围边界 2——如有相关指向其他 agent]
```

**文件**：`.claude/agents/[name].md`

---

### Command 模板

```markdown
---
name: [name]
description: "[此命令的作用一句话]"
argument-hint: "[arg] [--flag]"
---

# [命令名称]

[简要描述。解决什么问题。何时使用 vs 替代方案。]

## 参数

- `[arg]` — [描述]（默认：[值]）
- `--flag` — [描述]

## 用法

```bash
/[name]              # 基本用法
/[name] --flag       # 带标志
```

---

## 阶段 1 — [第一阶段名称]

[Claude 在此阶段做什么。]

```bash
# 适用的示例命令
```

## 阶段 2 — [第二阶段名称]

[Claude 做什么。]

## 阶段 3 — 输出

[输出格式。用 markdown 块展示结构。]

$ARGUMENTS
```

**文件**：`.claude/commands/[name].md`

---

### Skill 模板

```markdown
---
name: [skill-name]
description: "[此技能的作用。触发短语。用法：/[name] [arg]]"
---

# [技能名称]

[此技能的作用及何时适用。与类似技能区分。]

## 触发短语

- "[激活此技能的短语]"
- "[替代表述]"

## 何时使用

- [场景 1]
- [场景 2]

## 工作流

### 1. [第一个操作] — [简要描述]

[详情]

### 2. [第二个操作] — [简要描述]

[详情]

### 3. 交付输出

[输出格式]

## 要遵循的约定

[此技能必须遵守的项目特定规则、命名约定或模式。]

## 常见陷阱

- [错误 1 及如何避免]
- [错误 2 及如何避免]

$ARGUMENTS
```

**文件**：`.claude/skills/[name].md`

---

### Hook 模板

```bash
#!/usr/bin/env bash
# =============================================================================
# [name].sh — [PreToolUse | PostToolUse | UserPromptSubmit | Stop] Hook
# =============================================================================
# [此钩子做什么一行概括]
# 触发事件：[event] 匹配 [tool 或 pattern]
#
# Exit 0 = 允许 / 继续
# Exit 2 = 带消息阻止（仅 PreToolUse）
#
# stdin：来自 Claude Code 的 JSON payload
# =============================================================================

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# --- 主要逻辑 ---

# [你的验证逻辑在此处]
# 示例：阻止向保护路径写入
# FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
# if [[ "$FILE" == *"/secrets/"* ]]; then
#   echo "已阻止：不允许向 /secrets/ 写入" >&2
#   exit 2
# fi

exit 0
```

**文件**：`.claude/hooks/[name].sh`

还需添加到 `.claude/settings.json`：
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/[name].sh" }]
      }
    ]
  }
}
```

---

### Rule 模板

```markdown
# [规则标题]（自动加载）

## 指令

[一条祈使句形式的规则。]

## 何时适用

[触发条件、文件类型或此规则激活的场景。]

## 要求的行为

[Claude 必须具体做什么——请具体。]

## 反模式

❌ 不要：
- [禁止的示例]

✅ 要做：
- [正确行为]

---

**自动加载**：此文件在会话开始时自动加载。
```

**文件**：`.claude/rules/[name].md`

如果不在自动加载目录中，在 `CLAUDE.md` 中引用。

---

## 快速参考

如果用户不确定，展示此表格：

| 类型 | 触发方式 | 专业知识需求 | 复杂度 | 典型示例 |
|------|---------|-----------------|------------|-----------------|
| **Agent** | 手动或自动 | 高、领域特定 | 多步分析 | `migration-reviewer`、`dbt-specialist` |
| **Command** | 手动 `/name` | 低到中 | 简单、几个步骤 | `/commit`、`/pr`、`/release` |
| **Skill** | 手动 `/name` | 中到高 | 丰富的工作流、大量上下文 | `tdd-workflow`、`api-review` |
| **Hook** | 事件自动触发 | 无——bash 逻辑 | 脚本 | `security-gate.sh`、`format-on-save.sh` |
| **Rule** | 永久、每个会话 | 无——散文 | 指令 | `no-direct-push.md`、`english-only.md` |

---

## 来源

- 组件类型概览：[第 3 章节](../../guide/ultimate-guide.md)
- Agent 示例：[agents/](../agents/)
- Hook 示例：[hooks/](../hooks/)
- Skill 示例：[skills/](../skills/)
