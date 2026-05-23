---
title: "Claude Code — 开发工作流程图"
description: "TDD 周期、规范优先管线、计划驱动工作流、迭代优化循环"
tags: [workflows, tdd, spec-first, plan-driven, iterative]
---

# 开发工作流

组织 AI 辅助开发会话的成熟模式。

---

### 与 Claude 一起 TDD 红-绿-重构

为 Claude Code 调整的测试驱动开发：先编写失败测试，然后让 Claude 仅实现通过测试所需的代码。这可以防止过度工程化，并确保测试真正验证了行为。

```mermaid
flowchart TD
    A([Start: New feature needed]) --> B(Write failing test<br/>with human)
    B --> C(Run tests)
    C --> D{Tests fail<br/>as expected?}
    D -->|No: tests pass<br/>before impl!| E(Fix test — it's too weak)
    E --> B
    D -->|Yes: RED ✓| F(Ask Claude to implement<br/>minimal code to pass)
    F --> G(Run tests again)
    G --> H{Tests pass?}
    H -->|No| I(Diagnose with Claude<br/>fix implementation)
    I --> G
    H -->|Yes: GREEN ✓| J{Code needs<br/>refactoring?}
    J -->|Yes| K(Refactor with Claude)
    K --> L(Run tests: still green?)
    L -->|No| I
    L -->|Yes: REFACTOR ✓| M{More features<br/>needed?}
    J -->|No| M
    M -->|Yes| B
    M -->|No| N([Feature complete ✓])

    style B fill:#E85D5D,color:#fff
    style F fill:#E85D5D,color:#fff
    style D fill:#E87E2F,color:#fff
    style H fill:#E87E2F,color:#fff
    style J fill:#E87E2F,color:#fff
    style G fill:#7BC47F,color:#333
    style K fill:#6DB3F2,color:#fff
    style N fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "TDD — New feature"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Write failing test (RED)"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Run tests"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Tests fail as expected?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Fix test — too weak"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Claude implements minimal code"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Run tests again"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Tests pass? (GREEN)"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Diagnose with Claude"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Code needs refactoring?"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Refactor with Claude"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Run tests: still green?"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "More features needed?"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md" "Feature complete ✓"
```

<details>
<summary>ASCII version</summary>

```
Write failing test (RED)
        │
    Run tests
        │
  Fail as expected?
  ├─ No  → Fix test (too weak)
  └─ Yes → Ask Claude: implement minimal code
                │
           Run tests
                │
           Pass? (GREEN)
           ├─ No  → Diagnose + fix
           └─ Yes → Refactor?
                    ├─ Yes → Refactor (REFACTOR) → re-run tests
                    └─ No  → Next feature
```

</details>

> **Source**: [TDD with Claude](../workflows/tdd-with-claude.md)

---

### 规范优先开发管线

先写规范再写代码。Claude 以规范为唯一真理来源——防止计划与实际构建之间的偏差。

```mermaid
flowchart LR
    A([Idea / Requirement]) --> B(Write spec.md<br/>in natural language)
    B --> C(Claude reviews spec<br/>for clarity + completeness)
    C --> D{Spec approved<br/> by human?}
    D -->|No: gaps found| E(Refine spec<br/>address gaps)
    E --> C
    D -->|Yes| F(Generate tests<br/>from spec)
    F --> G(Generate implementation<br/>from spec + tests)
    G --> H(Run test suite)
    H --> I{All tests<br/>pass?}
    I -->|No| J(Claude fixes<br/>implementation)
    J --> H
    I -->|Yes| K(Human review<br/>spec vs output)
    K --> L{Matches<br/>spec?}
    L -->|No| M(Update spec<br/>or implementation)
    M --> K
    L -->|Yes| N([Merge ✓])

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style D fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style L fill:#E87E2F,color:#fff
    style N fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Idea / Requirement"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Write spec.md"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Claude reviews spec"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Spec approved by human?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Refine spec"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Generate tests from spec"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Generate implementation"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Run test suite"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "All tests pass?"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Claude fixes implementation"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Human review"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Matches spec?"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Update spec or implementation"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/spec-first.md" "Merge ✓"
```

<details>
<summary>ASCII version</summary>

```
Idea → Write spec.md → Claude reviews
                             │
                       Approved? ─No→ Refine spec
                             │ Yes
                       Generate tests from spec
                             │
                       Generate implementation
                             │
                       Run tests → Pass? ─No→ Claude fixes
                             │ Yes
                       Human review → Matches spec? ─No→ Fix
                             │ Yes
                           Merge ✓
```

