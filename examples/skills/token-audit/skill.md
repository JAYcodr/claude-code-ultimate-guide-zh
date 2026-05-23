<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
name: token-audit
description: "审计 Claude Code 配置以测量固定上下文的 token 开销，并生成带优先级的行为计划。在遇到速率限制、早期上下文压缩或添加重要配置后使用。"
effort: medium
allowed-tools: Read Grep Glob Bash
---

# /token-audit — 上下文 Token 审计

**目的**：测量在任何用户任务开始之前，你的 Claude Code 配置消耗了多少 token。识别最大的开销来源。生成带有节省估计的具体行动计划。

**何时使用**：
- 在一天结束前就遇到速率限制
- 会话感觉变慢或上下文过早压缩
- 你添加了许多规则文件并想知道实际成本
- 在重大配置变更后

---

## 你将测量什么

| 组件 | 加载时机 | 典型范围 |
|-----------|-------------|---------------|
| `~/.claude/CLAUDE.md` + @imports | 始终 | 5-15K tokens |
| 项目 `CLAUDE.md` | 始终 | 2-8K tokens |
| `.claude/rules/*.md` | 始终（所有文件） | 5-40K tokens |
| `MEMORY.md` | 始终 | 1-3K tokens |
| Claude Code 系统提示 | 始终 | ~7,500 tokens |
| 钩子 stdout | 每次工具调用 | 可变 |
| 命令、智能体、技能 | 仅调用时 | 默认为 0 |

关键洞见：`.claude/rules/` 在会话开始时加载每个 `.md` 文件，无论是否相关。命令和智能体是惰性加载的 — 它们在被调用前成本为零。规则文件是最常见的意外开销来源。

---

## 步骤 1 — 运行测量

从项目根目录执行这些命令：

```bash
# 组件大小
echo "=== PROJECT CLAUDE.md ===" && wc -c CLAUDE.md 2>/dev/null || echo "none"

echo ""
echo "=== RULES FILES (sorted by size) ===" && find .claude/rules -name "*.md" 2>/dev/null \
  | xargs wc -c 2>/dev/null | sort -rn | head -20

echo ""
echo "=== GLOBAL ~/.claude ===" && ls -la ~/.claude/*.md 2>/dev/null \
  | awk '{print $5, $9}' | sort -rn
```

然后计算完整预算：

```bash
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
MEMORY=$(find ~/.claude/projects -name "MEMORY.md" 2>/dev/null \
  | xargs grep -l "$(basename $(pwd))" 2>/dev/null | head -1 \
  | xargs wc -c 2>/dev/null | awk '{print $1}' || echo 0)
TOTAL=$(( GLOBAL + PROJECT + RULES + MEMORY + 30000 ))

echo "Global ~/.claude   : ~$(( GLOBAL / 4 )) tokens ($(( GLOBAL / 1000 ))K chars)"
echo "Project CLAUDE.md  : ~$(( PROJECT / 4 )) tokens"
echo "Rules (auto-loaded): ~$(( RULES / 4 )) tokens"
echo "MEMORY.md          : ~$(( MEMORY / 4 )) tokens"
echo "System prompt      : ~7,500 tokens"
echo "---"
echo "TOTAL fixed context: ~$(( TOTAL / 4 )) tokens"
echo "% of 200K window   : $(( TOTAL / 4 * 100 / 200000 ))%"
```

---

## 步骤 2 — 分类规则文件

对于 `.claude/rules/` 中的每个文件，进行分类：

| 类别 | 定义 | 操作 |
|-------|------------|--------|
| **始终** | 适用于大多数任务（约定、输出格式、安全） | 保持自动加载 |
| **有时** | 在 20-40% 的会话中相关 | 如果小（<3K chars）则保留；如果大则惰性加载 |
| **很少** | 在 <10% 的会话中相关（Figma、Windows、设计系统） | 从自动加载移除 |
| **从不** | 过时或已被其他文件覆盖 | 删除或归档 |

运行此分类提示：

```
读取 .claude/rules/ 中的每个文件。对每个文件，输出一个表格行：

| 文件 | 大小（字符） | 类别（始终/有时/很少/从不） | 理由（一句话） |

在每个类别内按大小降序排序。
最后，计算：如果所有很少和从不类别的文件都被排除，
将从固定上下文中减少多少字符。转换为 tokens（÷ 4）。
```

---

## 步骤 3 — 审计钩子开销

