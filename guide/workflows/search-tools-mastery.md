<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "搜索工具精通：组合 rg、grepai、Serena 和 ast-grep"
description: "通过组合正确的工具掌握代码搜索，实现最高效率"
tags: [workflow, search, guide, mcp]
---

# 搜索工具精通：组合 rg、grepai、Serena 和 ast-grep

> **通过组合正确的工具掌握代码搜索，实现最高效率**

**作者**：Florian BRUNIAUX | 来自 Claude（Anthropic）的贡献
**阅读时间**：约 20 分钟
**最后更新**：2026 年 1 月

---

## 目录

1. [快速参考矩阵](#快速参考矩阵)
2. [工具对比](#工具对比)
3. [决策树](#决策树)
4. [组合工作流](#组合工作流)
5. [真实世界场景](#真实世界场景)
6. [性能优化](#性能优化)
7. [常见陷阱](#常见陷阱)

---

## 快速参考矩阵

| 我需要... | 使用此工具 | 命令示例 |
|--------------|---------------|-----------------|
| 查找精确文本 | `rg`（Grep 工具） | `rg "authenticate" --type ts` |
| 按含义查找 | `grepai` | `grepai search "user login flow"` |
| 查找函数定义 | `Serena` | `serena find_symbol --name "login"` |
| 查找结构模式 | `ast-grep` | `ast-grep "async function $F"` |
| 查看谁调用函数 | `grepai` | `grepai trace callers "login"` |
| 获取文件结构 | `Serena` | `serena get_symbols_overview` |
| 跨文件重构 | `Serena + ast-grep` | 组合工作流 |
| 探索未知代码库 | `grepai → Serena` | 发现模式 |

---

## 工具对比

### 完整功能矩阵

| 功能 | rg（ripgrep） | grepai | Serena | ast-grep |
|---------|--------------|--------|--------|----------|
| **搜索类型** | 正则/文本 | 语义（含义） | 符号感知 | AST 结构 |
| **技术** | 模式匹配 | Embeddings（Ollama） | 符号解析 | 抽象语法树 |
| **速度** | ⚡ 约 20ms | 🐢 约 500ms | ⚡ 约 100ms | 🕐 约 200ms |
| **设置** | ✅ 无（内置） | ⚠️ Ollama + 安装 | ⚠️ MCP 配置 | ⚠️ npm 安装 |
| **集成** | ✅ 原生（Grep） | ⚠️ MCP 服务器 | ⚠️ MCP 服务器 | ⚠️ 插件 |
| **隐私** | ✅ 100% 本地 | ✅ 100% 本地 | ✅ 100% 本地 | ✅ 100% 本地 |
| **需要上下文** | 无 | 无 | 项目索引 | 无 |
| **语言** | 全部（文本） | 全部 | TS/JS/Py/Rust/Go | TS/JS/Py/Rust/Go/C++ |
| **调用图** | ❌ 否 | ✅ 是 | ❌ 否 | ❌ 否 |
| **符号跟踪** | ❌ 否 | ❌ 否 | ✅ 是 | ❌ 否 |
| **会话内存** | ❌ 否 | ❌ 否 | ✅ 是 | ❌ 否 |
| **误报** | 中等 | 低 | 非常低 | 非常低 |
| **学习曲线** | 低 | 中等 | 低 | 高 |

### Token 成本对比

| 工具 | 典型查询 | 消耗 Tokens | 返回结果 |
|------|---------------|-----------------|------------------|
| **rg** | "authenticate" | 约 500 | 仅精确匹配 |
| **grepai** | "auth flow" | 约 2000 | 基于意图的匹配 |
| **Serena** | find_symbol | 约 1000 | 符号 + 上下文 |
| **ast-grep** | AST 模式 | 约 1500 | 结构匹配 |

**关键洞察**：rg 的 token 效率高出 4 倍，但比语义工具的智能程度低 10 倍。

---

## 决策树

### 级别 1：你知道什么？

```
你知道确切的文本/模式吗？
│
├─ 是 → 使用 rg（ripgrep）
│  ├─ 已知函数名：rg "createSession"
│  ├─ 已知导入：rg "import.*React"
│  └─ 已知模式：rg "async function"
│
└─ 否 → 进入级别 2
```

### 级别 2：你在找什么？

```
你的搜索意图是什么？
│
├─ "按含义/概念查找"
│  → 使用 grepai
│  └─ 示例：grepai search "payment validation logic"
│
├─ "查找函数/类定义"
│  → 使用 Serena
│  └─ 示例：serena find_symbol --name "UserController"
│
├─ "按代码结构查找"
│  → 使用 ast-grep
│  └─ 示例：async without error handling
│
└─ "理解依赖关系"
   → 使用 grepai trace
   └─ 示例：grepai trace callers "validatePayment"
```

### 级别 3：优化

```
找到太多结果了吗？
│
├─ rg → 添加 --type 过滤器或缩小路径
├─ grepai → 添加 --path 过滤器或使用 trace
├─ Serena → 按符号类型过滤（function/class）
└─ ast-grep → 向模式添加约束
```

---

## 组合工作流

### 工作流 1：探索未知代码库

**目标**：快速理解新项目

**步骤**：

```bash
# 1. 语义发现（grepai）
# 查找与认证相关的文件
grepai search "user authentication and session management"
# → 输出：auth.service.ts、session.middleware.ts、user.controller.ts

# 2. 结构概览（Serena）
# 理解每个文件的结构
serena get_symbols_overview --file auth.service.ts
# → 输出：
#   - class AuthService
#     - login(email, password)
#     - logout(sessionId)
#     - validateSession(token)

# 3. 依赖映射（grepai trace）
# 查看 login 如何被使用
grepai trace callers "login"
# → 输出：由 UserController、ApiGateway、AdminPanel 调用

# 4. 精确搜索（rg）
# 查找具体实现细节
rg "validateSession" --type ts -A 5
# → 输出：5 行上下文的完整函数
```

**结果**：4 个命令完成全面理解（vs 30+ 文件读取）

---

### 工作流 2：大规模重构

**目标**：在 50+ 文件中将 `createSession` 重命名 → `initializeUserSession`

**步骤**：

```bash
# 1. 影响分析（grepai trace）
# 了解完整范围
grepai trace callers "createSession"
# → 输出：跨 23 个文件的 47 个调用者
grepai trace callees "createSession"
# → 输出：调用 validateUser、createToken、storeSession

# 2. 结构验证（ast-grep）
# 确保一致的使用模式
ast-grep "createSession($$$ARGS)"
# → 输出：所有调用及其参数模式

# 3. 符号感知重构（Serena）
# 精确重命名
serena find_symbol --name "createSession" --include-body true
# → 获取确切定义 + 所有引用

serena replace_symbol_body \
  --name "createSession" \
  --new-name "initializeUserSession"
# → 在所有文件中重命名，保持结构

# 4. 验证（rg）
# 确认没有旧引用残留
rg "createSession" --type ts
# → 应返回 0 结果
```

**结果**：带完整依赖感知的安全重构

---

### 工作流 3：安全审计

**目标**：发现安全漏洞

**步骤**：

```bash
# 1. 语义发现（grepai）
# 查找安全敏感代码
grepai search "SQL query construction"
grepai search "user input validation"
grepai search "password handling"

# 2. 结构模式（ast-grep）
# 查找特定漏洞模式

# SQL 注入风险
ast-grep 'db.query(`${$VAR}`)'

# XSS 风险
ast-grep 'innerHTML = $VAR'

# 缺少错误处理
ast-grep -p 'async function $F($$$) { $$$BODY }' \
  --without 'try { $$$TRY } catch'

# 3. 依赖追踪（grepai）
# 查看易受攻击代码的调用位置
grepai trace callers "executeQuery"
# → 识别所有入口点

# 4. 精确验证（rg）
# 确认发现
rg "innerHTML\s*=" --type ts
rg "password" --type ts | rg -v "hashed"
```

**结果**：几分钟内完成全面的安全审计

---

## 真实世界基准

### grepai vs grep（2026 年 1 月）

**背景**：在 Excalidraw（155k 行 TypeScript）上的基准测试
**作者**：YoanDev（grepai 维护者——潜在偏差）
**方法论**：5 个相同的代码发现问题的比较

| 指标 | grep | grepai | 差异 |
|----------|------|--------|------------|
| 工具调用 | 139 | 62 | **-55%** |
| 输入 tokens | 51k | 1.3k | **-97%** |

**要点**：语义搜索通过在第一次尝试时识别相关文件来急剧减少 tokens，避免迭代探索。

**局限**：
- 由工具维护者进行基准测试
- 单项目验证（仅 TypeScript）
- 截至目前无独立验证

**来源**：[yoandev.co/grepai-benchmark](https://yoandev.co/grepai-benchmark)

> **注意**：此基准反映 2026 年 1 月的状态。随着 Claude Code 和 grepai 的更新，性能可能会演变。

---

### 工作流 4：框架迁移

**目标**：将 React 类组件 → hooks 迁移

**步骤**：

```bash
# 1. 清单（ast-grep）
# 查找所有类组件
ast-grep 'class $C extends React.Component'
# → 输出：34 个要迁移的组件

# 2. 依赖分析（grepai）
# 理解组件关系
for component in $(ast-grep 'class $C extends' --json | jq -r '.[].name'); do
  grepai trace callers "$component"
done
# → 构建迁移顺序（先叶子组件）

# 3. 模式检测（ast-grep）
# 识别使用的生命周期方法
ast-grep 'componentDidMount() { $$$BODY }'
ast-grep 'componentWillReceiveProps($$$) { $$$BODY }'
# → 映射到等效的 hooks

# 4. 增量迁移（Serena + ast-grep）
# 一次迁移一个组件
serena find_symbol --name "UserProfile" --include-body true
# → 获取完整组件代码

# 使用 ast-grep 转换
ast-grep --rewrite \
  --from 'class $C extends React.Component' \
  --to 'const $C = () => { }'

# 5. 验证（rg + grepai）
# 确保迁移成功
rg "React.Component" --type tsx  # 应该减少
grepai search "component lifecycle methods"  # 查找任何遗漏
```

**结果**：最小破坏性的系统化迁移

---

### 工作流 5：性能优化

**目标**：识别和修复性能瓶颈

**步骤**：

```bash
# 1. 热点发现（grepai）
# 查找性能关键代码
grepai search "heavy computation or loops"
grepai search "database queries in loops"

# 2. 模式检测（ast-grep）
# 查找 N+1 查询模式
ast-grep 'for ($$$) { await db.query($$$) }'

# 查找缺少的记忆化
ast-grep 'useMemo' --invert-match \
  --in 'const $VAR = $$$'

# 3. 调用图分析（grepai trace）
# 查找热路径
grepai trace graph "renderUserList" --depth 3
# → 可视化依赖树

# 4. 符号跟踪（Serena）
# 跟踪函数变化
serena write_memory "perf_baseline" \
  "renderUserList: 450ms avg"

# 优化后
serena write_memory "perf_optimized" \
  "renderUserList: 45ms avg (10x improvement)"

# 5. 验证（rg）
# 确认优化已应用
rg "useMemo|useCallback" --type tsx
```

**结果**：数据驱动的性能改进

---

## 真实世界场景

### 场景 1："我不知道我在找什么"

**问题**：新项目，无文档，需要添加功能

**解决方案**：语义优先发现

```bash
# 从含义开始广泛搜索
grepai search "user profile management"
# → 发现相关文件

# 然后用结构缩小范围
serena get_symbols_overview --file user-profile.service.ts
# → 理解可用函数

# 最后，精确搜索细节
rg "updateProfile" --type ts -C 3
```

---

### 场景 2："这个函数被到处调用"

**问题**：需要修改一个函数但担心破坏东西

**解决方案**：首先进行依赖映射

```bash
# 1. 查看所有调用者
grepai trace callers "calculateTotal"
# → 发现 47 个调用者

# 2. 分析调用者上下文
for file in $(grepai trace callers "calculateTotal" --json | jq -r '.[].file'); do
  serena get_symbols_overview --file "$file"
done

# 3. 识别安全 vs 有风险的调用点
ast-grep 'calculateTotal($ARGS)' --json
# → 按参数模式分组

# 4. 有信心地进行更改
# 现在你知道所有影响点
```

---

### 场景 3："找到所有做 X 的代码"

**问题**：需要在代码库中应用一致的模式

**解决方案**：组合语义 + 结构

```bash
# 示例：查找所有错误处理代码

# 1. 语义发现
grepai search "error handling and exception management"

# 2. 结构模式
ast-grep 'try { $$$TRY } catch ($ERR) { $$$CATCH }'
ast-grep 'throw new Error($MSG)'

# 3. 验证一致性
rg "catch\s*\(" --type ts | wc -l
# 与 ast-grep 计数比较以发现异常
```

---

### 场景 4："我需要理解这个模块"

**问题**：复杂模块，职责不清晰

**解决方案**：多工具分析

```bash
# 1. 获取符号概览（Serena）
serena get_symbols_overview --file payment.module.ts
# → 查看所有导出、类、函数

# 2. 理解依赖（grepai）
grepai trace callees "PaymentModule"
# → 这个模块使用什么？

grepai trace callers "PaymentModule"
# → 谁使用这个模块？

# 3. 查找实现模式（ast-grep）
ast-grep 'export class $C' --file payment.module.ts
ast-grep 'async $METHOD($$$)' --file payment.module.ts

# 4. 读取具体实现（rg）
rg "processPayment" --type ts -A 20
```

---

## 性能优化

### 选择最快的工具

**一般规则**：

1. **知道确切文本** → 始终首先使用 rg
2. **不知道确切文本** → 使用 grepai，然后用 rg 验证
3. **重构** → 使用 Serena 确保符号安全
4. **大型迁移** → 使用 ast-grep 确保结构精确

### 性能基准

**测试**：在 50 万行代码库中查找认证代码

| 策略 | 时间 | 结果质量 |
|----------|------|-----------------|
| 仅 rg "auth" | 0.2s | 5000+ 误报 |
| 仅 grepai "auth" | 2.5s | 50 个相关结果 |
| grepai → rg（组合） | 2.7s | 50 个相关，已验证 |
| 仅 Serena 符号 | 1.5s | 12 个 auth 函数 |
| ast-grep 模式 | 3.0s | 8 个 auth 流 |

**赢家**：对于已知函数名，Serena 符号（最快 + 高质量）

### 并行化策略

**对于大型代码库（>100k 行）**：

```bash
# 并行运行搜索

# 终端 1：语义发现
grepai search "authentication flow" > /tmp/grepai-results.json &

# 终端 2：符号索引
serena get_symbols_overview --file src/**/*.ts > /tmp/symbols.json &

# 终端 3：模式检测
ast-grep 'async function $F' --json > /tmp/ast-results.json &

# 等待所有完成，然后合并结果
wait
jq -s '.[0] + .[1] + .[2]' \
  /tmp/grepai-results.json \
  /tmp/symbols.json \
  /tmp/ast-results.json
```

---

## 常见陷阱

### 陷阱 1：对精确匹配使用语义搜索

❌ **错误**：
```bash
grepai search "createSession"  # 慢，大材小用
```

✅ **正确**：
```bash
rg "createSession" --type ts  # 快，精确
```

**规则**：如果你知道确切文本，永远不要使用语义搜索。

---

### 陷阱 2：使用 rg 进行概念搜索

❌ **错误**：
```bash
rg "auth.*login.*session" --type ts  # 会遗漏变体
```

✅ **正确**：
```bash
grepai search "authentication and session management"
```

**规则**：正则不理解含义，使用语义工具。

---

### 陷阱 3：重构前忽略调用图

❌ **错误**：
```bash
# 不检查调用者直接重构
rg "oldFunction" --type ts | sed 's/oldFunction/newFunction/g'
```

✅ **正确**：
```bash
# 首先检查影响
grepai trace callers "oldFunction"
# 看到跨 23 个文件的 47 个调用者
# 然后规划重构策略
```

**规则**：修改共享代码前始终追踪依赖。

---

### 陷阱 4：不组合工具

❌ **错误**：
```bash
# 对复杂任务只使用一个工具
ast-grep 'async function $F' --json | jq '.[].file' | xargs -I {} vim {}
# 不理解上下文的情况下盲目编辑
```

✅ **正确**：
```bash
# 组合以获得全面理解
ast-grep 'async function $F' --json > /tmp/async.json
for file in $(jq -r '.[].file' /tmp/async.json); do
  serena get_symbols_overview --file "$file"  # 上下文
  grepai trace callers "$(jq -r '.[].name' /tmp/async.json)"  # 使用情况
done
```

**规则**：复杂任务需要多个视角。

---

### 陷阱 5：过度工程化简单搜索

❌ **错误**：
```bash
# 只是为了找 TODO 注释而设置 grepai + Ollama
grepai search "TODO comments in the code"
```

✅ **正确**：
```bash
rg "TODO" --type ts
```

**规则**：使用最简单的工具完成任务。

---

## 工具选择速查表

### 快速决策矩阵

| 你的情况 | 使用这个 | 不要用这个 |
|----------------|----------|----------|
| "找函数 `login`" | rg "login" | grepai search "login" |
| "找登录相关代码" | grepai "login flow" | rg "login.*" |
| "安全重命名函数" | Serena find_symbol | rg + sed |
| "谁调用这个函数？" | grepai trace callers | rg + grep |
| "获取文件结构" | Serena overview | rg "class\|function" |
| "找没有 try/catch 的 async" | ast-grep | rg "async.*{" |
| "迁移 React 类" | ast-grep | rg + 手动 |
| "找 TODO" | rg "TODO" | 任何其他工具 |

---

## 设置优先级

**推荐的设置顺序**：

1. **开始**：rg（已经内置在 Grep 工具中）✅
2. **下一步**：Serena MCP（符号感知、会话内存）
3. **然后**：grepai（语义搜索 + 调用图）
4. **最后**：ast-grep（结构模式、大型重构）

**理由**：90% 的搜索使用 rg + Serena 即可。為语义需求添加 grepai。只有在進行大型重構/遷移時才添加 ast-grep。

---

## 总结：四工具交响曲

```
┌─────────────────────────────────────────────────────────┐
│                   搜索工具精通                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  rg (ripgrep)     →  快速、精确文本匹配                 │
│  ├─ 使用：90% 的搜索                                    │
│  └─ 速度：⚡ 约 20ms                                     │
│                                                         │
│  grepai           →  语义 + 调用图                      │
│  ├─ 使用：概念发现、依赖追踪                             │
│  └─ 速度：🐢 约 500ms（但能找到 rg 找不到的）           │
│                                                         │
│  Serena           →  符号感知 + 会话内存                 │
│  ├─ 使用：符号安全重构、会话感知搜索                     │
│  └─ 速度：⚡ 约 100ms                                    │
│                                                         │
│  ast-grep         →  AST 结构 + 模式重写                │
│  ├─ 使用：结构搜索、大型代码迁移                         │
│  └─ 速度：🕐 约 200ms                                    │
│                                                         │
│  组合策略：                                             │
│  rg → Serena → grepai → ast-grep                        │
│  快速精确 → 符号感知 → 语义 → 结构精确                  │
└─────────────────────────────────────────────────────────┘
```

### 关键要点

1. **知道你想要什么**：确切的文本 → rg，未知概念 → grepai，结构 → ast-grep
2. **组合而非孤岛**：每个工具擅长不同事物，组合使用效果最佳
3. **追踪依赖**：在修改共享代码之前使用 `grepai trace`
4. **选择正确工具**：最简单够用的那个
5. **会话内存**：Serena 跨会话记住符号——为大型重构利用这一点

---

**最后更新**：2026 年 1 月