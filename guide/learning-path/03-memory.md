<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

# 模块 03：记忆与配置

**时间**: 1 小时 | **难度**: ⭐⭐ 初级

## 目标

配置 Claude Code，让它记住你的偏好和项目专属规则。创建你的第一个 CLAUDE.md 文件。

---

## 你将学到

- Claude Code 的记忆层级如何工作
- 创建和组织 CLAUDE.md 文件
- 设置及其优先级
- 自定义指令和智能体定义
- 项目级与全局配置

---

## 记忆层级

Claude Code 在三个层级记住偏好：

```
┌──────────────────────────────────────────┐
│ 1. 全局 (~/.claude/CLAUDE.md)            │
│    适用于你所有的项目                     │
│    例如：你的编码风格、时区                │
└──────────────────────────────────────────┘
                    ▲
                    │ （会被覆盖）
                    │
┌──────────────────────────────────────────┐
│ 2. 项目 (/your-project/CLAUDE.md)        │
│    仅适用于当前项目                       │
│    例如：团队标准、技术栈                  │
└──────────────────────────────────────────┘
                    ▲
                    │ （会被覆盖）
                    │
┌──────────────────────────────────────────┐
│ 3. 个人 (/your-project/.claude/)         │
│    本地设置，不纳入版本管理                │
│    例如：API 密钥、个人偏好                │
└──────────────────────────────────────────┘
```

### 规则
第 3 级覆盖第 2 级，第 2 级覆盖第 1 级。

---

## 创建你的第一个 CLAUDE.md

CLAUDE.md 是一个简单的 Markdown 文件，告诉 Claude Code 你的规则。

### 基本结构

```markdown
# 我的项目

## Purpose
这个项目做什么的简要说明。

## Tech Stack
- TypeScript
- React 18
- Next.js
- PostgreSQL

## Coding Standards
- 只使用函数式组件
- 所有导出必须有类型
- 每个文件不超过 300 行
- 使用有意义的变量名（不用 `x`、`temp`）

## Behavioral Rules
接受前一定看完 diff。
破坏性变更用 /plan。

## Git Workflow
- 所有工作在功能分支上完成
- PR 需要 1 人审批
- 提交需要 squash

## Current Status
你当前在做什么。
```

### 最小示例（从这里开始）

创建 `/your-project/CLAUDE.md`：

```markdown
# 我的项目

## Quick Context
- 前端：React with TypeScript
- 后端：Node.js with Express
- 数据库：PostgreSQL
- 包管理：pnpm

## Coding Rules
- 优先函数式编程
- 所有函数必须有类型签名
- 功能必须有测试
- 生产代码中不留 console.log

## My Preferences
- 架构变更用 /plan
- 注释写得详细，代码保持简洁
- 跨文件重构前先问一下
```

Claude 会在会话启动时自动读取这个文件，遵循你的规则。

---

## CLAUDE.md 里能放什么？

几乎什么都能配置。常见章节：

### 1. 项目概览
```markdown
## Purpose
这是我们的支付处理后端。
负责信用卡验证和交易日志。

## Important
- 涉及 PCI-DSS 合规关键代码
- 绝不能记录卡号
- 所有变更需要安全审查
```

### 2. 技术栈
```markdown
## Stack
- 语言：Python 3.10+
- 框架：Django 4.0
- 数据库：PostgreSQL 13
- 缓存：Redis
- 任务队列：Celery
```

### 3. 编码规范
```markdown
## Code Style
- 遵循 PEP 8
- 所有函数加类型注解
- 文档字符串用 Google 格式
- 禁止通配符导入
- 每行最长 100 个字符

## Testing
- 最低 80% 覆盖率
- 单元测试 + 集成测试
- 使用 pytest
```

### 4. 规则
```markdown
## Rules
- 所有 PR 需要审查
- 禁止直接推送到 main
- 数据库迁移需要审批
- 安全变更自动标记
- 超过 100 行的重构用 /plan 模式
```

### 5. 当前工作
```markdown
## Current Task
正在构建结账流程。
当前文件：src/checkout/payment-form.tsx
依赖：stripe-js 库、支付 API
```

---

## 全局 CLAUDE.md

对于适用于**你所有项目**的设置，创建 `~/.claude/CLAUDE.md`：

```markdown
# 我的全局偏好

## Communication Style
- 直接、讲事实
- 分步展示工作过程
- 不确定时给出替代方案

## Tools I Use
- 所有 JS 项目用 TypeScript
- 数据/脚本用 Python
- 部署用 Docker
- 所有版本控制用 Git

## My Timezone
America/New_York

## Work Hours
Mon-Fri 9am-5pm (UTC-5)
```

