---
name: canary
description: "部署后监控——部署后观察生产环境并在回归时发出告警"
argument-hint: "[--baseline]"
effort: medium
disable-model-invocation: true
---

# 金丝雀——部署后监控

部署后观察实时应用。在错误和回归时发出告警。与部署前基线进行对比。

**两种模式：**
- `--baseline` — 在部署前捕获当前状态
- （默认）— 部署后监控并与基线对比

## 使用说明

### 阶段 1：设置

解析用户参数并检测部署上下文。

```bash
# 检测当前分支和最近部署提交
git branch --show-current
git log --oneline -5

# 从配置文件自动检测平台
[ -f fly.toml ]         && echo "平台：fly"
[ -f render.yaml ]      && echo "平台：render"
[ -f vercel.json ]      && echo "平台：vercel"
[ -f netlify.toml ]     && echo "平台：netlify"
[ -f Procfile ]         && echo "平台：heroku"
[ -f railway.toml ]     && echo "平台：railway"

# 检查健康端点
curl -sf "${URL}/health" -w "\n%{http_code}" 2>/dev/null | tail -1
curl -sf "${URL}/api/health" -w "\n%{http_code}" 2>/dev/null | tail -1
```

创建工作目录：

```bash
mkdir -p .canary/baselines .canary/reports .canary/screenshots
```

---

### 阶段 2：基线捕获（`--baseline` 模式）

在部署前运行，捕获当前健康状态。

对每个要监控的页面，记录：

1. **HTTP 状态**——页面是否返回 200？
2. **响应时间**——加载耗时多少？
3. **内容快照**——关键文本内容，以便后续检测空白页面

```bash
# 对每个页面 URL
for PAGE_PATH in "/" "/dashboard" "/settings" "/api/health"; do
  SLUG=$(echo "$PAGE_PATH" | tr '/' '_' | tr -d '?&=')
  RESULT=$(curl -sf -o /dev/null -w "%{http_code}|%{time_total}" "${BASE_URL}${PAGE_PATH}" 2>/dev/null)
  STATUS=$(echo "$RESULT" | cut -d'|' -f1)
  TIME_MS=$(echo "$RESULT" | awk -F'|' '{printf "%.0f", $2 * 1000}')
  echo "  ${PAGE_PATH}：HTTP ${STATUS}，${TIME_MS}ms"
done
```

保存基线到 `.canary/baselines/baseline.json`：

```json
{
  "url": "<base-url>",
  "timestamp": "<ISO-8601>",
  "branch": "<branch-name>",
  "commit": "<git-SHA>",
  "pages": {
    "/": { "status": 200, "time_ms": 450 },
    "/dashboard": { "status": 200, "time_ms": 680 },
    "/api/health": { "status": 200, "time_ms": 45 }
  }
}
```

然后**停止**并告知用户："基线已捕获。部署你的更改，然后运行 `/canary <url>` 进行监控。"

---

### 阶段 3：页面发现

如果未指定页面，自动发现要监控的页面。

**从应用中：**

```bash
# 如有站点地图则检查
curl -sf "${URL}/sitemap.xml" 2>/dev/null | grep -oP '(?<=<loc>)[^<]+' | head -10

# 检查 robots.txt 中的已知路径
curl -sf "${URL}/robots.txt" 2>/dev/null | grep -i "allow\|disallow" | head -10

# 始终检查的常见路径
echo "始终检查：/ /login /dashboard /settings /api/health"
```

如果未找到任何页面，默认监控路径：`/`（仅主页）。

---

### 阶段 4：监控循环

按指定时长（默认：10 分钟）进行监控。每 60 秒运行一次检查。

**每个检查周期：**

```bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CHECK_NUM=$((CHECK_NUM + 1))

for PAGE_PATH in "${PAGES[@]}"; do
  # 检查 HTTP 状态和响应时间
  RESULT=$(curl -sf -o /dev/null -w "%{http_code}|%{time_total}" \
    --max-time 10 "${BASE_URL}${PAGE_PATH}" 2>/dev/null || echo "0|0")
  STATUS=$(echo "$RESULT" | cut -d'|' -f1)
  TIME_MS=$(echo "$RESULT" | awk -F'|' '{printf "%.0f", $2 * 1000}')

  # 与基线对比
  BASELINE_STATUS=$(jq -r ".pages[\"${PAGE_PATH}\"].status // 200" .canary/baselines/baseline.json 2>/dev/null)
  BASELINE_TIME=$(jq -r ".pages[\"${PAGE_PATH}\"].time_ms // 1000" .canary/baselines/baseline.json 2>/dev/null)

  echo "  [检查 #${CHECK_NUM}] ${PAGE_PATH}：HTTP ${STATUS}（${TIME_MS}ms）"
done
```

