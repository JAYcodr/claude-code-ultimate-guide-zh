---
name: audit-agents-skills
description: "审计 Claude Code 的 agent、技能和命令的质量和生产就绪度。用于评估技能质量、检查生产就绪评分，或将 agent 与最佳实践模板进行比较。"
allowed-tools: Read Grep Glob Bash Write
effort: high
disable-model-invocation: true
metadata:
  version: 1.0.0
---

# 审计 Agent/Skills/Commands（高级技能）

针对 Claude Code 的 agent、技能和命令的全面质量审计系统。提供基于行业最佳实践的量化评分、对比分析和生产就绪度评级。

## 目的

**问题**：手动验证 agent/skills 容易出错且不一致。据 LangChain Agent Report 2026，29.5% 的组织在无系统评估的情况下部署 agent，导致"agent bugs"成为首要挑战（18% 的团队）。

**解决方案**：基于 16 个加权标准的自动化质量评分，含生产就绪度阈值（80% = Grade B，生产部署最低要求）。

**主要特性**：
- 量化评分（agent/skills 32 分，commands 20 分）
- 加权标准（身份 3x、提示词 2x、验证 1x、设计 2x）
- 生产就绪度评级（A-F 等级，80% 阈值）
- 与参考模板的对比分析
- JSON/Markdown 双输出，支持程序化集成
- 针对失败标准的修复建议

---

## 模式

| 模式 | 用法 | 输出 |
|------|-------|--------|
| **快速审计** | 仅前 5 个关键标准 | 快速通过/失败（20 文件 3-5 分钟） |
| **完整审计** | 每个文件全部 16 个标准 | 详细评分 + 建议（10-15 分钟） |
| **对比审计** | 完整审计 + 与模板基准对比 | 分析 + 差距识别（15-20 分钟） |

**默认**：完整审计（首次运行推荐）

---

## 方法论

### 为什么是这些标准？

16 标准框架源自：
1. **Claude Code 最佳实践**（Ultimate Guide 第 4921 行：Agent 验证清单）
2. **行业数据**（LangChain Agent Report 2026：评估差距）
3. **生产故障**（社区反馈：硬编码路径、缺失错误处理）
4. **组合模式**（技能应引用其他技能，agent 应模块化）

### 评分理念

**权重理由**：
- **身份（3x）**：如果用户找不到/无法调用 agent，质量无从谈起（可发现性 > 质量）
- **提示词（2x）**：决定输出的可靠性和准确性
- **验证（1x）**：改进健壮性但次于核心功能
- **设计（2x）**：影响长期可维护性和可扩展性

**等级标准**：
- **A（90-100%）**：生产就绪，风险极小
- **B（80-89%）**：良好，满足生产阈值
- **C（70-79%）**：需改进后才能投入生产
- **D（60-69%）**：差距明显，不可用于生产
- **F（<60%）**：关键问题，需要重大重构

**行业对齐**：80% 阈值与软件工程生产部署最佳实践一致（如代码覆盖率 >80%、安全扫描通过率）。

---

## 工作流

### 阶段 1：发现

1. **扫描目录**：
   ```
   .claude/agents/
   .claude/skills/
   .claude/commands/
   examples/agents/      （如存在）
   examples/skills/      （如存在）
   examples/commands/    （如存在）
   ```

2. **按类型分类文件**（agent/skill/command）

3. **加载参考模板**（对比模式）：
   ```
   guide/examples/agents/     （基准文件）
   guide/examples/skills/     （基准文件）
   guide/examples/commands/   （基准文件）
   ```

### 阶段 2：评分引擎

从 `scoring/criteria.yaml` 加载评分标准：

```yaml
agents:
  max_points: 32
  categories:
    identity:
      weight: 3
      criteria:
        - id: A1.1
          name: "清晰的名称"
          points: 3
          detection: "frontmatter.name 存在且具描述性"
        # ...（共 16 个标准）
```

