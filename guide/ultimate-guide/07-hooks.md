# 7. Hooks

_Quick jump:_ [The Event System](#71-the-event-system) · [Creating Hooks](#72-creating-hooks) · [Hook Templates](#73-hook-templates) · [Security Hooks](#74-security-hooks) · [Hook Examples](#75-hook-examples)

---

## 📌 Section 7 TL;DR (60 seconds)

**What are Hooks**: Scripts that run automatically on events (like git hooks)

**Event types**:
- `PreToolUse` → Before Claude runs a tool (e.g., block dangerous commands)
- `PostToolUse` → After Claude runs a tool (e.g., auto-format code)
- `UserPromptSubmit` → When you send a message (e.g., inject context)

**Common use cases**:
- 🛡️ Security: Block file deletions, prevent secrets in commits
- 🎨 Quality: Auto-format, lint, run tests
- 📊 Logging: Track commands, audit changes

**Quick Start**: See [7.3 Hook Templates](#73-hook-templates) for copy-paste examples

**Read this section if**: You want automation or need safety guardrails
**Skip if**: Manual control is sufficient for your workflow

---

**Reading time**: 20 minutes
**Skill level**: Week 2-3
**Goal**: Automate Claude Code with event-driven scripts

## 7.1 The Event System

Hooks are scripts that run automatically when specific events occur.

### Event Types

**Lifecycle** (session-level events):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `SessionStart` | Session begins or resumes | No | Initialization, load dev context |
| `Setup` | Environment setup phase at session start | No | Install tools, validate prerequisites |
| `SessionEnd` | Session terminates | No | Cleanup, logging |

**Agent actions** (tool execution pipeline):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `Stop` | Claude finishes responding | Yes | Post-response actions, continue loops |
| `StopFailure` | Turn ends due to API error (rate limit, auth failure) | No | Alert on quota exhaustion, observability |
| `PreToolUse` | Before a tool call executes | Yes | Security validation, input modification |
| `PostToolUse` | After a tool completes successfully | No | Formatting, logging |
| `PostToolUseFailure` | After a tool call fails | No | Error logging, recovery actions |

**Permissions** (approval flow):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `PermissionRequest` | Permission dialog appears | Yes | Custom approval logic |
| `PermissionDenied` | A permission is denied | No | Audit denied operations, alert |

**Compaction** (context management):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `PreCompact` | Before context compaction | No | Save state before compaction |
| `PostCompact` | After context compaction completes | No | Restore state, log compaction |

**Multi-agent** (orchestration):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `SubagentStart` | Sub-agent spawned | No | Subagent initialization |
| `SubagentStop` | Sub-agent finishes | Yes | Subagent cleanup |
| `TeammateIdle` | Agent team member about to go idle | Yes | Team coordination, quality gates |
| `TaskCreated` | Task created via TaskCreate | No | Task monitoring, audit logging |
| `TaskCompleted` | Task being marked as completed | Yes | Enforce completion criteria |

**Configuration** (settings & instructions):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `ConfigChange` | Config file changes during session | Yes (except policy) | Enterprise audit, block unauthorized changes |
| `InstructionsLoaded` | CLAUDE.md or instructions file loaded | No | Audit which instruction files are active |

**File system** (workspace changes):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `CwdChanged` | Working directory changes during session | No | direnv reload, toolchain switching |
| `FileChanged` | A file is modified during session | No | Reload config, trigger watchers |
| `WorktreeCreate` | Worktree being created | Yes (non-zero exit) | Custom VCS setup |
| `WorktreeRemove` | Worktree being removed | No | Clean up VCS state |

**User interaction** (prompts & notifications):

| Event | When It Fires | Can Block? | Use Case |
|-------|---------------|------------|----------|
| `UserPromptSubmit` | User submits prompt, before Claude processes it | Yes | Context enrichment, prompt validation |
| `Notification` | Claude sends notification | No | Sound alerts, custom notifications |
| `Elicitation` | Claude requests information from user (headless) | Yes | Intercept and pre-answer questions in automation |
| `ElicitationResult` | Response to an elicitation is received | No | Log or audit user responses to Claude's questions |

> **`Stop` and `SubagentStop` — `last_assistant_message` field (v2.1.47+)**: These events now include a `last_assistant_message` field in their JSON input, giving direct access to Claude's final response without parsing transcript files. Useful for orchestration pipelines that need to inspect or log the last output.
>
> ```bash
> # In your Stop hook script
> LAST_MSG=$(cat | jq -r '.last_assistant_message // ""')
> echo "$LAST_MSG" >> ~/.claude/logs/session-outputs.log
> ```

### Event Flow

```
┌─────────────────────────────────────────────────────────┐
│                      EVENT FLOW                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   User types message                                    │
│        │                                                │
│        ▼                                                │
│   ┌────────────────────┐                                │
│   │ UserPromptSubmit   │  ← Add context (git status)    │
│   └────────────────────┘                                │
│        │                                                │
│        ▼                                                │
│   Claude decides to run tool (e.g., Edit)               │
│        │                                                │
│        ▼                                                │
│   ┌────────────────────┐                                │
│   │ PreToolUse         │  ← Security check              │
│   └────────────────────┘                                │
│        │                                                │
│        ▼ (if allowed)                                   │
│   Tool executes                                         │
│        │                                                │
│        ▼                                                │
│   ┌────────────────────┐                                │
│   │ PostToolUse        │  ← Auto-format                 │
│   └────────────────────┘                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Hook Execution Model (v2.1.0+)

Claude Code supports two execution models for hooks:

#### Synchronous (Default)

- Claude **blocks** until the hook completes
- Exit code and stdout available immediately for feedback
- **Use case**: Critical validation (security, type checking, blocking operations)
- **Configuration**: Omit `async` or set `async: false`

#### Asynchronous (Optional)

- Claude **continues immediately**, hook runs in background
- Exit code/stdout NOT available to Claude (no feedback loop)
- **Use case**: Non-critical operations (logging, notifications, formatting, metrics)
- **Configuration**: Add `async: true` to hook definition

#### Configuration Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/auto-format.sh",
            "timeout": 10000,
            "async": true  // ← Non-blocking execution
          },
          {
            "type": "command",
            "command": ".claude/hooks/typecheck.sh"
            // Sync by default - blocks on completion
          }
        ]
      }
    ]
  }
}
```

#### Decision Matrix

| Hook Purpose | Execution Mode | Reason |
|--------------|---------------|--------|
| Code formatting (Prettier, Black) | **Async** | Cosmetic change, no feedback needed |
| Linting with auto-fix (eslint --fix) | **Async** | Non-critical improvements |
| Type checking (tsc, mypy) | **Sync** | Errors must block for iteration |
| Security validation | **Sync** | Must block dangerous operations |
| Logging/metrics | **Async** | Pure side-effect, no feedback |
| Notifications (Slack, email) | **Async** | User alerts, non-blocking |
| Test execution | **Sync** | Results influence next action |
| Git context injection | **Sync** | Enriches prompt before processing |

#### Performance Impact

**Example session (10 file edits):**
- **Sync hooks**: `auto-format.sh` (500ms) × 10 = 5s blocked
- **Async hooks**: `auto-format.sh` runs in background = 0s blocked
- **Gain**: ~5-10s per typical development session

#### Limitations of Async Hooks

⚠️ Async hooks cannot:
- Block Claude on errors (exit code 2 ignored)
- Provide real-time feedback via stdout or `systemMessage`
- Guarantee execution order with other hooks
- Return `additionalContext` that Claude can use

Use async only when the hook's completion is truly independent of Claude's workflow.

#### When Async Was Introduced

- **v2.1.0**: Initial async hook support (configuration via `async: true`)
- **v2.1.23**: Fixed bug where async hooks weren't properly cancelled when headless streaming sessions ended

### Shell Scripts vs AI Agents: When to Use What

Not everything needs AI. Choose the right tool:

| Task Type | Best Tool | Why | Example |
|-----------|-----------|-----|---------|
| **Deterministic** | Bash script | Fast, predictable, no tokens | Create branch, fetch PR comments |
| **Pattern-based** | Bash + regex | Reliable for known patterns | Check for secrets, validate format |
| **Interpretation needed** | AI Agent | Judgment required | Code review, architecture decisions |
| **Context-dependent** | AI Agent | Needs understanding | "Does this match requirements?" |

**Rule of thumb**: If you can write a regex or a simple conditional for it, use a bash script. If it requires "understanding" or "judgment", use an agent.

**Example — PR workflow**:
```bash
# Deterministic (bash): create branch, push, open PR
git checkout -b feature/xyz
git push -u origin feature/xyz
gh pr create --title "..." --body "..."

# Interpretation (agent): review code quality
# → Use code-review subagent
```

**Why this matters**: Bash scripts are instant, free (no tokens), and 100% predictable. Reserve AI for tasks that genuinely need intelligence.

> Inspired by [Nick Tune's Coding Agent Development Workflows](https://medium.com/nick-tune-tech-strategy-blog/coding-agent-development-workflows-af52e6f912aa)

## 7.2 Creating Hooks

### Hook Registration (settings.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/security-check.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### Configuration Fields

| Field | Description |
|-------|-------------|
| `matcher` | Regex pattern filtering when hooks fire (tool name, session start reason, etc.) |
| `if` | Permission-rule filter controlling when the hook fires (e.g. `Bash(git *)`) — v2.1.85+ |
| `type` | Hook type: `"command"`, `"http"`, `"prompt"`, or `"agent"` |
| `command` | Shell command to run (for `command` type) |
| `args` | `string[]` — exec form: array of strings spawned directly without a shell. Path placeholders need no quoting. When present, `command` is ignored. Use to avoid shell-injection risks. (v2.1.139) |
| `prompt` | Prompt text for LLM evaluation (for `prompt`/`agent` types). Use `$ARGUMENTS` as placeholder for hook input JSON |
| `timeout` | Max execution time in seconds (default: 600s command, 30s prompt, 60s agent) |
| `model` | Model to use for evaluation (for `prompt`/`agent` types). Defaults to a fast model |
| `async` | If `true`, runs in background without blocking (for `command` type only) |
| `statusMessage` | Custom spinner message displayed while hook runs |
| `once` | If `true`, runs only once per session then is removed (skills only) |

> **Exec form (`args`)**: Use `args: ["program", "arg1", "arg2"]` to spawn the command without a shell interpreter. Useful when paths contain spaces or special characters that would require quoting in `command`. Exec form also avoids shell injection risks in automated contexts.

### Session-Scoped Hooks

Hooks do not have to be persisted in `settings.json`. Claude Code supports ephemeral **session-scoped hooks** that are registered at runtime and last only for the duration of the current session. They are never written to any config file and disappear when the session ends.

This is the mechanism skills use internally: when you invoke a skill, it can register one or more hooks for that invocation without permanently modifying your configuration. Once the skill finishes (or the session ends), those hooks are gone.

**When to use session-scoped hooks**:
- Skills that need event callbacks only while they are active
- Temporary automation (e.g., "audit every file I edit during this session only")
- CI pipelines or orchestration scripts that inject hooks via the API programmatically

Session-scoped hooks follow the same JSON schema as `settings.json` hooks (same event names, matchers, types, and output format) and can be registered through the programmatic API or by skills at invocation time.

**Hook types:**

- **`command`**: Runs a shell command. Receives JSON on stdin, returns JSON on stdout. Most common type.
- **`http`** *(v2.1.63+)*: POSTs JSON to a URL and reads JSON response. Useful for CI/CD webhooks and stateless backend integrations without shell dependencies. Configure with `url` and optional `allowedEnvVars` for header interpolation.
- **`prompt`**: Sends prompt + hook input to a Claude model (Haiku by default) for single-turn evaluation. Returns `{ok: true/false, reason: "..."}`. Configure model via `model` field.
- **`agent`**: Spawns a subagent with tool access (Read, Grep, Glob, etc.) for multi-turn verification. Returns same `{ok: true/false}` format. Up to 50 tool-use turns.

**HTTP hook example** (v2.1.63+):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "http",
            "url": "https://ci.example.com/webhook/claude-hook",
            "allowedEnvVars": ["CI_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

HTTP hooks receive the same JSON payload as `command` hooks and must return valid JSON. The `allowedEnvVars` field lists environment variables that can be referenced in headers (e.g., for Bearer token authentication).

### Conditional Hooks with `if` (v2.1.85+)

The `if` field filters when a hook fires using the same permission-rule syntax as `allowedTools`. This avoids spawning subprocesses on every event and eliminates the need for shell-side `case` statements.

```json
// Before: hook fires on every PostToolUse — guard logic inside the script
{
  "event": "PostToolUse",
  "command": "./scripts/log-tool-usage.sh"
}

// After: hook fires only when Bash executes a git command
{
  "event": "PostToolUse",
  "if": "Bash(git *)",
  "command": "./scripts/log-git-usage.sh"
}
```

Supported `if` patterns follow the same syntax as tool permission rules:

| Pattern | Fires when |
|---------|-----------|
| `Bash(git *)` | Any Bash call starting with `git` |
| `Edit` | Any Edit tool call |
| `Write(/tmp/*)` | Write to paths under `/tmp/` |
| `Bash(npm * \| yarn *)` | npm or yarn commands |

> **Performance**: Every hook spawn is a subprocess. Conditional `if` filtering reduces overhead in large repos where PostToolUse fires hundreds of times per session.

### Hook Input (stdin JSON)

Hooks receive JSON on stdin with common fields (all events) plus event-specific fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git status"
  }
}
```

> **Common fields (all events)**: `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`. Event-specific fields (like `tool_name` and `tool_input` for PreToolUse) are added on top.

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Unique session identifier |
| `transcript_path` | string | Path to session transcript file |
| `cwd` | string | Current working directory |
| `permission_mode` | string | Active permission mode |
| `hook_event_name` | string | Event that triggered the hook |
| `effort.level` | string | Active effort level: `low`, `medium`, `high`, `xhigh`, `max`. Bash-type hooks also receive this as `$CLAUDE_EFFORT` env var. (v2.1.133) |

### Hook Output

Hooks communicate results through exit codes and optional JSON on stdout. Choose one approach per hook: either exit codes alone, or exit 0 with JSON for structured control. Claude Code only processes JSON on exit 0, so if your hook exits with any other code, stdout and any JSON it contains are silently discarded.

**Universal JSON fields** (all events):

| Field | Default | Description |
|-------|---------|-------------|
| `continue` | `true` | If `false`, Claude stops processing entirely |
| `stopReason` | none | Message shown to user when `continue` is `false` |
| `suppressOutput` | `false` | If `true`, hides stdout from verbose mode |
| `systemMessage` | none | Warning message shown to user |

**Event-specific decision control** varies by event type:

- **PreToolUse**: Uses `hookSpecificOutput` with `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`, `updatedInput`, `additionalContext`. When multiple PreToolUse hooks return different decisions, precedence is: `deny` > `defer` > `ask` > `allow` (v2.1.89+).
- **PostToolUse, Stop, SubagentStop, UserPromptSubmit, ConfigChange**: Uses top-level `decision: "block"` with `reason`
- **TeammateIdle, TaskCompleted**: Exit code 2 only (no JSON decision control)
- **PermissionRequest**: Uses `hookSpecificOutput` with `decision.behavior` (allow/deny)

**`continueOnBlock`** (`PostToolUse` only, v2.1.139): When `true`, a `decision: "block"` response feeds the `reason` back to Claude as context and continues the turn instead of halting. Use to give Claude a chance to retry with a compliant approach:

```json
{
  "type": "PostToolUse",
  "matcher": "Write|Edit",
  "command": "check-file-policy.sh",
  "continueOnBlock": true
}
```

Without `continueOnBlock`, a blocked PostToolUse stops the turn and surfaces an error. With it, Claude receives the rejection reason and can self-correct.

**Output replacement** (`PostToolUse`, v2.1.121): `PostToolUse` hooks can replace what Claude receives as the tool result via `hookSpecificOutput.updatedToolOutput`. Works for all tools: Bash, Read, Write, Edit, MCP tools, etc.:

```json
{
  "hookSpecificOutput": {
    "updatedToolOutput": "redacted: output contained PII, removed by policy hook"
  }
}
```

Use cases: scrub PII from tool outputs before Claude processes them, compress large results, inject metadata or audit trails into every tool response.

**PreToolUse blocking example** (preferred over exit code 2):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

**PreToolUse context injection**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "Current git branch: feature/auth. 3 uncommitted files."
  }
}
```

**PreToolUse satisfying AskUserQuestion (v2.1.85+ — headless integrations)**:

When Claude fires `AskUserQuestion` mid-session, interactive prompts are not available in headless environments (CI pipelines, web frontends, orchestrators). A `PreToolUse` hook can intercept the question, collect the answer via an external UI, and return it before the tool executes:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "updatedInput": { "answer": "yes, proceed with migration" },
    "permissionDecision": "allow"
  }
}
```

The hook script is responsible for retrieving the answer (e.g., polling a webhook or reading from a queue). Return `updatedInput` with the answer and `permissionDecision: "allow"` to satisfy the question and continue execution without interactive prompts.

**PreToolUse `defer` decision (v2.1.89+ — headless/non-interactive only)**:

`defer` is designed for headless integrations where Claude is orchestrated by an external process. When a hook returns `permissionDecision: "defer"`, Claude pauses with `stop_reason: "tool_deferred"` and waits. The calling process can then collect input from a user or another system and resume the session with `--resume <session-id>`. In interactive terminal sessions, `defer` is ignored with a warning.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "defer",
    "permissionDecisionReason": "Awaiting human approval via external workflow"
  }
}
```

