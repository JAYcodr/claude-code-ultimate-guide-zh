<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

---

title: "The Ultimate Claude Code Guide"
description: "Comprehensive self-contained guide to mastering Claude Code from zero to power user"
tags: [guide, reference, workflows, agents, hooks, mcp, security]

---

# The Ultimate Claude Code Guide

> A comprehensive, self-contained guide to mastering Claude Code - from zero to power user.

**Author**: Florian BRUNIAUX | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Written with**: Claude (Anthropic)

**Reading time**: ~30-40 hours (full) | ~15 minutes (Quick Start only)

**Last updated**: January 2026

**Version**: 3.40.0

---

## Before You Start

**This guide is not official Anthropic documentation.** It's a community resource based on my exploration of Claude Code over several months.

**What you'll find:**
- Patterns that have worked for me
- Observations that may not generalize to your workflow
- Time estimates and percentages that are rough approximations, not measurements

**What you won't find:**
- Definitive answers (the tool is too new)
- Benchmarked performance claims
- Guarantees that any technique will work for you

**Use critically. Experiment. Share what works for you.**

> **⚠️ Note (Jan 2026)**: If you've heard about **ClawdBot** recently, that's a **different tool**. ClawdBot is a self-hosted chatbot assistant accessible via messaging apps (Telegram, WhatsApp, etc.), designed for personal automation and smart home use cases. Claude Code is a CLI tool for developers (terminal/IDE integration) focused on software development workflows. Both use Claude models but serve distinct audiences and use cases.

---

## TL;DR - The 5-Minute Summary

If you only have 5 minutes, here's what you need to know:

### Essential Commands
```bash
claude                    # Start Claude Code
/help                     # Show all commands
/powerup                  # Interactive lessons: CLAUDE.md, /rewind, memory, effort modes
/status                   # Check context usage
/compact                  # Compress context when >70%
/clear                    # Fresh start
/plan                     # Safe read-only mode
Ctrl+C                    # Cancel operation
```

### The Workflow
```
Describe → Claude Analyzes → Review Diff → Accept/Reject → Verify
```

### Context Management (Critical!)
| Context % | Action |
|-----------|--------|
| 0-50% | Work freely |
| 50-70% | Be selective |
| 70-90% | `/compact` now |
| 90%+ | `/clear` required |

*These thresholds are based on my experience. Your optimal workflow may differ depending on task complexity and working style.*

### Memory Hierarchy
```
~/.claude/CLAUDE.md       → Global (all projects)
/project/CLAUDE.md        → Project (committed)
/project/.claude/         → Personal (not committed)
```

### Power Features
| Feature | What It Does |
|---------|--------------|
| **Agents** | Specialized AI personas for specific tasks |
| **Skills** | Reusable knowledge modules |
| **Hooks** | Automation scripts triggered by events |
| **MCP Servers** | External tools (Serena, Context7, Playwright...) |
| **Plugins** | Community-created extension packages |

### The Golden Rules
1. **Always review diffs** before accepting changes
2. **Use `/compact`** before context gets critical
3. **Be specific** in your requests (WHAT, WHERE, HOW, VERIFY)
4. **Start with Plan Mode** for complex/risky tasks
5. **Create CLAUDE.md** for every project

### Quick Decision Tree
```
Simple task → Just ask Claude
Complex task → Use TodoWrite to plan
Risky change → Enter Plan Mode first
Repeating task → Create an agent or command
Context full → /compact or /clear
```

**Now read Section 1 for the full Quick Start, or jump to any section you need.**

---

## Choose Your Path

The guide has 11 chapters and 22,000+ lines. You don't need to read everything — here's what matters for your situation:

| I am... | Read this | Skip this | Time |
|---------|-----------|-----------|------|
| **Developer, getting started** | Ch.1 → Ch.2 → Ch.3 | Ch.9, Ch.11, Appendix | 3h |
| **Developer, intermediate** | Ch.2.6 → Ch.4 → Ch.5 → Ch.7 | Ch.1, Ch.10 ref only | 4h |
| **Power user / senior** | Ch.9 (Advanced) → Ch.4-8 | Ch.1 Quick Start | 2h |
| **Tech Lead / EM** | Ch.3.5 → Ch.9.17 → Ch.9.20 → Ch.11 | Ch.5-6 detail | 1h30 |
| **Just need a reference** | Ch.10.5 Cheatsheet | Everything else | 5 min |

