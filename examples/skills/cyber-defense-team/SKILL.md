---
name: cyber-defense-team
description: "编排 4 个 agent 的网络防御流水线，分析日志文件中的威胁。用于调查安全日志、检测访问模式中的异常、分类入侵严重性，或从 nginx/auth/syslog 文件生成事件报告。"
allowed-tools: Read Bash
argument-hint: "[日志文件路径]"
effort: high
metadata:
  version: 1.0.0
---

# 网络防御团队技能

编排 4 agent 流水线，分析日志文件中的安全威胁并生成事件报告。

## 流水线架构

```
[你] → 团队负责人（此技能）
           │
           ├─[1]─→ log-ingestor    (haiku)  → cyber-defense-events.json
           │
           ├─[2]─→ anomaly-detector (sonnet) → cyber-defense-anomalies.json
           │                                    (读取 events.json)
           ├─[3]─→ risk-classifier  (sonnet) → cyber-defense-risk.json
           │                                    (读取 anomalies.json)
           └─[4]─→ threat-reporter  (sonnet) → cyber-defense-report.md
                                                (读取所有 3 个 JSON 文件)
```

阶段 2 和 3 是顺序的（每个依赖前一个输出）。阶段 4 在所有数据就绪后运行。

## 执行步骤

### 步骤 1 — 验证输入

检查日志文件是否存在（或日志内容是否内联提供）。如果路径不存在，立即告知用户 — 不要继续。

### 步骤 2 — 启动日志解析器

使用 Agent 工具启动 `log-ingestor` agent：

```
任务：解析 [log_path] 处的日志文件，将结构化事件写入 cyber-defense-events.json。
日志路径：[log_path]
```

等待完成。确认 `cyber-defense-events.json` 已创建。

### 步骤 3 — 启动异常检测器

使用 Agent 工具启动 `anomaly-detector` agent：

```
任务：读取 cyber-defense-events.json 并检测异常。将结果写入 cyber-defense-anomalies.json。
```

等待完成。如果 `anomalies_found: 0`，跳到步骤 5（报告器仍会运行）。

### 步骤 4 — 启动风险分类器

使用 Agent 工具启动 `risk-classifier` agent：

```
任务：读取 cyber-defense-anomalies.json 并分类整体风险。将结果写入 cyber-defense-risk.json。
```

### 步骤 5 — 启动威胁报告器

使用 Agent 工具启动 `threat-reporter` agent：

```
任务：读取 cyber-defense-events.json、cyber-defense-anomalies.json 和 cyber-defense-risk.json。生成完整的事件报告并保存到 cyber-defense-report.md。
```

### 步骤 6 — 为用户总结

读取 `cyber-defense-risk.json` 并呈现：

```
✅ 分析完成

风险等级 : HIGH
评分      : 74/100
威胁     : 检测到 2 个异常
报告     : cyber-defense-report.md

主要威胁：来自 192.168.1.105 的暴力破解攻击
需要立即采取的措施：[首个 recommended_action]
```

## 错误处理

- 步骤 2 中 agent 失败：告知用户，停止流水线，显示原始错误。
- 步骤 3+ 中 agent 失败：显示部分结果，注明哪个阶段失败。
- 日志文件未找到："文件 [路径] 未找到。请提供有效路径或粘贴日志内容。"

## 成本估算

| 阶段 | 模型 | 典型 tokens |
|-------|-------|----------------|
| log-ingestor | haiku | ~2K |
| anomaly-detector | sonnet | ~3K |
| risk-classifier | sonnet | ~2K |
| threat-reporter | sonnet | ~3K |
| **总计** | | **~10K** |

对于大日志文件（>10K 行），log-ingestor 可能使用高达 20K tokens。

## 使用示例

```
/cyber-defense-team /var/log/nginx/access.log
/cyber-defense-team /tmp/auth.log
```
