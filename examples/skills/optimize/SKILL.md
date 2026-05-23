---
name: optimize
description: 分析并建议代码、查询或系统的性能改进
argument-hint: "<文件或模块> [--focus speed|memory|bundle]"
effort: medium
disable-model-invocation: true
---

# 性能优化器

分析并建议代码、查询或系统的性能改进。

## 目的

识别优化机会：
- 运行时性能瓶颈
- 内存使用问题
- 数据库查询效率低下
- 打包体积问题
- 算法复杂度

## 使用说明

### 步骤 1：确定范围

确定优化目标：
- **函数**：单个函数性能
- **模块**：相关函数/类
- **查询**：数据库查询优化
- **打包**：前端打包分析
- **系统**：架构级优化

### 步骤 2：性能分析

#### 运行时分析

```bash
# 查找可能慢的模式
grep -rn "forEach\|\.map\|\.filter\|\.reduce" --include="*.{ts,js}" . | head -20

# 查找嵌套循环（可能的 O(n²)）
grep -rn "for.*for\|\.forEach.*\.forEach\|\.map.*\.map" --include="*.{ts,js}" . | head -10

# 查找可异步的同步操作
grep -rn "readFileSync\|writeFileSync\|execSync" --include="*.{ts,js}" . | head -10
```

#### 内存分析

```bash
# 大型数组操作
grep -rn "new Array\|Array\.from\|\.concat\|spread" --include="*.{ts,js}" . | head -10

# 潜在的内存泄漏（事件监听、定时器）
grep -rn "addEventListener\|setInterval\|setTimeout" --include="*.{ts,js}" . | head -10
```

#### 数据库查询分析

```bash
# N+1 查询模式
grep -rn "await.*find\|await.*query" --include="*.{ts,js}" . | head -15

# 缺少索引提示
grep -rn "WHERE\|ORDER BY\|GROUP BY" --include="*.{ts,js,sql}" . | head -15
```

#### 打包分析

```bash
# 检查打包大小（如适用）
[ -f "package.json" ] && npm run build 2>/dev/null && ls -lh dist/*.js 2>/dev/null

# 大型依赖
[ -f "package.json" ] && cat package.json | jq '.dependencies | keys[]' | head -20
```

### 步骤 3：优先级排序

按以下因素排序发现：
1. **影响**：这将提升多少性能？
2. **工作量**：修复难度如何？
3. **风险**：可能破坏什么？

## 输出格式

---

### ⚡ 性能分析

**目标**：[文件/模块/系统]
**分析日期**：[时间戳]

### 📊 当前指标（若可测量）

| 指标 | 当前 | 目标 | 差距 |
|--------|---------|--------|-----|
| 响应时间 | Xms | <Yms | 需减少 -Z% |
| 内存使用 | XMB | <YMB | 需减少 -Z% |
| 打包大小 | XKB | <YKB | 需减少 -Z% |

### 🔴 关键问题

#### 1. [问题标题] - [位置]

**问题**：[什么慢及原因]

**当前**：
```typescript
// O(n²) - 嵌套循环
users.forEach(user => {
  permissions.forEach(perm => {
    if (user.id === perm.userId) { ... }
  });
});
```

**优化后**：
```typescript
// O(n) - Map 查找
const permMap = new Map(permissions.map(p => [p.userId, p]));
users.forEach(user => {
  const perm = permMap.get(user.id);
  if (perm) { ... }
});
```

**影响**：1000 个用户时快约 10 倍
**工作量**：低（5 分钟）
**风险**：低

### 🟠 高优先级

| 问题 | 位置 | 影响 | 工作量 |
|-------|----------|--------|--------|
| [描述] | file:line | [估计] | [时间] |

### 🟡 中优先级

| 问题 | 位置 | 影响 | 工作量 |
|-------|----------|--------|--------|
| [描述] | file:line | [估计] | [时间] |

### 💡 速胜

1. [效果好的小改动]
2. [另一个快速优化]
3. [低挂果实]

### 📈 优化路线图

```
第 1 周：关键修复（第 1-3 项）
第 2 周：高优先级（第 4-6 项）
第 3 周：测量和验证改进
```

---

## 常见模式

### 数组操作

| 模式 | 问题 | 修复 |
|---------|-------|-----|
| `arr.filter().map()` | 两次遍历 | 单次 `reduce()` 或 `flatMap()` |
| 循环中的 `arr.find()` | O(n²) | 先构建 Map/Set |
| `[...arr1, ...arr2]` | 内存分配 | `arr1.concat(arr2)` 或 push |

### 数据库

| 模式 | 问题 | 修复 |
|---------|-------|-----|
| 循环中 await | N+1 查询 | 用 `IN` 批量查询 |
| `SELECT *` | 过度获取 | 只选需要的列 |
| 缺少 WHERE 索引 | 全表扫描 | 添加复合索引 |

### React/前端

| 模式 | 问题 | 修复 |
|---------|-------|-----|
| JSX 中的内联函数 | 重渲染 | `useCallback` |
| 大型列表渲染 | DOM 抖动 | 虚拟化 |
| 未优化的图片 | LCP 慢 | Next/Image、懒加载 |

### Node.js

| 模式 | 问题 | 修复 |
|---------|-------|-----|
| 同步文件操作 | 阻塞事件循环 | 异步替代 |
| JSON.parse 大文件 | 内存峰值 | 流式解析器 |
| 无连接池 | 连接开销 | 使用 pg-pool 等池化 |

## 用法

**分析特定文件：**
```
/optimize src/services/user.ts
```

**关注特定领域：**
```
/optimize --queries src/repositories/
/optimize --bundle
/optimize --memory src/workers/
```

**带目标指标：**
```
/optimize --target=100ms src/api/search.ts
```

**快速扫描：**
```
/optimize --quick
```

## 说明

- 测量优于假设：优化前先分析
- 过早优化是万恶之源（Knuth）
- 关注热点路径：优化经常运行的代码
- 考虑权衡：速度 vs 可读性 vs 可维护性

$ARGUMENTS
