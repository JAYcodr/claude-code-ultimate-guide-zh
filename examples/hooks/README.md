---
title: "Claude Code 钩子"
description: "用于自动化、安全拦截和上下文增强的事件驱动脚本"
tags: [hooks, security, template, config]
---

# Claude Code 钩子

钩子是在 Claude Code 事件上自动执行的脚本。它们实现自动化、拦截危险操作并丰富上下文。

## 可用钩子

| 钩子                                                                | 事件         | 用途                                          | 平台         |
| ------------------------------------------------------------------- | ------------ | --------------------------------------------- | ------------ |
| [dangerous-actions-blocker.sh](./bash/dangerous-actions-blocker.sh) | PreToolUse   | 拦截危险命令/编辑                             | Bash         |
| [security-check.sh](./bash/security-check.sh)                       | PreToolUse   | 拦截命令中的密钥                              | Bash         |
| [prompt-injection-detector.sh](./bash/prompt-injection-detector.sh) | PreToolUse   | 检测注入尝试（+ANSI、null bytes、嵌套命令）   | Bash         |
| [unicode-injection-scanner.sh](./bash/unicode-injection-scanner.sh) | PreToolUse   | 检测零宽字符、RTL 覆盖、ANSI 转义、null bytes | Bash         |
| [repo-integrity-scanner.sh](./bash/repo-integrity-scanner.sh)       | PreToolUse   | 扫描 README/package.json 中的隐藏注入         | Bash         |
| [mcp-config-integrity.sh](./bash/mcp-config-integrity.sh)           | SessionStart | 验证 MCP 配置哈希（CVE-2025-54135/54136）     | Bash         |
| [claudemd-scanner.sh](./bash/claudemd-scanner.sh)                   | SessionStart | 检测 CLAUDE.md 注入攻击                       | Bash         |
| [output-secrets-scanner.sh](./bash/output-secrets-scanner.sh)       | PostToolUse  | 检测工具输出中的密钥 + 环境变量泄露           | Bash         |
| [auto-format.sh](./bash/auto-format.sh)                             | PostToolUse  | 编辑后自动格式化                              | Bash         |
| [rtk-baseline.sh](./bash/rtk-baseline.sh)                           | SessionStart | 保存 RTK 基线用于会话节省追踪                 | Bash         |
| [session-summary.sh](./bash/session-summary.sh)                     | SessionEnd   | 完整会话分析（15 个可配置分区）               | Bash         |
| [session-summary-config.sh](./bash/session-summary-config.sh)       | CLI 工具     | 配置 session-summary 分区、顺序、预览         | Bash         |
| [learning-capture.sh](./bash/learning-capture.sh)                   | Stop         | 提示每日学习记录                              | Bash         |
| [sandbox-validation.sh](./bash/sandbox-validation.sh)               | PreToolUse   | 验证沙箱隔离                                  | Bash         |
| [file-guard.sh](./bash/file-guard.sh)                               | PreToolUse   | 保护敏感文件不被修改                          | Bash         |
| [permission-request.sh](./bash/permission-request.sh)               | PreToolUse   | 高风险操作的显式权限流程                      | Bash         |
| [rtk-auto-wrapper.sh](./bash/rtk-auto-wrapper.sh)                   | PreToolUse   | 自动为命令包裹 RTK 以节省 token               | Bash         |
| [setup-init.sh](./bash/setup-init.sh)                               | SessionStart | 初始化会话环境                                | Bash         |
| [auto-checkpoint.sh](./bash/auto-checkpoint.sh)                     | PostToolUse  | 按间隔自动创建工作检查点                      | Bash         |
| [typecheck-on-save.sh](./bash/typecheck-on-save.sh)                 | PostToolUse  | 保存时运行 TypeScript 检查                    | Bash         |
| [test-on-change.sh](./bash/test-on-change.sh)                       | PostToolUse  | 文件变更时运行测试                            | Bash         |
| [output-validator.sh](./bash/output-validator.sh)                   | PostToolUse  | 启发式输出验证                                | Bash         |
| [session-logger.sh](./bash/session-logger.sh)                       | PostToolUse  | 记录操作用于监控                              | Bash         |
| [privacy-warning.sh](./bash/privacy-warning.sh)                     | PostToolUse  | 警告潜在隐私泄露                              | Bash         |
| [tts-selective.sh](./bash/tts-selective.sh)                         | PostToolUse  | 对选定输出进行文本转语音                      | Bash         |
| [subagent-stop.sh](./bash/subagent-stop.sh)                         | Stop         | 清理子智能体资源                              | Bash         |
| [pre-commit-secrets.sh](./bash/pre-commit-secrets.sh)               | Git 钩子     | 阻止密钥进入提交                              | Bash         |
| [pre-commit-evaluator.sh](./bash/pre-commit-evaluator.sh)           | Git 钩子     | LLM-as-a-Judge 提交前验证                     | Bash         |
| [notification.sh](./bash/notification.sh)                           | Notification | 基于上下文的 macOS 音效提醒                   | Bash (macOS) |
| [auto-rename-session.sh](./bash/auto-rename-session.sh)             | SessionEnd   | 通过 Haiku 生成 AI 驱动的会话标题             | Bash         |
| [security-gate.sh](./bash/security-gate.sh)                         | PreToolUse   | 写入源文件前检测有漏洞的代码模式              | Bash         |
| [velocity-governor.sh](./bash/velocity-governor.sh)                 | PreToolUse   | 限速工具调用以避免 API 限流                   | Bash         |
| [security-check.ps1](./powershell/security-check.ps1)               | PreToolUse   | 拦截命令中的密钥                              | PowerShell   |
| [auto-format.ps1](./powershell/auto-format.ps1)                     | PostToolUse  | 编辑后自动格式化                              | PowerShell   |

