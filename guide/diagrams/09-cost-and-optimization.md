---
title: "Claude Code — 成本与优化图解"
description: "模型选择、成本优化、订阅层级、Token 缩减策略"
tags: [cost, optimization, models, tokens, subscription]
---

# 成本与优化

如何在控制 Token 消耗和成本的同时，从 Claude Code 中获得最大价值。

---

### 模型选择决策流程

并非所有任务都需要最强大的模型。为合适的任务选择合适的模型，可在不牺牲质量的前提下将成本降低 5-10 倍。

> **此图解假定预算不受限制（Max/API）。** 在预算较为紧张的计划（Pro、Teams Standard）中，请应用下方的预算调整器。

```mermaid
flowchart TD
    A([Task to complete]) --> B{Task complexity?}

    B -->|Simple| C["Simple tasks:<br/>typo fixes, renames,<br/>formatting, translations"]
    C --> D([Haiku 4.5<br/>💰 Cheapest, fastest<br/>~5x cheaper than Sonnet])

    B -->|Standard| E["Standard tasks:<br/>feature implementation,<br/>bug fixes, refactoring"]
    E --> F([Sonnet 4.5/4.6<br/>💰💰 Balanced<br/>Best price/quality ratio])

    B -->|Complex| G{Needs deep<br/>reasoning?}
    G -->|Yes| H["Complex tasks:<br/>architecture decisions,<br/>security review,<br/>multi-file analysis"]
    H --> I([Opus 4.7 — Maximum capability xhigh<br/>Opus 4.6 — Deep analysis<br/>💰💰💰 Most capable<br/>~5x more than Sonnet])

    G -->|No: just large| J["Large but clear tasks:<br/>big refactors,<br/>doc generation"]
    J --> F

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style G fill:#E87E2F,color:#fff
    style D fill:#7BC47F,color:#333
    style F fill:#6DB3F2,color:#fff
    style I fill:#E87E2F,color:#fff
    style C fill:#B8B8B8,color:#333
    style E fill:#B8B8B8,color:#333
    style H fill:#B8B8B8,color:#333
    style J fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Task to complete"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Task complexity?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Simple tasks"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Haiku 4.5"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Standard tasks"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Sonnet 4.5/4.6"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Needs deep reasoning?"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Complex tasks"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Opus 4.7 / Opus 4.6 / Sonnet + --think-hard"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Large but clear tasks"
```

