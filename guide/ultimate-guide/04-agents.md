<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
# 4. Agents

_Quick jump:_ [What Are Agents](#41-what-are-agents) · [Creating Custom Agents](#42-creating-custom-agents) · [Agent Template](#43-agent-template) · [Best Practices](#44-best-practices) · [Agent Examples](#45-agent-examples)

---

## 📌 Section 4 TL;DR (60 seconds)

**What are Agents**: Specialized AI personas for specific tasks (think "expert consultants")

**When to create one**:
- ✅ Task repeats often (security reviews, API design)
- ✅ Requires specialized knowledge domain
- ✅ Needs consistent behavior/tone
- ❌ One-off tasks (just ask Claude directly)

**Quick Start**:
1. Create `.claude/agents/my-agent.md`
2. Add YAML frontmatter (name, description, tools, model)
3. Write instructions
4. Use: `@my-agent "task description"`

**Popular agent types**: Security auditor, Test generator, Code reviewer, API designer

**Read this section if**: You have repeating tasks or need domain expertise
**Skip if**: All your tasks are one-off exploratory work

---

**Reading time**: 20 minutes
**Skill level**: Week 1-2
**Goal**: Create specialized AI assistants

## 4.1 What Are Agents

Agents are specialized sub-processes that Claude can delegate tasks to.

### Why Use Agents?

| Without Agents | With Agents |
|----------------|-------------|
| One Claude doing everything | Specialized experts for each domain |
| Context gets cluttered | Each agent has focused context |
| Generic responses | Domain-specific expertise |
| Manual tool selection | Pre-configured tool access |

### Agent vs Direct Prompt

```
Direct Prompt:
You: Review this code for security issues, focusing on OWASP Top 10,
     checking for SQL injection, XSS, CSRF, and authentication vulnerabilities...

With Agent:
You: Use the security-reviewer agent to audit this code
```

The agent encapsulates all that expertise.

### Built-in vs Custom Agents

| Type | Source | Example |
|------|--------|---------|
| Built-in | Claude Code default | Explore, Plan |
| Custom | Your `.claude/agents/` | Backend architect, Code reviewer |

## 4.2 Creating Custom Agents

Agents are markdown files in `.claude/agents/` with YAML frontmatter.

### Agent File Structure

```markdown
---
name: agent-name
description: Clear activation trigger (50-100 chars)
model: sonnet
tools: Read, Write, Edit, Bash, Grep, Glob
---

[Markdown instructions for the agent]
```

### Frontmatter Fields

All official fields supported by Claude Code ([source](https://code.claude.com/docs/en/sub-agents)):

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Kebab-case identifier |
| `description` | ✅ | When to activate this agent (use "PROACTIVELY" for auto-invocation) |
| `model` | ❌ | `sonnet` (default), `opus`, `haiku`, or `inherit` |
| `tools` | ❌ | Allowed tools (comma-separated). Supports `Task(agent_type)` syntax to restrict spawnable subagents |
| `disallowedTools` | ❌ | Tools to deny, removed from inherited or specified list |
| `permissionMode` | ❌ | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan` |
| `maxTurns` | ❌ | Maximum agentic turns before the subagent stops |
| `skills` | ❌ | Skills to preload into agent context at startup (full content injected, not just available) |
| `mcpServers` | ❌ | MCP servers for this subagent — server name strings or inline configs |
| `hooks` | ❌ | Lifecycle hooks scoped to this subagent (`PreToolUse`, `PostToolUse`, `Stop`) |
| `memory` | ❌ | Persistent memory scope: `user`, `project`, or `local` |
| `background` | ❌ | `true` to always run as a background task (default: `false`) |
| `isolation` | ❌ | `worktree` to run in a temporary git worktree (auto-cleaned if no changes) |
| `color` | ❌ | CLI output color for visual distinction (e.g., `green`, `magenta`) |

**Memory scopes** — choose based on how broadly the knowledge should apply:

| Scope | Storage | Use when |
|-------|---------|----------|
| `user` | `~/.claude/agent-memory/<name>/` | Cross-project learning |
| `project` | `.claude/agent-memory/<name>/` | Project-specific, shareable via git |
| `local` | `.claude/agent-memory-local/<name>/` | Project-specific, not committed |

> Full coverage of agent memory — 200-line injection limit, MEMORY.md structure, scope selection guide — in [§4.5 Agent Memory](#45-agent-memory).

### Model Selection

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `haiku` | Quick tasks, simple changes | Fast | Low |
| `sonnet` | Most tasks (default) | Balanced | Medium |
| `opus` | Complex reasoning, architecture | Slow | High |

## 4.3 Agent Template

Copy this template to create your own agent:

```markdown
---
name: your-agent-name
description: Use this agent when [specific trigger description]
model: sonnet
tools: Read, Write, Edit, Bash, Grep, Glob
skills: []
---

# Your Agent Name

## Role Definition

You are an expert in [domain]. Your responsibilities include:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

## Activation Triggers

Use this agent when:
- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

## Methodology

When given a task, you should:
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]

## Output Format

Your deliverables should include:
- [Output 1]
- [Output 2]

## Constraints

- [Constraint 1]
- [Constraint 2]

## Examples

### Example 1: [Scenario Name]

**User**: [Example prompt]

**Your approach**:
1. [What you do first]
2. [What you do next]
3. [Final output]
```

## 4.4 Best Practices

### Do's and Don'ts

| ✅ Do | ❌ Don't |
|-------|----------|
| Make agents specialists | Create generalist agents |
| Define clear triggers | Use vague descriptions |
| Include concrete examples | Leave activation ambiguous |
| Limit tool access | Give all tools to all agents |
| Compose via skills | Duplicate expertise |

### Specialization Over Generalization

**Good**: An agent for each concern
```
backend-architect    → API design, database, performance
security-reviewer    → OWASP, auth, encryption
test-engineer        → Test strategy, coverage, TDD
```

**Bad**: One agent for everything
```
full-stack-expert    → Does everything (poorly)
```

### Explicit Activation Triggers

**Good description**:
```yaml
description: Use when designing APIs, reviewing database schemas, or optimizing backend performance
```

**Bad description**:
```yaml
description: Backend stuff
```

### Skill Composition

Instead of duplicating knowledge:

```yaml
# security-reviewer.md
skills:
  - security-guardian  # Inherits OWASP knowledge
```

### Agent Validation Checklist

Before deploying a custom agent, validate against these criteria:

**Efficacy** (Does it work?)
- [ ] Tested on 3+ real use cases from your project
- [ ] Output matches expected format consistently
- [ ] Handles edge cases gracefully (empty input, errors, timeouts)
- [ ] Integrates correctly with existing workflows

**Efficiency** (Is it cost-effective?)
- [ ] <5000 tokens per typical execution
- [ ] <30 seconds for standard tasks
- [ ] Doesn't duplicate work done by other agents/skills
- [ ] Justifies its existence vs. native Claude capabilities

**Security** (Is it safe?)
- [ ] Tools restricted to minimum necessary
- [ ] No Bash access unless absolutely required
- [ ] File access limited to relevant directories
- [ ] No credentials or secrets in agent definition

**Maintainability** (Will it last?)
- [ ] Clear, descriptive name and description
- [ ] Explicit activation triggers documented
- [ ] Examples show common usage patterns
- [ ] Version compatibility noted if framework-dependent

> 💡 **Rule of Three**: If an agent doesn't save significant time on at least 3 recurring tasks, it's probably over-engineering. Start with skills, graduate to agents only when complexity demands it.

> **Automated audit**: Run `/audit-agents-skills` for a comprehensive quality audit across all agents, skills, and commands. Scores each file on 16 criteria with weighted grading (32 points for agents/skills, 20 for commands). See `examples/skills/audit-agents-skills/` for the full scoring methodology.

### Background Subagents

Subagents can run in the background without blocking the main session. This is useful for fire-and-forget tasks like running tests, linting, or notifications.

| Mode | Behavior | Use when |
|------|----------|----------|
| Default | Parent waits for agent output | Need result before continuing |
| Background | Agent runs in parallel, parent continues | Fire-and-forget (tests, linting, notifications) |

**Managing background agents:**

```bash
# List running agents + kill overlay
ctrl+f    # Opens agent manager overlay

# Cancel main thread only (background agents keep running)
ESC
ctrl+c
```


## 4.5 Agent Memory

Introduced in **Claude Code v2.1.33** (February 2026), the `memory` frontmatter field gives subagents persistent, markdown-based knowledge that survives across sessions. Before this, every agent invocation started with a blank slate regardless of previous runs.

### Why Agent Memory Matters

Without memory, a code-reviewer agent that discovers your team prefers early-return patterns over nested `if` blocks has no way to carry that observation forward. The next invocation starts cold. Agent memory fixes this: the agent writes its findings to a structured file, and future invocations pick up where the last one left off.

This is distinct from the other memory systems in Claude Code. Each serves a different purpose:

| System | Written by | Read by | Scope | Persists |
|--------|------------|---------|-------|----------|
| **CLAUDE.md** | You (manually) | Main Claude + all agents | Project or global | Git-tracked |
| **Auto-memory** | Main Claude (automatic) | Main Claude only | Per-project per-user | Gitignored |
| **Agent memory** | The agent itself | That specific agent only | Configurable | Depends on scope |

An agent reads both `CLAUDE.md` (shared project context) and its own memory (agent-specific accumulated knowledge). The two layers are complementary.

### Memory Scopes

Choose a scope based on where the knowledge is useful:

| Scope | Storage location | Version controlled | Best for |
|-------|-----------------|-------------------|----------|
| `user` | `~/.claude/agent-memory/<agent-name>/` | No | Cross-project learning — a code reviewer that builds up pattern knowledge across every repo |
| `project` | `.claude/agent-memory/<agent-name>/` | Yes (committed) | Project-specific knowledge the whole team should share — e.g., API conventions discovered by a scaffolding agent |
| `local` | `.claude/agent-memory-local/<agent-name>/` | No (gitignored) | Project-specific knowledge that is personal and should not be committed |

These scopes mirror the settings hierarchy (`~/.claude/settings.json` → `.claude/settings.json` → `.claude/settings.local.json`), making the mental model consistent across the whole system.

Activate memory by adding one line to the agent frontmatter:

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and consistency
tools: Read, Grep, Glob
memory: user
---
```

### How the 200-Line Injection Works

When an agent starts, Claude Code reads the first 200 lines of `MEMORY.md` in the agent's memory directory and injects them directly into the agent's system prompt. This is automatic — no explicit tool call needed.

```
~/.claude/agent-memory/code-reviewer/
├── MEMORY.md                   ← First 200 lines injected at startup
├── react-patterns.md           ← Topic-specific file, loaded on demand
└── security-checklist.md       ← Topic-specific file, loaded on demand
```

Once `MEMORY.md` exceeds 200 lines the agent should move detailed content into topic-specific files and keep `MEMORY.md` as a concise index with references. The agent manages this itself — `Read`, `Write`, and `Edit` are automatically available to any agent with `memory` set.

**Practical implication**: structure `MEMORY.md` like a smart summary, not an append-only log. High-signal entries at the top, topic files for depth.

### MEMORY.md Structure

A well-structured agent memory file makes the injected content immediately useful:

```markdown
# code-reviewer memory
Last updated: 2026-03-10

## Project conventions (confirmed)
- Early return over nested conditionals (consistent across 12 reviews)
- `zod` for all API boundary validation — never `joi` or raw type checks
- Auth middleware must be applied before any controller logic

## Recurring issues
- Missing `await` on async DB calls in `/src/services/` (seen 4× this month)
- `any` casts in migration scripts accepted as a known exception

## Patterns to watch
- New contributors tend to skip error boundary wrapping in React trees

## Topic files
- [react-patterns.md](react-patterns.md) — component structure, hook usage, memoization rules
- [security-checklist.md](security-checklist.md) — OWASP Top 10 per-category notes
```

### Prompting Agents to Use Their Memory

Memory is only useful if the agent reads and writes it consistently. Explicit prompting in the agent body makes a large difference:

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
tools: Read, Write, Edit, Bash
memory: project
---

Before starting any task, review your memory for relevant conventions and
past decisions. After completing a task, update your memory with new patterns,
architectural decisions, or recurring issues you observed. Keep MEMORY.md
under 200 lines — move detailed notes to topic-specific files.
```

This pattern — skills for static startup knowledge, memory for dynamic accumulated knowledge — gives agents the best of both worlds. Skills inject curated reference material at first run; memory carries forward what the agent discovers on its own.

### Choosing the Right Scope

| Situation | Recommended scope |
|-----------|------------------|
| Generic code reviewer used across multiple projects | `user` — knowledge accumulates globally |
| API scaffolding agent that learns your team's endpoint conventions | `project` — commit the memory so teammates benefit |
| Personal refactoring agent with your preferred style preferences | `local` — stays on your machine only |
| Agent for a client project you do not want to mix with personal knowledge | `local` — isolated, not committed |

> **Sources**: [Create custom subagents](https://code.claude.com/docs/en/sub-agents) · [Manage Claude's memory](https://code.claude.com/docs/en/memory) · Claude Code v2.1.33 release notes

---

## 4.6 Agent Examples

### Example 1: Code Reviewer Agent

```markdown
---
name: code-reviewer
description: Use for code quality reviews, security audits, and performance analysis
model: sonnet
tools: Read, Grep, Glob
skills:
  - security-guardian
---

# Code Reviewer

## Scope Definition

Perform comprehensive code reviews with isolated context, focusing on:
- Code quality and maintainability
- Security best practices (OWASP Top 10)
- Performance optimization
- Test coverage analysis

Scope: Code review analysis only. Provide findings without implementing fixes.

## Activation Triggers

Use this agent when:
- Completing a feature before PR (need fresh eyes on code)
- Reviewing someone else's code (isolated review context)
- Auditing security-sensitive code (security-focused scope)
- Analyzing performance bottlenecks (performance-focused scope)

## Methodology

1. **Understand Context**: Read the code and understand its purpose
2. **Check Quality**: Evaluate readability, maintainability, DRY principles
3. **Security Scan**: Look for OWASP Top 10 vulnerabilities
4. **Performance Review**: Identify potential bottlenecks
5. **Provide Feedback**: Structured report with severity levels

## Output Format

### Code Review Report

**Summary**: [1-2 sentence overview]

**Critical Issues** (Must Fix):
- [Issue with file:line reference]

**Warnings** (Should Fix):
- [Issue with file:line reference]

**Suggestions** (Nice to Have):
- [Improvement opportunity]

**Positive Notes**:
- [What was done well]
```

### Example 2: Debugger Agent

```markdown
---
name: debugger
description: Use when encountering errors, test failures, or unexpected behavior
model: sonnet
tools: Read, Bash, Grep, Glob
---

# Debugger

## Scope Definition

Perform systematic debugging with isolated context:
- Investigate root causes, not symptoms
- Use evidence-based debugging approach
- Verify rather than assume (always review output—LLMs can make mistakes)

Scope: Debugging analysis only. Focus on root cause identification without context pollution from previous debugging attempts.

## Methodology

1. **Reproduce**: Confirm the issue exists
2. **Isolate**: Narrow down to smallest reproducible case
3. **Analyze**: Read code, check logs, trace execution
4. **Hypothesize**: Form theories about the cause
5. **Test**: Verify hypothesis with minimal changes
6. **Fix**: Implement the solution
7. **Verify**: Confirm fix works and doesn't break other things

## Output Format

### Debug Report

**Issue**: [Description]
**Root Cause**: [What's actually wrong]
**Evidence**: [How you know]
**Fix**: [What to change]
**Verification**: [How to confirm it works]
```

### Example 3: Backend Architect Agent

```markdown
---
name: backend-architect
description: Use for API design, database optimization, and system architecture decisions
model: opus
tools: Read, Write, Edit, Bash, Grep
skills:
  - backend-patterns
---

# Backend Architect

## Scope Definition

Analyze backend architecture with isolated context, focusing on:
- API design (REST, GraphQL, tRPC)
- Database modeling and optimization
- System scalability
- Clean architecture patterns

Scope: Backend architecture analysis only. Focus on design decisions without frontend or DevOps considerations.

## Activation Triggers

Use this agent when:
- Designing new API endpoints (need architecture-focused analysis)
- Optimizing database queries (database scope isolation)
- Planning system architecture (system design scope)
- Refactoring backend code (backend-only scope)

## Methodology

1. **Requirements Analysis**: Understand the business need
2. **Architecture Review**: Check current system state
3. **Design Options**: Propose 2-3 approaches with trade-offs
4. **Recommendation**: Suggest best approach with rationale
5. **Implementation Plan**: Break down into actionable steps

## Constraints

- Follow existing project patterns
- Prioritize backward compatibility
- Consider performance implications
- Document architectural decisions
```

## 4.7 Advanced Agent Patterns

### Tool SEO - Optimizing Agent Descriptions

The `description` field determines when Claude auto-activates your agent. Optimize it like SEO:

```yaml
# ❌ Bad description
description: Reviews code

# ✅ Good description (Tool SEO)
description: |
  Security code reviewer - use PROACTIVELY when:
  - Reviewing authentication/authorization code
  - Analyzing API endpoints
  - Checking input validation
  - Auditing data handling
  Triggers: security, auth, vulnerability, OWASP, injection
```

**Tool SEO Techniques**:
1. **"use PROACTIVELY"**: Encourages automatic activation
2. **Explicit triggers**: Keywords that trigger the agent
3. **Listed contexts**: When the agent is relevant
4. **Short nicknames**: `sec-1`, `perf-a`, `doc-gen`

### Agent Weight Classification

| Category | Tokens | Init Time | Optimal Use |
|----------|--------|-----------|-------------|
| **Lightweight** | <3K | <1s | Frequent tasks, workers |
| **Medium** | 10-15K | 2-3s | Analysis, reviews |
| **Heavy** | 25K+ | 5-10s | Architecture, full audits |

**Golden Rule**: A lightweight agent used 100x > A heavy agent used 10x

### The 7-Parallel-Task Method

Launch 7 scope-focused sub-agents in parallel for complete features:

```
┌─────────────────────────────────────────────────────────────┐
│   PARALLEL FEATURE IMPLEMENTATION                           │
│                                                             │
│   Task 1: Components     → Create React components          │
│   Task 2: Styles         → Generate Tailwind styles         │
│   Task 3: Tests          → Write unit tests                 │
│   Task 4: Types          → Define TypeScript types          │
│   Task 5: Hooks          → Create custom hooks              │
│   Task 6: Integration    → Connect with API/state           │
│   Task 7: Config         → Update configurations            │
│                                                             │
│   All in parallel → Final consolidation                     │
└─────────────────────────────────────────────────────────────┘
```

**Example Prompt**:
```
Implement the "User Profile" feature using 7 parallel sub-agents:

1. COMPONENTS: Create UserProfile.tsx, UserAvatar.tsx, UserStats.tsx
2. STYLES: Define Tailwind classes in a styles file
3. TESTS: Write tests for each component
4. TYPES: Create types in types/user-profile.ts
5. HOOKS: Create useUserProfile and useUserStats hooks
6. INTEGRATION: Connect with existing tRPC router
7. CONFIG: Update exports and routing

Launch all agents in parallel.
```

### Split Role Sub-Agents

**Concept**: Multi-perspective analysis in parallel.

**Process**:
```
┌─────────────────────────────────────────────────────────────┐
│   SPLIT ROLE ANALYSIS                                       │
│                                                             │
│   Step 1: Setup                                             │
│   └─ Activate Plan Mode (thinking enabled by default)       │
│                                                             │
│   Step 2: Role Suggestion                                   │
│   └─ "What expert roles would analyze this code?"           │
│      Claude suggests: Security, Performance, UX, etc.       │
│                                                             │
│   Step 3: Selection                                         │
│   └─ "Use: Security Expert, Senior Dev, Code Reviewer"      │
│                                                             │
│   Step 4: Parallel Analysis                                 │
│   ├─ Security Agent: [Vulnerability analysis]               │
│   ├─ Senior Agent: [Architecture analysis]                  │
│   └─ Reviewer Agent: [Readability analysis]                 │
│                                                             │
│   Step 5: Consolidation                                     │
│   └─ Synthesize 3 reports into recommendations              │
└─────────────────────────────────────────────────────────────┘
```

**Code Review Prompt** (scope-focused):
```
Analyze this PR with isolated scopes:
1. Architecture Scope: Design patterns, SOLID principles, modularity
2. Security Scope: Vulnerabilities, injection risks, auth/authz flaws
3. Performance Scope: Database queries, algorithmic complexity, caching
4. Maintainability Scope: Code clarity, documentation, naming conventions
5. Testing Scope: Test coverage, edge cases, testability

Context: src/**, tests/**, only files changed in PR
```

**UX Review Prompt** (scope-focused):
```
Evaluate this interface with isolated scopes:
1. Visual Design Scope: Consistency with design system, spacing, typography
2. Usability Scope: Discoverability, user flow, cognitive load
3. Efficiency Scope: Keyboard shortcuts, power user features, quick actions
4. Accessibility Scope: WCAG 2.1 AA compliance, screen reader, keyboard nav
5. Responsive Scope: Mobile breakpoints, touch targets, viewport handling

Context: src/components/**, styles/**, only UI-related files
```

**Production Example: Multi-Agent Code Review** (Pat Cullen, Jan 2026):

Scope-focused agents for comprehensive PR review:

1. **Consistency Scope**: Duplicate logic, pattern violations, DRY compliance (context: full PR diff)
2. **SOLID Scope**: SRP violations, nested conditionals (>3 levels), cyclomatic complexity >10 (context: changed classes/functions)
3. **Defensive Code Scope**: Silent catches, swallowed exceptions, hidden fallbacks (context: error handling code)

**Key patterns** (beyond generic Split Role):

- **Pre-flight check**: `git log --oneline -10 | grep "Co-Authored-By: Claude"` to detect follow-up passes and avoid repeating suggestions
- **Anti-hallucination**: Use `Grep`/`Glob` to verify patterns before recommending them (occurrence rule: >10 = established, <3 = not established)
- **Reconciliation**: Prioritize existing project patterns over ideal patterns, skip suggestions with documented reasoning
- **Severity classification**: 🔴 Must Fix (blockers) / 🟡 Should Fix (improvements) / 🟢 Can Skip (nice-to-haves)
- **Convergence loop**: Review → fix → re-review → repeat (max 3 iterations) until only optional improvements remain

**Production safeguards**:

- Read full file context (not just diff lines)
- Conditional context loading based on diff content (DB queries → check indexes, API routes → check auth middleware)
- Protected files skip list (package.json, migrations, .env)
- Quality gates: `tsc && lint` validation before each iteration

**Source**: [Pat Cullen's Final Review](https://gist.github.com/patyearone/c9a091b97e756f5ed361f7514d88ef0b)
**Implementation**: See `/review-pr` advanced section, `examples/agents/code-reviewer.md`, `guide/workflows/iterative-refinement.md` (Review Auto-Correction Loop)

### Named Perspective Agents

The guide lists "roleplaying expertise personas" as a bad reason to use agents (see §3.x, When NOT to use agents). Named Perspective Agents are a different pattern and should not be confused with it.

**The distinction**:

| Pattern | What it is | Problem |
|---------|-----------|---------|
| Persona roleplay (anti-pattern) | "You are a senior backend developer with 10 years of experience" | Generic role, adds nothing over a good prompt |
| Named Perspective | "Review from DHH's perspective" | Encodes a specific, recognizable set of engineering opinions |

A Named Perspective Agent uses a well-known engineering name as a compressed prompt. Naming an agent "DHH" bundles the following without spelling it out: fat models, thin controllers, REST conventions over configuration, skepticism of premature abstraction, Rails pragmatism. The name is a shortcut to a distinct opinionated style, not a costume.

**When it works**: Only for engineers whose views Claude has been trained on and whose opinions map to a stable, recognizable style. DHH (Rails), Kent Beck (TDD, simplicity), Martin Fowler (refactoring, patterns) are good candidates. Random names are not.

**Example** (from Every.to compound-engineering plugin):

```markdown
---
name: dhh-reviewer
description: Review code from DHH's perspective. Prioritize Rails conventions, fat models, thin controllers, pragmatic REST, and skepticism of unnecessary abstraction.
allowed-tools: Read, Grep
---
```

The agent's value is in surfacing a coherent perspective that might disagree with your default approach, not in simulating a person.

**Caveat**: Named Perspective Agents can drift as Claude's training evolves. Treat the name as a convenient shorthand, not a guarantee that the agent will track a real person's current opinions.

*Source: Every.to compound-engineering plugin (2026)*

### Parallelization Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│   PARALLELIZABLE?                                           │
│                                                             │
│              Non-destructive          Destructive           │
│              (read-only)              (write)               │
│                                                             │
│   Independent   ✅ PARALLEL           ⚠️ SEQUENTIAL        │
│                 Max efficiency         Plan Mode first      │
│                                                             │
│   Dependent     ⚠️ SEQUENTIAL         ❌ CAREFUL            │
│                 Order matters          Risk of conflicts    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**✅ Perfectly parallelizable**:
```
"Search 8 different GitHub repos for best practices on X"
"Analyze these 5 files for vulnerabilities (without modifying)"
"Compare 4 libraries and produce a comparative report"
```

**⚠️ Sequential recommended**:
```
"Refactor these 3 files (they depend on each other)"
"Migrate DB schema then update models then update routers"
```

**❌ Needs extra care**:
```
"Modify these 10 files in parallel"
→ Risk: conflicts if files share imports/exports
→ Solution: Plan Mode → Identify dependencies → Sequence if needed
```

### Multi-Agent Orchestration Pattern

```
┌─────────────────────────────────────────────────────────────┐
│   ORCHESTRATION PATTERN                                     │
│                                                             │
│                    ┌──────────────┐                         │
│                    │  Sonnet 4.5  │                         │
│                    │ Orchestrator │                         │
│                    └──────┬───────┘                         │
│                           │                                 │
│              ┌────────────┼────────────┐                    │
│              │            │            │                    │
│              ▼            ▼            ▼                    │
│        ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│        │ Haiku   │  │ Haiku   │  │ Haiku   │                │
│        │ Worker1 │  │ Worker2 │  │ Worker3 │                │
│        └────┬────┘  └────┬────┘  └────┬────┘                │
│              │            │            │                    │
│              └────────────┼────────────┘                    │
│                           │                                 │
│                           ▼                                 │
│                    ┌──────────────┐                         │
│                    │  Sonnet 4.5  │                         │
│                    │  Validator   │                         │
│                    └──────────────┘                         │
│                                                             │
│   Cost: 2-2.5x cheaper than Opus everywhere                 │
│   Quality: Equivalent for most common tasks                 │
└─────────────────────────────────────────────────────────────┘
```

### Tactical Model Selection Matrix

> See [Section 2.5 Model Selection & Thinking Guide](#25-model-selection--thinking-guide) for the canonical decision table with effort levels and cost estimates.

**Cost Optimization Example**:
```
Scenario: Refactoring 100 files

❌ Naive approach:
- Opus for everything
- Cost: ~$50-100
- Time: 2-3h

✅ Optimized approach:
- Sonnet: Analysis and plan (1x)
- Haiku: Parallel workers (100x)
- Sonnet: Final validation (1x)
- Cost: ~$5-15
- Time: 1h (parallelized)

Estimated savings: significant (varies by project)
```

---

### The Self-Evolving Agent Pattern

An agent that updates its own skills after each execution. Instead of manually maintaining documentation, the agent reads the current state of its domain and rewrites the knowledge injected into itself.

**When to use**: Long-lived agents whose domain evolves — presentation editors, API clients tracking schema changes, agents managing living documents.

**Core mechanism** (in agent system prompt):

```markdown
### Step N: Self-Evolution (after every execution)

After completing your main task, update your preloaded skills to stay in sync:

1. Read the current state of [the domain you modified]
2. Update `.claude/skills/<your-skill>/SKILL.md` to reflect reality
3. Log what changed and why in a "## Learnings" section of this agent file

This prevents knowledge drift between what you know and what is.
```

**Full example** — a presentation curator agent that keeps its own layout/weight knowledge fresh:

```yaml
---
name: presentation-curator
description: PROACTIVELY use when updating slides, structure, or weights
tools: Read, Write, Edit, Grep, Glob
model: sonnet
color: magenta
skills:
  - presentation/slide-structure
  - presentation/styling
---

## Step 5: Self-Evolution (after every execution)

Read presentation/index.html and update your skills:
- slide-structure skill: update section ranges, weight table, slide count
- styling skill: update CSS patterns if new ones were introduced
- Append new findings to the "## Learnings" section below

## Learnings
_Each run appends findings here. Future invocations start informed._
- Slide badges are JS-injected — never hardcode them in HTML.
```

**Why it works**: The `skills:` frontmatter injects skill content at agent startup. By writing back to those files after each run, the agent's next invocation starts with current knowledge. No human maintenance required.

**Key constraints**:
- Scope updates narrowly — only update what actually changed
- Keep a `## Learnings` log so the agent builds cumulative knowledge over sessions
- Pair with `memory: project` for cross-session persistence of broader context

---

