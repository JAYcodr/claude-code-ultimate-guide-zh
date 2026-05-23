<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->
---
title: "Astro 动态 OG 图片生成"
description: "在构建时自动生成社交预览图片，而不是维护过时的静态 PNG"
tags: [workflow, astro, og-image, static-generation]
---

# Astro 动态 OG 图片生成

在构建时自动生成社交预览图片，告别过时的静态 PNG。每次在 Twitter/X、LinkedIn 或 Slack 上分享都显示准确、最新的数据。

## 为什么要麻烦

静态 OG 图片会过时。当你添加第 200 个模板或达到 1k GitHub stars 时，社交预览仍然显示旧数字。动态生成一劳永逸解决这个问题。

下面的模式使用 Satori（Vercel）将类似 React 的树渲染为 SVG，然后用 resvg 转换为 PNG。它在 Astro 构建时运行——零运行时成本，无外部服务。

## 技术栈

| 包 | 角色 |
|---------|------|
| `satori` | 将 JSX 类对象树渲染为 SVG |
| `@resvg/resvg-js` | 将 SVG 转换为 PNG（Rust，快速） |
| `@fontsource/inter` | 本地字体文件（需要 woff1 格式） |

## 设置

```bash
pnpm add satori @resvg/resvg-js @fontsource/inter
```

在 `src/pages/og-image.png.ts` 创建文件。Astro 自动在 `/og-image.png` 提供服务。

从你的布局引用它：

```html
<meta property="og:image" content="/og-image.png" />
<meta name="twitter:image" content="/og-image.png" />
```

见可用的模板：[`examples/scripts/og-image-astro.ts`](../../examples/scripts/og-image-astro.ts)

## 模式

```typescript
import type { APIRoute } from 'astro'
import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

export const GET: APIRoute = () => {
  const fontData = readFileSync(
    resolve(__dirname, '../../node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')
  ).buffer as ArrayBuffer

  const svg = satori(
    { type: 'div', props: { style: { /* ... */ }, children: [ /* ... */ ] } },
    { width: 1200, height: 630, fonts: [{ name: 'Inter', data: fontData }] }
  )

  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng()

  return new Response(png.buffer as ArrayBuffer, {
    headers: { 'Content-Type': 'image/png' },
  })
}
```

## 动态统计数据

在构建时统计你的内容文件，而不是硬编码：

```typescript
function countQuestions(): number {
  const dir = resolve(__dirname, '../content/questions')
  let total = 0
  for (const cat of readdirSync(dir, { withFileTypes: true })) {
    if (cat.isDirectory()) {
      total += readdirSync(resolve(dir, cat.name))
        .filter(f => f.endsWith('.md')).length
    }
  }
  return total
}
```

可以自动统计的数据：
- 内容目录中的 Markdown 文件（问题、文章、文档）
- 数据文件中的 YAML 条目
- 大文档的行数

保持硬编码的统计数据（手动更新）：
- GitHub stars（动态，使用 `1.1k+` 作为保守标签）
- 来自另一个仓库的模板
- 性能基准

## 注意事项

### 字体格式重要

Satori 需要 **woff1** 或 **TTF**。使用 woff2 或重定向到 HTML 的远程 CDN URL 会静默失败或抛出错误。

```typescript
// 正确 — @fontsource 的本地 woff1
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')

// 失败 — resvg 不支持 woff2
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2')

// 失败 — CDN 可能返回 HTML（重定向、auth walls）
await fetch('https://fonts.gstatic.com/s/inter/...')
```

### 静态文件遮挡 API 路由

Astro dev server 在 API 路由**之前**服务 `public/` 中的静态文件。如果你有 `public/og-image.png`，它将始终被服务而不是你的动态端点。

**删除它：**
```bash
rm public/og-image.png
```

还要检查项目根和 `dist/` — 那里的文件也可能遮挡路由。用 `curl -I http://localhost:4321/og-image.png` 诊断：如果响应有 `Last-Modified` 头，你遇到的是静态文件，而非 API 路由。

### 浏览器缓存

删除静态文件后，进行硬刷新（`Cmd+Shift+R`）或在新的隐身窗口中测试。浏览器可能已经积极缓存了旧 PNG。

### 较新版本的 `satori` 是同步的

某些版本的 satori 返回 `Promise<string>`，其他返回 `string`。如果你得到 `[object Promise]` PNG，添加 `await`：

```typescript
const svg = await satori(tree, options)
```

## 测试

**本地预览** — 直接在浏览器中访问：
```
http://localhost:4321/og-image.png
```

**社交预览模拟** — 将你的生产 URL 粘贴到：
- [opengraph.xyz](https://www.opengraph.xyz) — 通用 OG 调试器
- LinkedIn Post Inspector（`linkedin.com/post-inspector/`）— 强制 LinkedIn 缓存刷新
- Twitter Card Validator（`cards-dev.twitter.com/validator`）

**CI 检查** — 如果你想捕获回归，可以添加构建步骤检查生成的 PNG 文件大小是否超过阈值：

```bash
# In CI after pnpm build
SIZE=$(wc -c < dist/og-image.png)
if [ "$SIZE" -lt 10000 ]; then
  echo "og-image.png looks too small ($SIZE bytes) — generation may have failed"
  exit 1
fi
```

## 变体

### 个人品牌（无统计网格）

```typescript
children: [
  { type: 'span', props: { style: { fontSize: '48px', color: '#c0522a' }, children: 'FB.' } },
  { type: 'span', props: { style: { fontSize: '80px', fontWeight: 800, color: '#f5f5f5' }, children: 'Your Name' } },
  { type: 'span', props: { style: { fontSize: '24px', color: '#8b949e' }, children: 'Your tagline here' } },
]
```

### 项目列表徽章

```typescript
['project-a.com', 'project-b.com', 'project-c.com'].map(label => ({
  type: 'div',
  props: {
    style: { background: '#161b22', border: '1px solid #30363d', borderRadius: '8px', padding: '8px 16px' },
    children: [{ type: 'span', props: { style: { color: '#c0522a' }, children: label } }],
  },
}))
```

### 终端风格徽章（用于 CLI 工具）

```typescript
{
  type: 'div',
  props: {
    style: { background: '#21262d', border: '1px solid #30363d', borderRadius: '20px', padding: '6px 16px', color: '#3fb950', fontFamily: 'monospace' },
    children: '>_ your-cli-tool',
  },
}
```

## 保持统计数据同步

维护单一真相来源。当你在 OG 图片中更新统计数据时，在同一提交中更新它们无处不在（landing page 徽章、README 等）。

对于有多个 landing 的项目，创建一个斜杠命令 `/update-stats-image-landings` 遍历每个仓库并提示你验证每个统计数据。这防止站点之间的漂移。