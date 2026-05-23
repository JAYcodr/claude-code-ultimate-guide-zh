# Claude Code 终极指南 - 项目上下文

## 目的

本仓库是 **Claude Code（Anthropic 的命令行工具）的全面文档**。通过指南、示例和模板，教会用户如何有效使用 Claude Code。

**元说明**：本仓库用于记录 Claude Code，因此其自身配置应具有示范性。

## 仓库结构

```
guide/                    # 核心文档
├── ultimate-guide.md     # 主指南（约 2 万行，参考文档）
├── cheatsheet.md         # 单页可打印摘要
├── cowork.md             # 协作重定向页面
├── core/                 # 架构、方法论、发布、已知问题、视觉参考
├── security/             # 安全加固、沙箱隔离、原生沙箱、生产安全、数据隐私
├── ecosystem/            # AI 生态系统、MCP 服务器生态系统、第三方工具、Remarkable AI
├── roles/                # AI 角色、采用方法、AI 学习、智能体评估
├── ops/                  # DevOps/SRE、可观测性、AI 可追溯性
├── diagrams/             # Mermaid 可视化图表
└── workflows/            # 分步工作流指南

examples/                 # 生产就绪模板
├── agents/               # 自定义智能体模板
├── commands/             # 斜杠命令模板
├── hooks/                # 事件钩子示例（bash + PowerShell）
├── skills/               # 技能模块模板
└── scripts/              # 实用脚本（审计、健康检查）

machine-readable/         # 供 LLM 使用
├── reference.yaml        # 精简索引（约 2000 token）
└── llms.txt              # AI 索引文件

whitepapers/              # 专题白皮书（法文 + 英文）
├── fr/                   # 10 个法文源文件（.qmd）
└── en/                   # 10 个英文翻译文件（.qmd）
# 发布于：https://www.florian.bruniaux.com/guides

tools/                    # 交互式工具
├── audit-prompt.md       # 设置审计提示词
└── onboarding-prompt.md  # 个性化学习提示词

docs/                     # 公开文档（已跟踪）
└── resource-evaluations/ # 外部资源评估（151 个文件）

claudedocs/               # Claude 工作文档（git 忽略）
├── resource-evaluations/ # 研究工作文档（提示词、私有审计）
└── *.md                  # 分析报告、计划、工作文档
```

## 关键文件

| 文件                              | 用途                         |
| --------------------------------- | ---------------------------- |
| `VERSION`                         | 版本唯一来源（当前 3.40.0）  |
| `guide/ultimate-guide.md`         | 主要参考文档（优先在此搜索） |
| `guide/cheatsheet.md`             | 日常使用的快速参考           |
| `machine-readable/reference.yaml` | LLM 优化的索引，带行号       |
| `CHANGELOG.md`                    | 所有变更的详细描述           |

## 命令

### 版本管理

```bash
# 检查所有文档中的版本一致性
./scripts/sync-version.sh --check

# 修复版本不匹配（从 VERSION 文件更新）
./scripts/sync-version.sh

# 提升版本
echo "3.7.0" > VERSION && ./scripts/sync-version.sh
```

### 白皮书、速查卡和指南导出

完整构建命令（PDF/EPUB/速查卡）、技术栈详情、电子书版本管理以及 Typst 模板同步规则：

@docs/workflows/whitepaper-build.md

### 提交前检查

```bash
# 验证版本已同步
./scripts/sync-version.sh --check
```

### 斜杠命令（维护）

本项目可用的自定义斜杠命令：

| 命令                                | 描述                                                     |
| ----------------------------------- | -------------------------------------------------------- |
| `/release <bump-type>`              | 发布指南版本（CHANGELOG + VERSION + 同步 + 提交 + 推送） |
| `/update-infos-release [bump-type]` | 更新 Claude Code 发布跟踪 + 可选的指南版本提升           |
| `/version`                          | 显示当前指南和 Claude Code 版本及统计信息                |
| `/changelog [count]`                | 查看最近的 CHANGELOG 条目（默认：5）                     |
| `/sync`                             | 检查指南/落地页同步状态                                  |
| `/audit-agents-skills [path]`       | 审计 .claude/ 配置中智能体、技能和命令的质量             |
| `/security-check`                   | 快速配置检查，对比已知威胁数据库（约 30 秒）             |
| `/security-audit`                   | 完整的 6 阶段安全审计，带分数 /100（2-5 分钟）           |
| `/update-threat-db`                 | 研究并更新威胁情报数据库                                 |