</details>

> **Source**: [Spec-First Development](../workflows/spec-first.md)

---

### 带标注的计划驱动工作流

复杂任务受益于计划模式：Claude 探索代码库、提出计划、你进行标注、然后 Claude 仅执行批准的内容。避免大型重构中的意外。

```mermaid
flowchart TD
    A([Complex task given]) --> B(Enter Plan Mode<br/>Shift+Tab × 2)
    B --> C(Claude explores<br/>codebase structure)
    C --> D(Claude proposes plan<br/>with file list)
    D --> E(Human reviews plan)
    E --> F{Plan<br/>acceptable?}
    F -->|No: issues found| G(Human annotates plan<br/>marks corrections)
    G --> H(Claude revises plan)
    H --> E
    F -->|Yes| I(Approve plan<br/>Exit Plan Mode)
    I --> J(Claude executes<br/>step by step)
    J --> K(Claude reports<br/>progress)
    K --> L{Unexpected<br/>issue?}
    L -->|Yes| M(Claude flags issue<br/>asks for guidance)
    M --> F
    L -->|No| N{All steps<br/>complete?}
    N -->|No| J
    N -->|Yes| O([Task done ✓])

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style F fill:#E87E2F,color:#fff
    style L fill:#E87E2F,color:#fff
    style N fill:#E87E2F,color:#fff
    style G fill:#F5E6D3,color:#333
    style O fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Complex task given"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#23-plan-mode" "Enter Plan Mode"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Claude explores codebase"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Claude proposes plan"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Human reviews plan"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Plan acceptable?"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Human annotates plan"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Claude revises plan"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#23-plan-mode" "Approve plan — Exit Plan Mode"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Claude executes step by step"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Claude reports progress"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Unexpected issue?"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Claude flags issue"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "All steps complete?"
    click O href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/plan-driven.md" "Task done ✓"
```

<details>
<summary>ASCII version</summary>

```
Complex task
     │
Plan Mode (Shift+Tab×2)
     │
Claude explores codebase
     │
Claude proposes plan
     │
Human reviews ──No──► Annotate + Claude revises ──► re-review
     │ Yes
Approve + exit plan mode
     │
Claude executes step by step
     │
Unexpected? ──Yes──► Flag + ask guidance
     │ No
Done? ──No──► continue
     │ Yes
Complete ✓
```

</details>

> **Source**: [Plan-Driven Workflow](../workflows/plan-driven.md)

---

### 迭代优化循环

输出很少能在第一次尝试时就达到目标。这个循环提供了一种系统性的方法，通过有针对性的反馈来改进结果，而不是依赖「做得更好」这种模糊指令。

```mermaid
flowchart TD
    A([Initial prompt]) --> B(Claude generates output)
    B --> C(Evaluate output quality)
    C --> D{Good<br/>enough?}
    D -->|Yes| E([Done ✓])
    D -->|No| F(Identify specific issue<br/>What exactly is wrong?)
    F --> G{Issue type?}
    G -->|Style/tone| H(Add: style constraints)
    G -->|Missing info| I(Add: provide missing context)
    G -->|Wrong approach| J(Add: redirect approach)
    G -->|Too verbose/brief| K(Add: length constraint)
    H --> L(Refine instruction)
    I --> L
    J --> L
    K --> L
    L --> M(Claude refines output)
    M --> N(Compare before/after)
    N --> O{Improvement<br/>detected?}
    O -->|Yes| C
    O -->|No| P(Different<br/>approach needed)
    P --> F

    style A fill:#F5E6D3,color:#333
    style D fill:#E87E2F,color:#fff
    style G fill:#E87E2F,color:#fff
    style O fill:#E87E2F,color:#fff
    style E fill:#7BC47F,color:#333
    style L fill:#6DB3F2,color:#fff
    style P fill:#E85D5D,color:#fff

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Initial prompt"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Claude generates output"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Evaluate output quality"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Good enough?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Done ✓"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Identify specific issue"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Issue type?"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Add style constraints"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Provide missing context"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Redirect approach"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Add length constraint"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Refine instruction"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Claude refines output"
    click N href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Compare before/after"
    click O href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Improvement detected?"
    click P href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Different approach needed"
```

<details>
<summary>ASCII version</summary>