## 钩子事件

| 事件                 | 触发时机             | 典型用例                   |
| -------------------- | -------------------- | -------------------------- |
| `SessionStart`       | 会话开始或恢复       | 初始化、环境设置、配置扫描 |
| `UserPromptSubmit`   | 用户发送消息         | 上下文增强、预处理         |
| `PreToolUse`         | 工具执行前           | 验证、拦截危险操作         |
| `PermissionRequest`  | 权限对话框出现       | 自定义审批逻辑             |
| `PostToolUse`        | 工具执行成功后       | 格式化、日志记录、清理     |
| `PostToolUseFailure` | 工具执行失败后       | 错误日志、恢复操作         |
| `Notification`       | Claude 发送通知      | 音效提醒、外部通知         |
| `SubagentStart`      | 子智能体创建         | 子智能体初始化             |
| `SubagentStop`       | 子智能体结束         | 子智能体清理               |
| `Stop`               | Claude 完成响应      | 响应后操作、状态保存       |
| `TeammateIdle`       | 智能体队友空闲       | 团队协调                   |
| `TaskCompleted`      | 任务标记为完成       | 工作流触发                 |
| `ConfigChange`       | 会话期间配置文件变更 | 企业审计、拦截未授权变更   |
| `WorktreeCreate`     | 智能体工作树创建     | 设置数据库分支、安装依赖   |
| `WorktreeRemove`     | 智能体工作树拆除     | 清理数据库分支、临时凭据   |
| `PreCompact`         | 上下文压缩前         | 压缩前保存状态             |
| `SessionEnd`         | 会话终止             | 清理、会话摘要             |

## 高级护栏（v3.3.0 新增）

受生产环境 LLM 系统启发的进阶保护模式。

### prompt-injection-detector.sh

**事件**：`PreToolUse`

在提示词注入尝试到达 Claude 之前检测并拦截：

**检测模式**：

- 角色覆盖："ignore previous instructions"、"you are now"、"pretend to be"
- 越狱尝试："DAN mode"、"developer mode"、"no restrictions"
- 分隔符注入：`</system>`、`[INST]`、`<<SYS>>`
- 权威冒充："anthropic employee"、"authorized to bypass"
- Base64 编码负载（解码后扫描）
- 上下文操纵：关于之前消息的虚假声明

**配置**：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/prompt-injection-detector.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### output-validator.sh

**事件**：`PostToolUse`

