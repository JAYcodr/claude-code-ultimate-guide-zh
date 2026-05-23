# 面向编码AI助手的规范完整性审计

> 一个自包含的提示词，用于审计代码库对AI代理委派的规范完备程度。
> 基于 Hamidreza Saghir 的"你的编码AI代理缺少规范"中的5层框架。

**用途**：在任何项目进行大规模AI代理委派前运行，以检测会导致无声架构漂移的规范缺口。

**耗时**：约3-5分钟。未经明确批准不会做任何更改。

---

## 使用方法

```bash
cd your-project-directory
claude
```

粘贴下方的提示词并按回车。

---

## 提示词内容

````markdown
# Spec Completeness Audit — v1.0

You are auditing how well this project is specified for safe agent delegation.

The goal: find gaps that will cause an agent to silently fill in architectural,
lifecycle, and cultural decisions from training priors instead of project intent.

Do NOT modify any files. Do NOT make changes. Audit and report only.

---

## Framework: 5 Specification Layers

Every coding task requires spec across 5 layers. Agents fill missing layers silently.

| Layer | What it covers | Missing → agent fills with |
|-------|---------------|---------------------------|
| 1. Behavioral | What the code does (features, endpoints, flows) | Training-data guesses on behavior |
| 2. Interface | Types, error contracts, invariants, I/O shapes | Optimistic error handling, loose types |
| 3. Architectural | What NOT to create, module boundaries, reuse constraints | Duplication, broken boundaries |
| 4. Lifecycle | How code ages, what's deferred and why, maintenance intent | Short-term fixes, band-aids |
| 5. Cultural | Team conventions, what "good" means here, taste | Average public code quality |

---

## Phase 1 — Project Inventory (bash)

Run this block. Store the full output for scoring.

