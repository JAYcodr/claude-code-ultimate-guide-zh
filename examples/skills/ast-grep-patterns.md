---
name: ast-grep-patterns
description: "教 Claude 何时以及如何使用 ast-grep 进行结构化代码搜索的技能"
effort: low
---

# 适用于 Claude Code 的 ast-grep 模式

> **技能**：教 Claude 何时以及如何使用 ast-grep 进行结构化代码搜索

## 安装

```bash
# 安装 ast-grep 技能
npx skills add ast-grep/agent-skill

# 或通过插件市场
/plugin marketplace add
```

## 何时建议使用 ast-grep

在以下场景向用户建议 ast-grep：

| 场景 | 信号词 | 为什么用 ast-grep？ |
|----------|--------------|---------------|
| **大型重构** | "重命名所有对...的调用"、"更改 API 签名"、">50k 行" | 需要结构精度 |
| **框架迁移** | "React 17→18"、"Vue 2→3"、"升级依赖" | AST 感知的转换 |
| **模式检测** | "查找没有...的函数"、"定位未使用的..."、"识别反模式" | 结构规则 |
| **代码库分析** | "哪些组件依赖..."、"查找紧耦合的..." | 依赖图 |

**不建议用于**：
- 简单字符串搜索（函数名、导入）→ 用 Grep
- 小项目（<10k 行）→ Grep 就足够了
- 一次性搜索 → Grep 更快
- 语义搜索 → 用 Serena MCP 或 grepai

## 决策树

```
用户请求分析：
├─ "查找字符串/文本" → Grep（原生）
├─ "按含义查找" → Serena MCP 或 grepai
├─ "按结构查找" → ast-grep（插件）
└─ 混合需求 → 从 Grep 开始，必要时升级
```

## 常见模式

### 1. 没有错误处理的异步函数

**用例**：查找缺少 try/catch 的异步函数

```yaml
# ast-grep rule
rule:
  pattern: |
    async function $FUNC($$$PARAMS) {
      $$$BODY
    }
  not:
    has:
      pattern: try { $$$TRY } catch
```

**何时使用**：安全审计、生产就绪检查

### 2. 含有特定 Hook 的 React 组件

**用例**：查找所有使用 `useEffect` 但没有清理的组件

```yaml
rule:
  pattern: |
    useEffect(() => {
      $$$BODY
    })
  not:
    has:
      pattern: return () => { $$$CLEANUP }
```

**何时使用**：内存泄漏检测、React 最佳实践审计

### 3. 参数超过阈值的函数

**用例**：查找 >5 个参数的函数（复杂度坏味道）

```yaml
rule:
  pattern: function $NAME($P1, $P2, $P3, $P4, $P5, $P6, $$$REST) { $$$BODY }
```

**何时使用**：代码质量改进、重构候选

### 4. 生产代码中的 console.log

**用例**：从生产文件中移除调试日志

```yaml
rule:
  pattern: console.log($$$ARGS)
  inside:
    pattern: |
      class $CLASS {
        $$$METHODS
      }
```

**何时使用**：生产清理、发布前审计

### 5. 未使用的 React Props

**用例**：检测传递但从未使用的 props

```yaml
rule:
  pattern: |
    function $COMP({ $PROP, $$$OTHER }) {
      $$$BODY
    }
  not:
    has:
      pattern: $PROP
      inside: $$$BODY
```

**何时使用**：死代码消除、性能优化

### 6. 已弃用 API 的使用

**用例**：查找旧 API 方法的使用

```yaml
rule:
  any:
    - pattern: React.Component
    - pattern: componentWillMount
    - pattern: componentWillReceiveProps
```

**何时使用**：框架迁移、弃用清理

### 7. SQL 注入风险模式

**用例**：查找潜在 SQL 注入漏洞

```yaml
rule:
  pattern: |
    db.query($TEMPLATE_LITERAL)
  where:
    $TEMPLATE_LITERAL:
      kind: template_string
```

**何时使用**：安全审计、漏洞扫描

### 8. 缺失 TypeScript 返回类型

**用例**：强制显式返回类型

```yaml
rule:
  pattern: |
    function $NAME($$$PARAMS) {
      $$$BODY
    }
  not:
    has:
      pattern: ': $TYPE'
```

**何时使用**：TypeScript 最佳实践、类型安全改进

### 9. 大型 Switch 语句（重构候选）

**用例**：查找 >10 个 case 的 switch 语句

```yaml
rule:
  pattern: |
    switch ($EXPR) {
      $C1: $$$B1
      $C2: $$$B2
      $C3: $$$B3
      $C4: $$$B4
      $C5: $$$B5
      $C6: $$$B6
      $C7: $$$B7
      $C8: $$$B8
      $C9: $$$B9
      $C10: $$$B10
      $C11: $$$B11
    }
```

**何时使用**：复杂度降低、多态重构

### 10. 空的 Catch 块（吞掉的错误）

**用例**：查找静默失败的错误处理

```yaml
rule:
  pattern: |
    try {
      $$$TRY
    } catch ($ERR) {
      // 空的或只有注释
    }
```

