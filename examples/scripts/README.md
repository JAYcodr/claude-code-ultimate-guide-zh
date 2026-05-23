---
title: "脚本"
description: "Claude Code 高级用户实用脚本：审计、健康检查和会话管理"
tags: [template, debugging, security, workflows]
---

# 脚本

面向 Claude Code 高级用户的实用脚本。

## 概览

| 脚本                             | 说明                                                       |
| -------------------------------- | ---------------------------------------------------------- |
| `pptx-to-pdf.sh`                 | 在 macOS 上通过 Keynote 批量转换 PPTX 为 PDF（无额外依赖） |
| `audit-scan.sh`                  | Claude Code 设置的安全与质量审计                           |
| `check-claude.sh/.ps1`           | Claude Code 安装的健康检查                                 |
| `clean-reinstall-claude.sh/.ps1` | Claude Code 的干净重装                                     |
| `fresh-context-loop.sh`          | 在全新上下文循环中运行 Claude Code                         |
| `session-search.sh`              | 跨 Claude Code 会话历史搜索                                |
| `cc-sessions.py`                 | 进阶会话搜索，支持增量索引（Python）                       |
| `session-stats.sh`               | Claude Code 会话统计信息                                   |
| `bridge.py`                      | 桥接：Claude Code → doobidoo → LM Studio                   |
| `bridge-plan-schema.json`        | bridge plan v1 格式的 JSON Schema                          |
| `migrate-arguments-syntax.sh`    | 迁移 v1 → v2 斜杠命令参数语法（Bash）                      |
| `migrate-arguments-syntax.ps1`   | 迁移 v1 → v2 斜杠命令参数语法（PowerShell）                |
| `rtk-benchmark.sh`               | 基准对比 RTK token 节省 vs 原始命令                        |
| `sync-claude-config.sh`          | 跨机器同步 Claude 配置文件                                 |
| `sonnetplan.sh`                  | 用 Sonnet 替代 Opus 运行 Claude（成本优化别名）            |
| `test-prompt-caching.ts`         | 验证 Anthropic 提示词缓存是否激活（无依赖，仅用 fetch）    |
| `smart-suggest-roi.py`           | 分析 smart-suggest 钩子建议采纳率 vs 会话活动              |

---

## Bridge 脚本（Claude Code → LM Studio）

**用途**：通过 LM Studio 在本地执行 Claude Code 计划，节省成本。

### 架构

```
┌──────────────┐     store_memory      ┌─────────────────┐
│ Claude Code  │ ─────────────────────►│    doobidoo     │
│   (Opus)     │   tag: "plan"         │   SQLite + Vec  │
│   计划者     │   status: "pending"   │ ~/.mcp-memory-  │
└──────────────┘                       │  service/       │
                                       └────────┬────────┘
                                                │
                                                │ 直接 SQLite 读取
                                                ▼
                                       ┌─────────────────┐
                                       │   bridge.py     │
                                       │                 │
                                       │ • PlanReader    │
                                       │ • StepExecutor  │
                                       │ • Validator     │
                                       └────────┬────────┘
                                                │
                                                │ HTTP POST
                                                │ /v1/chat/completions
                                                ▼
                                       ┌─────────────────┐
                                       │    LM Studio    │
                                       │  localhost:1234 │
                                       └─────────────────┘
```

### 依赖

```bash
pip install httpx
```

- **doobidoo MCP 服务器**，SQLite 后端（`~/.mcp-memory-service/`）
- **LM Studio** 在 `localhost:1234` 运行，且已加载模型

### 用法

```bash
# 检查 LM Studio 是否运行
python bridge.py --health

# 列出待执行计划
python bridge.py --list

# 执行所有待执行计划
python bridge.py

# 执行特定计划
python bridge.py --plan plan_auth_refactor

# 详细模式
python bridge.py -v
```

### 工作流

#### 1. Claude Code 创建计划

在 Claude Code（Opus）中，通过 doobidoo 存储计划：

```
store_memory("""
{
  "$schema": "bridge-plan-v1",
  "id": "plan_auth_refactor",
  "status": "pending",
  "context": {
    "project": "/path/to/project",
    "objective": "Refactor authentication to use JWT",
    "files_context": {
      "src/auth.py": "LOAD",
      "src/config.py": "REFERENCE"
    }
  },
  "steps": [
    {
      "id": 1,
      "type": "analysis",
      "description": "Analyze current auth implementation",
      "prompt": "Analyze the authentication code and identify migration points for JWT.",
      "validation": {"type": "non_empty"}
    },
    {
      "id": 2,
      "type": "code_generation",
      "description": "Generate JWT middleware",
      "prompt": "Generate a JWT authentication middleware based on the analysis.",
      "depends_on": [1],
      "validation": {"type": "syntax_check"},
      "file_output": "src/jwt_auth.py"
    }
  ]
}
""", tags=["plan"])
```

#### 2. 通过 bridge 执行

```bash
python bridge.py
# 从 doobidoo SQLite 读取计划
# 通过 LM Studio 执行每个步骤
# 将结果存回 doobidoo
```

#### 3. 在 Claude Code 中获取结果

```
search_by_tag(["result", "plan_auth_refactor"])
# 返回所有执行结果
```

### 计划 Schema

完整 JSON Schema 见 `bridge-plan-schema.json`。