### Exit Codes

| Code | Meaning | Result |
|------|---------|--------|
| `0` | Success | Allow operation, parse stdout for JSON output |
| `2` | Blocking error | Prevent operation (for blocking events), stderr fed to Claude. stdout is silently ignored. |
| Other | Non-blocking error | Stderr shown in verbose mode (`Ctrl+O`), execution continues |

### Silent Success Pattern

A key principle for keeping the agent's context clean: **hooks should be silent on success and verbose on failure only.**

```bash
#!/bin/bash
# .claude/hooks/build-check.sh — Silent Success pattern
# On success: completely silent (nothing enters agent context)
# On failure: surface errors + exit 2 to re-engage agent

OUTPUT=$(bun run build 2>&1)
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
    exit 0  # Silent — no output, no context noise
fi

# Failure: send errors to agent for correction
echo "$OUTPUT" >&2
exit 2
```

This asymmetry (silence on success, signal on failure) prevents successful build logs, test output, and lint reports from accumulating as "context noise" in long sessions. The agent only sees what requires action.

> Source: Pattern formalized by [HumanLayer — Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) (March 2026). Also validated by RTK's design philosophy: suppress successful command output, surface errors only.

## 7.3 Hook Templates

### Template 1: PreToolUse (Security Blocker)

```bash
#!/bin/bash
# .claude/hooks/security-blocker.sh
# Blocks dangerous commands

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# List of dangerous patterns
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf *"
    "sudo rm"
    "git push --force origin main"
    "git push -f origin main"
    "npm publish"
    "> /dev/sda"
)

# Check if command matches any dangerous pattern
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        echo "BLOCKED: Dangerous command detected: $pattern" >&2
        exit 2
    fi
done

exit 0
```

