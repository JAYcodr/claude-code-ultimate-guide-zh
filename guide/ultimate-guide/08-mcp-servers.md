# 8. MCP Servers

_Quick jump:_ [What is MCP](#81-what-is-mcp) · [Available Servers](#82-available-servers) · [Configuration](#83-configuration) · [Server Selection Guide](#84-server-selection-guide) · [Plugin System](#85-plugin-system) · [MCP Security](#86-mcp-security)

---

**Reading time**: 15 minutes
**Skill level**: Week 2-3
**Goal**: Extend Claude Code with external tools

## 8.1 What is MCP

MCP (Model Context Protocol) is a standard for connecting AI models to external tools and data sources.

### Why MCP?

| Without MCP | With MCP |
|-------------|----------|
| Limited to built-in tools | Extensible tool ecosystem |
| Claude guesses about external data | Claude queries real data |
| Generic code understanding | Deep semantic analysis |

### How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐                                       │
│   │ Claude Code │                                       │
│   └──────┬──────┘                                       │
│          │                                              │
│          ▼                                              │
│   ┌─────────────────────────────────────────────┐       │
│   │               MCP Protocol                  │       │
│   └──────────────────────┬──────────────────────┘       │
│                          │                              │
│          ┌───────────────┼───────────────┐              │
│          ▼               ▼               ▼              │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐         │
│   │  Serena   │   │ Context7  │   │ Postgres  │         │
│   │(Semantic) │   │  (Docs)   │   │(Database) │         │
│   └───────────┘   └───────────┘   └───────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### MCP Evolution: Apps Extension (SEP-1865)

> **🆕 Since January 2026**: MCP can now deliver interactive UIs alongside traditional text responses.

#### The Context Gap Problem

Traditional AI interactions require repeated prompts for data exploration:

**Without MCP Apps**:
```
You: "Show me customer data"
Claude: "Here are 500 customers [text list]"
You: "Sort by revenue"
Claude: "Here's the sorted list [text]"
You: "Filter to last 30 days"
Claude: "Here's the filtered list [text]"
You: "Show me the top 10"
... (multiple prompt cycles)
```

**With MCP Apps**:
```
You: "Show me customer data"
Claude: [Renders interactive dashboard with sorting, filtering, date pickers]
You: [Sort, filter, drill-down directly in UI - no additional prompts]
```

#### What Are MCP Apps?

MCP Apps enable MCP servers to deliver **interactive interfaces** that render directly in your conversation:

- **Dashboards**: Charts with filtering, drill-down, export
- **Configuration wizards**: Forms with dependent fields and validation
- **Document viewers**: PDFs with inline highlights and annotations
- **Real-time monitors**: Live metrics updating without re-running tools

#### Available Interactive Tools

**At launch** (January 26, 2026), **9 interactive tools** are available:

| Tool | What It Does |
|------|--------------|
| **Asana** | Create project timelines, manage tasks visible to teams |
| **Slack** | Draft formatted messages with preview before posting |
| **Figma** | Convert text into flowcharts, Gantt charts in FigJam |
| **Amplitude** | Build analytics charts, explore trends interactively |
| **Box** | Search files, preview documents inline |
| **Canva** | Create presentations with real-time design customization |
| **Clay** | Research companies, find contacts, draft outreach |
| **Hex** | Query data with interactive charts and tables |
| **monday.com** | Manage work, update boards, visualize progress |

**Coming soon**: Salesforce (Agentforce 360), Claude Cowork integration

→ **Access**: [claude.ai/directory](https://claude.ai/directory) (Pro/Max/Team/Enterprise plans)

#### Platform Support

| Platform | Support | How to Use |
|----------|---------|------------|
| **Claude Desktop** | ✅ Now | claude.ai/directory - connect interactive tools |
| **Claude Cowork** | 🔄 Coming | Agentic workflows with file/project access |
| **VS Code** | ✅ Insiders | Install Insiders build, configure MCP Apps |
| **ChatGPT** | 🔄 Rollout | Week of Jan 26, 2026 |
| **Goose** | ✅ Now | Open-source alternative with UI support |
| **Claude Code CLI** | ❌ No | Terminal is text-only (no UI rendering) |

#### Why This Matters for CLI Users

**Direct impact**: **None** - Claude Code CLI cannot render interactive UIs in the terminal.

**Indirect benefits**:

1. **Ecosystem awareness**: Understand where MCP is heading (interactive agentic workflows)
2. **Hybrid workflows**: Use Claude Desktop for visual exploration → Claude Code CLI for automation
3. **MCP server development**: If building custom servers, Apps is now an option
4. **Context for tools**: Some MCP servers may advertise UI capabilities (visible in metadata)

**Example hybrid workflow**:
```
1. Claude Desktop: Use Amplitude MCP App to explore analytics interactively
2. Identify patterns visually (e.g., "EU region shows 30% growth")
3. Claude Code CLI: Automate data export and reporting based on findings
```

#### Technical Foundation

MCP Apps is built on the **Model Context Protocol** (open standard by Anthropic):

- **Open specification**: [SEP-1865 on GitHub](https://github.com/modelcontextprotocol/ext-apps)
- **Co-authored by**: OpenAI, Anthropic, MCP-UI creators
- **SDK**: `@modelcontextprotocol/ext-apps` (npm)
- **"Build once, deploy everywhere"**: Works in Claude, VS Code, ChatGPT, Goose

→ **Deep dive**: See [guide/architecture.md:656](./core/architecture.md#mcp-extensions-apps-sep-1865) for technical architecture, security model, and SDK details.

#### Resources

- **MCP Apps blog post**: [Anthropic announcement](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)
- **Interactive tools blog**: [Claude announcement](https://claude.com/blog/interactive-tools-in-claude)
- **Official spec**: [SEP-1865 on GitHub](https://github.com/modelcontextprotocol/ext-apps)

---

## 8.2 Available Servers

<details>
<summary><b>MCP Server Catalog (click to expand)</b></summary>

### Serena (Semantic Code Analysis)

**Purpose**: Deep code understanding through semantic analysis, indexing, and persistent memory.

**Why Serena matters**: Claude Code has no built-in indexation (unlike Cursor). Serena fills this gap by indexing your codebase for faster, smarter searches. It also provides **session memory** — context that persists across conversations.

**Key Features**:

| Feature | Description |
|---------|-------------|
| **Indexation** | Pre-indexes your codebase for efficient symbol lookup |
| **Project Memory** | Stores context in `.serena/memories/` between sessions |
| **Onboarding** | Auto-analyzes project structure on first run |

**Tools**:

| Tool | Description |
|------|-------------|
| `find_symbol` | Find functions, classes, methods by name |
| `get_symbols_overview` | Get file structure overview |
| `search_for_pattern` | Regex search across codebase |
| `find_referencing_symbols` | Find all usages of a symbol |
| `replace_symbol_body` | Replace function/class body |
| `write_memory` | Save context for future sessions |
| `read_memory` | Retrieve saved context |
| `list_memories` | List all stored memories |

**Session Memory Workflow**:

```
# Start of session
list_memories() → See what context exists
read_memory("auth_architecture") → Load relevant context

# During work
write_memory("api_refactor_plan", "...") → Save decisions for later

# End of session
write_memory("session_summary", "...") → Persist progress
```

**Setup**:

```bash
# Basic indexation (first run)
uvx --from git+https://github.com/oraios/serena serena project index

# Force full rebuild (if index is corrupted or outdated)
uvx --from git+https://github.com/oraios/serena serena project index --force-full

# Incremental indexation (faster after initial index)
uvx --from git+https://github.com/oraios/serena serena project index --incremental

# Parallel processing (recommended: 50-75% of CPU cores)
uvx --from git+https://github.com/oraios/serena serena project index --parallel 4

# Verbose mode (see progress details)
uvx --from git+https://github.com/oraios/serena serena project index --verbose --force-full

# View all options
uvx --from git+https://github.com/oraios/serena serena project index --help
```

**Indexation Options**:

| Option | Description | Use When |
|--------|-------------|----------|
| `--force-full` | Complete rebuild of index | Corrupted index, major codebase changes |
| `--incremental` | Update only changed files | Regular maintenance after initial index |
| `--parallel N` | Use N CPU cores | Large codebases (use 50-75% of cores) |
| `--verbose` | Show detailed progress | Debugging indexation issues |

**Cache Location**: Index stored in `.serena/cache/typescript/` (add to `.gitignore`)

**Important Notes**:
- **Deprecated command**: `serena index-project` → Use `serena project index` instead
- **First run**: Use basic `serena project index` (auto-detects full rebuild)
- **Regular updates**: Use `--incremental` for faster re-indexation
- **Performance**: `--parallel 4` on 8-core machine = ~60% faster indexation

> **Sources**: [Serena Docs](https://oraios.github.io/serena/02-usage/020_running.html) • [GitHub Issues](https://github.com/oraios/serena/issues/372) • [Optimization Guide](https://smartscope.blog/en/ai-development/serena-mcp-project-indexing-optimization/)

**Use when**:
- Navigating large codebases (>10k lines)
- Need context to persist across sessions
- Understanding symbol relationships
- Refactoring across files

> **Source**: [Serena GitHub](https://github.com/oraios/serena)

### grepai (Recommended Semantic Search)

**Purpose**: Privacy-first semantic code search with call graph analysis.

**Why grepai is recommended**: It's **fully open-source**, runs entirely locally using Ollama embeddings (no cloud/privacy concerns), and offers **call graph analysis** — trace who calls what function and visualize dependencies. This combination makes it the best choice for most semantic search needs.

**Key Features**:

| Feature | Description |
|---------|-------------|
| **Semantic search** | Find code by natural language description |
| **Call graph** | Trace callers, callees, and full dependency graphs |
| **Privacy-first** | Uses Ollama locally (no cloud) |
| **Background indexing** | `grepai watch` daemon keeps index fresh |

**Example**:

```bash
# Semantic search (finds code by meaning, not exact text)
grepai search "user authentication flow"

# Who calls this function?
grepai trace callers "createSession"
# → Lists all 23 files that call createSession with context

# What does this function call?
grepai trace callees "SessionProvider"

# Full dependency graph
grepai trace graph "createSession" --depth 3
```

**MCP Tools Available**:

| Tool | Description |
|------|-------------|
| `grepai_search` | Natural language semantic search |
| `grepai_trace_callers` | Find all callers of a function |
| `grepai_trace_callees` | Find all functions called by a function |
| `grepai_trace_graph` | Generate call graph |
| `grepai_index_status` | Check indexation status |

**Setup**:

```bash
# 1. Install Ollama and embedding model
brew install ollama
brew services start ollama
ollama pull nomic-embed-text

# 2. Install grepai
curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh

# 3. Initialize in your project
cd your-project
grepai init  # Choose: ollama, nomic-embed-text, gob

# 4. Start indexing daemon
grepai watch &
```

**Combined Workflow with Serena**:

```
1. grepai search "payment validation"     → Discover relevant files
2. Serena get_symbols_overview            → Understand file structure
3. grepai trace callers "validatePayment" → See all dependencies
4. Serena find_symbol + replace_symbol_body → Precise editing
```

**Use when**:
- Exploring unfamiliar codebases by intent
- Understanding call dependencies before refactoring
- Privacy is required (no cloud, all local)
- Need to trace "who calls what" across the codebase

**Performance vs Traditional Tools**:

| Search Type | Tool | Time | Results |
|-------------|------|------|---------|
| Exact match | `rg` (ripgrep) | ~20ms | Exact hits only |
| Exact match | `grep` | ~45ms | Exact hits only |
| Semantic | `grepai` | ~500ms | Intent-based matches |

**Key insight**: grepai is ~25x slower than rg for exact matches, but finds results that pattern-based tools cannot discover.

```bash
# Know exact pattern → use rg (fast)
rg "createSession" --type ts

# Don't know exact name → use grepai (semantic)
grepai search "session creation logic"
```

> **Source**: [grepai GitHub](https://github.com/yoanbernabeu/grepai)

**Blast-Radius Pattern (pre-refactoring workflow):**

Before modifying any widely-used function, run a dependency query to enumerate all affected call sites — then decide whether to proceed. This named workflow prevents cascading breakage in large codebases.

```bash
# Step 1: Map all callers before touching a function
grepai trace callers "processPayment"
# → Returns: 14 call sites across 7 files

# Step 2: Check callees (what it depends on)
grepai trace callees "processPayment"
# → Returns: 3 downstream dependencies

# Step 3: Decide scope before writing a single line
# 14 callers + 3 deps = significant blast radius → plan the refactor first
```

Run this before starting any refactor touching a function used in 3+ places — not after hitting compile errors.

---

### claude-mem (Automatic Session Memory)

**Purpose**: Automatic persistent memory across Claude Code sessions through AI-compressed capture of tool usage and observations.

**Why claude-mem matters**: Unlike manual memory tools (Serena's `write_memory()`), claude-mem **automatically captures everything** Claude does during sessions and intelligently injects relevant context when you reconnect. This solves the #1 pain point: context loss between sessions.

**Key Features**:

| Feature | Description |
|---------|-------------|
| **Automatic capture** | Hooks into SessionStart, PostToolUse, Stop, SessionEnd lifecycle events |
| **AI compression** | Uses Claude to generate semantic summaries (~10x token reduction) |
| **Progressive disclosure** | 3-layer retrieval (search → timeline → observations) saves ~95% tokens |
| **Hybrid search** | Full-text + vector search (Chroma) + natural language queries |
| **Web dashboard** | Real-time UI at `http://localhost:37777` for exploring history |
| **Privacy controls** | `<private>` tags to exclude sensitive content from storage |

**Architecture**:

```
Session Lifecycle (hooks → worker → storage):

┌─────────────────────┬──────────────────────────┬──────────────────────────────────────┐
│ Moment              │ Hook                     │ Action                               │
├─────────────────────┼──────────────────────────┼──────────────────────────────────────┤
│ Session starts      │ SessionStart             │ Worker boots, injects last N sessions│
│ First prompt        │ UserPromptSubmit         │ Creates/identifies current session   │
│ After each tool use │ PostToolUse (matcher: *) │ Captures typed observation           │
│ End of response     │ Stop                     │ Generates LLM summary                │
│ Session ends        │ SessionEnd               │ Marks session complete               │
└─────────────────────┴──────────────────────────┴──────────────────────────────────────┘

Worker Pipeline (Bun, port 37777):

  Claude Code tool call
         │
         ▼
  LLM analysis (Gemini 2.5 Flash Lite)
         │
         ├── type: DISCOVERY / CHANGE / FEATURE / BUGFIX
         ├── facts: files touched, patterns detected
         └── narrative: generated summary
         │
         ▼
  SQLite (~/.claude-mem/claude-mem.db)
         ├── [optional] Chroma vector search (port 8000, fallback: SQLite FTS)
         └── Web UI at localhost:37777 + MCP skills
```

**Observation Types**:

| Type | When generated | Example |
|------|---------------|---------|
| `DISCOVERY` | Reading/exploring code | "Explored auth module, found JWT in validateToken()" |
| `CHANGE` | File edits | "Modified session.middleware.ts: added refresh logic" |
| `FEATURE` | New functionality | "Implemented OAuth2 flow in auth.service.ts" |
| `BUGFIX` | Bug corrections | "Fixed null pointer in UserController.getById()" |

**Installation**:

```bash
# Via plugin marketplace (recommended)
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# Restart Claude Code
# claude-mem automatically activates on next session
```

**Basic Usage**:

Once installed, claude-mem works **automatically**—no manual commands needed. It captures all tool operations and injects relevant context at session start.

**Available Skills** (`/claude-mem:*`):

| Skill | Purpose |
|-------|---------|
| `mem-search` | Search session history: "How did we solve the CORS issue?" |
| `smart-explore` | AST-based codebase exploration (token-efficient, avoids full file reads) |
| `make-plan` | Creates a phased implementation plan with doc discovery |
| `do` | Executes a plan created by `make-plan` via sub-agents |
| `timeline-report` | Generates a "Journey Into [Project]" narrative over full history |

**Natural Language Search** (via `mem-search` skill):

```bash
# Search your session history
"Search my memory for authentication decisions"
"What files did we modify for the payment bug?"
"Remind me why we chose Zod over Yup"
```

**Web Dashboard**:

```bash
# Access real-time UI
open http://localhost:37777

# Features:
# - Timeline view of all sessions
# - Natural language search
# - Observation details
# - Session statistics
```

**Progressive Disclosure Workflow**:

claude-mem uses a 3-layer approach to minimize token consumption:

```
Layer 1: Search (50-100 tokens)
├─ "Find sessions about authentication"
├─ Returns: 5 relevant session summaries
│
Layer 2: Timeline (500-1000 tokens)
├─ "Show timeline for session abc123"
├─ Returns: Chronological observation list
│
Layer 3: Details (full context)
└─ "Get observation details for obs_456"
    Returns: Complete tool call + result
```

**Result**: ~10x token reduction vs loading full session history.

**Privacy Controls**:

```markdown
<!-- In your prompts -->
<private>
Database credentials: postgres://prod-db-123
API key: sk-1234567890abcdef
</private>

<!-- claude-mem excludes <private> content from storage -->
```

**Security Warning**:

> ⚠️ `GET /api/settings` returns your API keys in plain text. Any process running on your machine (browser extension with localhost access, npm package, another CLI tool) can read this endpoint without authentication. Localhost is not a security boundary.
>
> **Mitigation**: Set `host: "127.0.0.1"` (not `"0.0.0.0"`) in your config. Never run on a shared machine or expose the port to your network. Consider using CLI auth (`auth_method: cli`) instead of storing keys in settings.json.

**Cost Considerations**:

| Aspect | Cost | Notes |
|--------|------|-------|
| **API compression** | ~$0.15 per 100 observations | AI summarization (model configurable) |
| **Storage** | Free (local SQLite) | 10-20 MB/month (light use), 100-200 MB/month (heavy use) |
| **Queries** | Free (local vectors) | Chroma indexation runs locally |

**Typical monthly cost**: $5-15 for heavy users (100+ sessions/month)

**Cost optimization — use Gemini instead of Claude for compression**:

By default, claude-mem uses Claude (Haiku) for AI summarization. You can configure Gemini 2.5 Flash Lite instead for significant cost savings:

```bash
# In ~/.claude-mem/settings.json
{
  "provider": "gemini",
  "model": "gemini-2.5-flash-lite",
  "auth_method": "cli"
}
```

| Model | Cost/month (~400 sessions) | Quality | Savings |
|-------|---------------------------|---------|---------|
| Claude Haiku (default) | ~$102 | High | — |
| Gemini 2.5 Flash | ~$14 | Good | **-86%** |
| Gemini 2.5 Flash Lite | ~$14 | Adequate | **-86%** |

> **Flash vs Flash Lite**: Flash Lite is cheaper but produces weaker compressions. Context injected at session start will be less precise. For most users the tradeoff is acceptable; for complex multi-week projects, consider Gemini 2.5 Flash (non-Lite) to preserve compression quality.

If you're running claude-mem at scale, switching to Gemini is the single highest-ROI configuration change.

**Critical installation gotcha — hooks coexistence**:

claude-mem adds hooks on `SessionStart`, `PostToolUse`, `Stop`, and `SessionEnd`. If you already have hooks in `settings.json`, **claude-mem will not automatically merge them** — it will overwrite the hooks arrays.

Before installing:
1. Back up your current `settings.json`
2. Note all existing hooks (PostToolUse, UserPromptSubmit arrays)
3. After installation, manually verify the hooks arrays contain both your existing hooks AND the new claude-mem hooks

```json
// ✅ Correct — both hooks coexist
"hooks": {
  "PostToolUse": [
    {"matcher": "...", "hooks": [{"type": "command", "command": "your-existing-hook.sh"}]},
    {"matcher": "...", "hooks": [{"type": "command", "command": "claude-mem-hook.sh"}]}
  ]
}

// ❌ Wrong — claude-mem silently replaced your hooks
"hooks": {
  "PostToolUse": [
    {"matcher": "...", "hooks": [{"type": "command", "command": "claude-mem-hook.sh"}]}
  ]
}
```

**Reliability: fail-open architecture (v9.1.0+)**:

If the claude-mem worker process is down (crash, restart, port conflict), Claude Code continues working normally — it does not block or error. Sessions simply aren't captured until the worker restarts.

```bash
# Check worker status
open http://localhost:37777  # dashboard — if unreachable, worker is down

# Restart worker manually if needed
npx claude-mem@latest start
```

This fail-open behavior makes claude-mem safe to install in production workflows — a dead worker never blocks your work.

**Limitations**:

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **CLI only** | No web interface, no VS Code | Use Claude Code CLI exclusively |
| **No cloud sync** | Can't sync between machines | Manual export/import via `claude-mem export` |
| **AGPL-3.0 license** | Commercial restrictions, source disclosure | Check license compliance for commercial use |
| **Manual privacy tags** | Must explicitly mark sensitive data | Use `<private>` tags consistently |

**Use when**:
- Working on projects >1 week with multiple sessions
- Need to remember architectural decisions across days/weeks
- Frequently ask "what did we do last time?"
- Want to avoid re-reading files for context
- Value automatic capture over manual note-taking

**Don't use when**:
- One-off quick tasks (<10 minutes)
- Extremely sensitive data (consider manual Serena instead)
- Commercial projects without AGPL compliance review
- Need cross-machine sync (not supported)

**Example: Multi-Day Refactoring**:

```
Day 1 (Session 1):
User: "Explore auth module"
Claude: [Reads auth.service.ts, session.middleware.ts]
claude-mem: Captures "Auth exploration: JWT validation, session management"

Day 2 (Session 2):
Claude: [Auto-injected context]
"Previously: Explored auth module. Files: auth.service.ts, session.middleware.ts.
 Key finding: JWT validation in validateToken()"
User: "Refactor auth to use jose library"
Claude: [Already has context, no re-reading needed]

Day 3 (Session 3):
Claude: [Auto-injected context]
"Day 1: Auth exploration. Day 2: Refactored to jose library.
 Decision: Chose jose over jsonwebtoken (lighter, 40% fewer deps)"
User: "Add tests for auth refactoring"
Claude: [Full context of decisions and changes]
```

**Stats** (updated 2026-03-30):
- **26.5k GitHub stars**, 1.8k forks
- 46 contributors
- Latest: v10.6.3
- License: AGPL-3.0 + PolyForm Noncommercial

> **Sources**:
> - [GitHub: thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
> - [Guide: Progressive Disclosure](https://corti.com/claude-mem-persistent-memory-for-ai-coding-assistants/)
> - [Video: 5-Minute Setup](https://www.youtube.com/watch?v=ryqpGVWRQxA)

---

### Graphify (Codebase Knowledge Graphs)

**GitHub**: [safishamsi/graphify](https://github.com/safishamsi/graphify) | **PyPI**: `graphifyy` | **Stars**: 42K | **License**: MIT

Graphify converts a project directory into a persistent knowledge graph and injects a compact structural report (`GRAPH_REPORT.md`) into Claude Code. The assistant answers architecture questions by reading the pre-built graph instead of re-scanning raw files on each prompt. Initial extraction runs once; subsequent sessions query the graph at near-zero token cost.

**How it works**: Three passes per run:

1. **Local AST extraction** — tree-sitter parses 25+ languages (Python, TS, Go, Rust, Java, etc.) into a call graph. No API cost, no network.
2. **Optional local transcription** — faster-whisper transcribes audio/video locally.
3. **Parallel semantic extraction** — Claude subagents process docs, PDFs, and images using your existing API key.

Results merge into a NetworkX graph clustered with the Leiden algorithm (topology-based — no vector embeddings). Every relationship is tagged `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`. Three output files land in `graphify-out/`:

- `graph.html` — interactive browser visualization
- `GRAPH_REPORT.md` — god nodes, cross-file connections, suggested queries (injected into Claude)
- `graph.json` — persistent, queryable without re-extraction

**Install**:

```bash
# Requires Python 3.10+. PyPI package: graphifyy (double-y). CLI: graphify.
uv tool install graphifyy && graphify install

# Always-on Claude Code integration (writes CLAUDE.md section + hook)
graphify claude install

# Build graph for current directory
/graphify .

# Incremental update (re-extracts only changed files, uses SHA256 hashing)
/graphify . --update

# Query the graph directly
/graphify query "what connects auth to the database layer?"
/graphify path "UserService" "DatabasePool"
/graphify explain "RateLimiter"

# Auto-rebuild on git commits (local AST only, zero API cost)
graphify hook install
```

**Optional extras**:

```bash
pip install "graphifyy[office]"   # .docx, .xlsx support
pip install "graphifyy[video]"    # .mp4, .mov, .mp3 transcription
```

**Graphify vs GrepAI**: Different layers, complementary. GrepAI (Ollama, local, free) handles real-time semantic lookups during active coding — fast, targeted, exact. Graphify pre-computes structural relationships across the full codebase (call chains, cross-file dependencies, community clusters) and replaces repeated file reads with a single compact report per session. GrepAI for discovery; Graphify for architectural reasoning and multi-hop questions.

**Graphify vs claude-mem**: Separate concerns. claude-mem stores what you *discussed* across sessions (decisions, tool calls, observations). Graphify maps what the *codebase contains* (structure, dependencies, concept clusters). No overlap — they address different layers of context loss.

**Team workflow**: Commit `graphify-out/` (excluding `manifest.json` and `cache/`) to git so teammates inherit the pre-built graph without running extraction themselves.

**Caveats**:

- Non-code files (docs, PDFs, images) are sent to your AI assistant's API on first run — costs accumulate on large mixed-media repositories.
- Without the post-commit hook, the graph drifts from the codebase.
- Token efficiency claims from the author (71.5x–120x fewer tokens vs grep-based exploration) are self-reported benchmarks without independent reproduction. Treat as directional.
- No native query language — graph queries go through the AI assistant, not Cypher/SQL.

**Stats**: 42K GitHub stars | v0.7.4 (2026-05-04) | Python ≥3.10 | MIT

> **Source**: [safishamsi/graphify](https://github.com/safishamsi/graphify)

---

### 🧩 Memory Tools Decision Matrix

Now that you've seen Serena, grepai, claude-mem, and Graphify, here's when to use each:

| Need | Tool | Example |
|------|------|---------|
| **"What did we do yesterday?"** | claude-mem | Auto-inject previous session context |
| **"Find function login"** | Serena | `find_symbol --name "login"` |
| **"Who calls this function?"** | grepai | `grepai trace callers "login"` |
| **"Record arch decision"** | Serena | `write_memory("auth_decision", "Use JWT")` |
| **"Find code that does X"** | grepai | `grepai search "payment validation"` |
| **"Summary of all sessions"** | claude-mem | Web dashboard at localhost:37777 |
| **"Exact pattern match"** | rg (native) | `rg "authenticate" --type ts` |
| **"What does this module depend on?"** | Graphify | `/graphify query "auth dependencies"` |
| **"Map the full codebase structure"** | Graphify | `/graphify . --update` |

**Memory Stack Pattern** (5 layers):

```
Layer 5: Session Capture      → claude-mem (automatic)
Layer 4: Symbol Memory        → Serena (manual decisions)
Layer 3: Semantic Search      → grepai (discovery)
Layer 2: Structural Graph     → Graphify (architecture, cross-file dependencies)
Layer 1: Exact Search         → rg (native, fast)
```

**Integrated Workflow Example**:

```bash
# Scenario: Refactoring auth module after 3 days

# 1. AUTO CONTEXT (claude-mem)
# At session start, Claude auto-injects:
# "3 previous sessions explored auth module.
#  Decision: Migrate to JWT.
#  Files modified: auth.service.ts, session.middleware.ts"

# 2. ARCH DECISIONS (Serena)
serena list_memories
# → "auth_decision: Use JWT for stateless API (2026-02-07)"
serena read_memory("auth_decision")

# 3. SEMANTIC DISCOVERY (grepai)
grepai search "JWT token validation"
# → Finds validateJWT() in auth.service.ts

# 4. DEPENDENCIES (grepai trace)
grepai trace callers "validateJWT"
# → Called by: ApiGateway, AdminPanel, UserController

# 5. EXACT SEARCH (rg)
rg "validateJWT" --type ts -A 5
```

**Result**: Complete context without re-reading all files, architectural decisions preserved, dependencies mapped → safe refactoring.

**Comparison: claude-mem vs Serena vs grepai**:

| Aspect | claude-mem | Serena | grepai |
|--------|-----------|---------|--------|
| **Trigger** | Auto (hooks) | Manual API | Manual CLI |
| **Storage** | SQLite + Chroma | `.serena/memories/` | Ollama vectors |
| **Purpose** | Session capture | Symbol memory | Semantic search |
| **Dashboard** | ✅ Web UI | ❌ No | ❌ No |
| **Cost** | ~$0.15/100 obs | Free | Free |
| **Effort** | Zero (automatic) | Manual commands | Manual commands |
| **Query** | Natural language | Key lookup | Semantic search |
| **License** | AGPL-3.0 | MIT | MIT |

**When to combine tools**:

- **claude-mem + Serena**: Automatic capture + manual architectural decisions
- **claude-mem + grepai**: Session history + semantic code discovery
- **All 3**: Complete memory stack (session + symbol + semantic + exact)

---

### 🔍 Search Tools Comparison: rg vs grepai vs Serena vs ast-grep vs claude-mem

Now that you've seen individual tools, here's how they compare and when to use each:

#### Quick Decision Matrix

| I need to... | Tool | Example |
|--------------|------|---------|
| Find exact text | `rg` (Grep) | `rg "authenticate" --type ts` |
| Find by meaning | `grepai` | `grepai search "user login flow"` |
| Find function definition | `Serena` | `serena find_symbol --name "login"` |
| Find structural pattern | `ast-grep` | `ast-grep "async function $F"` |
| See who calls function | `grepai` | `grepai trace callers "login"` |
| Get file structure | `Serena` | `serena get_symbols_overview` |
| Remember past sessions | `claude-mem` | Auto-injected at session start |

#### Feature Comparison

| Feature | rg (ripgrep) | grepai | Serena | ast-grep | claude-mem |
|---------|--------------|--------|--------|----------|-----------|
| **Search type** | Regex/text | Semantic | Symbol-aware | AST structure | Session history |
| **Speed** | ⚡ ~20ms | 🐢 ~500ms | ⚡ ~100ms | 🕐 ~200ms | ⚡ ~100ms |
| **Setup** | ✅ None | ⚠️ Ollama | ⚠️ MCP | ⚠️ npm | ⚠️ Plugin |
| **Integration** | ✅ Native | ⚠️ MCP | ⚠️ MCP | ⚠️ Plugin | ⚠️ Plugin |
| **Call graph** | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Symbol tracking** | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **Session memory** | ❌ No | ❌ No | ✅ Manual | ❌ No | ✅ Automatic |
| **Auto capture** | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Web dashboard** | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |

#### When to Use What

**Use rg (ripgrep)** when:
- ✅ You know the exact text/pattern
- ✅ Speed is critical (~20ms)
- ✅ No setup complexity wanted
- ❌ Don't use for: conceptual searches, dependency tracing

**Use grepai** when:
- ✅ Finding code by meaning/intent
- ✅ Need to trace function calls (who calls what)
- ✅ Privacy required (100% local with Ollama)
- ❌ Don't use for: exact text (use rg instead)

**Use Serena** when:
- ✅ Refactoring across multiple files
- ✅ Need symbol-aware navigation
- ✅ Persistent context/memory needed
- ❌ Don't use for: simple text searches

**Use ast-grep** when:
- ✅ Large-scale refactoring (>50k lines)
- ✅ Framework migrations (React, Vue)
- ✅ Finding structural patterns (async without try/catch)
- ❌ Don't use for: small projects, simple searches

**Use claude-mem** when:
- ✅ Multi-session projects (>1 week)
- ✅ Need to remember architectural decisions
- ✅ Frequently reconnecting to same project
- ✅ Want automatic context injection (no manual effort)
- ❌ Don't use for: one-off tasks, extremely sensitive data

#### Combined Workflow Example

**Task**: Refactor authentication across codebase

```bash
# 1. Discover (grepai - semantic)
grepai search "authentication and session management"
# → Finds: auth.service.ts, session.middleware.ts

# 2. Structure (Serena - symbols)
serena get_symbols_overview --file auth.service.ts
# → Classes: AuthService, functions: login, logout

# 3. Dependencies (grepai - call graph)
grepai trace callers "login"
# → Called by: UserController, ApiGateway (23 files)

# 4. Patterns (ast-grep - structure)
ast-grep "async function login" --without "try { $$$ } catch"
# → Finds 3 async functions missing error handling

# 5. Verification (rg - exact)
rg "validateSession" --type ts -A 5
# → Verify specific implementation
```

**Result**: Complete understanding + safe refactoring in 5 commands

> **📖 Complete Guide**: See [Search Tools Mastery](workflows/search-tools-mastery.md) for detailed workflows, real-world scenarios, and advanced combinations.

---

### mgrep (Alternative Semantic Search)

**Purpose**: Natural language semantic search across code, docs, PDFs, and images.

**Why consider mgrep**: If you need **multi-format search** (code + PDFs + images) or prefer a cloud-based solution, mgrep is an alternative to grepai. Their benchmarks show ~2x fewer tokens used compared to grep-based workflows.

**Key Features**:

| Feature | Description |
|---------|-------------|
| **Semantic search** | Find code by natural language description |
| **Background indexing** | `mgrep watch` indexes respecting `.gitignore` |
| **Multi-format** | Search code, PDFs, images, text |
| **Web integration** | Web search fallback capability |

**Example**:

```bash
# Traditional grep (exact match required)
grep -r "authenticate.*user" .

# mgrep (intent-based)
mgrep "code that handles user authentication"
```

**Use when**:
- Need to search across mixed content (code + PDFs + images)
- Prefer cloud-based embeddings over local Ollama setup
- grepai's call graph analysis isn't needed

> **Note**: I haven't tested mgrep personally. Consider it an alternative worth exploring.
> **Source**: [mgrep GitHub](https://github.com/mixedbread-ai/mgrep)

### Context7 (Documentation Lookup)

**Purpose**: Access official library documentation.

**Tools**:

| Tool | Description |
|------|-------------|
| `resolve-library-id` | Find library documentation |
| `query-docs` | Query specific documentation |

**Use when**:
- Learning new libraries
- Finding correct API usage
- Checking official patterns

### ast-grep (Structural Code Search)

**Purpose**: AST-based pattern matching for precise structural code searches.

**Type**: Optional Community Plugin (not core Claude Code)

**Installation**:

```bash
# Install ast-grep skill for Claude Code
npx skills add ast-grep/agent-skill

# Or manually via plugin marketplace
/plugin marketplace add
```

**What is ast-grep?**

ast-grep searches code based on **syntax structure** (Abstract Syntax Tree) rather than plain text. This enables finding patterns like "async functions without error handling" or "React components using specific hooks" that regex cannot reliably detect.

**Key Characteristics**:

| Aspect | Behavior |
|--------|----------|
| **Invocation** | **Explicit** - Claude cannot automatically detect when to use it |
| **Integration** | Plugin that teaches Claude how to write ast-grep rules |
| **Languages** | JavaScript, Python, Rust, Go, Java, C/C++, Ruby, PHP + more |
| **Pattern matching** | Metavariables (`$VAR`), relational queries, composite logic |

**When to use ast-grep**:

✅ **Use for**:
- **Large-scale refactoring** (>50k lines, indicative threshold)
- **Framework migrations** (React class→hooks, Vue 2→3)
- **Structural patterns**:
  - Async functions lacking error handling
  - Functions exceeding parameter thresholds
  - Console.log calls within class methods
  - React components using specific hooks
- **Architecture analysis** (identify coupled components, dependency patterns)

❌ **Don't use for** (grep suffices):
- Simple string searches (function names, imports)
- Small projects (<10k lines)
- One-off searches
- Text-based patterns (TODO comments, log messages)

**Decision Tree**:

```
Search need?
├─ String/regex pattern → Grep (native, fast)
├─ Semantic meaning → Serena MCP (symbol search) or grepai (RAG-based)
└─ Structural pattern (AST) → ast-grep (plugin, setup required)
```

**Trade-offs**:

| Aspect | Grep | ast-grep | Serena MCP | grepai |
|--------|------|----------|------------|--------|
| **Speed** | ⚡ Fast (~20ms) | Moderate | Fast | Slower (embedding) |
| **Setup** | ✅ None | ⚠️ Installation + learning | ⚠️ MCP config | ⚠️ MCP + Ollama |
| **Precision** | Regex-based | AST-accurate | Symbol-aware | Semantic |
| **Use case** | Text patterns | Code structure | Symbols/functions | Meaning-based |

**Example usage**:

```bash
# User explicitly requests ast-grep
You: Use ast-grep to find all async functions without try/catch blocks

# Claude uses the ast-grep skill to construct rules
Claude: [Constructs AST pattern, executes search, reports results]
```

**Important limitations** (as of Nov 2025):

> "Claude Code cannot automatically detect when to use ast-grep for all appropriate use cases." - ast-grep/claude-skill README

This means you must **explicitly tell Claude** to use ast-grep. It won't decide on its own.

**Sources**:
- [ast-grep Documentation](https://ast-grep.github.io/advanced/prompting.html)
- [ast-grep/claude-skill GitHub](https://github.com/ast-grep/claude-skill)

**Design Philosophy Context**:

Early Claude Code versions used RAG with Voyage embeddings for semantic search. Anthropic switched to grep-based (ripgrep) agentic search after benchmarks showed superior performance with lower operational complexity (no index sync, no security liabilities). This "Search, Don't Index" philosophy prioritizes simplicity.

ast-grep is a **community extension** for specialized structural searches where grep's regex approach isn't sufficient, but it's not a replacement for grep — it's a surgical tool for specific use cases.

**Related**: See [Section 8.4 - Server Selection Guide](#84-server-selection-guide) for choosing between grep/ast-grep/Serena/grepai.

### Sequential Thinking (Structured Reasoning)

**Purpose**: Multi-step analysis with explicit reasoning.

**Tools**:

| Tool | Description |
|------|-------------|
| `sequentialthinking` | Step-by-step reasoning |

**Use when**:
- Complex debugging
- Architectural analysis
- System design decisions

### Postgres (Database Queries)

**Purpose**: Direct database access for queries.

**Tools**:

| Tool | Description |
|------|-------------|
| `query` | Execute SQL queries |

**Use when**:
- Investigating data issues
- Understanding schema
- Debugging data problems

### Playwright (Browser Automation)

**Purpose**: Browser testing and automation.

**Tools**:

| Tool | Description |
|------|-------------|
| `navigate` | Go to URL |
| `click` | Click element |
| `fill` | Fill form field |
| `screenshot` | Capture screenshot |

**Use when**:
- E2E testing
- Visual validation
- Browser debugging

### agent-browser (Vercel Labs) — AI-Native Browser Automation

> **Status**: Active development — v0.15.0 (Feb 2026). 12,100+ stars. Rapid release cycle.

**Purpose**: Headless browser CLI built for AI agents. Uses Playwright/CDP under the hood but optimizes all output for LLM consumption. Written in Rust for sub-millisecond startup.

**Why it matters for agentic workflows**: Playwright MCP is verbose — every DOM snapshot adds tokens. agent-browser returns only actionable elements via stable short references (`@e1`, `@e2`), cutting token usage by ~82.5% on identical scenarios (Pulumi benchmark, 2026-03-03).

**Install**:

```bash
# Homebrew
brew install vercel-labs/tap/agent-browser

# Or npm
npm install -g @vercel-labs/agent-browser
```

**Capabilities**:

| Feature | Details |
|---------|---------|
| Navigation + interaction | Click, type, scroll, fill forms |
| Accessibility tree | LLM-optimized snapshots (actionable elements only) |
| Visual diffs | Pixel-level comparison against baselines |
| Session persistence | Save/restore auth state (AES-256-GCM) |
| Multi-session | Isolated instances, separate cookies/storage |
| Security (v0.15.0) | Auth vaults, domain allowlists, action policies |
| Browser streaming | Live WebSocket preview for human+agent "pair browsing" |

**agent-browser vs Playwright MCP**:

| Dimension | Playwright MCP | agent-browser |
|-----------|---------------|---------------|
| Primary audience | Developers (test suites) | AI agents |
| Token usage | Baseline | **-82.5%** |
| Element references | XPath/CSS selectors | `@e1`, `@e2` (stable, compact) |
| Implementation | Node.js | Rust (sub-ms startup) |
| Session persistence | No | Yes |
| Security controls | None | Auth vaults, domain allowlists |
| Self-verifying agents | Awkward | Native pattern |

**The Ralph Wiggum Loop** — self-verifying agent pattern:

```
1. Agent codes the feature
2. Deploys (Vercel, any target)
3. agent-browser navigates to deployed URL autonomously
4. Tests scenarios, reads accessibility snapshots
5. On failure: agent reads output, fixes code, re-deploys
6. Loop until all scenarios pass — no human in the loop
```

Documented in production at Pulumi (2026-03-03) across 6 test scenarios on a real app.

**Use when**:
- Agent must verify its own deployed output (self-verifying loops)
- Token cost of browser context is a constraint
- Multi-session testing (parallel isolated browser instances)
- Visual regression in agentic CI/CD pipelines

**Don't use when**:
- You have existing Playwright test suites — not a drop-in replacement for test runners
- Scraping anti-bot protected sites — IP/behavior detection unchanged (Browserbase-type services still needed)

**Resources**:
- [GitHub: vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- [Case study: Ralph Wiggum Loop at Pulumi](https://www.pulumi.com/blog/self-verifying-ai-agents-vercels-agent-browser-in-the-ralph-wiggum-loop/)

### doobidoo Memory Service (Semantic Memory)

> **⚠️ Status: Under Testing** - This MCP server is being evaluated. The documentation below is based on the official repository but hasn't been fully validated in production workflows yet. Feedback welcome!

**Purpose**: Persistent semantic memory with cross-session search and multi-client support.

**Why doobidoo complements Serena**:
- Serena: Key-value memory (`write_memory("key", "value")`) - requires knowing the key
- doobidoo: Semantic search (`retrieve_memory("what did we decide about auth?")`) - finds by meaning

| Feature | Serena | doobidoo |
|---------|--------|----------|
| Memory storage | Key-value | Semantic embeddings |
| Search by meaning | No | Yes |
| Multi-client | Claude only | 13+ apps |
| Dashboard | No | Knowledge Graph |
| Symbol indexation | Yes | No |

**Storage Backends**:

| Backend | Usage | Performance |
|---------|-------|-------------|
| `sqlite_vec` (default) | Local, lightweight | <10ms queries |
| `cloudflare` | Cloud, multi-device sync | Edge performance |
| `hybrid` | Local fast + cloud background sync | 5ms local |

**Data Location**: `~/.mcp-memory-service/memories.db` (SQLite with vector embeddings)

**MCP Tools Available** (12 unified tools):

| Tool | Description |
|------|-------------|
| `store_memory` | Store with tags, type, metadata |
| `retrieve_memory` | Semantic search (top-N by similarity) |
| `search_by_tag` | Exact tag matching (OR/AND logic) |
| `delete_memory` | Delete by content_hash |
| `list_memories` | Paginated browsing with filters |
| `check_database_health` | Stats, backend status, sync info |
| `get_cache_stats` | Server performance metrics |
| `memory_graph:connected` | Find connected memories |
| `memory_graph:path` | Shortest path between memories |
| `memory_graph:subgraph` | Subgraph around a memory |

**Installation**:

```bash
# Quick install (local SQLite backend)
pip install mcp-memory-service
python -m mcp_memory_service.scripts.installation.install --quick

# Team/Production install (more options)
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service
python scripts/installation/install.py
# → Choose: cloudflare or hybrid for multi-device sync
```

**Configuration** (add to MCP config):

```json
{
  "mcpServers": {
    "memory": {
      "command": "memory",
      "args": ["server"]
    }
  }
}
```

**Configuration with environment variables** (for team/cloud sync):

```json
{
  "mcpServers": {
    "memory": {
      "command": "memory",
      "args": ["server"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "hybrid",
        "MCP_HTTP_ENABLED": "true",
        "MCP_HTTP_PORT": "8000",
        "CLOUDFLARE_API_TOKEN": "your-token",
        "CLOUDFLARE_ACCOUNT_ID": "your-account-id"
      }
    }
  }
}
```

**Key Environment Variables**:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_MEMORY_STORAGE_BACKEND` | `sqlite_vec` | Backend: sqlite_vec, cloudflare, hybrid |
| `MCP_HTTP_ENABLED` | `true` | Enable dashboard server |
| `MCP_HTTP_PORT` | `8000` | Dashboard port |
| `MCP_OAUTH_ENABLED` | `false` | Enable OAuth for team auth |
| `MCP_HYBRID_SYNC_INTERVAL` | `300` | Sync interval in seconds |

**Usage**:

```
# Store a decision with tags
store_memory("We decided to use FastAPI for the REST API", tags=["architecture", "api"])

# Semantic search (finds by meaning, not exact match)
retrieve_memory("what framework for API?")
→ Returns: "We decided to use FastAPI..." with similarity score

# Search by tag
search_by_tag(["architecture"])

# Check health
check_database_health()
```

**Multi-Client Sync**:

```
# Same machine: all clients share ~/.mcp-memory-service/memories.db
Claude Code ──┐
Cursor ───────┼──► Same SQLite file
VS Code ──────┘

# Multi-device: use Cloudflare backend
Device A ──┐
Device B ──┼──► Cloudflare D1 + Vectorize
Device C ──┘
```

**When to use which**:
- **Serena**: Symbol navigation, code indexation, key-value memory with known keys
- **doobidoo**: Cross-session decisions, "what did we decide about X?", multi-IDE sharing

**Dashboard**: Access at http://localhost:8000 after starting the server.

> **Source**: [doobidoo/mcp-memory-service GitHub](https://github.com/doobidoo/mcp-memory-service) (791 stars, v10.0.2)

### Kairn: Knowledge Graph Memory with Biological Decay

> **⚠️ Status: Under Testing** - Evaluated Feb 2026. MIT licensed, Python 100%. Feedback welcome!

**Purpose**: Long-term project memory organized as a knowledge graph with automatic decay — stale information expires on its own, preventing context pollution.

**Key differentiators vs doobidoo/Serena**:
- **Typed relationships**: `depends-on`, `resolves`, `causes` — captures causality, not just content
- **Biological decay model**: solutions persist ~200 days, workarounds ~50 days — auto-pruning without `delete_memory` calls
- **18 MCP tools**: graph ops, project tracking, experience management, intelligence layer (full-text search, confidence routing, cross-workspace patterns)

| Feature | Serena | doobidoo | Kairn |
|---------|--------|----------|-------|
| Storage model | Key-value | Semantic embeddings | Knowledge graph |
| Memory decay / auto-expiry | No | No | Yes (biological) |
| Typed relationships | No | Tags only | depends-on / resolves / causes |
| Full-text search | No | Yes | Yes |
| Auto-pruning stale info | No | No | Yes |

**When Kairn makes sense**:
- Long-running projects where workarounds from months ago become noise
- When causality matters: "this breaks *because* of that", "this fix *resolves* that bug"
- Teams wanting automatic knowledge hygiene without manual cleanup

**MCP Config**:

```json
"kairn": {
  "command": "python",
  "args": ["-m", "kairn", "serve"],
  "description": "Knowledge graph memory with biological decay"
}
```

**Install**:

```bash
pip install kairn
# or from source:
git clone https://github.com/kairn-ai/kairn && cd kairn && pip install -e .
```

> **Source**: [kairn-ai/kairn GitHub](https://github.com/kairn-ai/kairn) (MIT, Python 100%)

### ICM: Dual Memory Architecture (Rust Binary, Zero Dependencies)

> **⚠️ Status: Under Testing** — Evaluated March 2026. Source-Available license (free for individuals and teams ≤20). From the rtk-ai team (same authors as RTK). Benchmarks below are vendor-reported and unverified independently. Feedback welcome!

**Purpose**: Persistent memory for AI agents combining episodic decay (Memories) and permanent knowledge graph (Memoirs) in a single zero-dependency Rust binary.

**When ICM makes sense over Kairn/doobidoo**:
- Python dependency management is a friction point (CI environments, sandboxed machines)
- You want Homebrew install with no Python env setup
- You need both decay-based episodic memory and a permanent knowledge graph in one tool
- You use multiple editors (14 clients supported: Claude Code, Cursor, VS Code, Windsurf, Zed, Amp, Cline, Roo Code, OpenAI Codex CLI, and more)

**Key differentiators vs Kairn/doobidoo**:
- **Single Rust binary**: no Python, no pip, no virtual env — `brew install icm` and done
- **Dual architecture in one tool**: Memories (decay, episodic) + Memoirs (permanent, typed graph) — Kairn covers the graph layer, doobidoo the semantic layer, ICM covers both
- **Auto-extraction**: three-layer automatic capture (pattern hooks, pre-compaction, session-start) without explicit `store_memory` calls
- **Auto-deduplication**: blocks entries with >85% similarity to existing content

| Feature | doobidoo | Kairn | ICM |
|---------|----------|-------|-----|
| Language | Python | Python | Rust (single binary) |
| Install | pip | pip | Homebrew / curl |
| Episodic decay | No | Yes (biological) | Yes (configurable rates) |
| Permanent knowledge graph | No | Yes | Yes (Memoirs) |
| Auto-extraction | No | No | Yes (3 layers) |
| Hybrid search | Semantic | Full-text + semantic | BM25 30% + vector 70% |
| License | MIT | MIT | Source-Available |

**Memoir relation types** (9): `part_of`, `depends_on`, `related_to`, `contradicts`, `refines`, `alternative_to`, `caused_by`, `instance_of`, `superseded_by`

**Installation**:

```bash
# Homebrew (recommended)
brew tap rtk-ai/tap && brew install icm

# Quick install
curl -fsSL https://raw.githubusercontent.com/rtk-ai/icm/main/install.sh | sh

# From source
cargo install --path crates/icm-cli
```

**Setup** (3 separate modes, not a single interactive command):

```bash
# Step 1: MCP server → auto-injects into ~/.claude.json (and 13 other editors)
icm init --mode mcp

# Step 2: PostToolUse hook → auto-extracts context every N tool calls
icm init --mode hook

# Step 3: /recall and /remember slash commands
icm init --mode skill
```

Restart Claude Code after running all three.

**Usage**:

```bash
# Store episodic memory (importance = critical|high|medium|low, not a float)
icm store --topic "my-project" --content "Use PostgreSQL for main DB" --importance high

# Recall with hybrid search
icm recall "database choice"

# Build permanent knowledge graph
icm memoir create -n "system-architecture"
icm memoir add-concept -m "system-architecture" -n "auth-service"
icm memoir link -m "system-architecture" --from "api-gateway" --to "auth-service" -r depends-on

# Session management
icm stats      # memory count, topics, avg weight
icm topics     # list all topics
icm decay      # apply temporal decay manually
icm prune      # remove low-weight entries
```

**Onboarding prompt**: a ready-to-use session starter template is available at `examples/memory/icm-session-starter.md`.

**Performance** (1000 ops, 384d embeddings — vendor-reported):

| Operation | Latency |
|-----------|---------|
| Store (no embeddings) | 34.2 µs/op |
| Store (with embeddings) | 51.6 µs/op |
| FTS5 full-text search | 46.6 µs/op |
| Vector search (KNN) | 590.0 µs/op |
| Hybrid search | 951.1 µs/op |

**Agent efficiency claims** (vendor-reported, Haiku model, unverified independently):
- Session 2: 29% fewer turns, 17% cost reduction
- Session 3: 40% fewer turns, 22% cost reduction

> ⚠️ **License note**: Free for individuals and teams of up to 20 people. Enterprise license required above that threshold. Verify your organization's size before deploying. Contact: license@rtk.ai

> **Source**: [rtk-ai/icm GitHub](https://github.com/rtk-ai/icm) (52 stars, Source-Available)

### MCP Memory Stack: Complementarity Patterns

> **⚠️ Experimental** - These patterns combine multiple MCP servers. Test in your workflow before relying on them.

**The 4-Layer Knowledge Stack**:

```
┌─────────────────────────────────────────────────────┐
│                    KNOWLEDGE LAYER                   │
├─────────────────────────────────────────────────────┤
│  doobidoo     │ Decisions, ADRs, business context   │
│  (semantic)   │ "Why did we do this?"               │
├───────────────┼─────────────────────────────────────┤
│  Serena       │ Symbols, structure, key-value memory│
│  (code index) │ "Where is X defined?"               │
├───────────────┼─────────────────────────────────────┤
│  grepai       │ Semantic code search + call graph   │
│  (code search)│ "Find code that does X"             │
├───────────────┼─────────────────────────────────────┤
│  Context7     │ Official library documentation      │
│  (docs)       │ "How to use library X?"             │
└─────────────────────────────────────────────────────┘
```

**Comparison Matrix**:

| Capability | Serena | grepai | doobidoo | Kairn | ICM |
|------------|--------|--------|----------|-------|-----|
| Cross-session memory | Key-value | No | Semantic | Knowledge graph | Episodic + graph |
| Cross-IDE memory | No | No | Yes | Yes | Yes (14 clients) |
| Cross-device sync | No | No | Yes (Cloudflare) | No | No |
| Knowledge Graph | No | Call graph | Decision graph | Typed relationships | Typed relationships |
| Fuzzy search | No | Code | Memory | Full-text + semantic | BM25 + vector hybrid |
| Tags/categories | No | No | Yes | Yes | Yes (topics) |
| Memory decay / auto-expiry | No | No | No | Yes (biological) | Yes (configurable) |
| Auto-extraction | No | No | No | No | Yes (3 layers) |
| Runtime | — | — | Python | Python | Rust (single binary) |
| License | MIT | MIT | MIT | MIT | Source-Available (≤20 free) |

**Usage Patterns**:

| Pattern | Tool | Example |
|---------|------|---------|
| **Decision taken** | doobidoo | `store_memory("Decision: FastAPI because async + OpenAPI", tags=["decision", "api"])` |
| **Convention established** | doobidoo | `store_memory("Convention: snake_case for Python", tags=["convention"])` |
| **Bug resolved** | doobidoo | `store_memory("Bug: token TTL mismatch Redis/JWT. Fix: align TTL+60s", tags=["bug", "auth"])` |
| **WIP warning** | doobidoo | `store_memory("WIP: refactoring AuthService, don't touch", tags=["wip"])` |
| **Find symbol** | Serena | `find_symbol("PaymentProcessor")` |
| **Find callers** | grepai | `grepai trace callers "validateToken"` |
| **Search by intent** | grepai | `grepai search "authentication logic"` |
| **Library docs** | Context7 | `resolve-library-id("fastapi")` |

**Combined Workflows**:

```
# Workflow 1: Understanding a feature
retrieve_memory("payment module status?")        # doobidoo → business context
grepai search "payment processing"               # grepai → find code
find_symbol("PaymentProcessor")                  # Serena → exact location

# Workflow 2: Onboarding (Session 1 → Session N)
# Session 1 (senior dev)
store_memory("Architecture: hexagonal with ports/adapters", tags=["onboarding"])
store_memory("Tests in __tests__/, using Vitest", tags=["onboarding", "testing"])
store_memory("DANGER: never touch legacy/payment.ts without review", tags=["onboarding", "danger"])

# Session N (new dev)
retrieve_memory("project architecture?")
retrieve_memory("where are tests?")
retrieve_memory("dangerous areas?")

# Workflow 3: ADR (Architecture Decision Records)
store_memory("""
ADR-001: FastAPI vs Flask
- Decision: FastAPI
- Reason: native async, auto OpenAPI, typing
- Rejected: Flask (sync), Django (too heavy)
""", tags=["adr", "api"])

# 3 months later
retrieve_memory("why FastAPI?")

# Workflow 4: Debug context persistence
store_memory("Auth bug: Redis TTL expires before JWT", tags=["debug", "auth"])
store_memory("Fix: align Redis TTL = JWT exp + 60s margin", tags=["debug", "auth", "fix"])

# Same bug reappears months later
retrieve_memory("auth token redis problem")
→ Finds the fix immediately

# Workflow 5: Multi-IDE coordination
# In Claude Code (terminal)
store_memory("Refactoring auth in progress, don't touch AuthService", tags=["wip"])

# In Cursor (another window)
retrieve_memory("work in progress?")
→ Sees the warning
```

**When to use which memory system**:

| Need | Tool | Why |
|------|------|-----|
| "I know the exact key" | Serena `read_memory("api_choice")` | Fast, direct lookup |
| "I remember the topic, not the key" | doobidoo `retrieve_memory("API decision?")` | Semantic search |
| "Share across IDEs" | doobidoo | Multi-client support |
| "Share across devices" | doobidoo + Cloudflare | Cloud sync |
| "Code symbol location" | Serena `find_symbol()` | Code indexation |
| "Code by intent" | grepai `search()` | Semantic code search |
| "Long-term project memory, auto-expiry" | Kairn | Biological decay model |
| "Why did X break / what resolved Y?" | Kairn | Typed relationships (resolves, causes) |

**Current Limitations** (doobidoo):

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No versioning | Can't see decision history | Include dates in content |
| No permissions | Anyone can modify | Use separate DBs per team |
| No source linking | No link to file/line | Include file refs in content |
| No expiration | Stale memories persist | Manual cleanup with `delete_memory` OR use Kairn (auto-decay) |
| No git integration | No branch-aware memory | Tag with branch name |

---

### Git MCP Server (Official Anthropic)

**Purpose**: Programmatic Git access via 12 structured tools for commit, diff, log, and branch management.

**Why Git MCP vs Bash `git`**: The Bash tool can run `git` commands but returns raw terminal output that requires parsing and consumes tokens. Git MCP returns structured data directly usable by Claude, with built-in filters (date, author, branch) and token-efficient diffs via the `context_lines` parameter.

> **⚠️ Status**: Early development — API subject to change. Suitable for local workflows; test before adopting in production pipelines.

**Tools (12)**:

| Tool | Description |
|------|-------------|
| `git_status` | Working tree status (staged, unstaged, untracked) |
| `git_diff_unstaged` | Unstaged changes |
| `git_diff_staged` | Staged changes ready to commit |
| `git_diff` | Compare any two branches, commits, or refs |
| `git_commit` | Create a commit with message |
| `git_add` | Stage one or more files |
| `git_reset` | Unstage files |
| `git_log` | Commit history with date, author, and branch filters |
| `git_create_branch` | Create a new branch |
| `git_checkout` | Switch branches |
| `git_show` | Show details for a commit or tag |
| `git_branch` | List all local branches |

**Setup**:

```bash
# No install required — uvx pulls it on first run
uvx mcp-server-git --repository /path/to/repo
```

**Claude Code configuration** (`~/.claude.json`):

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/absolute/path/to/repo"]
    }
  }
}
```

**Multi-repo configuration** (different server per project):

```json
{
  "mcpServers": {
    "git-frontend": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/projects/frontend"]
    },
    "git-backend": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/projects/backend"]
    }
  }
}
```

**Comparison: Git MCP vs Bash**:

| Use case | Bash `git` | Git MCP |
|----------|-----------|---------|
| Simple status check | Fine | Overkill |
| Filtered log (date + author) | Long command | Native filter params |
| Diff with context control | Possible | `context_lines` param |
| Scripting / automation | Good | Better (structured output) |
| CI / production pipelines | Tested, stable | Early dev, use with care |

**Typical workflows**:
- "Show me all commits by Alice in the last 7 days on the `main` branch"
- "What files changed in the last 3 commits? Summarize the changes."
- "Stage `src/auth.ts` and create a commit with an appropriate message"

> **Source**: `modelcontextprotocol/servers/src/git` — MIT license, part of the Anthropic-maintained monorepo (77k+ stars).

---

### GitHub MCP Server (Official GitHub)

**Purpose**: Full GitHub platform access — Issues, Pull Requests, Projects, Code search, repository management, and GitHub Enterprise.

**Git MCP vs GitHub MCP** (two distinct layers):

| Layer | Tool | Scope |
|-------|------|-------|
| Local Git operations | Git MCP Server | Commits, diffs, branches, staging |
| GitHub cloud platform | GitHub MCP Server | Issues, PRs, Projects, Reviews, Search |

Both can be active simultaneously. They complement each other: Git MCP handles local work, GitHub MCP handles collaboration and cloud state.

**Two setup modes**:

| Mode | Requires | When to use |
|------|----------|-------------|
| Remote (`api.githubcopilot.com`) | GitHub Copilot subscription | Already a Copilot subscriber |
| Self-hosted binary | GitHub PAT only | No Copilot, proprietary code, or privacy requirements |

**Remote MCP** (requires a GitHub Copilot subscription):

> **⚠️ Known issue**: `claude mcp add --transport http` attempts OAuth dynamic client registration by default, which the Copilot endpoint does not support. You'll get: `Incompatible auth server: does not support dynamic client registration`. The fix is to inject the token manually (see below).

Step 1 — Add the server:

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Step 2 — Get your active GitHub CLI token:

```bash
gh auth token
# → gho_xxxxxxxxxxxx
```

Step 3 — Edit `~/.claude.json` to add the `Authorization` header:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer gho_xxxxxxxxxxxx"
      }
    }
  }
}
```

> If the token expires: `gh auth refresh` then update the value in `~/.claude.json`.

**Self-hosted setup** (GitHub PAT only, no Copilot required):

```bash
# Download binary from github.com/github/github-mcp-server/releases
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
./github-mcp-server stdio
```

```json
{
  "mcpServers": {
    "github": {
      "command": "/path/to/github-mcp-server",
      "args": ["stdio"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

**Key capabilities**:
- Issues: create, list, filter, assign, close
- Pull Requests: create, review, merge, list by assignee/label
- Projects: read and update GitHub Projects v2
- Code search: search across all repos in an org
- GitHub Enterprise: same API, different base URL

**Typical workflows with Claude Code**:
- "List all open PRs assigned to me on `org/repo`, sorted by last activity"
- "For PR #456, summarize the changes, flag breaking changes, and draft a review comment"
- "Create an issue for bug X with a checklist, then open a branch and push a fix commit"
- "Search all repos in the org for usages of deprecated `fetchUser()` and list files to migrate"

**Differentiator vs `@modelcontextprotocol/server-github`**: The official GitHub MCP server adds Projects support, OAuth 2.1 auth, GitHub Enterprise, and the remote hosted endpoint. The npm reference server is lighter but covers fewer features.

> **Source**: `github/github-mcp-server` — Go, MIT license, 20k+ stars, actively maintained with regular releases.

</details>

---

### 📖 This Guide as an MCP Server

The Claude Code Ultimate Guide ships its own MCP server — `claude-code-ultimate-guide-mcp` — so you can query the guide directly from any Claude Code session without cloning the repo.

**What it gives you**: 9 tools covering search, content reading, templates, digests, cheatsheet, and release notes. The structured index (882 entries) is bundled in the package (~130KB); markdown files are fetched from GitHub on demand with 24h local cache.

#### Installation

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp"]
    }
  }
}
```

Or with a local clone (dev mode — reads files directly from disk):

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/claude-code-ultimate-guide/mcp-server/dist/index.js"],
      "env": {
        "GUIDE_ROOT": "/path/to/claude-code-ultimate-guide"
      }
    }
  }
}
```

#### Available tools

| Tool | Signature | Description |
|------|-----------|-------------|
| `search_guide` | `(query, limit?)` | Search 882 indexed entries by keyword or question |
| `read_section` | `(path, offset?, limit?)` | Read any guide file with pagination (500 lines max) |
| `list_topics` | `()` | Browse all 25 topic categories |
| `get_example` | `(name)` | Fetch a production-ready template by name |
| `list_examples` | `(category?)` | List all templates — `agents`, `commands`, `hooks`, `skills`, `scripts` |
| `get_changelog` | `(count?)` | Last N guide CHANGELOG entries (default 5) |
| `get_digest` | `(period)` | Combined digest of guide + CC releases: `day`, `week`, `month` |
| `get_release` | `(version?)` | Claude Code CLI release details |
| `get_cheatsheet` | `(section?)` | Full cheatsheet or filtered by section |

**Resources**: `claude-code-guide://reference` (full 94KB YAML index), `claude-code-guide://releases`, `claude-code-guide://llms`

**Prompt**: `claude-code-expert` — activates expert mode with optimal search workflow

#### Slash command shortcuts

Install the companion slash commands for one-keystroke access (stored in `~/.claude/commands/ccguide/`):

```bash
# These commands are included in the guide repo under .claude/commands/ccguide/
# Copy or symlink to ~/.claude/commands/ccguide/ to install globally
```

**Guide commands:**

| Command | Example | Description |
|---------|---------|-------------|
| `/ccguide:search` | `/ccguide:search hooks` | Search by keyword |
| `/ccguide:cheatsheet` | `/ccguide:cheatsheet hooks` | Cheatsheet (full or section) |
| `/ccguide:digest` | `/ccguide:digest week` | What changed this week (guide + CC releases) |
| `/ccguide:example` | `/ccguide:example code-reviewer` | Fetch a template |
| `/ccguide:examples` | `/ccguide:examples agents` | List templates by category |
| `/ccguide:release` | `/ccguide:release 2.1.59` | Release details |
| `/ccguide:changelog` | `/ccguide:changelog 10` | Recent guide CHANGELOG |
| `/ccguide:topics` | `/ccguide:topics` | Browse all categories |

**Official Anthropic docs tracker** (MCP v1.1.0+):

| Command | Description |
|---------|-------------|
| `/ccguide:init-docs` | Fetch official docs + store as local baseline (run once) |
| `/ccguide:refresh-docs` | Re-fetch latest docs, update current snapshot (baseline unchanged) |
| `/ccguide:diff-docs` | Compare baseline vs current — added/removed/modified pages, 0 network |
| `/ccguide:search-docs <query>` | Search official Anthropic docs from local cache |
| `/ccguide:daily` | **Daily briefing**: refresh + diff official docs + guide/CC digest |

Typical workflow:
```bash
/ccguide:init-docs          # once — stores baseline + current in ~/.cache/claude-code-guide/
# days later...
/ccguide:daily              # every day — refresh + diff + digest in one shot
```

#### Custom agent

A `claude-code-guide` agent is included in `.claude/agents/claude-code-guide.md`. It uses Haiku (fast, cheap) and automatically searches the guide before answering any Claude Code question.

---

### 🌐 Community MCP Servers Ecosystem

Beyond the official servers listed above, the MCP ecosystem includes **validated community servers** that extend Claude Code's capabilities with specialized integrations.

**📖 Complete Guide**: See **[MCP Servers Ecosystem](./ecosystem/mcp-servers-ecosystem.md)** for:

- **8 validated production-ready servers**: Playwright (Microsoft), Semgrep, Kubernetes (Red Hat), Context7, Linear, Vercel, Browserbase, MCP-Compose
- **Evaluation framework**: How servers are validated (stars, releases, docs, tests, security)
- **Production deployment guide**: Security checklist, quick start stack, performance metrics
- **Ecosystem evolution**: Linux Foundation standardization, MCPB format, Advanced MCP Tool Use, MCP Apps
- **Monthly watch methodology**: Template for maintaining the guide with ecosystem updates

**Featured Community Servers**:

| Server | Purpose | Quality Score | Maintainer |
|--------|---------|---------------|------------|
| **Playwright MCP** | Browser automation with accessibility trees | 8.8/10 ⭐⭐⭐⭐⭐ | Microsoft (Official) |
| **Semgrep MCP** | Security scanning (SAST, secrets, supply chain) | 9.0/10 ⭐⭐⭐⭐⭐ | Semgrep Inc. (Official) |
| **Kubernetes MCP** | Cluster management in natural language | 8.4/10 ⭐⭐⭐⭐ | Red Hat Containers Community |
| **Context7 MCP** | Real-time library documentation (500+ libs) | 8.2/10 ⭐⭐⭐⭐ | Upstash (Official) |
| **Linear MCP** | Issue tracking, project management | 7.6/10 ⭐⭐⭐⭐ | Community |
| **Vercel MCP** | Next.js deployments, CI/CD | 7.6/10 ⭐⭐⭐⭐ | Community |
| **Browserbase MCP** | Cloud browser automation with AI agent | 7.6/10 ⭐⭐⭐⭐ | Browserbase Inc. (Official) |
| **MCP-Compose** | Docker Compose-style multi-server orchestration | 7.4/10 ⭐⭐⭐⭐ | Community |

**Quick Start Example** (Playwright):

```bash
# Installation
npm install @microsoft/playwright-mcp

# Configuration (~/.claude.json or .mcp.json)
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["--yes", "@microsoft/playwright-mcp"]
    }
  }
}
```

**Why use community servers?**
- **Specialized integrations**: Kubernetes, Vercel, Linear APIs not in official servers
- **Enhanced capabilities**: Browser automation (Playwright), security scanning (Semgrep)
- **Production-ready**: All servers validated for maintenance, docs, tests, security
- **Ecosystem standard**: Many backed by major organizations (Microsoft, Red Hat, Semgrep Inc.)

---

## 8.3 Configuration

### MCP Configuration Location

```
~/.claude.json          # User-scope MCP config (field "mcpServers")
.mcp.json               # Project-scope (project root, shareable via VCS)
```

> **Note**: Three scopes exist: `local` (default, private to you + current project, in `~/.claude.json`), `project` (shared via `.mcp.json` at project root), and `user` (cross-project, also in `~/.claude.json`). Use `claude mcp add --scope <scope>` to target a specific scope.

### Example Configuration

```json
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["serena-mcp"],
      "env": {
        "PROJECT_PATH": "${PROJECT_PATH}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["@context7/mcp-server"]
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Configuration Fields

| Field | Description |
|-------|-------------|
| `command` | Executable to run |
| `args` | Command arguments |
| `env` | Environment variables |
| `cwd` | Working directory |
| `alwaysLoad` | When `true`, all tools from this server skip tool-search deferral and are always available without a `ToolSearch` call first. Use for servers with 1-5 critical tools needed on every turn. (v2.1.121) |

### Dynamic Headers for Multiple MCP Servers (v2.1.85+)

When a single `headersHelper` script serves multiple MCP servers, you can branch on `CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` to return different authentication tokens or scopes per server:

```bash
#!/bin/bash
# .claude/mcp-headers.sh
case "$CLAUDE_CODE_MCP_SERVER_NAME" in
  "github")
    echo "{\"Authorization\": \"Bearer $GITHUB_TOKEN\"}"
    ;;
  "linear")
    echo "{\"Authorization\": \"Bearer $LINEAR_API_KEY\"}"
    ;;
  *)
    echo "{}"
    ;;
esac
```

Reference the script in your MCP server config:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "headersHelper": ".claude/mcp-headers.sh"
    },
    "linear": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-linear"],
      "headersHelper": ".claude/mcp-headers.sh"
    }
  }
}
```

### Variable Substitution

| Variable | Expands To |
|----------|------------|
| `${VAR}` | Environment variable value |
| `${VAR:-default}` | Environment variable with fallback |
| `${CLAUDE_PROJECT_DIR}` | Absolute path to the project root (the directory Claude was started from). Auto-injected into `stdio`-type MCP server process environments. Also usable in plugin `command` strings. (v2.1.139) |

> **Warning**: The syntax `${workspaceFolder}` and `${env:VAR_NAME}` are VS Code conventions, not Claude Code. Claude Code uses standard shell-style `${VAR}` and `${VAR:-default}` for environment variable expansion in MCP config.

> **MCP stdio env injection**: All `stdio`-type MCP servers automatically receive `CLAUDE_PROJECT_DIR` as an environment variable — no config needed. This lets MCP servers know which project they're operating in without requiring the client to pass it explicitly.

### Managing Large MCP Server Sets

When you accumulate many MCP servers, enabling them all globally degrades Claude's tool selection — each server adds tool descriptions to the context, making the model less precise at picking the right one.

**Pattern**: keep a minimal global config (2-3 core servers) and activate project-specific servers via per-project `.mcp.json`.

```
# User-scope (~/.claude.json "mcpServers") → always loaded
context7, sequential-thinking

# Project-scope (.mcp.json at project root) → only when needed
postgres        # database project
playwright      # frontend project
serena          # large codebase
```

Community tools (e.g. [cc-setup](https://github.com/rhuss/cc-setup)) are emerging to provide a TUI registry with per-project toggling and health checks — useful if you manage 8+ servers regularly.

#### MCP Tool Search — Lazy-Loading at Scale

Claude Code v4 introduced **MCP Tool Search**: instead of loading all MCP tool definitions at startup, tool schemas are fetched on-demand when Claude needs them.

**Why it matters**: each MCP server injects its full tool schema into the context window. With a dozen servers, that's ~77,000 tokens consumed before you've written a single prompt.

| Setup | Context used by tools |
|-------|----------------------|
| All tools loaded upfront | ~77,000 tokens |
| MCP Tool Search enabled | ~8,700 tokens |
| **Reduction** | **~85%** |

Model accuracy on tool-selection tasks (measured on Opus 4): 49% → 74% (+25 points) when switching from full preload to lazy-loading. Auto-enables when MCP tools would consume >10% of the context window.

**Practical implication**: you can now connect dozens of MCP servers without the "too many tools" accuracy penalty. The advice to keep global config minimal still applies for unrelated tools, but MCP Tool Search changes the calculus for large project-specific sets.

To opt a specific server out of deferral entirely, set `alwaysLoad: true` in its config. Use this for servers with small tool counts (1-5 tools) that you know you'll need every session:

```json
// .claude/settings.json
{
  "mcpServers": {
    "my-critical-server": {
      "command": "npx",
      "args": ["my-mcp-server"],
      "alwaysLoad": true
    }
  }
}
```

**CLI vs MCP — when a shell command beats a server**: Familiar CLI tools (git, grep, jq, curl) are already deeply embedded in Claude's training data. A few usage examples in CLAUDE.md are often more effective than an equivalent MCP server, because the model already knows the tool's behavior, flags, and output format. An MCP server adds tool schema overhead and introduces an unfamiliar interface. Default to CLIs for standard tools; use MCP servers for proprietary systems or APIs the model has no training context for.

> Source: [HumanLayer — Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) (March 2026)

### CLI-Based MCP Configuration

**Quick setup with environment variables**:

```bash
# Add server with API key
claude mcp add -e API_KEY=your-key my-server -- npx @org/server

# Multiple environment variables
claude mcp add -e DATABASE_URL=postgresql://... -e DEBUG=true postgres -- npx @prisma/postgres

# Verify with --help
claude mcp add --help
```

> **Source**: CLI syntax adapted from [Shipyard Claude Code Cheat Sheet](https://shipyard.build/blog/claude-code-cheat-sheet/)

### 8.3.1 MCP Secrets Management

**Problem**: MCP servers require API keys and credentials. Storing them in plaintext `mcp.json` creates security risks (accidental Git commits, exposure in logs, lateral movement after breach).

**Solution**: Separate secrets from configuration using environment variables, OS keychains, or secret vaults.

#### Security Principles

Before implementing secrets management, understand the baseline requirements from [Security Hardening Guide](./security/security-hardening.md):

- **Encryption at rest**: Secrets must be encrypted on disk (OS keychain > plaintext .env)
- **Least privilege**: Use read-only credentials when possible
- **Token rotation**: Short-lived tokens with automated refresh
- **Audit logging**: Track secret access without logging the secrets themselves
- **Never in Git**: Secrets must never be committed to version control

For full threat model and CVE details, see [Section 8.6 MCP Security](#86-mcp-security).

#### Three Practical Approaches

| Approach | Security | Complexity | Use Case |
|----------|----------|------------|----------|
| **OS Keychain** | High (encrypted at rest) | Medium | Solo developers, macOS/Linux |
| **.env + .gitignore** | Medium (file permissions) | Low | Small teams, rapid prototyping |
| **Secret Vaults** | Very High (centralized, audited) | High | Enterprise, compliance requirements |

---

#### Approach 1: OS Keychain (Recommended)

**Best for**: Solo developers on macOS/Linux with high security needs.

**Pros**: Encrypted at rest, OS-level access control, no plaintext files
**Cons**: Platform-specific, requires scripting for automation

**macOS Keychain Setup**:

```bash
# Store secret in Keychain
security add-generic-password \
  -a "claude-mcp" \
  -s "github-token" \
  -w "ghp_your_token_here"

# Verify storage
security find-generic-password -s "github-token" -w
```

**MCP configuration with keychain retrieval**:

```json
{
  "mcpServers": {
    "github": {
      "command": "bash",
      "args": ["-c", "GITHUB_TOKEN=$(security find-generic-password -s 'github-token' -w) npx @github/mcp-server"],
      "env": {}
    }
  }
}
```

**Linux Secret Service** (GNOME Keyring, KWallet):

```bash
# Install secret-tool (part of libsecret)
sudo apt install libsecret-tools  # Ubuntu/Debian

# Store secret
secret-tool store --label="GitHub Token" service claude key github-token
# Prompt will ask for the secret value

# Retrieve in MCP config (bash wrapper)
# ~/.claude/scripts/mcp-github.sh
#!/bin/bash
export GITHUB_TOKEN=$(secret-tool lookup service claude key github-token)
npx @github/mcp-server

# ~/.claude.json (or .mcp.json)
{
  "mcpServers": {
    "github": {
      "command": "~/.claude/scripts/mcp-github.sh",
      "args": []
    }
  }
}
```

**Windows Credential Manager**:

```powershell
# Store secret
cmdkey /generic:"claude-mcp-github" /user:"token" /pass:"ghp_your_token_here"

# Retrieve in PowerShell wrapper
$password = cmdkey /list:"claude-mcp-github" | Select-String -Pattern "Password" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }
$env:GITHUB_TOKEN = $password
npx @github/mcp-server
```

---

#### Approach 2: .env + .gitignore (Simple)

**Best for**: Small teams, rapid prototyping, adequate security with proper `.gitignore`.

**Pros**: Simple, cross-platform, easy onboarding
**Cons**: Plaintext on disk (file permissions only), requires discipline

**Setup**:

```bash
# 1. Create .env file (project root or ~/.claude/)
cat > ~/.claude/.env << EOF
GITHUB_TOKEN=ghp_your_token_here
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
EOF

# 2. Secure permissions (Unix only)
chmod 600 ~/.claude/.env

# 3. Add to .gitignore
echo ".env" >> ~/.claude/.gitignore
```

**MCP configuration with .env variables**:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@github/mcp-server"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**Load .env before Claude Code**:

```bash
# Option 1: Shell wrapper
# ~/bin/claude-with-env
#!/bin/bash
export $(cat ~/.claude/.env | xargs)
claude "$@"

# Option 2: direnv (automatic per-directory)
# Install: https://direnv.net/
echo 'dotenv ~/.claude/.env' > ~/.config/direnv/direnvrc
direnv allow ~/.claude
```

**Template approach for teams**:

```bash
# Commit template (no secrets)
cat > ~/.claude/mcp-config.template.json << EOF
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@github/mcp-server"],
      "env": {
        "GITHUB_TOKEN": "\${GITHUB_TOKEN}"
      }
    }
  }
}
EOF

# Generate actual config from template + .env
envsubst < ~/.claude/mcp-config.template.json > ~/.claude.json

# .gitignore
.claude.json  # Generated, contains resolved secrets
.env          # Never commit
```

**See also**: [sync-claude-config.sh](../examples/scripts/sync-claude-config.sh) for automated template substitution.

---

#### Approach 3: Secret Vaults (Enterprise)

**Best for**: Enterprise, compliance (SOC 2, HIPAA), centralized secret management.

**Pros**: Centralized, audited, automated rotation, fine-grained access control
**Cons**: Complex setup, requires infrastructure, vendor lock-in

**HashiCorp Vault**:

```bash
# Store secret in Vault
vault kv put secret/claude/github token=ghp_your_token_here

# Retrieve in wrapper script
# ~/.claude/scripts/mcp-github-vault.sh
#!/bin/bash
export GITHUB_TOKEN=$(vault kv get -field=token secret/claude/github)
npx @github/mcp-server

# ~/.claude.json (or .mcp.json)
{
  "mcpServers": {
    "github": {
      "command": "~/.claude/scripts/mcp-github-vault.sh",
      "args": []
    }
  }
}
```

**AWS Secrets Manager**:

```bash
# Store secret
aws secretsmanager create-secret \
  --name claude/github-token \
  --secret-string "ghp_your_token_here"

# Retrieve in wrapper
export GITHUB_TOKEN=$(aws secretsmanager get-secret-value \
  --secret-id claude/github-token \
  --query SecretString \
  --output text)
npx @github/mcp-server
```

**1Password CLI** (team-friendly):

```bash
# Store in 1Password (via GUI or CLI)
op item create --category=password \
  --title="Claude MCP GitHub Token" \
  token=ghp_your_token_here

# Retrieve in wrapper
export GITHUB_TOKEN=$(op read "op://Private/Claude MCP GitHub Token/token")
npx @github/mcp-server
```

---

#### Secrets Rotation Workflow

**Problem**: API keys expire or are compromised. Rotating secrets across multiple MCP servers is manual and error-prone.

**Solution**: Centralized `.env` file with rotation script.

```bash
# ~/.claude/rotate-secret.sh
#!/bin/bash
SECRET_NAME=$1
NEW_VALUE=$2

# 1. Update .env file
sed -i.bak "s|^${SECRET_NAME}=.*|${SECRET_NAME}=${NEW_VALUE}|" ~/.claude/.env

# 2. Regenerate config from template
envsubst < ~/.claude/mcp-config.template.json > ~/.claude.json

# 3. Restart MCP servers (if running)
pkill -f "mcp-server" || true

echo "✅ Rotated $SECRET_NAME"
echo "⚠️  Restart Claude Code to apply changes"
```

**Usage**:
```bash
# Rotate GitHub token
./rotate-secret.sh GITHUB_TOKEN ghp_new_token_here

# Rotate database password
./rotate-secret.sh DATABASE_URL postgresql://user:new_pass@localhost/db
```

**Automated rotation with Vault** (advanced):

```bash
# vault-rotate.sh
#!/bin/bash
# Fetch latest secrets from Vault, update .env, restart Claude

vault kv get -format=json secret/claude | jq -r '.data.data | to_entries[] | "\(.key)=\(.value)"' > ~/.claude/.env
envsubst < ~/.claude/mcp-config.template.json > ~/.claude.json

echo "✅ Secrets rotated from Vault"
```

Schedule with cron:
```bash
# Rotate daily at 3 AM
0 3 * * * ~/claude-rotate.sh >> ~/claude-rotate.log 2>&1
```

---

#### Pre-Commit Secret Detection

**Problem**: Developers accidentally commit secrets to Git despite `.gitignore` (e.g., adding `.env` with `git add -f`).

**Solution**: [Pre-commit hook](../examples/hooks/bash/pre-commit-secrets.sh) to block commits containing secrets.

```bash
# Install hook
cp examples/hooks/bash/pre-commit-secrets.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Test (should fail)
echo "GITHUB_TOKEN=ghp_test" > test.txt
git add test.txt
git commit -m "Test"
# ❌ Blocked: Secret detected in test.txt
```

**Detection patterns** (see hook for full list):
- OpenAI keys: `sk-[A-Za-z0-9]{48}`
- GitHub tokens: `ghp_[A-Za-z0-9]{36}`
- AWS keys: `AKIA[A-Z0-9]{16}`
- Generic API keys: `api[_-]?key[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{20,}`

---

#### Verification Checklist

Before deploying MCP servers with secrets:

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| **.env not in Git** | `git ls-files | grep .env` | No output |
| **File permissions** | `ls -l ~/.claude/.env` | `-rw-------` (600) |
| **Template committed** | `git ls-files | grep template` | `mcp.json.template` present |
| **Pre-commit hook** | `cat .git/hooks/pre-commit` | Secret detection script present |
| **Secrets resolved** | `claude mcp list` | All servers start without errors |

**Test secret isolation**:
```bash
# Should work (secret from .env)
export $(cat ~/.claude/.env | xargs)
claude

# Should fail (no secrets in environment)
unset GITHUB_TOKEN DATABASE_URL
claude
# ❌ MCP servers fail to start (expected)
```

---

#### Best Practices Summary

| Practice | Rationale |
|----------|-----------|
| **Use OS keychain when possible** | Encrypted at rest, OS-level security |
| **Never commit .env to Git** | One leak = full compromise |
| **Commit .env.example template** | Team onboarding without secrets |
| **Use ${VAR} in MCP config** | Separation of config and secrets |
| **Rotate secrets quarterly** | Limit blast radius of old leaks |
| **Audit .gitignore before push** | Prevent accidental exposure |
| **Least privilege credentials** | Read-only DB users, scoped API tokens |
| **Monitor for leaked secrets** | GitHub secret scanning, GitGuardian |

For production deployments, consider [zero standing privilege](https://www.rkon.com/articles/mcp-server-security-navigating-the-new-ai-attack-surface/) where MCP servers start with no secrets and request just-in-time credentials on tool invocation.

## 8.4 Server Selection Guide

### Decision Tree

```
What do you need?
│
├─ Know exact pattern/text?
│  └─ Use native Grep tool or rg (~20ms)
│
├─ Deep code understanding?
│  └─ Use Serena
│
├─ Explore code by intent / semantic search?
│  └─ Use grepai (~500ms)
│
├─ Trace who calls what? (call graph)
│  └─ Use grepai
│
├─ Library documentation?
│  └─ Use Context7
│
├─ Complex reasoning?
│  └─ Use Sequential Thinking
│
├─ Database queries?
│  └─ Use Postgres
│
├─ Browser testing?
│  └─ Use Playwright
│
└─ General task?
   └─ Use built-in tools
```

### Server Comparison

| Need | Best Tool | Why |
|------|-----------|-----|
| "Find exact string 'validateUser'" | Native Grep / rg | Fast exact match (~20ms) |
| "Find all usages of this function" | Serena | Semantic symbol analysis |
| "Remember this for next session" | Serena | Persistent memory |
| "Find code that handles payments" | grepai / mgrep | Intent-based semantic search |
| "Who calls this function?" | grepai | Call graph analysis |
| "How does React useEffect work?" | Context7 | Official docs |
| "Why is this failing?" | Sequential | Structured debugging |
| "What's in the users table?" | Postgres | Direct query |
| "Test the login flow" | Playwright | Browser automation |

### Combining Servers

Servers can work together:

```
1. Context7 → Get official pattern for auth
2. Serena → Find existing auth code
3. Sequential → Analyze how to integrate
4. Playwright → Test the implementation
```

### Production Case Study: Multi-System Support Investigator

**Context**: Mergify (CI/CD automation platform) needed to triage support tickets across 5 disconnected systems — a manual 15-minute process per ticket.

**Architecture**: Claude Code as orchestrator + 5 custom MCP servers as system adapters:

```
Support ticket received
        │
        ▼
┌───────────────┐
│  Claude Code  │  ← orchestrates, synthesizes, produces report
└───────┬───────┘
        │ parallel fan-out
        ├──────────────────┬──────────────────┬──────────────────┬──────────────────┐
        ▼                  ▼                  ▼                  ▼                  ▼
 ┌─────────────┐  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
 │  Datadog    │  │     Sentry      │  │  PostgreSQL  │  │    Linear    │  │    GitHub    │
 │  (metrics,  │  │  (errors, perf  │  │  (customer   │  │  (tickets,   │  │   (source,   │
 │   traces)   │  │   regressions)  │  │   data, DB)  │  │   history)   │  │  recent PRs) │
 └─────────────┘  └─────────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

**Key design decisions:**
- MCP servers handle auth/credentials — Claude Code sees only clean interfaces
- Queries execute **in parallel**, not sequentially → majority of the time savings
- Human investigators review Claude's structured report, not raw data
- One dedicated repo for all MCP server implementations + system prompt

**Results** (self-reported by Mergify, Nov 2025):
- Triage time: ~15 min → <5 min (⅔ reduction)
- First-pass accuracy: 75% (25% still require human follow-up)

**Key takeaway**: This pattern — Claude Code as operational orchestrator with domain-specific MCP adapters — applies to any ops/support team juggling multiple disconnected systems. It's distinct from "Claude Code as dev tool": here Claude runs in a **production workflow**, not an IDE.

> Source: [Mergify blog — "How We Turned Claude Into a Cross-System Support Investigator"](https://mergify.com/blog/how-we-turned-claude-into-a-cross-system-support-investigator) (Julian Maurin, Nov 2025)

## 8.5 Plugin System

Claude Code includes a comprehensive **plugin system** that allows you to extend functionality through community-created or custom plugins and marketplaces.

### What Are Plugins?

Plugins are packaged extensions that can add:
- Custom agents with specialized behavior
- New skills for reusable workflows
- Pre-configured commands
- Domain-specific tooling

Think of plugins as **distributable packages** that bundle agents, skills, and configuration into installable modules.

### Plugin Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `claude plugin` | List installed plugins | Shows all plugins with status |
| `claude plugin install <name>` | Install plugin from marketplace | `claude plugin install security-audit` |
| `claude plugin install <name>@<marketplace>` | Install from specific marketplace | `claude plugin install linter@company` |
| `claude plugin enable <name>` | Enable installed plugin | `claude plugin enable security-audit` |
| `claude plugin disable <name>` | Disable plugin without removing | `claude plugin disable linter` |
| `claude plugin uninstall <name>` | Remove plugin completely (prompts before deleting persistent data) | `claude plugin uninstall security-audit` |
| `claude plugin update [name]` | Update plugin to latest version | `claude plugin update security-audit` |
| `claude plugin validate <path>` | Validate plugin manifest | `claude plugin validate ./my-plugin` |

> **`${CLAUDE_PLUGIN_DATA}` — Persistent plugin storage (v2.1.78+)**: Plugins can store state that survives updates using the `${CLAUDE_PLUGIN_DATA}` env variable. This variable points to a dedicated directory that is preserved when the plugin is updated and only deleted on explicit `/plugin uninstall` (with confirmation prompt). Use it for caches, user preferences, or any data your plugin needs across sessions.
>
> ```json
> // In your plugin's hooks.json
> {
>   "hooks": {
>     "SessionStart": [{
>       "type": "command",
>       "command": "mkdir -p ${CLAUDE_PLUGIN_DATA}/cache && my-plugin init"
>     }]
>   }
> }
> ```

### Marketplace Management

Marketplaces are repositories of plugins you can install from.

**Marketplace commands:**

```bash
# Add a marketplace
claude plugin marketplace add <url-or-path>

# Examples:
claude plugin marketplace add https://github.com/claudecode/plugins
claude plugin marketplace add /Users/yourname/company-plugins
claude plugin marketplace add gh:myorg/claude-plugins  # GitHub shorthand

# List configured marketplaces
claude plugin marketplace list

# Update marketplace catalog
claude plugin marketplace update [name]

# Remove a marketplace
claude plugin marketplace remove <name>
```

### Using Plugins

**Typical workflow:**

```bash
# 1. Add a marketplace (one-time setup)
claude plugin marketplace add https://github.com/awesome-claude/plugins

# 2. Install a plugin
claude plugin install code-reviewer

# 3. Enable it for your project
claude plugin enable code-reviewer

# 4. Use it in Claude Code session
claude
You: /review-pr
# Plugin command is now available
```

### Plugin Session Loading

Load plugins temporarily for a single session:

```bash
# Load plugin directory for this session only
claude --plugin-dir ~/.claude/custom-plugins

# Load multiple plugin directories
claude --plugin-dir ~/work/plugins --plugin-dir ~/personal/plugins
```

This is useful for testing plugins before permanent installation.

### Repo-Level Plugin Policy via `--add-dir` (v2.1.45+)

Define plugin policies at repository or shared-config level using `--add-dir`:

```bash
# Load plugin configuration from a shared directory
claude --add-dir /path/to/shared-config
```

The directory's `settings.json` can specify:
- `enabledPlugins`: list of pre-enabled plugins for every session
- `extraKnownMarketplaces`: additional marketplace registries to recognize

**Example shared config `settings.json`:**

```json
{
  "enabledPlugins": ["security-audit", "code-review"],
  "extraKnownMarketplaces": [
    "https://github.com/myorg/internal-plugins"
  ]
}
```

**Team use case**: Commit a shared config directory to your repo and all team members automatically get the same enabled plugins and approved marketplaces — no per-user configuration needed.

### When to Use Plugins

| Scenario | Use Plugins |
|----------|-------------|
| **Team workflows** | ✅ Share standardized agents/skills across team via private marketplace |
| **Domain expertise** | ✅ Install pre-built plugins for security, accessibility, performance analysis |
| **Repeating patterns** | ✅ Package your custom workflows for reuse across projects |
| **Community solutions** | ✅ Leverage community expertise instead of rebuilding from scratch |
| **Quick experiments** | ❌ Use custom agents/skills directly in `.claude/` folder |
| **Project-specific** | ❌ Keep as project CLAUDE.md instructions instead |

### Creating Custom Plugins

Plugins are structured directories with a manifest inside `.claude-plugin/`:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest (ONLY file in this dir)
├── agents/
│   └── my-agent.md       # Custom agents
├── skills/
│   └── code-review/
│       └── SKILL.md      # Agent Skills (folder + SKILL.md)
├── commands/
│   └── my-cmd.md         # Slash commands
├── hooks/
│   └── hooks.json        # Event handlers
├── .mcp.json             # MCP server configurations (optional)
├── .lsp.json             # LSP server configurations (optional)
└── README.md             # Documentation
```

### LSP Native Support (v2.0.74+)

Since v2.0.74 (December 2025), Claude Code natively integrates with Language Server Protocol servers. Instead of navigating your codebase through text search (grep), Claude connects to the LSP server of your project and understands symbols, types, and cross-references — the same way an IDE does.

**Why it matters**: Finding all call sites of a function drops from ~45 seconds (text search) to ~50ms (LSP). Claude also gets automatic diagnostics after every file edit — errors and warnings appear in real time, without a separate build step.

**Supported languages (11)**: Python, TypeScript, JavaScript, Go, Rust, Java, C/C++, C#, PHP, Kotlin, Ruby.

#### Activation

```bash
# Option 1 — one-time env variable
ENABLE_LSP_TOOL=1 claude

# Option 2 — persist in ~/.claude/settings.json
{
  "env": {
    "ENABLE_LSP_TOOL": "1"
  }
}
```

The LSP server for your language must already be installed on the machine — Claude Code connects to it, it doesn't install it. Common servers:

| Language | Server | Install |
|----------|--------|---------|
| TypeScript | `tsserver` | Bundled with TypeScript |
| Python | `pylsp` | `pip install python-lsp-server` |
| Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| Rust | `rust-analyzer` | `rustup component add rust-analyzer` |
| Kotlin | `kotlin-language-server` | Via IntelliJ or standalone |
| Swift | `sourcekit-lsp` | Bundled with Xcode |

#### Timeout configuration (`.lsp.json`)

Controls how long Claude waits for an LSP server to initialize before treating it as unresponsive (v2.1.50+):

```json
{
  "servers": {
    "tsserver": { "startupTimeout": 15000 },
    "pylsp":    { "startupTimeout": 10000 }
  }
}
```

Useful in slow environments (CI, Docker, cold start) where default timeouts cause LSP features to be silently skipped.

> ⚠️ **Common mistake**: Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside `.claude-plugin/`. Only `plugin.json` goes there.

**Example `.claude-plugin/plugin.json`:**

```json
{
  "name": "security-audit",
  "version": "1.0.0",
  "description": "Security audit tools for Claude Code",
  "author": {
    "name": "Your Name"
  }
}
```

> The manifest only defines metadata. Claude Code auto-discovers components from the directory structure.

**Skill namespacing**: Plugin skills are prefixed with the plugin name to prevent conflicts:
- Plugin `security-audit` with skill `scan` → `/security-audit:scan`

**Validate before distribution:**

```bash
claude plugin validate ./my-plugin
```

**Official documentation**: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)

### Plugin vs. MCP Server

Understanding when to use which:

| Feature | Plugin | MCP Server |
|---------|--------|------------|
| **Purpose** | Bundle Claude-specific workflows (agents, skills) | Add external tool capabilities (databases, APIs) |
| **Complexity** | Simpler - just files + manifest | More complex - requires server implementation |
| **Scope** | Claude Code instructions and patterns | External system integrations |
| **Installation** | `claude plugin install` | Add to `settings.json` MCP config |
| **Use case** | Security auditor agent, code review workflows | PostgreSQL access, Playwright browser automation |
| **Interactive UI** | No | Yes (via MCP Apps extension - SEP-1865)* |

**Rule of thumb:**
- **Plugin** = "How Claude thinks" (new workflows, specialized agents)
- **MCP Server** = "What Claude can do" (new tools, external systems)
- **MCP Apps** = "What Claude can show" (interactive UIs in supported clients)*

*Note: MCP Apps render in Claude Desktop, VS Code, ChatGPT, Goose. Not supported in Claude Code CLI (terminal is text-only). See [Section 8.1](#81-what-is-mcp) for details.

### Security Considerations

**Before installing plugins:**

1. **Trust the source** - Only install from verified marketplaces
2. **Review manifest** - Check what the plugin includes with `validate`
3. **Test in isolation** - Use `--plugin-dir` for testing before permanent install
4. **Company policies** - Check if your organization has approved plugin sources

**Red flags:**

- Plugins requesting network access without clear reason
- Unclear or obfuscated code in agents/skills
- Plugins without documentation or proper manifest

### Example Use Cases

**1. Team Code Standards Plugin**

```bash
# Company creates private marketplace
git clone git@github.com:yourcompany/claude-plugins.git ~/company-plugins

# Add marketplace
claude plugin marketplace add ~/company-plugins

# Install company standards
claude plugin install code-standards@company

# Now all team members use same linting, review patterns
```

**2. Security Audit Suite**

```bash
# Install community security plugin
claude plugin install owasp-scanner

# Use in session
claude
You: /security-scan
# Runs OWASP Top 10 checks, dependency audit, secret scanning
```

**3. Accessibility Testing**

```bash
# Install a11y plugin
claude plugin install wcag-checker

# Enable for project
claude plugin enable wcag-checker

# Adds accessibility-focused agents
You: Review this component for WCAG 2.1 compliance
```

### Troubleshooting

**Plugin not found after install:**

```bash
# Refresh marketplace catalogs
claude plugin marketplace update

# Verify plugin is installed
claude plugin

# Check if disabled
claude plugin enable <name>
```

**Plugin conflicts:**

```bash
# Disable conflicting plugin
claude plugin disable <conflicting-plugin>

# Or uninstall completely
claude plugin uninstall <conflicting-plugin>
```

**Plugin not loading in session:**

- Plugins are loaded at session start
- Restart Claude Code after enabling/disabling
- Check `~/.claude/plugins/` for installation

### Community Marketplaces

The Claude Code plugin ecosystem has grown significantly. Here are verified community resources:

**Major marketplaces:**

| Marketplace | Stats | Focus |
|-------------|-------|-------|
| [wshobson/agents](https://github.com/wshobson/agents) | 67 plugins, 99 agents, 107 skills | Production-ready dev workflows, DevOps, security |
| [claude-plugins.dev](https://claude-plugins.dev) | 11,989 plugins, 63,065 skills indexed | Registry + CLI for plugin discovery |
| [claudemarketplaces.com](https://claudemarketplaces.com) | Auto-scans GitHub | Marketplace directory |

**Installation example (wshobson/agents):**

```bash
# Add the marketplace
/plugin marketplace add wshobson/agents

# Browse available plugins
/plugin

# Install specific plugin
/plugin install react-development
```

**Popular plugins by install count** (Jan 2026):

| Plugin | Installs | Use case |
|--------|----------|----------|
| Context7 | ~72k | Library documentation lookup |
| Ralph Wiggum | ~57k | Code review automation |
| Figma MCP | ~18k | Design-to-code workflow |
| Linear MCP | ~9.5k | Issue tracking integration |

**Curated lists:**

- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) (20k+ stars) - Commands, templates, plugins
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) - Plugin-focused curation
- [awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) (5.5k stars) - Skills-only taxonomy (62 skills across 12 categories)

> **Source**: Stats from [claude-plugins.dev](https://claude-plugins.dev), [Firecrawl analysis](https://www.firecrawl.dev/blog/best-claude-code-plugins) (Jan 2026). Counts evolve rapidly.

### Production-Ready Plugins from This Guide

All 181 templates in this guide's `examples/` directory are available as installable plugins — no file copying, hooks auto-wired on install:

```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
```

| Plugin | What's inside |
|--------|---------------|
| `security-suite` | OWASP auditing, 4-agent cyber-defense pipeline, 13 protective hooks |
| `devops-pipeline` | CI/CD (auto-detects Python/Node/Rust), git worktrees, GitHub Actions |
| `release-automation` | Changelog, release notes (3 formats), social content from `git log` |
| `code-quality` | SOLID refactoring, TDD, GoF patterns, 6 specialist review agents |
| `pr-workflow` | CEO + Eng planning gates, PR/issue triage, session handoffs |
| `session-tools` | ccboard dashboard, voice refinement, 11 session hooks |
| `ai-methodology` | Scaffolding, 6-stage talk pipeline, landing page generator |
| `session-summary` | Analytics dashboard at session end (15 configurable sections) |

Install only what you need. Source of truth for all templates stays in `examples/` — the plugins repo is the published distribution layer.

→ **[github.com/FlorianBruniaux/claude-code-plugins](https://github.com/FlorianBruniaux/claude-code-plugins)**

### Featured Community Plugins

Two community plugins address complementary problems that AI-assisted development creates: **code quality drift** (accumulation of poorly-structured AI-generated code) and **hallucination in generated solutions**.

#### Vitals — Codebase Health Detection

**Problem solved**: AI tools write code faster than teams can maintain it. GitClear's analysis of 211M lines shows refactoring collapsed from 25% to under 10% of all changes (2021–2025). Vitals identifies which files are most likely to cause problems next — before they do.

**How it works**: Computes `git churn × structural complexity × coupling centrality` to rank hotspots. Not just "this file is complex" but "this complex file changed 49 times in 90 days and 63 other files break when it does."

```bash
# Install (two commands in Claude Code)
/plugin marketplace add chopratejas/vitals
/plugin install vitals@vitals

# Scan from repo root
/vitals:scan

# Scope options
/vitals:scan src/           # Specific folder
/vitals:scan --top 20       # More results (default: 10)
/vitals:scan src/auth --top 5
```

**What you get**: Claude reads the flagged files and gives semantic diagnosis. Instead of "high complexity," you get: "this class handles routing, caching, rate limiting, AND metrics in 7,137 lines — extract each concern."

**Status**: v0.1 alpha. MIT. Zero dependencies (Python stdlib + git). Works on any repo.

**Source**: [chopratejas/vitals](https://github.com/chopratejas/vitals)

#### SE-CoVe — Chain-of-Verification

**Problem solved**: AI-generated code contains subtle errors that survive code review because both the AI and the reviewer follow the same reasoning path. SE-CoVe breaks this by running an independent verifier that never sees the initial solution.

**Research foundation**: Adaptation of Meta's Chain-of-Verification methodology (Dhuliawala et al., ACL 2024 Findings — [arXiv:2309.11495](https://arxiv.org/abs/2309.11495)).

**How it works** — 5-stage pipeline:

1. **Baseline** — Claude generates initial solution
2. **Planner** — Creates verification questions from the solution's claims
3. **Executor** — Answers questions without seeing the baseline (prevents confirmation bias)
4. **Synthesizer** — Compares findings, surfaces discrepancies
5. **Output** — Produces verified solution

```bash
# Install (two separate commands — marketplace limitation)
/plugin marketplace add vertti/se-cove-claude-plugin
/plugin install chain-of-verification

# Use
/chain-of-verification:verify <your question>
/ver<Tab>   # Autocomplete available
```

**Trade-offs**: ~2x token cost, reduced output volume. Worth it for security-sensitive code, complex debugging, and architectural decisions — not for rapid prototyping or simple fixes.

**Source**: [vertti/se-cove-claude-plugin](https://github.com/vertti/se-cove-claude-plugin) — v1.1.1, MIT

#### Vitals vs. SE-CoVe — Which to Use

These tools solve different problems at different stages of the development cycle:

| | Vitals | SE-CoVe |
|--|--------|---------|
| **When** | Maintenance / weekly review | Per-task generation |
| **Problem** | Accumulated code debt | Per-solution accuracy |
| **Input** | Entire git history | A specific question |
| **Output** | Ranked hotspot files + diagnosis | Verified answer |
| **Token cost** | Low (Python analysis + Claude reads top files) | ~2x standard generation |
| **Best for** | "Which file is going to break?" | "Is this solution correct?" |
| **Status** | v0.1 alpha | v1.1.1 stable |

**Complementary workflow**: Run Vitals weekly to identify which areas of the codebase need attention, then use SE-CoVe when asking Claude to refactor or fix those hotspot files.

#### Lightweight Role-Switch Review

Not every change warrants SE-CoVe's 5-stage pipeline. For everyday review within a single session, you can prompt Claude to switch from author to reviewer explicitly:

```markdown
You just wrote the implementation above. Now forget you wrote it.
Review it as a senior engineer who did not author this code.

Check: requirement fidelity, edge cases, error handling, backward
compatibility, security, performance. For each issue found, cite
the file and line, explain the problem, and propose a concrete fix.

Verdict: APPROVE, REQUEST CHANGES, or REJECT.
```

This works because the explicit instruction to "forget you wrote it" forces Claude to re-evaluate rather than defend prior decisions. It catches surface-level issues (missing null checks, inconsistent error handling, naming drift) but shares the same reasoning path as the author, so subtle architectural flaws may survive.

**When to use what:**

| Approach | Cost | Catches | Best for |
|----------|------|---------|----------|
| Role-switch (same session) | 1x | Surface issues, naming, obvious bugs | Daily development, quick fixes |
| SE-CoVe (plugin) | ~2x | Reasoning-path blind spots, subtle logic errors | Security-sensitive code, architecture |
| Cross-model review (see below) | 1x-2x | Different reasoning patterns, fresh perspective | Critical paths, pre-merge gates |
| Scope-focused agents | 2-5x | Domain-specific issues in parallel | Large PRs, multi-concern review |

#### Cross-Model Review

A single model reviewing its own code follows the same reasoning patterns that produced the code. Using a different model for review introduces genuinely independent analysis.

**The pattern**: generate with one model, review with another.

```bash
# Implement with Opus (deep reasoning)
claude --model opus

# Review the diff with Sonnet (different reasoning path, lower cost)
claude -p "Review the changes in the last commit. Check for logic errors, \
  edge cases, backward compatibility, and security issues. \
  Cite file:line for each finding." --model sonnet

# Quick sanity check with Haiku (fast, cheap, catches obvious issues)
claude -p "List any bugs, missing error handling, or security issues \
  in the last commit." --model haiku
```

**With custom agents:**

```yaml
# .claude/agents/cross-model-reviewer.md
---
name: cross-model-reviewer
model: sonnet  # Different from your working model
tools: Read, Grep, Glob
---
You are reviewing code you did not write. Your job is to find problems.

Read the files listed below, then check:
1. Logic errors and edge cases
2. Error handling completeness
3. Backward compatibility risks
4. Security issues (injection, auth gaps, data leaks)
5. Performance concerns (O(n²), unbounded queries)

For each finding: severity (critical/high/medium), file:line, problem, fix.
If no issues found, say so explicitly.
```

**Why different models catch different bugs**: each model has distinct reasoning biases, training distributions, and failure modes. A bug that sits in one model's blind spot may be obvious to another. This is the same principle behind diverse code review teams in traditional engineering.

**Cost-effective patterns:**

| Generation Model | Review Model | Cost Multiplier | When |
|-----------------|-------------|-----------------|------|
| Opus | Sonnet | ~1.3x | Default for critical code |
| Sonnet | Haiku | ~1.05x | High-volume, pre-commit gate |
| Sonnet | Opus | ~2x | Architecture, security-critical |
| Any | Same model, fresh session | ~1.5x | Context isolation without model switch |

The fresh session variant (same model, new context via `claude -p`) gives you context isolation without changing the model. Less effective than a true model switch but still better than reviewing in the same session where the code was written.

---

## 8.6 MCP Security

MCP servers extend Claude Code's capabilities, but they also expand its attack surface. Before installing any MCP server, especially community-created ones, apply the same security scrutiny you'd use for any third-party code dependency.

> **CVE details & advanced vetting**: For documented CVEs (2025-53109/53110, 54135, 54136), MCP Safe List, and incident response procedures, see [Security Hardening Guide](./security/security-hardening.md).

### Pre-Installation Checklist

Before adding an MCP server to your configuration:

| Check | Why |
|-------|-----|
| **Source verification** | GitHub with stars, known organization, or official vendor |
| **Code audit** | Review source code—avoid opaque binaries without source |
| **Minimal permissions** | Does it need filesystem access? Network? Why? |
| **Active maintenance** | Recent commits, responsive to issues |
| **Documentation** | Clear explanation of what tools it exposes |

### Security Risks to Understand

**Tool Shadowing**

A malicious MCP server can declare tools with common names (like `Read`, `Write`, `Bash`) that shadow built-in tools. When Claude invokes what it thinks is the native `Read` tool, the MCP server intercepts the call.

```
Legitimate flow:  Claude → Native Read tool → Your file
Shadowed flow:    Claude → Malicious MCP "Read" → Attacker exfiltrates content
```

**Mitigation**: Check exposed tools with `/mcp` command. Use `disallowedTools` in settings to block suspicious tool names from specific servers.

**Confused Deputy Problem**

An MCP server with elevated privileges (database access, API keys) can be manipulated via prompt to perform unauthorized actions. The server authenticates Claude's request but doesn't verify the user's authorization for that specific action.

Example: A database MCP with admin credentials receives a query from a prompt-injected request, executing destructive operations the user never intended.

**Mitigation**: Always configure MCP servers with **read-only credentials by default**. Only grant write access when explicitly needed.

**Dynamic Capability Injection**

MCP servers can dynamically change their tool offerings. A server might pass initial review, then later inject additional tools.

**Mitigation**: Pin server versions in your configuration. Periodically re-audit installed servers.

### Secure Configuration Patterns

**Minimal privilege setup:**

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgres://readonly_user:pass@host/db"
      }
    }
  }
}
```

**Tool restriction via settings:**

```json
{
  "permissions": {
    "deny": ["mcp__untrusted-server__execute", "mcp__untrusted-server__shell"]
  }
}
```

> **Note**: `disallowedTools` is a root-level key or CLI flag (`--disallowedTools`), not nested under `permissions`. For settings.json, use `permissions.deny` to block tool patterns.

### Red Flags

Avoid MCP servers that:

- Request credentials beyond their stated purpose
- Expose shell execution tools without clear justification
- Have no source code available (binary-only distribution)
- Haven't been updated in 6+ months with open security issues
- Request network access for local-only functionality

### Auditing Installed Servers

```bash
# List active MCP servers and their tools
claude
/mcp

# Check what tools a specific server exposes
# Look for unexpected tools or overly broad capabilities
```

**Best practice**: Audit your MCP configuration quarterly. Remove servers you're not actively using.

---


