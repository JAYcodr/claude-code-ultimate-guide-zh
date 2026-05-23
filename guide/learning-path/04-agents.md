<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

# 模块 04：智能体与专业化

**时间**: 1.5 小时 | **难度**: ⭐⭐ 初级

## 目标

为特定任务创建专业智能体。学会如何把 AI 能力聚焦在特定问题上。

---

## 你将学到

- 什么是智能体，为什么有用
- 用 AGENT.md 创建自定义智能体
- 限制智能体的能力（沙箱隔离）
- 让智能体执行特定任务
- 什么时候用智能体，什么时候直接用 Claude

---

## 什么是智能体？

**智能体（Agent）** 是 Claude Code 的一个专业版本，为某个特定任务配置而成。

### 示例：代码审查智能体

与其让普通 Claude 做代码审查（需要切换思路），你直接用：

```bash
/agent code-reviewer
审查这个函数，找 bug 和性能问题
```

代码审查智能体：
- 只处理代码审查
- 有审查专用的工具
- 了解安全漏洞模式
- 不会被其他任务分心

### 普通 Claude vs 智能体

| 对比项 | 普通 Claude | 智能体 |
|--------|-------------|--------|
| 范围 | 通用 | 专精 |
| 上下文 | 记住所有内容 | 专注任务记忆 |
| 工具 | 全部可用 | 受限集合 |
| 速度 | 多任务处理 | 单项快速 |
| 用途 | 探索、学习 | 重复性、特定任务 |

---

## 创建你的第一个智能体

智能体定义在 `.claude/agents/AGENT.md` 文件中。

### 基本结构

```markdown
---
name: code-reviewer
type: agent
description: 审查代码的 bug、性能和安全性
auto_invoke: false
requires_approval: true
---

# Code Reviewer Agent

## Purpose
审查代码：
- Bug 和逻辑错误
- 性能问题
- 安全漏洞
- 代码风格一致性
- 测试覆盖

## Tools
- 代码分析
- Git diff 查看器
- 测试运行器
- 代码检查工具

## Instructions
审查时：
1. 检查空指针和边界情况
2. 寻找性能瓶颈（O(n²)、嵌套循环）
3. 扫描安全问题（SQL 注入、XSS）
4. 确认测试覆盖了变更
5. 给出改进建议，语气不要苛刻

## Example Usage
/agent code-reviewer
审查 src/auth.js 的安全问题
```

### 文件位置

放在你的项目中：

```
my-project/
└── .claude/
    └── agents/
        └── code-reviewer.md
```

### 让它可用

在你的项目 CLAUDE.md 中引用它：

```markdown
## Available Agents
用 /agent [name] 调用智能体

- **code-reviewer** - 代码质量和安全审查
  用法：/agent code-reviewer <description>
   
- **test-writer** - 为代码生成测试
  用法：/agent test-writer <file path>
```

---

## 智能体设计模式

### 模式 1：质量检查器

```markdown
---
name: quality-auditor
description: 审查代码质量指标
---

# Quality Auditor

## Purpose
检查代码：
- 测试覆盖率（<80% = 不通过）
- 类型安全（TypeScript strict 模式）
- 代码重复
- 圈复杂度

## Tools
- 代码分析
- 覆盖率报告
- 类型检查器

## Output Format
- ✅ 通过：[指标] = X
- ⚠️ 警告：[指标] = X
- ❌ 不通过：[指标] = X

## Scoring
基于所有指标计算 /100 分数
```

### 模式 2：安全专精

```markdown
---
name: security-auditor
description: 扫描代码漏洞
requires_approval: true
---

# Security Auditor

## Purpose
发现安全漏洞：
- 注入攻击（SQL、NoSQL、命令注入）
- 认证/授权问题
- 加密错误
- 数据泄露风险
- OWASP Top 10

## Tools
- 静态分析
- 依赖检查
- 密钥检测

## Severity Levels
- CRITICAL：立即停工
- HIGH：合并前修复
- MEDIUM：下个迭代修复
- LOW：考虑修复
```

### 模式 3：文档写手

```markdown
---
name: doc-writer
description: 生成文档
---

# Documentation Writer

## Purpose
创建或改进：
- README 文件
- API 文档
- 架构文档
- 用户指南
- CHANGELOG 记录

## Output Format
- 清晰的标题
- 每个功能附带代码示例
- 链接到相关文档
- 流程用编号列表

## Style
- 对新手友好
- 不解释的专业术语不用
- 展示修改前后的对比
```

---

## 智能体的能力与限制

### 默认能力

所有智能体都能：
- 读取文件（git 感知）
- 分析代码
- 写文档
- 检查语法
- 运行测试

### 限制能力