### Template 2: PostToolUse (Auto-Formatter)

```bash
#!/bin/bash
# .claude/hooks/auto-format.sh
# Auto-formats code after edits

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Only run for Edit/Write operations
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

# Get the file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Run Prettier on supported files
if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx|json|md|css|scss)$ ]]; then
    npx prettier --write "$FILE_PATH" 2>/dev/null
fi

exit 0
```

### Template 3: UserPromptSubmit (Context Enricher)

```bash
#!/bin/bash
# .claude/hooks/git-context.sh
# Adds git context to every prompt

# Get git information
BRANCH=$(git branch --show-current 2>/dev/null || echo "not a git repo")
LAST_COMMIT=$(git log -1 --format='%h %s' 2>/dev/null || echo "no commits")
STAGED=$(git diff --cached --stat 2>/dev/null | tail -1 || echo "none")
UNSTAGED=$(git diff --stat 2>/dev/null | tail -1 || echo "none")

# Output JSON with context
cat << EOF
{
  "hookSpecificOutput": {
    "additionalContext": "[Git] Branch: $BRANCH | Last: $LAST_COMMIT | Staged: $STAGED | Unstaged: $UNSTAGED"
  }
}
EOF

exit 0
```

### Template 4: Notification (Sound Alerts)

```bash
#!/bin/bash
# .claude/hooks/notification.sh
# Plays sounds on notifications (macOS)

INPUT=$(cat)
TITLE=$(echo "$INPUT" | jq -r '.title // ""')
MESSAGE=$(echo "$INPUT" | jq -r '.message // ""')
TYPE=$(echo "$INPUT" | jq -r '.notification_type // ""')

# Determine sound based on content
if [[ "$TITLE" == *"error"* ]] || [[ "$MESSAGE" == *"failed"* ]]; then
    SOUND="/System/Library/Sounds/Basso.aiff"
elif [[ "$TITLE" == *"complete"* ]] || [[ "$MESSAGE" == *"success"* ]]; then
    SOUND="/System/Library/Sounds/Hero.aiff"
else
    SOUND="/System/Library/Sounds/Pop.aiff"
fi

# Play sound (macOS)
afplay "$SOUND" 2>/dev/null &

exit 0
```

