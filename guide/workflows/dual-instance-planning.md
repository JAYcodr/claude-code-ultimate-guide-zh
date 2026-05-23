---
title: "双实例计划工作流"
description: "使用两个 Claude 实例，分别承担计划和实现角色"
tags: [workflow, architecture, design-patterns]
---

# 双实例计划工作流

> **可信度**：第 2 层 — 基于实践者经验（Jon Williams，2026 年 2 月）。模式经过 6 个月从 Cursor 到 Claude Code 的个人转型验证。

使用两个 Claude 实例，分别承担不同角色：一个用于计划和审查（Claude Zero），一个用于实现（Claude One）。职责分离提高了计划质量，减少了实现错误。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用此模式](#何时使用此模式)
3. [设置](#设置)
4. [完整工作流](#完整工作流)
5. [计划模板](#计划模板)
6. [成本分析](#成本分析)
7. [技巧与故障排查](#技巧与故障排查)
8. [另见](#另见)

---

## TL;DR

```
1. 启动 Claude Zero（计划者）：探索、编写计划、审查
2. 启动 Claude One（实现者）：读取计划、写代码、提交
3. 人工看门人：在实现前批准计划
4. 计划目录：Review/ → Active/ → Completed/
5. 成本：约 $100-200/月（vs Boris 水平模式 $500-1K）
```

**最适合**：独立开发者、需求密集型工作、质量优先于速度、预算 <$300/月

---

## 何时使用此模式

### ✅ 使用场景

- **复杂规范**：需求需要通过访谈式问题澄清
- **质量关键功能**：安全、支付、数据迁移
- **学习阶段**：新代码库、不熟悉的模式
- **产品设计师编码**：非开发者背景，需要计划严谨性
- **预算限制**：$100-200/月（vs 并行多实例 $500-1K）
- **需求密集型工作流**：详细需求、许多边缘情况

### ❌ 不使用场景

- **简单更改**：拼写错误修复、微不足道的重构（使用单实例）
- **探索性编码**：问题空间未知（计划开销不合理）
- **紧迫期限**：速度 > 质量（接受纠正循环）
- **高容量并行功能**：改用 Boris 模式（第 9.17 节）
- **预算非常有限**：<$100/月（使用 Sonnet，单实例）

### 与其他模式对比

| 模式 | 扩展轴 | 成本/月 | 最适合 |
|---------|--------------|------------|----------|
| **单实例** | 无 | $50-100 | 大多数开发者，通用用途 |
| **双实例（Jon）** | 垂直（计划 ↔ 实现） | $100-200 | 需求密集、质量聚焦 |
| **多实例（Boris）** | 水平（5-15 并行） | $500-1,000 | 团队、高容量发布 |

---

## 设置

### 步骤 1：创建目录结构

```bash
cd ~/projects/your-project
mkdir -p .claude/plans/{Review,Active,Completed}
```

**目录角色**：
- `Review/` — 等待人工批准的计划
- `Active/` — 已批准正在实现的计划
- `Completed/` — 已归档计划（学习资源）

**添加到 .gitignore**：
```bash
# .gitignore
.claude/plans/Review/
.claude/plans/Active/
# 可选：为团队学习提交 Completed/
```

### 步骤 2：启动 Claude Zero（计划者）

**终端 1**：
```bash
cd ~/projects/your-project
claude
```

**第一条消息**（角色强制）：
```
You are Claude Zero (Planner).

你的角色：
- 使用计划模式探索代码库（Shift+Tab 两次）
- 通过访谈了解需求
- 将详细计划写入 .claude/plans/Review/
- 在 Claude One 完成后审查实现
- 永远不直接编辑代码
- 永远不提交变更

开始时确认此角色。
```

Claude Zero 确认："明白了。我是 Claude Zero（计划者）。我将探索、计划和审查，但绝不触碰代码。"

### 步骤 3：启动 Claude One（实现者）

**终端 2**（新会话）：
```bash
cd ~/projects/your-project
claude
```

**第一条消息**（角色强制）：
```
You are Claude One (Implementer).

你的角色：
- 从 .claude/plans/Active/ 读取批准的计划
- 严格按照规范实现
- 每个逻辑步骤后提交变更
- 向用户报告完成情况
- 永远不创建计划
- 永远不跳过批准步骤

开始时确认此角色。
```

Claude One 确认："明白了。我是 Claude One（实现者）。我只执行批准的计划。"

---

## 完整工作流

### 阶段 1：计划（Claude Zero）

#### 步骤 1.1：开始计划

**你**（对 Claude Zero）：
```
# 进入计划模式（Shift+Tab 两次），然后：

为 API 实现 JWT 认证：
- 访问令牌（15 分钟过期）
- 刷新令牌（7 天过期）
- 保护路由的中间件
- 注销功能（撤销刷新令牌）
```

#### 步骤 1.2：Claude Zero 探索

Claude Zero（处于计划模式）：
- 读取现有认证代码
- 搜索代码库中的认证模式
- 识别依赖项（库、环境变量）

#### 步骤 1.3：Claude Zero 访谈你

Claude Zero 提出澄清问题：
```
在我起草计划之前，需要澄清：

1. 我们是否支持每个用户多个并发会话？
   （例如，用户同时在手机和笔记本电脑上登录）

2. 刷新令牌应该存储在哪里？
   - 数据库表
   - Redis
   - 其他

3. 哪些路由应该被保护？
   - 所有 /api/* 路由？
   - 仅特定路由？

4. 你想在登录尝试上设置速率限制吗？

5. "完成"的成功标准是什么？
   - 测试通过？
   - Postman 集合？
   - 文档已更新？
```

**你回答**，Claude Zero 完善理解。

#### 步骤 1.4：Claude Zero 编写计划

Claude Zero 创建 `.claude/plans/Review/auth-jwt.md`：

```markdown
# 计划：JWT 认证

**创建时间**：2026-02-04
**作者**：Claude Zero
**估计工作量**：3-4 小时
**风险级别**：中等（安全关键）

## 摘要
实现基于 JWT 的认证，采用访问/刷新令牌模式。
支持每个用户多个并发会话。
刷新令牌存储在数据库中，可撤销。

## 需求澄清
- 每个用户多个会话：是
- 刷新令牌存储：数据库（新表）
- 受保护路由：除 /api/auth/* 外的所有 /api/*
- 速率限制：是（每 15 分钟 5 次尝试）
- 成功标准：测试通过 + Postman 集合

## 要创建的文件

### 1. src/auth/jwt.ts（约 120 行）
**用途**：JWT 工具函数

**导出**：
- `generateAccessToken(userId: string): string`
  - Payload：{ userId, type: 'access' }
  - 过期时间：15 分钟
  - 使用 JWT_SECRET 签名

- `generateRefreshToken(userId: string): string`
  - Payload：{ userId, type: 'refresh', jti: uuid() }
  - 过期时间：7 天
  - 使用 JWT_REFRESH_SECRET 签名
  - jti = 用于撤销的唯一令牌 ID

- `verifyAccessToken(token: string): { userId: string } | null`
  - 验证签名
  - 检查过期
  - 返回 payload 或 null

- `verifyRefreshToken(token: string): { userId: string, jti: string } | null`
  - 验证签名
  - 检查过期
  - 检查未被撤销（数据库查询）
  - 返回 payload 或 null

**依赖**：jsonwebtoken、uuid

### 2. src/middleware/auth.ts（约 60 行）
**用途**：认证中间件

**导出**：
- `requireAuth(req, res, next)`
  - 从 Authorization header（Bearer 格式）提取令牌
  - 使用 verifyAccessToken() 验证
  - 将 userId 附加到 req.userId
  - 无效/缺失时返回 401

**依赖**：jwt.ts

### 3. src/db/migrations/YYYYMMDD_create_refresh_tokens.ts（约 40 行）
**用途**：刷新令牌的数据库表

**Schema**：
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  jti UUID NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  revoked_at TIMESTAMP
);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_jti ON refresh_tokens(jti);
```

## 要修改的文件

### 1. src/routes/api.ts
**位置**：第 23 行（导入之后）
**更改**：将 requireAuth 中间件应用于除 /auth/* 外的所有路由

**之前**：
```typescript
router.get('/profile', profileController);
router.post('/posts', createPostController);
```

**之后**：
```typescript
import { requireAuth } from '../middleware/auth';
router.get('/profile', requireAuth, profileController);
router.post('/posts', requireAuth, createPostController);
```

### 2. src/routes/auth.ts
**位置**：创建新文件或添加到现有 auth 路由
**更改**：
- POST /auth/login → 返回 { accessToken, refreshToken }
- POST /auth/refresh → 用刷新令牌换取新访问令牌
- POST /auth/logout → 撤销刷新令牌

### 3. src/config/env.ts
**位置**：第 15 行（现有 secrets 之后）
**添加**：
```typescript
JWT_SECRET: process.env.JWT_SECRET || '',
JWT_REFRESH_SECRET: process.env.JWT_REFRESH_SECRET || '',
```

### 4. .env.example
**添加**：
```
JWT_SECRET=your-secret-here-min-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-here-min-32-chars
```

## 实现步骤（顺序）

1. **安装依赖**
   ```bash
   npm install jsonwebtoken uuid
   npm install --save-dev @types/jsonwebtoken @types/uuid
   ```

2. **创建 JWT 工具**（jwt.ts）
   - 实现所有 4 个函数
   - 添加错误处理（verify 上的 try/catch）

3. **运行数据库迁移**（refresh_tokens 表）
   - 测试迁移 up/down

4. **创建认证中间件**（auth.ts）
   - 实现 requireAuth
   - 用模拟令牌测试

5. **创建/更新 auth 路由**（auth.ts 路由）
   - POST /auth/login
   - POST /auth/refresh
   - POST /auth/logout

6. **保护现有路由**（api.ts）
   - 将 requireAuth 应用于所有 /api/* 路由

7. **将 JWT secrets 添加到 .env**
   - 生成安全随机字符串（64 个字符）

8. **编写测试**
   - jwt.ts 函数的单元测试
   - auth 流的集成测试
   - 测试令牌过期
   - 测试撤销

9. **创建 Postman 集合**
   - 登录 → 获取令牌
   - 使用访问令牌访问受保护路由
   - 刷新访问令牌
   - 注销 → 撤销刷新令牌
   - 验证被撤销的令牌被拒绝

## 成功标准

- [ ] POST /auth/login 返回 accessToken + refreshToken
- [ ] 受保护路由在无有效访问令牌时返回 401
- [ ] 受保护路由在有有效访问令牌时返回 200
- [ ] POST /auth/refresh 用刷新令牌换取新访问令牌
- [ ] POST /auth/logout 撤销刷新令牌
- [ ] 被撤销的刷新令牌在 /auth/refresh 上被拒绝
- [ ] 过期的访问令牌被拒绝
- [ ] 每个用户多个会话工作（不同的刷新令牌）
- [ ] 所有测试通过（npm test）
- [ ] Postman 集合端到端工作

## 安全清单

- [ ] JWT secrets 在 .env 中（永不提交）
- [ ] JWT secrets ≥32 个字符
- [ ] 刷新令牌存储在数据库中（不只是 JWT）
- [ ] 刷新令牌有唯一 jti 用于撤销
- [ ] 访问令牌过期时间短（15 分钟）
- [ ] Authorization header 已验证（Bearer 格式）
- [ ] 令牌验证错误被捕获（无崩溃）

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|--------|------------|
| JWT secrets 泄露 | 高 | .env 在 .gitignore 中，永不记录 secrets |
| 令牌过期时间过长 | 中 | 15 分钟访问，7 天刷新（足够短） |
| 登录无速率限制 | 中 | 添加速率限制（每 15 分钟 5 次尝试） |
| 刷新令牌表无限增长 | 低 | 添加清理作业（删除过期令牌） |

## 给实现者（Claude One）的问题

如果在实现过程中遇到这些场景：

1. **现有用户登录流程**：与现有登录逻辑集成，不要替换整个认证系统
2. **数据库 ORM**：使用现有 ORM（Prisma/TypeORM/Knex）用于 refresh_tokens 表
3. **错误消息**：返回通用的"无效令牌"（不要泄露令牌是过期还是无效签名）

## 估计工作量分解

- JWT 工具：45 分钟
- 数据库迁移：15 分钟
- 中间件：30 分钟
- Auth 路由：60 分钟
- 保护现有路由：15 分钟
- 测试：90 分钟
- Postman 集合：15 分钟

**总计**：约 4 小时

---

**计划已批准？** → 移动到 `.claude/plans/Active/auth-jwt.md`
```

### 阶段 2：人工审查

**你审查** `.claude/plans/Review/auth-jwt.md`：

**清单**：
- [ ] 所有需求都已覆盖？
- [ ] 方法对这个代码库合理吗？
- [ ] 安全考虑已解决？
- [ ] 估计工作量现实吗？
- [ ] 成功标准清晰且可测试？
- [ ] 要创建/修改的文件路径正确？

**如果批准**：
```bash
mv .claude/plans/Review/auth-jwt.md .claude/plans/Active/
```

**如果需要更改**，要求 Claude Zero 修改：
```
（对 Claude Zero）：更新计划：
- 将刷新令牌过期时间改为 30 天而不是 7 天
- 在范围内添加密码重置流程
```

### 阶段 3：实现（Claude One）

**你**（对 Claude One）：
```
实现 .claude/plans/Active/auth-jwt.md

严格按照计划执行。每个逻辑步骤后提交。
完成后报告。
```

Claude One：
1. 读取计划文件
2. 安装依赖
3. 创建 jwt.ts
4. 创建数据库迁移
5. 运行迁移
6. 创建认证中间件
7. 更新路由
8. 添加环境变量
9. 编写测试
10. 创建 Postman 集合

**Claude One** 在每步后提交：
```
feat: add JWT utility functions
feat: create refresh_tokens table migration
feat: add auth middleware
feat: protect API routes with JWT auth
test: add JWT auth flow tests
```

### 阶段 4：验证（Claude Zero）

**你**（对 Claude Zero）：
```
审查 Claude One 刚完成的 JWT 实现。
对照 .claude/plans/Active/auth-jwt.md 中的计划进行检查。
```

Claude Zero 审查：
- 代码结构符合计划？
- 所有成功标准满足？
- 安全清单完成？
- 测试通过？
- 有无代码异味或问题？

**Claude Zero 报告**：
```
✅ Review complete: auth-jwt.md

Code Quality: 9/10
- All files created as planned
- Success criteria met (9/9)
- Security checklist complete
- Tests pass (15/15)

Minor suggestions:
1. Consider adding refresh token rotation (security best practice)
2. Add JSDoc comments to jwt.ts functions
3. Consider extracting magic numbers (15min, 7 days) to config

Critical issues: None

Ready to archive plan to Completed/.
```

### 阶段 5：归档

**如果批准**：
```bash
mv .claude/plans/Active/auth-jwt.md .claude/plans/Completed/
```

**计划现在已归档**，供将来参考和团队学习。

---

## 计划模板

将此模板保存到 `.claude/plan-template.md` 以获得一致的计划结构：

```markdown
# 计划：[功能名称]

**创建时间**：[日期]
**作者**：Claude Zero
**估计工作量**：[小时]
**风险级别**：低 | 中 | 高

## 摘要
[2-3 句话概述此计划实现的功能]

## 需求澄清
[通过访谈确认的需求列表]
- 需求 1：[答案]
- 需求 2：[答案]

## 要创建的文件

### 1. [文件路径]（约 [行数] 行）
**用途**：[此文件的作用]

**导出**：
- `functionName(params): returnType`
  - [它的作用]
  - [关键实现细节]

**依赖**：[库、其他文件]

## 要修改的文件

### 1. [文件路径]
**位置**：第 [N] 行（[上下文：在什么之后，什么之前]）
**更改**：[要更改什么]

**之前**：
```[语言]
[现有代码片段]
```

**之后**：
```[语言]
[修改后的代码片段]
```

## 实现步骤（顺序）

1. **[步骤名称]**
   - [子步骤]
   - [子步骤]

2. **[步骤名称]**
   - [子步骤]

## 成功标准

- [ ] [可测试标准 1]
- [ ] [可测试标准 2]

## 安全清单（如适用）

- [ ] [安全项目 1]
- [ ] [安全项目 2]

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|--------|------------|
| [风险] | [高/中/低] | [如何预防/处理] |

## 给实现者（Claude One）的问题

如果在实现过程中遇到这些场景：
1. [场景]：[指导]

## 估计工作量分解

- [任务 1]：[时间]
- [任务 2]：[时间]

**总计**：[小时]

---

**计划已批准？** → 移动到 `.claude/plans/Active/[filename].md`
```

---

## 成本分析

### 双实例 vs 带纠正的单实例

| 场景 | 单实例 | 双实例 | 节省 |
|----------|----------------|---------------|---------|
| **简单功能**（登录表单） | 1 会话 × $5 = **$5** | 2 会话 × $3 = $6 | +$1（单实例胜） |
| **中等功能**（认证系统） | 1 会话 × $15 + 2 次纠正 × $10 = **$35** | 2 会话 × $12 = $24 | **$11 节省** |
| **复杂功能**（模糊规范） | 1 会话 × $20 + 3 次纠正 × $15 = **$65** | 2 会话 × $18 = $36 | **$29 节省** |

**盈亏平衡点**：需要 ≥2 次纠正循环的功能 → 双实例更便宜。

### 月度预算估算

**假设**：
- 每月 20 个工作日
- 每天 2 个功能（简单 + 复杂的混合）
- Opus 4.5 定价（~$15/1M 输入，$75/1M 输出）

| 用户类型 | 功能/月 | 单实例 | 双实例 | 节省 |
|---------|----------------|----------------|---------------|---------|
| **轻度用户** | 20 个简单 | $100 | $120 | -$20（单实例胜） |
| **中度用户** | 30 个混合（60% 中等，40% 简单） | $650 | $480 | **$170 节省** |
| **重度用户** | 40 个复杂 | $2,000 | $1,200 | **$800 节省** |

**建议**：
- 仅有简单功能 → 单实例
- 中等/复杂功能 → 双实例省钱省时间

---

## 技巧与故障排查

### 角色强制

**问题**：Claude Zero 开始编辑代码。

**解决方案**：在每个请求中提醒：
```
（对 Claude Zero）：记住：你是 Claude Zero（仅计划者）。
不编辑代码。将计划写入 .claude/plans/Review/
```

**预防**：使用 CLAUDE.md 强制角色：

```markdown
# .claude/CLAUDE.md

## 如果你是 Claude Zero（计划者）：
- 使用计划模式进行所有探索（Shift+Tab 两次）
- 将所有计划保存到 .claude/plans/Review/[feature].md
- 永远不编辑代码
- 永远不提交变更
- 在 Claude One 完成后审查实现

## 如果你是 Claude One（实现者）：
- 从 .claude/plans/Active/ 读取计划
- 严格按照规范实现
- 每个逻辑步骤后提交
- 永远不创建计划
```

### 上下文污染

**问题**：Claude One 的上下文被计划讨论污染。

**解决方案**：使用独立的终端会话（独立上下文）：
- 终端 1 = Claude Zero（计划上下文）
- 终端 2 = Claude One（实现上下文）

**永不共享上下文** 在 Claude Zero 和 Claude One 之间。

### 计划漂移

**问题**：Claude One 在实现过程中偏离计划。

**解决方案**：在计划中包含此内容：
```markdown
## Claude One 的实施规则

- 按顺序执行计划步骤（不跳过或重新排序）
- 如果遇到阻塞器，停止并报告（不要即兴发挥）
- 每步后提交（粒度历史）
- 如果不清楚，问用户（不要猜测）
```

### 开销管理

**问题**：在目录之间移动文件是手动开销。

**解决方案**：创建 bash 别名：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc

# 将计划移动到 Active（批准）
approve-plan() {
    mv ".claude/plans/Review/$1.md" ".claude/plans/Active/"
    echo "✅ Approved: $1.md → Active/"
}

# 将计划移动到 Completed（归档）
complete-plan() {
    mv ".claude/plans/Active/$1.md" ".claude/plans/Completed/"
    echo "✅ Completed: $1.md → Archived"
}

# 按状态列出计划
plans() {
    echo "📋 Review:"
    ls -1 .claude/plans/Review/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "🔄 Active:"
    ls -1 .claude/plans/Active/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "✅ Completed:"
    ls -1 .claude/plans/Completed/ 2>/dev/null | tail -5 || echo "  (empty)"
}
```

**用法**：
```bash
plans                     # 列出所有计划
approve-plan auth-jwt     # 批准计划
complete-plan auth-jwt    # 归档完成计划
```

---

## 另见

- **主指南**：[第 9.17.1 节](#alternative-pattern-dual-instance-planning-vertical-separation) — 概述和对比
- **计划模式**：[plan-driven.md](plan-driven.md) — 计划工作流的基础
- **多实例（Boris）**：[第 9.17 节](#917-scaling-patterns-multi-instance-workflows) — 水平扩展替代方案
- **成本优化**：[第 8.10 节](#cost-optimization-tips) — 预算管理

**外部资源**：
- [Jon Williams LinkedIn 帖子](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu) — 原始模式描述（2026 年 2 月 3 日）
- [Claude Code 团队的 10 个技巧](https://paddo.dev/blog/claude-code-team-tips/) — 包括计划优先方法的工作流