对每个文件：
1. 解析 frontmatter（YAML）
2. 提取内容章节
3. 运行检测模式（正则、关键词搜索）
4. 计算分数：`(points / max_points) × 100`
5. 分配等级（A-F）

### 阶段 3：对比分析（仅对比模式）

对每个项目文件：
1. 找到最匹配的模板（按描述相似度）
2. 按标准对比分数
3. 识别差距：`template_score - project_score`
4. 标记显著差距（>10 分差异）

**示例**：
```
项目文件：.claude/agents/debugging-specialist.md（得分：78%，等级 C）
最匹配模板：examples/agents/debugging-specialist.md（得分：94%，等级 A）

差距：
- 抗幻觉措施：-2 分（模板有，项目没有）
- 边缘用例文档化：-1 分（模板有 5 个示例，项目有 1 个）
- 集成文档化：-1 分（模板引用 3 个技能，项目没有）

总差距：16 分（解释了 C vs A 的差异）
```

### 阶段 4：报告生成

**Markdown 报告**（`audit-report.md`）：
- 摘要表（总体 + 按类型）
- 各文件评分及首要问题
- 每个文件的详细分析（可折叠）
- 按优先级排列的建议

**JSON 输出**（`audit-report.json`）：
```json
{
  "metadata": {
    "project_path": "/path/to/project",
    "audit_date": "2026-02-07",
    "mode": "full",
    "version": "1.0.0"
  },
  "summary": {
    "overall_score": 82.5,
    "overall_grade": "B",
    "total_files": 15,
    "production_ready_count": 10,
    "production_ready_percentage": 66.7
  },
  "by_type": {
    "agents": { "count": 5, "avg_score": 85.2, "grade": "B" },
    "skills": { "count": 8, "avg_score": 78.9, "grade": "C" },
    "commands": { "count": 2, "avg_score": 92.0, "grade": "A" }
  },
  "files": [
    {
      "path": ".claude/agents/debugging-specialist.md",
      "type": "agent",
      "score": 78.1,
      "grade": "C",
      "points_obtained": 25,
      "points_max": 32,
      "failed_criteria": [
        {
          "id": "A2.4",
          "name": "抗幻觉措施",
          "points_lost": 2,
          "recommendation": "添加关于来源验证的章节"
        }
      ]
    }
  ],
  "top_issues": [
    {
      "issue": "缺少错误处理",
      "affected_files": 8,
      "impact": "运行时故障未处理",
      "priority": "high"
    }
  ]
}
```

### 阶段 5：修复建议（可选）

对每个失败的标准，生成**可操作的修复方案**：

```markdown
### 文件：.claude/agents/debugging-specialist.md
**问题**：缺少抗幻觉措施（丢失 2 分）

**修复**：
在"方法论"后添加此章节：

## 来源验证

- 技术声明始终引用来源
- 使用短语："根据[文档]..."、"基于[工具输出]..."
- 如果不确定，声明："我没有关于...的已验证信息"
- 绝不编造：统计数据、版本号、API 签名、堆栈跟踪

**检测**：Grep 关键词："verify"、"cite"、"source"、"evidence"
```

---

## 评分标准

完整定义见 `scoring/criteria.yaml`。摘要：

### Agents（满分 32 分）

| 类别 | 权重 | 标准数量 | 满分 |
|----------|--------|----------------|------------|
| 身份 | 3x | 4 | 12 |
| 提示词质量 | 2x | 4 | 8 |
| 验证 | 1x | 4 | 4 |
| 设计 | 2x | 4 | 8 |

**关键标准**：
- 清晰的名称（3 分）：不通用如"agent1"
- 含触发器的描述（3 分）：包含"when"/"use"
- 定义了角色（2 分）："You are..." 声明
- 3+ 个示例（1 分）：记录了使用场景
- 单一职责（2 分）：专注，非"通用目的"

### Skills（满分 32 分）

