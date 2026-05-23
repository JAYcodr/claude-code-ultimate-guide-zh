<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

---
title: "Claude Code 速查表"
description: "一页可打印的日常精华，帮你把 Claude Code 用出最大效率"
tags: [cheatsheet, reference]
---

# Claude Code 速查表

**1 页可打印** — 日常高频操作，一张纸搞定

**作者**: Florian BRUNIAUX | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**写作工具**: Claude (Anthropic)

**版本**: 3.40.0 | **最后更新**: 2026 年 5 月

---

## 常用命令

| 命令 | 操作 |
|------|------|
| `/help` | 上下文相关帮助 |
| `/powerup` | 互动式动画课程，边看边学 Claude Code 功能 |
| `/clear` | 重置对话 |
| `/compact` | 释放上下文空间 |
| `/status` | 会话状态 + 上下文用量 |
| `/context` | 详细的 token 拆分 |
| `/plan` | 进入计划模式（不改代码） |
| `/ultraplan` | 云端计划模式 — 云上起草，浏览器审阅（v2.1.91+） |
| `/execute` | 退出计划模式（执行变更） |
| `/model` | 切换模型（sonnet / opus / opusplan） |
| `/insights` | 用量分析 + 优化报告 |
| `/simplify` | 检测已变更代码中的过度设计并自动修复 |
| `/batch` | 通过 5–30 个并行 worktree 智能体执行大规模重构 |
| `/teleport` | 从网页端传送会话 |
| `/tasks` | 监控后台任务 |
| `/remote-env` | 配置云端环境 |
| `/remote-control` | 开启远程控制会话（Research Preview, Pro/Max） |
| `/rc` | `/remote-control` 的别名 |
| `/mobile` | 获取 Claude 移动应用下载链接 |
| `/fast` | 切换快速模式（2.5x 速度，6x 费用） |
| `/voice` | 切换语音输入（按住 Space 说话，松开发送） |
| `/recap` | 回到中断的会话时，展示上下文摘要（v2.1.108） |
| `/effort [level]` | 思考深度：low/medium/high/xhigh/max；不加参数则弹出交互式滑块（v2.1.111） |
| `/tui [fullscreen]` | 全屏无闪烁 TUI 渲染（v2.1.110） |
| `/focus` | 切换极简聚焦视图，与 Ctrl+O 独立（v2.1.110） |
| `/less-permission-prompts` | 扫描对话记录，自动提议只读工具白名单（v2.1.111） |
| `/btw [question]` | 侧边问题浮层 — 只读的一次性智能体，不污染历史，不使用工具 |
| `/loop [interval] [prompt]` | 重复执行一段提示词（例：`/loop 5m check the deploy`，默认 10m） |
| `/stats` | 用量图、最爱模型、连续使用天数（v2.1.118 起为 `/usage` 的别名） |
| `/usage` | 各模型的 token + 费用用量（v2.1.118） |
| `/ultrareview` | 多智能体云端代码审查（v2.1.114） |
| `/goal [condition]` | 自主多轮模式：Claude 持续工作直到条件满足，实时浮层显示耗时/轮次/token（v2.1.139） |
| `/scroll-speed` | 调节鼠标滚轮速度，带交互式实时预览滑块（v2.1.139） |
| `/rename [name]` | 命名或重命名当前会话 |
| `/copy` | 交互式选取器，复制代码块或完整回复 |
| `/debug` | 系统化故障排查 |
| `/exit` | 退出（或 Ctrl+D） |

---

## 键盘快捷键

| 快捷键 | 操作 |
|--------|------|
| `Shift+Tab` | 循环切换权限模式 |
| `Esc` × 2 | 回退（撤销） |
| `Ctrl+C` | 中断 |
| `Ctrl+R` | 搜索命令历史 |
| `Ctrl+L` | 清屏（保留上下文） |
| `Tab` | 自动补全 |
| `Shift+Enter` | 换行 |
| `Ctrl+B` | 后台任务 |
| `Ctrl+F` | 终止所有后台智能体（按两次） |
| `Alt+T` | 切换思考模式 |
| `Space`（按住） | 语音输入（需先启用 `/voice`） |
| `Ctrl+D` | 退出 |

