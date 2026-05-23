---
name: explain
description: 以可调节的深度级别解释代码、概念或系统行为
argument-hint: <文件或概念>
effort: low
---

# 代码解释器

以可调节的深度级别解释代码、概念或系统行为。

## 目的

获取清晰的解释：
- 特定代码如何工作
- 为什么使用某些模式
- 系统/模块的功能
- 架构决策和权衡

## 使用说明

### 步骤 1：确定范围

确定需要解释的内容：
- **文件**：整个文件的结构和目的
- **函数/方法**：具体实现细节
- **概念**：架构模式或设计决策
- **流程**：数据/控制如何在系统中流转

### 步骤 2：评估复杂度

```
简单（1-2 分钟阅读）     → 快速摘要，仅关键点
标准（3-5 分钟阅读）     → 目的、工作原理、关键决策
深入（10+ 分钟阅读）     → 全面拆解、替代方案、权衡
```

### 步骤 3：收集上下文

```bash
# 文件解释
head -50 "$FILE"  # 查看导入和结构

# 函数解释
grep -A 30 "function $NAME\|def $NAME\|fn $NAME" "$FILE"

# 模块解释
ls -la "$DIR"
cat "$DIR/index.ts" 2>/dev/null || cat "$DIR/__init__.py" 2>/dev/null
```

### 步骤 4：组织解释结构

## 输出格式

---

### 📖 解释：[目标]

**范围**：[文件/函数/概念/流程]
**深度**：[简单/标准/深入]

### 功能说明

[1-3 句描述目的]

### 工作原理

[按深度级别逐步拆解]

### 关键决策

| 决策 | 原因 | 替代方案 |
|----------|-----|-------------|
| [所做选择] | [理由] | [其他可行方案] |

### 使用示例

```typescript
// 如何正确使用
```

### 相关代码

- `path/to/related.ts` - [关系]
- `path/to/dependency.ts` - [关系]

### 💡 学习笔记（带 --learn 标志时）

[理解更广泛模式的额外上下文]

---

## 深度级别

### 简单（`/explain --simple`）

```markdown
**validateUser()** 检查用户对象是否包含必填字段
（email、password）并返回布尔值。使用正则验证邮箱格式。
```

### 标准（`/explain` - 默认）

```markdown
**validateUser(user: User): ValidationResult**

**目的**：在数据库操作前验证用户输入。

**流程**：
1. 检查必填字段是否存在（email、password）
2. 用正则验证邮箱格式
3. 检查密码符合要求（8+ 字符、特殊字符）
4. 返回 { valid: boolean, errors: string[] }

**被以下函数使用**：signup()、updateProfile()
```

### 深入（`/explain --deep`）

```markdown
[标准模式的所有内容，外加：]

**设计决策**：
- 返回 ValidationResult 而非抛异常，以支持批量验证
- 选择正则而非库，实现零依赖
- 密码规则通过 config.ts 可配置

**权衡**：
- 优点：快速，无依赖
- 缺点：正则邮箱验证不符合 RFC

**曾考虑的替代方案**：
- Zod schema：更强大但增加 50KB
- Class-validator：适合装饰器但偏 OOP
```

## 使用示例

**解释文件：**
```
/explain src/auth/middleware.ts
```

**解释函数：**
```
/explain payments.ts 中的 handleWebhook 函数
```

**解释概念：**
```
/explain 我们的事件溯源如何工作
```

**指定深度解释：**
```
/explain --deep 认证流程
/explain --simple useCallback 的作用
```

**为学习而解释：**
```
/explain --learn 这里使用的仓库模式
```

## 提示

1. **具体化**："解释第 45-60 行" > "解释这个文件"
2. **说明你的水平**："我是 TypeScript 新手" 有助于校准
3. **追问跟进**："为什么不用 X？" 加深理解
4. **请求类比**："我熟悉 Python 但不熟悉 TS" 帮助类比

$ARGUMENTS