### PowerShell Native Tool (Windows, v2.1.84+ opt-in preview)

On Windows, Claude Code can use PowerShell as a first-class tool alongside Bash — allowing `.ps1` scripts, PowerShell modules, and Windows-native commands without requiring WSL or Git Bash.

Enable it in `~/.claude/settings.json`:

```json
{
  "tools": {
    "powershell": {
      "enabled": true
    }
  }
}
```

Once enabled, Claude can execute PowerShell commands directly (e.g., `Get-ChildItem`, `Invoke-WebRequest`, `dotnet` CLI). Useful for teams working in Windows-first environments where `.ps1` scripts are the standard automation layer.

> **Preview**: This is an opt-in preview as of v2.1.84. The Bash tool remains available on Windows via Git Bash or WSL and is still preferred for cross-platform scripts.

### Windows Hook Templates

Windows users can create hooks using PowerShell (.ps1) or batch files (.cmd).

> **Note**: Windows hooks should use the full PowerShell invocation with `-ExecutionPolicy Bypass` to avoid execution policy restrictions.

#### Template W1: PreToolUse Security Check (PowerShell)

Create `.claude/hooks/security-check.ps1`:

```powershell
# security-check.ps1
# Blocks dangerous commands

$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
$command = $inputJson.tool_input.command

# List of dangerous patterns
$dangerousPatterns = @(
    "rm -rf /",
    "rm -rf ~",
    "Remove-Item -Recurse -Force C:\",
    "git push --force origin main",
    "git push -f origin main",
    "npm publish"
)

foreach ($pattern in $dangerousPatterns) {
    if ($command -like "*$pattern*") {
        Write-Error "BLOCKED: Dangerous command detected: $pattern"
        exit 2
    }
}

exit 0
```

#### Template W2: PostToolUse Auto-Formatter (PowerShell)

Create `.claude/hooks/auto-format.ps1`:

```powershell
# auto-format.ps1
# Auto-formats code after edits

$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
$toolName = $inputJson.tool_name

if ($toolName -ne "Edit" -and $toolName -ne "Write") {
    exit 0
}

$filePath = $inputJson.tool_input.file_path

if (-not $filePath) {
    exit 0
}

if ($filePath -match '\.(ts|tsx|js|jsx|json|md|css|scss)$') {
    npx prettier --write $filePath 2>$null
}

exit 0
```

#### Template W3: Context Enricher (Batch File)

Create `.claude/hooks/git-context.cmd`:

```batch
@echo off
setlocal enabledelayedexpansion

for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set BRANCH=%%i
if "%BRANCH%"=="" set BRANCH=not a git repo

for /f "tokens=*" %%i in ('git log -1 --format^="%%h %%s" 2^>nul') do set LAST_COMMIT=%%i
if "%LAST_COMMIT%"=="" set LAST_COMMIT=no commits

echo {"hookSpecificOutput":{"additionalContext":"[Git] Branch: %BRANCH% | Last: %LAST_COMMIT%"}}
exit /b 0
```

#### Template W4: Notification (Windows)

Create `.claude/hooks/notification.ps1`:

```powershell
# notification.ps1
# Shows Windows toast notifications and plays sounds

$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
$title = $inputJson.title
$message = $inputJson.message

# Determine sound based on content
if ($title -match "error" -or $message -match "failed") {
    [System.Media.SystemSounds]::Hand.Play()
} elseif ($title -match "complete" -or $message -match "success") {
    [System.Media.SystemSounds]::Asterisk.Play()
} else {
    [System.Media.SystemSounds]::Beep.Play()
}

# Optional: Show Windows Toast Notification (requires BurntToast module)
# Install-Module -Name BurntToast
# New-BurntToastNotification -Text $title, $body

exit 0
```

#### Windows settings.json for Hooks

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/security-check.ps1",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/auto-format.ps1",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

## 7.4 Security Hooks

Security hooks are critical for protecting your system.

> **Advanced patterns**: For comprehensive security including Unicode injection detection, MCP config integrity verification, and CVE-specific mitigations, see [Security Hardening Guide](./security/security-hardening.md).