| 字段                    | 必填 | 说明                                            |
| ----------------------- | ---- | ----------------------------------------------- |
| `$schema`               | 是   | 必须为 `"bridge-plan-v1"`                       |
| `id`                    | 是   | 唯一计划 ID（如 `plan_auth_refactor`）          |
| `status`                | 是   | `pending`、`in_progress`、`completed`、`failed` |
| `context.objective`     | 是   | 高层次目标描述                                  |
| `context.project`       | 否   | 项目根目录的绝对路径                            |
| `context.files_context` | 否   | 注入（`LOAD`）或引用的文件                      |
| `steps`                 | 是   | 执行步骤数组                                    |

### 步骤类型

| 类型                | 用例                         |
| ------------------- | ---------------------------- |
| `analysis`          | 分析代码、识别模式、规划变更 |
| `code_generation`   | 从零生成新代码               |
| `code_modification` | 修改已有代码                 |
| `decision`          | 做出架构或设计决策           |

### 验证类型

| 类型            | 说明             |
| --------------- | ---------------- |
| `non_empty`     | 输出非空（默认） |
| `json`          | 有效 JSON 输出   |
| `syntax_check`  | 有效 Python 语法 |
| `contains_keys` | JSON 包含特定键  |

### 失败处理

| on_failure           | 行为                     |
| -------------------- | ------------------------ |
| `retry_with_context` | 携带错误反馈重试（默认） |
| `skip`               | 跳过步骤，继续执行       |
| `halt`               | 停止整个计划             |

### 成本节省

- **计划阶段**（Opus）：每次复杂计划约 $0.50-2.00
- **执行阶段**（LM Studio）：免费（本地）
- **ROI**：实现任务成本降低 80-90%

### 局限性

| 局限                  | 缓解措施               |
| --------------------- | ---------------------- |
| 本地模型质量不一      | 严格验证 + 重试        |
| LM Studio 无 MCP 工具 | 在上下文中注入文件内容 |
| 上下文窗口有限        | 截断旧结果             |
| 无流式输出            | 每步 120 秒超时        |

---

## 审计扫描

对你的 Claude Code 配置进行安全和质量审计。

```bash
./audit-scan.sh
```

检查项：

- CLAUDE.md 文件中的敏感数据
- 权限配置
- MCP 服务器安全
- 钩子脚本安全

---

## 健康检查

快速验证 Claude Code 安装。

```bash
# macOS/Linux
./check-claude.sh

# Windows
./check-claude.ps1
```

---

## 干净重装

完整重装，保留配置。

```bash
# macOS/Linux
./clean-reinstall-claude.sh

# Windows
./clean-reinstall-claude.ps1
```

---

## 全新上下文循环

为长时间运行的任务以全新上下文运行 Claude Code。

```bash
./fresh-context-loop.sh --iterations 5 --project /path/to/project
```

---

## 会话搜索

跨所有 Claude Code 会话历史搜索。

```bash
./session-search.sh "authentication"
```

---

## 会话管理器（进阶）

用于会话搜索、浏览、恢复和模式发现的进阶 CLI，支持增量索引。

**对比 session-search.sh**：搜索更快（约 200ms vs 约 400ms），支持部分 ID 恢复、分支过滤、工作树支持、增量 JSONL 索引，以及用于自动配置优化的 `discover` 子命令。

**GitHub**：[FlorianBruniaux/cc-sessions](https://github.com/FlorianBruniaux/cc-sessions)

```bash
# 在当前项目中搜索
cc-sessions search "notion"

# 搜索所有项目
cc-sessions --all search "stripe"

# 按日期和分支过滤
cc-sessions search "auth" --since 7d --branch develop

# 最近会话
cc-sessions recent 10

# 通过部分 ID 恢复
cc-sessions resume 8d472d

# 脚本用 JSON 输出
cc-sessions --json search "prisma" | jq -r '.[].id'

# 发现重复模式（n-gram、本地、免费）
cc-sessions --all discover

# 通过 claude --print 进行语义分析
cc-sessions --all discover --llm

# 脚本用 JSON 输出
cc-sessions --all discover --json | jq '.[] | select(.category == "skill")'
```

**从 GitHub 安装**：

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/cc-sessions/main/cc-sessions \
  -o ~/.local/bin/cc-sessions && chmod +x ~/.local/bin/cc-sessions
```

**或本地复制**：`cp cc-sessions.py ~/bin/cc-sessions && chmod +x ~/bin/cc-sessions`

> [GitHub 仓库](https://github.com/FlorianBruniaux/cc-sessions) · [Gist](https://gist.github.com/FlorianBruniaux/992d4d1107592d9e98ca9d89838871c6)

---

## 会话统计

获取 Claude Code 使用统计。

```bash
./session-stats.sh
```

---

## PPTX 转 PDF（macOS）

使用 Keynote 批量将 PPTX 演示文稿转为 PDF。无需 LibreOffice、无需 Python —— 仅 macOS + Keynote。

```bash
# 转换文件夹中所有 PPTX（递归）
./pptx-to-pdf.sh ~/Downloads/Prose

# 转换当前目录
./pptx-to-pdf.sh
```

**依赖**：macOS + 已安装 Keynote。

**行为**：

- 递归：查找子目录中所有 `.pptx` 文件
- 幂等：已有 `.pdf` 的文件会跳过
- 输出：PDF 创建在每个 PPTX 旁边，同目录、同名
- 末尾打印摘要

**关键坑点**：脚本通过 Shell 的 `open -a "Keynote"` 打开文件，而非通过 AppleScript 自带的 `open` 命令。当 Keynote 通过 AppleScript 打开 PPTX 时，有时不会在内部列表中注册文档，导致 `document 1` 报错 -1719。Shell open + 8 秒等待模式可靠地解决了此问题。
