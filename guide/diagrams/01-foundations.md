---
title: "Claude Code — 基础原理图解"
description: "核心概念：四层模型、工作流管道、决策树、五种权限模式"
tags: [foundations, architecture, getting-started]
---
# 基础原理
Claude Code 的核心概念：它是什么，以及如何运作。
---
### "从聊天机器人到上下文系统"——四层模型
Claude Code 不是聊天机器人——它是一个上下文系统，在调用 API 之前将你的消息转换成一个丰富的多层提示。这张图展示了每次请求背后无形中发生的四层增强。

```mermaid
flowchart TD
    A([User Message]) --> B[[Layer 1: System Prompt]]
    B --> C[[Layer 2: Context Injection]]
    C --> D[[Layer 3: Tool Definitions]]
    D --> E[[Layer 4: Conversation History]]
    E --> F{{Claude API}}
    F --> G([Claude Response])

    B1[CLAUDE.md files<br/>global + project + subdir] --> B
    C1[Working directory<br/>Git status<br/>Project files] --> C
    D1[Glob, Grep, Read,<br/>Bash, Task, MCP tools] --> D
    E1[Previous messages<br/>+ tool results] --> E

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#6DB3F2,color:#fff
    style E fill:#6DB3F2,color:#fff
    style F fill:#E87E2F,color:#fff
    style G fill:#7BC47F,color:#333
    style B1 fill:#B8B8B8,color:#333
    style C1 fill:#B8B8B8,color:#333
    style D1 fill:#B8B8B8,color:#333
    style E1 fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "First Workflow"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Layer 1: System Prompt"
    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Memory Files (CLAUDE.md)"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Layer 2: Context Injection"
    click C1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Context Management"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Layer 3: Tool Definitions"
    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Tool Arsenal"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Layer 4: Conversation History"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Context Management"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Claude API — Master Loop"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Claude Response"
```

<details>
<summary>ASCII version</summary>

```
User Message
     │
     ▼
┌─────────────────────────────────┐
│ Layer 1: System Prompt          │ ← CLAUDE.md files
│ Layer 2: Context Injection      │ ← Working dir, git status
│ Layer 3: Tool Definitions       │ ← All available tools
│ Layer 4: Conversation History   │ ← Previous messages
└─────────────────┬───────────────┘
                  │
                  ▼
           Claude API Call
                  │
                  ▼
           Claude Response
```

</details>