```
Prompt → Output → Evaluate → Good? ──Yes──► Done
                                 │ No
                          Identify specific issue
                                 │
                          ┌──────┴──────────────┐
                         Style  Missing  Wrong  Length
                          └──────┬──────────────┘
                          Refine instruction
                                 │
                          Claude refines
                                 │
                          Better? ──Yes──► Evaluate again
                                 │ No
                          Different approach
```

</details>

> **Source**: [Iterative Refinement](../workflows/iterative-refinement.md) — Line ~347

---

### AI 流畅度——高流畅度与低流畅度路径

当 Claude 生成看似完美的输出时，一种认知偏差就会起作用：输出看起来越完整，大多数用户就越少批判性地评估它。这就是「工件悖论」，经 Anthropic 在 9,830 次对话中记录验证。该图展示了将 30% 的高流畅度用户与 70% 接受首次输出的用户区分开来的因素——以及结果质量上可衡量的差异。

```mermaid
flowchart TD
    A([User sends request to Claude]) --> B(Claude generates output<br/>code · file · config · plan)
    B --> C["⚠️ Artifact Paradox<br/>Polished output triggers<br/>cognitive acceptance bias"]

    C -->|"70% of users"| D(Accept first output<br/>without critical review)
    C -->|"30% of users"| E(Iterate + question<br/>define collaboration scope)

    D --> D1["Fluency behaviors drop:<br/>−5.2pp gap identification<br/>−3.7pp fact-checking<br/>−3.1pp reasoning challenge"]
    D1 --> D2([Silent defects · missed requirements])

    E --> E1("Challenge the output:<br/>'What did you miss?<br/>What assumptions made?'")
    E1 --> E2(Identify gaps<br/>Refine with full context)
    E2 --> E3{Satisfied?}
    E3 -->|No — iterate again| E1
    E3 -->|Yes| E4([Verified, robust output ✓])

    E4 --> G["Measured impact:<br/>5.6× more issue catches<br/>2.67 vs 1.33 avg behaviors<br/>Source: Anthropic AI Fluency Index, 2026"]

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#E85D5D,color:#fff
    style D fill:#E85D5D,color:#fff
    style D1 fill:#E85D5D,color:#fff
    style D2 fill:#E85D5D,color:#fff
    style E fill:#7BC47F,color:#333
    style E1 fill:#6DB3F2,color:#fff
    style E2 fill:#6DB3F2,color:#fff
    style E3 fill:#E87E2F,color:#fff
    style E4 fill:#7BC47F,color:#333
    style G fill:#7BC47F,color:#333

    click A href "https://www.anthropic.com/research/AI-fluency-index" "AI Fluency Index — Anthropic 2026"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#common-pitfalls--best-practices" "Claude generates output"
    click C href "https://www.anthropic.com/research/AI-fluency-index" "Artifact Paradox — Anthropic AI Fluency Index"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#common-pitfalls--best-practices" "Accept without review"
    click D1 href "https://www.anthropic.com/research/AI-fluency-index" "Fluency behaviors drop"
    click D2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#common-pitfalls--best-practices" "Silent defects"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#23-plan-mode" "Iterate and question"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#rev-the-engine" "Challenge the output"
    click E2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Identify gaps and refine"
    click E3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Satisfied?"
    click E4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/iterative-refinement.md" "Verified output"
    click G href "https://www.anthropic.com/research/AI-fluency-index" "Measured impact — AI Fluency Index"
```

<details>
<summary>ASCII version</summary>

```
User request → Claude output (code · file · config · plan)
                        ↓
              ⚠️ Artifact Paradox
          Polished output → cognitive bias
                        ↓
    ┌───────────────────┴──────────────────────┐
70% of users                            30% of users
Accept without review               Iterate + question
        ↓                                     ↓
Fluency behaviors drop:         Challenge: "What did you miss?
−5.2pp gap identification                What assumptions made?"
−3.7pp fact-checking                          ↓
−3.1pp reasoning challenge      Identify gaps → refine
        ↓                                     ↓
Silent defects                  Satisfied? ──No──► iterate
                                            ↓ Yes
                                Verified output ✓
                                            ↓
                               5.6× more issue catches
                               2.67 vs 1.33 avg behaviors
```

</details>

> **Source**: [Anthropic AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index) (Swanson et al., 2026-02-23) — [Guide section: Common Pitfalls](../ultimate-guide.md#common-pitfalls--best-practices)
