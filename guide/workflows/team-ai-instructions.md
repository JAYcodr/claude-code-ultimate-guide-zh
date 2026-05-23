<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "团队 AI 指令管理"
description: "使用基于配置文件的模块组装跨团队扩展 CLAUDE.md"
tags: [workflow, team, claude-md, configuration]
---

# 团队 AI 指令管理

跨团队管理 AI 指令（CLAUDE.md、.cursorrules）而不碎片化。

**模式**：基于配置文件的模块组装——共享模块 + 每开发者配置 + 自动化组装器。

**何时使用**：5 人以上开发团队、多个 AI 工具（Claude Code + Cursor/Windsurf）、混合操作系统。
**跳过如果**：独立开发者、同质团队（相同工具、相同操作系统）、短项目（<3 个月）。

---

## 问题：N x M x P 碎片化

当团队成长时，AI 指令快速碎片化：

| 因素 | 值 | 示例 |
|--------|--------|---------|
| **N 个开发者** | 5-20 | Alice、Bob、Charlie... |
| **M 个工具** | 2-4 | Claude Code、Cursor、Windsurf、Copilot |
| **P 个操作系统** | 2-3 | macOS、Linux、WSL |

**总变体**：N x M x P = 5 x 3 x 2 = **30 种可能配置**。

没有系统，会发生什么：

```
第 1 周：团队同意共享 CLAUDE.md
第 3 周：Alice 在本地添加 TypeScript 严格规则
第 5 周：Bob 复制 Alice 的文件，删除一半规则
第 8 周：新员工 Charlie 得到 Bob 的过时副本
第 12 周：5 个开发者，5 个不同的 CLAUDE.md 文件，没人知道哪个是规范
```

**根本原因**：CLAUDE.md 被当作单一文件而非组合配置。

---

## 架构概述

```
profiles/                    modules/
├── alice.yaml               ├── core-standards.md
├── bob.yaml                 ├── git-workflow.md
├── charlie.yaml             ├── typescript-rules.md
│                            ├── test-conventions.md
│                            ├── macos-paths.md
│                            ├── linux-paths.md
│                            ├── cursor-rules.md
│                            └── communication-verbose.md
│
├── skeleton/
│   └── claude-skeleton.md   ← 带 {{MODULE:name}} 占位符的模板
│
└── sync-ai-instructions.ts  ← 读取配置 → 注入模块 → 写入输出
        │
        ▼
output/
├── alice/CLAUDE.md          ← 生成（只读）
├── bob/CLAUDE.md
└── charlie/CLAUDE.md
```

**流程**：Profile（YAML）+ Skeleton（模板）+ Modules（片段）→ Assembler → 生成的 CLAUDE.md

---

## 阶段 1：审计你当前的 CLAUDE.md

**目标**：将每行分类为通用、条件或个人。

```markdown
# 审计模板

## 通用（所有开发者，所有工具）
- 架构：六边形
- 测试：PR 前必须通过
- 命名：文件用 kebab-case

## 条件（取决于工具或操作系统）
- Cursor：使用 @filename 语法 → 模块：cursor-rules
- macOS 路径：/opt/homebrew → 模块：macos-paths
- Linux 路径：/usr/local → 模块：linux-paths

## 个人（个人偏好）
- 风格：详细解释 → 配置偏好
- 语言：法语注释 → 配置偏好
```

**测量命令**：
```bash
wc -l CLAUDE.md  # 模块化前的总行数
# 给每行标记 [U]niversal、[C]onditional、[P]ersonal
# 按类别计数以估计模块拆分
```

**典型结果**：60% 通用、25% 条件、15% 个人。

---

## 阶段 2：提取模块

**目标**：每个主题组一个 `.md` 文件。

**推荐结构**：

```
modules/
├── core-standards.md         # 架构、命名、模式（所有开发者）
├── git-workflow.md           # Git 约定（所有开发者）
├── typescript-rules.md       # TS 严格配置（如果使用 TypeScript）
├── test-conventions.md       # 测试模式（所有开发者）
├── macos-paths.md            # macOS 特定路径（如果 macOS）
├── linux-paths.md            # Linux 路径（如果 Linux）
├── cursor-rules.md           # Cursor 特定规则（如果 Cursor）
└── communication-verbose.md  # 详细解释风格（如果偏好）
```

**模块格式**（每个模块是一个独立的 Markdown 片段）：

```markdown
<!-- modules/typescript-rules.md -->
## TypeScript 规则

- 使用严格模式：`"strict": true` in tsconfig
- 联合优先使用 `type` 而非 `interface`
- 不用 `any` — 用 `unknown` + 类型守卫
- 边界用 Zod 运行时验证
```

**指南**：
- 保持模块自包含（模块之间无交叉引用）
- 每个模块 15-50 行是最佳点
- 用领域命名模块，而非受众
- 一个模块 = 一个变更原因

---

## 阶段 3：创建开发者配置

**目标**：每个开发者一个 YAML，列出他们的模块。

```yaml
# profiles/alice.yaml
name: "Alice"
os: "macos"
tools:
  - claude-code
  - cursor
communication_style: "concise"
modules:
  core:
    - core-standards
    - git-workflow
    - typescript-rules
    - test-conventions
  conditional:
    - macos-paths          # os: macos 时自动包含
    - cursor-rules         # tools 中有 cursor 时自动包含
preferences:
  language: "english"
```

**配置规则**：
- `core` 模块：每个开发者都包含（团队标准）
- `conditional` 模块：根据 `os` 和 `tools` 字段包含
- `preferences`：注入到模板变量的个人设置