```bash
bash -c '
echo "=== PROJECT TYPE ==="
[ -f package.json ] && node -e "const p=require(\"./package.json\"); console.log(\"node:\", p.name, p.version)" 2>/dev/null
[ -f pyproject.toml ] && grep "^name\|^version" pyproject.toml | head -2
[ -f Cargo.toml ] && grep "^name\|^version" Cargo.toml | head -2
[ -f go.mod ] && head -2 go.mod
[ -f *.qmd ] && echo "quarto: documentation project"
[ -d guide ] && echo "docs: guide project"

echo ""
echo "=== SPEC DOCUMENTS ==="
for f in CLAUDE.md .claude/CLAUDE.md README.md AGENTS.md CONTRIBUTING.md \
          docs/ARCHITECTURE.md docs/architecture.md docs/ADR docs/adr \
          .cursor/rules .github/copilot-instructions.md; do
  [ -e "$f" ] && echo "  ✅ $f" || echo "  ❌ $f"
done

echo ""
echo "=== CLAUDE.md COVERAGE (layer mapping) ==="
if [ -f CLAUDE.md ]; then
  wc -l CLAUDE.md | awk "{print \"  Lines:\", \$1}"
  echo "  Layer 1 (behavior): $(grep -ci "what\|feature\|endpoint\|flow\|purpose\|goal\|objective" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 2 (interface): $(grep -ci "type\|schema\|contract\|error\|invariant\|input\|output\|interface" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 3 (arch): $(grep -ci "don.t\|avoid\|never\|not\|boundary\|module\|reuse\|pattern\|structure\|forbidden\|prohibited" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 4 (lifecycle): $(grep -ci "TODO\|defer\|later\|debt\|evolv\|future\|maintain\|migration\|tradeoff" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 5 (culture): $(grep -ci "convention\|style\|taste\|prefer\|standard\|naming\|format" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
else
  echo "  ❌ No CLAUDE.md — all layers unspecified from agent perspective"
fi

echo ""
echo "=== INTERFACE SPEC ==="
# TypeScript
ts_files=$(find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | grep -v node_modules | grep -v .git | wc -l | tr -d " ")
echo "  TypeScript files: $ts_files"
zod=$(grep -rl "z\.\|zod\|Zod" . --include="*.ts" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Zod schemas: $zod files"

# OpenAPI / Swagger
for f in openapi.yaml openapi.json swagger.yaml swagger.json api.yaml; do
  [ -f "$f" ] && echo "  ✅ API spec: $f"
done

# Error handling
error_files=$(grep -rl "catch\|Error\|exception\|throw" . --include="*.ts" --include="*.py" --include="*.rs" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Files with error handling: $error_files"

echo ""
echo "=== ARCHITECTURAL CONSTRAINTS ==="
# Negative constraints (what NOT to do)
negatives=0
for f in CLAUDE.md .claude/CLAUDE.md .claude/rules/*.md; do
  [ -f "$f" ] && count=$(grep -ci "don.t\|avoid\|never\|do not\|forbidden\|prohibited\|not allowed\|no \(mocks\|stubs\|placeholders\)\|pas de\|jamais\|éviter\|ne pas\|interdit" "$f" 2>/dev/null || echo 0)
  negatives=$(( negatives + count ))
done
echo "  Negative constraints found: $negatives"

# ADR (Architecture Decision Records)
adr_count=0
for d in docs/adr docs/ADR .adr adr; do
  [ -d "$d" ] && adr_count=$(find "$d" -name "*.md" 2>/dev/null | wc -l | tr -d " ") && echo "  ✅ ADR directory: $d ($adr_count records)"
done
[ $adr_count -eq 0 ] && echo "  ❌ No ADR directory"

# Module boundary docs
boundary=$(grep -ril "boundary\|module\|layer\|package\|service\|domain" . --include="*.md" 2>/dev/null | grep -v node_modules | grep -v ".git" | head -5)
[ -n "$boundary" ] && echo "  Module boundary docs:" && echo "$boundary" | sed "s/^/    /" || echo "  ❌ No module boundary documentation"

echo ""
echo "=== LIFECYCLE SPEC ==="
# Technical debt tracking
td=$(grep -rl "TODO\|FIXME\|HACK\|DEBT\|technical.debt" . --include="*.ts" --include="*.py" --include="*.rs" --include="*.md" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Files with TODO/FIXME/HACK/DEBT: $td"

# Changelog
for f in CHANGELOG.md CHANGELOG.rst docs/CHANGELOG.md; do
  [ -f "$f" ] && wc -l "$f" | awk "{print \"  ✅ Changelog: \" \$1 \" lines\"}"
done

# Migration guides
migrations=$(find . -name "*.md" 2>/dev/null | xargs grep -l "migration\|migrate\|upgrade\|breaking" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Migration/upgrade docs: $migrations files"

echo ""
echo "=== CULTURAL SPEC ==="
# Linters
for f in .eslintrc* .eslintrc.json .eslintrc.js eslint.config.* .pylintrc pyproject.toml .rubocop.yml; do
  [ -f "$f" ] && echo "  ✅ Linter config: $f"
done

# Formatting
for f in .prettierrc* biome.json .editorconfig rustfmt.toml; do
  [ -f "$f" ] && echo "  ✅ Formatter: $f"
done

# Naming / convention docs
naming=$(grep -rl "naming\|convention\|camelCase\|snake_case\|kebab" . --include="*.md" 2>/dev/null | grep -v node_modules | head -3)
[ -n "$naming" ] && echo "  Convention docs: $naming" || echo "  ❌ No naming/convention documentation"

echo ""
echo "=== REUSE CONSTRAINTS ==="
# Does the agent know what already exists?
reuse=$(grep -ril "already exists\|use existing\|reuse\|don.t create\|see \|refer to" CLAUDE.md .claude/CLAUDE.md .claude/rules/*.md 2>/dev/null | wc -l | tr -d " ")
echo "  Reuse/existing-code references in specs: $reuse"

# Map of what exists (README sections, module index)
index_quality=0
[ -f README.md ] && index_quality=$(wc -l < README.md | tr -d " ")
echo "  README lines: $index_quality"
'
```