> **Claude Code Security (research preview)**: Anthropic offers a dedicated codebase vulnerability scanner that traces data flows across files, challenges findings internally before surfacing them (adversarial validation), and generates patch suggestions. Separate from the Security Auditor Agent above — waitlist access only. See [Security Hardening Guide → Claude Code as Security Scanner](./security/security-hardening.md#claude-code-as-security-scanner-research-preview).
>
> **Validated at scale**: In a March 2026 partnership with Mozilla, Claude Opus 4.6 scanned ~6,000 C++ files in Firefox's JS engine in two weeks, surfacing 22 confirmed vulnerabilities (14 high severity) — roughly one fifth of all high-severity Firefox CVEs fixed in 2025. Demonstrates the model's practical depth for production security work, well beyond surface-level linting.

### Recommended Security Rules

```bash
#!/bin/bash
# .claude/hooks/comprehensive-security.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# === CRITICAL BLOCKS (Exit 2) ===

# Filesystem destruction
[[ "$COMMAND" =~ rm.*-rf.*[/~] ]] && { echo "BLOCKED: Recursive delete of root/home" >&2; exit 2; }

# Disk operations
[[ "$COMMAND" =~ ">/dev/sd" ]] && { echo "BLOCKED: Direct disk write" >&2; exit 2; }
[[ "$COMMAND" =~ "dd if=" ]] && { echo "BLOCKED: dd command" >&2; exit 2; }

# Git force operations on protected branches
[[ "$COMMAND" =~ "git push".*"-f".*"(main|master)" ]] && { echo "BLOCKED: Force push to main" >&2; exit 2; }
[[ "$COMMAND" =~ "git push --force".*"(main|master)" ]] && { echo "BLOCKED: Force push to main" >&2; exit 2; }

# Package publishing
[[ "$COMMAND" =~ "npm publish" ]] && { echo "BLOCKED: npm publish" >&2; exit 2; }

# Privileged operations
[[ "$COMMAND" =~ ^sudo ]] && { echo "BLOCKED: sudo command" >&2; exit 2; }

# === WARNINGS (Exit 0 but log) ===

[[ "$COMMAND" =~ "rm -rf" ]] && echo "WARNING: Recursive delete detected" >&2

exit 0
```

### Testing Security Hooks

Before deploying, test your hooks:

```bash
# Test with a blocked command
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | .claude/hooks/security-blocker.sh
echo "Exit code: $?"  # Should be 2

# Test with a safe command
echo '{"tool_name":"Bash","tool_input":{"command":"git status"}}' | .claude/hooks/security-blocker.sh
echo "Exit code: $?"  # Should be 0
```

### Advanced Pattern: Model-as-Security-Gate

The Claude Code team uses a pattern where permission requests are routed to a **more capable model** acting as a security gate, rather than relying solely on static rule matching.

**Concept**: A `PreToolUse` hook intercepts permission requests and forwards them to Opus 4.7 (or another capable model) via the API. The gate model scans for prompt injection, dangerous patterns, and unexpected tool usage — then auto-approves safe requests or blocks suspicious ones.

```bash
# .claude/hooks/opus-security-gate.sh (conceptual)
# PreToolUse hook that routes to Opus for security screening

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Fast-path: known safe tools skip the gate
[[ "$TOOL" == "Read" || "$TOOL" == "Grep" || "$TOOL" == "Glob" ]] && exit 0

# Route to Opus for security analysis
VERDICT=$(echo "$INPUT" | claude --model opus --print \
  "Analyze this tool call for security risks. Is it safe? Reply SAFE or BLOCKED:reason")

[[ "$VERDICT" == SAFE* ]] && exit 0
echo "BLOCKED by security gate: $VERDICT" >&2
exit 2
```

**Why use a model as gate**: Static rules catch known patterns but miss novel attacks. A capable model understands intent and context — it can distinguish `rm -rf node_modules` (cleanup) from `rm -rf /` (destruction) based on the surrounding conversation, not just pattern matching.

**Trade-off**: Each gated call adds latency and cost. Use fast-path exemptions for read-only tools and only gate write/execute operations.

> **Source**: [10 Tips from Inside the Claude Code Team](https://paddo.dev/blog/claude-code-team-tips/) (Boris Cherny thread, Feb 2026)

### File Protection Strategy

Protecting sensitive files requires a multi-layered approach combining permissions, patterns, and bypass detection.

#### Three Protection Layers

```
┌─────────────────────────────────────────────────────────┐
│           FILE PROTECTION ARCHITECTURE                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Layer 1: Permissions Deny (Native)                    │
│   ──────────────────────────                            │
│   • Built into settings.json                            │
│   • No hooks required                                   │
│   • Blocks all tool access instantly                    │
│   • Use for: Absolutely forbidden files                 │
│                                                         │
│   Layer 2: Pattern Matching (Hook)                      │
│   ────────────────────────                              │
│   • PreToolUse hook with .agentignore patterns          │
│   • Supports gitignore-style syntax                     │
│   • Centralized protection rules                        │
│   • Use for: Sensitive file categories                  │
│                                                         │
│   Layer 3: Bypass Detection (Hook)                      │
│   ──────────────────────────                            │
│   • Detects variable expansion ($VAR, ${VAR})           │
│   • Detects command substitution $(cmd), `cmd`          │
│   • Prevents path manipulation attempts                 │
│   • Use for: Defense against sophisticated attacks      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### Layer 1: permissions.deny

```json
{
  "permissions": {
    "deny": [
      ".env",
      ".env.local",
      ".env.production",
      "**/*.key",
      "**/*.pem",
      "credentials.json",
      ".aws/credentials"
    ]
  }
}
```

**Pros**: Instant blocking, no hooks needed
**Cons**: No custom logic, cannot log attempts

#### Layer 2: .agentignore Pattern File

Create `.agentignore` (or `.aiignore`) in your project root:

```gitignore
# Credentials
.env*
*.key
*.pem
*.p12
credentials.json
secrets.yaml

# Config
config/secrets/
.aws/credentials
.ssh/id_*

# Build artifacts (if generated from secrets)
dist/.env
build/config/production.json
```

**Unified hook** (See: `examples/hooks/bash/file-guard.sh`):

```bash
# .claude/hooks/file-guard.sh
# Reads .agentignore and blocks matching files
# Also detects bash bypass attempts
```

**Pros**: Gitignore syntax familiar, centralized rules, version controlled
**Cons**: Requires hook implementation

#### Layer 3: Bypass Detection

Sophisticated attacks may try to bypass protection using variable expansion:

```bash
# Attack attempts
FILE="sensitive.key"
cat $FILE              # Variable expansion bypass

HOME_DIR=$HOME
cat $HOME_DIR/.env     # Variable substitution bypass

cat $(echo ".env")     # Command substitution bypass
```

The `file-guard.sh` hook detects these patterns:

```bash
# Detection logic
detect_bypass() {
    local file="$1"

    # Variable expansion
    [[ "$file" =~ \$\{?[A-Za-z_][A-Za-z0-9_]*\}? ]] && return 0

    # Command substitution
    [[ "$file" =~ \$\( || "$file" =~ \` ]] && return 0

    return 1
}
```

#### Complete Protection Example

**1. Configure settings.json**:

```json
{
  "permissions": {
    "deny": [".env", "*.key", "*.pem"]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/file-guard.sh",
            "timeout": 2000
          }
        ]
      }
    ]
  }
}
```

**2. Create .agentignore**:

```gitignore
.env*
config/secrets/
**/*.key
**/*.pem
credentials.json
```

**3. Copy hook template**:

```bash
cp examples/hooks/bash/file-guard.sh .claude/hooks/
chmod +x .claude/hooks/file-guard.sh
```

#### Testing Protection

```bash
# Test direct access
echo '{"tool_name":"Read","tool_input":{"file_path":".env"}}' | \
  .claude/hooks/file-guard.sh
# Should exit 1 and show "File access blocked"

# Test bypass attempt
echo '{"tool_name":"Read","tool_input":{"file_path":"$HOME/.env"}}' | \
  .claude/hooks/file-guard.sh
# Should exit 1 and show "Variable expansion detected"
```

> **Cross-reference**: For full security hardening including CVE-specific mitigations and MCP config integrity, see [Security Hardening Guide](./security/security-hardening.md).

## 7.5 Hook Examples

### Smart Hook Dispatching

Instead of configuring dozens of individual hooks, use a **single dispatcher** that routes events intelligently based on file type, tool, and context.

**The problem**: As your hook collection grows, `settings.json` becomes unwieldy with repeated matchers and overlapping configurations.

**The solution**: One entry point that dispatches to specialized handlers.

```bash
#!/bin/bash
# .claude/hooks/dispatch.sh
# Single entry point for all PostToolUse hooks
# Routes to specialized handlers based on file type and tool

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.command // ""')
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // "unknown"')

HOOKS_DIR="$(dirname "$0")/handlers"

# Route by file extension
case "$FILE_PATH" in
    *.ts|*.tsx)
        [[ -x "$HOOKS_DIR/typescript.sh" ]] && echo "$INPUT" | "$HOOKS_DIR/typescript.sh"
        ;;
    *.py)
        [[ -x "$HOOKS_DIR/python.sh" ]] && echo "$INPUT" | "$HOOKS_DIR/python.sh"
        ;;
    *.rs)
        [[ -x "$HOOKS_DIR/rust.sh" ]] && echo "$INPUT" | "$HOOKS_DIR/rust.sh"
        ;;
    *.sql|*.prisma)
        [[ -x "$HOOKS_DIR/database.sh" ]] && echo "$INPUT" | "$HOOKS_DIR/database.sh"
        ;;
esac

# Route by tool (always runs, regardless of file type)
case "$TOOL_NAME" in
    Bash)
        [[ -x "$HOOKS_DIR/security.sh" ]] && echo "$INPUT" | "$HOOKS_DIR/security.sh"
        ;;
    Write)
        [[ -x "$HOOKS_DIR/new-file.sh" ]] && echo "$INPUT" | "$HOOKS_DIR/new-file.sh"
        ;;
esac

exit 0
```

**Configuration** (minimal `settings.json`):

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write|Bash",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/dispatch.sh"
      }]
    }]
  }
}
```

**Handler directory structure**:

```
.claude/hooks/
├── dispatch.sh              # Single entry point
└── handlers/
    ├── typescript.sh         # ESLint + tsc for .ts/.tsx
    ├── python.sh             # Ruff + mypy for .py
    ├── rust.sh               # cargo clippy for .rs
    ├── database.sh           # Schema validation for .sql/.prisma
    ├── security.sh           # Block dangerous bash commands
    └── new-file.sh           # Check naming conventions on Write
