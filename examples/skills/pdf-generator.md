<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
name: pdf-generator
description: 使用 Quarto/Typst 技术栈配合现代设计模板生成专业 PDF
effort: low
version: 1.0.0
---

# PDF 生成器技能

使用 Quarto + Typst 生成具有现代排版的专业 PDF。

## 技能目的

此技能协助：
- 设置 Quarto/Typst 项目
- 创建文档模板
- 从 Markdown 生成 PDF
- 排查渲染问题
- 自定义设计系统

## 技术栈

| 工具 | 版本 | 角色 |
|------|---------|------|
| **Quarto** | ≥1.4.0 | 文档渲染引擎 |
| **Typst** | 0.13.0 | 现代排版（集成） |
| **Pandoc** | 3.x | Markdown 转换（集成） |

### 生成管道

```
  来源              工具             模板                 输出
  ──────              ─────           ────────              ──────

  .qmd  ──────────► Quarto ────► --to whitepaper-typst ──► Typst 0.13 ──► .pdf ✅
  (Markdown           │           (_extensions/               (~270K–1.7M,
  + YAML)             │            typst-template.typ)         精美样式)
                      │
                      └──────► --to epub ──► Pandoc ──────────────────► .epub
                                             + epub-styles.css

  ⚠️  --to pdf（无模板）→ PDF 小、无样式 → 始终优先用 --to whitepaper-typst
```

### 可用格式

```
  ┌──────────────────────┬────────────────────────┬──────────────────┐
  │ 格式                  │ 命令                   │ 输出              │
  ├──────────────────────┼────────────────────────┼──────────────────┤
  │ 精美样式 PDF ✅        │ --to whitepaper-typst  │ ~270K–1.7M       │
  │ 标准 PDF ❌           │ --to pdf               │ ~80-190K，原始    │
  │ EPUB                 │ --to epub              │ epub-output/     │
  └──────────────────────┴────────────────────────┴──────────────────┘
```

## 快速开始

### 安装

```bash
# macOS
brew install quarto

# Linux
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb

# Windows
winget install Posit.Quarto
```

### 生成 PDF

```bash
# 单个文件
quarto render document.qmd

# 所有文件
quarto render *.qmd

# 带热重载的预览
quarto preview document.qmd
```

## YAML 前导模板

```yaml
---
title: "文档标题"
subtitle: "可选副标题"
author: "作者名"
date: 2026-01-17
date-format: "MMMM YYYY"
format:
  typst:
    toc: true
    toc-depth: 2
    section-numbering: "1.1"
lang: en
---
```

### 可用参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `title` | string | 主标题（封面页） |
| `subtitle` | string | 可选副标题 |
| `author` | string | 作者 |
| `date` | date | ISO 格式（YYYY-MM-DD） |
| `date-format` | string | 显示格式（`MMMM YYYY`） |
| `toc` | boolean | 显示目录 |
| `toc-depth` | number | 目录深度（1-3） |
| `section-numbering` | string | 格式（`1.1`、`1.a`） |
| `lang` | string | 语言（`fr`、`en`） |

## 项目结构

```
project/
├── _extensions/
│   └── custom-template/
│       ├── _extension.yml      # 扩展元数据
│       ├── typst-template.typ  # 主模板
│       └── typst-show.typ      # Quarto → Typst 桥接
├── document.qmd                # 源文件
└── document.pdf                # 生成输出
```

## Markdown 语法

### 分页

```markdown
{{< pagebreak >}}
```

### 代码块

标准围栏代码块，带语法高亮：

````markdown
```bash
npm install
```
````

### 表格

```markdown
| 列 A | 列 B |
|----------|----------|
| 值 1     | 值 2     |
```

### 图片

```markdown
![标题](path/to/image.png){width=50%}
```

## 自定义模板

### 扩展配置

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

### 设计系统（Typst）

```typst
// 颜色（Slate + Indigo 色板）
#let primary = rgb("#0f172a")      // Slate 900 - 标题
#let secondary = rgb("#334155")    // Slate 700 - 副标题
#let accent = rgb("#6366f1")       // Indigo 500 - 强调
#let muted = rgb("#64748b")        // Slate 500 - 元数据
#let light-bg = rgb("#f8fafc")     // Slate 50 - 代码背景
#let border-light = rgb("#e2e8f0") // Slate 200 - 边框
```

