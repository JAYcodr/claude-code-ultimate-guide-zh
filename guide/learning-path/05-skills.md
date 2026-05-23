<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

# 模块 05：技能与自动化

**时间**: 1.5 小时 | **难度**: ⭐⭐ 初级

## 目标

创建可复用的技能，让 Claude 拥有领域专有知识。把对重复问题的解决方案打包。

---

## 你将学到

- 什么是技能，为什么它很强
- 用 SKILL.md 创建技能
- 技能的 frontmatter 和元数据
- 技能的自动调用
- 构建知识库
- 将技能与项目捆绑

---

## 什么是技能？

**技能（Skill）** 是一个可复用的知识模块。它教会 Claude 如何做特定的事情。

### 示例：测试技能

与其在每个会话中解释你的测试方法，不如创建一个技能：

```markdown
# Testing Best Practices for Our Project

## Framework: Jest

## Style
- 描述性名称："should validate email with + symbols"
- Arrange-Act-Assert 模式
- Mock 外部依赖
- 测试行为，不测试实现

## Coverage Target
最低 80%
```

现在，每当 Claude 帮忙写测试时，它会读取这个技能并遵循你的方法。

### 技能 vs 智能体

| 对比项 | 技能 | 智能体 |
|--------|------|--------|
| 目的 | 传授知识 | 执行任务 |
| 范围 | 领域知识 | 专业化工作流 |
| 持久性 | 每次会话都会记住 | 显式调用 |
| 自动调用 | 可以（可选） | 只能手动 |
| 示例 | "我们怎么写测试" | "测试写手智能体" |

---

## 创建你的第一个技能

技能是 `.claude/skills/` 目录下的 Markdown 文件。

### 基本结构

```markdown
---
name: testing-standards
description: 我们项目的测试实践和约定
triggers: [test, testing, jest, spec]
auto_invoke: false
keywords: [jest, unit-test, integration-test, mocking]
version: 1.0.0
---

# Testing Standards

## Framework
Jest with @testing-library/react

## File Organization
- 测试放在源码旁边
- 命名：`[Component].test.tsx`
- 测试数据放在 `__fixtures__/`
- Mock 文件放在 `__mocks__/`

## Test Structure (AAA)
1. **Arrange**：准备测试数据
2. **Act**：调用函数/组件
3. **Assert**：检查结果

## Example

```typescript
describe('validateEmail', () => {
  it('should accept valid email addresses', () => {
    // Arrange
    const email = 'user@example.com';
    
    // Act
    const result = validateEmail(email);
    
    // Assert
    expect(result).toBe(true);
  });
});
```

## Coverage Requirements
- 目标：最低 80%
- 关键路径：100%
- 覆盖类型：行、分支、函数

## Mocking Strategy
- 外部 API：用 jest.mock()
- 数据库：用测试夹具
- 定时器：用 jest.useFakeTimers()

## Running Tests
```bash
npm test                 # 运行所有测试
npm test -- --coverage   # 带覆盖率报告
npm test -- --watch      # 监听模式
```
```

### 文件位置

```
my-project/
└── .claude/
    └── skills/
        └── testing-standards.md
```

---

## 技能特性

### 触发器

当 Claude 看到特定关键词时，自动调用技能：

```markdown
---
triggers: [test, jest, spec, coverage, mock]
---
```

如果 Claude 看到"给这个函数加测试"，它会自动读取测试技能。

### 自动调用

```markdown
---
auto_invoke: true
---
```

设为 `true` 时，Claude 在会话启动时自动加载这个技能（无需你手动触发）。适用于关键规则。

### 关键词

帮助 Claude 搜索找到这个技能：

```markdown
---
keywords: [testing, jest, unit-test, mocking, assertions]
---
```

### 版本

追踪技能版本：

```markdown
---
version: 1.0.0
---
```

技能有重大变化时更新。

---

## 常用技能模式

### 模式 1：编码规范

```markdown
---
name: python-standards
triggers: [python, flask, django]
---

# Python Coding Standards

## Style
- PEP 8 规范（最长 100 字符）
- 所有函数加类型注解
- 文档字符串用 Google 格式

## Testing
- 用 pytest 做单元测试
- 最低 80% 覆盖率
- Mock 外部依赖

## File Organization
src/
├── models/
├── services/
├── controllers/
└── tests/

## Imports
```python
# ✅ 好：具体导入
from models import User
from services.auth import authenticate

# ❌ 不好：通配符导入
from models import *
```
```

### 模式 2：领域知识

```markdown
---
name: payment-processing
description: 支付系统规则和边界情况
auto_invoke: true
---

# Payment Processing Rules

## PCI Compliance
- 绝不能记录卡号
- 使用令牌化（Stripe）
- 加密敏感数据
- 审计所有交易

## Common Issues
1. 部分扣款：用指数退避重试
2. 货币转换：始终保留 2 位小数
3. 时区处理：所有时间用 UTC 存储

## Edge Cases
- 卡被拒：给出清晰的错误信息
- 卡过期：建议更新支付方式
- 3D Secure：处理验证流程
```