---

## Phase 2 — Layer-by-Layer Scoring

Score each layer. Use Phase 1 output. Read key files where needed.

### Layer 1 — Behavioral Spec (15 pts)

**What to check**: Can an agent understand what this project should do — features, user flows, acceptance criteria — without guessing?

Read README.md top-level section if it exists.

Scoring:
- README with purpose + key features: 5 pts (3 if minimal, 0 if absent)
- CLAUDE.md covers what the project does: 3 pts
- Acceptance criteria or feature contracts exist (tests-as-spec, test descriptions, feature files): 4 pts
- Task/issue tracking linked or summarized somewhere the agent can see: 3 pts

### Layer 2 — Interface Spec (20 pts)

**What to check**: Are input/output shapes, error contracts, and invariants machine-readable or documented?

```bash
# Sample 3 key files for type coverage quality
find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | grep -v node_modules | grep -v ".git" | \
  shuf 2>/dev/null | head -3 | xargs grep -l "interface\|type\|z\.\|Schema" 2>/dev/null | head -3
```

Read 1-2 of the sampled files briefly to assess typing quality.

Scoring:
- TypeScript strict mode OR typed Python (mypy/pyright) OR Rust (automatic): 6 pts (3 if partial)
- Zod/Pydantic/Joi or equivalent schema validation at boundaries: 4 pts
- Error handling is explicit with typed errors (not just generic catch): 4 pts
- API contracts documented (OpenAPI, tRPC, GraphQL schema, Protobuf): 4 pts
- Invariants documented (pre/post conditions, state transitions): 2 pts

### Layer 3 — Architectural Spec (30 pts)

**This is the most commonly missing layer. Weight reflects that.**

**What to check**: Does the agent know what NOT to create, how things fit together, and what already exists?

Read CLAUDE.md architectural sections if present. Check for ADRs.

```bash
# Check CLAUDE.md for architectural content depth
[ -f CLAUDE.md ] && grep -n "not\|avoid\|don.t\|never\|boundary\|module\|reuse\|exist\|pattern\|structure" CLAUDE.md | head -20
```

Scoring:
- CLAUDE.md has explicit negative constraints ("never create X", "don't introduce Y", "reuse Z"): 8 pts (4 if implicit/weak, 0 if absent)
- Module/service boundaries are documented: 6 pts
- "What already exists" is surfaced to the agent (index, map, reference.yaml, or similar): 6 pts
- ADR or equivalent architectural decision log: 5 pts
- Patterns the codebase uses are named and explained: 5 pts

### Layer 4 — Lifecycle Spec (20 pts)

**What to check**: Does the agent know what's intentionally deferred, what's debt, and what future changes to anticipate?

Scoring:
- CHANGELOG.md exists and is maintained: 4 pts
- TODO/FIXME/DEBT markers are meaningful (have context, not just "fix later"): 4 pts (check a sample)
- Breaking change policy documented: 3 pts
- Known technical debt is documented with rationale: 5 pts
- Planned changes or roadmap visible to the agent: 4 pts

### Layer 5 — Cultural Spec (15 pts)

**What to check**: Does the agent know what "good" looks like here, specifically for this codebase?

Scoring:
- Linter config enforces code style: 3 pts
- Formatter config enforces formatting: 2 pts
- Naming conventions explicitly documented: 3 pts
- Code review criteria or quality bar documented: 3 pts
- Examples of "good" code referenced or present: 2 pts
- Prohibited patterns encoded (in linter or CLAUDE.md): 2 pts

---

## Phase 3 — Gap-Fill Risk Assessment

For each layer below 60% score, estimate what an agent will silently fill in.

```
Layer X (N/max pts) — RISK: [low/medium/high/critical]
Silent fills: [list 2-3 specific decisions the agent will make from training priors]
Most dangerous: [the one most likely to cause irreversible architectural drift]
```