---

## Top 5 sections by ROI

If you only have time for 5 sections:

1. **[2.6 Mental Model](ultimate-guide/02-core-concepts.md#26-mental-model)** — Understand how Claude Code thinks (20 min)
2. **[3.1 CLAUDE.md](ultimate-guide/03-memory-settings.md#31-memory-files-claudemd)** — Persistent memory that survives sessions (30 min)
3. **[9.1 The Trinity](ultimate-guide/09-advanced-patterns.md#91-the-trinity)** — The core pattern for agentic work (20 min)
4. **[7.4 Security Hooks](ultimate-guide/07-hooks.md#74-security-hooks)** — Automate guardrails you won't forget (30 min)
5. **[10.5 Cheatsheet](ultimate-guide/10-reference.md#105-cheatsheet)** — Daily reference, bookmark it (5 min)

---

## Table of Contents

- [1. Quick Start (Day 1)](ultimate-guide/01-quick-start.md) `🟢 Beginner` `⏱ 45 min`
  - [1.1 Installation](ultimate-guide/01-quick-start.md#11-installation)
  - [1.2 First Workflow](ultimate-guide/01-quick-start.md#12-first-workflow)
  - [1.3 Essential Commands](ultimate-guide/01-quick-start.md#13-essential-commands)
  - [1.4 Permission Modes](ultimate-guide/01-quick-start.md#14-permission-modes)
  - [1.5 Productivity Checklist](ultimate-guide/01-quick-start.md#15-productivity-checklist)
  - [1.6 Migrating from Other AI Coding Tools](ultimate-guide/01-quick-start.md#16-migrating-from-other-ai-coding-tools)
  - [1.7 Trust Calibration](ultimate-guide/01-quick-start.md#17-trust-calibration-when-and-how-much-to-verify)
  - [1.8 Eight Beginner Mistakes](ultimate-guide/01-quick-start.md#18-eight-beginner-mistakes-and-how-to-avoid-them)
- [2. Core Concepts](ultimate-guide/02-core-concepts.md) `🟡 Intermediate` `⏱ 60 min`
  - [2.1 The Interaction Loop](ultimate-guide/02-core-concepts.md#21-the-interaction-loop)
  - [2.2 Context Management](ultimate-guide/02-core-concepts.md#22-context-management)
  - [2.3 Plan Mode](ultimate-guide/02-core-concepts.md#23-plan-mode) (incl. [Ultraplan](#ultraplan), [OpusPlan](#opusplan-mode))
  - [2.4 Rewind](ultimate-guide/02-core-concepts.md#24-rewind)
  - [2.5 Model Selection & Thinking Guide](ultimate-guide/02-core-concepts.md#25-model-selection--thinking-guide)
  - [2.6 Mental Model](ultimate-guide/02-core-concepts.md#26-mental-model)
  - [2.7 Configuration Decision Guide](ultimate-guide/02-core-concepts.md#27-configuration-decision-guide)
  - [2.8 Structured Prompting with XML Tags](ultimate-guide/02-core-concepts.md#28-structured-prompting-with-xml-tags)
  - [2.9 Semantic Anchors](ultimate-guide/02-core-concepts.md#29-semantic-anchors)
  - [2.10 Data Flow & Privacy](ultimate-guide/02-core-concepts.md#210-data-flow--privacy)
  - [2.11 Under the Hood](ultimate-guide/02-core-concepts.md#211-under-the-hood)
- [3. Memory & Settings](ultimate-guide/03-memory-settings.md) `🟢 Beginner` `⏱ 30 min`
  - [3.1 Memory Files (CLAUDE.md)](ultimate-guide/03-memory-settings.md#31-memory-files-claudemd)
  - [3.2 The .claude/ Folder Structure](ultimate-guide/03-memory-settings.md#32-the-claude-folder-structure)
  - [3.3 Settings & Permissions](ultimate-guide/03-memory-settings.md#33-settings--permissions)
  - [3.4 Precedence Rules](ultimate-guide/03-memory-settings.md#34-precedence-rules)
  - [3.5 Team Configuration at Scale](ultimate-guide/03-memory-settings.md#35-team-configuration-at-scale)
- [4. Agents](ultimate-guide/04-agents.md) `🟡 Intermediate` `⏱ 45 min`
  - [4.1 What Are Agents](ultimate-guide/04-agents.md#41-what-are-agents)
  - [4.2 Creating Custom Agents](ultimate-guide/04-agents.md#42-creating-custom-agents)
  - [4.3 Agent Template](ultimate-guide/04-agents.md#43-agent-template)
  - [4.4 Best Practices](ultimate-guide/04-agents.md#44-best-practices)
  - [4.5 Agent Memory](ultimate-guide/04-agents.md#45-agent-memory)
  - [4.6 Agent Examples](ultimate-guide/04-agents.md#46-agent-examples)
  - [4.7 Advanced Agent Patterns](ultimate-guide/04-agents.md#47-advanced-agent-patterns)
- [5. Skills](ultimate-guide/05-skills.md) `🟡 Intermediate` `⏱ 30 min`
  - [5.1 Understanding Skills](ultimate-guide/05-skills.md#51-understanding-skills)
  - [5.2 Creating Skills](ultimate-guide/05-skills.md#52-creating-skills)
  - [5.3 Skill Template](ultimate-guide/05-skills.md#53-skill-template)
  - [5.4 Skill Examples](ultimate-guide/05-skills.md#54-skill-examples)
- [6. Commands](ultimate-guide/06-commands.md) `🟡 Intermediate` `⏱ 30 min`
  - [6.1 Slash Commands](ultimate-guide/06-commands.md#61-slash-commands)
  - [6.2 Creating Custom Commands](ultimate-guide/06-commands.md#62-creating-custom-commands)
  - [6.3 Command Template](ultimate-guide/06-commands.md#63-command-template)
  - [6.4 Command Examples](ultimate-guide/06-commands.md#64-command-examples)
- [7. Hooks](ultimate-guide/07-hooks.md) `🟡 Intermediate` `⏱ 45 min`
  - [7.1 The Event System](ultimate-guide/07-hooks.md#71-the-event-system)
  - [7.2 Creating Hooks](ultimate-guide/07-hooks.md#72-creating-hooks)
  - [7.3 Hook Templates](ultimate-guide/07-hooks.md#73-hook-templates)
  - [7.4 Security Hooks](ultimate-guide/07-hooks.md#74-security-hooks)
  - [7.5 Hook Examples](ultimate-guide/07-hooks.md#75-hook-examples)
- [8. MCP Servers](ultimate-guide/08-mcp-servers.md) `🟡 Intermediate` `⏱ 40 min`
  - [8.1 What is MCP](ultimate-guide/08-mcp-servers.md#81-what-is-mcp)
  - [8.2 Available Servers](ultimate-guide/08-mcp-servers.md#82-available-servers)
  - [8.3 Configuration](ultimate-guide/08-mcp-servers.md#83-configuration)
  - [8.4 Server Selection Guide](ultimate-guide/08-mcp-servers.md#84-server-selection-guide)
  - [8.5 Plugin System](ultimate-guide/08-mcp-servers.md#85-plugin-system)
  - [8.6 MCP Security](ultimate-guide/08-mcp-servers.md#86-mcp-security)
- [9. Advanced Patterns](ultimate-guide/09-advanced-patterns.md) `🔴 Advanced` `⏱ 3h`
  - [9.1 The Trinity](ultimate-guide/09-advanced-patterns.md#91-the-trinity)
  - [9.2 Composition Patterns](ultimate-guide/09-advanced-patterns.md#92-composition-patterns)
  - [9.3 CI/CD Integration](ultimate-guide/09-advanced-patterns.md#93-cicd-integration)
  - [9.4 IDE Integration](ultimate-guide/09-advanced-patterns.md#94-ide-integration)
  - [9.5 Tight Feedback Loops](ultimate-guide/09-advanced-patterns.md#95-tight-feedback-loops)
  - [9.6 Todo as Instruction Mirrors](ultimate-guide/09-advanced-patterns.md#96-todo-as-instruction-mirrors)
  - [9.7 Output Styles](ultimate-guide/09-advanced-patterns.md#97-output-styles)
  - [9.8 Vibe Coding & Skeleton Projects](ultimate-guide/09-advanced-patterns.md#98-vibe-coding--skeleton-projects)
  - [9.9 Batch Operations Pattern](ultimate-guide/09-advanced-patterns.md#99-batch-operations-pattern)
  - [9.10 Continuous Improvement Mindset](ultimate-guide/09-advanced-patterns.md#910-continuous-improvement-mindset)
  - [9.11 Common Pitfalls & Best Practices](ultimate-guide/09-advanced-patterns.md#911-common-pitfalls--best-practices)
  - [9.12 Git Best Practices & Workflows](ultimate-guide/09-advanced-patterns.md#912-git-best-practices--workflows)
  - [9.13 Cost Optimization Strategies](ultimate-guide/09-advanced-patterns.md#913-cost-optimization-strategies)
  - [9.14 Development Methodologies](ultimate-guide/09-advanced-patterns.md#914-development-methodologies)
  - [9.15 Named Prompting Patterns](ultimate-guide/09-advanced-patterns.md#915-named-prompting-patterns)
  - [9.16 Session Teleportation](ultimate-guide/09-advanced-patterns.md#916-session-teleportation)
  - [9.17 Scaling Patterns: Multi-Instance Workflows](ultimate-guide/09-advanced-patterns.md#917-scaling-patterns-multi-instance-workflows)
  - [9.18 Codebase Design for Agent Productivity](ultimate-guide/09-advanced-patterns.md#918-codebase-design-for-agent-productivity)
  - [9.19 Permutation Frameworks](ultimate-guide/09-advanced-patterns.md#919-permutation-frameworks)
  - [9.20 Agent Teams (Multi-Agent Coordination)](ultimate-guide/09-advanced-patterns.md#920-agent-teams-multi-agent-coordination)
  - [9.21 Legacy Codebase Modernization](ultimate-guide/09-advanced-patterns.md#921-legacy-codebase-modernization)
  - [9.22 Remote Control (Mobile Access)](ultimate-guide/09-advanced-patterns.md#922-remote-control-mobile-access)
  - [9.23 Configuration Lifecycle & The Update Loop](ultimate-guide/09-advanced-patterns.md#923-configuration-lifecycle--the-update-loop)
  - [9.24 Instinct-Based Continuous Learning](ultimate-guide/09-advanced-patterns.md#924-instinct-based-continuous-learning)
  - [9.25 Harness Engineering](ultimate-guide/09-advanced-patterns.md#925-harness-engineering)
- [10. Reference](ultimate-guide/10-reference.md) `🟢 All levels` `⏱ As needed`
  - [10.1 Commands Table](ultimate-guide/10-reference.md#101-commands-table)
  - [10.2 Keyboard Shortcuts](ultimate-guide/10-reference.md#102-keyboard-shortcuts)
  - [10.3 Configuration Reference](ultimate-guide/10-reference.md#103-configuration-reference)
  - [10.4 Troubleshooting](ultimate-guide/10-reference.md#104-troubleshooting)
  - [10.5 Cheatsheet](ultimate-guide/10-reference.md#105-cheatsheet)
  - [10.6 Daily Workflow & Checklists](ultimate-guide/10-reference.md#106-daily-workflow--checklists)
- [11. AI Ecosystem: Complementary Tools](ultimate-guide/11-ai-ecosystem.md) `🟡 Intermediate` `⏱ 20 min`
  - [11.1 Why Complementarity Matters](ultimate-guide/11-ai-ecosystem.md#111-why-complementarity-matters)
  - [11.2 Tool Matrix](ultimate-guide/11-ai-ecosystem.md#112-tool-matrix)
  - [11.3 Practical Workflows](ultimate-guide/11-ai-ecosystem.md#113-practical-workflows)
  - [11.4 Integration Patterns](ultimate-guide/11-ai-ecosystem.md#114-integration-patterns)
  - [For Non-Developers: Claude Cowork](ultimate-guide/11-ai-ecosystem.md#for-non-developers-claude-cowork)
- [Appendix: Templates Collection](ultimate-guide/10-reference.md#appendix-templates-collection)
  - [Appendix A: File Locations Reference](ultimate-guide/10-reference.md#appendix-a-file-locations-reference)
  - [Appendix B: FAQ](ultimate-guide/10-reference.md#appendix-b-faq)

---

> 💡 This guide is split into chapter files for easier navigation. Each link above opens the corresponding chapter.