```

**Benefits over individual hooks**:
- **Single matcher** in settings.json (instead of N matchers)
- **Easy to extend**: Drop a new handler in `handlers/`, no config change needed
- **Language-aware**: Different validation per file type
- **Composable**: File-type hooks and tool hooks both run when applicable
- **Debuggable**: `echo "$INPUT" | .claude/hooks/dispatch.sh` tests the full chain

### Example 1: Activity Logger

```bash
#!/bin/bash
# .claude/hooks/activity-logger.sh
# Logs all tool usage to JSONL file

INPUT=$(cat)
LOG_DIR="$HOME/.claude/logs"
LOG_FILE="$LOG_DIR/activity-$(date +%Y-%m-%d).jsonl"

# Create log directory
mkdir -p "$LOG_DIR"

# Clean up old logs (keep 7 days)
find "$LOG_DIR" -name "activity-*.jsonl" -mtime +7 -delete

# Extract tool info
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')

# Create log entry
LOG_ENTRY=$(jq -n \
  --arg timestamp "$TIMESTAMP" \
  --arg tool "$TOOL_NAME" \
  --arg session "$SESSION_ID" \
  '{timestamp: $timestamp, tool: $tool, session: $session}')

# Append to log
echo "$LOG_ENTRY" >> "$LOG_FILE"

exit 0
```

### Example 2: Linting Gate

```bash
#!/bin/bash
# .claude/hooks/lint-gate.sh
# Runs linter after code changes

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Only check after Edit/Write
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Only lint TypeScript/JavaScript
if [[ ! "$FILE_PATH" =~ \.(ts|tsx|js|jsx)$ ]]; then
    exit 0
fi

# Run ESLint
LINT_OUTPUT=$(npx eslint "$FILE_PATH" 2>&1)
LINT_EXIT=$?

if [[ $LINT_EXIT -ne 0 ]]; then
    cat << EOF
{
  "systemMessage": "Lint errors found in $FILE_PATH:\n$LINT_OUTPUT"
}
EOF
fi

exit 0
```

### Validation Pipeline Pattern

Chain multiple validation hooks to catch issues immediately after code changes. This pattern ensures code quality without manual intervention.

#### The Pattern

```
Edit/Write → TypeCheck → Lint → Tests → Notify Claude
   ↓            ↓         ↓       ↓
  file.ts    tsc check  eslint  jest file.test.ts
```

**Benefits**:
- Catch errors immediately (before next Claude action)
- No need to manually run `npm run typecheck && npm run lint && npm test`
- Fast feedback loop → faster iteration
- Prevents cascading errors (Claude gets quality signal early)

#### Three-Stage Pipeline Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/typecheck-on-save.sh",
            "timeout": 5000
          },
          {
            "type": "command",
            "command": ".claude/hooks/lint-gate.sh",
            "timeout": 5000
          },
          {
            "type": "command",
            "command": ".claude/hooks/test-on-change.sh",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

**Hook order matters**: Run fast checks first (typecheck ~1s), then slower ones (tests ~3-5s).

#### Stage 1: Type Checking

See: `examples/hooks/bash/typecheck-on-save.sh`

```bash
# Runs tsc on TypeScript files after edits
# Only reports errors (not warnings)
# Timeout: 5s (should be fast)
```

**What it catches**:
- Type mismatches
- Missing imports
- Invalid property access
- Generic constraints violations

#### Stage 2: Linting

Already documented in Example 2 above (lint-gate.sh).

**What it catches**:
- Code style violations
- Unused variables
- Missing semicolons
- Import order issues

#### Stage 3: Test Execution

See: `examples/hooks/bash/test-on-change.sh`

```bash
# Detects associated test file and runs it
# Supports: Jest (.test.ts), Pytest (_test.py), Go (_test.go)
# Only runs if test file exists
```

**Test file detection logic**:

| Source File | Test File Patterns |
|-------------|-------------------|
| `auth.ts` | `auth.test.ts`, `__tests__/auth.test.ts` |
| `utils.py` | `utils_test.py`, `test_utils.py` |
| `main.go` | `main_test.go` |

**What it catches**:
- Broken functionality
- Regression failures
- Edge case violations
- Integration issues

#### Smart Execution: Skip When Irrelevant

All three hooks check conditions before running:

```bash
# Only run on Edit/Write
[[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]] && exit 0

# Only run on specific file types
[[ ! "$FILE_PATH" =~ \.(ts|tsx|js|jsx)$ ]] && exit 0

