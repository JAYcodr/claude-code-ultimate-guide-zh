---
title: "Claude Code — 企业治理图解"
description: "治理风险层级、MCP 审批工作流、护栏层级选择"
tags: [security, enterprise, governance, compliance, mcp]
---

# 企业治理

团队大规模部署 Claude Code 的组织级模式——使用层级、MCP 审批工作流和护栏配置。

> **目标读者**：技术负责人、工程经理、安全负责人。个人开发者安全请参阅[安全与生产](./08-security-and-production.md)。

---

### 治理风险层级 — 控制什么以及何时控制

并非所有内容都需要严格治理。本决策树根据实际风险将你的上下文引导至正确的控制级别——从个人开发者工作流（最少控制）到受管控环境（完整合规堆栈）。

```mermaid
flowchart TD
    A([What are you governing?]) --> B{Usage context?}

    B --> P["Personal dev workflow<br/>Local, throwaway code<br/>One developer only"]
    B --> T["Team codebase<br/>Shared repo, not production<br/>5–20 developers"]
    B --> PR["Production system<br/>Customer-facing, real data<br/>Any team size"]
    B --> REG["Regulated environment<br/>HIPAA, SOC2, PCI, finance<br/>Legal/compliance obligations"]

    P --> TIER1(["Tier 1: Starter<br/>CLAUDE.md guidelines<br/>+ dangerous-actions-blocker hook<br/>10 min setup"])
    T --> TIER2(["Tier 2: Standard<br/>Shared settings.json + MCP registry<br/>+ PR gates + audit log<br/>~2 hours setup"])
    PR --> TIER3(["Tier 3: Strict<br/>Full permission deny list<br/>+ approval workflow<br/>+ session audit trail"])
    REG --> TIER4(["Tier 4: Regulated<br/>All of above<br/>+ compliance audit trail<br/>+ SOC2/ISO27001 controls"])

    NOTE["You CAN control: MCP servers, tool permissions,<br/>CLAUDE.md content, hooks, CI/CD gates<br/>You CANNOT control: personal ~/.claude settings,<br/>models on personal API keys, personal projects"] -.-> B

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style P fill:#B8B8B8,color:#333
    style T fill:#6DB3F2,color:#fff
    style PR fill:#E87E2F,color:#fff
    style REG fill:#E85D5D,color:#fff
    style TIER1 fill:#7BC47F,color:#333
    style TIER2 fill:#7BC47F,color:#333
    style TIER3 fill:#E87E2F,color:#fff
    style TIER4 fill:#E85D5D,color:#fff
    style NOTE fill:#F5E6D3,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#1-local-vs-shared-the-governance-split" "What are you governing?"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#1-local-vs-shared-the-governance-split" "Usage context?"
    click P href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Personal dev workflow"
    click T href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Team codebase"
    click PR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Production system"
    click REG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Regulated environment"
    click TIER1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Tier 1: Starter"
    click TIER2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Tier 2: Standard"
    click TIER3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Tier 3: Strict"
    click TIER4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#4-guardrail-tiers" "Tier 4: Regulated"
    click NOTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#12-what-you-can-and-cant-control" "What you can/cannot control"
```

<details>
<summary>ASCII version</summary>

```
Usage context?
├─ Personal dev workflow      → Tier 1: Starter     (CLAUDE.md + basic hooks, 10 min)
├─ Team codebase              → Tier 2: Standard    (shared settings.json + MCP registry + PR gates)
├─ Production system          → Tier 3: Strict      (full deny list + approval + audit trail)
└─ Regulated (HIPAA/SOC2/PCI) → Tier 4: Regulated  (all above + compliance audit trail)

You CAN control: settings.json in repo, CLAUDE.md, hooks, CI/CD gates, MCP registry
You CANNOT control: personal ~/.claude, personal API key model choice, personal projects
```

</details>

> **Source**: [Enterprise Governance](../security/enterprise-governance.md) — §1 Governance Split, §4 Guardrail Tiers

---

### MCP 治理工作流

单个 MCP 审查只需 5 分钟。组织级 MCP 治理是一个 5 步流水线，确保已批准的服务器保持批准状态、版本被锁定、风险在部署前已分类。

