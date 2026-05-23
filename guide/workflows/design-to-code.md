---
title: "设计到代码工作流（Figma MCP）"
description: "使用 Figma MCP Server 实现自动化设计系统实现，达到 1:1 设计代码对等"
tags: [workflow, mcp, integration]
---

# 设计到代码工作流（Figma MCP）

> **可信度**：第 2 层 — 基于记录的生产案例研究（Parallel HQ、builder.io）、MCP 服务器规范和社区工作流。

使用 Figma MCP Server 实现自动化设计系统实现，使产品设计师能够将生产就绪的规范交给 Claude Code，后者实现的组件保持 1:1 的设计代码对等。

---

## 目录

1. [TL;DR](#tldr)
2. [记录的影响](#记录的影响)
3. [架构概览](#架构概览)
4. [三层 Token 层级](#三层-token-层级)
5. [前置要求](#前置要求)
6. [核心工作流](#核心工作流)
7. [Code Connect 设置](#code-connect-设置)
8. [示例提示](#示例提示)
9. [团队采用模式](#团队采用模式)
10. [反模式](#反模式)
11. [实施路线图](#实施路线图)
12. [资源](#资源)

---

## TL;DR

```
设计师（Figma Make）→ 导出（Figma Design）→ Claude（Figma MCP）→ 生产代码

关键洞察：设计系统 = 事实来源
Claude 直接从 Figma 读取 token/组件
实现自动保持设计对等
```

---

## 记录的影响

基于 2026 年 1 月的生产案例研究：

| 指标 | 改进 | 来源 |
|--------|-------------|----------|
| 设计不一致 | 减少 62% | Parallel HQ 研究 |
| 工作流效率 | 提高 78% | builder.io 案例研究 |
| 节省工程时间 | 75 天（6 个月）| Parallel HQ 生产数据 |
| 上市时间 | 减少 56% | 多组织综合 |
| 设计技术债务 | 减少 82% | 实施后审计 |

**典型工作流时间**：
- 单帧 → 生产组件：2-3 分钟
- 设计系统偏移审计：3 周 → 3 分钟
- Token 更新传播：手动数小时 → 自动化秒级

*来源：builder.io/blog/claude-code-figma-mcp-server, parallelhq.com/blog/automating-design-systems-with-ai, composio.dev/blog/how-to-use-figma-mcp-with-claude-code*

---

## 架构概览

### 完整堆栈

```
[Figma 设计文件]
    ↓（变量和样式）
[Tokens Studio 插件]（可选但推荐）
    ↓（JSON 导出）
[GitHub 仓库]
    ↓（CI/CD）
[Style Dictionary]
    ↓（转换）
[CSS 自定义属性 / Tailwind 配置]
    ↓（被消耗）
[组件库]
    ↑（通过读取）
[Claude Code + Figma MCP]
```

### MCP 集成点

Claude Code 通过 Figma MCP Server 访问 Figma：

```
Claude Code
    ↓（使用）
Figma MCP Server（mcp-server-figma）
    ↓（通过以下方式进行身份验证）
Figma 个人访问令牌
    ↓（读取）
Figma 文件（Dev Mode 数据）
```

**Claude 可以访问的内容**：
- 文件结构和帧
- 颜色/文本/效果样式
- 组件属性
- 变量（token）
- Dev Mode 注释
- Code Connect 代码片段（如果已配置）

**Claude 无法访问的内容**：
- 没有令牌权限的私人文件
- 编辑能力（只读）
- 实时协作数据
- 版本历史（仅当前状态）

---

## 三层 Token 层级

现代设计系统使用层级 token 结构。Claude Code 在消费 Figma 数据时理解此层级。

| 层级 | 定义 | Figma 实现 | 代码输出 |
|------|------------|----------------------|-------------|
| **基础** | 原始值 | Figma 变量（例如 `blue-600: #0066CC`，`spacing-2: 8px`） | CSS 自定义属性（`--blue-600`，`--spacing-2`） |
| **复合** | 组合原始值 | 引用变量的组件填充 | Tailwind 配置或 CSS 类 |
| **语义** | 上下文含义 | 上下文变量别名（例如 `color-interactive-primary` → `blue-600`） | 组件 props 或主题 token |

### 层级示例

```
Base（基础）：
  --color-blue-600: #0066CC
  --spacing-2: 8px
  --radius-md: 4px

Composite（复合）：
  --button-padding: var(--spacing-2) var(--spacing-4)
  --button-border-radius: var(--radius-md)

Semantic（语义）：
  --interactive-primary: var(--color-blue-600)
  --interactive-primary-hover: var(--color-blue-700)
```

**Claude Code 行为**：当给出一个 Figma 组件时，Claude：
1. 提取引用的变量（基础层级）
2. 识别复合模式（间距、大小）
3. 应用来自 token 约定的语义命名
4. 生成与此层级匹配的代码

---

## 前置要求

### 设计师前置要求

| 要求 | 详情 |
|-------------|---------|
| **Figma 许可证** | Dev Mode 席位（启用变量检查、代码片段） |
| **组织化变量** | 使用 Figma 变量或 Tokens Studio 插件进行 token 管理 |
| **组件结构** | 自动布局、命名层、一致的命名约定 |
| **帧命名** | 描述性帧名称（Claude 用这些作为组件名称） |

### 开发者前置要求

| 要求 | 详情 |
|-------------|---------|
| **Claude Code** | 版本 1.5.0+（MCP 支持）|
| **Figma MCP Server** | `npm install -g @modelcontextprotocol/server-figma` |
| **个人访问令牌** | 从 Figma 账户设置 → 生成令牌 |
| **MCP 配置** | 在 Claude Code 设置中配置令牌 |

### MCP 配置

添加到 Claude Code MCP 设置（`.claude/mcp.json` 或设置 UI）：

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

**安全注意**：生产环境使用环境变量：
```json
{
  "env": {
    "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_TOKEN}"
  }
}
```

然后在 shell 中导出：`export FIGMA_TOKEN="figd_..."`

---

## 核心工作流

### 工作流 A：单帧 → 生产组件

**时间**：每个组件 2-3 分钟

**步骤**：

1. **设计师**：在 Figma 中使用正确变量/样式创建组件
2. **设计师**：与开发/Claude 分享 Figma 文件 URL
3. **开发者**：提示 Claude Code：

```
从 Figma 文件读取 "Button/Primary" 组件：
https://www.figma.com/design/FILE_KEY

实现为 React 组件，使用 TypeScript。
使用 Tailwind 样式，将 Figma 变量映射到我们的设计 token。
确保响应行为与 Figma 的自动布局约束匹配。
```

4. **Claude**：
   - 通过 Figma MCP 获取组件
   - 提取样式、尺寸、间距
   - 将变量映射到代码 token
   - 生成与 Figma 变体匹配的 props 组件

5. **验证**：`npm run dev` → 与 Figma 进行视觉对比

**示例输出**：
```tsx
// components/Button/Primary.tsx
interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({ size = 'md', disabled, children }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        'bg-interactive-primary text-white',
        'hover:bg-interactive-primary-hover',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        }
      )}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

---

### 工作流 B：设计系统偏移审计

**时间**：3 周手动审查 → 3 分钟自动化

**问题**：随着时间推移，代码偏离设计系统（魔术数字、硬编码颜色、不一致的间距）。

**解决方案**：Claude 根据 Figma 事实来源审计代码库。

**提示**：
```
审计 src/components 的设计系统合规性。
对比我们的 Figma 设计系统：
https://www.figma.com/design/FILE_KEY

报告：
1. 未使用设计 token 的硬编码颜色
2. 魔术数字间距值
3. 与 Figma 结构不匹配的组件
4. 缺少的响应模式

然后用 token 替换建议修复。
```

**Claude 输出**：
```markdown
## 设计系统审计结果

### 发现的问题（23 个总计）

#### 硬编码颜色（8 例）
- `src/components/Card.tsx:45` → `#0066CC` 应该是 `var(--interactive-primary)`
- `src/components/Header.tsx:12` → `#F3F4F6` 应该是 `var(--surface-secondary)`
...

#### 魔术数字（11 例）
- `src/components/Modal.tsx:23` → `padding: 16px 24px` 应该是 `var(--spacing-4) var(--spacing-6)`
...

#### 结构不匹配（4 例）
- `src/components/Button.tsx` → 缺少 Figma 中存在的 `icon-left` 变体
...
```

---

### 工作流 C：Token 自动化管道

**目标**：Figma 变量更改自动传播到代码。

**架构**：

```
Figma 变量
    ↓（Tokens Studio 导出或 Figma API）
GitHub 仓库（tokens.json）
    ↓（GitHub Actions CI/CD）
Style Dictionary 转换
    ↓（生成）
CSS / Tailwind / 平台特定 token
    ↓（提交和部署）
生产
```

**设置**（一次性）：

1. **Tokens Studio 插件**：连接到 GitHub 仓库
2. **Style Dictionary 配置**：定义转换规则
3. **GitHub Actions**：token 更新时自动运行
4. **Claude 角色**：审查和验证生成的 token

**开发者提示**（CI 运行后）：
```
审查提交 abc1234 的 token 更新。
检查是否有组件需要更新以使用新的 token。
如果存在破坏性更改，生成迁移指南。
```

**Claude 输出**：
```markdown
## Token 更新审查（v2.3.0 → v2.4.0）

### 更改
- 新增：`--spacing-7`、`--spacing-8`（设计要求）
- 更改：`--interactive-secondary` 色相偏移 5°（品牌刷新）
- 弃用：`--legacy-blue`（Q3 前移除）

### 影响分析
- 12 个组件引用 `--interactive-secondary` → 通过 token 引用自动更新
- 3 个组件使用弃用的 `--legacy-blue` → 需要迁移

### 需要迁移
1. `src/components/LegacyButton.tsx:34` → 将 `--legacy-blue` 替换为 `--interactive-primary`
2. `src/components/OldCard.tsx:67` → 替换为新 token
3. `src/utils/theme.ts:12` → 更新主题导出

### 迁移脚本
[Claude 生成 codemod 或查找/替换脚本]
```

---

### 工作流 D：视觉迭代循环（Figma + Playwright）

**目标**：针对 Figma 设计进行自动化视觉回归测试。

**MCP 堆栈**：Figma MCP + Playwright MCP

**设置**：
```
Claude Code 访问：
- Figma（设计事实来源）
- Playwright（自动化浏览器测试）
```

**提示**：
```
截取我们 Button 组件在所有变体下的截图。
对比 Figma 帧：
https://www.figma.com/design/FILE_KEY → "Button Tests" 页面

报告任何视觉差异（颜色、间距、版式）。
```

**工作流**：
1. Claude 读取 Figma 帧（预期状态）
2. Claude 使用 Playwright 截取实时组件截图（实际状态）
3. Claude 比较（像素差异或视觉检查）
4. 报告差异及修复建议

**示例输出**：
```markdown
## 视觉回归报告

### ✅ 匹配（5/7）
- Button/Primary/Default
- Button/Primary/Hover
- Button/Secondary/Default
...

### ❌ 不匹配（2/7）

#### Button/Primary/Disabled
- **问题**：代码中文本透明度 0.4，Figma 中 0.5
- **修复**：更新 `disabled:opacity-50` → `disabled:opacity-40`
- **文件**：`src/components/Button.tsx:23`

#### Button/Large
- **问题**：代码中 padding 12px，Figma 中 16px
- **修复**：更新 `py-3` → `py-4`（16px）
- **文件**：`src/components/Button.tsx:18`
```

---

## Code Connect 设置

**Code Connect** 是 Figma 的无代码工具，用于将设计组件链接到代码片段。这增强了 Claude 生成正确代码的能力。

### 它做什么

- 设计师在 Figma Dev Mode 中用代码示例注释组件
- Claude 通过 MCP 读取这些注释
- 生成的代码自动匹配团队约定

### 设置（面向设计师）

1. 在 Figma Dev Mode → 选择组件 → Code Connect 面板
2. 添加显示组件使用方式的代码片段：

```tsx
// Figma 中的示例 Code Connect 注释
<Button variant="primary" size="lg">
  Click me
</Button>
```

3. Claude 在被要求实现时看到这些，使用团队的确切模式

### 优势

| 没有 Code Connect | 有 Code Connect |
|---------------------|-------------------|
| Claude 生成通用代码 | Claude 使用团队约定 |
| Props 命名不一致 | Props 与 Figma 变体完全匹配 |
| 需要手动修正 | 首次通过即可投入生产 |

**参考**：在 parallelhq.com/blog 阅读更多（Code Connect UI 文章）

---

## 替代方案：Pencil（IDE 原生画布）

**概述**：[Pencil](https://pencil.dev) 将无限设计画布直接嵌入 Claude Code/Cursor/VSCode，消除了外部工具切换，并实现了设计即代码工作流。

### 架构

**核心创新**：与 Figma（云端）或 Excalidraw（独立）不同，Pencil 将设计画布直接嵌入 Claude 和代码所在的 IDE 中。

```
传统工作流：
Figma（设计）→ 导出 → Claude Code → 实现 → 手动同步

Pencil 工作流：
IDE 画布（设计 + AI 智能体 + 代码）→ Git 提交 → 持续对齐
```

**关键特性**：
- **WebGL 画布**：无限、高性能、完全可编辑
- **AI 多智能体**：并行智能体协作处理设计
- **Git 原生**：`.pen` 文件（JSON 格式）与代码一起版本控制
- **MCP 双向**：完全读写访问（不像 Figma MCP 那样仅读取）
- **Figma 导入**：直接从 Figma 复制粘贴，保留向量和样式

### Pencil vs. Figma MCP

| 方面 | Pencil | Figma MCP |
|--------|--------|-----------|
| **位置** | IDE 原生（Cursor/VSCode/Claude Code）| 外部云 |
| **格式** | `.pen` JSON（开放）| 专有二进制 |
| **版本控制** | Git 原生（分支/合并/历史）| Figma 云版本 |
| **AI 智能体** | 多玩家并行 | 通过 MCP 单线程 |
| **协作** | 代码优先（开发者 + 设计师）| 设计优先（设计师 + 开发者）|
| **MCP 访问** | 双向（读+写）| 只读 |
| **工作流** | 设计 → 提交 → 代码在同一环境 | 设计 → 导出 → 交接 → 代码 |
| **最适合** | 工程师-设计师、代码为中心的团队 | 传统设计-开发分离 |
| **成熟度** | 新兴（2026 年 1 月推出）| 成熟（2024+）|
| **定价** | 目前免费，未来待定 | Freemium（有免费层）|

### 何时使用 Pencil

✅ **适合**：
- 团队使用 Cursor 或 VSCode + Claude Code 作为主要环境
- 熟悉终端/IDE 工作流的工程师-设计师
- 需要紧密设计-代码对齐的项目（设计即代码范式）
- 希望对设计版本进行 git 原生控制（分支保护、回滚等）
- 希望利用并行 AI 智能体进行设计自动化

⚠️ **仔细考虑**：
- 传统设计团队（非技术）→ Figma 可能更好
- 需要企业 SLA/支持 → Pencil 仍在成熟
- 复杂设计系统有 50+ 组件 → Figma 生态系统更成熟
- 团队不使用 Cursor/VSCode → 兼容性有限

### 设置

1. **安装 Pencil 扩展**：
   - 访问 [pencil.dev](https://pencil.dev)
   - 按照 Cursor/VSCode/Claude Code 的安装说明操作
   - 创建账户（目前免费）

2. **创建第一个画布**：
   ```bash
   # 打开 IDE，启动 Pencil 扩展
   # 在你的仓库中创建新的 .pen 文件
   # 在无限画布上设计
   ```

3. **Git 工作流**：
   ```bash
   git add design/homepage.pen
   git commit -m "feat(design): add homepage hero section"
   git push
   ```

4. **Claude 集成**：
   - Claude 可以通过 MCP 读取 .pen 文件
   - 提示："从 design/components.pen 实现 Button 组件"
   - Claude 提取设计规范并生成代码

### 示例提示

```
从 design/homepage.pen 读取 "Hero Section"。

实现为 React 组件，具有：
- 与画布断点匹配的响应行为
- 设计中的动画（淡入、滑入）
- 完全按照画布中指定的副本
- 使用 Tailwind 样式

确保与设计规范像素完美匹配。
```

### 创始人和支持

**Tom Krcha**（CEO，Pencil）：
- Adobe XD 联合创始人（2014-2018），Adobe 10 年
- 之前退出：Alter Avatars（被 Google 收购）、Around（被 Miro 收购）
- 14+ 年开发经验

**资金**：a16z Speedrun（~$1M）+ KAYA VC

**吸引力**：发布时 100 万+ 浏览量，数千人注册，包括 Microsoft、Shopify、Uber 高管。

### 成熟度注意

**⚠️ 状态**：2026 年 1 月推出（非常新）。强劲的早期信号，但文档和生态系统仍在成熟中。

**建议**：
- **生产项目**：首先与 1-2 个非关键功能进行试点
- **新项目**：对使用 Cursor/Claude Code 的团队来说安全采用
- **传统工作流**：在 Pencil 成熟（3-6 个月）前坚持使用 Figma MCP

**监控**：预计 2026 年 Q2 的定价公告、公开 GitHub 仓库、成熟文档。

---

## 示例提示

### 组件实现
```
从我们的 Figma 设计系统实现 "Card/Product" 组件：
[Figma URL]

要求：
- 使用 tailwind.config.ts 中我们现有的设计 token
- 包含与 Figma 交互匹配的悬停状态
- 实现所有变体（default、featured、compact）
- 为所有 props 添加 TypeScript 类型
```

### 设计系统扩展
```
我们的设计团队在 Figma 中添加了新 "Badge" 组件：
[Figma URL → Badge 帧]

生成：
1. 包含所有变体的 React 组件
2. Storybook 故事
3. props 组合的单元测试
4. 更新设计系统文档
```

### Token 验证
```
将 Tailwind 配置中的颜色 token 与
Figma 变量对比：[Figma URL]

报告任何不匹配并生成更新脚本。
```

### 响应实现
```
使用与 Figma 完全相同的响应行为实现 "Hero" 部分：
[Figma URL → Hero/Responsive 帧]

Figma 配置了 3 个断点。精确匹配这些。
```

### 无障碍审计
```
根据 Figma 规范审查 "Modal" 组件实现：
[Figma URL]

检查：
- 焦点管理与 Figma 的交互流匹配
- 颜色对比符合 WCAG AA（Figma 有对比度检查器）
- 键盘导航（Figma 注释指定 tab 顺序）
```

### 设计 QA 交接前
```
审查 "Checkout Flow" 帧的实施准备情况：
[Figma URL → Checkout Flow 页面]

检查：
- 所有交互状态已定义（悬停、焦点、禁用、错误）
- 一致使用变量（无魔术值）
- 自动布局约束可实现
- 生产代码还缺少什么？
```

### 多组件原子实现
```
按顺序实现原子设计系统组件：

1. 原子：[Figma URL → Atoms 页面]
   - Button、Input、Label、Badge

2. 分子：[Figma URL → Molecules 页面]
   - FormField（Label + Input + Error）
   - SearchBar（Input + Button）

3. 有机体：[Figma URL → Organisms 页面]
   - LoginForm（使用分子）

确保每个层级只从较低层级导入。
```

---

## 团队采用模式

### 面向产品设计师

**新工作流**：
1. 使用正确的变量结构在 Figma 中设计
2. 使用 Figma Make 进行快速原型设计
3. 导出到启用了 Dev Mode 的 Figma Design
4. 与开发团队分享文件 URL + 具体帧
5. Claude 消费设计 → 生成实现
6. 设计师通过视觉对比（而非阅读代码）审查代码输出

**关键洞察**：设计师不需要学习代码。他们通过与 Figma 的视觉对比来审查实现。

### 面向开发者

**新工作流**：
1. 从设计师接收 Figma URL
2. 提示 Claude 从 Figma 事实来源实现
3. 审查生成的代码架构
4. 运行视觉对比（Playwright 或手动）
5. 提交生产就绪组件

**节省时间**：跳过手动像素完美实现。专注于逻辑，而非布局匹配。

### 面向产品经理

**新能力**：基于 Figma 帧请求设计实施估计。

**PM 提示**：
```
审查 "Dashboard Redesign" Figma 文件：
[Figma URL]

估计实施复杂性：
- 需要多少新组件？
- 哪些现有组件可以重用？
- 有技术障碍吗？

提供开发实施的时间表。
```

Claude 输出：
```markdown
## 实施分析

### 范围
- 共 12 帧
- 4 个新组件（DataTable、MetricCard、FilterPanel、DateRangePicker）
- 8 个现有组件重用

### 复杂性评估
- **低**：MetricCard（类似于现有 Card，1-2h）
- **中**：FilterPanel（多选逻辑，4-6h）
- **高**：DataTable（排序、分页、虚拟化，2-3 天）
- **高**：DateRangePicker（第三方库集成，1-2 天）

### 技术考虑
- DataTable 需要后端 API 用于服务器端分页
- DateRangePicker：评估 date-fns vs dayjs vs native
- FilterPanel 状态管理（本地 vs 全局）

### 估计时间表
- 开发：5-7 天
- 代码审查 + QA：2 天
- 总计：1.5-2 周
```

---

## 反模式

| ❌ 反模式 | 为什么失败 | ✅ 正确方法 |
|----------------|-------------|-------------------|
| **手动设计转录** | 易出错、耗时、偏移不可避免 | 让 Claude 通过 MCP 直接读取 Figma |
| **截图作为规范** | 无 token 数据、无交互性、模糊 | 分享 Figma URL，让 Claude 访问结构化数据 |
| **硬编码值** | 设计系统更新时破坏 | 使用 Figma 变量的设计 token |
| **设计师编码** | 设计师技能的低效使用 | 设计师设计 → Claude 编码 → 开发审查 |
| **开发者猜测间距** | 与设计系统不一致 | Claude 从 Figma 提取精确值 |
| **没有 Code Connect 注释** | 通用代码输出 | 注释一次 → Claude 使用团队约定 |
| **跳过视觉对比** | 实现偏移 | 始终根据 Figma 事实来源验证 |
| **Token 命名不匹配** | Figma 变量 ≠ 代码 token | 建立命名约定，使用 Style Dictionary |
| **缺少响应规范** | 开发者猜测断点 | Figma 有响应帧 → Claude 读取精确规范 |
| **单层 token** | 不灵活，难以主题化 | 使用 3 层层级（基础/复合/语义）|

---

## 实施路线图

### 阶段 1：基础（第 1-2 周）

**目标**：基本 Figma → Claude → 代码管道

- [ ] 安装 Figma MCP Server
- [ ] 配置个人访问令牌
- [ ] 测试连接：Claude 读取公共 Figma 文件
- [ ] 在项目 CLAUDE.md 中创建设计系统约定
- [ ] 实现 3-5 个简单组件（Button、Input、Badge）
- [ ] 建立视觉 QA 流程（手动对比）

**成功标准**：
- Claude 从 Figma URL 生成组件
- 输出在视觉上匹配设计
- 开发团队理解工作流

---

### 阶段 2：扩展（第 3-4 周）

**目标**：完整设计系统实现 + 自动化

- [ ] 从 Figma 库实现 20+ 组件
- [ ] 设置 token 自动化（Tokens Studio + Style Dictionary）
- [ ] 创建组件测试套件（Storybook + 视觉回归）
- [ ] 培训设计师变量卫生
- [ ] 在 CLAUDE.md 中记录团队约定
- [ ] 运行首次设计系统偏移审计

**成功标准**：
- 80%+ 的 UI 组件自动生成
- Token 更新自动传播
- 设计师对交接流程有信心

---

### 阶段 3：编排（第 5 周+）

**目标**：多 MCP 工作流 + 持续同步

- [ ] 集成 Playwright MCP 进行自动化视觉测试
- [ ] 设置设计-代码对等检查的 CI/CD
- [ ] 创建 Figma → GitHub → 生产管道
- [ ] 实施设计系统治理（linting、审计）
- [ ] 使非开发人员能够触发 Claude 实现（工单、Slack）
- [ ] 衡量指标（TTM、不一致率、节省的开发时间）

**成功标准**：
- 设计更新 → 生产 <1 天
- 零手动设计转录
- 可衡量的团队速度增加

---

## 资源

### 官方文档

- **Figma MCP Server**：[github.com/modelcontextprotocol/servers/tree/main/src/figma](https://github.com/modelcontextprotocol/servers/tree/main/src/figma)（GitHub）
- **Figma 开发者文档**：[figma.com/developers](https://www.figma.com/developers)
- **Style Dictionary**：[amzn.github.io/style-dictionary](https://amzn.github.io/style-dictionary/)
- **Tokens Studio 插件**：[tokens.studio](https://tokens.studio/)

### 案例研究和教程

- **builder.io**："Claude Code + Figma MCP Server: AI Design-to-Code Workflow"（2026 年 1 月）
  - [builder.io/blog/claude-code-figma-mcp-server](https://www.builder.io/blog/claude-code-figma-mcp-server)
  - 生产指标、工作流示例

- **Vladimir Siedykh**："Multi-MCP Orchestration with Claude Code"
  - [vladimirsiedykh.com/blog/claude-code-mcp-workflow](https://vladimirsiedykh.com/)
  - Figma + Playwright + Linear 集成

- **Parallel HQ**："Automating Design Systems with AI"
  - [parallelhq.com/blog/automating-design-systems-with-ai](https://parallelhq.com/)
  - 节省 75 天，Code Connect UI 指南

- **Composio**："How to Use Figma MCP with Claude Code"
  - [composio.dev/blog/how-to-use-figma-mcp-with-claude-code](https://composio.dev/)
  - Token 层级模式、设置指南

### 社区资源

- **Figma 社区**：搜索"Design System Tokens"获取起始模板
- **MCP 注册表**：[mcp.run](https://mcp.run/) → Figma 服务器示例
- **Discord**：Anthropic Discord → #mcp-servers 频道

### 相关工作流

- [使用图像和截图](#working-with-images-and-screenshots) — Claude Code 图像分析
- [ASCII Art 和线框图](#wireframing-tools-for-ai-development) — 低保真设计迭代
- [Playwright MCP](#playwright-browser-automation) — 视觉回归测试

---

## 另见

- [Figma MCP 部分](#figma-mcp-integration) — 主指南 Figma MCP 部分
- [examples/claude-md/product-designer.md](../../examples/claude-md/product-designer.md) — 产品设计师 CLAUDE.md 模板
- [../cheatsheet.md](../cheatsheet.md) — 快速参考