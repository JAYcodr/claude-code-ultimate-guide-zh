# 翻译进度追踪

> 自动维护，每次收工更新。

## 总览

| 优先级 | 总计 | ✅ 完成 | 🔄 进行中 | ❌ 未开始 |
|--------|------|--------|-----------|----------|
| P0 | 15 | 15 | 0 | 0 |
| P1 | 4 | 4 | 0 | 0 |
| P2 | 3 | 3 | 0 | 0 |
| P3 | 2 | 0 | 0 | 2 |
| P4 | 2 | 1 | 0 | 1 |
| **合计** | **26** | **23** | **0** | **3** |

## 详细状态

### P0 — 核心文档

| 文件 | 行数 | 状态 | 上游 commit | 完成日期 | 备注 |
|------|------|------|------------|---------|------|
| README.md | ~945 | ✅ | dbeb30c | 2026-05-23 | 已润色 |
| guide/learning-path/README.md | ~263 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/01-installation.md | ~256 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/02-core-loop.md | ~334 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/03-memory.md | ~415 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/04-agents.md | ~461 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/05-skills.md | ~492 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/06-hooks.md | ~435 | ✅ | dbeb30c | 2026-05-23 | |
| guide/learning-path/07-advanced.md | ~580 | ✅ | dbeb30c | 2026-05-23 | |
| guide/cheatsheet.md | ~677 | ✅ | dbeb30c | 2026-05-23 | |
| guide/ultimate-guide.md | ~240 | ✅ | dbeb30c | 2026-05-23 | TOC 导航页（分章后） |
| guide/ultimate-guide/01-quick-start.md | ~1,416 | ✅ | dbeb30c | 2026-05-23 | |
| guide/ultimate-guide/02-core-concepts.md | ~3,200 | ✅ | dbeb30c | 2026-05-23 | |
| guide/ultimate-guide/03-memory-settings.md | ~1,692 | ✅ | dbeb30c | 2026-05-23 | |
| guide/ultimate-guide/04-agents.md | ~873 | ✅ | dbeb30c | 2026-05-23 | 智能体系统 |

### P1 — 模板与架构

