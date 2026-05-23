---
name: rtk-optimizer
description: "用 RTK 包装高输出的 shell 命令以减少 token 消耗。在运行 git log、git diff、cargo test、pytest 或其他浪费上下文窗口 token 的冗长 CLI 输出时使用。"
allowed-tools: Bash
effort: low
metadata:
  version: 1.0.0
---

# RTK 优化器技能

**目的**：自动为高输出命令建议 RTK 包装器以减少 token 消耗。

## 工作原理

1. **检测用户请求中的高输出命令**
2. **建议 RTK 包装器**（如适用）
3. **用户确认后使用 RTK 执行**
4. **跟踪会话中的节省量**

## 支持的命令

### Git（>70% 减少）
- `git log` → `rtk git log`（减少 92.3%）
- `git status` → `rtk git status`（减少 76.0%）
- `find` → `rtk find`（减少 76.3%）

### 中等价值（50-70% 减少）
- `git diff` → `rtk git diff`（减少 55.9%）
- `cat <大文件>` → `rtk read <文件>`（减少 62.5%）

### JS/TS 栈（70-90% 减少）
- `pnpm list` → `rtk pnpm list`（减少 82%）
- `pnpm test` / `vitest run` → `rtk vitest run`（减少 90%）

### Rust 工具链（80-90% 减少）
- `cargo test` → `rtk cargo test`（减少 90%）
- `cargo build` → `rtk cargo build`（减少 80%）
- `cargo clippy` → `rtk cargo clippy`（减少 80%）

### Python & Go（90% 减少）
- `pytest` → `rtk python pytest`（减少 90%）
- `go test` → `rtk go test`（减少 90%）

### GitHub CLI（79-87% 减少）
- `gh pr view` → `rtk gh pr view`（减少 87%）
- `gh pr checks` → `rtk gh pr checks`（减少 79%）

### 文件操作
- `ls` → `rtk ls`（精简输出）
- `grep` → `rtk grep`（筛选输出）

## 激活示例

**用户**："显示 git 历史"
**技能**：检测到 `git log` → 建议 `rtk git log` → 解释 92.3% token 节省

**用户**："查找所有 markdown 文件"
**技能**：检测到 `find` → 建议 `rtk find "*.md" .` → 解释 76.3% 节省

## 安装检查

首次使用前，验证 RTK 已安装：
```bash
rtk --version  # 应输出：rtk 0.16.0+
```

如未安装：
```bash
# Homebrew（macOS/Linux）
brew install rtk-ai/tap/rtk

# Cargo（所有平台）
cargo install rtk
```

## 使用模式

```markdown
# 当用户请求高输出命令时：

1. 确认请求
2. 建议 RTK 优化：
   "我将使用 `rtk git log` 减少约 92% 的 token 使用"
3. 执行 RTK 命令
4. 可选跟踪节省：
   "节省约 13K tokens（基准：14K，RTK：1K）"
```

## 会话跟踪

可选：在会话中跟踪累计节省量：

```bash
# 会话结束时
rtk gain  # 显示会话的总 token 节省量（SQLite 持久化）
```

## 边缘用例

- **小输出**（<100 字符）：跳过 RTK（开销不值得）
- **已在用 Claude 工具**：Grep/Read 工具已优化
- **多个命令**：用 RTK 包装一次批量处理，而非逐个命令

## 配置

通过 CLAUDE.md 启用：
```markdown
## Token 优化

对高输出命令使用 RTK（Rust Token Killer）：
- git 操作（log、status、diff）
- 包管理器（pnpm、npm）
- 构建工具（cargo、go）
- 测试框架（vitest、pytest）
- 文件查找和读取
```

## 指标（已验证）

基于真实测试：
- `git log`：13,994 字符 → 1,076 字符（减少 92.3%）
- `git status`：100 字符 → 24 字符（减少 76.0%）
- `find`：780 字符 → 185 字符（减少 76.3%）
- `git diff`：15,815 字符 → 6,982 字符（减少 55.9%）
- `read file`：163,587 字符 → 61,339 字符（减少 62.5%）

**平均：token 减少 72.6%**

## 局限

- GitHub 上 446 星，积极维护（23 天内 30 个版本）
- 不适用于交互式命令
- 开发节奏快（检查是否有破坏性变更）

## 建议

**使用 RTK 的场景**：git 工作流、文件操作、测试框架、构建工具、包管理器
**跳过 RTK 的场景**：小输出、快速探索、交互式命令

## 参考

- RTK GitHub：https://github.com/rtk-ai/rtk
- RTK 网站：https://www.rtk-ai.app/
- 评估：`docs/resource-evaluations/rtk-evaluation.md`
- CLAUDE.md 模板：`examples/claude-md/rtk-optimized.md`