---

## 文件引用

```
@path/to/file.ts    → 引用文件
@agent-name         → 调用智能体
!shell-command      → 执行 shell 命令
```

| IDE | 快捷键 |
|-----|--------|
| VS Code | `Alt+K` |
| JetBrains | `Cmd+Option+K` |

---

## 你可能不知道的功能（但都是官方支持的！）

| 功能 | 起始版本 | 说明 |
|------|---------|------|
| **Tasks API** | v2.1.16 | 持久的任务列表，支持依赖关系 |
| **Background Agents** | v2.0.60 | 你写代码的时候子智能体在后台干活 |
| **Agent Teams** | v2.1.32 | 多智能体协同（TeamCreate / SendMessage） |
| **Auto-Memories** | v2.1.32 | 跨会话自动捕捉上下文 |
| **Session Forking** | v2.1.19 | 回退并创建平行时间线 |
| **LSP Tool** | v2.0.74 | IDE 级别的导航：符号、类型、引用。~50ms 对比 grep 的 45s。支持 11 种语言 |
| **Voice Mode** | v2.1.x | 原生语音输入，免费转写，不计入速率限制 |
| **Remote Control** | v2.1.51 | 从手机/浏览器控制本地会话（Research Preview, Pro/Max） |
| **`/loop`** | v2.1.71 | 会话内的循环定时器：`/loop 5m check the deploy`（会话结束即停止）。最小 1 分钟，每会话最多 50 个任务 |
| **`/goal`** | v2.1.139 | 自主完成循环：设定条件，Claude 跨轮次工作，直到独立的评估器（Haiku）确认条件达成。实时浮层显示耗时、轮次、token。三要素公式：可衡量的终点 + 验证机制 + 约束条件 |
| **Cloud Scheduled Tasks** | 2026 | 机器离线也能调度的定时任务，通过 `/schedule` 或 `claude.ai/code/scheduled` 设置。在 Anthropic 基础设施上运行，每次运行都重新克隆仓库，最小间隔 1 小时。Pro/Max/Team/Enterprise |
| **Desktop Scheduled Tasks** | 2026 | 通过桌面应用调度本地机器任务。最小间隔 1 分钟，完全访问本地文件，无需保持会话 |
| **Skill Evals** | 2026 年 3 月 | 两种技能类型：能力增强型（填补模型短板，会逐渐淡出） / 编码偏好型（固化工作流，持续生效）。支持基准模式、A/B 测试、触发调优 |
| **Output Styles** | v2.1.108 | `/config` → "Preferred output style"：**Default**（简洁）、**Explanatory**（附带设计思路）、**Learning**（结对编程风格，标注 `TODO(human)`）。可通过 `.claude/styles/` 自定义风格 |

**启用 LSP**：添加到 `~/.claude/settings.json` → `{ "env": { "ENABLE_LSP_TOOL": "1" } }`（需要先为你的语言安装对应的 LSP 服务：`tsserver`、`pylsp`、`gopls`、`rust-analyzer`、`sourcekit-lsp`……）

**小贴士**：这些不是什么秘密——都写在 [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) 里了。没事翻翻！

---

## 权限模式

| 模式 | 编辑 | 执行 |
|------|------|------|
| Default | 询问 | 询问 |
| acceptEdits | 自动 | 询问 |
| Plan Mode | ❌ | ❌ |
| dontAsk | 仅在白名单内 | 仅在白名单内 |
| bypassPermissions | 自动 | 自动（仅限 CI/CD） |

**Shift+Tab** 循环切换模式

---

## 记忆与设置（2 个层级）