**新团队成员模板**：见 [profile-template.yaml](../../examples/team-config/profile-template.yaml)

---

## 阶段 4：编写组装器脚本

**目标**：读取配置、注入模块、输出 CLAUDE.md 的脚本。

```typescript
// sync-ai-instructions.ts（简化 ~30 行）
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { parse } from 'yaml';
import { join } from 'path';

const profile = parse(readFileSync(`profiles/${process.argv[2]}.yaml`, 'utf8'));
let skeleton = readFileSync('skeleton/claude-skeleton.md', 'utf8');

// 从配置收集模块
const modules = [...profile.modules.core, ...profile.modules.conditional];

// 用模块内容替换每个占位符
for (const mod of modules) {
  const content = readFileSync(`modules/${mod}.md`, 'utf8');
  skeleton = skeleton.replace(`{{MODULE:${mod}}}`, content);
}

// 移除未使用的占位符
skeleton = skeleton.replace(/\{\{MODULE:\w+\}\}/g, '');

// 写入输出
const outDir = `output/${process.argv[2]}`;
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'CLAUDE.md'), skeleton);
console.log(`Generated ${outDir}/CLAUDE.md (${modules.length} modules)`);
```

**运行**：
```bash
npx ts-node sync-ai-instructions.ts alice   # 单个开发者
npx ts-node sync-ai-instructions.ts --all   # 生成所有配置
npx ts-node sync-ai-instructions.ts --check # 验证无漂移
```

完整模板：[sync-script.ts](../../examples/team-config/sync-script.ts)

---

## 阶段 5：CI 漂移检测

**目标**：捕获输出文件与配置/模块不同步时。

```yaml
# .github/workflows/ai-instructions-check.yml
name: AI Instructions Drift Check
on:
  push:
    paths:
      - 'modules/**'
      - 'profiles/**'
      - 'skeleton/**'
  schedule:
    - cron: '0 9 * * 1-5'  # 工作日上午 9 点

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx ts-node sync-ai-instructions.ts --check
      - name: Fail if drift detected
        run: |
          if git diff --quiet output/; then
            echo "No drift detected"
          else
            echo "::error::AI instructions are out of sync!"
            git diff output/
            exit 1
          fi
```

**它检测什么**：
- 模块被编辑但组装器未重新运行
- 添加了配置但不存在输出的 CLAUDE.md
- 开发者手动编辑了他们生成的 CLAUDE.md

**策略**：生成的文件是只读的。所有变更通过配置/模块，然后重新运行组装器。

---

## 阶段 6：新人开发者入职

**目标**：新开发者在 5 分钟内获得他们的 CLAUDE.md。

```bash
# 1. 克隆仓库
git clone <repo>

# 2. 复制配置模板
cp examples/team-config/profile-template.yaml profiles/dave.yaml
# 编辑：name、os、tools、modules

# 3. 生成
npx ts-node sync-ai-instructions.ts dave

# 4. 安装
cp output/dave/CLAUDE.md .claude/CLAUDE.md
```

**CLAUDE.md 放置提醒**：
- 项目范围：`project/CLAUDE.md`（提交，用于团队约定）
- 个人覆盖：`.claude/CLAUDE.md`（git 忽略，用于个人偏好）

---

## 故障排除

| 问题 | 原因 | 修复 |
|---------|-------|-----|
| 生成的文件太长 | 包含的模块太多 | 审查配置：移除很少使用的模块 |
| 输出中缺少模块 | 占位符拼写错误 | 检查 `{{MODULE:name}}` 与文件名匹配 |
| CI 漂移警报 | 模块编辑后未重新生成 | 运行 `sync-ai-instructions.ts` 并提交 |
| 开发者 A 有开发者 B 没有的规则 | 预期的 — 这就是要点 | 验证该开发者的配置正确 |
| 合并后输出陈旧 | 合并未触发重新生成 | 运行组装器后合并（添加 git hook） |

---

## 扩展阈值

| 团队规模 | 方式 |
|-----------|----------|
| 1-2 个开发者 | 共享 CLAUDE.md + 优先级规则（[第 3.4 节](#34-precedence-rules)） |
| 3-5 个开发者，相同工具 | 可选：仅模块，无配置 |
| 5+ 个开发者或多工具 | 基于配置文件的模块组装（此工作流） |
| 20+ 个开发者 | 考虑 CLAUDE.md 配置服务器 + 基于 PR 的模块变更 |

---

## 测量结果

来自生产团队（5 个开发者、3 个工具、2 个操作系统）：

| 指标 | 之前 | 之后 |
|--------|--------|--------|
| CLAUDE.md 行数 | ~380（单一） | ~185（组装） |
| Token 减少 | — | 减少 59% |
| 提取的模块 | 0 | 12 |
| 入职时间 | "复制某人的文件" | 5 分钟（模板 + 生成） |
| 漂移事件 | 每周 | 0（CI 捕获） |

---

## 相关

- [第 3.5 节 大规模团队配置](#35-team-configuration-at-scale) — 概念概述和测量结果
- [第 3.4 节 优先级规则](#34-precedence-rules) — Claude 如何读取多个 CLAUDE.md 文件
- [profile-template.yaml](../../examples/team-config/profile-template.yaml) — 配置模板
- [claude-skeleton.md](../../examples/team-config/claude-skeleton.md) — 骨架模板
- [sync-script.ts](../../examples/team-config/sync-script.ts) — 完整组装器脚本