**示例：**

```
/release patch                 # 提升补丁版本 + 发布（3.20.4 → 3.20.5）
/release minor                 # 提升次要版本 + 发布（3.20.4 → 3.21.0）
/update-infos-release          # 仅更新 CC 发布信息
/update-infos-release patch    # 更新 CC + 提升指南版本（3.9.11 → 3.9.12）
/update-infos-release minor    # 更新 CC + 提升指南版本（3.9.11 → 3.10.0）
/version                       # 显示版本和内容统计
/changelog 10                  # 最后 10 条 CHANGELOG 条目
/sync                          # 检查指南/落地页同步状态
/audit-agents-skills           # 审计当前项目
/audit-agents-skills --fix     # 审计 + 修复建议
/audit-agents-skills ~/other   # 审计另一个项目
/security-check                # 快速扫描配置，对比已知威胁
/security-audit                # 完整审计，带安全态势分数 /100
/update-threat-db              # 研究 + 更新 threat-db.yaml
```

这些命令定义在 `.claude/commands/` 中，自动化以下任务：

- Claude Code 发布跟踪（YAML + Markdown + 落地页徽章）
- 指南版本管理（VERSION 文件 + 所有文档同步）
- CHANGELOG 更新
- 落地站同步验证
- Git 提交并推送到两个仓库

### 命令命名约定

`.claude/commands/` 中使用的隐式前缀：

| 前缀         | 模式                   | 示例                                               |
| ------------ | ---------------------- | -------------------------------------------------- |
| `audit-*`    | 带评分输出的质量检查   | `audit-agents-skills`、`audit-deps`                |
| `update-*`   | 从外部源同步或刷新数据 | `update-infos-release`、`update-threat-db`         |
| `security-*` | 安全扫描，深度递增     | `security-check`（快速）、`security-audit`（完整） |
| _（无前缀）_ | 核心指南工作流命令     | `release`、`sync`、`version`、`changelog`          |

添加新命令时，选择与操作类型匹配的前缀。除非现有四个类别不适用，否则避免创建新的前缀类别。

## 行为规则

这些规则来自本仓库实际会话中观察到的摩擦模式。

### 始终更新 CHANGELOG.md

任何文件修改或功能实现后，在 `[Unreleased]` 下更新 `CHANGELOG.md`。除非明确告知，否则绝不跳过此步骤。这是最常见的遗漏步骤。

### 首次检查要详尽

当要求分析、审计或审查时——阅读每个相关文件。不要进行表面扫描。如果不确定范围，先询问而不是提供肤浅的结果。这适用于资源评估、文档审计和代码库审查。

### 使用绝对路径

在文档、报告或资源评估中引用文件时，始终使用完整绝对路径。绝不使用相对路径。

### 收尾清单

完成所有请求的任务后，始终主动确认：

1. 已更改的文件（列出它们）
2. CHANGELOG.md 已更新
3. 已提交并推送（如适用）——包含提交哈希

### 偏向行动

不要在探索或规划循环中花费过多时间。尽早产生文件和具体输出，然后迭代。如果任何步骤卡住超过 2 次尝试，解释阻塞点而不是循环。

## 约定

### 文档风格

- **准确性优于营销**：不编造百分比或未经验证的声明
- **实用示例**：每个概念都有具体示例
- **来源归属**：通过链接注明社区贡献
- **版本对齐**：所有版本号必须与 `VERSION` 文件匹配

### 文件组织

- 新指南 → `guide/`
- 新模板 → `examples/{agents,commands,hooks,skills}/`
- 导航更新 → 同时更新 `README.md` 和 `guide/README.md`

### 版本管理

- `VERSION` 文件是版本唯一来源
- 更改版本后运行 `./scripts/sync-version.sh`
- 包含版本的文件：README.md、cheatsheet.md、ultimate-guide.md、reference.yaml

## 当前重点

查看 `IDEAS.md` 了解计划改进，查看 `CHANGELOG.md [Unreleased]` 了解进行中的工作。

## 模型配置

**推荐模式**：`/model opusplan`

