# 10. Reference

_Quick jump:_ [Commands Table](#101-commands-table) · [Keyboard Shortcuts](#102-keyboard-shortcuts) · [Configuration Reference](#103-configuration-reference) · [Troubleshooting](#104-troubleshooting) · [Cheatsheet](#105-cheatsheet) · [Daily Workflow](#106-daily-workflow--checklists)

---

## 📌 Section 10 TL;DR (1 minute)

**What's inside**: Complete command reference, troubleshooting guides, and daily checklists.

### Quick Navigation by Need:

| I need to... | Go to |
|--------------|-------|
| Look up a command | [10.1 Commands Table](#101-commands-table) |
| Find keyboard shortcut | [10.2 Keyboard Shortcuts](#102-keyboard-shortcuts) |
| Configure settings | [10.3 Configuration Reference](#103-configuration-reference) |
| Fix an error | [10.4 Troubleshooting](#104-troubleshooting) |
| Quick daily reference | [10.5 Cheatsheet](#105-cheatsheet) |
| Set up workflow | [10.6 Daily Workflow](#106-daily-workflow--checklists) |
| **Copy ready-to-use templates** | **[examples/ directory](../examples/)** — Commands, hooks, agents |

### Most Common Lookups:
- **Context full?** → [10.4.1 Context Issues](#context-issues)
- **MCP not working?** → [10.4.4 MCP Troubleshooting](#mcp-issues)
- **Need clean reinstall?** → [10.4.3 Full Reinstall](#full-clean-reinstall-procedures)

**Usage tip**: Bookmark this section — you'll reference it often.

---

**Purpose**: Quick lookup for all Claude Code information

## 10.1 Commands Table

### Built-in Commands

| Command | Action | Category |
|---------|--------|----------|
| `/help` | Show all available commands | Navigation |
| `/clear` | Clear conversation history | Session |
| `/compact` | Summarize and compress context | Context |
| `/status` | Show session info (context, cost) | Info |
| `/usage` | Check rate limits and token allocation | Info |
| `/stats` | View usage statistics with activity graphs | Info |
| `/output-style` | **Deprecated** (Oct 2025) — use `/config` → "Preferred output style" instead (Default / Explanatory / Learning) | Display |
| `/feedback` | Report bugs or send feedback to Anthropic | Support |
| `/chrome` | Check Chrome connection, manage permissions | Mode |
| `/config` | View and modify global settings | Config |
| `/copy` | Copy last response to clipboard — interactive picker to select specific code blocks, or "Always copy full response" option (v2.1.59+) | Session |
| `/debug` | Systematic troubleshooting and error investigation | Debug |
| `/doctor` | Run diagnostics and troubleshooting checks | Debug |
| `/execute` | Exit Plan Mode | Mode |
| `/exit` | Exit Claude Code | Session |
| `/fast` | Toggle fast mode (Opus 4.6, 2.5x faster, 6x price) | Mode |
| `/hooks` | Interactive hook configuration | Config |
| `/init` | Generate starter CLAUDE.md based on project structure — ⚠️ output is LLM-generated; review and prune before committing (ETH Zürich research shows auto-generated context files reduce agent task success by ~3% and add 20%+ inference cost) | Config |
| `/login` | Log in to Claude account | Auth |
| `/logout` | Log out and re-authenticate | Auth |
| `/loop [interval] [prompt]` | Run a prompt or slash command on a recurring interval (e.g. `/loop 5m check the deploy`) — v2.1.71+ | Automation |
| `/mcp` | Manage Model Context Protocol servers | Config |
| `/memory` | View and edit auto-memory (context Claude automatically saved across sessions via MEMORY.md) — v2.1.59+ | Config |
| `/mobile` | Show App Store and Google Play download links | Info |
| `/model` | Change model (with left/right arrows for effort slider) | Mode |
| `/permissions` | Configure permission allowlists | Config |
| `/plan` | Enter Plan Mode | Mode |
| `/plugin` | Browse and install Claude Code plugins | Config |
| `/remote-control` (`/rc`) | Start remote control session (Pro/Max only) | Mode |
| `/rename` | Give current session a descriptive name | Session |
| `/resume` | Resume a previous session (from within a session) | Session |
| `/rewind` | Open rewind menu to undo recent changes | Edit |
| `/sandbox` | Enable OS-level isolation | Config |
| `Ctrl+D` | Exit Claude Code | Session |

### Quick Actions

| Action | Shortcut |
|--------|----------|
| Run shell command | `!command` |
| Reference file | `@filename` |
| Cancel operation | `Ctrl+C` |
| Search history | `Ctrl+R` |
| Dismiss suggestion | `Esc` |

## 10.2 Keyboard Shortcuts

### Session Control

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift+Enter` | New line in message |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |
| `Ctrl+R` | Search command history |
| `Ctrl+L` | Clear screen (keeps context) |
| `Ctrl+B` | Run command in background |
| `Esc` | Stop Claude mid-action (context preserved) |
| `Esc×2` (double-tap) | Open rewind menu (same as `/rewind`) |

### Input & Navigation

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Jump to beginning of line |
| `Ctrl+E` | Jump to end of line |
| `Ctrl+W` | Delete previous word |
| `Ctrl+G` | Open plan in external text editor for editing |
| `Tab` | Autocomplete file paths |
| `↑` / `↓` | Navigate command history |

### Mode & Model Toggles

| Shortcut | Action |
|----------|--------|
| `Alt+T` (`Option+T` on macOS) | Toggle thinking mode on/off |
| `Ctrl+O` | View thinking blocks |

### Voice Input

| Shortcut | Action |
|----------|--------|
| `Space` (hold) | Push-to-talk — hold to speak, release to send (default binding) |

**Rebinding**: The `voice:pushToTalk` binding is configurable in `~/.claude/keybindings.json` (v2.1.71+). Add a custom binding if Space conflicts with your workflow:

```json
{
  "voice:pushToTalk": "ctrl+space"
}
```

Toggle voice on/off with `/voice`. The push-to-talk binding only activates when voice mode is active.

### Agent Teams Navigation

| Shortcut | Action |
|----------|--------|
| `Shift+Down` | Cycle through active teammates (in-process mode) |
| `Ctrl+T` | Toggle task list visibility |
| `Enter` | View selected teammate's session |
| `Escape` | Interrupt current turn, return to prompt |

### Useful Flag Combinations

| Flags | Purpose | Example |
|-------|---------|---------|
| `-c -p "msg"` | Resume session + single prompt | `claude -c -p "run tests"` |
| `-r <id> -p` | Resume specific session + prompt | `claude -r abc123 -p "check status"` |
| `-p -p` | Non-interactive automation | `claude -p -p "lint fix" < errors.txt` |

> **Note**: Combine resume flags with `-p` for scripting and CI/CD workflows.

## 10.3 Configuration Reference

### CLAUDE.md Locations

| Location | Scope | Committed |
|----------|-------|-----------|
| `~/.claude/CLAUDE.md` | All projects (global) | N/A |
| `/project/CLAUDE.md` | This project (shared) | ✅ Yes |
| `/project/CLAUDE.local.md` | This project (local overrides) | ❌ No (.gitignored) |
| `/project/.claude/CLAUDE.md` | Personal project config | ❌ No |
| Parent/child directories | Auto-loaded in monorepos | Depends on location |

### Settings Files

| File | Purpose | Committed |
|------|---------|-----------|
| `settings.json` | Hook configuration | ✅ Yes |
| `settings.local.json` | Permission overrides | ❌ No |

### Permission Patterns

| Pattern | Matches |
|---------|---------|
| `Bash(git *)` | Any git command |
| `Bash(npm test)` | Exactly npm test |
| `Edit` | All file edits |
| `Write` | All file writes |
| `WebSearch` | Web search |
| `mcp__serena__*` | All Serena tools |
| `Read(file_path:*.env*)` | Block reading any `.env*` file path |
| `Edit(file_path:*.pem)` | Block editing `.pem` certificates |
| `Bash(command:*rm -rf*)` | Block destructive bash commands |

### CLI Flags Reference

Complete reference for all Claude Code command-line flags, subcommands, and startup environment variables.

#### Session & Context

| Flag | Short | Description |
|------|-------|-------------|
| `--continue` | `-c` | Continue the most recent conversation in the current directory |
| `--resume <ID>` | `-r` | Resume a specific session by UUID or name, or show interactive picker |
| `--from-pr <NUMBER\|URL>` | | Resume sessions linked to a specific GitHub PR |
| `--fork-session` | | Create a new session ID when resuming (use with `--resume` or `--continue`) |
| `--session-id <UUID>` | | Use a specific session UUID |
| `--no-session-persistence` | | Disable session persistence (print mode only) |
| `--remote` | | Create a new web session on claude.ai |
| `--teleport` | | Resume a web session in your local terminal |

#### Model & Configuration

| Flag | Short | Description |
|------|-------|-------------|
| `--model <NAME>` | | Set model with alias (`sonnet`, `opus`, `haiku`) or full model ID |
| `--fallback-model <NAME>` | | Auto-fallback model when default is overloaded (print mode only) |
| `--betas <LIST>` | | Beta headers to include in API requests (API key users only) |

#### Output & Format

| Flag | Short | Description |
|------|-------|-------------|
| `--print` | `-p` | Print response and exit without interactive mode (headless/SDK mode) |
| `--output-format <FORMAT>` | | Output format: `text`, `json`, `stream-json` |
| `--input-format <FORMAT>` | | Input format: `text`, `stream-json` |
| `--json-schema <SCHEMA>` | | Get validated JSON matching schema (print mode only) |
| `--include-partial-messages` | | Include partial streaming events (requires `--print` and `stream-json`) |
| `--verbose` | | Enable verbose logging with full turn-by-turn output |

#### Permissions & Security

| Flag | Short | Description |
|------|-------|-------------|
| `--dangerously-skip-permissions` | | Skip ALL permission prompts — use with extreme caution |
| `--allow-dangerously-skip-permissions` | | Enable permission bypassing as an option without activating it |
| `--permission-mode <MODE>` | | Begin in specified mode: `default`, `plan`, `acceptEdits`, `bypassPermissions` |
| `--allowedTools <TOOLS>` | | Tools that execute without prompting (permission rule syntax) |
| `--disallowedTools <TOOLS>` | | Tools removed from model context entirely |
| `--tools <TOOLS>` | | Restrict which built-in tools Claude can use (use `""` to disable all) |
| `--permission-prompt-tool <TOOL>` | | MCP tool to handle permission prompts in non-interactive mode |

#### System Prompt

| Flag | Short | Description |
|------|-------|-------------|
| `--system-prompt <TEXT>` | | Replace entire system prompt with custom text |
| `--system-prompt-file <PATH>` | | Load system prompt from file, replacing default (print mode only) |
| `--append-system-prompt <TEXT>` | | Append custom text to default system prompt |
| `--append-system-prompt-file <PATH>` | | Append file contents to default prompt (print mode only) |

#### Agent & Subagent

| Flag | Short | Description |
|------|-------|-------------|
| `--agent <NAME>` | | Specify an agent for the current session |
| `--agents <JSON>` | | Define custom subagents dynamically via JSON |
| `--teammate-mode <MODE>` | | Set agent team display: `auto`, `in-process`, `tmux` |

#### MCP & Plugins

| Flag | Short | Description |
|------|-------|-------------|
| `--mcp-config <PATH\|JSON>` | | Load MCP servers from JSON file or inline JSON string |
| `--strict-mcp-config` | | Only use MCP servers from `--mcp-config`, ignore all others |
| `--plugin-dir <PATH>` | | Load plugins from a directory or `.zip` archive for this session only (repeatable). Multiple `--plugin-dir` flags supported. (`.zip` since v2.1.128) |
| `--plugin-url <url>` | | Fetch a plugin `.zip` archive from a URL and load it for the current session. Useful for CI pipelines sharing plugins via artifact storage. (v2.1.129) |

#### Directory & Workspace

| Flag | Short | Description |
|------|-------|-------------|
| `--add-dir <PATH>` | | Add additional working directories for Claude to access |
| `--worktree` | `-w` | Start Claude in an isolated git worktree (branched from HEAD) |

#### Budget & Limits

| Flag | Short | Description |
|------|-------|-------------|
| `--max-budget-usd <AMOUNT>` | | Maximum dollar amount for API calls before stopping (print mode only) |
| `--max-turns <NUMBER>` | | Limit number of agentic turns (print mode only) |

#### Integration

| Flag | Short | Description |
|------|-------|-------------|
| `--chrome` | | Enable Chrome browser integration for web automation |
| `--no-chrome` | | Disable Chrome browser integration for this session |
| `--ide` | | Automatically connect to IDE on startup if exactly one valid IDE is available |
| `--channels` | | Enable MCP channels (Research Preview). Supports claude.ai OAuth and API key auth. Managed orgs require `channelsEnabled: true` in managed-settings. (v2.1.128) |

#### Initialization & Maintenance

| Flag | Short | Description |
|------|-------|-------------|
| `--init` | | Run initialization hooks and start interactive mode |
| `--init-only` | | Run initialization hooks and exit without starting a session |
| `--maintenance` | | Run maintenance hooks and exit |

#### Debug & Diagnostics

| Flag | Short | Description |
|------|-------|-------------|
| `--debug <CATEGORIES>` | | Enable debug mode with optional category filtering (e.g., `"api,hooks"`) |

#### Settings Override

| Flag | Short | Description |
|------|-------|-------------|
| `--settings <PATH\|JSON>` | | Path to settings JSON file or inline JSON string to load |
| `--setting-sources <LIST>` | | Comma-separated sources to load: `user`, `project`, `local` |
| `--disable-slash-commands` | | Disable all skills and slash commands for this session |

#### Version & Help

| Flag | Short | Description |
|------|-------|-------------|
| `--version` | `-v` | Output the current version number |
| `--help` | `-h` | Show help information |

### Subcommands

Top-level commands run as `claude <subcommand>`:

| Subcommand | Description |
|------------|-------------|
| `claude "query"` | Start REPL with an initial prompt |
| `claude agents` | Open Agent View — list all sessions (running / waiting / done) with peek and inline reply (v2.1.139+) |
| `claude auth login / logout / status` | Manage Claude Code authentication |
| `claude doctor` | Run diagnostics from the command line |
| `claude install` | Install or switch Claude Code native builds |
| `claude mcp add / remove / list / get / enable` | Configure MCP servers |
| `claude plugin` | Manage Claude Code plugins |
| `claude remote-control` | Manage remote control sessions |
| `claude setup-token` | Create a long-lived token for subscription usage |
| `claude update` / `claude upgrade` | Update to the latest version |
| `claude project purge [path]` | Delete all Claude Code state for a project: transcripts, tasks, file history, config entry. Options: `--dry-run`, `-y/--yes`, `-i/--interactive`, `--all`. (v2.1.126) |
| `claude ultrareview [target]` | Run `/ultrareview` non-interactively from CI/scripts. `target`: PR number, branch, or current branch if omitted. `--json` for machine-readable output. Exits 0 on completion, 1 on failure. (v2.1.120) |
| `claude plugin prune` | Remove orphaned auto-installed plugin dependencies. Cascade with `claude plugin uninstall --prune`. (v2.1.121) |
| `claude plugin details <name>` | Show plugin component inventory (skills, agents, commands, hooks, MCP servers) and projected per-session token cost. (v2.1.139) |

### Startup Environment Variables

Set these in your shell before launching Claude Code (these cannot be configured via `settings.json`):

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | Enable experimental agent teams |
| `CLAUDE_CODE_TMPDIR` | Override temp directory for internal files |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` | Enable additional directory CLAUDE.md loading |
| `DISABLE_AUTOUPDATER=1` | Disable automatic updates |
| `CLAUDE_CODE_EFFORT_LEVEL` | Control thinking depth for extended thinking models |
| `USE_BUILTIN_RIPGREP=0` | Use system ripgrep instead of built-in (useful on Alpine Linux) |
| `CLAUDE_CODE_SIMPLE` | Enable simple mode (Bash + Edit tools only, no agents/hooks/MCP) |
| `CLAUDE_BASH_NO_LOGIN=1` | Skip login shell invocation for BashTool |
| `CLAUDE_CODE_SESSION_ID` | Unique identifier for the current Claude Code session. Passed to all Bash tool subprocess environments. Matches `session_id` in hook stdin JSON. Use for correlating tool output with sessions in observability pipelines. (v2.1.132) |
| `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` | Opt out of the fullscreen alternate-screen renderer. Terminal output stays in the native scrollback buffer instead of the alternate screen. Use in environments that don't support alternate screen (some log-capture setups, embedded terminals). (v2.1.132) |
| `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` | When set, Homebrew or WinGet auto-upgrades Claude Code in the background and prompts to restart when a new version is available. (v2.1.129) |

For variables configurable via the `"env"` key in `settings.json` (including `MAX_THINKING_TOKENS`, `CLAUDE_CODE_SHELL`, `CLAUDE_CODE_ENABLE_TASKS`, `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, and more), see section 10.3 Configuration Reference.

**Common Combinations:**

```bash
# CI/CD mode - non-interactive with auto-accept
claude -p "fix linting errors" --dangerously-skip-permissions

# JSON output for scripting
claude -p "analyze code quality" --output-format json

# Economic analysis with Haiku
claude -p "review this file" --model haiku

# Allow access to a directory outside CWD
claude --add-dir ./src/components

# Plan mode for safety
claude --permission-mode plan

# Multi-directory project
claude --add-dir ../shared-lib ../utils ../config

# Limit agentic turns in automation
claude -p "refactor this module" --max-turns 10

# Resume specific session non-interactively
claude -r abc123 -p "summarize progress"
```

**Safety Guidelines:**

| Flag | Risk Level | Use When |
|------|-----------|----------|
| `--dangerously-skip-permissions` | High | Only in CI/CD, never on production |
| `--allowedTools` | Safe | Restricting tool access |
| `--disallowedTools` | Safe | Blocking specific tools |
| `--permission-mode plan` | Safe | Read-only exploration |
| `--debug` | Medium | Troubleshooting (verbose logs) |

## 10.4 Troubleshooting

> **Interactive Troubleshooting**: Use the `/diagnose` command for guided, interactive problem-solving. It auto-scans your environment and provides targeted solutions. See [examples/commands/diagnose.md](../examples/commands/diagnose.md).

### Quick Diagnostic Guide

Use this symptom-based guide for rapid issue identification and resolution:

| Symptom | Likely Cause | Quick Fix | Prevention |
|---------|--------------|-----------|------------|
| "Context too long" error | Session accumulated too much context | `/compact` first, then `/clear` if needed | Compact regularly at 70% |
| Slow/delayed responses | High context usage (>75%) | Check `/status`, run `/compact` | Monitor context with `/status` |
| "Rate limit exceeded" | API throttling from frequent requests | Wait 2 minutes, use `--model haiku` for simple tasks, or use [cc-copilot-bridge](https://github.com/FlorianBruniaux/cc-copilot-bridge) for flat-rate access | Batch operations, use `/compact`, consider Copilot Pro |
| Claude forgets instructions | Context overflow, CLAUDE.md lost | Create checkpoint, `/clear`, reload CLAUDE.md | Keep CLAUDE.md concise (<500 lines) |
| MCP server not connecting | Server crashed or config error | `claude mcp list`, check paths, restart server | Test servers after config changes |
| Permission prompts every time | Tool not in `allowedTools` | Add pattern to `settings.json` allowedTools | Use wildcards: `Bash(git *)` |
| Changes not taking effect | Cached configuration | Restart Claude Code session | Use `/exit` before config changes |
| Session won't resume | Corrupted session file | Start fresh with `/clear` | Exit cleanly with `/exit` or `Ctrl+D` |

**Quick Diagnosis Flow:**
1. Check context: `/status` → If >70%, run `/compact`
2. Check connectivity: Try simple command → If fails, check network
3. Check configuration: `claude mcp list` → Verify MCP servers
4. Check permissions: Review error message → Add to allowedTools if needed
5. Still failing: `/doctor` → Run diagnostics and verify system health

### Common Issues Reference

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Context too long" | Used 100% context | `/clear` or `/compact` |
| Slow responses | High context usage | `/compact` |
| "Permission denied" | Security settings | Check `settings.local.json` |
| Hook not running | Registration error | Check `settings.json` matcher |
| MCP tool not found | Server not running | Check `mcp.json` config |
| Agent not found | File naming | Check `.claude/agents/` |
| Command not found | Path error | Check `.claude/commands/` |
| Unexpected API charges despite active subscription | `ANTHROPIC_API_KEY` set in shell or `.env` bypasses subscription | Run `echo $ANTHROPIC_API_KEY` — if it returns a value, Claude Code is billing at API rates. Unset it from your shell profile to restore subscription billing. Run `claude /cost` to check spend in the current session. |

### Context Recovery

| Context Level | Recommended Action |
|---------------|-------------------|
| 0-50% | Continue normally |
| 50-75% | Be more specific in queries |
| 75-90% | Use `/compact` |
| 90%+ | Use `/clear` |

### Common Errors

**"Tool execution failed"**
- Check tool permissions in `settings.local.json`
- Verify command syntax
- Check for missing dependencies

**"Agent not available"**
- Verify agent file exists in `.claude/agents/`
- Check YAML frontmatter syntax
- Restart Claude Code session

**"Hook blocked operation"**
- Check hook exit code (2 = blocked)
- Review hook error message
- Adjust hook rules if needed

**"Unexpected API charges despite subscription"**
- Run `echo $ANTHROPIC_API_KEY` in your shell — any output means Claude Code is routing via API billing, not your subscription
- Remove the key from `~/.zshrc`, `~/.bashrc`, or `.env` files if subscription billing is intended
- Use `claude /cost` (or `/usage` since v2.1.118) to check real-time spend in the current session
- Use `npx ccusage` to review cross-session historical spend
- See [§9.13 — The Interactive/Programmatic Billing Split](#the-interactiveprogrammatic-billing-split-effective-june-15-2026) for the full billing model and June 15 changes

### MCP Server Issues

**Common MCP Errors and Solutions**

#### Error 1: Tool Name Validation Failed

```
API Error 400: "tools.11.custom.name: String should match pattern '^[a-zA-Z0-9_-]{1,64}'"
```

**Cause**: MCP server name contains invalid characters.

**Solution**:
- Server names must only contain: letters, numbers, underscores, hyphens
- Maximum 64 characters
- No special characters or spaces

**Example:**
```bash
# ❌ Wrong
claude mcp add my-server@v1 -- npx server

# ✅ Correct
claude mcp add my-server-v1 -- npx server
```

#### Error 2: MCP Server Not Found

```
MCP server 'my-server' not found
```

**Cause**: Server not properly registered or wrong scope.

**Solution**:
1. Check scope settings (local/user/project)
   ```bash
   claude mcp list  # Verify server is listed
   ```
2. Ensure you're in the correct directory for local scope
3. Restart Claude Code session
4. Re-add server if needed:
   ```bash
   claude mcp add my-server -s user -- npx @my/server
   ```

#### Error 3: Windows Path Issues

```
Error: Cannot find module 'C:UsersusernameDocuments'
```

**Cause**: Backslashes in Windows paths not properly escaped.

**Solution**:
```bash
# ❌ Wrong
claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem C:\Users\username\Documents

# ✅ Correct - Use forward slashes
claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem C:/Users/username/Documents

# ✅ Correct - Escape backslashes
claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem "C:\\Users\\username\\Documents"
```

#### MCP Debugging Techniques

**Enable Debug Mode:**
```bash
# Debug all MCP connections
claude --mcp-debug

# View MCP status inside Claude Code
/mcp
```

**View Log Files:**
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Linux
tail -f ~/.local/share/claude/logs/mcp*.log

# Windows (PowerShell)
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Wait -Tail 50
```

**Manual Server Test:**
```bash
# Test if server works standalone
npx -y @modelcontextprotocol/server-filesystem ~/Documents

# Expected: Server should start and output JSON-RPC messages
# If it crashes immediately, check server logs
```

**Quick Diagnostic Commands:**
```bash
# List all configured servers
claude mcp list

# Test specific server
claude --mcp-debug -p "List available tools"

# Remove and re-add server
claude mcp remove my-server
claude mcp add my-server -s user -- npx @my/server
```

**Connection Failed: Common Causes**

| Error | Cause | Solution |
|-------|-------|----------|
| `ECONNREFUSED` | Server not running | Check `mcp.json` command is correct |
| `Timeout after 30s` | Slow initialization | Increase timeout or check server logs |
| `Module not found` | Missing dependencies | Run `npm install` in server directory |
| `Permission denied` | File access | Check file permissions on server executable |
| `ENOENT` | Server binary not found | Verify npx/npm is in PATH |
| `Invalid JSON` | Server output malformed | Check server version compatibility |

**Serena MCP specific issues:**

```bash
# Index not found
serena list-memories
# If empty, re-index:
# In your project, ask Claude: "Index this project with Serena"

# Session not persisting
# Check mcp.json has correct data directory:
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@serenaai/serena-mcp"],
      "env": {
        "SERENA_DATA_DIR": "/absolute/path/to/.serena"
      }
    }
  }
}
```

**Context7 MCP issues:**

```bash
# Documentation not found
# Ensure you're searching for official libraries:
# ✅ "React useState documentation"
# ❌ "my-custom-lib documentation" (not in Context7)

# Slow lookups
# Context7 fetches from official docs - network dependent
# Check your internet connection
```

**Sequential Thinking MCP issues:**

```bash
# "Sequential not responding"
# Sequential uses significant compute - expect 10-30s responses
# Not an error, just be patient

# Quality seems off
# Sequential works best with specific, well-defined problems
# ✅ "Debug why user authentication fails on mobile"
# ❌ "Make the app better"
```

### Permission Issues

**Pattern matching problems:**

```json
// ❌ Wrong - too specific
{
  "allowedTools": ["Bash(npm test)"]
}
// This ONLY allows exactly "npm test"

// ✅ Right - use wildcards
{
  "allowedTools": ["Bash(npm *)"]
}
// This allows any npm command
```

**Common permission patterns:**

```json
{
  "allowedTools": [
    "Bash(git *)",           // All git commands
    "Bash(npm *)",           // All npm commands
    "Bash(pytest *)",        // All pytest commands
    "Edit",                  // All file edits
    "Write",                 // All file writes
    "Read",                  // All file reads
    "mcp__serena__*",        // All Serena tools
    "mcp__context7__*",      // All Context7 tools
    "Task"                   // Allow agent delegation
  ]
}
```

### Timeout Issues

**Claude stops responding mid-task:**

Possible causes:

1. **Network interruption** - Check your internet connection
2. **API rate limit** - Wait 1-2 minutes and retry
3. **Context exhausted** - Use `/compact` or `/clear`
4. **Long-running operation** - Some MCP operations take 30s+

**Workaround for long operations:**

```bash
# Instead of:
"Analyze all 500 files in the codebase"

# Break into chunks:
"Analyze files in /src/components/ first"
"Now analyze /src/utils/"
"Finally analyze /src/services/"
```

### Installation Issues

**Windows-specific problems:**

```powershell
# npm global install fails
# Run PowerShell as Administrator
npm install -g @anthropic-ai/claude-code

# PATH not updated
# Manually add to PATH:
$env:Path += ";$env:APPDATA\npm"

# Permission errors
# Check antivirus isn't blocking Node.js
```

**macOS-specific problems:**

```bash
# "Command not found" after install
# Check shell config loaded:
source ~/.zshrc  # or ~/.bashrc

# Permission denied on /usr/local
# Don't use sudo with npm
# Fix permissions:
sudo chown -R $(whoami) /usr/local

# curl install blocked
# Check firewall/VPN settings
```

**Linux-specific problems:**

```bash
# npm not found
# Install Node.js first:
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Global install permission issues
# Configure npm to use home directory:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### One-Shot Health Check Scripts

Diagnostic scripts for instant troubleshooting. Get them from:
- Windows: [`examples/scripts/check-claude.ps1`](../examples/scripts/check-claude.ps1)
- macOS/Linux: [`examples/scripts/check-claude.sh`](../examples/scripts/check-claude.sh)
- Bridge health: `python examples/scripts/bridge.py --health` (LM Studio connectivity)

### Full Clean Reinstall Procedures

⚠️ **Nuclear option for corrupted installations.** Use when all else fails.

Get the scripts from:
- Windows: [`examples/scripts/clean-reinstall-claude.ps1`](../examples/scripts/clean-reinstall-claude.ps1)
- macOS/Linux: [`examples/scripts/clean-reinstall-claude.sh`](../examples/scripts/clean-reinstall-claude.sh)

**When to use clean reinstall:**
- Mysterious errors that persist after normal troubleshooting
- Corrupted configuration files
- Breaking changes after Claude Code updates
- Migration to new machine (export/import workflow)

**What gets deleted:**
- ✓ Claude Code binary and npm packages
- ✓ Downloaded models and cache
- ✓ Local session data
- ⚠️ Config file (optional - backed up by default)

**What survives:**
- ✓ Project-level `.claude/` folders
- ✓ Project `CLAUDE.md` files
- ✓ Custom agents, skills, commands, hooks (in projects)
- ✓ MCP server configurations (in `mcp.json`)

## 10.5 Cheatsheet

### One-Page Quick Reference

```
╔══════════════════════════════════════════════════════════╗
║                 CLAUDE CODE CHEATSHEET                   ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  ESSENTIAL COMMANDS                                      ║
║  ─────────────────                                       ║
║  /help      Show commands     /clear    Fresh start      ║
║  /status    Session info      /compact  Save context     ║
║  /plan      Safe mode         /rewind   Undo changes     ║
║  /exit      Quit              Ctrl+C    Cancel           ║
║                                                          ║
║  QUICK ACTIONS                                           ║
║  ─────────────                                           ║
║  !command   Run shell         @file     Reference file   ║
║  Ctrl+R     Search            ↑/↓       History          ║
║                                                          ║
║  CONTEXT MANAGEMENT                                      ║
║  ──────────────────                                      ║
║  🟢 0-50%   Work freely                                  ║
║  🟡 50-75%  Be selective                                 ║
║  🔴 75-90%  /compact now                                 ║
║  ⚫ 90%+    /clear required                              ║
║                                                          ║
║  PERMISSION MODES                                        ║
║  ────────────────                                         ║
║  Default     Ask before changes                           ║
║  Auto-accept Execute without asking                       ║
║  Plan Mode   Read-only exploration                        ║
║                                                           ║
║  CONFIGURATION                                            ║
║  ─────────────                                            ║
║  ~/.claude/CLAUDE.md         Global settings              ║
║  /project/CLAUDE.md          Project settings             ║
║  .claude/settings.json       Hooks config                 ║
║  .claude/settings.local.json Permission overrides         ║
║                                                           ║
║  .claude/ FOLDER                                          ║
║  ───────────────                                          ║
║  agents/    Custom agents     commands/  Slash commands   ║
║  hooks/     Event scripts     rules/     Auto-load rules  ║
║  skills/    Knowledge modules                             ║
║                                                           ║
║  THINKING MODE (Opus 4.5/4.6: adaptive depth in 4.6)      ║
║  ─────────────────────────────────────────                ║
║  Alt+T          Toggle on/off   Current session           ║
║  /config        Global setting  Persists across sessions  ║
║  Note: "ultrathink" keywords are now cosmetic only        ║
║                                                           ║
║  MCP SERVERS                                              ║
║  ───────────                                              ║
║  Serena       Semantic code analysis                      ║
║  Context7     Library documentation                       ║
║  Sequential   Structured reasoning                        ║
║  Postgres     Database queries                            ║
║  Playwright   Browser automation                          ║
║                                                           ║
║  HOOKS (events)                                           ║
║  ──────────────                                           ║
║  PreToolUse       Before tool (security)                  ║
║  PostToolUse      After tool (format, log)                ║
║  UserPromptSubmit On message (enrich context)             ║
║                                                           ║
║  WORKFLOW                                                 ║
║  ────────                                                 ║
║  Describe → Analyze → Review → Accept/Reject → Verify     ║
║                                                           ║
║  BEST PRACTICE: Always read the diff before accepting!    ║
║                                                           ║
╚══════════════════════════════════════════════════════════╝
```

## 10.6 Daily Workflow & Checklists

### Daily Workflow Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MORNING (Setup)                                            │
│  ───────────────                                            │
│  □ Git pull latest changes                                  │
│  □ Review context with /status                              │
│  □ Load project memory (/sc:load if using Serena)           │
│  □ Review yesterday's progress                              │
│                                                             │
│  WORK SESSION                                               │
│  ────────────                                               │
│  □ Define task clearly before starting                      │
│  □ Use TodoWrite for multi-step work                        │
│  □ Commit after each completed task                         │
│  □ /compact when context >70%                               │
│  □ Take breaks every 90 minutes                             │
│                                                             │
│  END OF DAY                                                 │
│  ──────────                                                 │
│  □ Commit all work in progress                              │
│  □ Save session (/sc:save)                                  │
│  □ Note blockers or next steps                              │
│  □ Push to remote                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```


### Prompt Quality Checklist

Use this before sending complex requests:

```
□ WHAT: Clear deliverable described?
□ WHERE: File paths/locations specified?
□ HOW: Constraints/approach mentioned?
□ WHY: Context for decision-making?
□ VERIFY: Success criteria defined?
```

**Example applying checklist:**

```
❌ Vague: "Add user authentication"

✅ Complete:
"Add JWT authentication to the /api/login endpoint.
- WHERE: src/api/auth/login.ts
- HOW: Use jsonwebtoken library (already in deps),
       bcrypt for password comparison
- CONSTRAINTS: Token expires in 24h, include userId and role
- VERIFY: Test with wrong password, expired token, invalid token"
```

---

# Appendix: Templates Collection

> **💡 Production-Ready Examples**: For complete, battle-tested templates including advanced commands (`/pr`, `/release-notes`, `/sonarqube`) and security hooks, see the [`examples/`](../examples/) directory. The templates below are minimal starting points.

## A.1 Agent Template

```markdown
---
name: your-agent-name
description: Use this agent when [specific trigger]
model: sonnet
tools: Read, Write, Edit, Bash, Grep, Glob
skills: []
---

# Agent Name

## Role Definition
You are an expert in [domain].

## Activation Triggers
Use this agent when:
- [Trigger 1]
- [Trigger 2]

## Methodology
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format
[Expected deliverables]

## Examples
[Concrete usage examples]
```

## A.2 Skill Template

```markdown
---
name: skill-name
description: Expert guidance for [domain]
allowed-tools: Read Grep Bash
argument-hint: "[--option] <required_arg>"   # if the skill accepts $ARGUMENTS
---

# Skill Name

## Expertise Areas
- [Area 1]
- [Area 2]

## Methodology
1. [Step 1]
2. [Step 2]

## Checklists
- [ ] [Check 1]
- [ ] [Check 2]

## Examples
[Good and bad patterns]
```

## A.3 Command Template

```markdown
---
description: Brief description of what this command does
argument-hint: "<first_arg> [second_arg] [--flag]"
---
# Command Name

## Purpose
[What this command does]

## Process
1. **Step 1**: [Instructions]
2. **Step 2**: [Instructions]

## Arguments
- $ARGUMENTS[0] (or $0): First argument - [How to handle]
- $ARGUMENTS[1] (or $1): Second argument - [How to handle]

## Output Format
[Expected output]
```

## A.4 Hook Templates

### PreToolUse (Security)

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Block dangerous patterns
[[ "$COMMAND" =~ "dangerous-pattern" ]] && { echo "BLOCKED" >&2; exit 2; }

exit 0
```

### PostToolUse (Formatting)

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Auto-format
[[ "$FILE_PATH" =~ \.(ts|tsx)$ ]] && npx prettier --write "$FILE_PATH" 2>/dev/null

exit 0
```

### UserPromptSubmit (Context)

```bash
#!/bin/bash
CONTEXT="[Custom context here]"
cat << EOF
{"hookSpecificOutput":{"additionalContext":"$CONTEXT"}}
EOF
exit 0
```

## A.5 settings.json Template

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": ".claude/hooks/security.sh", "timeout": 5000}]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": ".claude/hooks/format.sh"}]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [{"type": "command", "command": ".claude/hooks/context.sh"}]
      }
    ]
  }
}
```

## A.6 settings.local.json Template

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm test)",
      "Bash(pnpm *)",
      "Edit",
      "Write"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ],
    "ask": [
      "Bash(npm publish)",
      "Bash(git push --force)"
    ]
  }
}
```

## A.7 CLAUDE.md Template

```markdown
# Project Name

## Tech Stack
- [Technology 1]
- [Technology 2]

## Code Conventions
- [Convention 1]
- [Convention 2]

## Architecture
- [Pattern 1]
- [Pattern 2]

## Commands
- `npm run dev` - Start development
- `npm test` - Run tests
```

---