**告警级别：**

| 级别 | 条件 | 触发 |
|-------|-----------|---------|
| **严重** | 页面加载失败 | HTTP 状态不是 2xx、curl 超时、DNS 失败 |
| **高** | 新错误 | 错误率相比基线增加（控制台错误、5xx 响应） |
| **中** | 性能回归 | 响应时间超过基线 2 倍 |
| **低** | 新断链 | 之前正常的路由现在返回 404 |

**关键原则：**
- **对变化发出告警，而非绝对值。** 基线中有 3 个错误的页面仍然只有 3 个就没问题。出现 1 个新错误才是告警。
- **容忍瞬态故障。** 仅在模式持续超过 2 次连续检查时才发出告警。单次网络波动不是告警。

**当严重或高级别告警触发时（连续 2 次检查）：**

```
金丝雀告警
════════════════════════════════════════
时间：     [检查 #N，已过 Xs]
页面：     [URL]
级别：     [严重/高/中/低]
发现：     [什么变了——请具体]
基线：     [基线值]
当前：     [当前值]
════════════════════════════════════════
选项：
  A) 立即调查——停止监控，聚焦此问题
  B) 继续监控——等待下次检查确认
  C) 回滚——撤销此次部署
  D) 忽略——已知问题，继续监控
```

---

### 阶段 5：健康报告

监控完成后（或用户停止），生成摘要。

```
金丝雀报告 — [url]
═══════════════════════════════════════════════════
时长：       [X 分钟]
检查次数：   [每个页面 N 次]
页面数：     [监控 N 个页面]
提交：       [部署的 SHA]
状态：       [健康/退化/损坏]

各页面结果：
─────────────────────────────────────────
  页面           状态       平均时间   告警数
  /              健康       450ms      0
  /dashboard     退化       1100ms     1 个中（原 450ms）
  /settings      健康       380ms      0
  /api/health    健康       45ms       0

已触发的告警：[N] 次（X 严重、Y 高、Z 中、W 低）

裁决：[部署健康/部署有问题——见上方告警]
═══════════════════════════════════════════════════
```

保存报告到 `.canary/reports/<日期>-canary.md`。

---

### 阶段 6：基线更新

如果部署健康且用户希望更新基线：

```bash
cp .canary/reports/latest-snapshot.json .canary/baselines/baseline.json
echo "基线已更新至提交 $(git rev-parse --short HEAD)"
```

---

## 输出格式

见上方阶段 5 的完整金丝雀报告模板。

内联告警格式（监控期间）：
```
[08:42:15] 检查 #3 — /dashboard：告警 高级 — 响应时间 1250ms（基线：420ms）
[08:43:15] 检查 #4 — /dashboard：告警 高级 — 响应时间 1180ms（基线：420ms）
→ 连续 2 次检查一致。发出告警。
```

## 用法

```
/canary https://app.example.com                # 监控主页 10 分钟
/canary https://app.example.com --baseline     # 部署前捕获基线
/canary https://app.example.com --duration 5m  # 监控 5 分钟
/canary https://app.example.com --quick        # 单次健康检查（不循环）
/canary https://app.example.com --pages /,/dashboard,/api/health
```

## 提示

1. **部署到生产前始终捕获基线**——运行 `/canary <url> --baseline`
2. **部署后立即开始监控**——前 5 分钟捕获 90% 的回归
3. **严重告警 = 立即调查**——不要等监控完成
4. **中告警（性能）**——可能是缓存预热，等待 2-3 次检查后再行动
5. **将 `.canary/baselines/` 纳入 git**——任何团队成员都可以针对同一基线运行金丝雀检查

## 相关命令

- `/ship` — 部署前检查清单（部署前运行）
- `/land-and-deploy` — 完整的合并到验证流水线（自动运行金丝雀）
- `/qa` — 发布前的交互式 QA 测试

$ARGUMENTS
