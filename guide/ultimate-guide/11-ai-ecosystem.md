# 11. AI Ecosystem: Complementary Tools

_Quick jump:_ [Why Complementarity](#111-why-complementarity-matters) · [Tool Matrix](#112-tool-matrix) · [Practical Workflows](#113-practical-workflows) · [Integration Patterns](#114-integration-patterns)

---

**Reading time**: 10 minutes

**Skill level**: Intermediate

**Goal**: Chain Claude Code with the right AI tools for optimal workflows

> **TL;DR**: Claude Code excels at contextual reasoning and multi-file implementation. Combine it with Perplexity (research), Gemini (images), Kimi (slides), and NotebookLM (synthesis) for a complete AI-powered development workflow.

## 11.1 Why Complementarity Matters

Claude Code is designed to be your **implementation partner** with deep codebase understanding. It deliberately doesn't try to do everything—and that's a strength.

### What Claude Code Does Best

| Capability | Why Claude Excels |
|-----------|------------------|
| **Contextual reasoning** | Reads entire project, understands patterns |
| **Multi-file editing** | Coordinates changes across modules |
| **Test integration** | Generates tests that understand your code |
| **CLI automation** | Perfect for CI/CD pipelines |
| **Persistent memory** | CLAUDE.md files maintain context |

### Where Other Tools Add Value

| Gap | Why | Solution |
|-----|-----|----------|
| **Deep research with sources** | WebSearch is limited (~5-10 sources) | Perplexity Pro (100+ verified sources) |
| **Image → Code** | No visual understanding | Gemini 2.5 (superior image analysis) |
| **Slide generation** | Limited PPTX (via Claude in PowerPoint add-in, research preview) | Kimi (native PowerPoint generation) |
| **Audio synthesis** | No TTS capability | NotebookLM (podcast-style overviews) |
| **Live browser prototyping** | No visual preview | v0.dev, Bolt (instant preview) |
| **Rate limits / cost control** | Per-token billing, API limits | cc-copilot-bridge (flat-rate via Copilot) |

The goal isn't replacement—it's **chaining the right tool for each step**.

## 11.2 Tool Matrix

### Quick Decision Guide

| I need to... | Use | Why Not Claude |
|--------------|-----|----------------|
| Implement a feature | **Claude Code** | ✅ Best choice |
| Research before implementing | **Perplexity** | Limited sources, no citations |
| Convert mockup to code | **Gemini → Claude** | Limited visual understanding |
| Create stakeholder deck | **Claude in PowerPoint (add-in)** or **Kimi** | Native PPTX generation limited to add-in |
| Understand new codebase quickly | **NotebookLM → Claude** | No audio synthesis |
| Rapid UI prototype | **v0/Bolt → Claude** | No live preview |
| Quick inline edits | **IDE + Copilot** | Context switching overhead |

### Complementary Tools Overview

| Tool | Primary Strength | Free Tier | Pro Cost |
|------|-----------------|-----------|----------|
| **[Perplexity](https://perplexity.ai)** | Research with verified sources | 5 Pro searches/day | $20/month |
| **[Gemini](https://gemini.google.com)** | Image understanding → code | Generous | $19.99/month |
| **[Kimi](https://kimi.ai)** | PPTX generation, 128K context | Generous | Free |
| **[NotebookLM](https://notebooklm.google.com)** | Doc synthesis + audio + **MCP integration** | Full features | Free |
| **[v0.dev](https://v0.dev)** | UI prototyping (Shadcn) | Limited | $20/month |
| **[Cursor](https://cursor.sh)** | IDE with AI autocomplete | Limited | $20/month |
| **[cc-copilot-bridge](https://github.com/FlorianBruniaux/cc-copilot-bridge)** | Multi-provider switching | Full | Copilot Pro $10/month |

### Multi-Provider Setup: cc-copilot-bridge

For heavy Claude Code usage, **cc-copilot-bridge** routes requests through GitHub Copilot Pro ($10/month) instead of Anthropic's per-token billing.

**What it solves:**
- Rate limits during intensive development sessions
- Cost optimization for high-volume usage (99%+ savings possible)
- Offline development with Ollama for proprietary code

**Quick Setup:**
```bash
# Install
git clone https://github.com/FlorianBruniaux/cc-copilot-bridge.git
cd cc-copilot-bridge && ./install.sh

# Use (3-character aliases)
ccc   # Copilot mode (flat $10/month via Copilot Pro)
ccd   # Direct mode (Anthropic per-token)
cco   # Offline mode (Ollama, 100% local)
```

**Cost Comparison:**

| Scenario | Anthropic Direct | With Copilot Pro | Savings |
|----------|------------------|-------------------|---------|
| Heavy daily usage | ~$300/month | $10/month | ~97% |
| 100M tokens/month | $1,500 | $10 | 99.3% |

> **Note**: Requires GitHub Copilot Pro subscription ($10/month) which provides access to Claude models through VS Code's API.

See: [cc-copilot-bridge Quick Start](https://github.com/FlorianBruniaux/cc-copilot-bridge#-quick-start)

### Local Execution Bridge (Opus Plan → LM Studio Execute)

For maximum cost savings, use Claude Code (Opus) for planning only, then execute locally via LM Studio.

**Architecture:**

```
┌──────────────┐     store_memory      ┌─────────────────┐
│ Claude Code  │ ─────────────────────►│    doobidoo     │
│   (Opus)     │   tag: "plan"         │   SQLite + Vec  │
│   PLANNER    │   status: "pending"   └────────┬────────┘
└──────────────┘                                │
                                                ▼
                                       ┌─────────────────┐
                                       │   bridge.py     │
                                       │  (Python CLI)   │
                                       └────────┬────────┘
                                                │ HTTP
                                                ▼
                                       ┌─────────────────┐
                                       │    LM Studio    │
                                       │  localhost:1234 │
                                       │   (MLX local)   │
                                       └─────────────────┘
```

**Cost model:**
- Planning (Opus): ~$0.50-2.00 per complex plan
- Execution (LM Studio): Free (100% local)
- **ROI**: 80-90% cost reduction on implementation tasks

**Setup:**

```bash
# Requires doobidoo MCP and LM Studio running
pip install httpx

# Health check
python examples/scripts/bridge.py --health

# List pending plans
python examples/scripts/bridge.py --list

# Execute all pending plans
python examples/scripts/bridge.py
```

**Workflow:**

1. **Claude Code creates plan** (stored in doobidoo):
```json
{
  "$schema": "bridge-plan-v1",
  "id": "plan_jwt_migration",
  "status": "pending",
  "context": {
    "objective": "Migrate auth to JWT",
    "files_context": {"src/auth.py": "LOAD"}
  },
  "steps": [
    {"id": 1, "type": "analysis", "prompt": "..."},
    {"id": 2, "type": "code_generation", "depends_on": [1], "file_output": "src/jwt.py"}
  ]
}
```

2. **Bridge executes locally** via LM Studio
3. **Results stored** back in doobidoo for Claude Code to review

**When to use:**
- Implementation tasks (not architectural decisions)
- Code generation with clear specs
- Bulk transformations
- When Opus planning + local execution beats Opus end-to-end

See: [`examples/scripts/bridge.py`](../examples/scripts/bridge.py), [`examples/scripts/README.md`](../examples/scripts/README.md)

## 11.3 Practical Workflows

### Research → Code Pipeline

Use when: You need to understand best practices before implementing.

```
┌─────────────────────────────────────────────────────────┐
│ 1. PERPLEXITY (Deep Research Mode - 5 min)              │
│                                                         │
│    "Research JWT refresh token best practices for       │
│     Next.js 15. Include security, common pitfalls,      │
│     and compare jose vs jsonwebtoken libraries."        │
│                                                         │
│    → Output: 2000-word spec with 20+ sources           │
│    → Export: Copy as Markdown → spec.md                │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ 2. CLAUDE CODE                                          │
│    > claude                                             │
│                                                         │
│    "Implement JWT refresh per @spec.md.                 │
│     Use jose library as recommended.                    │
│     Add to src/lib/auth/. Include tests."               │
│                                                         │
│    → Output: Working implementation + tests            │
└─────────────────────────────────────────────────────────┘
```

**When to use**: Any implementation requiring ecosystem knowledge, library comparisons, or security considerations.

### Visual → Code Pipeline

Use when: You have mockups, screenshots, or diagrams to implement.

```
┌─────────────────────────────────────────────────────────┐
│ 1. GEMINI 2.5 PRO                                       │
│                                                         │
│    Upload: dashboard-mockup.png                         │
│    "Convert to React component with Tailwind.           │
│     Include responsive breakpoints and accessibility."  │
│                                                         │
│    → Output: Initial JSX + Tailwind code               │
└───────────────────────────┬─────────────────────────────┘
                            ↓ Copy to clipboard
┌─────────────────────────────────────────────────────────┐
│ 2. CLAUDE CODE                                          │
│                                                         │
│    "Integrate this component into our Next.js app:      │
│     - Use our Button, Avatar components                 │
│     - Add TypeScript types matching User interface      │
│     - Connect to getUserProfile API hook                │
│     - Add loading and error states"                     │
│                                                         │
│    → Output: Production-ready integrated component     │
└─────────────────────────────────────────────────────────┘
```

**When to use**: Figma exports, whiteboard sketches, architecture diagrams, error screenshots.

### Documentation Pipeline

Use when: You need to quickly understand a new codebase or create audio overviews.

```
┌─────────────────────────────────────────────────────────┐
│ 1. EXPORT DOCS (Claude Code)                            │
│                                                         │
│    "Combine all markdown from docs/ into one file.      │
│     Include README.md and CLAUDE.md."                   │
│                                                         │
│    → Output: combined-docs.md                          │
└───────────────────────────┬─────────────────────────────┘
                            ↓ Upload to NotebookLM
┌─────────────────────────────────────────────────────────┐
│ 2. NOTEBOOKLM                                           │
│                                                         │
│    - Add combined-docs.md as source                     │
│    - Click "Generate Audio Overview"                    │
│    - Listen during commute (10-15 min)                  │
│                                                         │
│    → Output: Podcast-style system overview             │
└───────────────────────────┬─────────────────────────────┘
                            ↓ Take notes, return to Claude
┌─────────────────────────────────────────────────────────┐
│ 3. CLAUDE CODE                                          │
│                                                         │
│    "Based on my understanding from the audio:           │
│     Help me deep-dive into the payment flow."           │
│                                                         │
│    → Output: Contextual explanation + code walkthrough │
└─────────────────────────────────────────────────────────┘
```

**When to use**: Joining new team, reviewing unfamiliar codebase, onboarding prep.

> **💡 MCP Integration Available**: You can now query NotebookLM notebooks directly from Claude Code using the NotebookLM MCP server. See [ai-ecosystem.md § 4.1](./ecosystem/ai-ecosystem.md#41-notebooklm-mcp-integration) for installation and usage guide.

### Presentation Pipeline

Use when: You need to communicate technical changes to stakeholders.

```
┌─────────────────────────────────────────────────────────┐
│ 1. CLAUDE CODE                                          │
│                                                         │
│    "Summarize changes from last 5 commits.              │
│     Format: Overview, Key Features, Breaking Changes,   │
│     Migration Steps. Use business-friendly language."   │
│                                                         │
│    → Output: changes-summary.md                        │
└───────────────────────────┬─────────────────────────────┘
                            ↓ Upload to Kimi
┌─────────────────────────────────────────────────────────┐
│ 2. KIMI                                                 │
│                                                         │
│    "Create 10-slide deck for non-technical stakeholders.│
│     One key message per slide.                          │
│     Include summary and next steps."                    │
│                                                         │
│    → Output: stakeholder-update.pptx                   │
└─────────────────────────────────────────────────────────┘
```

**When to use**: Sprint demos, release announcements, executive updates.

## 11.4 Integration Patterns

### Full Workflow: Research-Heavy Feature

```bash
# 1. Research (Perplexity - 10 min)
# → "Best practices for WebSocket in Next.js 15"
# → Export to websocket-spec.md

# 2. Implementation (Claude Code - 40 min)
claude
> "Implement WebSocket per websocket-spec.md.
   Add to src/lib/websocket/. Include reconnection."

# 3. Stakeholder update (Kimi - 5 min)
# → Upload changes + screenshots
# → Generate 5-slide deck
```

### Full Workflow: Visual-Heavy Feature

```bash
# 1. UI Prototype (v0 - 10 min)
# → Generate dashboard layout

# 2. Visual refinement (Gemini - 5 min)
# → Upload Figma polish → Get refined code

# 3. Integration (Claude Code - 30 min)
claude
> "Integrate this dashboard.
   Connect to our data hooks. Add TypeScript types."
```

### Recommended Tool Stack by Budget

| Budget | Stack | Monthly |
|--------|-------|---------|
| **Minimal** | Claude Code + Perplexity Pro | $40-70 |
| **Balanced** | + Gemini + Cursor | $80-110 |
| **Power** | + v0 Pro | $100-130 |

### Cost Optimization Tips

1. **Use Haiku** for simple tasks (`/model haiku`)
2. **Batch research** in Perplexity Deep Research sessions
3. **Use free tiers**: NotebookLM, Kimi, Gemini Flash are free
4. **Check context** regularly (`/status`) to avoid waste
5. **Use Opus sparingly** - reserve for architectural decisions

---

> **📖 Deep Dive**: For detailed integration patterns, ready-to-use prompts, and tool comparisons, see the [complete AI Ecosystem guide](./ecosystem/ai-ecosystem.md).

### For Non-Developers: Claude Cowork

If you work with non-technical team members, **Cowork** brings Claude's agentic capabilities to knowledge workers without requiring terminal access.

| Aspect | Claude Code | Cowork |
|--------|-------------|--------|
| Target | Developers | Knowledge workers |
| Interface | Terminal | Desktop app |
| Execute code | Yes | No (files only) |
| Outputs | Code, scripts | Excel, PPT, docs |
| Status | Production | Research preview |

**Collaboration pattern**: Developers use Claude Code for specs → PMs use Cowork for stakeholder summaries. Shared context via `~/Shared/CLAUDE.md`.

> **Availability**: Pro ($20/mo) or Max ($100-200/mo) subscribers, macOS only (Jan 2026).
> See [AI Ecosystem Section 9](./ecosystem/ai-ecosystem.md#9-claude-cowork-research-preview) for details.

## Further Reading

### Whitepapers (FR + EN)

A series of 9 focused whitepapers covering Claude Code topics in depth, available in French and English:

| # | Topic | Scope |
|---|-------|-------|
| 00 | Foundations | First steps, core concepts |
| 01 | Effective Prompts | Prompting method, context, hooks |
| 02 | Customization | CLAUDE.md, agents, skills |
| 03 | Security | 17 hooks, threat DB, permissions |
| 04 | Architecture | Agent loop, context, token pricing |
| 05 | Team Deployment | CI/CD, observability, 50+ devs |
| 06 | Privacy & Compliance | Anthropic data, ZDR, retention |
| 07 | Reference Guide | Complete synthesis + workflows |
| 08 | Agent Teams | Multi-agent orchestration |

→ **[Download all whitepapers (FR + EN)](https://cc.bruniaux.com/whitepapers/)**

---

### Advanced Workflows

For advanced autonomous workflows, see Nick Tune's [Coding Agent Development Workflows](https://medium.com/nick-tune-tech-strategy-blog/coding-agent-development-workflows-af52e6f912aa) - a pipeline-driven approach focusing on fully autonomous PR generation with multi-tool orchestration.


### Community Resources

The Claude Code ecosystem is growing rapidly. Here are curated resources to continue learning:

#### Awesome Lists

| Repository | Focus |
|------------|-------|
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Commands, workflows, IDE integrations |
| [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Custom skills collection |
| [awesome-claude-skills (BehiSecc)](https://github.com/BehiSecc/awesome-claude-skills) | Skills taxonomy (62 skills, 12 categories) |
| [youtube-skills](https://github.com/ZeroPointRepo/youtube-skills) | YouTube skills pack (search, transcripts, chapters, analysis) |
| [awesome-claude](https://github.com/alvinunreal/awesome-claude) | General Claude resources (SDKs, tools) |

#### Frameworks

| Framework | Description | Link |
|-----------|-------------|------|
| **SuperClaude** | Advanced configuration framework with 30+ commands (`/sc:*`), cognitive personas, and MCP integration | [GitHub](https://github.com/SuperClaude-Org/SuperClaude_Framework) |

SuperClaude transforms Claude Code into a structured development platform through behavioral instruction injection. Key features:
- 30+ specialized commands for common dev tasks
- Smart personas for different contexts
- MCP server integration
- Task management and session persistence
- **Behavioral modes** for optimized workflows

#### Production Config Collections

For **battle-tested, ready-to-use configurations** from production environments:

| Repository | Author | Stats | Focus |
|------------|--------|-------|-------|
| [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | Affaan Mustafa (Anthropic hackathon winner) | ⭐ 31.9k | Production configs from 10+ months intensive use |

**Why this matters**: This is the **largest community-validated Claude Code resource** (31.9k stars in 9 days). Unlike tutorials, these are **configs proven in production** through winning Anthropic's hackathon (Zenith project).

**Unique innovations not found elsewhere**:
- **hookify**: Conversational hook creation (describe need → JSON generated)
- **pass@k metrics**: Formal verification approach (k=3 → 91% success rate)
- **Sandboxed subagents**: Tool restrictions per agent (security-reviewer can't Edit files)
- **Strategic compaction skills**: Manual compaction suggestions to manage context growth
- **Plugin ecosystem**: One-command installation for all configs

**Positioning**: Complementary to this guide—we teach concepts ("why"), they provide production configs ("how").

**See also**: [Comprehensive evaluation](../docs/resource-evaluations/015-everything-claude-code-github-repo.md) (Score 5/5)

---

#### SuperClaude Behavioral Modes

> ⚠️ **Non-official Extension**: SuperClaude flags (`--learn`, `--uc`, `--think`, etc.) are **NOT Claude Code CLI flags**. They work via prompt injection in CLAUDE.md files and require installing the SuperClaude framework.

SuperClaude includes configurable behavioral modes stored in `~/.claude/MODE_*.md` files:

| Mode | Purpose | Activation |
|------|---------|------------|
| **Orchestration** | Smart tool selection, parallel execution | Auto (multi-tool ops, >75% context) |
| **Task Management** | Hierarchical task tracking with memory | Auto (>3 steps, >2 directories) |
| **Token Efficiency** | Symbol-enhanced compression (30-50% reduction) | Auto (>75% context) or `--uc` |
| **Learning** | Just-in-time skill development | `--learn` flag or "why/how" questions |

#### Learning Mode: Installation & Usage

Learning Mode provides contextual explanations when techniques are first used, without overwhelming you with repeated explanations.

**Installation**:

1. Create the mode file:
```bash
# Create MODE_Learning.md in your global Claude config
touch ~/.claude/MODE_Learning.md
```

2. Add the content (or copy from SuperClaude framework):
```markdown
# Learning Mode

**Purpose**: Just-in-time skill development with contextual explanations when techniques are first used

## Activation Triggers
- Manual flag: `--learn`, `--learn focus:[domain]`
- User explicitly asks "why?" or "how?" about an action
- First occurrence of advanced technique in session

## Default Behavior
**OFF by default** - Activates via triggers above or explicit `--learn` flag

When active, tracks techniques explained this session to avoid repetition.
```

3. Register in `~/.claude/CLAUDE.md`:
```markdown
# Behavioral Modes
@MODE_Learning.md
```

4. Add flags to `~/.claude/FLAGS.md`:
```markdown
**--learn**
- Trigger: User requests learning mode, beginner signals, "why/how" questions
- Behavior: Enable just-in-time explanations with first-occurrence tracking

**--no-learn**
- Trigger: User wants pure execution without educational offers
- Behavior: Suppress all learning mode offers
```

**Usage**:

```bash
# Activate for entire session
claude --learn

# Focus on specific domain
claude --learn focus:git
claude --learn focus:architecture
claude --learn focus:security

# Batch explanations at end
claude --learn batch
```

**Offer Format**:

When Learning Mode is active, Claude offers explanations after technical actions:

```
git rebase -i HEAD~3
-> Explain: rebase vs merge? (y/detail/skip)
```

Response options:
- `y` → Surface explanation (20-50 tokens)
- `detail` → Medium depth (100-200 tokens)
- `skip` → Continue without explanation

**With Token Efficiency Mode** (compressed format):
```
git rebase -i HEAD~3
-> ?rebase
```

**Integration with Other Modes**:

| Combined With | Behavior |
|---------------|----------|
| Token Efficiency (`--uc`) | Compressed offer format: `-> ?[concept]` |
| Task Management | Batch explanations at phase completion |
| Brutal Advisor | Brutal on diagnosis, pedagogical on explanation |

**Priority Rules**:
```
--no-learn > --uc > --learn
Token Efficiency constraints > Learning verbosity
Task flow > Individual explanations
```

**Example Session**:

```bash
$ claude --learn

You: Refactor the authentication module

Claude: [Reads files, implements changes]
git rebase -i HEAD~3
-> Explain: rebase vs merge? (y/detail/skip)

You: y

Claude: Rebase rewrites history linearly; merge preserves branches.
Use rebase for clean history before push, merge for shared branches.

[Continues work - won't ask about rebase again this session]
```

**When to Use Learning Mode**:

| Use `--learn` | Use `--no-learn` |
|---------------|------------------|
| New to a technology | Expert in the domain |
| Onboarding to project | Time-critical tasks |
| Want to understand decisions | Already know the patterns |
| Mentoring yourself | High context pressure |

#### Learning Sites

| Site | Description |
|------|-------------|
| [Claudelog.com](https://claudelog.com/) | Tips, patterns, tutorials, and best practices |
| [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) | Practical productivity tips (voice workflows, context management, terminal efficiency) |
| [Official Docs](https://docs.anthropic.com/en/docs/claude-code) | Anthropic's official Claude Code documentation |

> **Tip**: These resources evolve quickly. Star repos you find useful to track updates.

**Additional topics from ykdojo worth exploring** (not yet integrated in this guide):
- **Voice transcription workflows** - Native voice input now available via `/voice` (rolling out, Pro/Max/Team/Enterprise). Hold Space to speak, release to send. Transcription is free and doesn't count against rate limits. Previously required superwhisper/MacWhisper as external workarounds.
- **Tmux for autonomous testing** - Running interactive tools in tmux sessions for automated testing
- **cc-safe security tool** - Auditing approved commands to prevent accidental deletions
- **Cascade method** - Multitasking pattern with 3-4 terminal tabs for parallel work streams
- **Container experimentation** - Using Docker with `--dangerously-skip-permissions` for safe experimental work
- **Half-clone technique** - Manual context trimming to keep recent conversation history only

### Tools

#### Audit Your Setup

Use the included audit prompt to analyze your current Claude Code configuration:

**File**: [`tools/audit-prompt.md`](../tools/audit-prompt.md)

**What it does**:
1. Scans your global (`~/.claude/`) and project (`.claude/`) configuration
2. Compares against best practices from this guide
3. Generates a prioritized report with actionable recommendations
4. Provides ready-to-use templates tailored to your tech stack

**How to use**:
1. Copy the prompt from the file
2. Run `claude` in your project directory
3. Paste the prompt and review findings
4. Choose which recommendations to implement

**Example output**:

| Priority | Element | Status | Action |
|----------|---------|--------|--------|
| 🔴 High | Project CLAUDE.md | ❌ | Create with tech stack + conventions |
| 🟡 Medium | Security hooks | ⚠️ | Add PreToolUse for secrets check |
| 🟢 Low | MCP Serena | ❌ | Configure for large codebase |

The audit covers: Memory files, folder structure, agents, hooks, MCP servers, context management, and CI/CD integration patterns.

#### Audit Your Project's Spec Completeness

Before delegating heavy coding work to an agent, check whether your project is well-specified enough to do it safely:

**File**: [`tools/spec-completeness-audit.md`](../tools/spec-completeness-audit.md)

**The problem**: agents don't fail because they lack capability — they fail because the spec is incomplete. They silently fill gaps from training priors (average public code). This audit finds the holes before you delegate.

**Framework** — 5 layers, 100 pts total:

| Layer | What it covers | Weight |
|-------|---------------|--------|
| 1. Behavioral | What the code does: features, flows | 15 pts |
| 2. Interface | Types, error contracts, invariants | 20 pts |
| 3. Architectural | What NOT to create, module boundaries, reuse constraints | 30 pts |
| 4. Lifecycle | What's deferred, known debt, maintenance intent | 20 pts |
| 5. Cultural | Conventions, naming, what "good code" means here | 15 pts |

Layer 3 weighs the most because it's the most frequently absent and produces the hardest-to-detect bugs: code that works today and drifts next month.

**Output**: per-layer score + risk tier (🟢/🟡/🔴), silent-fill prediction for each gap, delegation verdict, and 3 quick wins with templates.

**Delegation verdict**:

| Score | Tier | Posture |
|-------|------|---------|
| ≥80 | Safe | Broad delegation OK |
| 60–79 | Supervised | Delegate with explicit L3 per task |
| 40–59 | Risky | Plan-mode + review agent |
| <40 | Unsafe | Code tasks only, never architectural |

**Available as a slash command** if the `ai-methodology` plugin is installed:

```bash
/spec-completeness-audit              # current project
/spec-completeness-audit ~/other      # another project
```

---

## Appendix A: File Locations Reference

Quick reference for where Claude Code stores files and configuration.

### Windows

| Component | Location |
|-----------|----------|
| **npm global bin** | `C:\Users\<username>\AppData\Roaming\npm` |
| **Node.js install** | `C:\Program Files\nodejs` |
| **Claude data directory** | `C:\Users\<username>\.claude\` |
| **Claude config file** | `C:\Users\<username>\.claude.json` |
| **Log files** | `%APPDATA%\Claude\logs\` |
| **MCP config** | `C:\Users\<username>\.claude.json` (`mcpServers` field) |
| **Session data** | `C:\Users\<username>\.claude\local\` |
| **Downloads/cache** | `C:\Users\<username>\.claude\downloads\` |

**Quick Access (PowerShell):**
```powershell
# Open Claude data directory
explorer "$env:USERPROFILE\.claude"

# Open config file
notepad "$env:USERPROFILE\.claude.json"

# View logs
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Wait -Tail 50
```

### macOS

| Component | Location |
|-----------|----------|
| **npm global bin** | `/usr/local/bin` or `$(npm config get prefix)/bin` |
| **Node.js install** | `/usr/local/bin/node` (Homebrew) or `/opt/homebrew/bin/node` (M1/M2) |
| **Claude data directory** | `~/.claude/` |
| **Claude config file** | `~/.claude.json` |
| **Log files** | `~/Library/Logs/Claude/` |
| **MCP config** | `~/.claude.json` (`mcpServers` field) |
| **Session data** | `~/.claude/local/` |
| **Downloads/cache** | `~/.claude/downloads/` |

**Quick Access:**
```bash
# Open Claude data directory
open ~/.claude

# Edit config file
code ~/.claude.json  # VS Code
# or
nano ~/.claude.json  # Terminal editor

# View logs
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Linux

| Component | Location |
|-----------|----------|
| **npm global bin** | `/usr/local/bin` or `~/.npm-global/bin` |
| **Node.js install** | `/usr/bin/node` |
| **Claude data directory** | `~/.claude/` |
| **Claude config file** | `~/.claude.json` |
| **Log files** | `~/.local/share/claude/logs/` or `~/.cache/claude/logs/` |
| **MCP config** | `~/.claude.json` (`mcpServers` field) |
| **Session data** | `~/.claude/local/` |
| **Downloads/cache** | `~/.claude/downloads/` |

**Quick Access:**
```bash
# Open Claude data directory
cd ~/.claude

# Edit config file
nano ~/.claude.json
# or
vim ~/.claude.json

# View logs
tail -f ~/.local/share/claude/logs/mcp*.log
```

### Project-Level Files

These are the same across all platforms:

| File/Directory | Location | Purpose | Commit to Git? |
|----------------|----------|---------|----------------|
| `CLAUDE.md` | Project root | Project memory (team) | ✅ Yes |
| `.claude/CLAUDE.md` | Project root | Personal memory | ❌ No |
| `.claude/settings.json` | Project root | Hook configuration | ✅ Yes |
| `.claude/settings.local.json` | Project root | Personal permissions | ❌ No |
| `.claude/agents/` | Project root | Custom agents | ✅ Yes (team) |
| `.claude/commands/` | Project root | Custom commands | ✅ Yes (team) |
| `.claude/hooks/` | Project root | Event hooks | ✅ Yes (team) |
| `.claude/skills/` | Project root | Knowledge modules | ✅ Yes (team) |
| `.claude/rules/` | Project root | Auto-load rules | ✅ Yes (team) |
| `.claude/.serena/` | Project root | Serena MCP index | ❌ No |

### Environment Variables

Set these in your shell profile (`~/.zshrc`, `~/.bashrc`, or Windows System Properties):

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | API authentication | `sk-ant-api03-...` |
| `ANTHROPIC_BASE_URL` | Alternative API endpoint | `https://api.deepseek.com/anthropic` |
| `ANTHROPIC_MODEL` | Default model | `claude-sonnet-4-20250514` |
| `ANTHROPIC_SMALL_FAST_MODEL` | Fast model for simple tasks | `claude-haiku-4-20250514` |
| `BASH_DEFAULT_TIMEOUT_MS` | Bash command timeout | `60000` |
| `ANTHROPIC_AUTH_TOKEN` | Alternative auth token | Your auth token |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | Disable 1M context window support (v2.1.50+) | `true` |
| `CLAUDE_CODE_SIMPLE` | Fully minimal mode: disables skills, agents, MCP, hooks, CLAUDE.md loading (v2.1.50+) | `true` |

### Finding Your Paths

**Can't find npm global bin?**
```bash
# Universal command
npm config get prefix

# Should output something like:
# macOS/Linux: /usr/local or ~/.npm-global
# Windows: C:\Users\<username>\AppData\Roaming\npm
```

**Can't find Claude executable?**
```bash
# macOS/Linux
which claude

# Windows (PowerShell)
where.exe claude

# Windows (CMD)
where claude
```

**Can't find log files?**
```bash
# Run Claude with debug and check output
claude --debug 2>&1 | grep -i "log"
```

### Recommended .gitignore

Add these to your project's `.gitignore`:

```gitignore
# Claude Code - Personal/Local
.claude/settings.local.json
.claude/CLAUDE.md
.claude/.serena/
.claude/local/

# Claude Code - Team (DO commit these)
# .claude/agents/
# .claude/commands/
# .claude/hooks/
# .claude/skills/
# .claude/settings.json

# API Keys
.env
.env.local
.env.*.local
*.key

# OS Files
.DS_Store
Thumbs.db
```

---

## Appendix B: FAQ

### Claude Code vs ClawdBot: What's the Difference?

**Question**: Both tools use "Claude" in their name and I've seen buzz about both recently. Are they competitors? Which should I choose?

**Short answer**: They serve completely different use cases. Not competitors—complementary tools for different audiences.

**Detailed comparison**:

| Aspect | Claude Code | ClawdBot |
|--------|-------------|----------|
| **Interface** | Terminal/CLI + IDE integration (VS Code, Cursor, etc.) | Messaging apps (WhatsApp, Telegram, Discord, Signal, iMessage) |
| **Primary audience** | Software developers, DevOps, tech leads | Everyone (personal assistants, smart home, knowledge workers) |
| **Core use case** | Software development (code generation, refactoring, debugging, architecture) | Personal automation, task management, smart home control, 24/7 assistance |
| **Access model** | Local terminal session, requires being at computer or SSH | Remote access via messaging apps from any device (phone, watch, tablet) |
| **Installation** | `npm install -g claude-code` (simple CLI install) | Self-hosted (Docker/VPS ~$5/month + LLM API costs) |
| **Architecture** | CLI tool + MCP servers + hooks/skills/agents system | Agent + Gateway + Skills + Memory (4-component architecture) |
| **Smart home** | Not covered (development-focused) | ✅ Native Home Assistant integration, monitoring, automation |
| **Code development** | ✅ Core use case (pair programming, code review, refactoring) | Possible but not the primary focus |
| **Pricing** | Anthropic API usage (pay-as-you-go, ~$3-15/project typical) | Open-source (free) + infrastructure (VPS ~$5/mo + LLM API costs) |
| **Ideal for** | Writing code, reviewing PRs, debugging, architectural decisions | Daily reminders, email management, calendar, monitoring, personal tasks |

**When to choose Claude Code**:
- You're a developer working in terminal/IDE
- You need pair programming, code reviews, refactoring help
- Your workflow is codebase analysis and software architecture
- You want deep IDE integration and git workflow automation

**When to choose ClawdBot**:
- You want a 24/7 personal assistant accessible from your phone
- You need smart home automation (Home Assistant, IoT devices)
- Your use cases are: task management, reminders, email/calendar, monitoring
- You want messaging app interface (WhatsApp, Telegram, etc.)

**Can you use both?**:

Yes! They complement each other well:
- **ClawdBot**: Handles daily personal automation, monitoring, reminders
- **Claude Code**: Handles software development work when at your computer

Example workflow:
```
ClawdBot (on phone): "Remind me to review the PR when I'm at my desk"
  → Get notification
Claude Code (at desk): "Review the authentication PR, check for security issues"
  → Deep code analysis with full codebase context
```

**Quick decision tree**:

```
What's your primary goal?
├─ Write/review code → Claude Code
├─ Personal automation/smart home → ClawdBot
└─ Both? → Use both (they don't conflict)
```

**Resources**:
- **ClawdBot**: [https://clawd.bot/](https://clawd.bot/) | [GitHub](https://github.com/clawdbot/clawdbot) | [Setup guide](https://docs.clawd.bot/start/getting-started) | [Community adoption analysis](https://docs.google.com/document/d/1Mz4xt1yAqb2gDxjr0Vs_YOu9EeO-6JYQMSx4WWI8KUA/preview?pru=AAABnBoVzFA*FCvVY_gbqraEBXgWPRJfQw&tab=t.0)
- **Claude Code**: This guide | [GitHub](https://github.com/anthropics/claude-code)

**Community confusion**:

Common misconceptions we've seen:
- ❌ "ClawdBot is Claude Code but with messaging interface" → **False**. Different architectures, different use cases.
- ❌ "I need to choose one or the other" → **False**. They complement each other.
- ❌ "ClawdBot is a fork of Claude Code" → **False**. Independent projects with different creators.

**Final note**: This comparison reflects Jan 2026 state of both tools. ClawdBot has documented strong community adoption (5,600+ social mentions, use cases ranging from smart home to radio decoding). Both are evolving rapidly. Check official documentation for latest capabilities.

### Can Product Managers use Claude Code?

**Short answer**: Yes, but consider your primary workflow first.

**Code-adjacent PMs** (reviewing technical specs, PRDs, architecture feasibility):
- ✅ Claude Code CLI is appropriate for technical validation workflows
- Example: Granola meeting notes → ChatPRD generation → Claude Code refinement
- Use case: Auditing technical feasibility, generating specs from PRDs

**Non-coding PMs** (strategy, research, stakeholder management):
- ⚠️ Claude Code CLI overhead not justified
- ✅ Better fit: Claude Desktop (see [Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide))
- Use case: Research synthesis, stakeholder communication, roadmap planning

**Tool Stack Example** (via [Stilyan Mitrev, Head of Product StableLab](https://www.linkedin.com/pulse/how-i-currently-ai-product-manager-stilyan-mitrev-ycvvf/)):
- Meeting capture: Granola + Wispr Flow (dictation)
- PRD generation: ChatPRD → Claude Code review
- UI prototyping: v0 → Claude Code feasibility check
- Workflow pattern: Base context project + specialized projects per domain

**Reality check**: PM workflows with Claude Code are an **emerging area** with limited community validation. We currently have 1 practitioner report (the source practitioner noted they tried Claude Code but didn't adopt it long-term). If you're a PM using Claude Code successfully, [contribute your workflow](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/discussions) to help the community.

**See also**:
- [AI Ecosystem Guide](ecosystem/ai-ecosystem.md) — Complementary tools (Granola, Wispr Flow, ChatPRD, v0)
- [Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide) — Claude Desktop for non-technical PMs
- [Design-to-Code Workflow](workflows/design-to-code.md#for-product-managers) — PM perspective on Figma MCP

---

### Can I continue a session from a different project folder?

**Short answer**: Not with native \`--resume\`, but manual filesystem operations work reliably.

**The limitation**: Claude Code's \`--resume\` command is scoped to the current working directory by design. Sessions are stored at \`~/.claude/projects/<encoded-path>/\` where the path is derived from your project's absolute location. Moving a project or forking a session to a new folder breaks the resume capability.

**Why this design?**: Sessions store absolute file paths, project-specific context (MCP server configurations, \`.claudeignore\` rules, environment variables). Cross-folder resume would require path rewriting and context validation, which isn't implemented yet.

**Workaround - Manual migration** (recommended):

\`\`\`bash
# When moving a project folder
cd ~/.claude/projects/
mv -- -old-location-myapp- -new-location-myapp-

# When forking sessions to a new project
cp -n ./-source-project-/*.jsonl ./-target-project-/
cp -r ./-source-project-/subagents ./-target-project-/ 2>/dev/null || true

cd /path/to/target/project && claude --continue
\`\`\`

**⚠️ Migration risks**:
- Hardcoded secrets/credentials may not transfer correctly
- Absolute paths in session context may break
- MCP server configurations may differ between projects
- \`.claudeignore\` rules are project-specific

**Community automation**: The [claude-migrate-session](https://github.com/jimweller/dotfiles/tree/main/dotfiles/claude-code/skills/claude-migrate-session) skill by Jim Weller automates this process, but has limited testing (0 stars/forks as of Feb 2026). Manual approach is safer.

**Detailed guide**: See [Session Resume Limitations & Cross-Folder Migration](ops/observability.md#session-resume-limitations--cross-folder-migration) for complete workflow and edge cases.

**Related**: GitHub issue [#1516](https://github.com/anthropics/claude-code/issues/1516) tracks community requests for native cross-folder support.

---

## Appendix C: Resource Evaluation Process

This guide systematically evaluates external resources (tools, methodologies, articles, frameworks) before integration to maintain quality and prevent noise.

### Evaluation Methodology

**5-Point Scoring System** (Critical → Low):

| Score | Action | Timeline |
|-------|--------|----------|
| 5 | Critical - Integrate immediately | <24h |
| 4 | High Value - Integrate within 1 week | 1 week |
| 3 | Moderate - Integrate when time available | Flexible |
| 2 | Marginal - Minimal mention or skip | - |
| 1 | Low - Reject | - |

**Full methodology**: See [`docs/resource-evaluations/README.md`](../docs/resource-evaluations/README.md)

### Current Evaluations

**14 documented assessments** in `docs/resource-evaluations/`:

- **Methodologies**: GSD (Get Shit Done), Vibe Coding patterns
- **Tools**: Worktrunk, AST-grep, SE-CoVe plugin
- **Content**: Boris Cherny Cowork video, ClawdBot Twitter analysis
- **Research**: Prompt repetition papers, self-improvement skills
- **And more**: Nick Jensen plugins, Wooldridge productivity stack

**Browse all evaluations**: [`docs/resource-evaluations/`](../docs/resource-evaluations/)

### Why Public Evaluations?

**Transparency**: Contributors can see exactly why resources were:
- ✅ **Integrated** (score 3+): Added to guide with attribution
- ⚠️ **Mentioned** (score 2): Brief reference without deep coverage
- ❌ **Rejected** (score 1): Documented reason for exclusion

**Quality Control**: Technical review + challenge phase by specialized agents ensures objectivity and prevents marketing hype from influencing decisions.

**Community Contribution**: Evaluation template available in `docs/resource-evaluations/README.md` for suggesting new resources with systematic assessment.

---

## Appendix D: Myths vs Reality

This section addresses common misconceptions about Claude Code circulating in online communities, social media, and discussions.

### ❌ Myth: "Claude Code has hidden features you can unlock with secret flags"

**Reality**: All public features are documented in the [official CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).

**What people confuse**:
- **Progressive rollout ≠ Hidden features**: Anthropic uses feature flags for staged deployment (standard industry practice)
- **Experimental features ≠ Secrets**: Features like TeammateTool exist but are clearly marked as experimental/unstable
- **Community discovery ≠ Hacking**: When users discover unreleased features in compiled code, that's exploration, not "unlocking secrets"

**The truth about feature flags**:

| Flag | Purpose | Status |
|------|---------|--------|
| `CLAUDE_CODE_ENABLE_TASKS=false` | **Revert** to old TodoWrite system (v2.1.19+) | Official migration path |
| TeammateTool flags | Progressive deployment of multi-agent orchestration | Experimental, unstable |
| Other internal flags | Quality assurance, A/B testing, staged rollout | Not meant for end users |

**Best practice**: Read the [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) and official release notes. Features become public when they're stable and documented. Using experimental features via workarounds can cause:
- Data loss or corruption
- Crashes and instability
- Incompatibility with future versions
- Loss of official support

**Red flags to watch for** (signs of misinformation):
- "Hidden feature that will blow your mind!"
- "Secret trick the devs don't want you to know"
- No citation of official sources (CHANGELOG, docs, GitHub issues)
- FOMO language: "If you're not using this, you're falling behind"
- Dramatic claims: "This changes everything" without evidence

---

### ❌ Myth: "Tasks API allows fully autonomous parallel agents"

**Reality**: The Tasks API (v2.1.16+) enables **coordination** of parallel work, but agents are **not autonomous**.

**What Tasks API actually does**:
- Creates a shared task list with dependency tracking
- Allows main session + sub-agents to coordinate work
- Persists tasks across sessions for resumption
- Notifies sessions when tasks complete

**What it does NOT do**:
- ❌ Automatically spawn agents for each task
- ❌ Create self-organizing "swarms" of independent agents
- ❌ Enable agents to make decisions without human approval
- ❌ Replace your need to manage and direct the work

**How parallel execution actually works**:

```
You → Create tasks with TaskCreate
You → Spawn sub-agents with Task tool (explicit action)
You → Sub-agents work independently in parallel
You → Sub-agents return summaries
You → Coordinate next steps
```

**Sources**:
- [CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2116---2026-01-22) - Official task management release
- [Section 2.6 - Task Management](ultimate-guide.md#26-task-management) - Full documentation

---

### ❌ Myth: "Claude Code is 100x faster than other AI coding tools"

**Reality**: Performance depends on task complexity, model choice, and how you use the tool. No tool is universally "100x faster."

**What affects speed**:
- **Model selection**: Haiku (fast) vs Sonnet (balanced) vs Opus (thorough)
- **Context management**: Effective use of sub-agents, MCP servers, strategic compaction
- **Prompt quality**: Clear requirements vs vague instructions
- **Task complexity**: Simple refactoring vs architectural analysis

**Honest comparison** (typical use cases):

| Task | Claude Code | Other Tools | Winner |
|------|-------------|-------------|--------|
| Simple edits (typos, formatting) | ~5-10s | ~5-10s | ≈ Tie |
| Multi-file refactoring | 30-60s | 60-120s | Claude Code (2x) |
| Complex architecture analysis | 2-5min | 5-15min | Claude Code (3x) |
| Learning curve (first week) | Moderate | Varies | Depends on tool |

**The truth**: Claude Code is **powerful and efficient**, but claims of "100x faster" are marketing hyperbole. Real advantage comes from:
- Deep context window (200K tokens)
- Smart sub-agent system (prevents context pollution)
- MCP ecosystem (specialized tools)
- Strong system prompts (high-quality outputs)

---

### ✅ Reality: What Makes Claude Code Actually Special

**Documented, verifiable strengths**:

1. **Context Window**: 200K tokens (~150K words) - one of the largest in the industry
2. **Sub-Agent System**: Isolated context windows prevent pollution during exploration
3. **MCP Ecosystem**: 100+ community servers for specialized tasks
4. **Permission System**: Granular control over tool access and dangerous operations
5. **CLI-First Design**: Terminal integration, git workflows, IDE compatibility
6. **Transparent Pricing**: Pay-as-you-go, no subscriptions, predictable costs
7. **Active Development**: Weekly releases with community-driven features

**Sources**: All claims verifiable in [official documentation](https://code.claude.com/docs) and [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).

---

### How to Spot Reliable Information

✅ **Trust these sources**:
- Official [Claude Code documentation](https://code.claude.com/docs)
- [GitHub CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [GitHub Issues](https://github.com/anthropics/claude-code/issues) with Anthropic staff responses
- Community resources citing official sources (like [Claudelog.com](https://claudelog.com/))
- This guide (with 14 evaluated resources and clear sourcing)

❌ **Be skeptical of**:
- Social media posts with no sources
- "Secret tricks" without CHANGELOG references
- Percentage claims without benchmarks ("50% faster", "10x productivity")
- Dramatic language designed to create FOMO
- Content that discourages reading official docs

---

### Contributing to This Section

Found a new myth circulating online? [Open an issue](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/issues) with:
- The myth/misconception
- Where you saw it (platform, approximate reach)
- Why it's misleading (with sources)

We'll evaluate and add it to this section if it meets quality criteria.

---

## About This Guide

**End of Guide**

---

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Written with**: Claude (Anthropic) - This guide was collaboratively written with Claude Code, demonstrating the tool's capabilities for technical documentation.

**Inspired by**:
- [Claudelog.com](https://claudelog.com/) - An excellent resource for Claude Code tips, patterns, and advanced techniques that served as a major reference for this guide.
- [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) - Practical productivity techniques that informed keyboard shortcuts, context handoffs, and terminal workflow optimizations in sections 1.3, 2.2, and 10.2.
- [Nick Tune's Coding Agent Development Workflows](https://medium.com/nick-tune-tech-strategy-blog/coding-agent-development-workflows-af52e6f912aa) - Advanced workflow patterns integrated in sections 3.1, 7.1, 9.3, and 9.10.

**License**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) - Feel free to use, adapt, and share with attribution.

**Contributions**: Issues and PRs welcome.

**Last updated**: January 2026 | **Version**: 3.40.0