对 Claude 输出进行启发式验证（不调用 LLM，纯 Bash）：

**验证检查**：

- 占位路径：`/path/to/`、`/your/project/`
- 占位内容：`TODO:`、`your-api-key`、`example.com`
- 输出中潜在的密钥（正则模式）
- 不确定性指标（多处 "I'm not sure"、"probably"）
- 不完整实现：`NotImplementedError`、`throw new Error`
- 未验证的引用声明

**行为**：通过 `systemMessage` 警告，不拦截。如需深度验证，使用 `output-evaluator` 智能体。

### session-logger.sh

**事件**：`PostToolUse`

将所有 Claude 操作记录到 JSONL 文件，用于监控和成本追踪：

**日志位置**：`~/.claude/logs/activity-YYYY-MM-DD.jsonl`

**记录数据**：

- 时间戳、会话 ID、工具名称
- 文件路径和命令（截断）
- 项目名称
- Token 估算（输入/输出）

**分析**：使用 `session-stats.sh` 脚本分析日志。

**环境变量**：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `CLAUDE_LOG_DIR` | `~/.claude/logs` | 日志目录 |
| `CLAUDE_LOG_TOKENS` | `true` | 启用 token 估算 |
| `CLAUDE_SESSION_ID` | auto | 自定义会话 ID |

完整文档见[可观测性指南](../../guide/ops/observability.md)。

### pre-commit-evaluator.sh

**类型**：Git 预提交钩子（非 Claude 钩子）

每次提交前的 LLM-as-a-Judge 评估。由于 API 费用，**仅需主动启用**。

**安装**：

```bash
cp pre-commit-evaluator.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
export CLAUDE_PRECOMMIT_EVAL=1  # 启用评估
```

**成本**：每次提交约 $0.01-0.05（Haiku 模型）

**绕过**：`git commit --no-verify` 或 `CLAUDE_SKIP_EVAL=1 git commit`

---

## 安全钩子

### dangerous-actions-blocker.sh

**事件**：`PreToolUse`（Bash、Edit、Write）

全面的危险操作防护：

**Bash - 被拦截的命令**：

- 系统破坏：`rm -rf /`、`rm -rf ~`、`sudo rm`
- 磁盘操作：`dd if=`、`mkfs`、`> /dev/sda`
- Fork 炸弹：`:(){:|:&};:`
- 数据库删除：`DROP DATABASE`、`DROP TABLE`
- 强制推送：`git push --force main/master`
- 包发布：`npm publish`、`pnpm publish`
- 密钥模式：`password=`、`api_key=`、`token=`

**Edit/Write - 受保护文件**：

- 环境配置：`.env`、`.env.local`、`.env.production`
- 凭据：`credentials.json`、`serviceAccountKey.json`
- SSH 密钥：`id_rsa`、`id_ed25519`、`id_ecdsa`
- 配置：`.npmrc`、`.pypirc`、`secrets.yml`

**Edit/Write - 允许的路径**：

- `$CLAUDE_PROJECT_DIR`（当前项目）
- `~/.claude/`（Claude 配置）
- `/tmp/`（临时文件）
- 通过 `$ALLOWED_PATHS` 环境变量添加的额外路径

**退出码**：

```bash
exit 0  # 允许操作
exit 2  # 拦截（stderr 消息展示给 Claude）
```

**配置**：

```bash
# 添加自定义允许路径（冒号分隔）
export ALLOWED_PATHS="/custom/path:/another/path"
```

### security-check.sh

**事件**：`PreToolUse`（Bash）

专注于检测命令中的密钥：

- 密码模式
- API 密钥（常见格式如 `sk-xxx`、`pk-xxx`）
- AWS 凭据
- 私钥
- 硬编码 token

### claudemd-scanner.sh

**事件**：`SessionStart`

在会话启动时扫描 CLAUDE.md 文件，检测潜在提示词注入攻击：

**检测模式**：

- "ignore previous instructions" 变体
- Shell 注入：`curl | bash`、`wget | sh`、`eval(`
- Base64 编码内容（潜在的混淆手段）
- HTML 注释中的隐藏指令
- 可疑超长行（>500 字符）
- 敏感关键词附近的非 ASCII 字符（同形字攻击）

