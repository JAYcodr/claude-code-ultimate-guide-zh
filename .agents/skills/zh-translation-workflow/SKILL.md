---
name: zh-translation-workflow
description: "Claude Code Ultimate Guide 汉化工作流。触发词：翻译/开始工作 → 读取两份计划文档并按优先级执行翻译；结束/今天先到这/辛苦了 → 更新 TRANSLATION_STATUS.md、提交、推送、总结进度。"
---

# 汉化工作流

本 skill 管理 `claude-code-ultimate-guide-zh` 的翻译工作流。

## 触发词

| 触发词 | 行为 |
|--------|------|
| `翻译` / `开始工作` / `继续` / `下一节` | 载入上下文，读取计划文档，继续翻译 |
| `结束` / `收工` / `今天先到这` / `辛苦了` / `下次继续` | 更新 TRANSLATION_STATUS.md，提交推送，输出总结 |

---

## 开工流程

当用户说 `翻译` 或 `开始工作` 时，按此顺序执行：

### Step 1 — 读取计划文档

按顺序读取以下文档，理解翻译策略、质量标准、术语表和项目约束：

1. `TRANSLATION-PLAN.md` — 翻译原则、优先级、质量标准与审校流程（§4）、术语表（§6）、上游同步策略（§5）
2. `PROJECT-KICKOFF.md` — 边界清单（§2）、对象定义（§7）、Agent 施工约束（§13）

### Step 2 — 读取进度

读取 `TRANSLATION_STATUS.md`，了解当前完成状态和进行中文件。

### Step 3 — 确认工作目标

根据优先级表，确定本次要翻译的文件：
- P0 ✅ 全部完成（14/14）：learning-path(8)、cheatsheet、README、ultimate-guide §1-3（分章管理）
- P1: `guide/core/architecture.md`(1,625行)、`guide/core/methodologies.md`(608行)、`examples/skills/`(~100个文件)、`examples/agents/`(23个文件)
- P2: `guide/workflows/`、`guide/diagrams/`、`quiz/`(271题)
- 以此类推

询问用户本次要翻译哪个文件（如果用户没有指定）。

### Step 4 — 翻译

执行翻译，遵循 TRANSLATION-PLAN.md §4 的质量标准：

1. **初译** — 逐段翻译，标记不确定处
2. **自检** — 对照 §4.3 检查清单
3. **润色** — 脱离原文，读中文版，改成自然中文
4. **终检** — 对照原文检查漏译/误译，检查 Markdown 渲染

**批次限制**：单次翻译不超过 800 行，超过时分批写入（Write 首批，bash cat >> 后续）

### 核心约束

- 代码块、命令、路径、URL 绝不翻译
- Mermaid 图不翻译
- 文件顶部添加 header comment：`<!-- 中文翻译版 · 基于上游 commit: xxx -->`
- 术语以 TRANSLATION-PLAN.md §6 为准
- 长文件（>800 行）分批次，首批用 Write，后续用 `bash cat >>`
- 翻译本质差最后修复：多余的"的""进行""一个""这个"，破折号超标，欧化长句

---

## 收工流程

当用户说 `结束` / `今天先到这` / `辛苦了` 时：

### Step 1 — 更新 TRANSLATION_STATUS.md

在 TRANSLATION_STATUS.md 追加或更新本次完成内容：

```markdown
## 2026-05-23

| 文件 | 状态 | 备注 |
|------|------|------|
| path/to/file.md | ✅ 完成 | xxx 行，commit xxxxxx |
| path/to/file.md | ❌ 未开始 | - |
```

### Step 2 — 提交

```bash
git add <translated-file> TRANSLATION_STATUS.md
git commit -m "feat: 汉化 <path>" --author="opencode <JAYcodr@users.noreply.github.com>"
git push
```

注意：不要 `git push` 除非用户特别说"推送"——只 commit 即可。

### Step 3 — 输出总结

向用户输出本次工作总结：

```
━ 本次工作 ━━━━━━━━━━━━━━━━━━━━━━━━
翻译文件：xxx.md（xxx 行）
修改/新增：xxx 行
commit：xxxxxxxx
────────────────────────────────
进度：P0 x/x  |  P1 x/x  |  P2 x/x
下一建议：xxx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 审校模式

当用户说 `审校` / `润色` / `review` 时，只做审校不翻译：

1. 读取 TRANSLATION-PLAN.md §4（质量标准）
2. 对照 §4.3 检查清单逐项检查指定文件
3. 输出审校结果：通过/不通过 + 具体问题列表
4. 如果不通过，给出修改建议
