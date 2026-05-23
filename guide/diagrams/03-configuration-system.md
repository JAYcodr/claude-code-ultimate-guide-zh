---
title: "Claude Code — 配置系统图解"
description: "配置优先级、技能与命令与代理、代理生命周期、钩子管道"
tags: [configuration, hooks, agents, skills, commands]
---

# 配置系统

Claude Code 如何加载设置、解决冲突以及编排可扩展性。

---

### 配置优先级（5 个层级）

Claude Code 通过严格的优先级层次结构解析设置。较高层级会覆盖较低层级。了解这一点可以防止"为什么我的配置不生效？"这类错误。

```mermaid
flowchart TD
    A["1️⃣ CLI Flags<br/>--model, --dangerously-skip-permissions<br/>--max-turns, --system-prompt"] --> B["2️⃣ Environment Variables<br/>ANTHROPIC_API_KEY<br/>CLAUDE_MODEL, CLAUDE_CONFIG"]
    B --> C["3️⃣ Project Config<br/>.claude/settings.json<br/>.claude/settings.local.json"]
    C --> D["4️⃣ Global Config<br/>~/.claude/settings.json<br/>~/.claude/CLAUDE.md"]
    D --> E["5️⃣ Built-in Defaults<br/>Hardcoded in Claude Code binary"]

    A1["Highest priority<br/>Overrides everything<br/>Use: automation, CI/CD"] --> A
    E1["Lowest priority<br/>Fallback values<br/>Use: baseline behavior"] --> E

    style A fill:#E87E2F,color:#fff
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#F5E6D3,color:#333
    style E fill:#B8B8B8,color:#333
    style A1 fill:#B8B8B8,color:#333
    style E1 fill:#B8B8B8,color:#333

    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "CLI Flags — highest priority"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#33-settings--permissions" "Environment Variables"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#33-settings--permissions" "Project Config"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Global Config"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Built-in Defaults"
    click A1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Highest priority"
    click E1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Lowest priority"
```

<details>
<summary>ASCII version</summary>

```
PRIORITY (highest to lowest)
═══════════════════════════
1. CLI Flags            ← --model, --system-prompt
2. Environment Vars     ← ANTHROPIC_API_KEY
3. Project .claude/     ← settings.json, settings.local.json
4. Global ~/.claude/    ← settings.json, CLAUDE.md
5. Built-in defaults    ← hardcoded fallbacks
```

</details>

