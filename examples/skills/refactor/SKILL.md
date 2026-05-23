---
name: refactor
description: 分析代码中的 SOLID 违规并建议有针对性的改进
argument-hint: "<文件或模块> [--pattern <名称>]"
effort: medium
disable-model-invocation: true
---

# SOLID 重构助手

分析代码中的 SOLID 违规并建议有针对性的改进。

## 目的

基于以下方面识别重构机会：
- SOLID 原则违规
- 代码异味和反模式
- 复杂度指标
- 重复检测

## 使用说明

### 步骤 1：范围分析

根据用户输入确定重构范围：
- 单个文件：深度分析
- 目录：跨文件模式检测
- 函数/类：聚焦提取建议

```bash
# 获取文件/目录统计
if [ -f "$TARGET" ]; then
  wc -l "$TARGET"
  echo "单文件分析"
elif [ -d "$TARGET" ]; then
  find "$TARGET" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" \) | wc -l
  echo "目录分析"
fi
```

### 步骤 2：SOLID 违规检测

#### S - 单一职责

查找：
- 超过 300 行的文件
- 超过 50 行的函数
- 超过 10 个方法的类
- 混合关注点（数据 + UI + 业务逻辑）

```bash
# 查找大文件
find . -name "*.{ts,js,py}" -exec wc -l {} + 2>/dev/null | sort -rn | head -10

# 行数多的函数（近似）
grep -rn "function\|def \|fn " --include="*.{ts,js,py,rs}" . | head -20
```

#### O - 开闭原则

查找：
- 对类型使用 switch/case
- 重复的 if/else 类型检查
- 直接修改而非扩展

#### L - 里氏替换

查找：
- 抛出"not implemented"的重写方法
- 方法调用前的类型检查
- 空方法重写

#### I - 接口隔离

查找：
- 大接口（超过 10 个方法）
- 实现了未使用的接口方法的类
- 臃肿的服务类

#### D - 依赖反转

查找：
- 直接实例化依赖（`new Service()`）
- 硬编码的类引用
- 缺少依赖注入

### 步骤 3：代码异味

```bash
# 重复模式
grep -rn --include="*.{ts,js,py}" . 2>/dev/null | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -10

# 长参数列表（> 4 个参数）
grep -rn "function.*,.*,.*,.*," --include="*.{ts,js}" . 2>/dev/null | head -10

# 深度嵌套（4 层以上）
grep -rn "^\s\{16,\}" --include="*.{ts,js,py}" . 2>/dev/null | head -10
```

### 步骤 4：复杂度评估

对发现的每个问题评估：
- **影响**：影响多少代码？
- **风险**：可能破坏什么？
- **工作量**：需要改多少行、需要多少测试？

## 输出格式

---

### 🔧 重构分析

**目标**：[文件/目录]
**分析行数**：[数量]

### 📊 SOLID 评分卡

| 原则 | 状态 | 发现的问题数 |
|-----------|--------|--------------|
| 单一职责 | 🟡 | 3 个大类 |
| 开闭原则 | 🟢 | OK |
| 里氏替换 | 🟢 | OK |
| 接口隔离 | 🔴 | 2 个臃肿接口 |
| 依赖反转 | 🟡 | 5 处直接实例化 |

### 🎯 优先重构项

#### 1. [影响最大] - 从 `UserService` 提取类

**违规**：单一职责
**当前**：450 行，处理 auth + profile + notifications
**建议**：
```
UserService.ts (450 行)
    ↓ 提取
AuthService.ts (~150 行)
ProfileService.ts (~150 行)
NotificationService.ts (~100 行)
```
**风险**：中（更新导入）
**需要的测试**：更新测试中的依赖注入

#### 2. [第二优先级] - 用多态替换 switch

**位置**：`src/handlers/payment.ts:45`
**当前**：
```typescript
switch (paymentType) {
  case 'card': // 50 行
  case 'bank': // 50 行
  case 'crypto': // 50 行
}
```
**建议**：使用 `PaymentProcessor` 接口的策略模式
**风险**：低（隔离变更）

### 📝 代码异味

| 异味 | 位置 | 严重性 |
|-------|----------|----------|
| 长方法 | `api.ts:calculateTotal`（120 行） | 🟠 高 |
| 重复代码 | `utils/*.ts`（3 个相似块） | 🟡 中 |
| 深度嵌套 | `parser.ts:parse`（6 层） | 🟡 中 |

### 🚀 速胜（低风险、高价值）

1. 将 `validateEmail()` 提取到共享工具（在 4 处使用）
2. 用命名常量替换魔法数字
3. 添加提前返回到 `processOrder()` 以减少嵌套

### ⚠️ 技术债务说明

- [要在未来迭代中跟踪的条目]

---

## 重构安全清单

应用建议前：

- [ ] 受影响代码存在测试
- [ ] 创建功能分支
- [ ] 提交当前状态
- [ ] 一次只应用一个重构
- [ ] 每次修改后运行测试
- [ ] 提交前审查 diff

## 用法

**分析特定文件：**
```
/refactor src/services/user.ts
```

**分析目录：**
```
/refactor src/api/
```

**关注特定原则：**
```
/refactor --focus=srp src/services/
```

**带复杂度阈值：**
```
/refactor --threshold=high
```

## 参考

- Martin Fowler 的 Refactoring Catalog
- 《代码整洁之道》Robert C. Martin
- SOLID 原则 by Robert C. Martin

$ARGUMENTS