> **定价**：展示的是相对成本 — 请查阅 [anthropic.com/pricing](https://www.anthropic.com/pricing) 了解当前费率。

**预算调整器** — 在受限计划中，每个阶段降级一层：

| 计划 | 规划阶段 | 实施阶段 |
|------|---------------|---------------------|
| **Max / API unconstrained (xhigh)** | Opus 4.7 | Sonnet |
| **Max / API unconstrained** | Opus 4.6 | Sonnet |
| **Pro / Teams Standard** | Sonnet | Haiku (mechanical tasks) |
| **API tight budget** | Sonnet | Haiku |

> *社区实践模式（Teams Standard $25/月）：Sonnet 用于规划 → Haiku 用于实施。在机械性任务上以极低成本获得相同质量的输出。*

<details>
<summary>ASCII version</summary>

```
Task complexity?
├─ Simple (typos, format, rename) → Haiku 4.5       ($  — ~5x cheaper than Sonnet)
├─ Standard (features, bugs)      → Sonnet 4.5/4.6  ($$ — best price/quality ratio)
└─ Complex (architecture, sec.)
   ├─ Needs deep reasoning?        → Opus 4.7 (xhigh) / Opus 4.6  ($$$ — ~5x more than Sonnet)
   └─ Just large/clear?            → Sonnet 4.6                    ($$ — handles it)

Budget modifier (downgrade one tier on constrained plans):
  Max/API (xhigh)  → Opus 4.7 plan, Sonnet impl
  Max/API          → Opus 4.6 plan, Sonnet impl
  Pro/Teams        → Sonnet plan, Haiku impl (mechanical tasks)
```

</details>

> **Source**: [Model Selection](../ultimate-guide.md#model-selection) — Line ~2634

---

### 成本优化决策树

高 Token 成本通常是可以解决的。本系统化决策树帮助识别根本原因，并为每种浪费模式指出正确的修复方法。

```mermaid
flowchart TD
    A([High token costs?]) --> B{Context<br/>too large?}
    B -->|Yes| C(Use /compact<br/>or start fresh session)
    C --> Z([Saves 40-60%<br/>per session])

    B -->|No| D{Verbose<br/>responses?}
    D -->|Yes| E(Add CLAUDE.md instruction:<br/>'Be concise, avoid explanations')
    E --> Z2([Saves 20-30%])

    D -->|No| F{Re-explaining<br/>context repeatedly?}
    F -->|Yes| G(Move repeated context<br/>to CLAUDE.md)
    G --> Z3([Saves 15-25%])

    F -->|No| H{Using wrong<br/>model for task?}
    H -->|Yes| I(Use Haiku for simple tasks<br/>See model selection tree)
    I --> Z4([Saves 50-90%<br/>on simple tasks])

    H -->|No| J{MCP server<br/>noisy output?}
    J -->|Yes| K(Review MCP verbosity<br/>Filter tool output)
    K --> Z5([Saves 10-20%])

    J -->|No| L([Baseline cost<br/>acceptable])

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style F fill:#E87E2F,color:#fff
    style H fill:#E87E2F,color:#fff
    style J fill:#E87E2F,color:#fff
    style Z fill:#7BC47F,color:#333
    style Z2 fill:#7BC47F,color:#333
    style Z3 fill:#7BC47F,color:#333
    style Z4 fill:#7BC47F,color:#333
    style Z5 fill:#7BC47F,color:#333
    style L fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "High token costs?"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Context too large?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Use /compact or start fresh"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Verbose responses?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Add CLAUDE.md instruction"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Re-explaining context?"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Move context to CLAUDE.md"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Wrong model?"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Use Haiku for simple tasks"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Noisy MCP output?"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Review MCP verbosity"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Baseline cost acceptable"
    click Z href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 40-60%"
    click Z2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 20-30%"
    click Z3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 15-25%"
    click Z4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 50-90%"
    click Z5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 10-20%"
```

<details>
<summary>ASCII version</summary>

```
High costs?
├─ Context too large?      → /compact or new session    (40-60% saving)
├─ Verbose responses?      → CLAUDE.md: be concise      (20-30% saving)
├─ Repeating context?      → Move to CLAUDE.md          (15-25% saving)
├─ Wrong model?            → Use Haiku for simple tasks (50-90% saving)
├─ Noisy MCP output?       → Filter tool output         (10-20% saving)
└─ None of the above?      → Baseline cost, acceptable
```

</details>

> **努力程度滑块** — `/effort xlow/low/default/high/xhigh`（v2.1.111）可让你按任务调整思考深度。努力程度越低，思考消耗的 Token 越少。与模型选择结合使用，实现细粒度的成本控制。

> **Source**: [Cost Optimization](../ultimate-guide.md#cost-optimization) — Line ~8878

---

### 订阅层级 — 各层解锁能力

不同层级解锁不同的 Claude Code 功能。了解各层限制有助于规划使用量并合理论证升级需求。

```mermaid
flowchart LR
    subgraph FREE["Free Tier"]
        F1[Claude.ai web only]
        F2[Limited messages/day]
        F3[❌ No Claude Code CLI]
        F4[❌ No parallel sessions]
    end

    subgraph PRO["Pro ($20/mo)"]
        P1[Claude Code CLI ✓]
        P2[Limited usage<br/>~1x baseline]
        P3[Personal projects]
        P4[❌ No parallel sessions<br/>out of the box]
    end

    subgraph MAX["Max ($100-200/mo)"]
        M1[Claude Code CLI ✓]
        M2[5x-20x more usage]
        M3[Parallel sessions ✓]
        M4[Priority access ✓]
    end

    subgraph TEAM["Team / Enterprise"]
        T1[Per-seat pricing]
        T2[Admin controls ✓]
        T3[Usage analytics ✓]
        T4[SSO + compliance ✓]
        T5[Audit logs ✓]
    end

    style F3 fill:#E85D5D,color:#fff
    style F4 fill:#E85D5D,color:#fff
    style P4 fill:#E87E2F,color:#fff
    style P1 fill:#7BC47F,color:#333
    style M1 fill:#7BC47F,color:#333
    style M2 fill:#7BC47F,color:#333
    style M3 fill:#7BC47F,color:#333
    style M4 fill:#7BC47F,color:#333
    style T1 fill:#6DB3F2,color:#fff
    style T2 fill:#6DB3F2,color:#fff
    style T3 fill:#6DB3F2,color:#fff
    style T4 fill:#6DB3F2,color:#fff
    style T5 fill:#6DB3F2,color:#fff

    click F1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Free: Claude.ai web only"
    click F2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Free: Limited messages"
    click F3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Free: No CLI"
    click F4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Free: No parallel sessions"
    click P1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Pro: Claude Code CLI"
    click P2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Pro: Limited usage"
    click P3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Pro: Personal projects"
    click P4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Pro: No parallel sessions"
    click M1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Max: Claude Code CLI"
    click M2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Max: 5x-20x usage"
    click M3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Max: Parallel sessions"
    click M4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Max: Priority access"
    click T1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Team: Per-seat pricing"
    click T2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Team: Admin controls"
    click T3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Team: Usage analytics"
    click T4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Team: SSO + compliance"
    click T5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Team: Audit logs"
```

<details>
<summary>ASCII version</summary>

```
FREE         PRO ($20)        MAX ($100-200)   TEAM/Enterprise
────         ─────────        ──────────────   ───────────────
Web only     CLI ✓            CLI ✓            Per-seat
Limited msgs Limited usage    5-20x usage      Admin controls
No CLI       Personal use     Parallel ✓       Analytics
             No parallel      Priority ✓       SSO + compliance
```

</details>

> **Source**: [Subscription Tiers](../ultimate-guide.md#subscription-tiers) — Line ~1933

---

### Token 缩减策略管道

多项策略可叠加使用，实现累积的 Token 节省。按从最高收益到最低投入的顺序依次应用。

```mermaid
flowchart LR
    BASE([Baseline:<br/>100% tokens]) --> RTK

    subgraph RTK["Strategy 1: RTK Proxy"]
        R1[Raw CLI output<br/>→ filtered output]
        R2["git status, cargo test,<br/>pnpm list → compressed"]
        R3[Saves 60-90%<br/>on CLI commands]
    end

    RTK --> COMP

    subgraph COMP["Strategy 2: /compact"]
        C1[Long conversation<br/>→ summarized]
        C2[Keep decisions,<br/>drop verbose reasoning]
        C3[Saves 40-60%<br/>at checkpoint]
    end

    COMP --> CLAUDE_MD

    subgraph CLAUDE_MD["Strategy 3: CLAUDE.md"]
        CM1[Repeated context<br/>→ persistent instructions]
        CM2[No re-explaining<br/>project conventions]
        CM3[Saves 15-25%<br/>per session]
    end

    CLAUDE_MD --> MODEL

    subgraph MODEL["Strategy 4: Model Selection"]
        MO1[Haiku for simple tasks<br/>instead of Sonnet]
        MO2[Same quality output<br/>at fraction of cost]
        MO3[Saves 50-90%<br/>on simple tasks]
    end

    MODEL --> RESULT([Optimized:<br/>10-20% of baseline<br/>for typical usage])

    style BASE fill:#E85D5D,color:#fff
    style R3 fill:#7BC47F,color:#333
    style C3 fill:#7BC47F,color:#333
    style CM3 fill:#7BC47F,color:#333
    style MO3 fill:#7BC47F,color:#333
    style RESULT fill:#7BC47F,color:#333

    click BASE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Baseline: 100% tokens"
    click R1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Raw CLI output filtered"
    click R2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "RTK commands"
    click R3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 60-90% on CLI"
    click C1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Long conversation summarized"
    click C2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Keep decisions"
    click C3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 40-60% at checkpoint"
    click CM1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Repeated context persistent"
    click CM2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "No re-explaining conventions"
    click CM3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Saves 15-25% per session"
    click MO1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Haiku for simple tasks"
    click MO2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Same quality at lower cost"
    click MO3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#25-model-selection--thinking-guide" "Saves 50-90% on simple"
    click RESULT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#913-cost-optimization-strategies" "Optimized: 10-20% of baseline"
```

<details>
<summary>ASCII version</summary>

```
100% baseline
    │
RTK proxy (CLI output compression)  → -60-90% on CLI ops
    │
/compact (conversation summarization) → -40-60% at checkpoint
    │
CLAUDE.md (avoid repeated context)    → -15-25% per session
    │
Model selection (Haiku for simple)    → -50-90% on simple tasks
    │
~10-20% of baseline for typical usage
```

</details>

> **跟踪用量** — 使用 `/usage` 监控 Token 消耗和成本（自 v2.1.118 起替代 `/cost`；`/cost` 仍为有效别名）。

> **Source**: [Token Optimization](../ultimate-guide.md#token-optimization) — Line ~13355
