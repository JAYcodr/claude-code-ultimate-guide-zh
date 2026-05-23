# 待探索创意

> 未来指南改进的研究主题。精心筛选、已校验。

## 已完成

### MCP 安全加固 ✅

统一安全研究，涵盖 MCP 漏洞、提示词注入和密钥检测。

**已完成**：[安全加固指南](./guide/security/security-hardening.md) 涵盖：

- CVE-2025-53109/53110、54135、54136 及缓解措施
- MCP 审查工作流，附带 5 分钟审计清单
- MCP 安全清单（社区审查）
- 提示词注入规避技术（Unicode、ANSI、null bytes）
- 密钥检测工具对比（Gitleaks、TruffleHog、GitGuardian）
- 事件响应流程（密钥泄露、MCP 失陷）
- 3 个新钩子：`unicode-injection-scanner.sh`、`repo-integrity-scanner.sh`、`mcp-config-integrity.sh`

---

## 高优先级

### gstack 风格命令（从 2026-03-26 审计延后）

对 [gstack](https://github.com/garrytan/gstack)（Garry Tan 的 Claude Code 冲刺工具集）审计发现以下缺口。高优先级项已实现（`/investigate`、`/qa`、`/canary`、`/land-and-deploy`、`/review-pr` 更新）。其余项延后到此。

**`/autoplan`** — 单一命令，自动串联 CEO → 设计 → 工程评审，内置编码决策原则。将决策分类为机械型（自动裁决）与品味型（提交用户判断）。前提：我们的 `/plan-ceo-review` 和 `/plan-eng-review` 命令需先稳定。来源：`gstack/autoplan/SKILL.md`。

**`/office-hours`** — YC 风格产品诊断，规划前先回答 6 个强制性问题。位于 `/plan-ceo-review` 上游。将设计概要写入 `~/.claude/projects/`。来源：`gstack/office-hours/SKILL.md`。

**`/design-review`** — 实时网站视觉审计 + 修复循环。截取 URL 截图，审计间距/排版/颜色/对比度，检测 AI 粗糙模式（紫色渐变、三列网格、全局居中）。需先完成浏览器工具标准化。来源：`gstack/design-review/SKILL.md` + `design-checklist.md`。

**`/benchmark`** — Core Web Vitals 回归检测（TTFB、FCP、LCP、DOM 加载、打包体积）。基线对比与回归阈值（>50% 或 >500ms = 回归）。来源：`gstack/benchmark/SKILL.md`。

**`/retro`** — 每周回顾，按贡献者分析 git 日志。当前窗口与上一窗口对比。来源：`gstack/retro/SKILL.md`。

**`/freeze` + `/unfreeze`** — 通过 PreToolUse 钩子锁定运行时目录编辑（硬拒绝，非警告）。状态文件位于 `~/.claude/freeze-dir.txt`。可与 `/careful` 组合成 `/guard` 命令。来源：`gstack/freeze/SKILL.md`。

**`/document-release`** — 发布后文档更新。读取自上次发布以来的 diff，更新 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md，润色 CHANGELOG，清理 TODO。来源：`gstack/document-release/SKILL.md`。

**效率压缩表** — 加入技能模板：每种任务类型的人工耗时 vs AI 耗时。需先在技能格式层面做架构决策，再在所有技能中推广实施。

**触发实施条件**：读者需求，或进行「工作流完整性」冲刺时。

---

### 智能体技能 — 文档缺口（来自 agentskills.io 官方文档，2026-05-14）

对照 agentskills.io 官方规范与客户端实现指南后，确认指南技能章节缺失以下 6 个事实性条目。

**[高] 跨客户端目录约定 `.agents/skills/`** — 指南仅记录了 `.claude/skills/`（Claude Code 专属）。开放标准定义 `.agents/skills/`（项目级）和 `~/.agents/skills/`（用户级）为跨客户端路径。放在这些路径下的技能适用于所有 35+ 兼容客户端。这个区别直接影响可移植性声明。添加到「技能存放位置」章节。

**[高] 4 级技能加载优先级** — 指南未记录完整层级：企业 → 个人 → 项目 → 插件。目前指南仅暗示个人与项目两级。企业级（托管设置，最高优先级）和插件级（最低）缺失。添加到优先级层级章节。

**[中] 渐进式披露的 Token 成本** — 规范给出具体数字：目录约 50-100 token/技能（仅名称 + 描述），完整 SKILL.md 正文建议 <5000 token，资源文件按需加载。指南解释了概念但从未给出 token 数值。对读者决定安装多少技能有参考价值。

**[中] SKILL.md 正文 500 行限制** — 规范建议 SKILL.md 不超过 500 行。指南中未记录。添加为结构章节中的实用性经验法则。

**[中] `name` 必须与父目录名一致** — 规范要求此结构约束。指南记录了 `name` 的字符/格式规则，但遗漏此要求。不一致会导致 `skills-ref validate` 失败。

**[低] 评估存储约定** — 规范定义了标准文件布局：技能文件夹内的 `evals/evals.json` + `my-skill-workspace/iteration-N/with_skill|without_skill/` 存放评估运行结果。指南评估章节未记录。对与 `skill-creator` 元技能的跨工具兼容性很重要。

**来源**：`claudedocs/anthropic-cert/01-agent-skills/agentskills-io-docs.md`（第 2、6、8 节）

---

## 中优先级

### CI/CD 工作流图库 ✅

**已完成**：[GitHub Actions 工作流](./guide/workflows/github-actions.md) — 5 种使用 `anthropics/claude-code-action` 的模式（PR 评审、自动评审、Issue 分类、安全、定时维护）。包含成本控制、fork 安全、Bedrock/Vertex 认证替代方案。从主指南 9.3 节交叉引用。

### MCP 服务器目录

详尽的 MCP 服务器列表及实际用例。

**主题：**

- 按类别划分的可用服务器（开发工具、数据库、API）
- 与原生工具的性能基准对比
- 各服务器的安全信任等级
- 自定义服务器开发模式

**Perplexity 查询：**

```
MCP Model Context Protocol 服务器目录 2024-2025：
- 对开发者最有用的服务器
- MCP vs 原生工具性能对比
- 如何构建自定义 MCP 服务器
```

---

## 低优先级

### CLAUDE.md 模式库

面向常见项目类型的、按技术栈划分的模板。

**主题：**

- React/Next.js 优化配置
- Python/FastAPI 模式
- Go 项目约定
- Monorepo 配置

**Perplexity 查询：**

```
CLAUDE.md 按框架分类的配置示例：
- React、Next.js、Vue 模式
- Python、FastAPI、Django 模式
- GitHub 仓库中的最佳实践
```

---

## 观察中（等待需求）

### prompt-caching MCP 插件

MCP 插件，为使用 Anthropic SDK 构建应用的开发者自动放置 `cache_control`。本地安装在 `/Users/florianbruniaux/Sites/prompt-caching`，通过 `~/.claude.json` 连接到 Claude Code。

**状态：** 测试中。需要实际使用数据后才能决定是否编写文档。

**已知信息：**

- 29 星、v1.3.0、单人维护 — 维护风险
- 作者报告的基准数据（节省 80-92%）— 未验证，不可引用
- 填补真实缺口：没有其他 MCP 工具做到这点；Spring AI / LiteLLM / Pydantic AI 服务不同受众
- 博客文章（Mathieu Grenier）独立记录了同样的痛点 + 5 个反模式 — 评分 3/5，无论结果如何都值得整合到「策略 6」

**待解问题：**

- [ ] 此项目的实际会话是否能命中缓存？（10+ 轮后运行 `get_cache_stats`）
- [ ] 插件是否足够稳定以推荐使用？是否有错误、内存泄漏、会话问题？
- [ ] 在本指南这样包含大量 CLAUDE.md 的项目上，实际节省多少？

**如果测试结果积极（确认缓存命中、无稳定性问题）：**

- 添加到 `guide/ecosystem/third-party-tools.md`，附验证后的数据（非 README 声明）
- 添加到落地页第三方工具区
- 评分升级：3/5 → 4/5

**如果测试结果不明确或插件不稳定：**

- 移至已废弃创意
- 保留 Mathieu Grenier 博客文章整合（独立价值）

**下次检查：** 实际使用一周后

---

### 多 LLM 咨询模式

从 Claude Code 调用外部 LLM（Gemini、GPT-4）作为「第二意见」。

**状态：** 无验证需求。如果收到 3 个以上读者请求则添加。

**已完成调研（2026 年 1 月）：**

- 简单方案：调用 Gemini API 的 Bash 脚本
- 生产方案：[Plano](https://github.com/katanemo/plano)（对个人开发者过度）
- 社区采用率：Claude Code 用户中几乎为零

**如果实施：**

- `examples/scripts/gemini-second-opinion.sh`

### 面向 AI 智能体效率的类型驱动 API 设计

Schema 优先开发对 Claude Code token 消耗的影响。

**状态：** 仅有轶事证据（无实证数据）。如果出现基准测试再重新评估。

**已评估资源（2026 年 2 月）：**

- [ShipTypes](https://shiptypes.com/) by Boris Tane (Cloudflare)
- **评分：** 2/5（边缘）—「类型 → 更少 token」声称未验证
- **完整评估：** `docs/resource-evaluations/shiptypes-evaluation.md`

**缺失内容：**

- 对比 token 消耗的基准测试：类型化 API（tRPC/Zod）vs 非类型化（REST/文档）
- A/B 测试展示 AI 智能体在有/无类型下的迭代次数
- 带有可重现指标的案例研究

**重新评估触发条件：**

- [ ] 带有实证数据（token 消耗指标）的学术论文/博客
- [ ] Anthropic 对 Claude Code 中 Schema 优先的官方推荐
- [ ] 5+ 社区讨论/Issue 请求此主题

**如果验证通过（评分升级至 4/5）：**

- 在 `guide/core/methodologies.md` 中添加子章节（CDD 之后，第 172 行）
- 使用微集成模板：`docs/resource-evaluations/shiptypes-evaluation.md`（「集成计划」节）

**下次检查：** 2026 年 8 月

- 「参见」区 3 行提及
- 不写完整指南（维护负担，范围蔓延）

**来源：** [daily.dev 文章](https://app.daily.dev/posts/make-claude-code-opus-talk-to-gemini-pro-b7pyiq394)

### Vibe Coding 讨论

AI 辅助开发中「开发者即架构师」叙事的演变。

**参考：** [Craig Adam - "Agile is Out, Architecture is Back"](https://medium.com/@craig_32726/agile-is-out-architecture-is-back-7586910ab810)

**状态：** 观察中。术语「vibe coding」已成主流（Collins 2025 年度词汇）。

---

## 已废弃创意

| 创意                       | 废弃原因                                            |
| -------------------------- | --------------------------------------------------- |
| LLM 微调指南               | 超出范围 - 用户无法控制模型训练                     |
| 模型架构内部原理           | 过于理论化，无法落地                                |
| Token 定价优化             | 变化太快，参考官方文档即可                          |
| A2A 协议（智能体对智能体） | Claude Code 是单智能体 + 子智能体，非真正的多智能体 |
| AgentOps 企业仪表盘        | CLI 工具没有对应基础设施                            |
| LLM-as-a-Judge 评估        | 对 CLI 过度，增加延迟却无相应价值                   |
| 决策轨迹日志               | 无法访问内部追踪（黑盒）                            |
| 四大支柱形式框架           | 过于学术 - 指南已务实覆盖各类症状                   |
| 金丝雀/蓝绿部署            | 基础设施模式，与 CLI 不相关                         |
| 内存投毒防御               | 理论风险，需先存在系统失陷前提                      |
| 面向代码生成的提示词工程   | 已充分覆盖（xml_prompting、prompt_formula）         |
| 上下文窗口优化             | 已充分覆盖（context_management、context_triage）    |
| 任务分解模式               | 已通过 plan_mode、interaction_loop 覆盖             |
| 智能体架构对比             | 超出范围 - 非多智能体理论                           |
| 真实案例研究               | 指标不可验证，易带营销性质                          |
| 与其他工具对比             | 超出范围，快速过时                                  |

---

## 贡献

发现有意思的内容？按以下格式添加：

1. 主题名称及其价值
2. 具体研究问题
3. 启动调研的 Perplexity 查询