| 层级 | macOS/Linux | Windows | 范围 | Git |
|------|-------------|---------|------|-----|
| **项目级** | `.claude/` | `.claude\` | 团队共享 | ✅ |
| **个人级** | `~/.claude/` | `%USERPROFILE%\.claude\` | 你（所有项目） | ❌ |

**优先级**：项目级覆盖个人级

| 文件 | 位置 | 用途 |
|------|------|------|
| `CLAUDE.md` | 项目根目录 | 团队记忆（指令） |
| `settings.json` | `.claude/` | 团队设置（钩子） |
| `settings.local.json` | `.claude/` | 你的个人设置覆盖 |
| `CLAUDE.md` | `~/.claude/`（Win: `%USERPROFILE%\.claude\`） | 个人记忆 |

---

## .claude/ 目录结构

```
.claude/
├── CLAUDE.md           # 本地记忆（已 gitignore）
├── settings.json       # 钩子配置（纳入版本管理）
├── settings.local.json # 权限配置（不纳入版本管理）
├── agents/             # 自定义智能体
├── hooks/              # 事件脚本
├── rules/              # 自动加载的规则
└── skills/             # Slash 命令 + 知识模块（统一存放）
```

---

## 典型工作流

```
1. 启动会话        → claude
2. 检查上下文       → /status
3. 计划模式         → Shift+Tab × 2（复杂任务时）
4. 描述任务         → 清晰、具体的提示词
5. 审查变更         → 每次都要读 diff！
6. 接受/拒绝        → y/n
7. 验证             → 跑测试
8. 提交             → 任务完成时
9. /compact         → 上下文 >70% 时
```

---

## 上下文管理（关键！）

### 状态栏

```
Model: Sonnet | Ctx: 89.5k | Cost: $2.11 | Ctx(u): 56.0%
```
**关注 `Ctx(u):`** → >70% = 执行 `/compact`，>85% = 执行 `/clear`

**增强状态栏（[ccstatusline](https://github.com/sirmalloc/ccstatusline)）：** 添加到 `~/.claude/settings.json`：
```json
{ "statusLine": { "type": "command", "command": "npx -y ccstatusline@latest", "padding": 0 } }
```

### 上下文阈值

| 上下文占比 | 状态 | 操作 |
|-----------|------|------|
| 0-50% | 🟢 绿色 | 放心干活 |
| 50-70% | 🟡 黄色 | 开始精打细算 |
| 70-90% | 🟠 橙色 | 马上 `/compact` |
| 90%+ | 🔴 红色 | 必须 `/clear` |

### 按症状处理

| 表现 | 操作 |
|------|------|
| 回复变短 | `/compact` |
| 频繁忘记 | `/clear` |
| 上下文 >70% | `/compact` |
| 任务完成 | `/clear` |

### 上下文恢复命令

| 命令 | 用法 |
|------|------|
| `/compact` | 摘要总结，释放上下文 |
| `/clear` | 从头再来 |
| `/rewind` | 撤销最近的变更 |
| `claude -c` | 恢复上次会话（CLI 参数） |
| `claude -r <id>` | 恢复指定会话（CLI 参数） |

---

## 底层原理（速览）

| 概念 | 要点 |
|------|------|
| **主循环** | 简单的 `while(tool_call)` — 没有 DAG，没有分类器 |
| **工具** | 8 个核心工具：Bash, Read, Edit, Write, Grep, Glob, Task, TodoWrite |
| **上下文** | ~200K tokens，75-92% 时自动压缩 |
| **子智能体** | 独立上下文，最大深度 = 1 |
| **设计哲学** | "少搭架子，多信模型" — 相信 Claude 的推理能力 |

**深度阅读**：[架构与内部原理](./core/architecture.md)

---

## 计划模式与思考

| 功能 | 激活方式 | 用法 |
|------|---------|------|
| **Plan Mode** | `Shift+Tab × 2` 或 `/plan` | 只探索不改代码 |
| **OpusPlan** | `/model opusplan` | Opus 做计划，Sonnet 执行 |
| **Ultraplan** | `/ultraplan <prompt>` | 云端规划，浏览器审阅，终端不用等（v2.1.91+，需 GitHub） |

> **Opus 4.7**（v2.1.114+）：Claude Code 默认思考深度 = **xhigh**（所有计划）。新增 `xhigh` 级别，位于 `high` 和 `max` 之间——更精细的推理/延迟控制。用 `ultrathink` 强制下一轮使用最大深度。

| 控制方式 | 操作 | 持久性 |
|---------|------|--------|
| **Alt+T** | 开关思考模式 | 会话内 |
| **/config** | 全局启用/禁用 | 永久 |
| **`/model` 滑块** | 左右箭头：`low\|medium\|high\|xhigh` | 会话内 |
| **`CLAUDE_CODE_EFFORT_LEVEL`** | 环境变量：`low\|medium\|high\|xhigh\|max` | Shell 会话 |
| **`effortLevel` 设置** | settings.json 中：`low\|medium\|high\|xhigh\|max` | 永久 |
| **skill frontmatter 中的 `effort`**（v2.1.80+） | 按技能覆盖：`low\|medium\|high\|xhigh` | 每次调用 |

**省钱技巧**：简单任务用 Alt+T 关掉思考模式 → 更快更便宜。

**按技能调深度**——机械性技能（commit、sync、scaffold）加 `effort: low`，分析型技能（security-audit、architecture-review）加 `effort: high`。自动覆盖会话设置。

**OpusPlan 工作流**：`/model opusplan` → `Shift+Tab × 2`（Opus 做计划）→ `Shift+Tab`（Sonnet 执行）

**Ultraplan 工作流**：`/ultraplan <task>` → 云端起草时终端依然可用 → 在浏览器中内联审阅 → 批准后在网页端执行（PR）或传送回终端

**适用场景**：涉及 3 个以上文件的改动、架构设计、复杂调试

### 快速模型选择

| 任务 | 模型 | 思考深度 |
|------|------|---------|
| 重命名、模板代码、测试生成 | Haiku | low |
| 功能开发、调试、重构 | Sonnet | medium–high |
| 架构设计、安全审计 | Opus | high–max |

> 完整决策表含费用估算：[§2.5 模型选择与思考指南](ultimate-guide.md#25-model-selection--thinking-guide)

### 会话中动态切换模型

**模式**：先用 Sonnet（快）→ 遇到复杂问题切 Opus → 切回 Sonnet

**工作流**：
```bash
# 会话启动（默认 Sonnet）
claude

