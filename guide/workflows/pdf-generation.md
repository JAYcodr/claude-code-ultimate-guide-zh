---
title: "PDF 生成与 Claude Code"
description: "使用 Claude Code 通过 Quarto 和 Typst 技术栈生成专业 PDF"
tags: [workflow, guide, integration]
---

# PDF 生成与 Claude Code

> **可信度**：第 2 层 — 基于 Quarto/Typst 技术栈的生产测试工作流。

用 Claude Code 和现代排版设计生成专业 PDF（文档、白皮书、报告）。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用](#何时使用)
3. [技术栈概述](#技术栈概述)
4. [设置](#设置)
5. [工作流](#工作流)
6. [与 Claude Code 集成](#与-claude-code-集成)
7. [自定义](#自定义)
8. [故障排除](#故障排除)
9. [另见](#另见)

---

## TL;DR

```bash
# 安装
brew install quarto  # macOS

# 生成
quarto render document.qmd  # → document.pdf

# 预览
quarto preview document.qmd  # 热重载
```

**技术栈**：Quarto（编排）+ Typst（排版）+ Pandoc（markdown）

---

## 何时使用

| 用例 | 适合度 | 替代方案 |
|----------|----------|-------------|
| 技术文档 | ✅ | — |
| 白皮书/报告 | ✅ | — |
| API 文档 | ⚠️ | OpenAPI + Redoc |
| 幻灯片/演示 | ⚠️ | Quarto Revealjs |
| 快速笔记 | ❌ | 纯 Markdown |
| 协作编辑 | ❌ | Google Docs、Notion |

**最适合**：需要专业布局、版本控制和可重现性的长篇技术内容。

---

## 技术栈概述

```
┌─────────────────────────────────────────────────┐
│                  Your .qmd File                 │
│         (Markdown + YAML frontmatter)           │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                    Quarto                       │
│           (Document rendering engine)           │
│         • Processes YAML metadata               │
│         • Handles extensions                   │
│         • Manages output formats               │
└─────────────────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│       Pandoc        │    │       Typst         │
│   (MD → AST → ?)    │    │  (Typography/PDF)   │
│  • Markdown parser  │    │  • Modern engine    │
│  • AST transforms   │    │  • Fast compilation │
│  • Format bridges  │    │  • No LaTeX needed  │
└─────────────────────┘    └─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                  document.pdf                   │
│        (Professional typography output)         │
└─────────────────────────────────────────────────┘
```

### 输出格式和命令

```
  格式                命令                      输出
  ─────              ────────                  ──────

  标准 PDF     →  quarto render doc.qmd            doc.pdf
                     --to typst                       (无模板自定义)

  样式 PDF ✅ →  quarto render doc.qmd            doc.pdf
                     --to whitepaper-typst            (~270K–1.7M, Bold Guy)
                     (通过 _extensions/ 自定义格式)

  EPUB        →  quarto render doc.qmd            doc.epub
                     --to epub

  预览        →  quarto preview doc.qmd           浏览器热重载
```

### 扩展结构

```
_extensions/
└── whitepaper/
    ├── _extension.yml       ← 声明 "whitepaper-typst" 格式
    ├── typst-template.typ   ← 设计系统（颜色、排版、callouts）
    └── typst-show.typ       ← 桥接 Quarto → Typst

⚠️ 如果你在 fr/ en/ 和根目录维护副本：
    保持 3 个 typst-template.typ 文件同步
```

### 快速故障排除

```
  症状                        原因                    修复
  ────────                    ─────                    ───
  PDF 小 (~80-190K)，未样式化   --to pdf 而非          改用 --to whitepaper-typst
                                --to whitepaper-typst

  "bibliography" 错误           @ 在 callout 标题中     删除标题中的 @
                                 → 被解释为引用

  表格渲染为代码              开头 ``` 未闭合         计数 ```（必须是偶数）

  "Extension not found"        错误的目录              验证 _extensions/ 路径
```

| 组件 | 版本 | 角色 |
|-----------|---------|------|
| **Quarto** | ≥1.4.0 | 编排、扩展、多格式 |
| **Typst** | 0.13.0 | 现代排版（替代 LaTeX）|
| **Pandoc** | 3.x | Markdown 解析（随 Quarto 捆绑）|

---

## 设置

### 安装

**macOS**：
```bash
brew install quarto
```

**Linux（Debian/Ubuntu）**：
```bash
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb
```

**Windows**：
```powershell
winget install Posit.Quarto
```

**验证**：
```bash
quarto --version  # 应该 ≥1.4.0
```

### 项目结构

```
project/
├── _extensions/           # Quarto 扩展（模板）
│   └── custom-template/
│       ├── _extension.yml
│       ├── typst-template.typ
│       └── typst-show.typ
├── documents/
│   ├── guide.qmd          # 源文件
│   └── guide.pdf          # 生成输出
└── assets/
    └── logo.png           # 共享资源
```

### 最小文档

创建 `document.qmd`：

```yaml
---
title: "My Document"
author: "Author Name"
date: 2026-01-17
format:
  typst:
    toc: true
lang: en
---

# Introduction

Your content here...

## Section 1

More content with **bold** and `code`.

```bash
echo "Code blocks work!"
```

## Section 2

| Column A | Column B |
|----------|----------|
| Data 1   | Data 2   |
```

生成：
```bash
quarto render document.qmd  # Creates document.pdf
```

---

## 工作流

### 1. 内容优先方法

```
1. 用 Markdown (.qmd) 写内容
2. 添加 YAML frontmatter 用于元数据
3. 用热重载预览
4. 生成最终 PDF
5. 源代码和 PDF 都版本控制
```

### 2. 可用 YAML 参数

| 参数 | 类型 | 描述 | 示例 |
|-----------|------|-------------|---------|
| `title` | string | 主标题 | `"Technical Guide"` |
| `subtitle` | string | 副标题 | `"v2.0 Edition"` |
| `author` | string/array | 作者 | `"John Doe"` |
| `date` | date | 文档日期 | `2026-01-17` |
| `date-format` | string | 显示格式 | `"MMMM YYYY"` |
| `toc` | boolean | 目录 | `true` |
| `toc-depth` | number | TOC 级别（1-3）| `2` |
| `lang` | string | 语言 | `fr` or `en` |
| `section-numbering` | string | 编号格式 | `"1.1"` |

### 3. Markdown 功能

**分页**：
```markdown
{{< pagebreak >}}
```

**代码块**（带语法高亮）：
````markdown
```typescript
function hello(): string {
  return "world";
}
```
````

**表格**：
```markdown
| Feature | Supported |
|---------|-----------|
| Tables  | ✅        |
| Images  | ✅        |
| Links   | ✅        |
```

**图片**：
```markdown
![Alt text](path/to/image.png){width=50%}
```

---

## 与 Claude Code 集成

### 使用 pdf-generator 技能

调用技能以获得引导式 PDF 生成：

```
/pdf-generator
```

技能提供：
- 带 YAML frontmatter 的模板
- 设计系统配置
- 常见故障排除修复
- 生成命令

### 提示词示例

**生成文档**：
```
Create a technical guide for our API as a Quarto document.
Use the Typst format with a table of contents.
Include sections for: Authentication, Endpoints, Error Codes.
```

**转换现有 Markdown**：
```
Convert README.md to a professional PDF.
Add a cover page with title and date.
Use Quarto/Typst format.
```

**创建模板**：
```
Create a Quarto extension for our company's document style:
- Logo in header
- Custom colors: primary #0f172a, accent #6366f1
- Inter font for body, JetBrains Mono for code
```

### 使用计划模式

对于复杂文档：
```
[Press Shift+Tab to enter Plan Mode]

I need to create a series of 5 technical whitepapers.
Plan the structure:
1. Common template/extension
2. Shared assets
3. Build automation
4. Version management
```

### 使用钩子

使用 PostToolUse 钩子在编辑后自动生成 PDF：

```json
// In .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$TOOL_INPUT\" | grep -q '.qmd'; then quarto render \"$FILE\"; fi"
      }
    ]
  }
}
```

---

## 自定义

### 自定义模板扩展

创建 `_extensions/mytemplate/_extension.yml`：

```yaml
title: My Template
author: Your Name
version: 1.0.0
contributes:
  formats:
    typst:
      template: typst-template.typ
      template-partials:
        - typst-show.typ
```

### Typst 模板变量

在 `typst-template.typ` 中：

```typst
// Colors
#let primary = rgb("#0f172a")      // Dark text
#let secondary = rgb("#334155")    // Lighter text
#let accent = rgb("#6366f1")       // Highlights

// Typography
#set text(
  font: ("Inter", "Helvetica Neue", "Arial"),
  size: 11pt,
)

#set par(
  leading: 0.75em,  // Line height
  justify: true,
)

// Code blocks
#show raw.where(block: true): it => {
  block(
    fill: rgb("#f8fafc"),
    stroke: (left: 3pt + accent),
    inset: 10pt,
    radius: 4pt,
    it,
  )
}
```

### Callout 框

在模板中定义：

```typst
#let info(title: "Note", body) = {
  block(
    fill: rgb("#E0F2FE"),
    stroke: (left: 3pt + rgb("#0284C7")),
    inset: 12pt,
    radius: 4pt,
    [*#title*: #body]
  )
}

#let warning(title: "Warning", body) = { ... }
#let success(title: "Success", body) = { ... }
#let danger(title: "Danger", body) = { ... }
```

在文档中使用：
```typst
#info[This is an informational note.]
#warning(title: "Attention")[Check your configuration.]
```

---

## 故障排除

### 快速检查

```bash
# 验证 Quarto
quarto --version

# 检查扩展是否存在
ls _extensions/*/

# 验证代码块对（必须是偶数）
grep -c '^```' document.qmd

# 检查编码
file -i document.qmd  # 应该显示 utf-8
```

### 常见问题

| 问题 | 症状 | 修复 |
|-------|---------|-----|
| 嵌套代码块 | 内容逃逸代码块 | 外层使用 4+ 反引号 |
| 表格作为代码 | 灰色背景 | 检查上方未匹配的 ` ``` ` |
| 缺少扩展 | "Extension not found" | 验证 `_extensions/` 路径 |
| 字体警告 | "unknown font family" | 正常；使用回退 |
| 特殊字符损坏 | `?` 或乱码 | 转换为 UTF-8 |

### 嵌套代码块

**问题**：内部代码块过早关闭外层代码块。

**解决方案**：外层使用更多反引号：

`````markdown
````markdown
# Outer block with 4 backticks

```bash
echo "Inner block with 3 backticks"
```

Outer block continues...
````
`````

### 验证脚本

```bash
#!/bin/bash
# validate-qmd.sh

for f in *.qmd; do
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f has odd code block count ($count)"
  fi
done
```

---

## 另见

- [Quarto 文档](https://quarto.org/docs/guide/)
- [Typst 文档](https://typst.app/docs/)
- [Quarto + Typst 指南](https://quarto.org/docs/output-formats/typst.html)
- [examples/skills/pdf-generator.md](../../examples/skills/pdf-generator.md) — 技能模板
- [whitepapers/README.md](../../whitepapers/README.md) — 生产示例