**扫描文件**：

- `CLAUDE.md`（项目根目录）
- `.claude/CLAUDE.md`（本地覆盖）
- `.claude/` 目录中的所有 `.md` 文件

**为什么重要**：当你克隆陌生仓库时，恶意 CLAUDE.md 可能注入指令危及系统。此钩子在 Claude 处理潜在危险指令前向你发出警告。

**配置**：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/claudemd-scanner.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### output-secrets-scanner.sh

**事件**：`PostToolUse`

作为 `security-check.sh` 的补充，扫描工具的**输出**（而非输入）中泄露的密钥。

**检测模式**：

- API 密钥：OpenAI、Anthropic、AWS、GCP、Azure、Stripe、Twilio、SendGrid
- Token：GitHub、GitLab、NPM、PyPI、JWT
- 私钥：RSA、EC、DSA、OpenSSH、PGP
- 嵌入密码的数据库 URL
- 通用 `api_key=`、`secret=`、`password=` 模式

**为什么重要**：Claude 可能读取 `.env` 文件并在响应或提交中包含凭据。此钩子在密钥泄露前将其捕获。

**配置**：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/output-secrets-scanner.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

## 生产力钩子

### rtk-baseline.sh

**事件**：`SessionStart`

在会话启动时捕获 RTK 累计统计数据，用于增量追踪。与 `session-summary.sh` 配合使用，后者在会话结束时计算每次会话的 RTK 节省量。

**配置**：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/rtk-baseline.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### session-summary.sh (v3)

**事件**：`SessionEnd`

完整的会话分析，包含 15 个可配置分区、CLI 配置工具和 JSONL 日志记录。

**插件安装（推荐）**：

```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
claude plugin install session-summary@florian-claude-tools
```