> **Source**: [How Claude Code Works](../ultimate-guide.md#how-claude-code-works) — Line ~2360

---

### 九步工作流管道

每次向 Claude Code 发出的请求都会经过这条管道——从解析你的意图到显示最终响应。理解这个循环可以帮助你写出更好的指令并更快地排查问题。

```mermaid
flowchart LR
    A([User Message]) --> B(Parse Intent)
    B --> C(Load Context)
    C --> D(Plan Actions)
    D --> E(Execute Tools)
    E --> F{More tools<br/>needed?}
    F -->|Yes| G(Collect Results)
    G --> E
    F -->|No| H(Update Context)
    H --> I(Generate Response)
    I --> J([Display to User])

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#E87E2F,color:#fff
    style E fill:#E87E2F,color:#fff
    style F fill:#E87E2F,color:#fff
    style G fill:#B8B8B8,color:#333
    style H fill:#B8B8B8,color:#333
    style I fill:#6DB3F2,color:#fff
    style J fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "First Workflow"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Parse Intent — Master Loop"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Load Context"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#23-plan-mode" "Plan Actions — Plan Mode"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Execute Tools"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "More Tools? — Master Loop"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Collect Results"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#22-context-management" "Update Context"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#1-the-master-loop" "Generate Response"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Display to User"
```

<details>
<summary>ASCII version</summary>

```
User Message → Parse Intent → Load Context → Plan Actions
                                                   │
                          ┌────────────────────────┘
                          ▼
                    Execute Tools ◄─────────────────┐
                          │                          │
                    More tools?  ──── Yes ─── Collect Results
                          │ No
                          ▼
                   Update Context → Generate Response → Display
```

</details>

> **Source**: [Getting Started](../ultimate-guide.md#getting-started) — Line ~277

---

### 快速决策树——"我该用 Claude Code 吗？"

并非所有任务都需要 Claude Code。这个决策树帮你把合适的任务分配给合适的工具——Claude Code CLI、Claude.ai，还是基于剪贴板的方式。

```mermaid
flowchart TD
    A([Start: I have a task]) --> B{Involves<br/>codebase?}
    B -->|No| C{Pure writing<br/>or analysis?}
    B -->|Yes| D{Repetitive or<br/>>30 min manual?}

    C -->|Yes| E([Use Claude.ai<br/>or API])
    C -->|No| F([Clipboard +<br/>Claude.ai])

    D -->|No| G{Single file,<br/>simple change?}
    D -->|Yes| H([Claude Code<br/>✓ Best choice])

    G -->|Yes| I{Need file<br/>access?}
    G -->|No| H

    I -->|No| F
    I -->|Yes| H

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style G fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style E fill:#6DB3F2,color:#fff
    style F fill:#6DB3F2,color:#fff
    style H fill:#7BC47F,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "When to Use Claude Code"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Involves codebase?"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Pure writing or analysis?"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Repetitive or long manual task?"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Use Claude.ai"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Clipboard + Claude.ai"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Single file, simple change?"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#11-installation" "Claude Code — Best choice"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#12-first-workflow" "Need file access?"
```

<details>
<summary>ASCII version</summary>

```
Task involves codebase?
├── No → Pure writing/analysis? → Yes → Claude.ai
│                              → No  → Clipboard + Claude.ai
└── Yes → Repetitive or >30min?
          ├── Yes → ✓ Claude Code
          └── No  → Single file, simple?
                    ├── Yes → Need file access? → No → Clipboard
                    │                            → Yes → Claude Code
                    └── No  → ✓ Claude Code
```

</details>

> **Source**: [Quick Start Decision](../ultimate-guide.md#quick-start) — See also `machine-readable/reference.yaml` (decide section)

---

### 权限模式对比

Claude Code 有五种权限模式，控制它可以自动做什么以及什么需要你的批准。选错模式是排名第一的安全错误。

```mermaid
flowchart TD
    subgraph DEFAULT["🔒 Default Mode (Recommended)"]
        D1(File reads) --> D2([Auto-approved])
        D3(File writes) --> D4([Prompt required])
        D5(Shell commands) --> D6([Prompt required])
        D7(Risky ops) --> D8([Prompt required])
    end

    subgraph ACCEPT["✏️ acceptEdits Mode"]
        A1(File reads) --> A2([Auto-approved])
        A3(File writes) --> A4([Auto-approved])
        A5(Shell commands) --> A6([Prompt required])
        A7(Risky ops) --> A8([Prompt required])
    end

    subgraph BYPASS["⚠️ bypassPermissions Mode"]
        B1(ALL operations) --> B2([Auto-approved])
        B3["Use only in:<br/>CI/CD, sandboxed<br/>environments"] --> B2
    end

    subgraph PLAN["🔍 Plan Mode (Read-Only)"]
        PL1(File reads) --> PL2([Auto-approved])
        PL3(File writes) --> PL4([Blocked])
        PL5(Shell commands) --> PL6([Blocked])
        PL7["Exit with /execute<br/>or Shift+Tab"] --> PL2
    end

    subgraph DONTASK["🚫 dontAsk Mode"]
        DA1(ALL operations) --> DA2([Auto-denied])
        DA3["Unless pre-approved<br/>via /permissions add"] --> DA2
    end

    style D2 fill:#7BC47F,color:#333
    style D4 fill:#E87E2F,color:#fff
    style D6 fill:#E87E2F,color:#fff
    style D8 fill:#E87E2F,color:#fff
    style A2 fill:#7BC47F,color:#333
    style A4 fill:#7BC47F,color:#333
    style A6 fill:#E87E2F,color:#fff
    style A8 fill:#E87E2F,color:#fff
    style B2 fill:#E85D5D,color:#fff
    style B3 fill:#F5E6D3,color:#333
    style PL2 fill:#7BC47F,color:#333
    style PL4 fill:#E85D5D,color:#fff
    style PL6 fill:#E85D5D,color:#fff
    style DA2 fill:#E85D5D,color:#fff
    style DA3 fill:#F5E6D3,color:#333

    click D1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Default Mode — Permission Modes"
    click D2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click D3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "File writes"
    click D4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click D5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Shell commands"
    click D6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click D7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Risky ops"
    click D8 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click A1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "acceptEdits Mode"
    click A2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click A3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "File writes — auto"
    click A4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click A5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Shell commands"
    click A6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click A7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Risky ops"
    click A8 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Prompt required"
    click B1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "bypassPermissions Mode"
    click B2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved (all)"
    click B3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "CI/CD, sandboxed only"
    click PL1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Plan Mode — File reads"
    click PL2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-approved"
    click PL3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Plan Mode — File writes blocked"
    click PL4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Blocked"
    click PL5 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Plan Mode — Shell commands blocked"
    click PL6 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Blocked"
    click PL7 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Exit Plan Mode"
    click DA1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "dontAsk Mode — All operations"
    click DA2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Auto-denied"
    click DA3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#14-permission-modes" "Pre-approve via /permissions add"
```

<details>
<summary>ASCII version</summary>

```
DEFAULT (Recommended)        acceptEdits               bypassPermissions
─────────────────────        ───────────               ─────────────────
File reads    → AUTO ✓       File reads    → AUTO ✓    ALL ops → AUTO ⚠️
File writes   → PROMPT       File writes   → AUTO ✓
Shell cmds    → PROMPT       Shell cmds    → PROMPT    Use: CI/CD only,
Risky ops     → PROMPT       Risky ops     → PROMPT    sandboxed env

Plan Mode (Read-Only)        dontAsk Mode
─────────────────────        ────────────
File reads    → AUTO ✓       ALL ops → AUTO DENIED ✗
File writes   → BLOCKED ✗    Unless pre-approved via
Shell cmds    → BLOCKED ✗    /permissions add
Exit: /execute or Shift+Tab
```

</details>

> **Source**: [Permission System](../ultimate-guide.md#permission-system) — Line ~760