# 遇到复杂功能
> "Implement OAuth2 flow with PKCE"
/model opus                    # 切换到深度推理

# 功能完成，回到日常
/model sonnet                  # 速度和费用优化
```

**最佳实践**：
- ✅ **在任务边界切换**，不要在任务中间切
- ✅ 架构决策、复杂调试、安全关键代码 → 用 Opus
- ✅ 日常编辑、重构、写测试 → 用 Sonnet
- ✅ 简单修复、拼写检查、验证 → 用 Haiku
- ❌ 实现过程中不要切模型（会丢失上下文）

**费用影响**：
| 模型 | 输入 | 输出 | 适用场景 |
|------|------|------|---------|
| Opus 4.7 | $5/MTok | $25/MTok | 复杂推理（10-20% 的任务） |
| Sonnet 4.6 | $3/MTok | $15/MTok | 日常开发（70-80% 的任务） |
| Haiku 4.5 | $0.80/MTok | $4/MTok | 简单验证（5-10% 的任务） |

**动态切换**让你在复杂任务上兼顾质量和成本。

**来源**：[Gur Sannikov embedded engineering workflow](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

## MCP 服务器

| 服务器 | 用途 |
|-------|------|
| **Serena** | 索引 + 会话记忆 + 符号搜索 |
| **grepai** | 语义搜索 + 调用图分析 |
| **Context7** | 库文档查询 |
| **Sequential** | 结构化推理 |
| **Playwright** | 浏览器自动化 |
| **Postgres** | 数据库查询 |
| **doobidoo** | 语义记忆 + 多客户端 + 知识图谱 |

**Serena 记忆**：`write_memory()` / `read_memory()` / `list_memories()`

**Serena 索引**：
```bash
# 首次建立索引
uvx --from git+https://github.com/oraios/serena serena project index