| 类别 | 权重 | 标准数量 | 满分 |
|----------|--------|----------------|------------|
| 结构 | 3x | 4 | 12 |
| 内容 | 2x | 4 | 8 |
| 技术 | 1x | 4 | 4 |
| 设计 | 2x | 4 | 8 |

**关键标准**：
- 有效的 SKILL.md（3 分）：正确命名
- 名称有效（3 分）：小写、1-64 字符、无空格
- 描述了方法论（2 分）：存在 Workflow 章节
- 无硬编码路径（1 分）：无 `/Users/`、`/home/`
- 清晰的触发器（2 分）：有"何时使用"章节

### Commands（满分 20 分）

| 类别 | 权重 | 标准数量 | 满分 |
|----------|--------|----------------|------------|
| 结构 | 3x | 4 | 12 |
| 质量 | 2x | 4 | 8 |

**关键标准**：
- 有效 frontmatter（3 分）：name + description
- 参数提示（3 分）：如使用 `$ARGUMENTS`
- 逐步工作流（3 分）：编号章节
- 错误处理（2 分）：提及失败模式

---

## 检测模式

### Frontmatter 解析

```python
import yaml
import re

def parse_frontmatter(content):
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None
```

### 关键词检测

```python
def has_keywords(text, keywords):
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)

# 示例
has_trigger = has_keywords(description, ['when', 'use', 'trigger'])
has_error_handling = has_keywords(content, ['error', 'failure', 'fallback'])
```

### 重叠检测（重复检查）

```python
def jaccard_similarity(text1, text2):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) if union else 0

# 如果相似度 > 0.5，标记
if jaccard_similarity(desc1, desc2) > 0.5:
    issues.append("与另一个文件高度重叠")
```

### Token 计数（近似）

```python
def estimate_tokens(text):
    # 粗略估计：1 token ≈ 0.75 词
    word_count = len(text.split())
    return int(word_count * 1.3)

# 检查预算
tokens = estimate_tokens(file_content)
if tokens > 5000:
    issues.append("文件过大（>5K tokens）")
```

---

## 行业背景

**来源**：LangChain Agent Report 2026（公开报告，第 14-22 页）

**关键发现**：
- **29.5%** 的组织在无系统评估的情况下部署 agent
- **18%** 将"agent bugs"列为首要挑战
- **仅 12%** 使用自动化质量检查（88% 手动或无检查）
- **43%** 报告维持 agent 质量随时间推移的困难
- **首要问题**：幻觉（31%）、错误处理不佳（28%）、触发器不明确（22%）

**影响**：
1. **自动化差距**：大多数团队依赖手动清单（大规模时容易出错）
2. **质量债务**：未经验证部署的 agent 积累技术债务
3. **维护负担**：43% 因缺乏跟踪系统而难以维持质量

**此技能解决的问题**：
- 自动化：用量化评分替代手动清单
- 跟踪：JSON 输出支持随时间趋势分析
- 标准：80% 阈值提供明确的生产门禁

---

## 输出示例

### 快速审计（前 5 个标准）

```markdown
# 快速审计：Agents/Skills/Commands

**文件**：15 个（5 agent、8 skill、2 command）
**关键问题**：3 个文件未通过前 5 个标准

## 前 5 个标准（通过/失败）

| 文件 | 有效名称 | 有触发器 | 错误处理 | 无硬编码路径 | 示例 |
|------|------------|--------------|----------------|--------------------|----------|
| agent1.md | ✅ | ✅ | ❌ | ✅ | ❌ |
| skill2/ | ✅ | ❌ | ✅ | ❌ | ✅ |

## 需要采取的行动

1. **添加错误处理**：5 个文件
2. **移除硬编码路径**：3 个文件
3. **添加使用示例**：4 个文件
```

### 完整审计

见上方案例 4：报告生成章节的完整结构。

### 对比审计（完整 + 基准）

