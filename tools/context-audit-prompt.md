# 审计你的上下文工程设置

> 一个独立的提示词，用于衡量和改善你的 Claude Code 上下文架构。

**作者**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | 创始工程师 [@Méthode Aristote](https://methode-aristote.fr)

**参考**: [Claude Code 终极指南](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. 这是做什么的

本提示词指示 Claude 审计你的上下文工程设置，具体包括：

1. **衡量** 总常驻上下文大小、CLAUDE.md 长度和路径作用域比率
2. **检测** 技能与规则的平衡、冗余度以及负面与正面指令的对比
3. **标记** 过时信号（最后更新时间、损坏的导入、已弃用的引用）
4. **评分** 涵盖 8 个维度，总分 /100，附带优先级建议

**性能**：使用 bash/grep 进行高效扫描。Claude 仅在需要特定内容分析时读取文件。

**重要提示**：Claude 不会在未经你明确批准的情况下做任何更改。

---

## 2. 适用对象

| 级别 | 你将获得 |
|-------|-------------|
| **独立开发者** | 快速制胜：精简冗余、补充缺失章节、修复过时导入 |
| **小团队（2-10人）** | 发现一致性差距和基于配置文件组装的机会 |
| **大团队（10人以上）** | 系统性的上下文架构评估与成熟度评分 |

**前置条件**：
- 已安装并正常运行的 Claude Code
- 至少包含 CLAUDE.md 或 `.claude/` 目录的项目
- Bash 终端（macOS/Linux 原生支持，Windows 使用 WSL）

**耗时**：约 3-5 分钟

---

## 3. 使用方法

### 步骤 1：复制提示词

复制下方[第 4 节](#4-the-prompt)代码块中的所有内容。

### 步骤 2：运行 Claude Code

```bash
cd your-project-directory
claude
```

### 步骤 3：粘贴并执行

粘贴提示词并按下回车。Claude 将开始审计。

### 步骤 4：查看结果

Claude 将展示审计结果，然后在进行任何更改前征求你的确认。

### 平台说明

| 平台 | 全局配置路径 |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. 提示词

```markdown
# 审计我的上下文工程设置

## 上下文

对我的 Claude Code 配置进行全面上下文工程审计。
重点关注上下文大小、结构质量、新鲜度和团队可扩展性。

参考：https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md

## 指令

### 阶段 1：发现（Bash 扫描）

**重要提示**：此阶段仅使用 bash 命令。请勿读取文件。

#### 1.1 大小与结构扫描

```bash
bash -c '
echo "=== GLOBAL CLAUDE.MD ==="
if [ -f ~/.claude/CLAUDE.md ]; then
  lines=$(wc -l < ~/.claude/CLAUDE.md | tr -d " ")
  chars=$(wc -c < ~/.claude/CLAUDE.md | tr -d " ")
  tokens=$(echo "scale=0; $chars / 4" | bc 2>/dev/null || echo "~$((chars/4))")
  echo "Lines: $lines"
  echo "Chars: $chars (~$tokens tokens)"
  echo "Imports: $(grep -c "^@" ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
  echo "Rules count: $(grep -cE "^[-*] |^\d+\. " ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
  echo "Last commit: $(cd ~/.claude && git log --format="%ar" -- CLAUDE.md 2>/dev/null | head -1 || echo "not tracked")"
else
  echo "NOT FOUND"
fi

echo ""
echo "=== PROJECT CLAUDE.MD ==="
for f in ./CLAUDE.md ./.claude/CLAUDE.md; do
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f" | tr -d " ")
    chars=$(wc -c < "$f" | tr -d " ")
    tokens=$(echo "scale=0; $chars / 4" | bc 2>/dev/null || echo "~$((chars/4))")
    echo "File: $f"
    echo "Lines: $lines"
    echo "Chars: $chars (~$tokens tokens)"
    echo "Imports: $(grep -c "^@" "$f" 2>/dev/null || echo 0)"
    echo "Rules count: $(grep -cE "^[-*] |^\d+\. " "$f" 2>/dev/null || echo 0)"
    echo "Last commit: $(git log --format="%ar" -- "$f" 2>/dev/null | head -1 || echo "not tracked")"
  fi
done

echo ""
echo "=== IMPORTED FILES ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  while IFS= read -r line; do
    [[ "$line" =~ ^@ ]] || continue
    import_path="${line#@}"
    import_path="${import_path/ */}"
    resolved="${import_path/#\~/$HOME}"
    resolved="${resolved/#./$PWD}"
    if [ -f "$resolved" ]; then
      sz=$(wc -c < "$resolved" | tr -d " ")
      tk=$(echo "scale=0; $sz / 4" | bc 2>/dev/null || echo "$((sz/4))")
      echo "  FOUND $line (~$tk tokens)"
    else
      echo "  BROKEN $line (file not found)"
    fi
  done < "$f"
done

echo ""
echo "=== RULES & MODULES ==="
for d in ~/.claude ./.claude; do
  [ -d "$d" ] || continue
  for sub in rules skills commands agents hooks; do
    if [ -d "$d/$sub" ]; then
      count=$(find "$d/$sub" -maxdepth 1 -type f | wc -l | tr -d " ")
      total_chars=$(find "$d/$sub" -maxdepth 1 -type f -exec cat {} \; 2>/dev/null | wc -c | tr -d " ")
      tokens=$((total_chars / 4))
      echo "  $d/$sub: $count files (~$tokens tokens)"
    fi
  done
done
'
```

**保存输出**，用于后续评估。

#### 1.2 质量模式扫描

```bash
bash -c '
echo "=== NEGATIVE VS POSITIVE INSTRUCTIONS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  neg=$(grep -ciE "never|do not|dont|avoid|prohibited|forbidden|not allowed|do NOT" "$f" 2>/dev/null || echo 0)
  pos=$(grep -ciE "always|prefer|use|should|must|recommended|do this" "$f" 2>/dev/null || echo 0)
  echo "$f: negative=$neg positive=$pos"
done

echo ""
echo "=== VAGUE INSTRUCTIONS (red flags) ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -inE "be careful|good practice|appropriately|as needed|when necessary|use your judgment|you should know|be smart" "$f" 2>/dev/null | head -5 || echo "  none found"
done

echo ""
echo "=== DUPLICATE SECTION HEADERS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  dupes=$(grep -E "^#{1,3} " "$f" | sort | uniq -d)
  [ -n "$dupes" ] && echo "$f DUPLICATES: $dupes" || echo "$f: no duplicate headers"
done

echo ""
echo "=== DEPRECATED REFERENCES ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -niE "claude-1|claude-2\.0|claude-3-haiku-|gpt-3\.5|text-davinci|codex|copilot X|cursor pro 1\." "$f" 2>/dev/null | head -5 || echo "  none found"
done

echo ""
echo "=== PATH SCOPING (modular setup) ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  scoped=$(grep -cE "^@.+\.(ts|tsx|js|jsx|py|rs|go|md)$|globs:|path:" "$f" 2>/dev/null || echo 0)
  echo "$f path-scoped entries: $scoped"
done

echo ""
echo "=== SESSION & UPDATE PROTOCOL ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_update=$(grep -ciE "update|review|quarterly|maintenance|how to update|keep.*fresh" "$f" 2>/dev/null || echo 0)
  has_session=$(grep -ciE "session|retro|checkpoint|lesson learned|knowledge loop" "$f" 2>/dev/null || echo 0)
  echo "$f: update-protocol=$has_update session-retro=$has_session"
done

echo ""
echo "=== TEAM/PROFILE READINESS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_profile=$(grep -ciE "profile|role:|junior|senior|lead|persona|persona-" "$f" 2>/dev/null || echo 0)
  has_module=$(grep -cE "^@" "$f" 2>/dev/null || echo 0)
  echo "$f: profile-mentions=$has_profile module-imports=$has_module"
done
'
```

**保存输出**，用于后续评估。

#### 1.3 新鲜度与冲突扫描

```bash
bash -c '
echo "=== GIT FRESHNESS ==="
for path in ~/.claude ./; do
  if git -C "$path" rev-parse --git-dir &>/dev/null 2>&1; then
    echo "Repo at $path:"
    git -C "$path" log --format="%ar %s" -- CLAUDE.md .claude/CLAUDE.md 2>/dev/null | head -3 || echo "  no commits for CLAUDE.md"
  fi
done

echo ""
echo "=== CONFLICTING RULES PATTERNS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  # Look for contradictory patterns like "always X" near "never X"
  always_terms=$(grep -ioE "always [a-z ]+" "$f" 2>/dev/null | sed "s/always //i" | sort)
  never_terms=$(grep -ioE "never [a-z ]+" "$f" 2>/dev/null | sed "s/never //i" | sort)
  conflicts=$(comm -12 <(echo "$always_terms") <(echo "$never_terms") 2>/dev/null)
  [ -n "$conflicts" ] && echo "  POTENTIAL CONFLICTS: $conflicts" || echo "  no obvious contradictions"
done

echo ""
echo "=== OVERVIEW / ARCHITECTURE SECTION ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_overview=$(grep -ciE "^## (overview|purpose|about|architecture|what this|context)" "$f" 2>/dev/null || echo 0)
  has_antip=$(grep -ciE "anti.pattern|bad example|do not do|wrong way|pitfall" "$f" 2>/dev/null || echo 0)
  has_hierarchy=$(grep -cE "^#{1,3} " "$f" 2>/dev/null || echo 0)
  echo "$f: has-overview=$has_overview anti-patterns=$has_antip section-count=$has_hierarchy"
done
'
```

**保存输出**，用于后续评估。

### 阶段 2：在 8 个维度上进行评估

使用阶段 1 的扫描输出。仅在报告需要内容示例时读取特定文件章节。

#### 维度 1：大小与预算（15 分）

Evaluate based on token estimates from Phase 1:

| 检查项 | 分值 | 阈值 |
|-------|--------|-----------|
| 总常驻上下文低于 8K tokens | 5 | 所有 CLAUDE.md + 导入之和 |
| 规则数量低于 150 条 | 5 | 全局 + 项目合并 |
| 无单个文件超过 400 行 | 5 | 超出则标记 |

如果超出阈值则按比例扣分。600 行的文件 = 3/5 而非 0。

#### 维度 2：结构（15 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| 包含概述/目的章节 | 4 | 带有"overview"、"purpose"、"about"、"context"的 h2 |
| 包含架构或项目布局章节 | 3 | 带有"architecture"、"structure"、"layout"的 h2 |
| 包含反模式或错误示例 | 4 | "anti-pattern"、"do not"、"pitfall" |
| 章节数量体现清晰的层级结构 | 4 | 3 个以上不同的 h2 章节 |

#### 维度 3：路径作用域（12 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| 使用 @imports 进行模块化拆分 | 5 | 至少 2 行 @import |
| 至少一条路径特定或 glob 作用域的规则 | 4 | globs: 或特定文件章节 |
| 非单一文件（所有指令在一个块中） | 3 | 多个文件或章节 |

#### 维度 4：规则质量（15 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| 正面与负面指令比例 >= 2:1 | 5 | 来自负面/正面计数 |
| 未检测到模糊指令 | 5 | 零个"be careful"、"as needed"等 |
| 规则具体且可执行 | 5 | 在报告生成时通过样本判断 |

#### 维度 5：新鲜度（12 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| CLAUDE.md 在过去 6 个月内有提交 | 5 | git log 输出 |
| 无已弃用的工具/模型引用 | 4 | 弃用扫描输出 |
| 无损坏的 @imports | 3 | 导入扫描中的 BROKEN 行 |

#### 维度 6：团队就绪度（10 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| 包含基于配置文件或角色的结构 | 4 | profile 提及次数 >= 1 |
| 模块导入实现选择性组装 | 3 | module-imports >= 3 |
| 为团队记录的更新协议 | 3 | update-protocol >= 1 |

#### 维度 7：冲突检测（11 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| 未检测到矛盾规则 | 5 | 扫描无冲突 |
| 无重复章节标题 | 3 | 未发现重复 |
| 会话回顾或知识循环模式 | 3 | session-retro >= 1 |

#### 维度 8：知识循环（10 分）

| 检查项 | 分值 | 信号 |
|-------|--------|--------|
| 具有已文档化的更新/审查协议 | 4 | update-protocol >= 1 |
| 具有会话回顾或经验教训模式 | 3 | session-retro >= 1 |
| 上下文在 git 中跟踪（可审计的变更） | 3 | git 新鲜度扫描显示有提交 |

#### 计算总分

`总分 = 所有 8 个维度得分之和`

### 阶段 3：生成报告

请严格按照以下结构输出：

---

## 上下文工程审计

### 得分：[XX]/100

| 维度 | 得分 | 备注 |
|-----------|-------|-------|
| 大小与预算 | X/15 | 总计 ~X tokens，X 条规则 |
| 结构 | X/15 | X 个章节，有/缺少概述 |
| 路径作用域 | X/12 | X 个导入，单体/模块化 |
| 规则质量 | X/15 | X% 正面，发现 X 处模糊 |
| 新鲜度 | X/12 | 最后更新 X，X 个损坏导入 |
| 团队就绪度 | X/10 | X 个配置文件，更新协议：有/无 |
| 冲突检测 | X/11 | X 处矛盾，X 个重复标题 |
| 知识循环 | X/10 | git 跟踪：有/无，回顾：有/无 |

### 上下文预算
- 全局 CLAUDE.md：~X tokens
- 项目 CLAUDE.md：~X tokens
- @imports 合计：~X tokens
- 总常驻上下文：~X tokens
- 规则数量：X/150 条

### 优先级问题（优先修复）
1. [问题] — [具体修复方案及示例]
2. [问题] — [具体修复方案及示例]
3. [问题] — [具体修复方案及示例]

### 快速制胜（每项 < 30 分钟）
- [修复]：[做什么及在哪里]
- [修复]：[做什么及在哪里]
- [修复]：[做什么及在哪里]

### 成熟度等级
[选择一个并说明原因]

**Level 1 — 空置**（0-19）：无结构化上下文。Claude 在零项目知识下运行。
**Level 2 — 基础**（20-39）：存在 CLAUDE.md，但为单体、过时或大多为模糊规则。
**Level 3 — 结构化**（40-59）：清晰的章节和导入，但缺少新鲜度或团队模式。
**Level 4 — 已优化**（60-79）：模块化、作用域限定、正面优先规则，具有已知的更新节奏。
**Level 5 — 工程级**（80-100）：配置文件感知、git 跟踪、无冲突、知识循环活跃。

### 即用型改进

提供 2-3 个具体文本块，用户可直接粘贴到他们的 CLAUDE.md 中。
每个块必须解决上述优先级问题。格式：

**改进 1：[名称]**
文件：`[路径]` — 添加到[顶部/章节 X/末尾]
```
[要粘贴的精确文本]
```

**改进 2：[名称]**
文件：`[路径]` — 添加到[顶部/章节 X/末尾]
```
[要粘贴的精确文本]
```

---

### 阶段 4：等待确认

**关键提示**：未经明确批准，请勿创建或修改任何文件。

呈现报告后，询问：

"你希望我实施哪些改进？

选项：
- `all` — 应用所有即用型改进
- `1, 2` — 按编号指定改进
- `priority` — 仅修复优先级问题
- `none` — 仅保留报告供参考

请指定你的选择："

等待用户明确回复后再采取任何行动。

## 输出格式

请严格按以下结构组织回复：

1. **得分表**，包含各维度细分
2. **上下文预算**摘要
3. **优先级问题**（编号，优先修复）
4. **快速制胜**（项目列表，每项 < 30 分钟）
5. **成熟度等级**及说明
6. **即用型改进**（可直接粘贴的文本块）
7. **确认请求**（实施前先询问）
```

---

## 5. 预期结果

以下是审计报告示例：

### 得分表示例

```
## 上下文工程审计

### 得分：52/100

| 维度 | 得分 | 备注 |
|-----------|-------|-------|
| 大小与预算 | 10/15 | 总计约 6,200 tokens，182 条规则（超出限制） |
| 结构 | 9/15 | 4 个章节，无反模式章节 |
| 路径作用域 | 4/12 | 1 个导入，单体项目 CLAUDE.md |
| 规则质量 | 8/15 | 60% 正面，发现 3 条模糊指令 |
| 新鲜度 | 9/12 | 最后提交在 4 个月前，1 个损坏导入 |
| 团队就绪度 | 3/10 | 无配置文件，无更新协议 |
| 冲突检测 | 6/11 | 1 处"总是/从不"矛盾，无重复标题 |
| 知识循环 | 3/10 | 未进行 git 跟踪，无回顾模式 |
```

### 快速制胜示例

```
快速制胜（每项 < 30 分钟）：
- 修复损坏导入：@~/.claude/TONE.md 未找到 — 更新路径或移除
- 添加概述章节：在 CLAUDE.md 顶部添加 2 行项目描述
- 精简规则数量：将 3 条格式规则合并为一个压缩块
```

---

## 6. 评分指南

| 分数 | 成熟度 | 建议操作 |
|-------|----------|--------------------|
| **80-100** | Level 5：工程级 | 每季度审查维护 |
| **60-79** | Level 4：已优化 | 解决优先级问题，达到 80 |
| **40-59** | Level 3：结构化 | 专门安排一次改进会话 |
| **20-39** | Level 2：基础 | 建议重构，使用模板 |
| **0-19** | Level 1：空置 | 使用骨架模板重新开始 |

---

## 7. 术语表

| 术语 | 定义 |
|------|-----------|
| **常驻上下文** | Claude 在第一条消息之前加载的所有内容：CLAUDE.md 文件及所有 @imports |
| **@import** | CLAUDE.md 中以 `@` 开头的行，用于将另一个文件加载到上下文中 |
| **路径作用域** | 仅对特定文件类型或目录应用规则，而非全局 |
| **规则质量** | 指令的明确性和可执行性 — 模糊的规则浪费 tokens 并使 Claude 困惑 |
| **知识循环** | 根据会话中有效和无效的内容更新上下文文件的实践 |
| **配置文件组装** | 组合不同的上下文模块以创建特定角色的设置（初级、高级、审查者） |
| **过时信号** | 表明上下文已过时的指标：损坏的导入、已弃用的模型名称、无 git 历史 |
| **冲突** | 两条相互矛盾的规则 — Claude 会任意选择一条，通常选错 |
| **单体 CLAUDE.md** | 包含所有指令的单个大文件，无导入，无模块化拆分 |
| **成熟度等级** | 衡量上下文工程成熟度的 1-5 级量表，从空置到工程级 |

---

## 8. 常见问题

### "Token 估算似乎不准"

**原因**：估算使用 chars/4 作为 GPT 风格 tokens 的粗略代理。Claude 的分词器可能略有不同。

**修复**：关注相对数字和阈值，而非绝对 token 计数。8K 常驻预算是一种启发式规则，而非硬性限制。

### "分数很低但 Claude 似乎运行正常"

**原因**：Claude 在没有上下文工程的情况下也能工作 — 分数反映的是优化程度，而非基本功能。

**修复**：低分意味着你还有生产力提升空间。每个维度的差距都会增加每次会话的认知开销。

### "标记了损坏的导入但文件存在"

**原因**：相对路径解析与 Claude 启动时的实际工作目录不同。

**修复**：对全局导入使用绝对路径（`~/.claude/file.md`）。对项目导入使用项目相对路径（`./docs/conventions.md`）。

### "标记了配置文件就绪度但我是个人开发者"

**原因**：审计会检查团队可扩展性模式，无论团队规模如何。

**修复**：基于配置文件的组装在切换上下文时（审查 PR vs 编写功能 vs 调试）仍然有益于个人开发者。个人使用时可选项。

---

## 9. 相关资源

- [Claude Code 终极指南](../guide/ultimate-guide.md) - 完整参考
- [审计你的 Claude Code 设置](./audit-prompt.md) - 完整配置审计（代理、钩子、MCP、CI）
- [速查表](../guide/cheatsheet.md) - 日常快速参考
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code) - Anthropic 文档
- [context-evaluator.ai](https://context-evaluator.ai) - 零安装、LLM 原生的 CLAUDE.md 和 AGENTS.md 审计：17 个 AI 评估器，自动 `.patch` 修复。通过更深入的逐规则分析和不同的评估角度（LLM 作为评判者 vs bash 启发式）来补充此提示词。

---

*最后更新：2026 年 4 月 | 版本 1.1*