# 强制重建
serena project index --force-full

# 增量更新（更快）
serena project index --incremental --parallel 4
```

查看状态：`/mcp`

---

## 创建自定义组件

### 智能体（Agent）（`.claude/agents/my-agent.md`）
```yaml
---
name: my-agent
description: Use when [trigger]
model: sonnet
tools: Read, Write, Edit, Bash
---
# 指令写在这里
```

### 技能 — 可被用户调用（`.claude/skills/my-command/SKILL.md`）
```markdown
---
description: Brief description
argument-hint: "<required_arg> [--flag]"
disable-model-invocation: true
---
# 命令名称
具体怎么做...
$ARGUMENTS[0] $ARGUMENTS[1]（或 $0 $1）— 用户传入的参数
```

### 钩子（Hook）（macOS/Linux: `.sh` | Windows: `.ps1`）

**Bash**（macOS/Linux）：
```bash
#!/bin/bash
INPUT=$(cat)
# 处理 JSON 输入
exit 0  # 0=继续，2=阻止
```

**PowerShell**（Windows）：
```powershell
$input = [Console]::In.ReadToEnd() | ConvertFrom-Json
# 处理 JSON 输入
exit 0  # 0=继续，2=阻止
```

---

## 反模式

| ❌ 不要 | ✅ 要 |
|--------|-------|
| 模糊的提示词 | 用 @ 引用明确指定文件 + 行号 |
| 不看就接受 | 逐条读 diff |
| 无视警告 | 70% 就用 `/compact` |
| 跳过权限 | 生产环境绝不这么做 |
| 只给负面约束 | 提供替代方案 |

---

## 快速提示词公式

```
WHAT: [具体交付物]
WHERE: [文件路径]
HOW: [约束条件、实现方式]
VERIFY: [验收标准]
```

**示例：**
```
为登录表单添加输入验证。
WHERE: src/components/LoginForm.tsx
HOW: 使用 Zod 校验，内联显示错误信息
VERIFY: 空邮箱报错，格式错误报错
```

---

## CLI 参数速查

| 参数 | 用法 |
|------|------|
| `-p "query"` | 非交互模式（CI/CD） |
| `-c` / `--continue` | 继续上次会话 |
| `-r` / `--resume <id>` | 恢复指定会话 |
| `--teleport` | 从网页端传送会话 |
| `remote-control` | 子命令：启动远程控制会话 |
| `--model sonnet` | 切换模型 |
| `--add-dir ../lib` | 允许访问工作目录外的路径 |
| `--permission-mode plan` | 计划模式 |
| `--tools "Tool1,Tool2"` | 为本会话启用特定工具 |
| `--max-budget-usd 5.00` | 最大 API 消费上限（打印模式） |
| `--system-prompt "..."` | 追加自定义系统提示词 |
| `--worktree` / `-w` | 在隔离的 git worktree 中运行 |
| `--dangerously-skip-permissions` | 自动接受（谨慎使用） |
| `--debug` | 调试输出 |
| `--allowedTools "Edit,Read"` | 工具白名单 |

> 完整 CLI 参考（~45 个参数）：参见 [cli-reference on code.claude.com](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

## 关键 CLI 子命令

| 命令 | 说明 |
|------|------|
| `claude project purge [path]` | 删除项目所有 Claude Code 状态（对话记录、任务、配置）。`--dry-run` 预览 (v2.1.126) |
| `claude ultrareview [target]` | 非交互式云端代码审查，适用于 CI。`--json` 输出。退出码 0/1 (v2.1.120) |
| `claude plugin prune` | 清理孤儿插件依赖 (v2.1.121) |
| `claude plugin details <name>` | 显示插件清单和 token 费用估算 (v2.1.139) |
| `claude --plugin-url <url>` | 从 URL 加载插件 `.zip`，仅限当前会话 (v2.1.129) |

---

## 调试命令

```bash
claude --version     # 版本号
claude update        # 检查/安装更新
claude doctor        # 诊断
claude --debug       # 详细输出模式
claude --mcp-debug   # MCP 调试
/mcp                 # MCP 状态（Claude 会话内）
```

---

## CI/CD 模式（无头模式）

```bash
# 非交互执行
claude -p "analyze this file" src/api.ts

