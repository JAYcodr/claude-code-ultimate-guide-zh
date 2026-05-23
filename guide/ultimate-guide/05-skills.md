# 5. Skills

_Quick jump:_ [Two Kinds of Skills](#50-two-kinds-of-skills) · [Understanding Skills](#51-understanding-skills) · [Creating Skills](#52-creating-skills) · [Skill Lifecycle](#5x-skill-lifecycle--retirement) · [Skill Evals](#5y-skill-evals) · [Skill Template](#53-skill-template) · [Skill Examples](#54-skill-examples)

---

> **CC 2.1.3 (January 2026)**: Skills and Commands are now unified. `.claude/commands/` is merged into `.claude/skills/`. Skills have two invocation modes: user-triggered (`/skill-name`, equivalent to old commands) and model-triggered (auto-loaded by description match). To restrict a skill to user-invocation only, add `disable-model-invocation: true` to its frontmatter. Existing files in `.claude/commands/` remain backward-compatible but all new development belongs in `.claude/skills/`.

---

**Reading time**: 20 minutes
**Skill level**: Week 2
**Goal**: Create, test, and manage reusable knowledge modules

## 5.0 Two Kinds of Skills

> **New in March 2026**: Anthropic's Skill Creator update formalizes a taxonomy that changes how you design, test, and eventually retire skills. Sources: ainews.com, mexc.co, claudecode.jp — not yet reflected in the official `llms-full.txt`.

Not all skills age the same way. The type you're building determines how you write it, how you test it, and when to retire it.

| | Capability Uplift | Encoded Preference |
|---|---|---|
| **What it does** | Fills a gap the base model can't handle consistently | Sequences existing capabilities your team's specific way |
| **Examples** | Precise PDF text placement, custom code patterns | NDA review checklist, weekly status update workflow |
| **Durability** | Fades as the model improves | Stays durable as long as the workflow is relevant |
| **Retirement signal** | Model passes the eval without the skill | Workflow changes or becomes irrelevant |
| **Eval approach** | A/B test: with vs. without the skill | Fidelity check: does it follow the sequence correctly? |

**Capability Uplift** teaches Claude something it genuinely can't do well on its own — yet. High value today, but carries a maintenance debt: as Claude improves, these skills may become redundant. Evals tell you when that happens before a user does.

**Encoded Preference** encodes your team's specific way of doing something Claude already knows how to do. An NDA review follows your legal team's criteria, not a generic checklist. These skills don't compete with model improvements — they capture workflow decisions that are yours to make, and stay relevant as long as your process does.

> **Practical implication**: When building a Capability Uplift skill, budget time for evals. When building an Encoded Preference skill, budget time for keeping the workflow description accurate as your process evolves.

## 5.1 Understanding Skills

Skills are knowledge packages that agents can inherit.

### Skills vs Agents vs Commands

| Concept | Purpose | Invocation |
|---------|---------|------------|
| **Agent** | Context isolation tool | Task tool delegation |
| **Skill** | Knowledge module or workflow template | `/skill-name` (user) or auto-loaded (model) |

#### Detailed Comparison

| Aspect | Skills (user-invocable) | Skills (model-invocable) | Agents |
|--------|------------------------|--------------------------|--------|
| **What it is** | Workflow template | Knowledge module | Context isolation tool |
| **Location** | `.claude/skills/` | `.claude/skills/` | `.claude/agents/` |
| **Invocation** | `/skill-name` (user types) | Auto-loaded by model | Task tool delegation |
| **Frontmatter** | `disable-model-invocation: true` | Default (no flag needed) | n/a |
| **Execution** | In main conversation | Loaded into context | Separate subprocess |
| **Context** | Shares main context | Adds to agent context | Isolated context |
| **Best for** | Repeatable manual workflows | Reusable knowledge | Scope-limited analysis |
| **Token cost** | Low (template only) | Medium (knowledge loaded) | High (full agent) |
| **Examples** | `/commit`, `/pr`, `/ship` | TDD, security-guardian | security-audit, perf-audit |

#### Decision Tree: Which to Use?

```
Is this a repeatable workflow with steps?
├─ Yes → Use a SKILL (user-invocable, disable-model-invocation: true)
│        Example: /commit, /release-notes, /ship
│
└─ No → Is this specialized knowledge multiple agents need?
        ├─ Yes → Use a SKILL
        │        Example: TDD methodology, security checklist
        │
        └─ No → Does this need isolated context or parallel work?
                ├─ Yes → Use an AGENT
                │        Example: code-reviewer, performance-auditor
                │
                └─ No → Just write it in CLAUDE.md as instructions
```

> **The 20% rule**: if an instruction applies to more than 20% of your conversations, put it in `CLAUDE.md` (always loaded). If it applies to fewer than 20%, make it a skill (loaded on demand). The difference matters for token efficiency: a skill's system prompt is injected only when Claude invokes it, while CLAUDE.md content counts against every request's context window.

> **See also**: [§2.7 Configuration Decision Guide](#27-configuration-decision-guide) for a broader decision tree covering all seven mechanisms (including Hooks, MCP, and CLAUDE.md vs rules). To automate detection of what belongs in each category, use [`cc-sessions discover`](#session-pattern-discovery) — it applies this 20% threshold to your actual session history.

#### Common Patterns

| Need | Solution | Example |
|------|----------|---------|
| Run tests before commit | Command | `/commit` with test step |
| Security review knowledge | Skill + Agent | security-guardian skill → security-audit agent |
| Parallel code review | Multiple scope-focused agents | Launch 3 review agents with isolated scopes |
| Quick git workflow | Command | `/pr`, `/ship` |
| Architecture knowledge | Skill | architecture-patterns skill |
| Complex debugging | Agent | debugging-specialist agent |

#### Skills and Subagents

Subagents don't inherit skills automatically — this is a common source of confusion.

| Rule | Details |
|------|---------|
| **Built-in agents can't use skills** | Explorer, Plan, and Verify agents have no access to skills |
| **Custom subagents need explicit wiring** | Skills must be listed in the agent's `skills:` frontmatter field |
| **Skills load at agent start** | Not on-demand like in the main conversation — all listed skills are loaded upfront |
| **List only always-relevant skills** | Don't add a skill unless it applies to every single task the subagent performs |

Custom subagent frontmatter with skills (`.claude/agents/my-agent.md`):

```yaml
---
name: frontend-reviewer
description: "Use this agent when reviewing frontend code for accessibility and security"
tools: Bash, Glob, Grep, Read, WebFetch
model: sonnet
skills: accessibility-audit, security-guardian
---
```

The skills listed in `skills:` must exist in `.claude/skills/` (project) or `~/.claude/skills/` (personal). Create agents with skills via `/agents` in Claude Code or add the `skills:` field to an existing agent file.

### Why Skills?

Without skills:
```
Agent A: Has security knowledge (duplicated)
Agent B: Has security knowledge (duplicated)
Agent C: Has security knowledge (duplicated)
```

With skills:
```
security-guardian skill: Single source of security knowledge
Agent A: inherits security-guardian
Agent B: inherits security-guardian
Agent C: inherits security-guardian
```

### What Makes a Good Skill?

| Good Skill | Bad Skill | Expected Lifespan |
|------------|-----------|-------------------|
| Reusable across agents | Single-agent specific | — |
| Domain-focused | Too broad | — |
| Contains reference material | Just instructions | — |
| Includes checklists | Missing verification | — |
| Has evals defined | "Seems to work" validation | Capability Uplift: monitor regularly; Encoded Preference: stable |
| Clear retirement criteria | No lifecycle plan | Capability Uplift: short-medium; Encoded Preference: long |

## 5.2 Creating Skills

Skills live in `.claude/skills/{skill-name}/` directories.

### Skill Folder Structure

```
skill-name/
├── SKILL.md          # Required - Main instructions
├── reference.md      # Optional - Detailed documentation
├── checklists/       # Optional - Verification lists
│   ├── security.md
│   └── performance.md
├── examples/         # Optional - Code patterns
│   ├── good-example.ts
│   └── bad-example.ts
└── scripts/          # Optional - Helper scripts
    └── audit.sh
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: Short description for activation (max 1024 chars)
allowed-tools: Read Grep Bash
---
```

| Field | Spec | Description |
|-------|------|-------------|
| `name` | [agentskills.io](https://agentskills.io) | Lowercase, 1-64 chars, hyphens only, no `--`, must match directory name |
| `description` | [agentskills.io](https://agentskills.io) | What the skill does and when to use it (max 1024 chars) |
| `allowed-tools` | [agentskills.io](https://agentskills.io) | Space-delimited list of pre-approved tools. Supports wildcard scoping: `Bash(npm run *)`, `Bash(agent-browser:*)`, `Edit(/docs/**)` |
| `license` | [agentskills.io](https://agentskills.io) | License name or reference to bundled file |
| `compatibility` | [agentskills.io](https://agentskills.io) | Environment requirements (max 500 chars) |
| `metadata` | [agentskills.io](https://agentskills.io) | Arbitrary key-value pairs (author, version, etc.) |
| `effort` | **CC only** (v2.1.80+) | `low\|medium\|high` — overrides the session effort level when this skill is invoked. Set `low` for mechanical tasks (commit, format, scaffold), `high` for analysis or architectural reasoning. |
| `argument-hint` | **CC only** | Placeholder shown in the slash command menu when the skill accepts `$ARGUMENTS`. Format: `"[--flag] [positional_arg]"`. Example: `"[--verbose] [--max N] <branch>"`. |
| `disable-model-invocation` | **CC only** | `true` to make skill manual-only (workflow with side effects) |

**`effort` per skill** (v2.1.80+) — override the session effort level for a specific skill invocation. Independent of `effortLevel` in settings.json: the skill's value takes precedence only while that skill runs, then reverts.

```yaml
---
name: security-audit
description: Deep security analysis with threat modeling
effort: high      # Always high effort, regardless of session setting
allowed-tools: Read Grep Glob Bash
---
```

```yaml
---
name: commit
description: Stage and commit changes with conventional format
effort: low       # Mechanical — no reasoning budget needed
allowed-tools: Bash
---
```

**Why it matters**: Effort controls thinking depth, tool call verbosity, and analysis depth — not just tokens. A `low` effort skill runs faster and cheaper. A `high` effort skill reasons deeper without the user having to manually adjust the session setting. This enables automatic cognitive budget allocation per task type: pay for reasoning only where it adds value.

**`${CLAUDE_EFFORT}` in skill content** (v2.1.120): Skill body text can reference `${CLAUDE_EFFORT}` as a variable. Claude substitutes it with the current effort level string (`low`, `medium`, `high`, `xhigh`, `max`) before processing the skill. Use this to branch instructions based on effort:

```markdown
---
name: review-code
effort: medium
---

Review the changed files for correctness.

${if CLAUDE_EFFORT == "high" or CLAUDE_EFFORT == "xhigh"}
Also run a full security audit and check all edge cases.
${end}
```

This lets one skill serve both quick-scan (low/medium) and thorough (high/xhigh) use cases without maintaining two separate skills.

**`allowed-tools` wildcard scoping** — limit a skill to specific command namespaces rather than opening full Bash access:

```yaml
# Scope to a specific CLI tool only — no other Bash commands allowed
allowed-tools: Bash(agent-browser:*)

# Scope to npm scripts only
allowed-tools: Bash(npm run *)

# Read-only + scoped writes
allowed-tools: Read Grep Glob Edit(/docs/**)
```

This is more secure than granting broad `Bash` access: the skill can only run commands matching the pattern. Ideal for skills wrapping a specific CLI tool.

> **Open standard**: Agent Skills follow the [agentskills.io specification](https://agentskills.io), created by Anthropic and supported by 35+ platforms (Cursor, VS Code, GitHub Copilot, Codex, Gemini CLI, Goose, Roo Code, OpenHands, Amp, Letta, Junie, etc.). Skills you create for Claude Code are portable. The `disable-model-invocation` field is a Claude Code extension.

### Validating Skills

Use the official [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) CLI to validate your skill before publishing:

```bash
skills-ref validate ./my-skill      # Check frontmatter + naming conventions
skills-ref to-prompt ./my-skill     # Generate <available_skills> XML for agent prompts
```

> **Beyond spec validation**: Three complementary audit tools:
> - `/audit-agents-skills` — broad quality audit across agents, skills, AND commands (16 criteria, 32-pt weighted grading). Use for general production readiness.
> - `/eval-skills` — skills-only audit with effort-level inference engine. Discovers all skills, infers the appropriate `effort` level from content analysis, flags mismatches, and prints copy-paste ready frontmatter patches. Use when adding `effort` fields to an existing library or auditing a new project. See `examples/skills/eval-skills/`.
> - `/eval-rules` — rules-focused audit with interactive usefulness review. Resolves every `paths:` glob pattern against real project files, flags dead or over-broad patterns, then asks you rule-by-rule whether each rule still fires in the right context and whether its content is still accurate. Can apply edits in-place based on your answers. Use for periodic rules hygiene or when a rule fires too often/never. See `examples/skills/eval-rules/`.

### Skill Quality Gates

Before publishing or committing a skill, run through this content checklist. `/audit-agents-skills` scores frontmatter and structure; this checklist covers the content layer that automated tools miss.

**Checklist (Every.to compound-engineering criteria, adapted)**:

- [ ] **Frontmatter complete**: `name`, `description`, `allowed-tools` all present and accurate
- [ ] **"When to Apply" section**: explicitly states the triggers and anti-triggers (when NOT to use)
- [ ] **Methodology is structured**: numbered steps or a clear decision sequence, not free-form paragraphs
- [ ] **No TODOs or placeholders**: every section is complete and actionable
- [ ] **allowed-tools scoped to minimum**: if the skill only reads files, don't grant Bash; if it searches, don't grant Edit
- [ ] **Output format documented**: what does Claude produce? Example or template included
- [ ] **No AskUserQuestion for cross-platform skills**: skills invoked by other agents should not block on interactive prompts
- [ ] **Single responsibility**: one skill, one domain — not a catch-all that dispatches to sub-skills
- [ ] **Description is a trigger sentence**: the `description` field should tell Claude when to activate this skill, not what it does internally

A skill that passes these 9 gates is ready for production use or sharing via the agentskills.io registry.

## 5.X Skill Lifecycle & Retirement

Skills have a lifecycle. Treating them like permanent artifacts leads to skill rot: dead code in `.claude/skills/` that consumes tokens and provides no value.

Two patterns govern when to act:

```
CATCH REGRESSIONS                    SPOT OUTGROWTH
─────────────────                    ──────────────
Model Evolves                        Model Improves
      ↓                                    ↓
 Skill Drifts                     Skill Passes Alone
      ↓                              (without help)
 Eval Alerts                               ↓
 (early signal)                      Skill Retired
      ↓                           (no longer needed)
Fix or Retire
```

**Catch Regressions**: Your skill worked last month. The model updated. Now it behaves differently. Without evals, you discover this when a user reports a problem. With evals, you catch it before the failure reaches anyone.

**Spot Outgrowth**: You built a Capability Uplift skill to cover a gap. Six months later, Claude handles that gap natively. Run the eval without the skill — if it passes, the skill is no longer needed. Remove it to reduce context load and maintenance overhead.

### Retirement Decision Checklist

- [ ] **Run eval without the skill**: does Claude pass on its own?
- [ ] **Check last activation date**: when did this skill last fire in practice?
- [ ] **Check workflow accuracy**: for Encoded Preference skills, has the underlying process changed?
- [ ] **Archive before deleting**: move to `.claude/skills/archive/` with a dated note explaining why it was retired

> **See also**: [§5.Y Skill Evals](#5y-skill-evals) — how to run evals to inform retirement decisions.

---

## 5.Y Skill Evals

Skill evals move quality from "seems to work" to "know it works." They're the testing layer that makes skills production-grade.

> **Available via**: Skill Creator plugin (Anthropic GitHub) for Claude Code users. Live on Claude.ai and Cowork as of March 2026. Sources: ainews.com, mexc.co — not yet in official `llms-full.txt`.

### How It Works

```
Skill → Test Prompts + Files
              ↓
     Expected Output (what good looks like)
              ↓
          Run Evals
              ↓
      Pass ✓  /  Fail ✗
              ↓
     Improve skill → Re-run
```

You define three things: test prompts (realistic inputs that trigger the skill), expected outputs (description of what "good" looks like — not exact string matching), and a pass rate threshold. Claude executes the skill against each test case and judges the output.

Results report: pass rate, elapsed time, token usage per test case.

### The Three Eval Tools

**Benchmark Mode** — tracks pass rates, elapsed time, and token usage across model updates. Runs tests in parallel with clean, isolated contexts (no cross-contamination between cases). Use this to detect regressions automatically when Claude updates.

**A/B Testing (Comparator Agents)** — blind head-to-head comparison between two versions of a skill. Version A vs. Version B, judged without knowing which is which. Removes confirmation bias from skill improvement decisions.

**Trigger Tuning (Description Optimizer)** — analyzes your skill's `description` field and suggests improvements to reduce false positives (skill fires when it shouldn't) and false negatives (skill doesn't fire when it should). Anthropic's internal test: 5 of 6 document-creation skills showed improved triggering accuracy after optimization. [Source: claudecode.jp — directional, not independently verified]

### Two Uses of Evals

| Use Case | When | Action |
|----------|------|--------|
| **Catch Regressions** | After model updates | Run benchmark → alert if pass rate drops |
| **Spot Outgrowth** | Periodically for Capability Uplift skills | Run eval *without* the skill → if it passes, retire |

### Practical Eval Structure

```
.claude/skills/my-skill/
├── SKILL.md
└── tests/                      ← Eval directory
    ├── test-01-basic.md        # Prompt + expected output description
    ├── test-02-edge-case.md    # Edge case coverage
    └── benchmark-config.md     # Pass rate threshold, token budget
```

### Eval Design Principles

- **One behavior per test**: don't combine multiple assertions — failures become ambiguous
- **Include edge cases**: test the inputs that made the skill necessary in the first place
- **Define "good" precisely**: vague expected outputs make eval judgments unreliable
- **Set a pass rate threshold**: 80% is a reasonable starting point; adjust for criticality

> **See also**: [§5.2 Skill Quality Gates](#52-creating-skills) for pre-publish checklist | [§5.X Skill Lifecycle](#5x-skill-lifecycle--retirement) for retirement workflow

---

## 5.3 Skill Template

```markdown
---
name: your-skill-name
description: Expert guidance for [domain] problems
allowed-tools: Read Grep Bash
---

# Your Skill Name

## Expertise Areas

This skill provides knowledge in:
- [Area 1]
- [Area 2]
- [Area 3]

## When to Apply

Use this skill when:
- [Situation 1]
- [Situation 2]

## Methodology

When activated, follow this approach:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Key Concepts

### Concept 1: [Name]
[Explanation]

### Concept 2: [Name]
[Explanation]

## Checklists

### Pre-Implementation Checklist
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

### Post-Implementation Checklist
- [ ] [Verification 1]
- [ ] [Verification 2]

## Examples

### Good Pattern
```[language]
// Good example
```

### Anti-Pattern
```[language]
// Bad example - don't do this
```

## Reference Material

See `reference.md` for detailed documentation.

## 5.4 Skill Examples

### Example 1: Security Guardian Skill

```markdown
---
name: security-guardian
description: Security expertise for OWASP Top 10, auth, and data protection
allowed-tools: Read Grep Bash
---

# Security Guardian

## Expertise Areas

- OWASP Top 10 vulnerabilities
- Authentication & Authorization
- Data protection & encryption
- API security
- Secrets management

## OWASP Top 10 Checklist

### A01: Broken Access Control
- [ ] Check authorization on every endpoint
- [ ] Verify row-level permissions
- [ ] Test IDOR vulnerabilities
- [ ] Check for privilege escalation

### A02: Cryptographic Failures
- [ ] Check for hardcoded secrets
- [ ] Verify TLS configuration
- [ ] Review password hashing (bcrypt/argon2)
- [ ] Check data encryption at rest

### A03: Injection
- [ ] Review SQL queries (parameterized?)
- [ ] Check NoSQL operations
- [ ] Review command execution
- [ ] Check XSS vectors

[... more checklists ...]

## Authentication Patterns

### Good: Secure Password Hashing
```typescript
import { hash, verify } from 'argon2';

const hashedPassword = await hash(password);
const isValid = await verify(hashedPassword, inputPassword);
```

### Bad: Insecure Hashing
```typescript
// DON'T DO THIS
const hashed = md5(password);
const hashed = sha1(password);
```

## Secrets Management

### Never Commit Secrets
```
# .gitignore
.env
.env.local
*.pem
*credentials*
```

### Use Environment Variables
```typescript
// Good
const apiKey = process.env.API_KEY;

// Bad
const apiKey = "sk-1234567890abcdef";
```


### Example 2: TDD Skill

```markdown
---
name: tdd
description: Test-Driven Development methodology and patterns
allowed-tools: Read Write Bash
---

# TDD (Test-Driven Development)

## The TDD Cycle

┌─────────────────────────────────────────────────────────┐
│                    RED → GREEN → REFACTOR               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1. RED     ──→  Write a failing test                  │
│        │                                                │
│        ▼                                                │
│   2. GREEN   ──→  Write minimal code to pass            │
│        │                                                │
│        ▼                                                │
│   3. REFACTOR ──→  Improve code, keep tests green       │
│        │                                                │
│        └────────────→  Repeat                           │
│                                                         │
└─────────────────────────────────────────────────────────┘


## Methodology

### Step 1: RED (Write Failing Test)

Write a test for the behavior you want BEFORE writing any code.

```typescript
// user.test.ts
describe('User', () => {
  it('should validate email format', () => {
    expect(isValidEmail('test@example.com')).toBe(true);
    expect(isValidEmail('invalid')).toBe(false);
  });
});
```

Run: `pnpm test` → Should FAIL (function doesn't exist)

### Step 2: GREEN (Minimal Implementation)

Write the MINIMUM code to make the test pass.

```typescript
// user.ts
export const isValidEmail = (email: string): boolean => {
  return email.includes('@');
};
```

Run: `pnpm test` → Should PASS

### Step 3: REFACTOR (Improve)

Now improve the implementation while keeping tests green.

```typescript
// user.ts (improved)
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};
```

Run: `pnpm test` → Should still PASS

## Test Structure: AAA Pattern

```typescript
it('should calculate order total', () => {
  // Arrange - Set up test data
  const items = [
    { price: 10, quantity: 2 },
    { price: 5, quantity: 3 }
  ];

  // Act - Execute the code
  const total = calculateTotal(items);

  // Assert - Verify the result
  expect(total).toBe(35);
});
```

### Example 3: Design Patterns Analyzer Skill

**Purpose**: Detect, analyze, and suggest Gang of Four design patterns in TypeScript/JavaScript codebases with stack-aware recommendations.

**Location**: `examples/skills/design-patterns/`

**Key Features**:
- Detects 23 GoF design patterns (Creational, Structural, Behavioral)
- Stack-aware detection (React, Angular, NestJS, Vue, Express, RxJS, Redux, ORMs)
- Code smell detection with pattern suggestions
- Quality evaluation (5 criteria: Correctness, Testability, SRP, Open/Closed, Documentation)
- Prefers stack-native alternatives (e.g., React Context over Singleton)

**Structure**:
```
design-patterns/
├── SKILL.md                           # Main skill instructions
├── reference/
│   ├── patterns-index.yaml            # 23 patterns metadata
│   ├── creational.md                  # 5 creational patterns
│   ├── structural.md                  # 7 structural patterns
│   └── behavioral.md                  # 11 behavioral patterns
├── signatures/
│   ├── stack-patterns.yaml            # Stack detection + native alternatives
│   ├── detection-rules.yaml           # Grep patterns for detection
│   └── code-smells.yaml               # Smell → pattern mappings
└── checklists/
    └── pattern-evaluation.md          # Quality scoring system
```

**Operating Modes**:

1. **Detection Mode**: Find existing patterns in codebase
   ```bash
   # Invoke via skill or direct analysis
   "Analyze design patterns in src/"
   ```

2. **Suggestion Mode**: Identify code smells and suggest patterns
   ```bash
   "Suggest design patterns to fix code smells in src/services/"
   ```

3. **Evaluation Mode**: Score pattern implementation quality
   ```bash
   "Evaluate the Factory pattern implementation in src/lib/errors/"
   ```

**Example Output**:

```json
{
  "stack_detected": {
    "primary": "react",
    "version": "19.0",
    "secondary": ["typescript", "next.js", "prisma"],
    "detection_sources": ["package.json", "tsconfig.json"]
  },
  "patterns_found": {
    "factory-method": [{
      "file": "src/lib/errors/factory.ts",
      "lines": "12-45",
      "confidence": 0.9,
      "quality_score": 8.2,
      "notes": "Well-implemented with proper abstraction"
    }],
    "singleton": [{
      "file": "src/config.ts",
      "confidence": 0.85,
      "quality_score": 4.0,
      "recommendation": "Consider React Context instead"
    }]
  },
  "code_smells": [{
    "type": "switch_on_type",
    "file": "src/components/data-handler.tsx",
    "line": 52,
    "severity": "medium",
    "suggested_pattern": "strategy",
    "rationale": "Replace conditional logic with strategy objects"
  }]
}
```

**Stack-Native Recommendations**:

| Pattern | React Alternative | Angular Alternative | NestJS Alternative |
|---------|-------------------|---------------------|-------------------|
| Singleton | Context API + Provider | @Injectable() service | @Injectable() (default) |
| Observer | useState + useEffect | RxJS Observables | EventEmitter |
| Decorator | Higher-Order Component | @Decorator syntax | @Injectable decorators |
| Factory | Custom Hook pattern | Factory service | Provider pattern |

**Detection Methodology**:

1. **Stack Detection**: Analyze package.json, tsconfig.json, config files
2. **Pattern Search**: Use Glob → Grep → Read pipeline
   - Glob: Find candidate files (`**/*factory*.ts`, `**/*singleton*.ts`)
   - Grep: Match detection patterns (regex for key structures)
   - Read: Verify pattern implementation
3. **Quality Evaluation**: Score on 5 criteria (0-10 each)
4. **Smell Detection**: Identify anti-patterns and suggest refactoring

**Quality Evaluation Criteria**:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | Follows canonical pattern structure |
| Testability | 25% | Easy to mock, no global state |
| Single Responsibility | 20% | One clear purpose |
| Open/Closed | 15% | Extensible without modification |
| Documentation | 10% | Clear intent, usage examples |

**Example Usage in Agent**:

```markdown
---
name: architecture-reviewer
description: Review system architecture and design patterns
tools: Read, Grep, Glob
skills:
  - design-patterns  # Inherits pattern knowledge
---

When reviewing architecture:
1. Use design-patterns skill to detect existing patterns
2. Evaluate pattern implementation quality
3. Suggest improvements based on stack-native alternatives
4. Check for code smells requiring pattern refactoring
```

**Integration with Méthode Aristote**:

This skill is now installed in the Méthode Aristote repository at:
```
/Users/florianbruniaux/Sites/MethodeAristote/app/.claude/skills/design-patterns/
```

**Usage**:
1. Direct invocation: "Analyze design patterns in src/"
2. Via agent: Create an agent that inherits the design-patterns skill
3. Automated review: Use in CI/CD to detect pattern violations

**Reference**:
- Full documentation: `examples/skills/design-patterns/SKILL.md`
- Pattern reference: `examples/skills/design-patterns/reference/*.md`
- Detection rules: `examples/skills/design-patterns/signatures/*.yaml`

### Example 4: Tally Form Builder Skill

**Purpose**: Create and modify Tally forms via MCP — no browser, no UI, just `/tally-form-builder` and a description.

**Location**: `~/.claude/skills/tally-form-builder/`

**What This Pattern Demonstrates**: MCP wrapping with deferred tool loading. The Tally MCP tools are not available by default — their schemas must be fetched via `ToolSearch` before any call. This skill handles that automatically and documents all the gotchas that cause failures when calling the API blind.

**Key Features**:
- OAuth flow management (authenticate → browser → callback URL → complete)
- Block-chaining with `insertAfterBlockUuid` to preserve order
- HTML support awareness (TEXT blocks yes, option labels no)
- Batch text updates in a single call
- Known-issues reference file with 7 documented limitations and workarounds

**Structure**:
```
tally-form-builder/
├── SKILL.md                     # Full workflow + rules + anti-patterns
└── references/
    ├── block-types.md           # All block types with payloads and examples
    └── known-issues.md          # 7 limitations with workarounds
```

**Core Concept: Deferred Tools**

Tally MCP tools are deferred — calling them without `ToolSearch` first returns `InputValidationError`. The skill enforces a mandatory `ToolSearch` step before any MCP call. This pattern applies to any MCP server with deferred tools.

```
ToolSearch → authenticate → list_workspaces → create_new_form
          → create_blocks → configure_blocks → update_text → save_form
```

**Block Chaining Pattern**:

Each block must reference the UUID of the block that precedes it. The skill tracks UUIDs across calls to maintain correct insertion order:

```
FORM_TITLE (uuid: "abc")
  → create_blocks([TITLE], insertAfterBlockUuid: "abc") → returns "def"
  → create_blocks([CHECKBOX × N], insertAfterBlockUuid: "def") → returns "ghi"
  → create_blocks([PAGE_BREAK], insertAfterBlockUuid: "ghi") → ...
```

**Critical Rule**: `save_form` is mandatory. Without it, the form does not exist in Tally and `list_forms` returns 0 results.

**Usage**:

```
/tally-form-builder
Create a survey form on [topic] with:
- Page 1: intro + checkbox question with options [A, B, C, D]
- Page 2: context questions (team size, role)
- Page 3: optional contact info (first name, email)
Publish as PUBLISHED.
```

```
/tally-form-builder
Edit form [formId]:
- Change "2 min" to "3 min max" in the intro
- Add a "SMB" option to the team size question
```

**Key Limitations (documented in `references/known-issues.md`)**:
- Options (checkbox, dropdown, multiple choice) do not support HTML — labels are always plain text
- "Other" option generates a fixed small input; cannot be converted to a textarea via API
- `list_forms` always returns 0 until `save_form` is called

**Reference**:
- Full skill: `~/.claude/skills/tally-form-builder/SKILL.md`
- Block types: `~/.claude/skills/tally-form-builder/references/block-types.md`
- Known issues: `~/.claude/skills/tally-form-builder/references/known-issues.md`
- MCP wrapping template: `examples/skills/mcp-integration-reference/SKILL.md`

## 5.5 Community Skill Repositories

### Registry-based Discovery: ctx7 CLI

Before diving into specific repositories, Context7 provides a CLI companion (`ctx7`) that automates skill discovery and installation. Instead of manually cloning repos, `ctx7 skills suggest` analyzes your project's dependencies and recommends matching skills from the [context7.com/skills](https://context7.com/skills) registry — with trust scores to help evaluate quality.

**Install**:

```bash
npx ctx7 --help          # No install required (npx)
npm install -g ctx7       # Global install
```

**Discovery workflow**:

```bash
# Auto-detect project deps and suggest matching skills
npx ctx7 skills suggest

# Search by keyword
npx ctx7 skills search terraform

# Install from any GitHub repository
npx ctx7 skills install antonbabenko/terraform-skill
npx ctx7 skills install owner/repo

# List / remove installed skills
npx ctx7 skills list
npx ctx7 skills remove skill-name
```

**Setup wizard** (replaces manual `claude mcp add`):

```bash
# Configure Context7 for Claude Code — detects editor, picks MCP or CLI+Skills mode
npx ctx7 setup --claude
```

`ctx7 setup` runs a wizard that configures Context7 in the right mode for your editor. Use it when setting up Context7 for the first time instead of writing `claude mcp add` manually. The `--claude` flag targets Claude Code specifically; `--cursor` and `--universal` are available for other editors.

**Registry vs. agentskills.io**: The [agentskills.io](https://agentskills.io) specification is the open standard defining the skill format (supported by 30+ platforms — see §5.1). The [context7.com/skills](https://context7.com/skills) registry is a hosted directory of skills conforming to that standard. The two are complementary: agentskills.io defines the format, context7.com/skills is one place to discover and share conforming skills. Skills installed via `ctx7` land in `~/.claude/skills/` and work identically to manually installed ones.

**Skill generation** (authenticated, rate-limited):

```bash
npx ctx7 skills generate    # AI-generated custom skill
                             # Free: 6 generations/week — Pro: 10/week
```

Generation is best reserved for skills with no equivalent in the registry. For team onboarding at scale, the `suggest` + `install` workflow is more practical than generation.

**CLI doc lookup** (alternative to MCP):

```bash
# Search available libraries
npx ctx7 library react

# Fetch docs for a specific library + query
npx ctx7 docs /facebook/react "useEffect cleanup"
```

This is the terminal equivalent of what the Context7 MCP server does. Useful when you want to look something up yourself without invoking Claude, or in environments where MCP is not configured. Claude Code users who already have the MCP server active don't need this — Claude handles it automatically.

---

### Cybersecurity Skills Repository

The Claude Code community has created specialized skill collections for specific domains. One notable collection focuses on cybersecurity and penetration testing.

**Repository**: [zebbern/claude-code-guide](https://github.com/zebbern/claude-code-guide)
**Skills Directory**: [/skills](https://github.com/zebbern/claude-code-guide/tree/main/skills)

This repository contains **29 cybersecurity-focused skills** covering penetration testing, vulnerability assessment, and security analysis:

**Penetration Testing & Exploitation**
- SQL Injection Testing
- XSS (Cross-Site Scripting) Testing
- Broken Authentication Testing
- IDOR (Insecure Direct Object Reference) Testing
- File Path Traversal Testing
- Active Directory Attacks
- Privilege Escalation (Linux & Windows)

**Security Tools & Frameworks**
- Metasploit Framework
- Burp Suite Testing
- SQLMap Database Pentesting
- Wireshark Analysis
- Shodan Reconnaissance
- Scanning Tools

**Infrastructure Security**
- AWS Penetration Testing
- Cloud Penetration Testing
- Network 101
- SSH Penetration Testing
- SMTP Penetration Testing

**Application Security**
- API Fuzzing & Bug Bounty
- WordPress Penetration Testing
- HTML Injection Testing
- Top Web Vulnerabilities

**Methodologies & References**
- Ethical Hacking Methodology
- Pentest Checklist
- Pentest Commands
- Red Team Tools
- Linux Shell Scripting

#### Usage Example

To use these skills in your Claude Code setup:

1. Clone or download specific skills from the repository
2. Copy the skill folder to your `.claude/skills/` directory
3. Reference in your agents using the `skills` frontmatter field

```bash
# Example: Add SQL injection testing skill
cd ~/.claude/skills/
curl -L https://github.com/zebbern/claude-code-guide/archive/refs/heads/main.zip -o skills.zip
unzip -j skills.zip "claude-code-guide-main/skills/sql-injection-testing/*" -d sql-injection-testing/
```

Then reference in an agent:

```yaml
---
name: security-auditor
description: Security testing specialist for penetration testing
tools: Read, Grep, Bash
---
```

#### Important Disclaimer

> **Note**: These cybersecurity skills have not been fully tested by the maintainers of this guide. While they appear well-structured and comprehensive based on their documentation, you should:
>
> - **Test thoroughly** before using in production security assessments
> - **Ensure you have proper authorization** before conducting any penetration testing
> - **Review and validate** the techniques against your organization's security policies
> - **Use only in legal contexts** with written permission from system owners
> - **Contribute back** if you find issues or improvements

The skills appear to follow proper ethical hacking guidelines and include appropriate legal prerequisites, but as with any security tooling, verification is essential.

### claude-red: Offensive Security Skill Library

A more comprehensive alternative to the zebbern collection above. claude-red is a curated library of **58 offensive security skills** across 13 attack surface categories, built for authorized red team engagements, bug bounty hunting, and security audits on your own systems.

**Repository**: [SnailSploit/Claude-Red](https://github.com/SnailSploit/Claude-Red) — 1,200+ stars, MIT license, active maintenance (updated May 2026).

**Categories**: Web app (16 skills: SQLi, XSS, SSRF, SSTI, XXE, IDOR, RCE, deserialization, race conditions, request smuggling, WAF bypass, GraphQL…), Auth & Identity (JWT manipulation, OAuth exploitation), Active Directory, Wireless (13 skills), Cloud (AWS/Azure/GCP), Mobile (Android/iOS), IoT & Embedded, Infrastructure & Red Team, Exploit Development (6 skills), Fuzzing & Vulnerability Research, OSINT/Recon, AI Security, and Utility (fast triage checklist, reporting).

Each skill is a structured `SKILL.md` with frontmatter (name, description, trigger phrases), detailed methodology, tool enumeration, and escalation paths — not ready-to-copy exploits, but expert-level operational guidance.

#### One-Shot Usage (No Global Install)

The most important pattern with claude-red is loading skills **without permanently installing them**. This keeps your global `~/.claude/skills/` clean.

**Option 1 — Read directly in session**: Ask Claude to read a skill file and apply its methodology. The context disappears when the session closes.

**Option 2 — `--system-file` at launch**: Load one or more skills at session start via CLI:

```bash
# Single skill
claude --system-file path/to/Skills/utility/offensive-fast-checking/SKILL.md

# Multiple skills (concatenated)
cat Skills/utility/offensive-fast-checking/SKILL.md \
    Skills/web/offensive-sqli/SKILL.md \
  | claude --system-file /dev/stdin
```

**Option 3 — Project-level `.claude/skills/`**: Symlink only the relevant skills into the target repo's `.claude/skills/`, run the audit, then remove the directory. Zero pollution beyond the repo boundary.

#### Targeted Prompt Pattern

Rather than loading all 58 skills, craft a prompt that matches skills to your stack. This is the highest-value pattern: Claude reads only the skills relevant to your attack surface and applies them with your codebase as context.

Example for a Next.js + Prisma + Clerk app:

```
You are doing a security audit on this Next.js/tRPC/Prisma/Clerk codebase.

Read these skills in order:
1. Skills/utility/offensive-fast-checking/SKILL.md   — quick wins triage
2. Skills/web/offensive-idor/SKILL.md               — role-based access flaws
3. Skills/auth/offensive-jwt/SKILL.md               — Clerk JWT manipulation
4. Skills/web/offensive-sqli/SKILL.md               — Prisma ORM injection paths
5. Skills/ai/offensive-ai-security/SKILL.md         — prompt injection on AI endpoints

Priority vectors: IDOR between user roles, JWT algorithm confusion,
Prisma raw query injection, SSRF via external API integrations.

Codebase: [path to project root]

Start with the fast-checking triage, then dig into IDOR and auth.
```

Tailor the skill list to your actual stack: a Rust CLI project would load fuzzing and exploit-dev skills instead of web skills; a map application with external tile loading would prioritize SSRF and XSS over SQLi.

#### Ethical & Legal Scope

> Use only on systems you own or have explicit written authorization to test. The repository's [SECURITY.md](https://github.com/SnailSploit/Claude-Red/blob/main/SECURITY.md) details scope: authorized engagements, bug bounty programs, CTF competitions, and internal security research only. Misuse may violate computer-crime statutes (CFAA, Computer Misuse Act).

---

### Infrastructure as Code Skills

**Repository**: [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill)
**Author**: Anton Babenko (creator of [terraform-aws-modules](https://github.com/terraform-aws-modules), 1B+ downloads, AWS Community Hero)
**Documentation**: [terraform-best-practices.com](https://www.terraform-best-practices.com/)

A production-grade Claude Code skill for **Terraform** and **OpenTofu** infrastructure management, covering:

**Testing & Validation**
- Test strategy decision frameworks (native tests vs Terratest)
- Workflow examples for different testing scenarios

**Module Development**
- Naming conventions and versioning patterns
- Structural best practices for reusable modules

**CI/CD Integration**
- GitHub Actions and GitLab CI templates
- Cost estimation and compliance checks baked in

**Security & Compliance**
- Static analysis and policy-as-code integration
- Security scanning workflows

**Patterns & Anti-patterns**
- Side-by-side examples of recommended vs problematic approaches
- Decision frameworks over prescriptive rules

#### Why This Skill is Notable

This skill demonstrates several best practices for production-grade skill development:

1. **Marketplace distribution**: Uses `.claude-plugin/marketplace.json` for easy installation
2. **Structured references**: Organized `references/` directory with knowledge base
3. **Test coverage**: Includes `tests/` directory for skill validation
4. **Decision frameworks**: Emphasizes frameworks over rigid rules, enabling contextual decisions

#### Installation

```bash
# Via marketplace (if available)
/install terraform-skill@antonbabenko

# Manual installation
cd ~/.claude/skills/
git clone https://github.com/antonbabenko/terraform-skill.git terraform
```

#### Contributing

If you create specialized skills for other domains (DevOps, data science, ML/AI, etc.), consider sharing them with the community through similar repositories or pull requests to existing collections.

### Automatic Skill Generation: Claudeception

**Repository**: [blader/Claudeception](https://github.com/blader/Claudeception)
**Author**: Siqi Chen (@blader) | **Stars**: 1k+ | **License**: MIT

Unlike traditional skill repositories, Claudeception is a **meta-skill** that generates new skills during Claude Code sessions. It addresses a fundamental limitation: *"Every time you use an AI coding agent, it starts from zero."*

#### How It Works

1. **Monitors** your Claude Code sessions via hook activation
2. **Detects** non-obvious discoveries (debugging techniques, workarounds, project-specific patterns)
3. **Writes** new skill files with Problem/Context/Solution/Verification structure
4. **Retrieves** matching skills in future sessions when similar contexts arise

#### Validated Use Case

A user reported Claudeception auto-generated a `pre-merge-code-review` skill from their actual workflow—transforming an ad-hoc debugging session into a reusable, automatically-triggered skill.

#### Installation

```bash
# User-level installation
git clone https://github.com/blader/Claudeception.git ~/.claude/skills/claudeception

# Project-level installation
git clone https://github.com/blader/Claudeception.git .claude/skills/claudeception
```

See the [repository README](https://github.com/blader/Claudeception) for hook configuration.

#### Considerations

| Aspect | Recommendation |
|--------|----------------|
| **Governance** | Review generated skills periodically; archive or merge duplicates |
| **Overhead** | Hook-based activation adds evaluation per prompt |
| **Scope** | Start with non-critical projects to validate the workflow |
| **Quality gates** | Claudeception only persists tested, discovery-driven knowledge |

#### Why It's Notable

This skill demonstrates the **skill-that-creates-skills** pattern—a meta-approach where Claude Code improves itself through session learning. Inspired by academic work on reusable skill libraries (Voyager, CASCADE, SEAgent, Reflexion).

### Automatic Skill Improvement: Claude Reflect System

**Repository**: [claude-reflect-system](https://github.com/haddock-development/claude-reflect-system)
**Author**: Haddock Development | **Status**: Production-ready (2026)
**Marketplace**: [Agent Skills Index](https://agent-skills.md/skills/haddock-development/claude-reflect-system/reflect)

While Claudeception creates new skills from discovered patterns, **Claude Reflect System** automatically improves existing skills by analyzing Claude's feedback and detected corrections during sessions.

#### How It Works

Claude Reflect operates in two modes:

**Manual Mode** (`/reflect [skill-name]`):
```bash
/reflect design-patterns  # Analyze and propose improvements for specific skill
```

**Automatic Mode** (Stop hook):
1. **Monitors** Stop hook triggers (session end, error, explicit stop)
2. **Parses** session transcript for skill-related feedback
3. **Classifies** improvement type (correction, enhancement, new example)
4. **Proposes** skill modifications with confidence level (HIGH/MED/LOW)
5. **Waits** for explicit user review and approval
6. **Backs up** original skill file to Git
7. **Applies** changes with validation (YAML syntax, markdown structure)
8. **Commits** with descriptive message

#### Safety Features

| Feature | Purpose | Implementation |
|---------|---------|----------------|
| **User Review Gate** | Prevent automatic unwanted changes | All proposals require explicit approval before application |
| **Git Backups** | Enable rollback of bad improvements | Auto-commits before each modification with descriptive messages |
| **Syntax Validation** | Maintain skill file integrity | YAML frontmatter + markdown body validation before write |
| **Confidence Levels** | Prioritize high-quality improvements | HIGH (clear correction) > MED (likely improvement) > LOW (suggestion) |
| **Locking Mechanism** | Prevent concurrent modifications | File locks during analysis and application phases |

#### Installation

```bash
# Clone to skills directory
git clone https://github.com/haddock-development/claude-reflect-system.git \
  ~/.claude/skills/claude-reflect-system

# Configure Stop hook (add to ~/.claude/hooks/Stop.sh or Stop.ps1)
# Bash example:
echo '/reflect-auto' >> ~/.claude/hooks/Stop.sh
chmod +x ~/.claude/hooks/Stop.sh

# PowerShell example:
Add-Content -Path "$HOME\.claude\hooks\Stop.ps1" -Value "/reflect-auto"
```

See the [repository README](https://github.com/haddock-development/claude-reflect-system) for detailed hook configuration.

#### Use Case Example

**Problem**: You use a `terraform-validation` skill that doesn't catch a specific security misconfiguration. During the session, Claude detects and corrects the issue manually.

**Reflect System detects**:
- Claude corrected a pattern not covered by the skill
- Correction was verified (tests passed)
- High confidence (clear improvement)

**Proposal**:
```yaml
Skill: terraform-validation
Confidence: HIGH
Change: Add S3 bucket encryption validation
Diff:
  + - Check bucket encryption: aws_s3_bucket.*.server_side_encryption_configuration
  + - Reject: Encryption not set or using AES256 instead of aws:kms
```

**User reviews** → approves → **skill updated** → future sessions automatically catch this issue.

#### ⚠️ Security Warnings

Self-improving systems introduce specific security risks. Claude Reflect System includes mitigations, but users must remain vigilant:

| Risk | Description | Mitigation | User Responsibility |
|------|-------------|------------|---------------------|
| **Feedback Poisoning** | Adversarial inputs manipulate improvement proposals | User review gate, confidence scoring | Review all HIGH confidence proposals, reject suspicious changes |
| **Memory Poisoning** | Malicious edits to learned patterns accumulate | Git backups, syntax validation | Periodically audit skill history via Git log |
| **Prompt Injection** | Embedded instructions in session transcripts | Input sanitization, proposal isolation | Never approve proposals with executable commands |
| **Skill Bloat** | Unbounded growth without curation | Manual `/reflect [skill]` mode, curate regularly | Archive or merge redundant improvements quarterly |

**Academic sources**:
- [Anthropic Memory Cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/memory/guide.md) (official guidance on agent memory systems)
- Research on adversarial attacks against AI learning systems

#### Activation and Control

| Command | Effect |
|---------|--------|
| `/reflect-on` | Enable automatic Stop hook analysis |
| `/reflect-off` | Disable automatic analysis (manual mode only) |
| `/reflect [skill-name]` | Manually trigger analysis for specific skill |
| `/reflect status` | Show enabled/disabled state and recent proposals |

Default: **Disabled** (opt-in for safety)

#### Comparison: Claudeception vs Reflect System

| Aspect | Claudeception | Claude Reflect System |
|--------|---------------|----------------------|
| **Focus** | Skill generation (create new) | Skill improvement (refine existing) |
| **Trigger** | New patterns discovered | Corrections/feedback detected |
| **Input** | Session discoveries, workarounds | Claude's self-corrections, user feedback |
| **Review** | Implicit (skill created, user evaluates in next session) | Explicit (proposal shown, user approves/rejects) |
| **Safety** | Quality gates (only tested discoveries) | Git backups, syntax validation, confidence levels |
| **Use Case** | Bootstrap project-specific skills | Evolve skills based on real-world usage |
| **Overhead** | Hook evaluation per prompt | Stop hook evaluation (session end) |

#### Recommended Combined Workflow

1. **Bootstrap** (Claudeception): Let Claude generate skills from discovered patterns during initial project work
2. **Iterate** (Use skills): Apply generated skills in subsequent sessions
3. **Refine** (Reflect System): Enable `/reflect-on` to capture improvements as skills evolve with usage
4. **Curate** (Manual): Quarterly review via `/reflect status` and Git history to archive or merge redundant patterns

**Example timeline**:
- Week 1-2: Claudeception generates `api-error-handling` skill from debugging sessions
- Week 3-6: Skill used in 20+ sessions, catches 80% of error cases
- Week 7: Reflect detects 3 missed edge cases, proposes HIGH confidence additions
- Week 8: User approves, skill now catches 95% of cases automatically

#### Resources

- **GitHub Repository**: [haddock-development/claude-reflect-system](https://github.com/haddock-development/claude-reflect-system)
- **Marketplace**: [Agent Skills Index](https://agent-skills.md/skills/haddock-development/claude-reflect-system/reflect)
- **Video Tutorial**: [YouTube walkthrough](https://www.youtube.com/watch?v=...) (check repo for latest)
- **Academic Foundation**: [Anthropic Memory Cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/memory/guide.md)

### Design Intelligence: UI UX Pro Max

**Repository**: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
**Site**: [ui-ux-pro-max-skill.nextlevelbuilder.io](https://ui-ux-pro-max-skill.nextlevelbuilder.io/) | [uupm.cc](https://uupm.cc)
**Stars**: 33.7k | **Forks**: 3.3k | **License**: MIT | **Latest**: v2.2.1 (Jan 2026)

UI UX Pro Max is the most popular design skill in the AI coding assistant ecosystem. It adds a **design reasoning engine** to Claude Code (and 14 other assistants), replacing generic AI-generated UI with professional, industry-aware design systems.

The engine works offline — it runs BM25 search over ~400 local JSON rules to recommend styles, palettes, and typography. No external LLM calls, no network dependency at runtime.

#### What It Provides

| Asset | Count | Examples |
|-------|-------|---------|
| UI Styles | 67 | Glassmorphism, Brutalism, Bento Grid, AI-Native UI, Claymorphism… |
| Color Palettes | 96 | Industry-specific: SaaS, fintech, healthcare, e-commerce, luxury… |
| Font Pairings | 57 | Curated Google Fonts combinations with context rules |
| Chart Types | 25 | Dashboard, analytics, BI recommendations |
| UX Guidelines | 99 | Best practices, anti-patterns, accessibility rules |
| Industry Reasoning Rules | 100 | SaaS, fintech, healthcare, e-commerce, beauty, Web3, gaming… |

#### Flagship Feature: Design System Generator

The Design System Generator (v2.0+) analyzes your product type and generates a complete, tailored design system in seconds:

```bash
# Generate design system for a SaaS dashboard project
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "saas analytics dashboard" \
  --design-system -p "MyApp"

# Output: pattern + style + palette + typography + effects + anti-patterns + checklist
```

**Master + Override pattern** for multi-page projects:

```bash
# Generate and persist a global design system
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "saas dashboard" \
  --design-system --persist -p "MyApp"

# Create page-specific overrides
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "checkout flow" \
  --design-system --persist -p "MyApp" --page "checkout"
```

This creates a `design-system/` folder:
```
design-system/
├── MASTER.md          # Global: colors, typography, spacing, components
└── pages/
    └── checkout.md    # Page-specific overrides only
```

Reference in your Claude Code prompts:
```
I am building the Checkout page.
Read design-system/MASTER.md, then check design-system/pages/checkout.md.
Prioritize page rules if present, otherwise use Master rules.
Now generate the code.
```

#### Installation

**Option 1 — Claude Marketplace** (two commands):
```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

**Option 2 — CLI** (recommended):
```bash
npm install -g uipro-cli
cd /path/to/your/project
uipro init --ai claude   # Claude Code
```

**Option 3 — Manual** (no npm):
```bash
git clone --depth=1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill /tmp/uipro
cp -r /tmp/uipro/.claude/skills/ui-ux-pro-max .claude/skills/
```

**Prerequisite**: Python 3.x must be installed (the reasoning engine is a Python script).

#### Usage

Once installed, the skill activates automatically for UI/UX requests in Claude Code:

```
Build a landing page for my SaaS product
Create a dashboard for healthcare analytics
Design a fintech app with dark theme
```

#### Considerations

| Aspect | Notes |
|--------|-------|
| **Scope** | Multi-platform — supports Cursor, Windsurf, Copilot, Gemini CLI, and 10 others alongside Claude Code |
| **Quality signal** | 33.7k stars, 3.3k forks in 3 months — strongest community traction of any design skill |
| **Maintenance** | Active — v2.0→v2.2.1 in 10 days (Jan 2026), updated regularly |
| **Chinese community** | Strong adoption: listed on [jimmysong.io](https://jimmysong.io/ai/ui-ux-pro-max-skill/), benchmark repos in Chinese dev ecosystem |

> **Security note**: `npm install -g uipro-cli` installs a package from an anonymous organization ("nextlevelbuilder") globally. Source audit (Feb 2026) confirmed:
> - **No preinstall/postinstall scripts** in the npm package
> - **No network calls** in the Python engine (`search.py`, `core.py`, `design_system.py` — stdlib + local CSV/JSON only)
>
> Option 3 (manual git clone) remains the safest route if you want to inspect before installing. The package has not been formally audited by Anthropic or the maintainers of this guide.

### DevOps & SRE Guide

For comprehensive DevOps/SRE workflows, see **[DevOps & SRE Guide](./ops/devops-sre.md)**:
- **The FIRE Framework**: First Response → Investigate → Remediate → Evaluate
- **Kubernetes troubleshooting**: Prompts by symptom (CrashLoopBackOff, OOMKilled, etc.)
- **Incident response**: Solo and multi-agent patterns
- **IaC patterns**: Terraform, Ansible, GitOps workflows
- **Guardrails**: Security boundaries and team adoption checklist

**Quick Start**: [Agent Template](../examples/agents/devops-sre.md) | [CLAUDE.md Template](../examples/claude-md/devops-sre.md)

### Skills Marketplace: skills.sh

**URL**: [skills.sh](https://skills.sh/) | **GitHub**: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | **Launched**: January 21, 2026

Skills.sh (Vercel Labs) provides a centralized marketplace for discovering and installing agent skills with one-command installation:

```bash
npx add-skill vercel-labs/agent-skills  # React/Next.js best practices (35K+ installs)
npx add-skill supabase/agent-skills     # Postgres optimization patterns
npx add-skill anthropics/skills         # Frontend design + skill-creator
npx add-skill anthropics/claude-plugins-official  # CLAUDE.md auditor + automation recommender
```

#### How It Works

**Installation**: Skills are copied to `~/.claude/skills/` (same format as this guide)

**Supported agents**: 20+ including Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, Goose, and others

**Format**: Standard SKILL.md with YAML frontmatter (100% compatible with Section 5.2-5.3)

#### Top Skills by Category (January 2026)

| Category | Top Skills | Installs | Creator |
|----------|-----------|----------|---------|
| **Frontend** | vercel-react-best-practices | 35K+ | vercel-labs |
| | web-design-guidelines | 26.6K | vercel-labs |
| | frontend-design | 5.6K | anthropics |
| **Database** | supabase-postgres-best-practices | 1K+ | supabase |
| **Auth** | better-auth-best-practices | 2K+ | better-auth |
| **Testing** | test-driven-development | 721 | obra ([Superpowers](https://github.com/obra/superpowers)) |
| **Media** | remotion-best-practices | New | remotion-dev |
| **Meta** | skill-creator | 3.2K | anthropics |
| **Tooling** | claude-md-improver | 472 | anthropics |
| | claude-automation-recommender | 333 | anthropics |

Full catalog: [skills.sh leaderboard](https://skills.sh/)

#### Security Audits (February 2026)

Vercel launched automated security scanning on every skills.sh skill ([announcement, Feb 17, 2026](https://vercel.com/changelog/automated-security-audits-now-available-for-skills-sh)), partnering with three independent security firms covering 60,000+ skills:

| Partner | Method | Performance |
|---------|--------|-------------|
| **Socket** | Cross-ecosystem static analysis + LLM-based noise reduction (curl\|sh, obfuscation, exfiltration, suspicious deps) | 95% precision, 97% F1 |
| **Snyk** | `mcp-scan` engine: LLM judges + deterministic rules, detects "toxic flows" between natural language and executable code | 90-100% recall, 0% false positives on legit skills |
| **Gen (Agent Trust Hub)** | Real-time monitoring of connections in/out of agents to prevent data exfiltration and prompt injection | Continuous |

**Risk levels** displayed on every skill page and shown before installation via `skills@1.4.0+`:

| Rating | Meaning |
|--------|---------|
| ✅ Safe | Verified against security best practices |
| 🟡 Low Risk | Minor risk indicators detected |
| 🔴 High Risk | Significant security concerns |
| ☠️ Critical | Severe or malicious behavior — hidden from search |

**Continuous monitoring**: skills are re-evaluated as detection improves. If a repository becomes malicious after install, its rating updates automatically.

> **Mental model**: treat a skill like a Docker image — it's an executable dependency, not a prompt. Verify the rating before installing in production.

#### Status & Trade-offs

**Status**: Launched Jan 21, 2026, security-audited since Feb 17, 2026 (Socket + Snyk + Gen)

**Governance**: Community project by Vercel Labs (not official Anthropic). Skills contributed by Vercel, Anthropic, Supabase, and community members.

**Trade-offs**:
- ✅ Centralized discovery + leaderboard (200+ skills)
- ✅ One-command install (vs manual GitHub clone)
- ✅ Format 100% compatible with this guide
- ✅ Automated 3-layer security audit before installation
- ✅ Continuous monitoring post-install
- ⚠️ Multi-agent focus (not Claude Code specific)
- ⚠️ Skills require explicit invocation; agents only auto-invoke them ~56% of the time ([Gao, 2026](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)). For critical instructions, prefer always-loaded CLAUDE.md

#### When to Use

| Use Case | Recommendation |
|----------|----------------|
| **Discover popular patterns** | skills.sh (leaderboard, trending) |
| **Install official framework skills** | skills.sh (Vercel React, Supabase, etc.) |
| **Team-specific/internal skills** | GitHub repos (like [claude-code-templates](https://github.com/davila7/claude-code-templates), 17K⭐) |
| **Custom enterprise skills** | Local `.claude/skills/` (Section 5.2-5.3) |

#### Installation Examples

**Standard installation** (global, all Claude Code sessions):
```bash
# Install Vercel bundle (3 skills: react + web-design + deploy)
npx add-skill vercel-labs/agent-skills

# Install Supabase Postgres patterns
npx add-skill supabase/agent-skills

# Verify installation
ls ~/.claude/skills/
# Output: react-best-practices/ web-design-guidelines/ vercel-deploy/
```

**Manual installation** (project-specific):
```bash
# Clone from GitHub
git clone https://github.com/vercel-labs/agent-skills.git /tmp/agent-skills

# Copy specific skill
cp -r /tmp/agent-skills/react-best-practices .claude/skills/

# Claude Code auto-discovers skills in .claude/skills/
```

#### References

- [Vercel Changelog: Introducing Agent Skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [Vercel Changelog: Automated security audits for skills.sh](https://vercel.com/changelog/automated-security-audits-now-available-for-skills-sh)
- [Snyk Blog: Securing the Agent Skill Ecosystem](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/)
- [Gen + Vercel: Agent Trust Hub partnership](https://www.prnewswire.com/news-releases/gen-and-vercel-partner-to-bring-independent-safety-verification-to-the-ai-skills-ecosystem-302691006.html)
- [GitHub: vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
- [Platform Claude Docs: Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- See also: [AI Ecosystem Guide](./ecosystem/ai-ecosystem.md) for complementary tools

---