**理由**：此文档仓库受益于混合智能：

- **规划阶段**（Opus + 思考）：架构决策、研究综合、多文件分析
- **执行阶段**（Sonnet）：文档更新、版本同步、模板编辑、格式化

**OpusPlan 工作流**：

1. `/model opusplan` → 设置混合模式
2. `/plan` 或 `Shift+Tab × 2` → 用 Opus 规划（启用思考）
3. `Shift+Tab` → 用 Sonnet 执行（更快、更便宜）

**典型任务分解**：

| 任务类型 | 模型 | 理由 |
|----------|------|------|
| 文档编辑、拼写修正 | Sonnet | 直接，无需深度推理 |
| 版本同步、格式化 | Sonnet | 机械模式匹配 |
| 指南重构 | Opus（规划）→ Sonnet（执行） | 需要先进行架构思考 |
| 研究综合 | Opus（规划）→ Sonnet（撰写） | 复杂分析，然后清晰撰写 |
| 多文件一致性检查 | Opus（规划）→ Sonnet（修复） | 依赖分析，然后编辑 |

**成本优化**：OpusPlan 仅对规划支付 Opus 费用（通常占 token 的 10-20%），Sonnet 处理 80-90% 的执行工作。

## 落地站同步

同步工作流、触发条件、指南阅读器重建、RSS 订阅源、站点地图和公告横幅：

@docs/workflows/landing-sync.md

## 生态系统（4 个仓库）

架构、仓库详情、跨仓库同步触发器、仓库间关系及历史：

@docs/ecosystem.md

## 研究资源

**Perplexity Pro 可用**：对于需要关于 Claude Code、Anthropic 或 AI 辅助开发实践的可靠来源或最新信息的任何研究：

- 请我进行 Perplexity 搜索（比基本 WebSearch 更有效）
- 我将提供带来源的结果
- 适用于：Claude Code 新功能、社区最佳实践、工具比较、更新的官方文档

## Claude Code 发布跟踪

文件、更新工作流和 YAML 条目格式：

@docs/workflows/releases-tracking.md

## 资源评估工作流

外部资源（文章、视频、讨论）在集成到指南前会进行评估。

### 流程

1. **研究**：初始 Perplexity 搜索 → 将提示词 + 结果保存在 `claudedocs/resource-evaluations/`（私有）
   1b. **交叉引用**：如果资源与 Claude Code 相关，验证声明与 `https://code.claude.com/docs/llms-full.txt` 对比（官方来源约 98KB）
2. **评估**：系统评分（1-5）→ 在 `docs/resource-evaluations/` 中创建评估文件（已跟踪）
3. **挑战**：智能体进行技术审查以确保客观性
4. **决策**：集成（评分 3+）、提及（评分 2）或拒绝（评分 1）

### 文件组织

| 位置                               | 内容                       | 跟踪状态            |
| ---------------------------------- | -------------------------- | ------------------- |
| `docs/resource-evaluations/`       | 最终评估（151 个文件）     | ✅ Git 跟踪（公开） |
| `claudedocs/resource-evaluations/` | 工作文档、提示词、私有审计 | ❌ Git 忽略（私有） |

### 评分网格

| 评分 | 操作                        |
| ---- | --------------------------- |
| 5    | 关键 - 立即集成（<24 小时） |
| 4    | 高价值 - 一周内集成         |
| 3    | 中等 - 有时间时集成         |
| 2    | 边缘 - 最小提及或跳过       |
| 1    | 低 - 拒绝                   |

完整方法论见：[`docs/resource-evaluations/README.md`](docs/resource-evaluations/README.md)

## 快速查找

回答关于 Claude Code 的问题时：0. **官方 Anthropic 文档（LLM 优化）**：`https://code.claude.com/docs/llms.txt`（索引约 65 页）或 `https://code.claude.com/docs/llms-full.txt`（完整文档约 98KB）用于官方事实

1. 先搜索 `machine-readable/reference.yaml`（有指向完整指南的行号）
2. 使用这些行号从 `guide/ultimate-guide.md` 读取相关部分
3. 检查 `examples/` 获取即用模板
4. 检查 `guide/core/claude-code-releases.md` 获取最新功能/变更
5. 如果信息缺失或不确定 → 请求 Perplexity 搜索（社区、比较、反馈）
