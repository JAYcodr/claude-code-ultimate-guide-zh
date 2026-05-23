---
title: "带内置评估的分析智能体"
description: "生产级分析智能体，带自动化指标收集和安全验证"
tags: [agents, template, testing, performance]
---

# 带内置评估的分析智能体

**模板**：带自动化指标收集的生产级分析智能体

**用例**：具有质量追踪、性能监控和安全验证的 SQL 查询生成

**相关指南**：[智能体评估](../../../guide/roles/agent-evaluation.md)

---

## 包含内容

| 文件 | 用途 |
|------|---------|
| `analytics-agent.md` | 包含评估标准的智能体定义 |
| `hooks/post-response-metrics.sh` | 每次响应后自动记录指标 |
| `eval/metrics.sh` | 聚合收集指标的分析脚本 |
| `eval/report-template.md` | 月度评估报告模板 |

---

## 设置

### 1. 将智能体复制到项目

```bash
# 复制智能体定义
cp analytics-agent.md ~/.claude/agents/

# 或用于特定项目：
cp analytics-agent.md /path/to/project/.claude/agents/
```

### 2. 安装钩子

```bash
# 将钩子复制到项目
cp hooks/post-response-metrics.sh /path/to/project/.claude/hooks/

# 设为可执行
chmod +x /path/to/project/.claude/hooks/post-response-metrics.sh
```

### 3. 配置钩子触发器

添加到 `.claude/settings.json`：

```json
{
  "hooks": {
    "postToolUse": [
      {
        "command": ".claude/hooks/post-response-metrics.sh",
        "enabled": true,
        "description": "记录分析智能体指标"
      }
    ]
  }
}
```

### 4. 创建日志目录

```bash
mkdir -p /path/to/project/.claude/logs
```

---

## 用法

### 调用智能体

```bash
# 在 Claude Code 会话中
"使用 analytics-agent 为 [任务描述] 生成 SQL 查询"
```

### 检查指标

```bash
# 查看原始指标日志
cat .claude/logs/analytics-metrics.jsonl

# 运行分析
./examples/agents/analytics-with-eval/eval/metrics.sh
```

### 生成月度报告

```bash
# 复制模板
cp eval/report-template.md reports/analytics-2026-02.md

# 从 metrics.sh 输出中填入指标
```

---

## 收集的指标

钩子自动记录：

| 指标 | 描述 | 来源 |
|--------|-------------|--------|
| `timestamp` | ISO 8601 时间戳 | 系统 |
| `query` | 生成的 SQL 查询 | 智能体响应 |
| `exec_time` | 查询执行时间 | 数据库 |
| `safety` | 破坏性操作的 PASS/FAIL | 查询分析 |
| `row_count` | 返回的行数 | 数据库 |
| `error` | 查询失败时的错误信息 | 数据库 |

**日志格式**：JSONL（JSON Lines）在 `.claude/logs/analytics-metrics.jsonl`

---

## 指标输出示例

```bash
$ ./eval/metrics.sh

=== 分析智能体指标报告 ===
期间：2026-02-01 至 2026-02-10

总查询数：45
安全检查：
  - PASS：42 (93%)
  - FAIL：3 (7%)

执行时间：
  - 平均值：2.3s
  - 中位数：1.8s
  - P95：5.2s
  - P99：8.1s

常见失败：
  1. 没有 WHERE 子句的 DELETE（2 次）
  2. 查询中的 DROP TABLE（1 次）

建议：
  - 审查智能体指令以强调 WHERE 子句要求
  - 添加对 DROP 操作的明确禁止
```

---

## 自定义

### 修改安全检查

编辑 `hooks/post-response-metrics.sh` 第 12-16 行：

```bash
# 添加更多模式
if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE|ALTER'; then
  SAFETY="FAIL"
fi
```

### 添加自定义指标

扩展 JSON 日志结构：

```bash
echo "{
  \"timestamp\":\"$(date -Iseconds)\",
  \"query\":\"$QUERY\",
  \"your_metric\":\"$VALUE\"
}" >> .claude/logs/analytics-metrics.jsonl
```

### 更改日志位置

更新钩子脚本中的 `POST_RESPONSE_LOG` 变量。

---

## 故障排查

### 钩子未触发

**检查**：
1. 钩子是否可执行：`ls -l .claude/hooks/*.sh`
2. 钩子是否在 settings.json 中启用
3. 智能体名称是否匹配：`analytics-agent`（连字符）

**调试**：
```bash
# 手动测试钩子
export CLAUDE_RESPONSE='{"content":"SELECT * FROM users;"}'
./.claude/hooks/post-response-metrics.sh
```

### 日志中无指标

**检查**：
1. 日志目录是否存在：`mkdir -p .claude/logs`
2. 写入权限：`touch .claude/logs/test.log`
3. 查询提取模式是否匹配你的 SQL 格式

### 指标分析失败

**检查**：
1. `jq` 是否已安装：`which jq`
2. 日志文件是否是有效的 JSONL：`jq . .claude/logs/analytics-metrics.jsonl`

---

## 生产考虑

### 性能

- 钩子每次响应增加 ~50ms 开销
- 日志文件每次查询增长 ~200 字节
- 每月轮转日志以防膨胀

### 隐私

- 日志包含实际的 SQL 查询（可能包含敏感数据）
- 添加到 `.gitignore`：`.claude/logs/`
- 考虑在钩子脚本中清洗敏感值

### 数据库连接

- 钩子需要数据库访问以测量 `exec_time`
- 在钩子脚本中配置连接或使用环境变量
- 确保只读凭据以确保安全

---

## 相关资源

- **[智能体评估指南](../../../guide/roles/agent-evaluation.md)**：完整的评估方法论
- **[钩子文档](../../../guide/ultimate-guide.md#5-hooks)**：钩子系统参考
- **[nao 框架](https://github.com/getnao/nao/)**：生产级分析智能体框架（灵感来源）

---

## 许可证

与父仓库相同（MIT）

**有问题？** 在主仓库中发起 issue 或讨论。