钩子自动接入，无需手动配置。详见[插件仓库](https://github.com/FlorianBruniaux/claude-code-plugins)。

**分区**（均可通过环境变量或配置文件配置）：

| 分区       | 默认值 | 说明                                     |
| ---------- | ------ | ---------------------------------------- |
| `meta`     | always | 会话 ID、名称、分支                      |
| `duration` | always | 墙钟时间、活跃时间、轮次、退出原因       |
| `tools`    | always | 工具调用明细（成功/失败）                |
| `errors`   | on     | 按工具分组的错误详情                     |
| `files`    | on     | 读取/编辑/创建的文件及编辑次数最多的文件 |
| `features` | on     | MCP 服务器、智能体、技能、团队、计划模式 |
| `git`      | on     | Git diff 摘要（增减行数、变更文件数）    |
| `loc`      | on     | 通过 Edit/Write 编写的代码行数           |
| `models`   | always | 模型使用（请求数、token 数）             |
| `cache`    | always | 缓存命中率                               |
| `cost`     | always | 估算成本（ccusage 或定价表）             |
| `rtk`      | on     | RTK token 节省（相对于会话开始时的增量） |
| `ratio`    | on     | 对话比率（交互轮次/自动轮次）            |
| `thinking` | off    | 思考块计数                               |
| `context`  | off    | 上下文窗口估算（峰值百分比）             |

**日志文件**：`~/.claude/logs/session-summaries.jsonl`（结构化 JSONL，包含所有指标）

**配置优先级**：`环境变量（SESSION_SUMMARY_*）` > `配置文件（~/.config/session-summary/config.sh）` > `默认值`

**环境变量**：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `NO_COLOR` | - | 禁用 ANSI 颜色 |
| `SESSION_SUMMARY_SKIP` | `0` | 设为 `1` 禁用摘要 |
| `SESSION_SUMMARY_LOG` | `~/.claude/logs` | 覆盖日志目录 |
| `SESSION_SUMMARY_FILES` | `1` | 文件分区开关 |
| `SESSION_SUMMARY_RTK` | `auto` | `auto` / `1` / `0` |
| `SESSION_SUMMARY_GIT` | `1` | Git diff 开关 |
| `SESSION_SUMMARY_ERRORS` | `1` | 错误详情开关 |
| `SESSION_SUMMARY_LOC` | `1` | 代码行数开关 |
| `SESSION_SUMMARY_RATIO` | `1` | 对话比率开关 |
| `SESSION_SUMMARY_FEATURES` | `1` | 使用功能开关 |
| `SESSION_SUMMARY_THINKING` | `0` | 思考块开关 |
| `SESSION_SUMMARY_CONTEXT` | `0` | 上下文估算开关 |
| `SESSION_SUMMARY_SECTIONS` | (全部) | 逗号分隔的分区顺序 |

**CLI 配置工具**（`session-summary-config.sh`）：

```bash
session-summary-config show              # 当前配置及分区状态
session-summary-config set git=0         # 禁用某个分区
session-summary-config set thinking=1    # 启用某个分区
session-summary-config reset             # 重置为默认值
session-summary-config sections          # 显示分区顺序
session-summary-config sections "meta,duration,tools,cost"  # 最小化输出
session-summary-config preview           # 以当前配置展示演示输出
session-summary-config install           # 在 settings.json 中安装钩子
session-summary-config log 5             # 最近 5 次会话摘要
```

**依赖**：

- `jq`（JSON 解析必需）
- `ccusage`（可选，用于精确成本计算）
- `rtk`（可选，用于 token 节省追踪）

**截图**（真实会话输出）：

![Session Summary v3](../../docs/images/session-summary-v3.png)

**示例输出**（全部分区启用）：

```
═══ 会话摘要 ═══════════════════
ID:       abc-123-def-456...
名称:     Fix session summary hook
分支:   main
时长: 墙钟 5m 28s | 活跃 1m 33s | 12 轮 | 退出: user

工具调用: 29 (成功 27 / 失败 2)
  Edit: 13  Bash: 8  Read: 6  Grep: 1  Glob: 1

错误: 2
  Bash: "command not found: rtk" (x1)
  Edit: "old_string not unique" (x1)

文件: 3 读取 · 2 编辑 · 1 创建
  session-summary.sh (8 次编辑), settings.json (3 次编辑)

功能: MCP (perplexity x4, chrome x12) · 智能体 (Explore x3, Plan x1) · 技能 (commit)

Git: +142 -37 行 · 4 个文件变更
代码: +87 -12 净增 (通过 Edit/Write)

模型使用              请求    输入     输出
claude-opus-4-6       59      93K      628
缓存: 85% 命中率 (读取 3.9M / 创建 322K)
估算成本: $0.045

RTK 节省: 24 命令 · ~12.4K token 节省 (73%)
轮次: 12 (8 交互 · 4 自动) · 平均 6.7s/轮
═══════════════════════════════════════
```

**配置**：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/session-summary.sh"
          }
        ]
      }
    ]
  }
}
```

**快速安装**：插件系统（见上文）或手动：`session-summary-config.sh install`（复制钩子 + 更新 settings.json）

**与 tweakcc 的 `/cost` 补丁对比**：

[tweakcc](https://github.com/Piebald-AI/tweakcc)（1K+ 星）通过补丁修改 Claude Code 的 `cli.js` 来为 Pro/Max 订阅者重新启用 `/cost`。做法不同，取舍不同：

|                  | tweakcc `/cost`             | session-summary.sh                                                                      |
| ---------------- | --------------------------- | --------------------------------------------------------------------------------------- |
| 方式             | 补丁修改 Claude Code 二进制 | 官方钩子 API（无修改）                                                                  |
| 能否经受 CC 更新 | 否（每次更新需重新应用）    | 是                                                                                      |
| 触发方式         | 手动（`/cost` 命令）        | 会话退出时自动                                                                          |
| 指标             | 成本、时长、token、代码行数 | 15 个分区（成本、token、工具、错误、文件、功能、git diff、代码行数、缓存、RTK、比率等） |
| 历史记录         | 无                          | JSONL 日志，包含所有指标                                                                |
| 依赖             | Node.js                     | jq（Bash 原生）                                                                         |

tweakcc 是更广泛的工具（主题、提示词、工具集）——`/cost` 补丁只是其中一项功能。本钩子专注于会话分析，指标更深，且不修改 Claude Code 内部。

### auto-format.sh / auto-format.ps1

**事件**：`PostToolUse`（Edit、Write）

编辑后自动格式化文件：

| 扩展名                          | 格式化工具       |
| ------------------------------- | ---------------- |
| `.ts`、`.tsx`、`.js`、`.jsx`    | Prettier         |
| `.json`、`.css`、`.scss`、`.md` | Prettier         |
| `.prisma`                       | `prisma format`  |
| `.py`                           | Black / autopep8 |
| `.go`                           | `go fmt`         |

**静默运行**：无输出，失败忽略以避免阻塞 Claude。

**依赖**：在项目中安装格式化工具：

```bash
# Node.js 项目
npm install -D prettier