用 `capabilities` 来限制智能体：

```markdown
---
name: code-reviewer
capabilities:
  - read_files      # 能读代码
  - run_tests       # 能跑测试
  - check_syntax    # 能代码检查
  - write_comments  # 能建议变更，但……
  - NO: commit      # ……不能提交
  - NO: push        # ……不能推送到 git
---
```

这个智能体可以审查代码，但不会意外把出问题的代码推送上去。

### 常用限制配置

```markdown
# 分析器（只读）
capabilities:
  - read_files
  - run_tests
# 不能修改任何东西

# 重构智能体（可写，不可推送）
capabilities:
  - read_files
  - write_files
  - run_tests
  - NO: commit
  - NO: push
# 可以改代码，但需要你先审查再推送

# 全权限智能体（无限制）
capabilities:
  - all
# 什么都能做（谨慎使用）
```

---

## 在工作流中使用智能体

### 调用智能体

```bash
/agent code-reviewer
审查我刚对 src/auth.js 做的修改
```

Claude 切换到 code-reviewer 智能体并回复。

### 链式调用智能体

依次使用多个智能体：

```bash
# 第 1 步：测试写手生成测试
/agent test-writer
为 src/utils/validators.js 写测试

# 第 2 步：代码审查员检查测试
/agent code-reviewer
审查刚才写的测试

# 第 3 步：安全审计员扫描
/agent security-auditor
检查测试和代码中是否有漏洞
```

### 智能体配合计划模式

对有风险的操作，在智能体中使用 `/plan`：

```bash
/agent refactoring-specialist
/plan
把支付处理模块重构为 async/await
```

---

## 练习：创建一个测试写手智能体

### 第一步：创建智能体文件

```bash
cat > .claude/agents/test-writer.md << 'EOF'
---
name: test-writer
description: 生成全面的测试
capabilities:
  - read_files
  - write_files
  - run_tests
---

# Test Writer Agent

## Purpose
为以下内容生成高质量的测试：
- 单元测试（纯函数）
- 集成测试（组件交互）
- 边界情况和错误条件
- 性能测试

## Style
- Arrange-Act-Assert 模式
- 描述性的测试名称
- 每个测试只关注一个行为
- 目标 70%+ 代码覆盖率

## Tools
- 测试框架（Jest、pytest 等）
- Mock 库
- 断言库

## Output
- 测试放在源代码同目录
- 命名：[file].test.js 或 [file].spec.js
- 包含 setup/teardown 代码
EOF
```

### 第二步：在 CLAUDE.md 中引用

```markdown
## Available Agents
- test-writer：为任意函数或模块生成测试
  用法：/agent test-writer <file path>
```

### 第三步：使用它

```bash
/agent test-writer
为 src/utils/formatDate.js 写测试
```

智能体会：
1. 读取 formatDate.js
2. 理解它做什么
3. 生成全面的测试
4. 展示测试文件给你看

### 第四步：审查

接受前检查测试：
- 覆盖了边界情况吗？
- 命名清晰吗？
- 能真正跑起来吗？

---

## 什么时候用智能体

### 用智能体：

✅ 你反复做同样的任务（代码审查、测试、安全审计）
✅ 你想让 AI 专注做一件事
✅ 你想限制能力范围（安全考虑）
✅ 你在搭建团队工作流
✅ 任务有清晰的验收标准

### 用普通 Claude：

✅ 你在探索/学习
✅ 任务是全新的
✅ 你需要通用帮助
✅ 你在调试复杂问题
✅ 你想要来回对话交流

---

## 最佳实践

### 应该

✅ 给智能体清晰、聚焦的职责

✅ 在智能体定义中写明输出格式

✅ 限制你不需要的能力

✅ 先在示例任务上测试智能体

✅ 将智能体纳入版本管理（在 .claude/agents/ 下）

### 不应该

❌ 创建职责重叠的智能体（会混淆）

❌ 让智能体太通用（违背了初衷）

❌ 完全信任智能体（始终要审查）

❌ 为一次性任务创建智能体（直接用 Claude 就好）

---

## 验证：完成本模块的标志

✓ 你至少创建了一个自定义智能体

✓ 你理解智能体和普通 Claude 的区别

✓ 你能限制智能体的能力

✓ 你知道如何调用智能体（/agent name）

✓ 你在真实任务上测试过你的智能体

---

## 下一步

**模块 05：技能与自动化**讲的是：
- 创建可复用的技能（知识模块）
- 打包能力以供分发
- 技能的自动调用
- 构建你的自定义知识库

这教你如何把知识打包让 Claude 跨会话记住。

---

**已完成模块 04？** → 准备进入模块 05：技能与自动化