### 模式 3：流程文档

```markdown
---
name: code-review-checklist
triggers: [review, pull request, pr]
---

# Code Review Checklist

## Before Requesting Review
- [ ] 本地测试通过
- [ ] 没有 console.log
- [ ] 代码中没有密钥
- [ ] 提交信息清晰

## Security Checks
- [ ] 没有 SQL 注入漏洞
- [ ] 没有 XSS 漏洞
- [ ] 没有泄露的 API 密钥
- [ ] 输入已做校验

## Performance
- [ ] 没有 N+1 查询
- [ ] 没有无限循环
- [ ] 加载时间可接受

## Testing
- [ ] 添加了单元测试
- [ ] 更新了集成测试
- [ ] 覆盖率 >80%
```

---

## 打包技能

你可以将多个相关技能打包在一起。

### 项目技能包

```
my-project/
└── .claude/
    └── skills/
        ├── testing-standards.md
        ├── api-design.md
        ├── database-patterns.md
        └── security-checklist.md
```

在 CLAUDE.md 中引用它们：

```markdown
## Available Skills
我们的自定义技能会自动加载：
- **testing-standards**：我们怎么写测试
- **api-design**：REST API 规范
- **database-patterns**：常见查询和迁移
- **security-checklist**：安全审查流程
```

### 分发技能

与团队共享技能，将其纳入版本管理：

```bash
git add .claude/skills/
git commit -m "添加测试和 API 设计技能"
git push
```

团队成员签出项目后自动获得这些技能。

---

## 练习：创建一个领域技能

### 场景

你在建一个电商网站。想让 Claude 理解你的产品数据模型。

### 第一步：创建技能

```bash
cat > .claude/skills/product-data-model.md << 'EOF'
---
name: product-data-model
description: 电商产品数据结构和规则
triggers: [product, catalog, sku, price, inventory]
auto_invoke: false
version: 1.0.0
---

# Product Data Model

## Core Entities

### Product
```
{
  id: UUID,
  name: string,
  slug: string,  // URL 友好
  description: string,
  category_id: UUID,
  created_at: timestamp,
  updated_at: timestamp
}
```

### SKU (Stock Keeping Unit)
```
{
  id: UUID,
  product_id: UUID,
  sku: string,  // 例如 "BLUE-XL-001"
  price: decimal,  // 始终 2 位小数
  cost: decimal,
  inventory: integer,
  weight: float,  // 单位 kg
}
```

### Inventory Rules
- 下单时扣减库存
- 退货时增加库存
- 低库存提醒：<5 件
- 补货阈值：按产品设置

## Common Queries

### 获取产品及所有 SKU
```sql
SELECT p.*, s.* 
FROM products p 
JOIN skus s ON p.id = s.product_id 
WHERE p.slug = ?
```

### 检查库存
```sql
SELECT sum(inventory) FROM skus WHERE product_id = ?
```

## Edge Cases
1. 缺货：返回 404 或 "unavailable"
2. 变体选择：按 SKU 显示价格
3. 价格变动：在 SKU 层级更新，不是 Product 层级
EOF
```

### 第二步：在 CLAUDE.md 中引用

```markdown
## Skills
- **product-data-model**：了解我们的产品结构
```

### 第三步：使用它

在一个会话中：

```
写一个查询，找出所有低库存（<5 件）的产品
```

Claude 会：
1. 读取 product-data-model 技能
2. 理解你的数据结构
3. 写出正确的 SQL

---

## 最佳实践

### 应该

✅ 为重复做的事创建技能

✅ 保持技能专注（一个技能一个领域）

✅ 将技能纳入版本管理

✅ 在技能中包含示例

✅ 需求变化时更新技能

✅ 与团队分享技能

### 不应该

❌ 为一次性知识创建技能（用 CLAUDE.md 代替）

❌ 让技能太长（>500 行就拆成多个技能）

❌ 用技能存放临时指令（用 CLAUDE.md 或 AGENT.md）

❌ 以为技能本身就是完整的文档

---

## 技能生命周期

1. **创建**：识别重复的模式或领域知识
2. **记录**：写下技能，包含示例
3. **测试**：在会话中使用并验证 Claude 遵循了它
4. **优化**：根据反馈更新
5. **分享**：提交到 git，供团队使用
6. **维护**：随着实践发展而更新

---

## 验证：完成本模块的标志

✓ 你至少创建了一个自定义技能

✓ 你理解触发器和自动调用

✓ 你知道技能和智能体的区别

✓ 你能说明什么时候用技能，什么时候用 CLAUDE.md

✓ 你的技能在真实会话中测试过

---

## 下一步

**模块 06：钩子与事件**讲的是：
- 自动化系统事件的响应
- 提交前验证
- 操作后通知
- 构建安全的自动化

这教你如何让重复性任务自动完成，无需人工介入。

---

**已完成模块 05？** → 准备进入模块 06：钩子与事件