# Only run if config exists
[[ ! -f "tsconfig.json" ]] && exit 0
```

This prevents wasted execution on README edits, config changes, or non-code files.

#### Performance Considerations

| Project Size | Pipeline Time | Acceptable? |
|--------------|---------------|-------------|
| Small (<100 files) | ~1-2s per edit | ✅ Yes |
| Medium (100-1000 files) | ~2-5s per edit | ✅ Yes (with incremental) |
| Large (1000+ files) | ~5-10s per edit | ⚠️ Consider async or skip tests |

**Optimization strategies**:
1. Use `async: true` for lint/format (cosmetic checks)
2. Keep typecheck sync (errors must block)
3. Skip full test suite, run only changed file's tests
4. Use incremental compilation (`tsc --incremental`)

#### Example Output (Error Case)

```
You: Fix the authentication logic
Claude: [Edits auth.ts]

⚠ TypeScript errors in src/auth.ts:

src/auth.ts:45:12 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.

45   userId: user.id.toString(),
              ~~~~~~~~~~~~~~~~~~~

⚠ Tests failed in src/__tests__/auth.test.ts:

FAIL src/__tests__/auth.test.ts
  ● Authentication › should validate user token
    Expected token to be valid

Fix implementation or update tests.
```

Claude sees these messages immediately and can iterate without manual test runs.

### Example 3: Session Summary Hook

**Event**: `Stop`

Display comprehensive session statistics when Claude Code ends, inspired by Gemini CLI's session summary feature.

#### The Problem

After a long Claude Code session, you might wonder:
- How much time did I spend?
- How many API requests did Claude make?
- Which tools did I use most?
- What did this session cost?

Without session tracking, this information is buried in JSONL files that are hard to parse manually.

#### The Solution

A Stop hook that automatically displays a formatted summary with:
- Session metadata (ID, auto-generated name, git branch)
- Duration breakdown (wall time vs active Claude time)
- Tool usage statistics with success/error counts
- Model usage per model (requests, input/output tokens, cache stats)
- Estimated cost (via ccusage or built-in pricing table)

#### Implementation

**File**: `examples/hooks/bash/session-summary.sh`

**Requirements**:
- `jq` (required for JSON parsing)
- `ccusage` (optional, for accurate cost calculation via Claude Code Usage tool)
- bash 3.2+ (macOS compatible)

**Plugin Install (Recommended)**:

```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
claude plugin install session-summary@florian-claude-tools
```

Hooks are auto-wired for `SessionStart` (RTK baseline) and `SessionEnd` (summary display). No manual configuration needed.

**Manual Configuration** (alternative):

```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/session-summary.sh"
      }]
    }]
  }
}
```

**Environment Variables**:

| Variable | Default | Description |
|----------|---------|-------------|
| `NO_COLOR` | - | Disable ANSI colors |
| `SESSION_SUMMARY_LOG` | `~/.claude/logs` | Override log directory |
| `SESSION_SUMMARY_SKIP` | `0` | Set to `1` to disable summary |

#### Example Output

```
═══ Session Summary ═══════════════════
ID:       abc-123-def-456
Name:     Security hardening v3.26
Branch:   main
Duration: Wall 1h 34m | Active 14m 24s

Tool Calls: 47 (OK 45 / ERR 2)
  Read: 12  Bash: 10  Edit: 8  Write: 6
  Grep: 5   Glob: 4   WebSearch: 2

Model Usage         Reqs    Input    Output
claude-sonnet-4-5     42   493.9K     2.5K
claude-haiku-4-5       5    12.4K       46

Cache: 1.2M read / 45.3K created
Est. Cost: $0.74
═══════════════════════════════════════
```

#### Data Sources

The hook extracts data from two locations:

**1. Session JSONL file** (`~/.claude/projects/{encoded-path}/{session-id}.jsonl`):
- API requests count
- Token usage per model
- Tool calls (extracted from assistant messages)
- Tool errors (from tool_result with is_error: true)
- Turn durations (system messages with subtype: turn_duration)
- Wall time (first to last timestamp)

**2. Sessions index** (`~/.claude/projects/{encoded-path}/sessions-index.json`):
- Session summary (auto-generated by Claude)
- Git branch
- Message count

#### Log File

Session summaries are also logged to `~/.claude/logs/session-summaries.jsonl` for historical analysis:

```json
{
  "timestamp": "2026-02-13T10:30:00Z",
  "session_id": "abc-123-def",
  "session_name": "Security hardening v3.26",
  "git_branch": "main",
  "project": "/path/to/project",
  "duration_wall_ms": 5640000,
  "duration_active_ms": 864000,
  "api_requests": 47,
  "tool_calls": {"Read": 12, "Bash": 10, "Edit": 8},
  "tool_errors": 2,
  "models": {
    "claude-sonnet-4-5-20250929": {
      "requests": 42,
      "input": 493985,
      "output": 2505,
      "cache_read": 1200000,
      "cache_create": 45300
    }
  },
  "total_tokens": {
    "input": 506458,
    "output": 2551,
    "cache_read": 1200000,
    "cache_create": 45300
  },
  "cost_usd": 0.74
}
```

#### Performance

- **Execution time**: <2s for sessions up to 100MB
- **Memory**: Streaming JSONL processing via `jq reduce inputs` (memory-bounded)
- **Impact**: Runs at session end (doesn't block during work)

#### Cost Calculation

**Priority 1**: ccusage tool (accurate, if available)

```bash
ccusage session --id <session-id> --json --offline
```

**Fallback**: Built-in pricing table (as of 2026-02)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| claude-opus-4-6 | $15.00 | $75.00 |
| claude-sonnet-4-5 | $3.00 | $15.00 |
| claude-haiku-4-5 | $0.80 | $4.00 |

#### Edge Cases Handled

- **Empty sessions** (0 API requests): Displays minimal summary
- **Missing JSONL file**: Falls back to sessions-index.json
- **ccusage unavailable**: Uses pricing table fallback
- **No turn_duration entries**: Shows wall time only
- **Very large sessions** (500MB+): Streams with jq (memory safe)

#### Installation

**Plugin system** (recommended):
```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
claude plugin install session-summary@florian-claude-tools
```

**Manual** (alternative):
```bash
# Copy hook
cp examples/hooks/bash/session-summary.sh .claude/hooks/
chmod +x .claude/hooks/session-summary.sh

# Add to settings.json (see Configuration above)