# JSON 输出
claude -p "review" --output-format json

# 经济模式
claude -p "lint" --model haiku

# 自动接受
claude -p "fix typos" --dangerously-skip-permissions
```

---

## 远程控制 — 移动端访问（v2.1.51+, Research Preview）

> **仅限 Pro/Max** — Team、Enterprise 和 API Key 不可用

```bash
# 从终端启动（新会话）
claude remote-control

# 或在活跃会话中：
/rc        #（或 /remote-control）
```

**从手机/平板/浏览器连接：**
1. 扫描 **二维码**（启动后按空格键显示）
2. 或在浏览器 / Claude 移动应用中打开 **会话 URL**
3. 或：`/mobile` → 显示 App Store + Play Store 链接

| ⚠️ 已知限制 | 说明 |
|------------|------|
| 同时只能 1 个会话 | 同一时间只允许一个远程会话 |
| Slash 命令不能用 | `/new`、`/compact` 等在远程端会变成纯文本 → 请在本地终端执行 |
| 终端必须保持打开 | 关闭本地终端会结束会话 |
| 网络超时 | ~10 分钟断连 → 会话过期 |

**进阶：tmux 多会话**（绕过 1 会话限制）
```bash
tmux new-session -s dev
# 每个窗格 = 独立的 claude 会话
# 在要远程控制的窗格内执行 /rc
```

**自动启用：** `/config` → 切换 "Remote Control: auto-enable"

**完整文档**：[§9.22 远程控制](ultimate-guide.md#922-remote-control-mobile-access) | [安全说明](security/security-hardening.md#remote-control-security)

---

## 任务管理（v2.1.16+）

**两套系统可选：**

| 系统 | 什么时候用 | 持久性 |
|------|-----------|--------|
| **Tasks API**（v2.1.16+） | 跨会话项目、有依赖关系的任务 | ✅ 磁盘（`~/.claude/tasks/`） |
| **TodoWrite**（旧版） | 简单的单次会话 | ❌ 仅限当前会话 |

### Tasks API 命令

```bash
# 启用跨会话持久化
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude

# 在 Claude 内：创建任务层级
> "为认证系统创建任务，包含依赖关系"

# 稍后恢复（新会话）
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude
> "TaskList 查看当前状态"
```

**核心能力：**
- 📁 **持久化**：会话结束、上下文压缩都不丢失
- 🔗 **依赖关系**：任务 A 阻塞任务 B
- 🔄 **多会话**：向多个终端广播状态
- 📊 **状态**：pending → in_progress → completed/failed

**⚠️ 限制**：TaskList 只显示 `id`、`subject`、`status`、`blockedBy`。
要查看 `description` / `metadata` → 逐一调用 `TaskGet(taskId)`。

**小贴士**：把关键信息放在 `subject` 里，方便快速浏览。

**迁移标记**（v2.1.19+）：
```bash
# 回退到旧的 TodoWrite 系统
CLAUDE_CODE_ENABLE_TASKS=false claude
```

**→ 完整工作流**：[guide/workflows/task-management.md](workflows/task-management.md)

---

## 黄金法则

1. **接受前一定看完 diff**
2. **上下文快到危险线（>70%）之前就用 `/compact`**
3. **需求写得越具体越好**（WHAT, WHERE, HOW, VERIFY）
4. **复杂/有风险的任务先走计划模式**
5. **每个项目都创建 `CLAUDE.md`**
6. **每完成一个任务就提交一次**
7. **搞清什么被发出去了** — 提示词、文件、MCP 结果都会发给 Anthropic（可在[设置](https://claude.ai/settings/data-privacy-controls)中选择退出训练）

---

## 快速决策树

```
简单任务       → 直接问 Claude
复杂任务       → 先用 Tasks API 规划
有风险的操作    → 先走计划模式
重复性任务     → 创建智能体或命令
上下文满了     → /compact 或 /clear
需要查文档     → 用 Context7 MCP
深度分析       → 用 Opus（默认开启思考）
```

---

## 常见问题快速修复

| 问题 | 解决方案 |
|------|---------|
| "Command not found" | 检查 PATH，重新安装：`curl -fsSL https://claude.ai/install.sh \| sh` |
| 上下文过高（>70%） | 马上 `/compact` |
| 回复慢 | `/compact` 或 `/clear` |
| MCP 不工作 | `claude mcp list`，检查配置 |
| 权限被拒 | 检查 `settings.local.json` |
| 钩子阻塞 | 检查钩子的退出码，审查逻辑 |