Claude 启动时会加载它，并与你的项目 CLAUDE.md 合并使用。

---

## 项目级 vs 全局

### 全局适合放什么：
- 你的通用编码风格（命名习惯、做法）
- 你一直用的工具
- 沟通偏好
- 通用原则

### 项目级适合放什么：
- 团队标准（如果和你的全局设置不同）
- 项目专属技术栈
- 业务规则（PCI 合规等）
- 当前工作上下文

### 示例

**全局** (~/.claude/CLAUDE.md)：
```markdown
## My Style
函数式编程、清晰的变量名、有类型的函数
```

**项目** (my-payment-app/CLAUDE.md)：
```markdown
## Special Rules
安全关键——所有变更用 /plan。
必须处理 PCI 合规。
```

Claude 会合并两者：你的风格 + 项目规则。

---

## 练习：创建你的 CLAUDE.md

### 第一步：选一个项目

用现有项目或建一个测试目录：

```bash
mkdir test-claude-config
cd test-claude-config
git init
```

### 第二步：创建 CLAUDE.md

```bash
cat > CLAUDE.md << 'EOF'
# 我的测试项目

## Tech Stack
- 语言：[你的主力语言]
- 框架：[你在用的框架]
- 数据库：[如果有的话]

## Coding Standards
- [规则 1]
- [规则 2]

## My Preferences
- [偏好 1]
- [偏好 2]
EOF
```

### 第三步：启动 Claude

```bash
claude
```

Claude 会显示它在启动时加载了 CLAUDE.md。

### 第四步：测试

让 Claude 做点事，它应该遵循你的规则。

```
添加一个叫 greet 的函数，返回 "Hello, World!"
```

Claude 应该：
1. 提到你的技术栈
2. 遵循你的编码规范
3. 尊重你的偏好

---

## .claude/ 目录

本地设置（不纳入版本管理）放在 `.claude/` 里：

```
my-project/
├── CLAUDE.md           （纳入版本管理——团队规则）
├── .claude/
│   ├── settings.json   （不纳入版本管理——个人设置）
│   ├── agents/         （自定义智能体）
│   ├── skills/         （自定义技能）
│   └── hooks/          （自动化脚本）
```

添加到 `.gitignore`：
```
.claude/
.claude/settings.json
```

例外：如果 `.claude/agents/` 是团队共享的，可以纳入版本管理。

---

## Settings.json（可选）{ .optional }

需要更精细的控制时，创建 `.claude/settings.json`：

```json
{
  "model": "claude-opus-4-7",
  "temperature": 0.7,
  "context_threshold": 0.75,
  "auto_compact": true,
  "require_diff_review": true,
  "max_file_size": 10000
}
```

常用设置：
- **model**：使用哪个 Claude 模型
- **context_threshold**：什么时候警告上下文过高（0.7 = 70%）
- **auto_compact**：达到阈值时自动压缩
- **require_diff_review**：强制审查所有变更（安全的默认值）

---

## 智能体与技能（预览）

在 CLAUDE.md 中，可以引用自定义智能体：

```markdown
## Available Agents
- /code-reviewer：审查代码质量
- /security-auditor：扫描漏洞
- /test-writer：生成测试用例

使用方式：/agent code-reviewer
```

这些定义在 `.claude/agents/` 中（模块 04 会讲）。

---

## 最佳实践

### 应该

✅ 随着项目发展及时更新 CLAUDE.md

✅ 将项目级 CLAUDE.md 纳入版本管理（帮助队友）

✅ 要求写得越具体越好

✅ 包含"Current Status"章节，给 Claude 上文

✅ 记录重要的业务规则

### 不应该

❌ 在 CLAUDE.md 里存密码或密钥（用 .env 或密钥管理器）

❌ 写得太长（超过 500 行就太冗长了）

❌ 全局和项目之间出现冲突的规则

❌ 以为 Claude 会记住之前会话的偏好

---

## 验证：完成本模块的标志

✓ 你在项目中创建了 CLAUDE.md 文件

✓ 你能解释三级层级结构（全局、项目、个人）

✓ 你理解什么该放进已纳入版本管理的 CLAUDE.md，什么该放 .claude/

✓ 你启动过 Claude，看到它加载了你的 CLAUDE.md

✓ Claude 至少遵循了你 CLAUDE.md 里的一条规则

---

## 下一步

**模块 04：智能体与专业化**讲的是：
- 为特定任务创建专业智能体
- 限制智能体的能力
- 编排多个智能体
- 智能体的团队工作流

这教你如何创建专注的 AI 角色，而不是什么都用同一个通用 Claude。

---

**已完成模块 03？** → 准备进入模块 04：智能体与专业化