# Python 项目
pip install black

# Go 项目（内置）
go fmt
```

### notification.sh

**事件**：`Notification`（仅 macOS）

根据通知内容播放不同音效：

| 上下文 | 音效           | 触发条件                         |
| ------ | -------------- | -------------------------------- |
| 成功   | Hero.aiff      | "completed"、"done"、"success"   |
| 错误   | Basso.aiff     | "error"、"failed"、"problem"     |
| 等待   | Submarine.aiff | "waiting"、"permission"、"input" |
| 警告   | Sosumi.aiff    | "warning"、"attention"、"alert"  |
| 默认   | Ping.aiff      | 其他通知                         |

**特性**：

- 非阻塞（后台播放）
- 原生 macOS 通知
- 通过关键词自动检测上下文
- 多语言支持（英语/法语）

**依赖**：macOS，`afplay` 和 `osascript`（内置）

## 配置

钩子在 `.claude/settings.json` 中配置：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/dangerous-actions-blocker.sh",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-format.sh",
            "timeout": 10000
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/notification.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

**匹配器模式**：

- `".*"` — 匹配所有工具
- `"Bash"` — 仅匹配 Bash 工具
- `"Edit|Write"` — 匹配 Edit 或 Write 工具
- `"Bash|Edit|Write"` — 匹配多个工具

## 创建自定义钩子

### 基础模板

```bash
#!/bin/bash
# 钩子: [事件类型] - 描述
# Exit 0 = 成功/允许, Exit 2 = 拦截（仅 PreToolUse）

set -e

# 从 stdin 读取 JSON
INPUT=$(cat)

# 提取数据
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# 你的逻辑……

# 返回可选 JSON
cat << EOF
{
  "systemMessage": "展示给 Claude 的消息",
  "hookSpecificOutput": {
    "additionalContext": "添加的额外上下文"
  }
}
EOF

exit 0
```

### 环境变量

钩子脚本中可用：

| 变量                 | 说明                     |
| -------------------- | ------------------------ |
| `CLAUDE_PROJECT_DIR` | 当前项目路径             |
| `CLAUDE_FILE_PATHS`  | 通过 `-f` 标志传入的文件 |
| `CLAUDE_TOOL_INPUT`  | JSON 格式的工具输入      |
| `HOME`               | 用户主目录               |

### 最佳实践

1. **短超时**：最大 5-10 秒，避免阻塞 Claude
2. **优雅失败**：对非关键操作使用 `|| true`
3. **最小化日志**：避免 stdout 输出（结构化 JSON 除外）
4. **依赖 jq**：使用 `jq` 可靠解析 JSON
5. **充分测试**：部署前用各种输入测试
6. **文档化行为**：清晰注释钩子功能
7. **处理错误**：提供适当的调试错误消息

### 示例：Git 上下文增强

创建 `git-context.sh`（UserPromptSubmit 事件）：

```bash
#!/bin/bash
# 钩子: UserPromptSubmit — 向提示词添加 Git 上下文

set -e

INPUT=$(cat)

# 获取 Git 信息
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
LAST_COMMIT=$(git log -1 --oneline 2>/dev/null || echo "none")
UNCOMMITTED=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')

# 返回增强的上下文
cat << EOF
{
  "systemMessage": "[Git] 分支: $BRANCH | 最近: $LAST_COMMIT | 未提交: $UNCOMMITTED 文件 | 暂存: $STAGED 文件"
}
EOF

