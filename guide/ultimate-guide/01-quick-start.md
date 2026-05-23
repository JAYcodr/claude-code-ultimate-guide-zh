<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
# 1. 快速入门（第 1 天）

_快速跳转：_ [安装](#11-安装) · [第一个工作流](#12-第一个工作流) · [常用命令](#13-常用命令) · [权限模式](#14-权限模式) · [效率清单](#15-效率清单) · [从其他工具迁移](#16-从其他-ai-编程工具迁移) · [初学者的八个误区](#18-初学者的八个误区及避免方法)

---

**阅读时间**：15 分钟

**技能等级**：初级

**目标**：从零到能干活

> **已经在用 Claude Code？** 跳到 [1.6 迁移指南](#16-从其他-ai-编程工具迁移) 或直接前往 [第 2 章 核心概念](02-core-concepts.md)。

## 1.1 安装

根据你的操作系统选择安装方式：

```C
/*──────────────────────────────────────────────────────────────*/
/* 通用方法                  */ npm install -g @anthropic-ai/claude-code
/*──────────────────────────────────────────────────────────────*/
/* Windows (CMD)             */ npm install -g @anthropic-ai/claude-code
/* Windows (PowerShell)      */ irm https://claude.ai/install.ps1 | iex
/*──────────────────────────────────────────────────────────────*/
/* macOS (npm)               */ npm install -g @anthropic-ai/claude-code
/* macOS (Homebrew)          */ brew install claude-code
/* macOS (Shell Script)      */ curl -fsSL https://claude.ai/install.sh | sh
/*──────────────────────────────────────────────────────────────*/
/* Linux (npm)               */ npm install -g @anthropic-ai/claude-code
/* Linux (Shell Script)      */ curl -fsSL https://claude.ai/install.sh | sh
```

### 验证安装

```bash
claude --version
```

### 更新 Claude Code

保持 Claude Code 最新，以获取最新功能、修复和模型改进：

```bash
# 检查可用更新
claude update

# 或通过 npm 更新
npm update -g @anthropic-ai/claude-code

# 验证更新
claude --version

# 更新后检查系统健康状态
claude doctor
```

**可用的维护命令：**

| 命令 | 用途 | 何时使用 |
|---------|---------|-------------|
| `claude update` | 检查并安装更新 | 每周一次，或遇到问题时 |
| `claude doctor` | 验证自动更新健康状态 | 系统变更后，或更新失败时 |
| `claude --version` | 显示当前版本 | 报告 bug 前 |
| `claude auth login` | 命令行登录认证 | CI/CD、devcontainer、脚本化部署 |
| `claude auth status` | 检查当前认证状态 | 验证正在使用哪个账号/方式 |
| `claude auth logout` | 清除已保存的凭据 | 共享机器、安全清理 |

**更新频率建议：**
- **每周**：在正常开发中检查更新
- **重大工作前**：确保拥有最新功能和修复
- **系统变更后**：运行 `claude doctor` 验证健康状态
- **出现异常行为时**：先更新，再排查

### 桌面应用：无需终端的 Claude Code

Claude Code 有两种形态：CLI（本指南重点）和 Claude 桌面应用的 **Code 标签页**。底层引擎相同，图形界面替代终端。支持 macOS 和 Windows，无需安装 Node.js。

**桌面版在标准 Claude Code 之上的新增功能：**

| 功能 | 说明 |
|---------|---------|
| 可视化 diff 审查 | 在接受前内联查看文件变更并添加评论 |
| 实时应用预览 | Claude 启动你的开发服务器，打开嵌入式浏览器，自动验证变更 |
| GitHub PR 监控 | 自动修复 CI 失败，检查通过后自动合并 |
| 并行会话 | 侧边栏中多个会话，每个自动使用 Git worktree 隔离 |
| 连接器 | GitHub、Slack、Linear、Notion — GUI 配置，无需手动 MCP 配置 |
| 文件附件 | 直接将图片和 PDF 附加到提示中 |
| 远程会话 | 在 Anthropic 云端运行长任务，关闭应用后继续 |
| SSH 会话 | 连接远程机器、云 VM、开发容器 |

**何时选桌面版 vs CLI：**

| 场景选桌面版 | 场景选 CLI |
|--------------------|-----------------|
| 想要可视化 diff 审查 | 需要脚本和自动化（`--print`、输出管道） |
| 带同事上手 | 使用第三方提供商（Bedrock、Vertex、Foundry） |
| 想要侧边栏管理会话 | 需要 `dontAsk` 权限模式 |
| 做直播演示或结对审查 | 需要 Agent 团队 / 多智能体编排 |
| 想要文件附件（图片、PDF） | 使用 Linux（桌面版仅 macOS + Windows） |

**桌面版不支持的**（仅 CLI）：第三方 API 提供商、脚本标志（`--print`、`--output-format`）、`--allowedTools`/`--disallowedTools`、Agent 团队、`--verbose`、Linux。

**共享配置**：桌面版和 CLI 读取相同的文件——CLAUDE.md、MCP 服务器（通过 `~/.claude.json` 或 `.mcp.json`）、钩子、技能和设置。你的 CLI 配置直接继承。

> **迁移小技巧**：在终端中运行 `/desktop` 可将活动中的 CLI 会话移至桌面应用。仅限 macOS 和 Windows。

> **关于 MCP 服务器**：在 `claude_desktop_config.json`（Chat 标签页）中配置的 MCP 服务器与 Claude Code 是分开的。要在 Code 标签页中使用 MCP 服务器，请在 `~/.claude.json` 或项目的 `.mcp.json` 中配置。参见 [第 8.1 节 — MCP](08-mcp-servers.md#81-什么是-mcp)。

> **完整文档**：[code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop)

---

### 各平台路径

| 平台 | 全局配置路径 | Shell 配置 |
|----------|-------------------|--------------|
| **macOS/Linux** | `~/.claude/` | `~/.zshrc` 或 `~/.bashrc` |
| **Windows** | `%USERPROFILE%\.claude\` | PowerShell profile |

> **Windows 用户**：本指南中看到 `~/.claude/` 时，请用 `%USERPROFILE%\.claude\` 或 `C:\Users\你的用户名\.claude\` 代替。

### 首次启动

```bash
cd your-project
claude
```

首次启动时：

1. 系统会提示你使用 Anthropic 账号进行认证
2. 接受服务条款
3. Claude Code 将索引你的项目（大型代码库可能需要数秒）

> **注意**：Claude Code 需要有效的 Anthropic 订阅。请访问 [claude.com/pricing](https://claude.com/pricing) 查看当前方案和 token 限制。

## 1.2 第一个工作流

我们一起修一个 bug。这演示了核心交互循环。

### 第一步：描述问题

```
你：登录函数有一个 bug——用户无法使用含加号的邮箱地址登录
```

### 第二步：Claude 分析

Claude 会：
- 在代码库中搜索相关文件
- 读取登录相关代码
- 定位问题
- 提出修复方案

### 第三步：审查 diff

```diff
- const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
+ const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
```

💡 **关键**：接受前务必阅读 diff。这是你的安全网。

### 第四步：接受或拒绝

- 按 `y` 接受更改
- 按 `n` 拒绝并要求其他方案
- 按 `e` 手动编辑更改

### 第五步：验证

```
你：运行测试看看能否通过
```

Claude 会运行你的测试套件并报告结果。

### 第六步：提交（可选）

```
你：提交这个修复
```

Claude 会用一条合适的消息创建 commit。

## 1.3 常用命令

以下 7 个是我最常用的命令：

| 命令 | 作用 | 何时使用 |
|---------|--------|-------------|
| `/help` | 显示所有命令 | 迷失方向时 |
| `/clear` | 清空对话 | 重新开始 |
| `/compact` | 压缩上下文 | 上下文快不够用了 |
| `/status` | 显示会话信息 | 检查上下文使用量 |
| `/exit` 或 `Ctrl+D` | 退出 Claude Code | 工作结束 |
| `/plan` | 进入计划模式 | 安全探索 |
| `/rewind` | 撤销更改 | 犯了错 |
| `/voice` | 切换语音输入 | 说话代替打字 |

### 快速操作与快捷键

| 快捷键 | 作用 | 示例 |
|----------|--------|---------|
| `!command` | 直接运行 shell 命令 | `!git status`、`!npm test` |
| `@file.ts` | 引用特定文件 | `@src/app.tsx`、`@README.md` |
| `Ctrl+C` | 取消当前操作 | 停止长时间运行的分析 |
| `Ctrl+R` | 搜索命令历史 | 查找之前的提示 |
| `Esc` | 让 Claude 立即停下 | 中断当前操作 |

#### Shell 命令 `!`

无需让 Claude 代劳，直接执行命令：

```bash
# 快速状态检查
!git status
!npm run test
!docker ps

# 查看日志
!tail -f logs/app.log
!cat package.json

# 快速搜索
!grep -r "TODO" src/
!find . -name "*.test.ts"
```

**什么时候用 `!`，什么时候交给 Claude：**

| `!` 适合... | 交给 Claude 适合... |
|----------------|-------------------|
| 快速状态检查（`!git status`） | 需要决策的 Git 操作 |
| 查看命令（`!cat`、`!ls`） | 文件分析和理解 |
| 已经知道的命令 | 复杂的命令构造 |
| 终端中的快速迭代 | 不确定的命令 |

**示例工作流：**
```
你：!git status
输出：显示 5 个已修改文件

你：用约定式 commit 格式提交这些更改
Claude：[分析文件，建议 commit 消息]
```

#### 文件引用 `@`

在提示中引用特定文件，进行精准操作：

```bash
# 单个文件
检查 @src/auth/login.tsx 的安全问题

# 多个文件
重构 @src/utils/validation.ts 和 @src/utils/helpers.ts，消除重复

# 通配符（某些上下文支持）
分析所有测试文件 @src/**/*.test.ts

# 相对路径也可以
查看 @./CLAUDE.md 的项目约定
```

**为什么用 `@`：**
- **精准**：直接定位文件，不用让 Claude 搜索
- **速度**：跳过文件发现阶段
- **上下文**：提示 Claude 按需读取这些文件
- **清晰**：让意图一目了然

**示例：**
```
# 不用 @
你：修复认证 bug
Claude：哪个文件包含认证逻辑？[浪费时间搜索]

# 用 @
你：修复 @src/auth/middleware.ts 中的认证 bug
Claude：[按需读取文件并提出修复]
```

#### 使用图片和截图

Claude Code 支持**直接输入图片**进行视觉分析、设计稿实现和设计反馈。

**如何使用图片：**

1. **直接在终端粘贴**（macOS/Linux/Windows 现代终端）：
   - 将截图或图片复制到剪贴板（macOS 用 `Cmd+Shift+4`，Windows 用 `Win+Shift+S`）
   - 在 Claude Code 会话中用 `Cmd+V` / `Ctrl+V` 粘贴
   - Claude 收到图片后可以分析

2. **拖放**（部分终端）：
   - 将图片文件拖入终端窗口
   - Claude 加载并处理图片

3. **通过路径引用**：
   ```bash
   分析这个设计稿：/path/to/design.png
   ```

**常见用例：**

```bash
# 根据设计稿实现 UI
你：[粘贴 Figma 设计截图]
用 React + Tailwind CSS 实现这个登录界面

# 调试视觉问题
你：[粘贴布局错乱的截图]
按钮没有对齐。修一下 CSS。

# 分析图表
你：[粘贴架构图]
解释这个系统架构，找出潜在瓶颈

# 把白板草图变成代码
你：[粘贴白板算法的照片]
把这个算法转换成 Python 代码

# 无障碍审计
你：[粘贴 UI 截图]
检查这个界面是否有 WCAG 2.1 合规问题
```

**支持的格式**：PNG、JPG、JPEG、WebP、GIF（静态）

**最佳实践：**
- **高对比度**：确保文字/图表清晰可见
- **裁剪相关部分**：去掉不必要的 UI 元素，聚焦分析
- **必要时标注**：圈出或高亮你希望 Claude 关注的具体区域
- **配合文字**："重点关注头部区域"能提供额外上下文

**示例工作流：**
```
你：[粘贴浏览器控制台中的错误截图]
用户点击提交按钮时出现这个错误。排查一下。

Claude：我看到错误是 "TypeError: Cannot read property 'value' of null"。
这说明表单字段的引用有问题。让我检查一下你的表单处理代码...
[读取相关文件并提出修复]
```

**限制：**
- 图片消耗大量上下文 token（约等于 1000-2000 个单词的文字）
- 粘贴图片后用 `/status` 监控上下文用量
- 上下文紧张时，考虑用文字描述复杂图表
- 部分终端可能不支持剪贴板图片粘贴（备用方案：保存文件然后引用路径）

> **💡 小技巧**：给错误消息、设计稿和文档截图，而不是用文字描述。视觉输入通常比文字描述更快、更准确。

##### AI 开发线框图工具

在开始实现之前设计 UI 时，低保真线框图可以帮助 Claude 理解意图，而不会过度约束输出。以下是推荐的工具：

| 工具 | 类型 | 价格 | MCP 支持 | 最擅长 |
|------|------|-------|-------------|----------|
| **Excalidraw** | 手绘风格 | 免费 | ✓ 社区 | 快速线框图、架构图 |
| **tldraw** | 极简画布 | 免费 | 发展中 | 实时协作、自定义集成 |
| **Pencil** | IDE 原生画布 | 免费* | ✓ 原生 | Claude Code 集成、AI 智能体、基于 Git |
| **Frame0** | 低保真 + AI | 免费 | ✓ | 现代 Balsamiq 替代品、AI 辅助 |
| **纸质草图** | 实体 | 免费 | 无 | 最快迭代、零配置 |

**Excalidraw** (excalidraw.com)：
- 开源，手绘风格减少过度设计
- MCP 可用：`github.com/yctimlin/mcp_excalidraw`
- 导出：推荐 PNG（1000-1200px），也支持 SVG/JSON
- 最适合：架构图、快速 UI 草图

**tldraw** (tldraw.com)：
- 无限画布，极简 UI，SDK 优秀
- 提供 Agent 入门套件，用于构建 AI 集成工具
- 导出：JSON 原生，PNG 截图
- 最适合：协作式线框图、嵌入自定义工具

**Frame0** (frame0.app)：
- 现代 Balsamiq 替代品（2025），离线优先桌面应用
- 内置 AI：文本转线框图、截图转线框图
- 原生 MCP 集成 Claude 工作流
- 最适合：需要 AI 辅助低保真线框图的团队

**Pencil** (pencil.dev)：
- IDE 原生无限画布（Cursor/VSCode/Claude Code）
- AI 多人智能体并行运行，支持协作设计
- 格式：`.pen` JSON，支持 git 分支和合并
- MCP：双向读写设计文件
- 创始人 Tom Krcha（前 Adobe XD），a16z Speedrun 投资
- 导出：`.pen` JSON 原生、PNG 截图、Figma 导入（复制粘贴）
- 最适合：工程师-设计师，想用"设计即代码"范式的团队，基于 Cursor/Claude Code 工作流

**⚠️ 注意**：2026 年 1 月发布，增长强劲（100 万+ 浏览，FAANG 采用）但仍处于成长期。目前免费；定价模式待定。推荐愿意快速迭代的早期采用者尝试。

**纸质 + 拍照**：
- 真的，这效果出奇得好
- 用手机拍一张照片 → 直接在 Claude Code 中粘贴
- 技巧：光线充足、裁剪紧凑、避免反光和阴影
- Claude 对旋转和手绘图画处理得很好

**推荐导出设置**：PNG 格式，最长边 1000-1200px，高对比度

##### Figma MCP 集成

Figma 提供了**官方 MCP 服务器**（2025 年宣布），让 Claude 直接访问你的设计文件，相比纯截图大幅减少 token 消耗。

**配置方式：**

```bash
# 远程 MCP（所有 Figma 方案，任何机器）
claude mcp add --transport http figma https://mcp.figma.com/mcp

# 桌面 MCP（需要 Figma 桌面版 + Dev Mode）
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
```

**Figma MCP 提供的工具：**

| 工具 | 用途 | Token |
|------|---------|--------|
| `get_design_context` | 从 frame 提取 React+Tailwind 结构 | 低 |
| `get_variable_defs` | 获取设计 token（颜色、间距、排版） | 非常低 |
| `get_code_connect_map` | 将 Figma 组件映射到你的代码库 | 低 |
| `get_screenshot` | 捕获 frame 的视觉截图 | 高 |
| `get_metadata` | 返回节点属性、ID、位置 | 非常低 |

**为什么用 Figma MCP 而不是截图？**
- **节省 3-10 倍 token**：结构化数据 vs 图片分析
- **直接获取 token**：颜色、间距值直接提取，而非人工解读
- **组件映射**：Code Connect 将 Figma 链接到实际代码文件
- **可迭代工作流**：小修改不需要重新截图

**推荐工作流：**
```
1. get_metadata          → 了解整体结构
2. get_design_context    → 获取特定 frame 的组件层级
3. get_variable_defs     → 每个项目提取一次设计 token
4. get_screenshot        → 只在需要视觉参考时使用
```

**示例会话：**
```bash
你：根据 Figma 实现仪表盘头部
Claude：[调用 header frame 的 get_design_context]
→ 返回：React 结构 + Tailwind class、精确间距
Claude：[调用 get_variable_defs]
→ 返回：--color-primary: #3B82F6, --spacing-md: 16px
Claude：[精确匹配 Figma 实现组件]
```

**前置条件：**
- Figma 账号（免费版支持远程 MCP）
- 桌面 MCP 功能需要 Dev Mode 席位
- 设计文件必须对你的账号可访问

**MCP 配置文件**（`examples/mcp-configs/figma.json`）：
```json
{
  "mcpServers": {
    "figma": {
      "transport": "http",
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

##### Claude 视觉识别的图片优化

了解 Claude 的图片处理方式有助于优化速度和准确性。

**分辨率指南：**

| 范围 | 效果 |
|-------|--------|
| **< 200px** | 精度丢失，文字不可读 |
| **200-1000px** | 大多数线框图的最佳区间 |
| **1000-1568px** | 质量/token 平衡最佳 |
| **1568-8000px** | 自动降采样（浪费上传时间） |
| **> 8000px** | API 拒绝 |

**Token 计算**：`(宽 × 高) / 750 ≈ 消耗的 token`

| 图片尺寸 | 大约 Token |
|------------|-------------------|
| 200×200 | ~54 |
| 500×500 | ~334 |
| 1000×1000 | ~1,334 |
| 1568×1568 | ~3,279 |

**格式建议：**

| 格式 | 适用场景 |
|--------|----------|
| **PNG** | 线框图、图表、文字、清晰线条 |
| **WebP** | 普通截图，压缩效果好 |
| **JPEG** | 仅限照片——压缩失真影响线条检测 |
| **GIF** | 避免（仅静态，画质差） |

**优化检查清单：**
- [ ] 裁剪到只有相关区域
- [ ] 如果大于 1000-1200px 则缩小
- [ ] 线框图/图表用 PNG
- [ ] 粘贴后用 `/status` 检查上下文使用量
- [ ] 上下文超过 70% 时考虑用文字描述

> **💡 Token 提示**：一张 1000×1000 的线框图用 ~1,334 token。相同信息的结构化文本（通过 Figma MCP）可能只用 200-400 token。视觉上下文用截图，实现用结构化数据。

#### 会话续传与恢复

Claude Code 允许你在终端会话之间**继续之前的对话**，保持完整的上下文和对话历史。

**两种恢复方式：**

1. **继续上次会话**（`--continue` 或 `-c`）：
   ```bash
   # 自动恢复最近一次对话
   claude --continue
   # 简写
   claude -c
   ```

2. **恢复指定会话**（`--resume <id>` 或 `-r <id>`）：
   ```bash
   # 通过 ID 恢复指定会话
   claude --resume abc123def
   # 简写
   claude -r abc123def
   ```

3. **关联 GitHub PR**（`--from-pr <number>`，v2.1.49+）：
   ```bash
   # 启动与特定 PR 关联的会话
   claude --from-pr 123

   # 在 Claude 会话中通过 gh pr create 创建的会话
   # 会自动关联到该 PR——用 --from-pr 恢复
   gh pr create --title "Add auth" --body "..."
   # 之后：
   claude --from-pr 123  # 恢复与此 PR 相关的会话上下文
   ```

   用于在某个 PR 的上下文中"从哪里停的从哪里继续"，不用记 session ID。

**查找会话 ID：**

```bash
# 原生：交互式会话选择器
claude --resume

# 原生：通过 Serena MCP 列出（如已配置）
claude mcp call serena list_sessions

# 推荐：快速搜索，附带可直接使用的恢复命令
# 参见 examples/scripts/session-search.sh（bash，零依赖，15ms 列表，400ms 搜索）
# 参见 examples/scripts/cc-sessions.py（Python，增量索引，部分恢复，分支筛选）
cs                    # 列出最近 10 个会话
cs "authentication"   # 全文搜索所有会话

# 退出时也会显示会话 ID
你：/exit
Session ID: abc123def（已保存，可恢复）
```

> **会话搜索工具**：快速搜索请查看 [session-search.sh](../examples/scripts/session-search.sh)（bash，轻量）和 [cc-sessions.py](../examples/scripts/cc-sessions.py)（Python，高级功能：增量索引、部分 ID 恢复、分支筛选、`discover` 自动化模式分析——[GitHub](https://github.com/FlorianBruniaux/cc-sessions)）。另见：[可观测性指南](../ops/observability.md#会话搜索与恢复)。

**常见使用场景：**

| 场景 | 命令 | 为什么 |
|----------|---------|-----|
| 工作中断 | `claude -c` | 从停下的地方继续 |
| 跨天功能开发 | `claude -r abc123` | 跨越数天继续复杂任务 |
| 开会/休息后 | `claude -c` | 不丢失上下文继续 |
| 并行项目 | `claude -r <id>` | 在不同项目上下文之间切换 |
| 代码审查跟进 | `claude -r <id>` | 在原始上下文中处理审查意见 |

**示例工作流：**

```bash
# 第 1 天：开始实现认证功能
cd ~/project
claude
你：用 refresh token 实现 JWT 认证
Claude：[分析和初始实现]
你：/exit
Session ID: auth-feature-xyz（27% 上下文已用）

# 第 2 天：继续工作
cd ~/project
claude --continue
Claude：正在恢复会话 auth-feature-xyz...
你：在认证接口上加限流
Claude：[带着第 1 天的完整上下文继续]
```

**最佳实践：**

- **正确使用 `/exit`**：始终用 `/exit` 或 `Ctrl+D` 退出（不要强杀），确保会话被保存
- **描述性的最后消息**：结束会话时留点上下文（"已准备好测试"），恢复时能想起状态
- **主动管理上下文**：用 `/status` 监控，遵循经过验证的阈值：
  - **< 70%**：最佳——完整的推理能力
  - **75%**：手动 `/compact` 的好时机——在质量下降之前
  - **85%**：自动压缩区间——Claude Code 会在剩余上下文低于固定缓冲（窗口的约 6-7%）时自动压缩。建议在此之前手动交接（[研究依据](../core/architecture.md#自动压缩)）
  - **95%**：强制交接——质量严重下降，立即重置
- **会话命名**：用 `/rename` 给会话起个描述性的名字——并行运行多个会话时至关重要（参见下面的[自动重命名](#会话自动重命名)）

**恢复 vs 重新开始：**

| 应该恢复... | 应该重新开始... |
|-------------------|---------------------|
| 继续某个功能/任务时 | 切换到不相关的工作时 |
| 基于之前的决策继续时 | 之前的会话跑偏了时 |
| 上下文仍然相关（< 75%）时 | 上下文膨胀（> 85%）时 |
| 多步骤实现进行中时 | 快速的一次性问题时 |

**限制：**

- 会话存储在本地（不会跨机器同步）
- 很老的会话可能被清理（取决于本地存储限制）
- 损坏的会话无法恢复（用 `/clear` 重新开始）
- 不同模型或 MCP 配置启动的会话无法恢复

**上下文保留：**

恢复时，Claude 保留：
- ✅ 完整的对话历史
- ✅ 之前读取/编辑过的文件
- ✅ CLAUDE.md 和项目设置
- ✅ MCP 服务器状态（如果使用了 Serena）
- ✅ 未提交代码变更的感知

**结合 MCP Serena 使用：**

用于高级会话管理，带项目记忆和符号追踪：

```bash
# 为项目初始化 Serena 记忆
claude mcp call serena initialize_session

# 在全会话持久化状态下工作
你：实现用户认证
Claude：[用 Serena 追踪符号和上下文工作]

# 退出，之后在项目记忆完整的情况下恢复
claude -c
Claude：[带着 Serena 持久化的项目理解恢复]
```

> **💡 小技巧**：在活跃项目中，把 `claude -c` 作为默认启动方式。这样除非你明确想要全新的开始（用 `claude` 不加参数），否则永远不会丢失之前会话的上下文。

> **来源**：[DeepTo Claude Code Guide - Context Resume Functions](https://cc.deeptoai.com/docs/en/best-practices/claude-code-comprehensive-guide)

### 会话模式发现（cc-sessions discover）{#session-pattern-discovery}

你的会话历史是一个数据源。每次你让 Claude 在多个会话中做同一类事情，就是一个信号：把它提取成技能、命令或 CLAUDE.md 规则，不要再为每次请求支付上下文税。

`cc-sessions discover` 自动完成这个分析。它读取你的会话历史，找出用户消息中的重复模式，并告诉你应该提取什么。

**安装：**

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/cc-sessions/main/cc-sessions \
  -o ~/.local/bin/cc-sessions && chmod +x ~/.local/bin/cc-sessions
```

**两种模式：**

| 模式 | 方式 | 成本 | 速度 |
|------|-----|------|-------|
| N-gram（默认） | 对消息分词，构建 3-6 词短语的频率索引 | 免费，本地 | 12 个项目约 3s |
| `--llm` | 去重消息，批量发送 `claude --print` | 使用你的订阅 | 约 15s |

```bash
# N-gram 模式：所有项目，最近 90 天
cc-sessions --all discover

# 更低阈值，更窄时间窗口
cc-sessions --all discover --since 60d --min-count 2 --top 15

# 通过 claude --print 进行语义分析
cc-sessions --all discover --llm

# JSON 输出用于脚本
cc-sessions --all discover --json | jq '.[] | select(.category == "skill")'
```

**输出示例：**

```
  cc-sessions discover — 847 个会话 · 12 个项目 · 最近 90 天

  📋  CLAUDE.md RULE
  ────────────────────────────────────────────────────────────
  实现前先写测试
     234 个会话 (28%) · 891 次出现 · 得分 0.416
     → 3a72f1c4-...

  🧩  SKILL
  ────────────────────────────────────────────────────────────
  安全审查认证流程
     71 个会话 (8%) · 203 次出现 · 得分 0.084
     → 9f1c3a22-...

  ⚡  COMMAND
  ────────────────────────────────────────────────────────────
  生成 prisma migration 回滚脚本
     18 个会话 (2%) · 44 次出现 · 得分 0.021
     → 44aab71c-...
```

**评分内置的 20% 规则**：超过 20% 会话的模式成为 `CLAUDE.md rule`（始终加载），5-20% 成为 `skill`（按需加载），低于 5% 成为 `command`（显式调用）。跨项目加成（1.5×）优先考虑跨多个代码库重复出现的模式——即使频率较低也值得提取。

参见 [§5.1 理解技能](05-skills.md#51-理解技能) 了解 CLAUDE.md 规则、技能和命令之间的区别，以及 [20% 规则](#the-20-rule) 的决策框架。

**GitHub**：[FlorianBruniaux/cc-sessions](https://github.com/FlorianBruniaux/cc-sessions)

### 会话自动重命名

当你在多个终端/WebStorm 标签/并行工作流中同时运行多个 Claude Code 会话时，`/resume` 选择器只显示时间戳或截断后的第一条提示——根本无法一眼区分。

两种互补方法解决这个问题。可以单独使用，也可以一起使用。

#### 方法 A：CLAUDE.md 行为指令（会话中）

在 `~/.claude/CLAUDE.md` 中加入行为指令，让 Claude 在 2-3 次对话后自动调用 `/rename`。无需工具，适用于所有 IDE 和终端。

```markdown
# Session Naming（自动重命名）

## 预期行为

1. **早期重命名**：一旦会话的主要主题清晰（2-3 次对话后），
   用简短描述性标题执行 `/rename`（不超过 50 个字符）
2. **会话结束时更新**：如果范围发生了重大变化，在关闭前提议改个标题

## 标题格式

`[动作] [主题]` — 示例：
- "fix whitepaper PDF build"
- "add auth middleware + tests"
- "refactor hook system"
- "update CC releases v2.2.0"

## 规则

- 最多 50 字，不加 "Session:" 前缀，不加日期
- 动宾结构（fix、add、refactor、update、research、debug...）
- 多主题：只写主要主题，不列清单
- 早期重命名不用请求确认（直接执行）
```

这在活动会话中效果很好，但取决于 Claude 是否能一致地遵循指令。

#### 方法 B：SessionEnd 钩子（自动，AI 生成）

`SessionEnd` 钩子直接从 `~/.claude/projects/` 读取会话的 JSONL 文件，提取前几条用户消息作为上下文，并调用 `claude -p --model claude-haiku-4-5-20251001` 生成 4-6 个词的描述性标题。如果 Haiku 不可用，则退回到第一条消息的净化版本。

该钩子同时更新 `sessions-index.jsonl`（用于自定义会话浏览器）和 JSONL 文件中的 slug 字段（用于原生 `/resume` 兼容）。

```json
// .claude/settings.json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/auto-rename-session.sh"
          }
        ]
      }
    ]
  }
}
```

前置条件：`claude` CLI 在 PATH 中，`python3` 用于 JSON 解析。设置 `SESSION_AUTORENAME=0` 可对特定会话禁用。

会话结束后，`/resume` 选择器显示的是 `"fix auth middleware"` 而不是 `"2026-03-04T14:23..."`。

#### 两者一起用

两种方法处理会话生命周期中的不同时刻。方法 A 在早期重命名，让会话在运行时就可识别。方法 B 在结束时用反映完整会话范围的标题重命名，可能会覆盖会话中的名称，使其更精确。

**限制（两种方法）**：WebStorm 和 iTerm2 中的终端标签页名称不受影响。JetBrains 会过滤 ANSI 转义序列。重命名的是 Claude 会话，不是 OS 标签页。

> 完整模板：`examples/claude-md/session-naming.md`
> 钩子模板：`examples/hooks/bash/auto-rename-session.sh`

## 1.4 权限模式

Claude Code 有五种权限模式，控制 Claude 的自主程度：

### 默认模式

Claude 在执行以下操作前需要询问权限：
- 编辑文件
- 运行命令
- 提交 commit

这是学习中最安全的模式。

### 自动接受模式（`acceptEdits`）

```
你：在本会话中开启自动接受
```

Claude 自动批准文件编辑，但仍要求 shell 命令的权限。当你信任编辑内容并想要速度时使用。

⚠️ **警告**：仅在定义明确、可逆的操作中使用自动接受。

### 计划模式

```
/plan
```

Claude 只能读取和分析，不允许修改。适用于：
- 理解不熟悉的代码
- 探索架构选项
- 在更改之前安全地调查

准备好做出更改时用 `/execute` 退出。

### 不询问模式（`dontAsk`）

自动拒绝工具调用，除非通过 `/permissions` 或 `permissions.allow` 规则预先批准。Claude 不会用权限提示打断你：如果工具没有明确允许，就静默拒绝。

适用于限制性工作流——你想严格控制哪些工具可以运行，又不需要交互式确认。

### 自动模式（Max 订阅用户，v2.1.114+）

自动模式让 Claude 在执行长时间任务时替你做出权限决策。Claude 不再因为每次有风险的操作需要批准而停下，而是运用自己的判断——你审查结果，而不是审批每一步。

```
# 通过 settings.json 启用
{ "permissionMode": "auto" }
```

与 `bypassPermissions`（盲目批准）不同，自动模式使用分类器评估每个操作。当分类器拦截某项操作时，会触发 `PermissionDenied` 钩子，让你了解什么被拒绝了。专为长时间任务设计，中断更少，风险低于跳过所有权限。

**硬拒绝规则**（`settings.autoMode.hard_deny`，v2.1.136）：自动模式的分类器可以用无条件拦截规则补充，这些规则在分类器之前触发，且不能被用户意图或 allow 例外覆盖：

```json
// .claude/settings.json
{
  "autoMode": {
    "hard_deny": [
      { "tool": "Bash", "pattern": "rm -rf" },
      { "tool": "Write", "pathPattern": "/etc/**" },
      { "tool": "Write", "pathPattern": "**/.env" }
    ]
  }
}
```

与分类器规则（权衡用户意图）不同，`hard_deny` 条目是绝对的。用于那些无论上下文如何都绝不能自动批准的操作：生产环境破坏性命令、凭据文件、系统配置路径。

**前置条件**：Max 计划订阅。自 v2.1.114 起可用。

### 绕过权限模式（`bypassPermissions`）

自动批准一切，包括 shell 命令。没有任何权限提示。

⚠️ **警告**：仅在沙箱 CI/CD 环境中使用。从 CLI 启用需要 `--dangerously-skip-permissions`。切勿在生产系统上或与不可信代码一起使用。

**安全不变性——即使在 `bypassPermissions` 模式下，某些路径始终会提示**：

某些写入操作被认为太过敏感，无法在任何配置下自动批准。Claude Code 在修改以下内容前始终会提示：

| 受保护的目标 | 示例 |
|-----------------|---------|
| `.git/` 目录 | 仓库内的 git hooks、refs、config |
| `.claude/` 目录 | agents、skills、hooks、settings——除了 `.claude/worktrees/` |
| Shell 配置文件 | `.bashrc`、`.zshrc`、`.bash_profile`、`.profile` |
| VCS 和工具配置 | `.gitconfig`、`.mcp.json`、`.claude.json` |

在 `settings.json` 或 CLAUDE.md 中定义的特定内容 allow 规则（如 `Bash(npm publish:*)`）在 `bypassPermissions` 模式下仍然生效——它们在所有权限模式之上继续作为额外过滤器。这让你可以构建精确的安全护栏（如"发布 npm 前始终询问"），无论会话如何启动都有效。

### 权限疲劳（反模式）

一个常见的陷阱：你在任务中深入操作，提示不断弹出，你开始不经阅读就批准。这就是**权限疲劳**——它完全违背了权限系统的目的。

解决办法是在开始之前选择合适的模式，而不是一个接一个地点提示：

| 情况 | 正确模式 | 为什么 |
|-----------|-----------|-----|
| 探索性工作，不熟悉的代码库 | 计划模式 | 不会意外修改任何东西 |
| 可信的本地编辑，没有 shell 操作 | `acceptEdits` | 静默批准编辑，仍拦截命令 |
| 长时间智能体任务，Max 计划 | 自动模式 | Claude 自行判断；更少中断，风险低于 bypass |
| 自动化流水线，沙箱环境 | `bypassPermissions` | 完全无提示——但仅在隔离环境中安全 |
| 只需要一个工具自动批准 | 在 CLAUDE.md 中设置 `permissions.allow` | 精细控制，不是全有或全无 |
| 默认新会话 | 默认模式 | 对每个操作显式审查 |

要避免的失败模式：在有 SSH 密钥、API token 或生产访问权限的开发机器上使用 `--dangerously-skip-permissions`。权限系统只有在"你真正阅读正在批准的内容"或配置了与你真实信任级别匹配的模式时才有价值。

## 1.5 效率清单

当你能做到以下事项时，说明你已经准备好进入第 2 天了：

- [ ] 在项目中启动 Claude Code
- [ ] 描述一个任务并审查建议的更改
- [ ] 阅读 diff 后接受或拒绝更改
- [ ] 用 `!` 运行 shell 命令
- [ ] 用 `@` 引用文件
- [ ] 用 `/clear` 重新开始
- [ ] 用 `/status` 检查上下文使用量
- [ ] 用 `/exit` 或 `Ctrl+D` 正确退出

## 1.6 从其他 AI 编程工具迁移

> **最后更新**：2026 年 3 月。AI 编程工具变化很快；请到官网核实定价和功能。

从 GitHub Copilot、Cursor 或其他 AI 助手切换过来？以下是你需要知道的。

### Claude Code 的不同之处

| 功能 | GitHub Copilot | Cursor | Windsurf | Zed | Claude Code |
|---------|---------------|--------|----------|-----|-------------|
| **交互方式** | Agent + Chat + 自动补全 | Agent + Chat + 自动补全 | Cascade agent | Agent panel + Zeta2 | CLI + 对话 |
| **上下文** | 完整代码库（agent 模式） | 代码库感知（Composer） | ~200K token（IDE） | 最多 1M token | 整个项目（agentic） |
| **自主性** | Agent 模式 + coding agent | Agent + Background Agents | Cascade（Cognition AI） | Agent + subagents | 完整任务执行 |
| **自定义** | MCP、自定义 agent、AGENTS.md | MCP Apps、.cursorrules | Cascade hooks | ACP Registry、MCP | Agents、skills、hooks、MCP |
| **MCP 支持** | ✅ GA（自动批准） | ✅ MCP Apps v2.6 | 未记录 | ✅ OAuth | ✅ 原生 |
| **内联自动补全** | ✅ 原生 | ✅ Tab | ✅ Supercomplete | ✅ Zeta2 | ❌ 需搭配使用 |
| **离线/本地** | ❌ | ❌ | ❌ | BYO 提供商 | ❌ |
| **最适合** | IDE 原生、GitHub 团队 | IDE 原生 AI UX | 多智能体 IDE | 速度 + 开源 | 终端/CLI、大型重构 |

#### 价格对比（2026 年 3 月）

| 工具 | 免费 | Pro | Power/Plus | Teams | Enterprise |
|------|------|-----|------------|-------|------------|
| **GitHub Copilot** | ✅（2000 次补全） | $10/月 | Pro+ $39/月 | Business $19/座位 | $39/座位 |
| **Cursor** | ✅（2000 次补全） | $20/月 | Ultra $200/月 | $40/座位 | — |
| **Windsurf** | ✅（25 条提示） | $20/月 | $200/月 | $30/座位 | $60/座位 |
| **Zed** | — | $10/月 | — | — | — |
| **Claude Code** | — | $20/月 | Max $100-200/月 | — | 通过 Anthropic |

**关键思维转变**：Claude Code 是一个**结构化上下文系统**，不是聊天机器人或自动补全工具。你构建的持久上下文（CLAUDE.md、skills、hooks）会随时间增加价值——参见 [§2.5](#25-从聊天机器人到上下文系统)。

### 迁移指南：GitHub Copilot → Claude Code

#### Copilot 的优势

- **内联建议** - 输入时快速自动补全
- **熟悉的工作流** - 在编辑器内工作
- **低摩擦** - 无需上下文切换
- **Agent 模式** - 多文件编辑、终端命令、自主迭代（VS Code + JetBrains GA）
- **免费版** - 每月 0 美元享受 2000 次补全 + 50 次高级请求
- **模型选择** - 自 2026 年 2 月起可选择 Claude、Codex、GPT 模型

#### Claude Code 的优势

- **终端原生工作流** - 不依赖 IDE；可通过 SSH、CI/CD、任何终端工作
- **持久上下文系统** - CLAUDE.md + skills + hooks 随时间累积；Copilot 的自定义指令较新且粒度较粗
- **Agent 编排** - Agent 团队、子 agent、并行执行、确定性多文件协调
- **按使用量付费** - 没有高级请求配额；Copilot agent 模式受每月高级配额限制（Pro 300/月，Pro+ 1500/月）
- **无头/CI 模式** - 可在流水线、自动化、非交互式环境中运行
- **深度自定义** - 自定义 slash 命令、事件钩子、技能模块、MCP 服务器组合

#### 混合使用（推荐）

**Copilot 用于：**
- 输入时快速自动补全
- 样板代码生成
- 简单函数补全
- IDE 中直接的多文件任务（agent 模式）
- 关于可见代码的快速聊天问题

**Claude Code 用于：**
- 跨多个仓库或架构的功能实现
- 需要深入代码库遍历的系统性调试
- CI/CD 自动化和无头执行
- 大规模代码审查和重构
- 理解不熟悉的代码库
- 为整个模块编写测试

**工作流示例：**

```bash
# 上午：用 Claude Code 规划功能
claude
你："我需要添加用户认证。这个代码库的最佳方案是什么？"
# Claude 分析项目，建议架构

# 编码中：用 Copilot 做内联补全
# 在 VS Code 中输入，Copilot 自动补全

# 下午：用 Claude Code 调试
claude
你："移动端登录失败，桌面端正常。排查一下。"
# Claude 系统性地调查

# 下班前：用 Claude Code 审查
claude
你："审查我今天做的更改。检查安全问题。"
# Claude 审查所有修改过的文件
```

### 迁移指南：Cursor → Claude Code

#### Cursor 的优势

- **内联编辑** - 在编辑器中直接修改代码
- **GUI 界面** - 熟悉的 VS Code 体验
- **Chat + 自动补全** - 一个工具中两种模式
- **Agent 模式** - 自主多文件编辑（2026 年 3 月 GA）
- **Background Agents** - 在远程 VM 上委托任务，并行执行

#### Claude Code 的优势

- **终端原生工作流** - 更适合 CLI 重度开发者
- **高级自定义** - Agents、skills、hooks、commands
- **MCP 生态成熟度** - 原生 MCP，更广泛的服务器兼容性和更深度的集成
- **成本透明** - 直接 API 计费，无信用系统或不透明配额
- **Git 集成** - 原生 git 操作，commit 生成
- **CI/CD 集成** - 无头模式用于自动化

#### 什么时候该切换

**继续用 Cursor 如果：**
- 你更偏好 GUI 而非 CLI
- 你想要一体化 IDE 体验
- 你偏好 GUI 优先的工作流 + 集成 agent 模式
- 你不需要高级自定义

**切换到 Claude Code 如果：**
- 你适应终端工作流
- 你想要更深度的自定义（agents、hooks）
- 你处理复杂的多仓库项目
- 你想把 AI 集成到 CI/CD
- 你想要直接 API 计费，没有信用池

#### 两者同时使用

你可以同时使用两个工具：

```bash
# Cursor 用于编辑和快速修改
# 终端中的 Claude Code 用于复杂任务

# 示例工作流：
# 1. 用 Cursor 探索和快速编辑
# 2. 打开终端：claude
# 3. 让 Claude Code："审查我的更改并提出改进建议"
# 4. 在 Cursor 中应用建议
# 5. 用 Claude Code 生成测试
```

### 迁移检查清单

#### 第 1 周：学习阶段

```markdown
□ 完成快速入门（第 1 章）
□ 理解上下文管理（关键！）
□ 尝试 3-5 个小任务（bug 修复、小功能）
□ 学会何时使用 /plan 模式
□ 练习在接受前审查 diff
```

#### 第 2 周：建立工作流

```markdown
□ 创建项目 CLAUDE.md 文件
□ 为常用任务设置 1-2 个自定义命令
□ 配置 MCP 服务器（Serena、Context7）
□ 定义你的混合工作流（何时用 Claude Code vs 其他工具）
□ 追踪成本并根据使用情况优化
```

#### 第 3-4 周：高级使用

```markdown
□ 为专业任务创建自定义 agent
□ 设置自动化钩子（格式化、linting）
□ 如适用，集成到 CI/CD
□ 如果是团队协作，建立团队模式
□ 根据学习结果优化 CLAUDE.md
```

### 常见迁移问题

**问题 1："我怀念内联建议"**

- **解决方案**：继续用 Copilot/Cursor 做自动补全，用 Claude Code 做复杂任务
- **替代方案**：让 Claude 生成代码片段供你粘贴

**问题 2："上下文切换很烦"**

- **解决方案**：使用分屏终端（编辑器在左，Claude Code 在右）
- **小技巧**：设置键盘快捷键切换终端焦点

**问题 3："我不知道什么时候该用哪个工具"**

- **经验法则**：
  - **<5 行代码** → 用 Copilot/自动补全
  - **5-50 行，单个文件** → 哪个工具都行
  - **>50 行或多文件** → 用 Claude Code

**问题 4："Claude Code 比自动补全慢"**

- **客观认识**：Claude Code 解决的问题不同
- **不要对比**：自动补全 vs 完整任务执行
- **优化**：使用具体查询，管理好上下文

**问题 5："成本不可预测"**

- **解决方案**：在 Anthropic Console 中追踪成本
- **预算**：每次会话设个心理预算（$0.10-$0.50）
- **优化**：使用 `/compact`，查询尽量具体

### 过渡策略

**策略 1：渐进式（推荐）**

```
第 1 周：每天用 Claude Code 1-2 次做特定任务
第 2 周：用 Claude Code 做所有调试和审查
第 3 周：用 Claude Code 做功能实现
第 4 周：完整工作流集成
```

**策略 2：一刀切**

```
第 1 天：禁用 Copilot/Cursor，强迫自己只用 Claude Code
第 2-3 天：挫折期（学习曲线）
第 4-7 天：生产力恢复
第 2 周+：完全熟练
```

**策略 3：按任务分配**

```
Claude Code 专门做：
- 所有新功能
- 所有调试
- 所有代码审查

Copilot/Cursor 做：
- 快速编辑
- 自动补全
```

### 衡量成功

**当你满足以下条件时，说明迁移成功：**

- [ ] 遇到复杂任务下意识地去找 Claude Code
- [ ] 不假思索地理解上下文管理
- [ ] 至少创建了 2-3 个自定义命令/agent
- [ ] 能在开始会话前估算成本
- [ ] 相比内联文档，你更喜欢 Claude Code 的解释
- [ ] 已将 Claude Code 融入日常工作流

**主观生产力指标**（你的体验可能不同）：

- 在复杂任务上感觉更高效
- 花在样板代码和调试上的时间减少
- 通过 Claude 审查发现更多问题
- 更好地理解不熟悉的代码

## 1.7 信任校准：何时以及需要验证多少

AI 生成的代码需要**基于风险级别的比例验证**。盲目接受所有输出和偏执地审查每一行都是浪费时间。本节帮助你校准信任度。

### 问题：验证债

研究一致显示 AI 代码的缺陷率高于人类编写的代码：

| 指标 | AI vs 人类 | 来源 |
|--------|-------------|--------|
| 逻辑错误 | 多 1.75× | [ACM 研究，2025](https://dl.acm.org/doi/10.1145/3716848) |
| 安全缺陷 | 45% 包含漏洞 | [Veracode GenAI 报告，2025](https://veracode.com/blog/genai-code-security-report) |
| XSS 漏洞 | 多 2.74× | [CodeRabbit 研究，2025](https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) |
| PR 大小增加 | +18% | [Jellyfish，2025](https://jellyfish.co) |
| 每个 PR 的事故数 | +24% | [Cortex.io，2026](https://cortex.io) |
| 变更失败率 | +30% | [Cortex.io，2026](https://cortex.io) |

**关键见解**：AI 生成代码更快，但验证成为瓶颈。问题不是"它能工作吗？"而是"我怎么知道它能工作？"

> **关于下游可维护性的细微说明**：一项双盲随机对照试验（Borg 等，2025，n=151 名专业开发者）发现，下游开发者在演进 AI 生成代码 vs 人类生成代码所需的时间上无显著差异。上述缺陷率是真实的——但它们不会系统性转化为下一个开发者的更高维护负担。风险范围比通常假设的要窄。（[arXiv:2507.00788](https://arxiv.org/abs/2507.00788)）

### 验证光谱

并非所有代码都需要同样的审查。将验证力度与风险匹配：

| 代码类型 | 验证级别 | 时间投入 | 技术 |
|-----------|-------------------|-----------------|------------|
| **样板代码**（配置、import） | 快速扫一眼 | 10-30 秒 | 瞟一眼，相信结构 |
| **工具函数**（格式化、辅助） | 快速测试 | 1-2 分钟 | 一个快乐路径测试 |
| **业务逻辑** | 深度审查 + 测试 | 5-15 分钟 | 逐行、边界情况 |
| **安全关键**（认证、加密、输入验证） | 最大 + 工具 | 15-30 分钟 | 静态分析、模糊测试、同行评审 |
| **外部集成**（API、数据库） | 集成测试 | 10-20 分钟 | Mock + 真实端点测试 |

### 个人 vs 团队验证

**个人开发者策略：**

没有同行评审时，用以下方式弥补：

1. **高测试覆盖率（>70%）**：你的安全网
2. **Vibe Review**：介于"盲目接受"和"逐行审查"之间的中间层：
   - 阅读 commit 消息 / 摘要
   - 扫一眼 diff 中有没有意外的文件变化
   - 跑测试
   - 在应用中快速做一下冒烟测试
   - 全绿就发布
3. **静态分析工具**：ESLint、SonarQube、Semgrep 捕捉你看漏的
4. **时间箱**：不要在 10 行工具函数上花 30 分钟审查

```
个人工作流：
生成 → Vibe Review → 测试通过？→ 发布
                ↓
        测试失败？→ 深度审查 → 修复
```

**团队策略：**

多人时：

1. **AI 首轮审查**：让 Claude 或 Copilot 先审查（能发现 70-80% 的问题）
2. **人工签字**：AI 审查 ≠ 批准
3. **关键路径找领域专家**：安全代码 → 经安全培训的审查者
4. **轮换审查者**：防止形成盲点

```
团队工作流：
生成 → AI 审查 → 人工审查 → 合并
              ↓              ↓
         标记问题     最终批准
```

### "证明它能工作"检查清单

发布 AI 生成的代码前，验证：

**功能正确性：**
- [ ] 快乐路径正常（手动测试或自动测试）
- [ ] 边界情况已处理（null、空值、边界值）
- [ ] 错误状态优雅处理（不要静默失败）

**安全基线：**
- [ ] 输入验证已做（永远不要信任用户输入）
- [ ] 没有硬编码的密钥（搜索 `password`、`secret`、`key`）
- [ ] 认证/授权检查完好无损（没有绕过现有防护）

**集成合理性：**
- [ ] 现有测试仍然通过
- [ ] diff 中没有意外的文件变化
- [ ] 新增的依赖是合理且已审计的

**代码质量：**
- [ ] 遵循项目约定（命名、结构）
- [ ] 没有明显的性能问题（N+1、内存泄漏）
- [ ] 注释解释"为什么"而不是"是什么"

### 要避免的反模式

| 反模式 | 问题 | 更好的方式 |
|--------------|---------|-----------------|
| **"能编译，发吧"** | 语法 ≠ 正确性 | 至少跑一个测试 |
| **"AI 写的，一定安全"** | AI 优化的是看似合理，而非安全 | 安全关键代码始终手动审查 |
| **"测试过了，好了"** | 测试可能没有覆盖变更 | 检查修改行的测试覆盖率 |
| **"跟上回一样"** | 上下文变了，AI 可能生成不同代码 | 每次生成都是独立的 |
| **"高级工程师写的提示"** | 高级 ≠ 输出质量保证 | 审查输出，而不是输入 |
| **"只是样板代码"** | 样板代码也可能藏问题 | 至少扫一眼有没有意外的东西 |

### 随时间校准

你的验证策略应该持续演进：

1. **开始谨慎**：刚用 Claude Code 时审查所有东西
2. **追踪失败模式**：bug 从哪里溜进来的？
3. **收紧关键路径**：对过去出过事的领域加倍下功夫
4. **放松低风险区域**：在稳定、经过测试的代码类型上多信任 AI 一些
5. **定期审计**：偶尔抽查"被信任"的代码

**心智模型**：把 AI 想象成一个能干的初级开发者。你不会不经审查就部署他们的代码，但也不会重写他们写的一切。

### 综合起来

```
┌─────────────────────────────────────────────────────────┐
│                     信任校准流程                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AI 生成代码                                             │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ 什么类型？    │                                       │
│  └──────────────┘                                       │
│    │    │    │                                          │
│    ▼    ▼    ▼                                          │
│  样板  业务  安全                                        │
│  代码  逻辑  关键                                        │
│    │    │    │                                          │
│    ▼    ▼    ▼                                          │
│  扫一  测试  完整                                        │
│  眼   +     审查                                         │
│       审查  + 工具                                       │
│    │    │    │                                          │
│    └──────┴────────┘                                    │
│            │                                            │
│            ▼                                            │
│    测试通过？─否──► 调试 & 修复                         │
│            │                                            │
│           是                                            │
│            │                                            │
│            ▼                                            │
│        发布                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> "AI 让你写代码更快——确保你不是也在更快地失败。"
> — 改编自 Addy Osmani

**归属**：本节参考了 Addy Osmani 的 ["AI Code Review"](https://addyosmani.com/blog/code-review-ai/)（2026 年 1 月），以及 ACM、Veracode、CodeRabbit 和 Cortex.io 的研究。

## 1.8 初学者的八个误区（及避免方法）

常见陷阱会拖慢 Claude Code 新用户：

### 1. ❌ 跳过计划

**误区**：上来就说"修复这个 bug"而没有说明上下文。

**修复**：使用 WHAT/WHERE/HOW/VERIFY 格式：
```
WHAT：修复登录超时错误
WHERE：src/auth/session.ts
HOW：将 token 过期时间从 1 小时增加到 24 小时
VERIFY：浏览器刷新后登录状态仍然保持
```

### 2. ❌ 忽略上下文限制

**误区**：一直工作到上下文达到 95%，响应质量下降。

**修复**：注意状态栏中的 `Ctx(u):`。70% 时 `/compact`，90% 时 `/clear`。

### 3. ❌ 使用模糊的提示

**误区**："让这段代码更好"或"检查有没有 bug"

**修复**：要具体："重构 `calculateTotal()`，使其在不抛出异常的情况下处理 null 价格"

### 4. ❌ 盲目接受更改

**误区**：不经审查 diff 就按 "y"。

**修复**：始终审查 diff。用 "n" 拒绝，然后说明哪里有问题。

### 5. ❌ 没有版本控制保护

**误区**：不做 commit 就做大规模修改。

**修复**：大改动前先 commit。使用功能分支。Claude 可以帮忙：`/commit`

### 6. ❌ 权限过于宽泛

**误区**：设置 `Bash(*)` 或 `--dangerously-skip-permissions`

**修复**：从限制性开始，需要时再扩大。使用白名单：`Bash(npm test)`、`Bash(git *)`

### 7. ❌ 混合不相关的任务

**误区**："修复认证 bug AND 重构数据库 AND 添加新测试"

**修复**：每次会话只做一个任务。`/clear` 在不同任务之间清空。

**如何为 Claude Code 确定任务大小：**

| 信号 | 太大 | 刚好 | 太小 |
|--------|---------|------------|-----------|
| 描述 | 用"和"连接多个行为 | 一个垂直切片，一个用户行为 | 一个你手动做更快的一行改动 |
| 会话 | 上下文用完或跑偏 | 一个会话内完成 | 只需 30 秒 |
| 审查 | 审查者记不住完整的 diff | diff 能在一次审查中看完 | 不值得审查 |
| 回滚 | 回滚会破坏其他东西 | `git revert` 干净地撤销一切 | 不适用 |

**拆分启发**：如果你的任务描述在"两个用户可见行为"之间用了"和"，就拆开它。"用户可以重置密码"是一个任务。"用户可以重置密码 AND 管理员可以强制过期会话"是两个任务。

> **深入阅读**：[Spec-First 工作流 — 任务粒度](../workflows/spec-first.md#任务粒度为智能体合理划分工作量) 涵盖了垂直切片模式、PRD 质量检查清单和具体的前后对比示例。

### 8. ❌ 把 Claude Code 当聊天机器人用

**误区**：每次会话都临时输入指令。重复项目约定、重新解释架构、手动强制执行质量检查。

**修复**：构建随时间累积的结构化上下文：
- **CLAUDE.md**：你的约定、技术栈和模式——每次会话自动加载
- **Skills**：可重用工作流（`/review`、`/deploy`）确保一致性
- **Hooks**：自动化护栏（lint、安全、格式化）——零手动操作

从第 1 周的 CLAUDE.md 开始。完整框架见 [§2.6 心智模型](#26-从聊天机器人到上下文系统)。

### 快速自查

下次会话前，确认：

- [ ] 我有明确、具体的目标
- [ ] 我的项目有 CLAUDE.md 文件（见 [§2.5](#25-从聊天机器人到上下文系统)）
- [ ] 我在功能分支上（不是 main）
- [ ] 我知道我的上下文使用情况（`/status`）
- [ ] 我会在接受前审查每个 diff

> **小技巧**：收藏第 9.11 节，里面有详细的陷阱解释和解决方案。

---