`PreToolUse` 和 `PostToolUse` 上的钩子每次工具调用都会触发。每次调用将其 stdout 注入上下文。一个输出 500 字符的钩子，在 150 次工具调用下 = 75K 字符 ≈ 19K 额外 token。

检查你有哪些：

```bash
# 按事件类型列出钩子
python3 - << 'EOF'
import json, os
for path in [os.path.expanduser("~/.claude/settings.json"), ".claude/settings.json"]:
    if not os.path.exists(path): continue
    print(f"\n--- {path} ---")
    data = json.load(open(path))
    for event, hooks in data.get("hooks", {}).items():
        for h in hooks:
            cmd = h.get("command", "?")
            matcher = h.get("matcher", "*")
            print(f"  [{event}] matcher={matcher} → {cmd[:80]}")
EOF
```

对于每个 `PreToolUse` 或 `PostToolUse` 钩子，通过手动运行来估计其 stdout 大小。乘以你的平均每次会话工具调用数（在会话后可在 `/cost` 中查看）。

**红旗**：
- 无条件 `cat` 文件的钩子
- 每次调用都执行 `git status` 或 `git log`
- 从未移除的调试用多行 echo 输出
- 作为上下文注入的 JSON blobs

---

## 步骤 4 — 构建行动计划

生成一个带优先级的表格。经验法则：只包含无需外部基础设施即可实现的操作（无需 RAG、无向量数据库、无自定义 MCP 服务器）。

| 操作 | 估计 token 节省 | 工作量 | 风险 |
|--------|------------------------|--------|------|
| 从自动加载移除很少使用的文件 | 视情况 | 30 分钟 | 低 |
| 将大规则拆分为核心+详情 | 视情况 | 1-2h | 低 |
| 将钩子 stdout 裁剪到必要字段 | 视情况 | 1h | 低 |
| 压缩冗长规则（见 §8 context-engineering.md） | 规则的 20-30% | 1-2h | 低 |
| 归档过时的 MEMORY.md 条目 | 500-1K tokens | 30 分钟 | 低 |

---

## 步骤 5 — RAG 问题

通过向量数据库的惰性加载（RAG）有时被宣传为解决方案。在承诺之前诚实地评估：

1. 经过步骤 1-4 后，还有多少固定上下文 token？（先测量这个）
2. RAG 合理吗？一个 pgvector + 自定义 MCP 设置需要 1-2 周。
3. 盈亏平衡点：如果你有 10 个平均 3K 字符的规则文件，分类（30 分钟）节省的和 RAG 一样多。当规则文件超过 50 个且基于意图的路由是唯一可扩展的解决方案时，RAG 才值回成本。

---

## 输出格式

运行审计后，生成此报告：

```markdown
## Token 审计 — [项目] — [日期]

### 预算总结

| 组件 | Tokens | 占总数的 % |
|-----------|--------|------------|
| Global ~/.claude | X | Y% |
| 项目 CLAUDE.md | X | Y% |
| 规则文件（自动加载） | X | Y% |
| MEMORY.md | X | Y% |
| 系统提示 | 7,500 | Y% |
| **总计** | **X** | **100%** |

在任何任务开始前使用的上下文窗口：200K 的 X%

### 规则文件分类

| 文件 | 字符 | 类别 | 操作 |
|------|-------|-------|--------|
| ... | ... | 始终/有时/很少 | 保留/惰性加载/移除 |

### 钩子开销

| 钩子 | 事件 | 估计 stdout | 调用/会话 | 总 tokens/会话 |
|------|-------|-------------|---------------|----------------------|
| ... | PreToolUse | X 字符 | ~Y | ~Z tokens |

### 行动计划

| 操作 | 节省 | 工作量 | 风险 |
|--------|---------|--------|------|
| ... | -X tokens | 30 分钟 | 低 |

**无需基础设施即可实现的总节省**：-X tokens → 从 Y 到 Z（减少 N%）

### RAG 判断

[一段：经过行动计划后剩余的开销、RAG 是否合理、
估计的设置成本 vs 节省。]
```

---

## 解读结果

| 固定上下文 | 评估 |
|---------------|------------|
| < 20K tokens | 健康 — 无需紧急操作 |
| 20-40K tokens | 中等 — 运行分类流程，获取轻松收益 |
| 40-60K tokens | 高 — 值得花一个下午做规则审计 |
| > 60K tokens | 关键 — 你在任何任务开始前就已经烧掉了 30%+ 的窗口 |

在配置较重的项目上经过首次审计后，通常可实现 48% 的减少，且无需基础设施变更 — 只需从自动加载中移除很少使用的文件即可。
