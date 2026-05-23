---
name: zh-translation-workflow
description: "Claude Code Ultimate Guide 汉化工作流。翻译/开始工作 → 按优先级翻译；结束/辛苦了 → 更新状态、提交、推送、总结。"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
effort: high
---

# 汉化工作流

管理 `claude-code-ultimate-guide-zh` 的翻译工作流。

## 触发词

| 触发词 | 行为 |
|--------|------|
| `翻译` / `开始工作` / `继续` / `下一节` | 读取计划文档 + 进度，继续翻译 |
| `结束` / `收工` / `今天先到这` / `辛苦了` | 更新状态表、提交推送、输出总结 |
| `审校` / `润色` / `review` | 只审校不翻译，输出问题列表 |

---

## 开工流程

### Step 1 — 读取计划
1. `TRANSLATION-PLAN.md` — 翻译原则、质量标准（§4）、术语表（§6）
2. `PROJECT-KICKOFF.md` — 边界清单（§2）、施工约束（§13）
3. `TRANSLATION_STATUS.md` — 当前进度

### Step 2 — 确认目标

根据优先级表确定本次翻译文件。当前状态：

| 优先级 | 总计 | 状态 |
|--------|------|------|
| P0 | 14 | ✅ 全部完成 |
| P1 | 4 | 🔄 已翻译，待审查提交 |
| P2 | 3 | ❌ 未开始（workflows、diagrams、quiz） |
| P3-P4 | 4 | ❌ 未开始 |

### Step 3 — 翻译执行

遵循 TRANSLATION-PLAN.md §4 质量标准：

1. **初译** — 逐段翻译，标记不确定处
2. **自检** — 对照 §4.3 检查清单
3. **润色** — 脱离原文读中文版，改成自然中文
4. **终检** — 对照原文检查漏译/误译

**批次限制**：单次不超过 800 行，首批用 Write，后续用 `bash cat >>`

### 核心约束
- 代码块、命令、路径、URL、Mermaid 图绝不翻译
- 文件顶部添加 header：`<!-- 中文翻译版 · 基于上游 commit: xxx -->`
- 术语以 TRANSLATION-PLAN.md §6 为准
- 注意清理：多余"的""进行""一个""这个"，破折号超标，欧化长句

---

## 收工流程

### Step 1 — 更新状态
在 TRANSLATION_STATUS.md 追加工作日志。

### Step 2 — 提交并推送
```bash
git add <changed-files> TRANSLATION_STATUS.md
git commit -m "feat: 汉化 <file>"
git push
```

### Step 3 — 输出总结
```
━ 本次工作 ━━━━━━━━━━━━━━━━━━━━━
文件：xxx.md（xxx 行）
commit：xxxxxxxx
进度：P0 x/x | P1 x/x | P2 x/x
────────────────────────────
```

---

## 审校模式

用户说 `审校` / `润色` / `review` 时：

1. 读取 TRANSLATION-PLAN.md §4（质量标准）
2. 对照 §4.3 检查清单逐项检查
3. 输出：通过/不通过 + 具体问题列表 + 修改建议
