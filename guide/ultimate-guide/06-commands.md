# 6. Commands (User-Invocable Skills)

_Quick jump:_ [Slash Commands](#61-slash-commands) · [Creating Custom Commands](#62-creating-custom-commands) · [Command Template](#63-command-template) · [Command Examples](#64-command-examples)

---

> **CC 2.1.3 (January 2026)**: Skills and Commands are now unified. `.claude/commands/` is merged into `.claude/skills/`. Skills have two invocation modes: user-triggered (`/skill-name`, equivalent to old commands) and model-triggered (auto-loaded by description match). To restrict a skill to user-invocation only, add `disable-model-invocation: true` to its frontmatter. Existing files in `.claude/commands/` remain backward-compatible but all new development belongs in `.claude/skills/`.

---

**Reading time**: 10 minutes
**Skill level**: Week 1-2
**Goal**: Create custom slash commands

## 6.1 Slash Commands

Slash commands are user-invocable skills. Since CC 2.1.3, they live in `.claude/skills/` (not `.claude/commands/`). The `/name` invocation syntax is unchanged. Add `disable-model-invocation: true` to a skill's frontmatter to make it user-only.

### Built-in Commands

| Command | Action |
|---------|--------|
| `/help` | Show all commands |
| `/clear` | Clear conversation |
| `/compact` | Summarize context |
| `/status` | Show session info |
| `/context` | Detailed context/token breakdown with actionable suggestions |
| `/cost` | Per-model token cost breakdown for the session *(use `/usage` since v2.1.118)* |
| `/plan` | Enter Plan Mode |
| `/rewind` | Undo changes |
| `/undo` | Alias for /rewind |
| `/resume` | Resume a previous session with interactive picker |
| `/voice` | Toggle voice input (hold Space to speak, release to send) |
| `/recap` | Show context summary when returning to a session after a break |
| `/config` | Interactive configuration editor |
| `/model` | Switch model (sonnet/opus/opusplan) |
| `/effort [level]` | Set thinking depth: low/medium/high/xhigh/max; no arg = interactive slider |
| `/focus` | Toggle focus view (minimal UI, hides metadata) |
| `/tui [fullscreen]` | Switch to full-screen flicker-free TUI rendering |
| `/copy` | Interactive picker: copy a code block or full response |
| `/loop [interval] [prompt]` | Run a prompt on a recurring interval |
| `/proactive` | Alias for /loop |
| `/simplify` | Review changed code and fix over-engineering |
| `/batch` | Large-scale changes via parallel worktree agents |
| `/insights` | Generate usage analytics report |
| `/btw [question]` | Side question via ephemeral overlay: read-only, no tools, single response, doesn't pollute main history |
| `/doctor` | Diagnostic check: environment, settings, connectivity |
| `/release-notes` | Browse Claude Code changelog interactively |
| `/less-permission-prompts` | Scan transcripts and propose a read-only tool allowlist |
| `/team-onboarding` | Generate a teammate ramp-up guide from CLAUDE.md and recent sessions |
| `/terminal-setup` | Configure terminal scroll sensitivity (VS Code, Cursor, Windsurf) |
| `/reload-plugins` | Reload MCP plugins and auto-install missing dependencies |
| `/mcp` | Show MCP server status |
| `/memory` | View/edit memory files |
| `/plugin` | Manage plugins (install, list, update) |
| `/keybindings` | Edit key bindings (opens ~/.claude/keybindings.json) |
| `/setup-bedrock` | Interactive Bedrock configuration wizard |
| `/setup-vertex` | Interactive Vertex AI configuration wizard |
| `/ultrareview` | Cloud-based parallel multi-agent code review (Pro/Max) |
| `/goal [condition]` | Set a completion condition. Claude works autonomously across turns until the condition is met, displaying a live overlay with elapsed time, turn count, and token usage. Example: `/goal all tests pass and build is green` (v2.1.139) |
| `/scroll-speed` | Interactive slider to tune mouse wheel scroll speed. Changes take effect immediately with live preview. (v2.1.139) |
| `/exit` | Exit Claude Code |

### The /btw Command

`/btw` lets you ask a quick side question while Claude is working without breaking your flow. Type `/btw what does this function return?` and get an instant response in an overlay — the main task keeps running uninterrupted.

**How it works**: Claude spawns a temporary ephemeral agent with NO tools available. It cannot read files, run commands, or take actions. It responds once based solely on the current conversation context, then the overlay closes. The exchange never enters your main conversation history.

**Key constraints:**
- Read-only — no file access, no shell commands
- Single response — no follow-up in the overlay
- Context-only — answers from what's already in the conversation, not from disk
- "Full context aware" means conversation context, not project files

**When to use it:**
- Quick clarification mid-task ("btw what's the default port for Postgres?")
- Terminology check without stopping work
- Sanity check on something Claude just mentioned

**Syntax**: Start your message with `btw` (lowercase, no slash required) followed by your question. Claude Code detects the `btw` prefix and routes it to the ephemeral overlay agent.

> Note: This feature (`btw-side-question`) was introduced around v2.0.73 and matured by v2.1.23. If you encounter issues, verify you're on a recent version.

### Session Forking

Session forking creates a new independent session that starts from an existing point in history. Use it when you hit a decision point and want to explore two directions without restarting from scratch.

**Two ways to fork:**

```bash
# From inside an active session
/branch

# From the CLI when resuming
claude --resume <session-id> --fork-session
```

`/branch` was added in v2.1.77, replacing `/fork` (still works as an alias).

**When to fork instead of restart:**
- You're at a working state and want to explore a risky refactor without losing it
- You want to try two different approaches to the same problem in parallel
- You found a good mid-session checkpoint and want to branch off for a hypothesis test

**After forking**: both branches are independent — changes in one don't affect the other. Resume either later with `claude --resume` and the interactive session picker.

**Tip**: run `/rename` before forking so you can tell the two branches apart in the picker.

### /recap: Session Context on Return

`/recap` provides a context summary when you come back to a session after a break. Claude automatically detects the absence and generates a brief recap of what was being worked on, the last actions taken, and what comes next. This makes returning to a long session significantly less disorienting, especially after an overnight gap or a context compaction.

**Behavior**: The recap fires automatically on re-entry to a session. It does not trigger at the end of a session; the trigger is when you *return* to one that has been inactive.

**Configuration options:**

| Method | Effect |
|--------|--------|
| `/config` then search "recap" | Enable/disable the feature in the UI |
| `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=1` | Force-enable (useful if telemetry is disabled) |
| `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` | Disable completely |

The feature works even with telemetry disabled (Bedrock, Vertex, Foundry, `DISABLE_TELEMETRY`). You can also toggle it from `/config` without touching environment variables.

**Version history**: Introduced in v2.1.108. Extended to telemetry-disabled environments in v2.1.110. A regression that caused auto-firing while the user was still composing a message was fixed in v2.1.113.

### The /insights Command

`/insights` analyzes your Claude Code usage history to generate a comprehensive report identifying patterns, friction points, and optimization opportunities.

#### What It Analyzes

The command processes your session data to detect:

- **Project areas**: Automatically clusters your work into thematic areas (e.g., "Frontend Development", "CLI Tooling", "Documentation") with session counts
- **Interaction style**: Identifies your workflow patterns (plan-driven, exploratory, iterative, supervisory)
- **Success patterns**: Highlights what's working well in your usage (multi-file coordination, debugging approaches, tool selection)
- **Friction categories**: Pinpoints recurring issues (buggy code, wrong directories, context loss, misunderstood requests)
- **Tool usage**: Tracks which tools you use most (Bash, Read, Edit, Grep, etc.) and identifies optimization opportunities
- **Multi-clauding behavior**: Detects parallel session patterns (running multiple Claude instances simultaneously)
- **Temporal patterns**: Identifies your most productive time windows and response time distribution

#### What It Produces

Running `/insights` generates an interactive HTML report at `~/.claude/usage-data/report.html` containing:

**At a Glance Summary**:
- What's working: 2-3 sentences on successful patterns
- What's hindering: 2-3 sentences on main friction points
- Quick wins: 1-2 actionable suggestions (setup time < 5 minutes)
- Ambitious workflows: 1-2 advanced patterns for future exploration

**Detailed Sections**:
1. **What You Work On**: 3-5 auto-detected project areas with descriptions
2. **How You Use Claude Code**: Narrative analysis (2-3 paragraphs) of your interaction style + key pattern summary
3. **Impressive Things You Did**: 3 "big wins" — sophisticated workflows the system detected (e.g., multi-agent reviews, custom automation layers)
4. **Where Things Go Wrong**: 3 friction categories with examples and mitigation strategies
5. **Existing CC Features to Try**:
   - 6+ CLAUDE.md additions (pre-formatted, ready to copy)
   - 3 features with setup code (Custom Skills, Hooks, Task Agents)
6. **New Ways to Use Claude Code**: 3 usage patterns with copyable prompts
7. **On the Horizon**: 3 ambitious workflows with detailed implementation prompts (300+ tokens each)
8. **Fun Ending**: An anecdote from your sessions (e.g., a memorable user intervention or pattern)

**Interactive Elements**:
- Copy buttons for all code snippets and prompts
- Checkboxes for CLAUDE.md additions (bulk copy)
- Charts and visualizations (tool usage, friction types, outcomes, time-of-day distribution)
- Navigation TOC with anchor links
- Responsive design (works on mobile)

#### How to Use It

**Basic usage**:
```bash
/insights
```

The command runs silently (no progress output) and takes ~10-30 seconds depending on session count. You'll see:
```
1281 sessions · 10,442 messages · 3445h · 1160 commits
2025-12-15 to 2026-02-06

## At a Glance
[4 summary sections...]

Report URL: file:///Users/you/.claude/usage-data/report.html
```

**Open the report**:
- CLI: `open ~/.claude/usage-data/report.html` (macOS) or `xdg-open ~/.claude/usage-data/report.html` (Linux)
- The report is self-contained HTML (no external dependencies)

**When to run it**:
- **After major projects**: Identify what worked and what to improve for next time
- **Monthly**: Track evolution of your workflow patterns
- **When feeling stuck**: Get data-driven suggestions for friction points
- **Before optimizing CLAUDE.md**: See which patterns to codify
- **When context feels broken**: Check if detected patterns explain frustration

#### Typical Insights Generated

The report may identify patterns like:

**Friction categories**:
- "Buggy Code Requiring Multiple Fix Rounds" (22 instances) → Suggests build-check-fix loops after each edit
- "Wrong Directory Before Starting Work" (12 instances) → Recommends explicit working directory confirmation in CLAUDE.md
- "Insufficient Real-World Testing" → Proposes manual testing protocols beyond automated checks
- "Context Loss" → Flags sessions where conversation became disconnected from original goal

**Success patterns**:
- "Plan-Driven Execution at Scale" → Detects users who provide numbered plans and achieve 80%+ completion rates
- "Multi-Agent Review and Challenge Loops" → Identifies sophisticated users who spawn sub-agents for adversarial review
- "Custom Slash Commands for Recurring Workflows" → Highlights automation layer patterns

**CLAUDE.md suggestions** (example):
```markdown
## Project Directories
Always confirm the correct working directory before starting work:
- Frontend: /path/to/web-app
- Backend: /path/to/api
- Docs: /path/to/documentation
Never assume which project to work in — ask if ambiguous.
```

**Feature recommendations** (example):
- "Your #1 friction is buggy code (22 occurrences). A pre-commit hook running build checks would catch these before they compound."
- "You run 73% of messages in parallel sessions (multi-clauding). Consider a session coordination protocol in CLAUDE.md."

**Horizon workflows** (example):
```markdown
Self-Healing Builds With Test-Driven Agents

Implement the following plan step by step. After EVERY file edit,
run the full build command. If the build fails, immediately diagnose
the error, fix it, and rebuild before moving to the next step.
Never proceed with a broken build.

[300-token detailed prompt follows...]
```

#### Technical Details

- **Analysis engine**: Uses Claude Haiku (fast, cost-effective)
- **Session limit**: Analyzes up to 50 recent sessions per run
- **Token budget**: Max 8192 tokens per analysis pass
- **Data location**: `~/.claude/usage-data/` (sessions stored as JSONL)
- **Privacy**: All analysis runs locally; no data sent to external services beyond standard Claude Code API usage

#### How /insights Works (Architecture Overview)

The analysis pipeline processes session data through 7 stages:

1. **Session Filtering**: Loads from `~/.claude/projects/`, excludes agent sub-sessions, sessions with <2 user messages, or <1 minute duration
2. **Transcript Summarization**: Chunks sessions exceeding 30,000 characters into 25,000-character segments
3. **Facet Extraction**: Uses Claude Haiku to classify sessions into structured categories
4. **Aggregated Analysis**: Detects cross-session patterns and recurring workflows
5. **Executive Summary**: Generates "At a Glance" synthesis across four dimensions
6. **Report Generation**: Renders interactive HTML with visualizations and narrative sections
7. **Facet Caching**: Saves classifications to `~/.claude/usage-data/facets/<session-id>.json` for fast subsequent runs

**Facets Classification System**:

The system categorizes sessions using these dimensions:

**Goals (13 types)**:
Debug/Investigate, Implement Feature, Fix Bug, Write Script/Tool, Refactor Code, Configure System, Create PR/Commit, Analyze Data, Understand Codebase, Write Tests, Write Docs, Deploy/Infra, Cache Warmup

**Friction Types (12 categories)**:
Misunderstood requests, Wrong approach, Buggy code, User rejected actions, Claude blocked, Early user stoppage, Wrong file locations, Over-engineering, Slowness/verbosity, Tool failures, Unclear requests, External issues

**Satisfaction Levels (6)**:
Frustrated → Dissatisfied → Likely Satisfied → Satisfied → Happy → Unsure

**Outcomes (4 states)**:
Not Achieved → Partially Achieved → Mostly Achieved → Fully Achieved

**Success Categories (7)**:
Fast accurate search, Correct code edits, Good explanations, Proactive help, Multi-file changes, Good debugging, None

**Session Types (5)**:
Single task, Multi-task, Iterative refinement, Exploration, Quick question

Understanding these categories helps interpret your report:
- High "Buggy code" friction → Consider implementing pre-commit hooks (see Hooks feature)
- Low satisfaction on "Implement Feature" goals → Improve planning phase specificity
- "Early user stoppage" pattern → May indicate requests lack sufficient context

**Performance optimization**: The caching system ensures subsequent runs only analyze new sessions (not previously classified ones), making regular monthly runs fast even with large session histories.

> **Source**: Architecture details from [Zolkos Technical Deep Dive](https://www.zolkos.com/2026/02/04/deep-dive-how-claude-codes-insights-command-works.html) (2026-02-04)

#### Limitations

- **Requires history**: Needs at least ~10 sessions for meaningful patterns
- **Recency bias**: Focuses on last 50 sessions (older patterns not detected)
- **Model-estimated satisfaction**: Satisfaction scores are inferred, not explicit user ratings
- **No cross-project aggregation**: Each project analyzed independently (no global patterns across multiple repos)

#### Integration with Other Tools

**Feed insights into CLAUDE.md**:
```bash
# 1. Generate report
/insights

# 2. Open report in browser
open ~/.claude/usage-data/report.html

# 3. Copy CLAUDE.md additions (use checkboxes + "Copy All Checked")
# 4. Paste into Claude Code:
"Add these CLAUDE.md sections: [paste copied text]"
```

**Track evolution over time**:
```bash
# Save timestamped reports
cp ~/.claude/usage-data/report.html ~/insights-reports/$(date +%Y-%m-%d).html

# Compare monthly
diff ~/insights-reports/2026-01-01.html ~/insights-reports/2026-02-01.html
```

**Combine with other analytics**:
- Use with `ccboard` skill for deeper dive into session economics
- Cross-reference with git history: `git log --since="2025-12-15" --until="2026-02-06" --oneline | wc -l`
- Compare detected friction with actual bug reports

#### Example Workflow

**Monthly optimization routine**:
```bash
# 1. Generate current insights
/insights

# 2. Review "What's hindering you" section
# Note: Common friction → buggy code (48% of events)

# 3. Implement quick win (PostToolUse hook for build checks)
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run build 2>&1 | tail -20"
          }
        ]
      }
    ]
  }
}
EOF

# 4. Update CLAUDE.md with detected patterns
# (Copy from "Suggested CLAUDE.md Additions" section)

# 5. Re-run next month to measure improvement
```

#### Comparison with Other Analytics

| Tool | Scope | Output | Use Case |
|------|-------|--------|----------|
| `/insights` | Session behavior, friction, patterns | Interactive HTML report | Workflow optimization, self-improvement |
| `/status` | Current session only | Text summary (context, costs, tools) | Real-time monitoring |
| `ccboard` | Economics, cost analysis, project breakdown | TUI/Web dashboard | Budget tracking, cost optimization |
| Git history | Code changes only | Commit log | Delivery metrics, PR velocity |

> **Tip**: Run `/insights` monthly, `/status` per session, and `ccboard` weekly for comprehensive visibility.

### The /simplify Command

Added in v2.1.63, `/simplify` is a bundled slash command that reviews your recently changed code for over-engineering and redundant abstractions, then fixes the problems it finds.

#### When to Use It

Run it after finishing a feature, before opening a pull request:

```bash
# Review everything changed since last commit
/simplify

# Focus on a specific concern
/simplify focus on error handling
/simplify check for unnecessary dependencies
/simplify look at the database query patterns
```

#### What It Does

`/simplify` analyzes changed code for:
- **Reuse** — duplicated logic that could be extracted
- **Quality** — patterns that reduce readability or maintainability
- **Efficiency** — algorithmic and structural improvements

It operates at the architecture and structure level, not at the formatter or linter level. `/simplify` complements tools like ESLint or Prettier rather than replacing them.

#### Positioning

| Tool | Level | Fixes |
|------|-------|-------|
| Prettier | Formatting | Style, whitespace |
| ESLint | Syntax rules | Simple patterns, unused vars |
| `/simplify` | Architecture | Over-abstraction, duplication, design |

> **Note**: `/simplify` is a bundled slash command (ships with Claude Code), not a custom skill you need to create. Available from v2.1.63+.

### The /batch Command

Added in v2.1.63, `/batch` orchestrates large-scale codebase changes by distributing work across 5–30 parallel agents in isolated git worktrees, each opening its own pull request.

#### How It Works

1. **Research & plan** — analyzes the codebase and breaks the change into independent units
2. **Parallel execution** — spawns 5–30 isolated git worktree agents simultaneously
3. **PR per agent** — each agent completes its portion and opens a pull request

#### Usage

```bash
/batch migrate from react to vue
/batch replace all uses of lodash with native equivalents
/batch add type annotations to all JavaScript files
```

#### When to Use It

`/batch` is the native equivalent of the parallel worktrees multi-agent pattern (see §15). Use it for large, repetitive, file-level changes that can be split into independent units: migrations, refactors, bulk type annotations, dependency replacements.

> **Note**: Both `/simplify` and `/batch` are bundled slash commands that ship with Claude Code v2.1.63+. No configuration required.

### Scheduled Tasks: Three Methods

Claude Code provides three distinct mechanisms for running recurring tasks. They differ on where the execution happens, how the task is triggered, and whether a local machine needs to be on.

#### Comparison Table

| | Routines | Desktop Tasks | `/loop` |
|--|--|--|--|
| Runs on | Anthropic cloud | Local machine | Local machine |
| Machine must be on | No | Yes | Yes |
| Session must be open | No | No | Yes |
| Persists between restarts | Yes | Yes | No |
| Local file access | No (fresh repo clone) | Yes | Yes |
| Trigger types | Schedule / API / GitHub events | Schedule only | In-session only |
| MCP servers | Configured connectors per task | Config files + connectors | Inherited from session |
| Permission prompts | None (autonomous) | Configurable | Inherited from session |
| Minimum interval | 1 hour (schedule trigger) | 1 minute | 1 minute |
| Daily run limit | 5–25/day (plan-based) | Unlimited | Session-scoped |

#### Routines (Cloud Automation)

Routines run on Anthropic's infrastructure — your machine can be completely off. Each run clones a fresh copy of your GitHub repository. Three trigger types can be combined on a single routine.

> **Research preview**: behavior, limits, and API surface may change.

**Access**: Pro, Max, Team, and Enterprise plans.

**Daily run limits**:

| Plan | Runs/day |
|------|----------|
| Pro | 5 |
| Max | 15 |
| Team / Enterprise | 25 |

Extra runs are available with billing enabled beyond the daily cap.

**Create a routine** via:
- `claude.ai/code/routines` — web interface
- Desktop app — **New task** → **New remote task**
- `/schedule` in the CLI (schedule trigger only; API and GitHub triggers require the web UI)

**How each run works**: Anthropic clones your repo, spins up a Claude session with the configured environment and MCP connectors, executes the task, then pushes any commits to a branch prefixed `claude/` by default.

**Key constraints**:
- No local file access (only files tracked in the GitHub repo)
- Minimum interval is 1 hour for the schedule trigger
- Supports MCP connectors: Slack, Linear, Google Drive, and others configured per routine
- Runs appear as full sessions you can inspect, continue, or PR from

##### Schedule Trigger

Runs on a recurring cron cadence. Four presets (hourly / daily / weekdays / weekly), plus custom expressions set via `/schedule update` in the CLI.

```bash
/schedule "every Monday at 9am, open a PR summarizing last week's merged PRs"
/schedule "every night at 2am, pull the top bug from Linear and open a draft fix PR"
/schedule "every Friday, scan merged PRs for docs drift and open update PRs"
```

##### API Trigger

Each routine gets a dedicated HTTP endpoint. POST to it from any external system — alerting tools, deploy pipelines, CI scripts — and Claude opens a new autonomous session.

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01.../fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

The optional `text` field passes run-specific context (alert body, deploy ID, log snippet) to the routine's prompt. The response returns a `session_url` to observe the run live.

**Setup**: add an API trigger from the routine's edit page in the web UI, click **Generate token** (shown once — store it immediately), copy the endpoint URL. Tokens are per-routine and can be rotated or revoked from the same panel.

**Use cases**: Datadog alert fires → Claude correlates trace with recent commits, opens draft fix PR; CD pipeline calls endpoint after deploy → smoke checks + go/no-go to Slack channel.

##### GitHub Event Trigger

Fires a new session automatically on matching GitHub repository events. Requires installing the Claude GitHub App on the target repo (separate from `/web-setup`).

**17 supported event types**: pull request, push, issues, releases, check run, check suite, workflow run, workflow job, workflow dispatch, repository dispatch, pull request review, PR review comment, issue comment, discussion, discussion comment, commit comment, merge queue entry.

**PR filters**: narrow by author, title, body, base/head branch, labels, draft state, merge state, or fork origin. All conditions must match.

```
# Example filter combinations
PR opened from a fork                       → security review routine
PR labeled "needs-backport", is merged      → backport-to-next routine
Any merged PR changing /sdk/python/         → auto-port to Go SDK routine
PR opened, is not draft                     → team review checklist routine
```

**Important**: each matching event opens its own independent session. Two PRs opened = two sessions. There is no session reuse across events.

**Official docs**: `https://code.claude.com/docs/en/routines`

##### Finding Use Cases for Your Project

A good Routine candidate has three properties: it runs the same logic every time (or reacts to a well-defined event), the output is concrete (PR opened, message posted, file updated), and no human needs to be in the loop during execution.

Five angles to audit any project:

| Angle | Questions to ask |
|-------|-----------------|
| Scheduled maintenance | What do you do manually on a schedule and sometimes forget? Dependency audits, stale PR triage, coverage drift, dead code reports |
| Event-driven reactions | What should happen on every PR open or merge but doesn't because nobody gets to it? Review checklists, changelog updates, cross-repo sync |
| Alert response | When monitoring fires, what's the first thing a dev does? Could that step run automatically before the human looks? |
| Cross-system sync | What drifts because the sync is manual? Two SDKs, a doc site and an API, GitHub issues and Linear |
| Release automation | What do you run by hand before or after a deploy? Smoke tests, release notes, stakeholder notifications |

Use the `/routines-discover` command to run this analysis against any codebase — it reads the repo, identifies concrete candidates across the five angles, and ranks them by value-to-effort ratio.

```bash
/routines-discover
```

Template: `examples/commands/routines-discover.md`

#### Desktop Scheduled Tasks

Desktop tasks run on your local machine via the Claude Code Desktop app. Your machine must be on, but you do not need an active terminal session.

Unlike Cloud tasks, Desktop tasks have full access to local files and your existing MCP configuration. The minimum interval is 1 minute.

**Create a task**: open the Desktop app, go to the **Schedule** page, click **New task**. You can also create a remote (cloud) task from the same page by selecting **New remote task**.

**How each run works**: A fresh Claude instance starts, reads your project files, executes the task prompt, and shuts down. Missed runs (machine was off) are queued and executed when the app reopens.

**Official docs**: `https://code.claude.com/docs/en/desktop-scheduled-tasks`

#### DIY: System Cron + `claude --print`

For full control without the Desktop app, wire up the system cron directly with Claude's headless flag:

```bash
# crontab -e
0 8 * * 1-5 bash -c 'source /home/user/.env && cd /your/repo && claude --print "summarize git changes since yesterday" >> /var/log/claude-daily.log 2>&1'
```

This approach runs entirely offline without any Anthropic infrastructure and has no minimum interval. Three things to get right: use the full path to `claude` (check with `which claude`), load your `ANTHROPIC_API_KEY` from a file rather than hardcoding it, and redirect both stdout and stderr to a log file so you have a record of each run.

#### The /loop Command

`/loop [interval] [prompt]` runs a prompt or slash command on a recurring interval within your current session. It stops when you press `Ctrl+C` or send any new message.

```bash
/loop 5m check the deploy
/loop 30m /slack-feedback
/loop 1h /pr-pruner
```

**How it works**: Claude executes the prompt, waits for the interval, executes again, repeat. Each execution is timestamped in the transcript. You can reference a slash command (like `/loop 30m /review-pr`) or write a free-form prompt directly.

**Use cases from Boris Cherny (Claude Code creator):**

| Loop | What it does |
|------|-------------|
| `/loop 5m /babysit` | Auto-handle code review, rebase, push PRs forward |
| `/loop 30m /slack-feedback` | Post PRs for team feedback every 30 min |
| `/loop 1h /pr-pruner` | Clean up stale PRs on a schedule |

**Constraints**: Session-scoped only. Max 3 days runtime, minimum 1 minute interval, maximum 50 tasks per session.

> `/loop` added in v2.1.71. Timestamp markers in loop transcripts added in v2.1.86. Cloud and Desktop Scheduled Tasks launched March 9, 2026. Source: [code.claude.com/docs/en/whats-new](https://code.claude.com/docs/en/whats-new)

### User-Invocable Skills (formerly "Custom Commands")

Since CC 2.1.3, user-invocable skills live in `.claude/skills/`:

```
/tech:commit    → .claude/skills/tech/commit/SKILL.md
/tech:pr        → .claude/skills/tech/pr/SKILL.md
/product:scope  → .claude/skills/product/scope/SKILL.md
```

Add `disable-model-invocation: true` to the frontmatter to prevent the model from auto-loading the skill when not explicitly invoked.

## 6.2 Creating Custom Commands

Commands are markdown files that define a process.

### Command File Location

```
.claude/skills/
├── tech/           # Development workflows
│   ├── commit/SKILL.md
│   └── pr/SKILL.md
├── product/        # Product workflows
│   └── problem-framer/SKILL.md
└── support/        # Support workflows
    └── ticket-analyzer/SKILL.md
```

### Command Naming

| File | Invocation |
|------|------------|
| `commit.md` in `tech/` | `/tech:commit` |
| `pr.md` in `tech/` | `/tech:pr` |
| `problem-framer.md` in `product/` | `/product:problem-framer` |

### Variable Interpolation

Commands can accept arguments:

```markdown
# My Command

You received the following arguments: $ARGUMENTS[0] $ARGUMENTS[1] $ARGUMENTS[2]
(Or use shorthand: $0 $1 $2)

Process them accordingly.
```

Usage:
```
/tech:deploy production
```

`$ARGUMENTS[0]` (or `$0`) becomes `production`.

> **⚠️ Breaking Change (v2.1.19)**: The argument syntax changed from dot notation (`$ARGUMENTS.0`) to bracket syntax (`$ARGUMENTS[0]`). If you have existing custom commands using the old syntax, update them:
> ```bash
> # Old (< v2.1.19):
> $ARGUMENTS.0 $ARGUMENTS.1
>
> # New (v2.1.19+):
> $ARGUMENTS[0] $ARGUMENTS[1]
> # Or use shorthand:
> $0 $1
> ```

**Pair `$ARGUMENTS` with `argument-hint`** so users see available options in the command picker. The hint appears as placeholder text when typing the command:

```yaml
---
description: Deploy to a target environment
argument-hint: "<env> [--skip-tests] [--dry-run]"
---
Deploy to $ARGUMENTS[0] environment.
```

When the user types `/deploy`, the menu shows: `/deploy <env> [--skip-tests] [--dry-run]`

## 6.3 Command Template

```markdown
---
description: Brief description of what this command does
argument-hint: "[--flag] <required_arg> [optional_arg]"
---
# Command Name

## Purpose

[Brief description of what this command does]

## Process

Follow these steps:

1. **Step 1 Name**
   [Detailed instructions]

2. **Step 2 Name**
   [Detailed instructions]

3. **Step 3 Name**
   [Detailed instructions]

## Arguments

If arguments provided:
- First argument: $ARGUMENTS[0] (or $0)
- Second argument: $ARGUMENTS[1] (or $1)
- Handle accordingly: [Instructions]
If no arguments: [Default behavior]

## Output Format

[Expected output structure]

## Examples

### Example 1
Input: `/command arg1`
Output: [Expected result]

## Error Handling

If [error condition]:
- [Recovery action]
```

### Recipe Template: Context Validation Checkpoints

The standard template above works well for workflow commands. For commands that are procedurally risky (deploy flows, data migrations, one-way operations), add a "Context Validation Checkpoints" section before the steps:

```markdown
## Context Validation Checkpoints

Before executing any step, verify all of these are true.
If any checkpoint fails, stop and explain why.

* [ ] Target branch exists and is up to date with main
* [ ] No uncommitted changes in the affected files
* [ ] Required config file exists at path X
* [ ] Credentials or permissions are available
```

The checklist forces explicit precondition verification rather than letting Claude discover failures mid-execution. A failed checkpoint produces a clear error with a fixable reason; a mid-step failure produces a partial state that is harder to recover from.

Fork-ready template at `examples/commands/recipe-template.md` in this repo.

> Pattern from [Packmind command files](https://github.com/packmind/packmind) (Apache 2.0). See [Credits](./core/credits.md).

## 6.4 Command Examples

### Example 1: Commit Command

```markdown
# Commit Current Changes

## Purpose

Create a well-formatted git commit following Conventional Commits.

## Process

1. **Check Status**
   Run `git status` to see all changes.

2. **Analyze Changes**
   Run `git diff` to understand what changed.

3. **Review History**
   Run `git log -5 --oneline` to see recent commit style.

4. **Draft Message**
   Create commit message following:
   - `feat`: New feature
   - `fix`: Bug fix
   - `refactor`: Code restructuring
   - `docs`: Documentation
   - `test`: Test changes
   - `chore`: Maintenance

5. **Stage and Commit**
   ```bash
   git add [relevant files]
   git commit -m "[type](scope): description"
   ```

6. **Verify**
   Run `git status` to confirm commit succeeded.

## Arguments

If $ARGUMENTS[0] provided:
- Use as commit message hint: "$ARGUMENTS[0]" (or "$0")

## Output Format

Commit: [hash] [message]
Files: [number] changed


### Example 2: PR Command

```markdown
# Create Pull Request

## Purpose

Create a well-documented pull request on GitHub.

## Process

1. **Check Branch State**
   - `git status` - Verify clean working directory
   - `git branch` - Confirm on feature branch
   - `git log main..HEAD` - Review all commits

2. **Analyze Changes**
   - `git diff main...HEAD` - See all changes vs main
   - Understand the full scope of the PR

3. **Push if Needed**
   If branch not pushed:
   ```bash
   git push -u origin [branch-name]
   ```

4. **Create PR**

```bash
gh pr create --title "[title]" --body "[body]"
```

## PR Body Template

```markdown
## Summary
[1-3 bullet points describing changes]

## Changes
- [Specific change 1]
- [Specific change 2]

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regressions

## Screenshots
[If UI changes]
```

## Arguments

If $ARGUMENTS[0] provided:
- Use as PR title hint: "$ARGUMENTS[0]" (or "$0")

## Error Handling

If not on feature branch:
- WARN: "Create a feature branch first"

If working directory dirty:
- ASK: "Commit changes first?"

### Example 3: Problem Framer Command

```markdown
# Problem Framer

## Purpose

Challenge and refine problem definitions before solution design.

## Process

1. **Capture Initial Problem**
   Record the problem as stated by user.

2. **5 Whys Analysis**
   Ask "Why?" 5 times to find root cause:
   - Why 1: [First answer]
   - Why 2: [Deeper answer]
   - Why 3: [Even deeper]
   - Why 4: [Getting to root]
   - Why 5: [Root cause]

3. **Stakeholder Analysis**
   - Who is affected?
   - Who has decision power?
   - Who benefits from solution?

4. **Constraint Identification**
   - Technical constraints
   - Business constraints
   - Time constraints
   - Resource constraints

5. **Success Criteria**
   Define measurable outcomes:
   - [Metric 1]: [Target]
   - [Metric 2]: [Target]

6. **Reframe Problem**
   Write refined problem statement:
   "How might we [action] for [user] so that [outcome]?"

## Output Format

### Problem Analysis Report

**Original Problem**: [As stated]

**Root Cause**: [From 5 Whys]

**Refined Problem Statement**:
"How might we [X] for [Y] so that [Z]?"

**Success Criteria**:
1. [Measurable outcome 1]
2. [Measurable outcome 2]

**Constraints**:
- [Constraint 1]
- [Constraint 2]
```

---