> **Source**: [Configuration System](../ultimate-guide.md#configuration) — Line ~3760

---

### 技能 vs 命令 vs 代理 — 何时使用

三种可扩展性机制各有不同的目的和权衡。选择错误的抽象会导致过度工程化或自动化能力不足。

```mermaid
flowchart LR
    subgraph SKILLS["📦 Skills (.claude/skills/)"]
        S1[Bundled capability<br/>with resources]
        S2[Invoked via /skillname]
        S3[Portable across projects]
        S4["Use for: reusable<br/>cross-project capabilities"]
    end

    subgraph COMMANDS["⚡ Commands (.claude/commands/)"]
        C1[Simple template<br/>or script]
        C2[Project slash command]
        C3[Project-specific only]
        C4["Use for: project<br/>automation, shortcuts"]
    end

    subgraph AGENTS["🤖 Agents (.claude/agents/)"]
        A1[Full autonomous agent]
        A2[Own tool set & CLAUDE.md]
        A3[Spawned via Task tool]
        A4["Use for: complex<br/>delegated tasks"]
    end

    Q{What are<br/>you building?} --> |Reusable feature| SKILLS
    Q --> |Project shortcut| COMMANDS
    Q --> |Complex sub-task| AGENTS

    style S1 fill:#6DB3F2,color:#fff
    style S4 fill:#7BC47F,color:#333
    style C1 fill:#F5E6D3,color:#333
    style C4 fill:#7BC47F,color:#333
    style A1 fill:#E87E2F,color:#fff
    style A4 fill:#7BC47F,color:#333
    style Q fill:#E87E2F,color:#fff

    click S1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Bundled capability"
    click S2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Invoked via /skillname"
    click S3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Portable across projects"
    click S4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Reusable capabilities"
    click C1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Simple template"
    click C2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Project slash command"
    click C3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Project-specific"
    click C4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Project automation"
    click A1 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Full autonomous"
    click A2 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Own tool set"
    click A3 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Spawned via Task tool"
    click A4 href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Complex delegated tasks"
    click Q href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#41-what-are-agents" "What are you building?"
```

<details>
<summary>ASCII version</summary>

```
                    Skills              Commands           Agents
Location:      .claude/skills/     .claude/commands/  .claude/agents/
Trigger:       /skillname          /commandname       Task tool
Scope:         Cross-project       This project       Any context
Complexity:    Medium (bundled)    Low (template)     High (autonomous)
Use when:      Reusable caps       Quick shortcuts    Complex tasks
```

</details>

> **Source**: [Extensibility System](../ultimate-guide.md#extensibility) — Line ~4495, ~5025, ~3900

---

### 代理生命周期与作用域隔离

子代理与父代理完全隔离运行。它们会收到上下文副本，但不共享任何状态。理解这一点可以避免"为什么我的子代理看不到 X？"的困惑。

```mermaid
sequenceDiagram
    participant P as Parent Claude
    participant T as Task Tool
    participant S as Sub-Agent
    participant FS as File System

    P->>T: Task(prompt, tools_allowed)
    T->>S: Spawn new Claude instance
    Note over S: Gets: prompt + tool grants<br/>Does NOT get: parent conversation

    S->>FS: Read files (if granted)
    S->>FS: Edit files (if granted)
    S->>S: Independent reasoning

    Note over S,FS: Fully isolated execution
    Note over S: No access to parent state

    S->>T: Return: text result only
    T->>P: Result string
    P->>P: Continues with result

    Note over P,T: Parent sees only final text<br/>No side-effects leaked back
```

<details>
<summary>ASCII version</summary>

```
Parent ──Task(prompt, tools)──► Sub-Agent
                                    │
                               [isolated exec]
                               - read files
                               - edit files
                               - bash (if allowed)
                                    │
Parent ◄───── text result ──────────┘
(no state sharing, no side effects back)
```

</details>

> **Source**: [Sub-Agents](../ultimate-guide.md#sub-agents) — Line ~3900

---

### 钩子事件管道

钩子让你在 Claude Code 生命周期的关键点运行自定义代码——用于安全扫描、日志记录、执行策略或通知。执行顺序很重要。

```mermaid
flowchart TD
    INIT([Session starts]) -.->|v2.1.69+| INST{InstructionsLoaded Hook}
    INST -.-> A

    A([User sends message]) --> UPS{UserPromptSubmit Hook}
    UPS -->|Exit 0: proceed| B{PreToolUse Hook}
    UPS -->|Exit 2: feedback| A
    B -->|Exit 0: allow| C[Tool executes]
    B -->|Exit 1: block| D([Tool blocked<br/>Claude stops])
    C --> E{PostToolUse Hook}
    E --> F[Next tool or response]
    F --> G{More tool calls?}
    G -->|Yes| B
    G -->|No| H([Session ends])
    H --> I{Stop / SessionEnd Hook}
    I --> J([Complete])

    K{PreCompact Hook} -.->|Before /compact| L[/compact runs]
    L --> M{PostCompact Hook}

    NOTE["Hook types:<br/>bash (exit 0/1/2)<br/>http (POST JSON → URL, v2.1.63+)"] -.-> B

    style INST fill:#6DB3F2,color:#fff
    style UPS fill:#6DB3F2,color:#fff
    style B fill:#E87E2F,color:#fff
    style D fill:#E85D5D,color:#fff
    style E fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style K fill:#6DB3F2,color:#fff
    style M fill:#6DB3F2,color:#fff
    style C fill:#7BC47F,color:#333
    style J fill:#7BC47F,color:#333
    style NOTE fill:#F5E6D3,color:#333

    click INIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "Session starts"
    click INST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "InstructionsLoaded Hook — v2.1.69+"
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "User sends message"
    click UPS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "UserPromptSubmit Hook"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "PreToolUse Hook"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Tool executes"
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "Tool blocked"
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "PostToolUse Hook"
    click F href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "Next tool or response"
    click G href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "More tool calls?"
    click H href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "Session ends"
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "Stop / SessionEnd Hook"
    click J href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#72-creating-hooks" "Complete"
    click K href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "PreCompact Hook"
    click L href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "/compact runs"
    click M href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "PostCompact Hook"
```

<details>
<summary>ASCII version</summary>

```
Session starts
     │ (InstructionsLoaded Hook — v2.1.69+)
User message
     │
 UserPromptSubmit ──exit 2──► feedback to Claude (loop)
     │ exit 0
 PreToolUse ──exit 1──► BLOCKED
     │ exit 0
     ▼
Tool executes
     │
PostToolUse
     │
More tools? ──yes──► PreToolUse (loop)
     │ no
Session ends
     │
  Stop / SessionEnd Hook
     │
 Complete

Separately: PreCompact ──► /compact ──► PostCompact

Hook types: bash (exit 0/1/2) | http POST JSON (v2.1.63+)
```

</details>

> **Source**: [Hooks System](../ultimate-guide.md#hooks) — Line ~5350 | UserPromptSubmit + HTTP hooks: v2.1.63+ | InstructionsLoaded: v2.1.69+