Concrete examples:
- Missing L3 + unfamiliar codebase = agent creates a new auth module instead of finding the existing one
- Missing L2 error contracts = agent writes optimistic error handling, returns 200 on partial failure
- Missing L4 lifecycle = agent "fixes" intentional shortcuts, breaking the known-debt contract
- Missing L5 culture = agent uses its most common training pattern, not yours

---

## Phase 4 — Unified Report

### Executive Summary

```
Total Score: X/100
Risk Tier: Safe (80+) | Supervised (60-79) | Risky (40-59) | Unsafe (<40)

Gap-Fill Risk: [which layers will generate the most dangerous silent decisions]
Top 3 Highest-ROI Fixes: [sorted by: impact × time to implement]
```

### Layer Scorecard

| Layer | Name | Score | Max | Risk | Key Gap |
|-------|------|-------|-----|------|---------|
| 1 | Behavioral | X | 15 | 🟢/🟡/🔴 | one line |
| 2 | Interface | X | 20 | 🟢/🟡/🔴 | one line |
| 3 | Architectural | X | 30 | 🟢/🟡/🔴 | one line |
| 4 | Lifecycle | X | 20 | 🟢/🟡/🔴 | one line |
| 5 | Cultural | X | 15 | 🟢/🟡/🔴 | one line |
| | **TOTAL** | **X** | **100** | | |

Risk: 🟢 ≥80% | 🟡 50–79% | 🔴 <50%

### Detailed Findings

For each 🔴 and 🟡 gap:

```
[Layer N — Name]
Gap: what is missing
Silent fill: what the agent will invent to fill it
Fix: specific file to create or section to add (with example content)
Effort: <30min / 1h / half-day
```

### Delegation Verdict

Based on total score, state explicitly:

- **Score ≥80**: Safe for broad delegation. Document remaining gaps in CLAUDE.md before each task.
- **Score 60–79**: Delegate with constraints. Specify architectural layer per prompt. Review every commit.
- **Score 40–59**: High-supervision mode. Define L3 before each delegation. Use plan-mode + review agent.
- **Score <40**: Do not delegate architectural work. Code tasks only with exhaustive per-task specs.

---

## Phase 5 — Quick Wins

List the 3 highest-ROI improvements, each with:

1. Exact file to create or modify
2. Minimal template to add right now
3. Estimated effort

Then ask:

"Implement these quick wins?
- **yes** → implement all three
- **1, 3** → specific items
- **none** → keep report, no changes"

Wait for explicit user response before taking any action.
````

---

## 理解结果

### 风险等级

| 分数 | 等级 | AI代理委派姿态 |
|------|------|---------------|
| 80–100 | 安全 | 可进行广泛委派。每项任务附带简要架构提醒。 |
| 60–79 | 受监督 | 每项任务附带显式的L3约束进行委派。审查每次提交。 |
| 40–59 | 高风险 | 计划模式 + 审查AI代理。每次会话前指定架构。 |
| <40 | 不安全 | 仅限编码任务，绝不涉及架构。每项任务给出详尽规范。 |

### 最重要的层级

**层级3（架构规范，30分）** 权重最高，因为它既是最常缺失的，也是最难在出错时检测的。一个正确完成L1但失败于L3的AI代理会编写今天能工作但下个月就腐化的代码。没有测试能捕获这种问题。

### "安全"意味着什么

一个得分80+的项目仍然需要每项任务针对特定层级增强提示词。"安全"意味着AI代理有足够的上下文来避免最糟糕的无声填补——而不是你可以委派后一走了之。

---

## 相关链接

- [`tools/audit-prompt.md`](audit-prompt.md) — Claude Code 设置审计（安全、规则、记忆、MCP）
- [`tools/context-audit-prompt.md`](context-audit-prompt.md) — Token 预算与上下文工程
- 来源：Hamidreza Saghir, "你的编码AI代理缺少规范"（2026年5月）

---

*版本 1.0 — 规范完整性审计*