```mermaid
sequenceDiagram
    participant DEV as Developer
    participant TL as Tech Lead + Security
    participant REG as MCP Registry<br/>.claude/mcp-registry.yaml
    participant REPO as Shared Config Repo<br/>settings.json

    DEV->>TL: Submit MCP request<br/>Name, source URL, use case, data scope

    TL->>TL: 5-min security audit<br/>Stars >50? Recent commits?<br/>CVEs? Dangerous flags?
    TL->>TL: Classify risk: LOW / MEDIUM / HIGH

    alt LOW risk
        TL->>REG: Approve — add to registry<br/>Pin version, set 6-month expiry
    else MEDIUM or HIGH risk
        TL->>TL: 2-week sandbox trial<br/>+ Security team sign-off
        TL->>REG: Approve with restrictions<br/>Shorter expiry (3 months)
    else HIGH risk (unacceptable)
        TL->>DEV: Denied — document reason in registry
    end

    REG->>REPO: Deploy via committed settings.json<br/>No local overrides for approved MCPs
    Note over REPO: Version-pinned, team-wide, auditable

    REPO->>TL: Monitor every 30 days<br/>Patch bumps: auto re-approve<br/>Minor+ bumps: manual re-review<br/>Quarterly: full registry audit
```

<details>
<summary>ASCII version</summary>

```
Developer submits MCP request (name, source, use case, data scope)
    │
Tech Lead: 5-min security audit (stars, commits, CVEs, flags)
    │
Classify risk: LOW / MEDIUM / HIGH
    │
┌───┴────────────────────────────┐
LOW                             MED/HIGH
Approve immediately             2-week sandbox trial
                                + Security team sign-off
    │
Add to registry (.claude/mcp-registry.yaml)
  - Pin exact version
  - Set expiry (6 months for LOW, 3 months for MED)
  - Document approved scope
    │
Deploy via committed settings.json (no local overrides)
    │
Monitor every 30 days:
  - Check security advisories
  - Patch bumps: auto | Minor+ bumps: manual re-review
  - Quarterly: full registry audit
```

</details>

> **Source**: [MCP Governance Workflow](../security/enterprise-governance.md#3-mcp-governance-workflow) — §3.1 Approval Workflow

---

### 数据分类与 Claude Code 访问规则

数据分类决定了允许 Claude Code 读取和处理哪些内容。在这方面犯错是影响最大的治理失败。四个级别，明确规则，RESTRICTED 级别无例外。

```mermaid
flowchart LR
    subgraph PUBLIC["🟢 PUBLIC"]
        PU1["Open source code<br/>Public documentation<br/>Shared blog content"]
        PU2(["Allowed — no restrictions"])
    end

    subgraph INTERNAL["🔵 INTERNAL"]
        IN1["Internal tools<br/>Non-sensitive code<br/>Team documentation"]
        IN2(["Allowed — standard config"])
    end

    subgraph CONFIDENTIAL["🟠 CONFIDENTIAL"]
        CO1["Internal business secrets<br/>Non-regulated IP<br/>Architecture docs"]
        CO2(["Enterprise plan only<br/>Zero Data Retention required"])
    end

    subgraph RESTRICTED["🔴 RESTRICTED"]
        RE1["Customer PII<br/>PCI card data / PHI<br/>Credentials & API keys"]
        RE2(["NEVER in AI context<br/>Block via permissions.deny<br/>No exceptions"])
    end

    PU1 --> PU2
    IN1 --> IN2
    CO1 --> CO2
    RE1 --> RE2

    style PU2 fill:#7BC47F,color:#333
    style IN2 fill:#6DB3F2,color:#fff
    style CO2 fill:#E87E2F,color:#fff
    style RE2 fill:#E85D5D,color:#fff
    style RE1 fill:#E85D5D,color:#fff

    click PU1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "PUBLIC data"
    click IN1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "INTERNAL data"
    click CO1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "CONFIDENTIAL data"
    click RE1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "RESTRICTED data"
    click PU2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "PUBLIC: allowed"
    click IN2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "INTERNAL: standard config"
    click CO2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "CONFIDENTIAL: Enterprise only"
    click RE2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/enterprise-governance.md#2-ai-usage-charter" "RESTRICTED: never in AI context"
```

<details>
<summary>ASCII version</summary>

```
PUBLIC       → Allowed, no restrictions
INTERNAL     → Allowed, standard config
CONFIDENTIAL → Enterprise plan only (Zero Data Retention required)
RESTRICTED   → NEVER in AI context (PII, PCI, PHI, credentials)
               Block via: permissions.deny Read(.env, *.key, *.pem, secrets/**)

Hard rule: RESTRICTED data never enters a context window.
Not in prompts, not in files Claude reads, not as examples.
```

</details>

> **Source**: [AI Usage Charter](../security/enterprise-governance.md#2-ai-usage-charter) — §2.1 Data Classification