```markdown
# 对比审计

## 项目 vs 模板

| 文件 | 项目评分 | 模板评分 | 差距 | 主要缺失 |
|------|---------------|----------------|-----|-------------|
| debugging-specialist.md | 78%（C） | 94%（A） | -16 分 | 抗幻觉措施、边缘用例 |
| testing-expert/ | 85%（B） | 91%（A） | -6 分 | 集成文档 |

## 建议

专注于以下差距以达到模板质量：
1. **抗幻觉措施**（8 个文件）：添加来源验证章节
2. **边缘用例文档**（5 个文件）：添加失败场景示例
3. **集成文档**（4 个文件）：列出兼容的 agent/skills
```

---

## 用法

### 基本用法（完整审计）

```bash
# 在 Claude Code 中
使用技能：audit-agents-skills

# 指定路径
使用技能：audit-agents-skills for ~/projects/my-app
```

### 带选项

```bash
# 快速审计
使用技能：audit-agents-skills with mode=quick

# 对比审计（基准分析）
使用技能：audit-agents-skills with mode=comparative

# 生成修复方案
使用技能：audit-agents-skills with fixes=true

# 自定义输出路径
使用技能：audit-agents-skills with output=~/Desktop/audit.json
```

### 仅 JSON 输出

```bash
# 用于程序化集成
使用技能：audit-agents-skills with format=json output=audit.json
```

---

## CI/CD 集成

### 预提交钩子

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 对已更改的 agent/skill/command 文件运行快速审计
changed_files=$(git diff --cached --name-only | grep -E "^\.claude/(agents|skills|commands)/")

if [ -n "$changed_files" ]; then
    echo "正在对已更改的文件运行快速审计..."
    # 运行审计（需要 Claude Code CLI 包装器）
    # 如果有文件评分 <80%，退出码为 1
fi
```

### GitHub Actions

```yaml
name: 审计 Agents/Skills
on: [pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 运行质量审计
        run: |
          # 运行审计技能
          # 解析 JSON 输出
          # 如果 overall_score < 80 则失败
```

---

## 对比：Command vs Skill

| 方面 | Command（`/audit-agents-skills`） | Skill（本文件） |
|--------|----------------------------------|-------------------|
| **范围** | 仅当前项目 | 多项目、对比 |
| **输出** | Markdown 报告 | Markdown + JSON |
| **速度** | 快（5-10 分钟） | 较慢（10-20 分钟含对比） |
| **深度** | 标准 16 标准 | 同上 + 基准分析 |
| **修复建议** | 通过 `--fix` 标志 | 内置建议 |
| **程序化** | 终端输出 | JSON 用于 CI/CD 集成 |
| **最适合** | 快速检查、开发工作流 | 深度审计、质量跟踪 |

**建议**：日常检查用 command，发布门禁和质量跟踪用 skill。

---

## 维护

### 更新标准

编辑 `scoring/criteria.yaml`：
```yaml
agents:
  categories:
    identity:
      criteria:
        - id: A1.5  # 新标准
          name: "指定了 API 版本"
          points: 3
          detection: "提及 API 版本或兼容性"
```

版本号提升：当标准变化时，递增 frontmatter 中的 `version`。

### 添加文件类型

为支持新的文件类型（如"workflows"）：
1. 添加到 `scoring/criteria.yaml`：
   ```yaml
   workflows:
     max_points: 24
     categories: [...]
   ```
2. 更新检测逻辑（文件路径模式）
3. 更新报告模板

---

## 相关

- **Command 版本**：`.claude/commands/audit-agents-skills.md`
- **Agent 验证清单**：guide 第 4921 行（手动 16 标准）
- **技能验证**：guide 第 5491 行（规范文档）
- **参考模板**：`examples/agents/`、`examples/skills/`、`examples/commands/`

---

## 变更日志

**v1.0.0**（2026-02-07）：
- 初始版本
- 16 标准框架（agents/skills/commands）
- 3 种审计模式（快速/完整/对比）
- JSON + Markdown 输出
- 修复建议
- 行业背景（LangChain 2026 报告）

---

**技能已就绪**：`audit-agents-skills`
