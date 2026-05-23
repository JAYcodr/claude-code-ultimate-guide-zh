<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "使用 Claude Code 进行 TDD"
description: "红-绿-重构循环的显式提示测试驱动开发工作流"
tags: [workflow, tdd, testing]
---

# 使用 Claude Code 进行 TDD

> **可信度**：第 1 层 — 基于官方 Anthropic 最佳实践和广泛的社区验证。

使用 Claude 进行测试驱动开发需要显式提示。Claude 自然先写实现代码，后写测试。TDD 要求相反。

---

## 目录

1. [TL;DR](#tldr)
2. [问题](#问题)
3. [设置](#设置)
4. [红-绿-重构循环](#红-绿-重构循环)
5. [与 Claude Code 功能集成](#与-claude-code-功能集成)
6. [反模式](#反模式)
7. [高级模式](#高级模式)
8. [另见](#另见)

---

## TL;DR

```
Red → Green → Refactor

但你必须显式提示 Claude：
"为 [功能] 写一个会失败的测试。还不要写实现。"
```

---

## 问题

没有显式指令，Claude 会：
1. 写实现代码
2. 然后写针对该实现通过的测试

这违背了 TDD 的目的：测试应该驱动设计，而不是验证现有代码。

---

## 设置

### CLAUDE.md 配置

添加到项目的 CLAUDE.md：

```markdown
## 测试约定

### TDD 工作流
- 始终在实现之前写失败的测试
- 使用 AAA 模式：Arrange-Act-Assert
- 可能时每个测试一个断言
- 测试名称描述行为："should_return_empty_when_no_items"

### 测试优先规则
- 当我要求一个功能时，先写测试
- 测试最初应该失败（不存在实现）
- 只有在测试写完后，实现最小代码使其通过
```

### 自动运行测试的钩子（可选）

创建 `.claude/hooks/test-on-save.sh`：

```bash
#!/bin/bash
# Auto-run tests when test files change
if [[ "$1" == *test* ]] || [[ "$1" == *spec* ]]; then
  npm test --watchAll=false 2>&1 | head -20
fi
```

---

## 红-绿-重构循环

### 阶段 1：红（写会失败的测试）

**提示词**：
```
为 [功能描述] 写一个会失败的测试。
还不要写实现。
测试应该因为函数/方法不存在而失败。
```

**示例**：
```
为计算购物车中商品总价的函数写一个会失败的测试，
如果有 $100 以上，应用 10% 折扣。
还不要实现这个函数。
```

**预期的 Claude 行为**：
- 创建测试文件及测试用例
- 测试引用不存在的函数
- 运行测试会失败，显示"function not defined"或类似错误

**验证**：
```bash
npm test  # 应该失败并显示 "calculateCartTotal is not defined"
```

### 阶段 2：绿（最小实现）

**提示词**：
```
现在实现最小代码使这些测试通过。
只写通过当前测试所需的代码，不要更多。
```

**预期的 Claude 行为**：
- 创建实现文件
- 写最小代码满足测试
- 避免过度工程

**验证**：
```bash
npm test  # 应该通过
```

### 阶段 3：重构（清理）

**提示词**：
```
重构实现以提高代码质量。
测试必须在重构后保持绿色。
专注于：[可读性 / 性能 / 消除重复]
```

**预期的 Claude 行为**：
- 改进代码而不改变行为
- 运行测试验证仍然通过
- 记录任何重大变更

---

## 与 Claude Code 功能集成

### 使用 TodoWrite

在任务列表中跟踪 TDD 阶段：

```
用户："用 TDD 实现用户认证"

Claude 创建待办事项：
- [ ] RED：为登录写会失败的测试
- [ ] GREEN：实现登录以通过测试
- [ ] REFACTOR：清理登录实现
- [ ] RED：为登出写会失败的测试
- [ ] GREEN：实现登出
- [ ] REFACTOR：清理
```

### 使用计划模式

用于测试策略的计划：

```
[按 Shift+Tab 进入计划模式]

我需要用 TDD 实现购物车。
在开始写任何代码之前计划测试用例。
```

Claude 将在只读模式下探索代码库，然后在写任何实现之前提出测试计划。

### 使用钩子

使用 PostToolUse 钩子在编辑后自动运行测试：

```json
// In .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npm test --watchAll=false 2>&1 | head -20"
      }
    ]
  }
}
```

### 使用子智能体

将测试编写委托给范围聚焦的智能体：

```
使用 test-writer 智能体为 UserService 类创建全面测试，
覆盖所有边缘情况。
然后我来实现以通过这些测试。
```

---

## 反模式

### 验证缺口

验证缺口是智能体在验证套件确认之前报告功能完成的失败模式。这是多会话智能体工作中最常见的可靠性失败，完全可以用正确的工具设计防止。

三个可观察症状：智能体在任何测试命令运行之前打印成功消息；测试运行但 stderr 被丢弃或未读取；只有单元测试通过而验收标准指定了端到端行为。

修复是一个三层验证堆栈，任何功能在特征列表中标记为 `passing` 之前必须全部通过：

1. **Lint** — 语法和风格检查（最快，在运行测试前捕获明显错误）
2. **单元和集成测试** — 各个组件的功能正确性
3. **端到端测试** — 用户或外部调用者看到的 behavioral contract

每层捕获不同类别的失败。单元测试通过时组件边界可能破坏。端到端测试暴露单元测试看不到的状态传播错误和生命周期问题。跳过任何层都会留下缺口。

独立评估器原则：写代码的智能体不能是与确认完成相同的调用。这不是对模型的不信任；这是关于上下文如何影响评估。刚花两小时构建功能的智能体会 charitable 地解释模糊输出。PostToolUse 钩子或读取退出代码的第二个智能体不会。`examples/hooks/bash/verification-gate.sh` 中的钩子实现了这个模式。

Anthropic 在他们的工具设计研究中记录了这个失败：裸运行（无工具）时，他们的智能体在 20 分钟后报告游戏编辑器完成。什么都不能用。添加独立评估器到工具后，相同模型运行 6 小时并交付可用结果。（来源：[https://www.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)）

WIP=1 规则与此相关：保持只有一个功能 `active` 意味着验证缺口（如果发生）影响一个功能，而非同时影响多个。

### 不要做什么

| 反模式 | 为什么错误 | 正确方式 |
|--------------|----------------|------------------|
| "为这个功能写测试" | Claude 先实现 | "写还不存在的会失败的测试" |
| "添加测试和实现" | 失去测试优先好处 | 分成两个提示词 |
| "确保测试通过" | 鼓励先实现 | "先写测试，然后最小实现" |
| 跳过重构阶段 | 技术债务积累 | 绿色后始终重构 |
| 同时多功能 | 失去专注 | 每个 TDD 循环一个功能 |

### 常见错误

**错误**：让 Claude "测试"现有代码。
```
# 错误
"为现有的 calculateTotal 函数写测试"

# 正确
"为 calculateTotal 行为写测试，假设函数不存在。
然后验证现有实现通过。"
```

**错误**：合并红绿阶段。
```
# 错误
"用测试实现 calculateTotal"

# 正确
"为 calculateTotal 写会失败的测试。停在那里。"
[测试写完后]
"现在实现以通过那些测试。"
```

---

## 高级模式

### 属性测试

```
为 sort 函数写属性测试。
要测试的属性：
- 输出长度等于输入长度
- 所有输入元素存在于输出
- 输出有序
使用 fast-check 或类似库。
```

### 变异测试

```
测试通过后，运行变异测试以找到弱点。
识别不能捕获变异的测试。
```

> **进一步**：JiTTesting 在 PR 时自动应用变异测试——LLM 生成，临时，无需维护。Meta 在规模上部署了这一点，相比传统测试改进了 4 倍回归捕获。见 [Just-in-Time Catching Test Generation at Meta](https://arxiv.org/abs/2601.22832) 和[方法论指南](../core/methodologies.md#jittesting-just-in-time-testing)，了解今天用 Claude Code 的近似模式。

### 遗留代码的 TDD

```
我需要重构 legacyFunction。
首先，写表征测试以捕获当前行为。
然后我们有信心地重构。
```

---

## 示例会话

### 用户请求
```
用 TDD 实现 URL 缩短服务。
```

### 阶段 1：红
```
让我们用 TDD。首先，为以下写会失败的测试：
1. 缩短 URL 返回短码
2. 检索短码返回原始 URL
3. 无效 URL 被拒绝
4. 过期链接返回错误

还不要实现任何东西。
```

### 阶段 2：绿
```
测试已写完并失败。现在实现最小代码使它们通过。
暂时用内存存储。
```

### 阶段 3：重构
```
测试通过。现在重构：
- 将 URL 验证提取到单独函数
- 添加适当的错误类型
- 改进变量名

每次变更后运行测试确保它们保持绿色。
```

---

## 另见

- [../core/methodologies.md](../core/methodologies.md) — 完整方法论参考
- [紧密反馈循环](../ultimate-guide.md) — 第 9.5 节
- [examples/skills/tdd-workflow.md](../../examples/skills/tdd-workflow.md) — TDD 技能模板
- [Anthropic 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices)
- [task-management.md](./task-management.md) — 使用 Tasks API 跨会话跟踪 TDD 循环
- [Superpowers](https://github.com/obra/superpowers) — 强制 TDD 作为必选门禁的插件套件：在失败的测试存在之前写的代码被删除并从零重做。比手动提示更严格的强制。