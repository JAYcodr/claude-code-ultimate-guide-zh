# Claude Code 终极指南 — 中文翻译计划

> 管理 `claude-code-ultimate-guide-zh` 的翻译流程，确保质量一致性和术语统一。

---

## 1. 项目概况

### 1.1 项目信息
- **上游仓库**: [FlorianBruniaux/claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)
- **中文仓库**: [JAYcodr/claude-code-ultimate-guide-zh](https://github.com/JAYcodr/claude-code-ultimate-guide-zh)
- **当前版本**: v3.41.0
- **基准 commit**: dbeb30c

### 1.2 翻译进度总览
| 优先级 | 总计 | ✅ 完成 | 🔄 进行中 | ❌ 未开始 |
|--------|------|--------|-----------|----------|
| P0 | 15 | 15 | 0 | 0 |
| P1 | 4 | 4 | 0 | 0 |
| P2 | 3 | 3 | 0 | 0 |
| P3 | 2 | 0 | 0 | 2 |
| P4 | 2 | 1 | 0 | 1 |
| **合计** | **26** | **23** | **0** | **3** |

---

## 2. 质量标准

### 2.1 翻译原则
1. **信**: 准确传达原意，不漏译、不误译
2. **达**: 通顺自然，符合中文表达习惯
3. **雅**: 专业术语统一，文笔流畅

### 2.2 质量检查清单
- [ ] 专业术语统一（见 §6 术语表）
- [ ] 代码块、命令、URL、路径不翻译
- [ ] Mermaid 图表保持原样
- [ ] 去除翻译腔（如过多的「的」「进行」「一个」）
- [ ] 欧化长句拆分为短句
- [ ] 标点符号统一为中文全角（除代码外）
- [ ] 文件头部添加翻译注释
- [ ] 链接指向更新为中文页面（如适用）

### 2.3 译后自检
1. 脱离原文通读译文，确保流畅
2. 对照原文检查漏译、误译
3. 检查术语一致性
4. 检查格式和链接

---

## 3. 翻译流程（严格执行）

### 3.1 初译阶段
1. 选择待翻译文件（按优先级）
2. 通读原文，理解内容
3. 逐段翻译，标记不确定处
4. 保留所有代码、命令、图表

### 3.2 润色阶段
1. 脱离原文通读译文
2. 调整语序，使符合中文习惯
3. 去除冗余词汇
4. 优化表达

### 3.3 校对阶段
1. 对照原文逐句核对
2. 检查术语一致性
3. 检查格式和链接
4. 填写校对记录

### 3.4 提交阶段
1. 更新 `TRANSLATION_STATUS.md`
2. 添加工作日志
3. git add / commit / push

---

## 4. 优先级说明

### P0 — 核心文档（已完成）
- README.md
- guide/learning-path/（完整）
- guide/cheatsheet.md
- guide/ultimate-guide/（核心章节）

### P1 — 模板与架构（已完成）
- examples/skills/（5个文件）
- examples/agents/（15个文件）
- guide/core/architecture.md
- guide/core/methodologies.md

### P2 — 工作流与图表（已完成）
- guide/diagrams/（12个文件）
- guide/workflows/（25个文件）

### P3 — 辅助文件（待完成）
- examples/hooks/ + examples/scripts/（~200行）
- docs/resource-evaluations/（~3,000行，151个文件）

### P4 — 低优先级（部分完成）
- machine-readable/（~967行，评估中）
- tools/（已完成，7个提示词模板）

---

## 5. 待翻译文件清单

### 5.1 高优先级
- [ ] quiz/questions/*.yaml（271题，~1,000行）

### 5.2 中优先级
- [ ] examples/hooks/*
- [ ] examples/scripts/*
- [ ] docs/resource-evaluations/*.md（151个文件）

### 5.3 低优先级
- [ ] machine-readable/*

---

## 6. 专业术语表

| 英文 | 中文 | 说明 |
|------|------|------|
| Agent | 智能体 | 核心概念，不译「代理」 |
| Skill | 技能 | 核心概念，不译「技巧」 |
| Command | 命令 | 如 `/help`、`/plan` |
| Hook | 钩子 | 事件触发器 |
| Workflow | 工作流 | 核心概念 |
| Worktree | 工作树 | Git 概念 |
| Session | 会话 | Claude Code 会话 |
| Context | 上下文 | AI 上下文 |
| Memory | 记忆 | 记忆系统 |
| Plugin | 插件 | 第三方插件 |
| MCP | MCP | Model Context Protocol，保留缩写 |
| TDD | TDD | Test-Driven Development，保留缩写 |
| BDD | BDD | Behavior-Driven Development，保留缩写 |
| SDD | SDD | Specification-Driven Development，保留缩写 |
| CVE | CVE | Common Vulnerabilities and Exposures，保留缩写 |
| CI/CD | CI/CD | 保留缩写 |

---

## 7. 常见问题

### 7.1 什么时候翻译？
- 主要内容（散文、说明）→ 翻译
- 代码、命令、路径、URL → 不译
- 技术术语 → 按术语表统一
- Mermaid 图表 → 只译注释和标签（如果有）

### 7.2 如何处理专有名词？
- 优先使用术语表中的翻译
- 不确定的标记出来，集体讨论
- 人名、品牌名保留原文

### 7.3 格式如何处理？
- 保留所有 Markdown 格式
- 列表、表格结构不变
- 代码块原样保留

---

## 8. 协作方式

1. 每次只翻译一个文件/批次
2. 翻译前先 pull 最新代码
3. 翻译后及时 push
4. 有问题开 Issue 讨论

---

## 9. 版本同步

定期从上游同步更新：
```bash
# 添加上游远程仓库（如果还没）
git remote add upstream https://github.com/FlorianBruniaux/claude-code-ultimate-guide.git

# 同步上游
git fetch upstream
git merge upstream/main

# 检查冲突，解决后提交
git status
git add .
git commit -m "sync: 同步上游更新"
git push
```

---

## 10. 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-23 | v1.0 | 初始翻译计划 |