| 文件 | 行数 | 状态 | 上游 commit | 完成日期 | 备注 |
|------|------|------|------------|---------|------|
| examples/skills/*.md（5 个独立文件） | ~1,200 | ✅ | dbeb30c | 2026-05-23 | ast-grep、pdf-generator、security-checklist、smart-explore、tdd-workflow |
| examples/agents/*.md（15 个文件） | ~1,000 | ✅ | dbeb30c | 2026-05-23 | 代码评审员、架构师、规划师等 |
| guide/core/architecture.md | ~85KB | ✅ | dbeb30c | 2026-05-23 | 译文质量好，无需大改 |
| guide/core/methodologies.md | ~30KB | ✅ | dbeb30c | 2026-05-23 | |

### P2 — 工作流与图表

| 文件 | 行数 | 状态 | 上游 commit | 完成日期 | 备注 |
|------|------|------|------------|---------|------|
| guide/diagrams/README.md | ~112 | ✅ | dbeb30c | 2026-05-23 | 48 张图表导航 |
| guide/diagrams/*.md（12 个文件） | ~3,500 | ✅ | dbeb30c | 2026-05-23 | 仅译英文散文，Mermaid 不动 |
| guide/workflows/ | ~12,700 | ✅ | dbeb30c | 2026-05-23 | 25/25 文件已翻译+润色 |
| quiz/ | ~1,000 | ❌ | - | - | 271 题 |

### P3 — 辅助文件

| 文件 | 行数 | 状态 | 上游 commit | 完成日期 | 备注 |
|------|------|------|------------|---------|------|
| examples/hooks/ + examples/scripts/ | ~200 | ❌ | - | - | |
| docs/resource-evaluations/ | ~3,000 | ❌ | - | - | 151 个文件 |

### P4 — 低优先级

| 文件 | 行数 | 状态 | 上游 commit | 完成日期 | 备注 |
|------|------|------|------------|---------|------|
| machine-readable/ | ~967 | ❌ | - | - | 评估后决定 |
| tools/ | ~2,900 | ✅ | dbeb30c | 2026-05-23 | 7 个提示词模板，中文用户可直接使用 |

## 工作日志

| 日期 | 文件 | 操作 | commit |
|------|------|------|--------|
| 2026-05-23 | README.md | 首版翻译 + 润色 | 0a3e442 |
| 2026-05-23 | guide/cheatsheet.md | 首版翻译 | f8a16a3 |
| 2026-05-23 | guide/learning-path/README.md + 01 + 02 | 首版翻译 | 7a043e2 |
| 2026-05-23 | guide/learning-path/03 + 04 | 首版翻译 | 263e863 |
| 2026-05-23 | guide/learning-path/05 + 06 | 首版翻译 | 263e863 |
| 2026-05-23 | scripts/sync-upstream.sh | 创建 | 4a98b77 |
| 2026-05-23 | guide/learning-path/07-advanced.md | 首版翻译 | 8ce0b77 |
| 2026-05-23 | §1 Quick Start + 拆分 ultimate-guide | 首版翻译 + 重构 | 183fdec |
| 2026-05-23 | §2 Core Concepts | 首版翻译（3,200 行，4 批次） | 5770bef |
| 2026-05-23 | §3 记忆与设置 | 首版翻译（1,692 行，3 批次） | 7e8fb2d |
| 2026-05-23 | §2 + §3 润色 5 处 | 修复翻译腔 | e0f5121 |
| 2026-05-23 | P1 批次 + ultimate-guide TOC | 汉化 + 润色 + 工作流优化 | 94560ee |
| 2026-05-23 | TRANSLATION_STATUS.md | 更新 P0 完成状态 | bbb0547 |
| 2026-05-23 | 删除上游英文版 workflow | 清理 CI | fd2ea4b |
| 2026-05-23 | 添加 .nojekyll | 修复 GitHub Pages | f11f3ef |
| 2026-05-23 | 升级 GitHub Actions | 兼容 Node.js 24 | 8ac0165 |
| 2026-05-23 | 添加 index.md | GitHub Pages 入口页 | 3f7b2dd |
| 2026-05-23 | 修正 index.md 链接 | 修复链接指向 | 2e496f5 |
| 2026-05-23 | 修复 index → index.html | 修复 GitHub Pages 404 | ebbdc24 |
| 2026-05-23 | 补全工作日志 | 更新文档 | ac5bad6 |
| 2026-05-23 | §4 智能体章节 | 汉化（873 行） | 3852331 |
| 2026-05-23 | guide/diagrams/README.md | 汉化（112 行） | ccd2844 |
| 2026-05-23 | workflows Batch 1（10 文件）| 批量翻译 | 8f2c7d7 |
| 2026-05-23 | workflows Batch 2（6 文件）| 批量翻译 | b23a768 |
| 2026-05-23 | workflows 润色 README + tdd + plan-driven | 去除机翻感 | d3500b6 |
| 2026-05-23 | workflows 润色第二批（10 文件）| 去除机翻感 | 69bb599 |
| 2026-05-23 | workflows/agent-teams.md | 汉化（1506 行）| - |
| 2026-05-23 | workflows/dual-instance-planning.md | 汉化（753 行）| - |
| 2026-05-23 | workflows/task-management.md | 汉化（872 行）| - |
| 2026-05-23 | workflows/agent-teams-quick-start.md | 汉化（593 行）| - |
| 2026-05-23 | workflows/search-tools-mastery.md | 汉化（~650 行）| - |
| 2026-05-23 | workflows/iterative-refinement.md | 汉化（~639 行）| - |
| 2026-05-23 | workflows/rpi.md | 汉化（~765 行）| - |
| 2026-05-23 | workflows/spec-first.md | 汉化（~955 行）| - |
| 2026-05-23 | TRANSLATION_STATUS.md | 更新 P2 workflows 状态 | f4d0072 |
| 2026-05-23 | TRANSLATION_STATUS.md | P1 完成 + 重排优先级 | 712599c |
| 2026-05-23 | guide/diagrams/*.md | 汉化全部 12 个图表文件 | 8700277 |
| 2026-05-23 | tools/（7 个提示词模板） | 汉化全部提示词模板 | - |