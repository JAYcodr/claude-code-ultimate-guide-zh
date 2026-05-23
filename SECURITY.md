# 安全策略

## 范围

本仓库包含 Claude Code 的**文档和教育模板**。不包含处理用户输入或在生产环境中运行的可执行代码。

**与本仓库相关的安全问题：**

- 安全实践的文档准确性
- 模板代码质量和安全模式
- 威胁数据库完整性（[`machine-readable/threat-db.yaml`](./machine-readable/threat-db.yaml)）

**不在范围内：**

- Claude Code CLI 本身的安全漏洞 → 向 [Anthropic](https://github.com/anthropics/claude-code/security) 报告
- MCP 服务器的安全问题 → 向相关服务器维护者报告

## 报告安全问题

如果你发现与本指南相关的安全问题（示例：恶意模板、错误的安全建议、威胁数据库不准确），请：

1. **发送邮件**：`florian.bruniaux@methode-aristote.fr`
   - 主题：`[SECURITY] Claude Code Guide - 简要描述`
   - 包含：受影响的文件/章节、描述、影响评估

2. **GitHub 私下披露**：使用 [安全公告](../../security/advisories/new) 报告敏感问题

**响应 SLA**：我们力争 48 小时内响应，关键问题 7 天内发布修复。

## 安全资源

本指南维护全面的安全文档：

- **[安全加固指南](./guide/security-hardening.md)** — MCP 审核、注入防御、审计工作流
- **[威胁数据库](./machine-readable/threat-db.yaml)** — 18 个 CVE、341 个恶意技能
- **[安全钩子](./examples/hooks/)** — 30 个生产环境钩子（bash + PowerShell）
- **[安全命令](./examples/skills/)** — `/security-check`、`/security-audit`、`/update-threat-db`

## 安全维护

**威胁数据库更新**：威胁情报数据库基于以下来源更新：

- CVE 公告和安全通告
- 社区报告的恶意技能/MCP 服务器
- Anthropic 安全公告
- 学术研究（例如提示词注入论文）

**审计计划**：

- 每周审核新的 MCP 服务器和技能
- 每月审计安全文档准确性
- 每季度全面刷新威胁数据库

**最后更新**：2026-02-11 (v3.26.0)

## 协同披露

如果你是安全研究员，发现影响 Claude Code 生态中多个仓库的问题：

1. 先通过邮件联系我们（推荐协同披露）
2. 如有需要，我们将协调其他维护者
3. 公开披露时间：90 天或修复后，以先到者为准

## 致谢

感谢通过负责任的披露帮助改进本指南安全内容的安全研究员。

---

**作者**：[Florian BRUNIAUX](https://github.com/FlorianBruniaux) | 创始工程师 [@Méthode Aristote](https://methode-aristote.fr)

**指南协议**：[CC BY-SA 4.0](./LICENSE)