# Test it
echo '{"session_id":"test","cwd":"'$(pwd)'"}' | .claude/hooks/session-summary.sh
```

#### Comparison with Gemini CLI

| Feature | Gemini CLI | Claude Code (with this hook) |
|---------|------------|------------------------------|
| Session summary | ✅ Built-in | ✅ Via hook |
| Duration tracking | ✅ Wall + active | ✅ Wall + active |
| Tool calls breakdown | ✅ Yes | ✅ Yes (with success/error) |
| Model usage | ✅ Requests + tokens | ✅ Requests + tokens + cache |
| Cost estimation | ✅ Yes | ✅ ccusage or pricing table |
| Structured logging | ❌ No | ✅ JSONL for analysis |

---

### Identity Re-injection After Compaction

**The problem**: When Claude compacts context during a long session, agents configured with a specific role — team lead, developer, reviewer — can "forget" their identity. The compacted transcript no longer contains the original system instructions, so the next response drops the role entirely and starts behaving generically.

This is most visible in agent teams with explicit identity prefixes. A developer agent that was consistently marking messages with `🔨 DEVELOPER:` suddenly stops after compaction and starts responding as a generic assistant.

**The pattern**: Store the agent's identity in a file (`.claude/agent-identity.txt`). After each user message, a `UserPromptSubmit` hook checks whether the last assistant response includes the expected identity marker. If not — which happens after compaction — it injects the identity file contents as `additionalContext`. The next response re-establishes the role without human intervention.

```bash
# .claude/agent-identity.txt
# Your agent's identity instructions — anything that should survive compaction

You are the feature team lead. You coordinate the team — you do not write code
and you do not review code.

Prefix every message with the current state:
  SPAWN / PLANNING / DEVELOPING / REVIEWING / COMMITTING / COMPLETE
```

```bash
# .claude/hooks/identity-reinjection.sh
# UserPromptSubmit hook — re-injects identity after compaction

IDENTITY_FILE="${CLAUDE_IDENTITY_FILE:-.claude/agent-identity.txt}"
IDENTITY_MARKER="${CLAUDE_IDENTITY_MARKER:-}"

[[ ! -f "$IDENTITY_FILE" ]] && exit 0

IDENTITY=$(cat "$IDENTITY_FILE")
[[ -z "$IDENTITY" ]] && exit 0

# Default marker: first non-empty line of the identity file
[[ -z "$IDENTITY_MARKER" ]] && IDENTITY_MARKER=$(grep -m1 -v '^#' "$IDENTITY_FILE" | head -c 40)

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

LAST_ASSISTANT=$(jq -r '
    [.[] | select(.role == "assistant")] | last | .content |
    if type == "array" then map(select(.type == "text") | .text) | join("") else . end
' "$TRANSCRIPT_PATH" 2>/dev/null)

# Identity intact: no action
echo "$LAST_ASSISTANT" | grep -qF "$IDENTITY_MARKER" && exit 0

# Identity missing: re-inject
jq -n --arg ctx "[Identity reminder]\n\n$IDENTITY" '{"additionalContext": $ctx}'
exit 0
```

**Configuration** (`settings.json`):

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/identity-reinjection.sh"
      }]
    }]
  }
}
```

**How it behaves**:
- Zero overhead when identity marker is present (exits immediately on match)
- Silent no-op when no `.claude/agent-identity.txt` file exists
- Triggers automatically after compaction — no manual intervention needed
- Works in both solo sessions (long-running agents) and agent team configurations

**Customization**: Set `CLAUDE_IDENTITY_MARKER` in your environment to a short, distinctive string from the agent's standard output (e.g. `"LEAD:"`, `"DEVELOPER:"`, `"🔨"`). If not set, the hook uses the first 40 characters of the identity file as the marker.

> **Full implementation**: [`examples/hooks/bash/identity-reinjection.sh`](../examples/hooks/bash/identity-reinjection.sh)
>
> **Origin**: Pattern sourced from Nick Tune's [hook-driven dev workflows](https://nick-tune.me/blog/2026-02-28-hook-driven-dev-workflows-with-claude-code/) (2026-02-28). The broader article covers state machine workflows with agent teams — see [Agent Teams Workflow](workflows/agent-teams.md) for context.

---

## 7.6 Hook Profiles

**Reading time**: 5 minutes
**Skill level**: Team setup

As your hook collection grows, a tension emerges: some developers want minimal overhead (fast startup, no blocking checks), while security-conscious members or CI pipelines want strict enforcement. A single `settings.json` can't serve both well.

**The pattern**: gate each hook behind an environment variable that declares the desired enforcement level. Three levels cover most teams:

```
minimal   — only critical safety hooks (secrets detection, permission blocks)
standard  — development workflow hooks (format, typecheck, lint)
strict    — full enforcement (governance, compliance, MCP health, quality gates)
```

### Implementation

Each hook checks `ECC_HOOK_PROFILE` before executing:

```bash
#!/bin/bash
# .claude/hooks/format-on-edit.sh
# Runs at: standard or strict only

REQUIRED_LEVEL="${HOOK_REQUIRED_LEVEL:-standard}"
CURRENT_LEVEL="${ECC_HOOK_PROFILE:-standard}"

# Level hierarchy: minimal < standard < strict
level_value() {
  case "$1" in
    minimal)  echo 1 ;;
    standard) echo 2 ;;
    strict)   echo 3 ;;
    *)        echo 2 ;;
  esac
}

REQUIRED_VAL=$(level_value "$REQUIRED_LEVEL")
CURRENT_VAL=$(level_value "$CURRENT_LEVEL")

if [[ "$CURRENT_VAL" -lt "$REQUIRED_VAL" ]]; then
  exit 0  # Skip silently
fi

# Hook logic follows...
```

**Configure per-hook level** in `settings.json` via the environment prefix:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "HOOK_REQUIRED_LEVEL=minimal .claude/hooks/secrets-scan.sh"
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "HOOK_REQUIRED_LEVEL=standard .claude/hooks/format-on-edit.sh"
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "HOOK_REQUIRED_LEVEL=strict .claude/hooks/governance-capture.sh"
        }]
      }
    ]
  }
}
```

**Activate per session** — or export globally in your shell profile:

```bash
# Exploration session — fast startup, minimal checks
export ECC_HOOK_PROFILE=minimal && claude

# Standard developer session (default if unset)
export ECC_HOOK_PROFILE=standard && claude

# Security review, CI/CD, pre-release
export ECC_HOOK_PROFILE=strict && claude
```

Or set per-project in `.envrc` (direnv):

```bash
# .envrc — activated automatically on cd
export ECC_HOOK_PROFILE=strict
```

### When to Use Each Level

| Profile | Use case | Hooks active |
|---------|----------|-------------|
| `minimal` | Exploration, quick prototypes, CI agents | Secrets detection, permission blocks |
| `standard` | Day-to-day development | + format, typecheck, lint, smart-suggest |
| `strict` | Security reviews, pre-release, compliance | + governance, quality gates, MCP health |

### Key Design Rules

- **Security hooks** (`minimal`) should never be gated — hardcode them without the level check
- **Default to `standard`** if `ECC_HOOK_PROFILE` is unset — never default to `minimal` as the fallback
- **Document in CLAUDE.md** which hooks run at which level so teammates aren't surprised

> **Credit**: Hook profile gating pattern from [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) (Affaan Mustafa, Anthropic hackathon winner).

---