**何时使用**：调试神秘故障、错误处理审计

## 设置复杂度与价值

| 代码库大小 | 值得设置？ | 替代方案 |
|---------------|-----------------|-------------|
| <10k 行 | ❌ 否 | 用 Grep |
| 10k-50k 行 | ⚠️ 也许 | 从 Grep 开始，必要时升级 |
| 50k-200k 行 | ✅ 是 | ast-grep 用于结构，Grep 用于文本 |
| >200k 行 | ✅ 肯定 | ast-grep + Serena MCP 组合 |

## 故障排查

### 未找到 ast-grep

```bash
# 验证安装
npx ast-grep --version

# 重新安装技能
npx skills add ast-grep/agent-skill --force
```

### Claude 未使用 ast-grep

**问题**：Claude 用 Grep 而非 ast-grep

**解决方案**：在请求中明确说明
- ❌ "查找异步函数"
- ✅ "使用 ast-grep 查找异步函数"

### 性能问题

**问题**：ast-grep 在大型代码库上慢

**解决方案**：
1. 缩小搜索范围：`ast-grep --path src/components/`
2. 使用文件过滤器：`ast-grep --lang tsx`
3. 缓存结果以进行迭代优化

### 模式不匹配

**问题**：ast-grep 模式不匹配预期代码

**调试步骤**：
1. 隔离测试模式：`ast-grep -p 'your-pattern' file.js`
2. 检查 AST 结构：`ast-grep --debug-query`
3. 逐步简化模式
4. 验证语言语法（JS vs TS vs JSX）

## 集成示例

### 工作流：带 ast-grep 的预提交钩子

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 检查暂存文件中的 console.log
if ast-grep -p 'console.log($$$)' $(git diff --cached --name-only); then
  echo "❌ 发现 console.log 语句"
  exit 1
fi
```

### 工作流：迁移脚本

```bash
#!/bin/bash
# 迁移 React 类组件到 hooks

# 查找所有类组件
ast-grep -p 'class $C extends React.Component' --json > components.json

# 处理每个组件
jq -r '.[] | .file' components.json | while read file; do
  echo "迁移中：$file"
  # ... 转换逻辑
done
```

### 工作流：安全审计

```bash
#!/bin/bash
# security-audit.sh

echo "=== 安全审计 ==="

# SQL 注入风险
ast-grep -p 'db.query(`${$VAR}`)' --lang ts

# XSS 风险
ast-grep -p 'innerHTML = $VAR' --lang js

# 硬编码密钥
ast-grep -p 'password: "$PASSWORD"' --lang ts
```

## Claude 提示模板

### 模板 1：大型重构

```
我需要重构 [功能]，代码库约 [大小] 行。

使用 ast-grep：
1. 查找所有 [旧模式] 的实例
2. 识别哪些文件会受影响
3. 建议转换策略
4. 创建分阶段迁移计划

从分析开始，等待我批准后再做变更。
```

### 模板 2：框架迁移

```
我们要从 [旧框架 v1] 迁移到 [新框架 v2]。

使用 ast-grep：
1. 查找所有已弃用的 API 使用
2. 映射到新 API 的等效功能
3. 估计迁移工作量（受影响的文件数）
4. 识别高风险变更

提供显示迁移顺序的依赖图。
```

### 模板 3：代码质量审计

```

用 ast-grep 对 [目录] 运行代码质量审计。

聚焦于：
- >5 个参数的函数
- 没有错误处理的异步函数
- 空的 catch 块
- 未使用的函数参数

按严重性排列问题并提供重构建议。
```

## 高级：将 ast-grep 与其他工具结合

### ast-grep + Serena MCP

```bash
# 1. ast-grep 查找结构模式
ast-grep -p 'async function $F' --json > async-funcs.json

# 2. Serena 查找符号和依赖
claude mcp call serena find_symbol --name "authenticate"

# 3. 合并见解以获取完整上下文
# ast-grep："这是一个异步函数"
# Serena："被其他 12 个函数调用"
```

### ast-grep + grepai

```bash
# 1. grepai 用于语义搜索
# "查找认证相关代码"

# 2. ast-grep 用于结构优化
# "在这些结果中，哪些是异步但没有错误处理的？"
```

## 最佳实践

1. **从简单开始**：从 Grep 开始，必要时升级到 ast-grep
2. **测试模式**：在运行整个代码库之前，在小文件上验证
3. **文档化模式**：将成功的模式保存为可复用规则
4. **明确请求**：始终明确告诉 Claude 何时使用 ast-grep
5. **组合工具**：ast-grep 用于结构，Grep 用于文本，Serena 用于符号

## 资源

- [ast-grep 文档](https://ast-grep.github.io/)
- [模式游乐场](https://ast-grep.github.io/playground.html)
- [ast-grep GitHub](https://github.com/ast-grep/ast-grep)
- [Claude 技能](https://github.com/ast-grep/claude-skill)

---

**最后更新**：2026 年 1 月
**兼容**：Claude Code 2.1.7+


