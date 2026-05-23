
# 模块 01：安装与设置

**时间**: 15 分钟 | **难度**: ⭐ 入门

## 目标

在你的系统上安装 Claude Code 并让它跑起来。用第一条命令验证是否正常工作。

---

## 你将学到

- 在你的平台安装 Claude Code（macOS / Linux / Windows）
- 理解基本的提示词 → 响应循环
- 运行你的第一个命令
- 使用帮助系统

---

## 安装

### macOS（推荐）

```bash
brew install anthropic/tap/claude-code
```

验证：
```bash
claude --version
```

### Linux

```bash
curl -sSL https://dl.claudecode.com/install.sh | bash
```

验证：
```bash
claude --version
```

### Windows

从 https://dl.claudecode.com/windows 下载安装包，或用：

```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://dl.claudecode.com/install.ps1'))
```

### Docker（任何平台）

```bash
docker run -it anthropic/claude-code:latest
```

---

## 首次运行

进入任意项目目录，启动 Claude：

```bash
cd ~/my-project
claude
```

你会看到：

```
Claude Code v2.x.x ready
Project: ~/my-project (git: main)
Context: 0% · Tokens available: 200,000

Type /help for commands or ask me anything
>
```

---

## 常用命令

| 命令 | 用途 |
|------|------|
| `/help` | 显示所有可用命令 |
| `/status` | 查看上下文用量和会话状态 |
| `/clear` | 从头开始（清空对话历史） |
| `Ctrl+C` | 取消当前操作 |
| `/exit` | 关闭 Claude Code |

---

## 前 5 分钟

### 练习 1：查看可用命令
```bash
/help
```

浏览命令列表。注意：
- **工作流**：`/plan`、`/rewind`、`/think`
- **导航**：`/goto`、`/read`
- **记忆**：启动时加载记忆
- **进阶**：`/model`、`/mode`

### 练习 2：查看会话状态
```bash
/status
```

你会看到：
- 上下文使用占比
- 可用 token 数
- 当前项目
- Git 分支

### 练习 3：问 Claude 一个问题

```
我的项目里有哪些文件？
```

Claude 会读取项目结构并回复。这就是核心循环：

```
你的提示词 → Claude 读取文件 → Claude 建议变更 → 你审查 → 应用
```

### 练习 4：审查一个建议的变更

如果 Claude 建议改代码，你会看到：
1. 变更说明
2. `diff` 视图（加/删了什么）
3. 接受或拒绝的提示

**规则**：接受前一定看完 diff。这是你防止意外变更的保障。

---

## 核心概念：循环

每次交互都遵循这个模式：

```
┌─────────────┐
│ 你提问       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Claude      │
│ 读取文件    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Claude      │
│ 建议变更    │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ 你审查 diff       │
│ 并批准            │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ 变更已应用       │
│ 到你的文件        │
└──────────────────┘
```

---

## 关键概念

### 会话

每次执行 `claude`，你都会开始一个新的**会话**。会话是你和 Claude 的对话，在你使用 Claude Code 期间一直存在。

- 会话默认**不保存**（退出即结束）
- 会话一次**只对一个项目**有效
- 你的上下文会随着提问增多而增长（最多 ~200K tokens）

### 上下文

**上下文**是 Claude 能记住的对话内容量，以百分比显示（0-100%）。

- 0-50%：空间充足，放心干活
- 50-70%：开始精打细算，可以考虑 `/compact`
- 70%+：执行 `/compact` 释放空间
- 90%+：会被强制清理

### Git 感知

Claude Code 是**知道 git 的**。它能：
- 检测你当前所在分支
- 显示未提交的变更
- 帮你提交和审查代码
- 防止意外破坏性变更

---

## 验证：完成本模块的标志

✓ 你能执行 `claude --version` 并看到已安装的版本
✓ 你能在项目中用 `claude` 启动 Claude
✓ 你理解了提示词 → 响应的循环
✓ 你能执行 `/status` 并理解它的输出
✓ 你至少审查过一次 Claude 的 diff

---

## 下一步

学完本模块后，进入**模块 02：核心循环**，了解：
- Claude 如何读取你的项目
- 上下文的工作原理
- 如何写出更有效的请求
- 计划模式与思考模式

**到下一模块的时间**：随时可以开始（只需跑过一次 Claude）

---

## 故障排查

### "claude: command not found"
安装未完成。试试：
- **macOS**：重新执行 `brew install anthropic/tap/claude-code`
- **Linux**：重新执行安装脚本
- **Windows**：从 https://dl.claudecode.com/windows 下载安装包

### "Project not found"
确认你所在的目录包含 `package.json`、`.git` 或其他项目文件。Claude Code 在项目目录中工作效果最好。

### "Permission denied"（macOS）
试试：
```bash
chmod +x /usr/local/bin/claude
```

---

## 资源

- **官方文档**：https://code.claude.com/docs
- **常见问题**：参见 `guide/ultimate-guide.md` 附录 B
- **示例**：本指南的 `examples/` 目录

---

**已完成模块 01？** → 准备进入模块 02：核心循环