### 排版

```typst
#set text(
  font: ("Inter", "Helvetica Neue", "Arial"),
  size: 11pt,
)

#set par(
  leading: 0.75em,
  justify: true,
)

// 代码块
#show raw.where(block: true): it => {
  block(
    fill: light-bg,
    stroke: (left: 3pt + accent),
    inset: 10pt,
    radius: 4pt,
    it,
  )
}
```

### 提示框

```typst
#let info(title: "注意", body) = {
  block(
    fill: rgb("#E0F2FE"),
    stroke: (left: 3pt + rgb("#0284C7")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let warning(title: "警告", body) = {
  block(
    fill: rgb("#FEF3C7"),
    stroke: (left: 3pt + rgb("#D97706")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let success(title: "成功", body) = {
  block(
    fill: rgb("#DCFCE7"),
    stroke: (left: 3pt + rgb("#16A34A")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let danger(title: "危险", body) = {
  block(
    fill: rgb("#FEE2E2"),
    stroke: (left: 3pt + rgb("#DC2626")),
    inset: 12pt,
    [*#title*: #body]
  )
}
```

## 故障排查

### 快速验证

```bash
# 检查 Quarto 版本
quarto --version  # >= 1.4.0

# 验证扩展存在
ls _extensions/*/

# 验证代码块配对（必须为偶数）
grep -c '^```' document.qmd

# 检查编码
file -i document.qmd  # 必须显示 utf-8
```

### 常见问题

| 问题 | 原因 | 修复 |
|-------|-------|-----|
| 嵌套代码块中断 | 内部 ` ``` ` 关闭了外部的 | 外部使用 4+ 个反引号 |
| 表格渲染为代码 | 上方 ` ``` ` 不配对 | 检查定界符数量 |
| 扩展未找到 | 目录错误 | 验证 `_extensions/` 路径 |
| 字体警告 | 字体未安装 | 正常；会使用后备字体 |
| 字符损坏 | 编码错误 | 转换为 UTF-8 |

### 嵌套代码块

外部块使用更多反引号：

`````markdown
````markdown
# 这是外部块

```bash
echo "这是嵌套的"
```

外部继续...
````
`````

### 验证脚本

```bash
#!/bin/bash
for f in *.qmd; do
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "错误：$f 有奇数个代码块（$count）"
  fi
done
```

### 完整验证管道

```bash
#!/bin/bash
# validate-qmd.sh

echo "=== 验证 QMD 文件 ==="
errors=0

for f in *.qmd; do
  # 检查代码块配对
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "错误：$f - 代码块数量为奇数（$count）"
    ((errors++))
  fi

  # 检查 UTF-8
  encoding=$(file -i "$f" | grep -o 'charset=[^;]*')
  if [[ "$encoding" != *"utf-8"* ]]; then
    echo "警告：$f - 编码为 $encoding"
  fi
done

echo "=== 验证完成：$errors 个错误 ==="
exit $errors
```

## 示例用例

### 技术文档

```yaml
---
title: "API 参考"
subtitle: "v2.0"
author: "工程团队"
date: 2026-01-17
format:
  typst:
    toc: true
    toc-depth: 3
---

# 认证

所有请求都需要 API 密钥...
```

### 白皮书系列

```yaml
---
title: "安全最佳实践"
series: "工程白皮书"
wp-number: "03"
author: "安全团队"
date: 2026-01-17
format:
  whitepaper-typst:
    toc: true
---
```

### 内部报告

```yaml
---
title: "第一季度性能报告"
author: "分析团队"
date: 2026-01-17
date-format: "Q1 YYYY"
format:
  typst:
    toc: false
---
```

## 资源

- [Quarto 文档](https://quarto.org/docs/guide/)
- [Typst 文档](https://typst.app/docs/)
- [Quarto + Typst 指南](https://quarto.org/docs/output-formats/typst.html)
- [工作流指南](../../guide/workflows/pdf-generation.md)