**健康检查脚本**（保存并运行）：
```bash
# macOS/Linux
which claude && claude doctor && claude mcp list

# Windows PowerShell
where.exe claude; claude doctor; claude mcp list
```

---

## 费用优化

| 模型 | 适用场景 | 费用 |
|------|---------|------|
| Haiku | 简单修复、代码审查 | $ |
| Sonnet | 日常开发 | $$ |
| Opus | 架构设计、复杂 Bug | $$$ |
| OpusPlan | 计划（Opus）+ 执行（Sonnet） | $$ |

**小贴士**：用 `--add-dir` 允许工具访问当前工作目录之外的文件

---

## 社区工具

| 工具 | 用途 | 安装方式 |
|------|------|---------|
| **ccusage** | 费用跟踪与报告 | `bunx ccusage daily` |
| **RTK** | token 压缩（60-90%） | `brew install rtk-ai/tap/rtk` 或 `cargo install rtk` · [官网](https://www.rtk-ai.app/) |
| **claude-code-viewer** | 会话历史 UI | `npx @kimuson/claude-code-viewer` |
| **Entire CLI** | 会话检查点 + 治理 | [entire.io](https://entire.io)（2026 年 2 月） |

> **Entire CLI**：由前 GitHub CEO 打造的智能体平台，支持可回退的检查点、审批门禁、审计痕迹。适用于合规场景（SOC2、HIPAA）或多智能体工作流。

---

## 搜索工具速查

快速决策（5 秒）：精确文本 → `rg` | 精确名称 → `rg` / Serena | 概念 → grepai | 结构 → ast-grep

| 任务 | 工具 | 命令 |
|------|------|------|
| "找 TODO 注释" | `rg` | `rg "TODO"` |
| "找认证代码" | `grepai` | `grepai search "authentication"` |
| "谁调用了 login？" | `grepai` | `grepai trace callers "login"` |
| "查看文件结构" | `Serena` | `serena get_symbols_overview` |
| "没写 try/catch 的 async" | `ast-grep` | `ast-grep "async function $F"` |

速度：`rg`（~20ms）→ Serena（~100ms）→ ast-grep（~200ms）→ grepai（~500ms）

> 完整工作流：[workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md)

---

## 资源

- **官方文档**：[docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code)
- **进阶指南**：[Claudelog.com](https://claudelog.com/) — 技巧与模式
- **全文指南**：`ultimate-guide.md`（本仓库）
- **白皮书（FR + EN）**：[cc.bruniaux.com/whitepapers](https://cc.bruniaux.com/whitepapers/) — 10 份专题 PDF
- **项目记忆**：在项目根目录创建 `CLAUDE.md`
- **DeepSeek（高性价比）**：通过 `ANTHROPIC_BASE_URL` 配置

---

**作者**: Florian BRUNIAUX | [@Méthode Aristote](https://methode-aristote.fr) | 写作工具: Claude

*最后更新: 2026 年 5 月 | 版本 3.40.0*