exit 0
```

在 settings 中注册：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/git-context.sh",
            "timeout": 3000
          }
        ]
      }
    ]
  }
}
```

## 安装

### 项目级（团队共享）

1. 创建钩子目录：

```bash
mkdir -p .claude/hooks
```

1. 从 examples 复制钩子：

```bash
cp /path/to/examples/hooks/bash/dangerous-actions-blocker.sh .claude/hooks/
chmod +x .claude/hooks/*.sh
```

1. 在 `.claude/settings.json` 中配置（见上文配置章节）

1. 提交到仓库：

```bash
git add .claude/hooks/ .claude/settings.json
git commit -m "添加 Claude Code 钩子"
```

### 个人/全局（仅本机）

1. 创建全局钩子目录：

```bash
mkdir -p ~/.claude/hooks
```

1. 复制钩子：

```bash
cp /path/to/examples/hooks/bash/notification.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

1. 在 `~/.claude/settings.json` 中配置

**优先级**：项目钩子覆盖全局钩子。

## 平台注意事项

### macOS / Linux（Bash）

- 使用 `.sh` 扩展名
- 需 `chmod +x` 赋予执行权限
- 路径分隔符：`/`
- 主目录：`~` 或 `$HOME`

### Windows（PowerShell）

- 使用 `.ps1` 扩展名
- 可能需要执行策略：`Set-ExecutionPolicy RemoteSigned`
- 路径分隔符：`\`
- 主目录：`$env:USERPROFILE`

## 故障排查

### 钩子未执行

**原因**：未在 settings.json 中注册或路径错误

**修复**：验证配置，使用绝对路径或 `$CLAUDE_PROJECT_DIR`

### 权限拒绝

**原因**：钩子不可执行

**修复**：

```bash
chmod +x .claude/hooks/*.sh
```

### 钩子拦截所有操作

**原因**：无条件退出码 2

**修复**：检查逻辑，确保 `exit 0` 是默认情况

### 超时错误

**原因**：钩子耗时过长（>超时值）

**修复**：优化钩子性能或在 settings 中增加超时

### jq 未找到

**原因**：未安装 `jq`

**修复**：安装 jq：

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Windows
choco install jq
```

## 进阶示例

### 活动记录器

将所有 Claude 操作记录到 JSONL 文件：

```bash
#!/bin/bash
# PostToolUse — 记录所有活动

set -e

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
LOG_FILE="$HOME/.claude/logs/activity-$(date +%Y-%m-%d).jsonl"

mkdir -p "$(dirname "$LOG_FILE")"

# 创建日志条目
cat << EOF >> "$LOG_FILE"
{"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","tool":"$TOOL","session":"$CLAUDE_SESSION_ID"}
EOF

exit 0
```

### 数据库迁移检测器

当迁移文件创建时发出提醒：

```bash
#!/bin/bash
# PostToolUse — 检测数据库迁移

set -e

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL" == "Write" ]]; then
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')

    if [[ "$FILE" == *"/migrations/"* ]]; then
        cat << EOF
{
  "systemMessage": "⚠️ 数据库迁移已创建: $FILE\n\n提醒:\n1. 仔细审查迁移\n2. 先在开发数据库测试\n3. 合并后运行 'prisma migrate deploy'"
}
EOF
    fi
fi

exit 0
```

## 安全注意事项

1. **绝不在钩子中存储密钥**：使用环境变量
2. **验证输入**：始终清理来自 stdin 的数据
3. **限制钩子范围**：使用精确匹配器，而非 `".*"`
4. **审查拦截操作**：记录钩子拦截的行为
5. **隔离测试**：先在 Claude 外部测试钩子
6. **版本控制**：将钩子提交到仓库以供团队共享

## 资源

- [主指南 — 第 7 节：钩子](../../guide/ultimate-guide.md#7-hooks)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)
- [钩子事件参考](../../guide/ultimate-guide.md#71-hook-events)

---

_详细说明和进阶模式见[主指南](../../guide/ultimate-guide.md)。_
