---
name: sonarqube
description: 分析特定 PR 的 SonarCloud 质量问题
argument-hint: "[project_key]"
effort: medium
disable-model-invocation: true
---

# SonarQube 分析

分析特定 PR 的 SonarCloud 质量问题。生成包含指标、主要违规者和操作计划的综合报告。

**核心原则**：仅分析 = 无代码更改，纯洞察。

## 流程

1. **验证 Token**：检查 `$SONARQUBE_TOKEN` 环境变量
2. **获取问题**：调用 SonarCloud API 获取 PR 问题
3. **解析数据**：按严重性、类型、文件、规则分组
4. **生成报告**：结构化的输出及操作计划
5. **清理**：删除临时文件

## 前置条件

### 环境变量

```bash
# 设置 SonarQube token（添加到 ~/.bashrc 或 ~/.zshrc）
export SONARQUBE_TOKEN="your_token_here"

# 验证 token 已设置
echo $SONARQUBE_TOKEN
```

**获取 token：**
1. 前往 SonarCloud → My Account → Security
2. 生成新 token
3. 复制并导出为环境变量

### 项目配置

配置你的 SonarCloud 项目详情：

```bash
# 添加到项目的 CLAUDE.md 或作为环境变量
SONAR_ORGANIZATION="your-org-name"
SONAR_PROJECT_KEY="your-org_your-project"
SONAR_BASE_URL="https://sonarcloud.io/api"
```

**如未设置：** 询问用户提供组织和项目 key。

## 获取问题

**重要：** 在 zsh 中直接使用 `-u "$SONARQUBE_TOKEN:"` 的 curl 会因身份验证解析失败。使用 bash 脚本包装器：

```bash
# 创建临时 bash 脚本处理身份验证
cat > /tmp/fetch_sonar.sh << 'SCRIPT'
#!/bin/bash
curl -s -u "${SONARQUBE_TOKEN}:" \
  "https://sonarcloud.io/api/issues/search?componentKeys=${SONAR_PROJECT_KEY}&pullRequest=$1&issueStatuses=OPEN,CONFIRMED&sinceLeakPeriod=true&ps=500"
SCRIPT

chmod +x /tmp/fetch_sonar.sh
/tmp/fetch_sonar.sh $PR_NUMBER > /tmp/sonar_pr_$PR_NUMBER.json
```

**API 参数：**
- `componentKeys`：你的项目 key
- `pullRequest`：PR 编号
- `issueStatuses`：OPEN,CONFIRMED（排除已解决的）
- `sinceLeakPeriod`：仅此 PR 中的新问题
- `ps`：页面大小（最多 500）

## 分析脚本

在 `/tmp/sonar_analyze.js` 创建 Node.js 分析脚本：

```javascript
const fs = require('fs');
const prNumber = process.argv[2];
const data = JSON.parse(fs.readFileSync(`/tmp/sonar_pr_${prNumber}.json`, 'utf8'));
const issues = data.issues || [];

// 按严重性分组
const bySeverity = issues.reduce((acc, i) => {
  acc[i.severity] = (acc[i.severity] || 0) + 1;
  return acc;
}, {});

// 按类型分组
const byType = issues.reduce((acc, i) => {
  acc[i.type] = (acc[i.type] || 0) + 1;
  return acc;
}, {});

// 按文件分组
const byFile = issues.reduce((acc, i) => {
  const file = i.component.split(':')[1] || i.component;
  acc[file] = (acc[file] || 0) + 1;
  return acc;
}, {});

// 按规则分组
const byRule = issues.reduce((acc, i) => {
  if (!acc[i.rule]) {
    acc[i.rule] = {
      count: 0,
      severity: i.severity,
      message: i.message
    };
  }
  acc[i.rule].count++;
  return acc;
}, {});

// 输出结构化数据
console.log(JSON.stringify({
  total: data.total,
  bySeverity,
  byType,
  topFiles: Object.entries(byFile)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10),
  topRules: Object.entries(byRule)
    .map(([rule, d]) => ({ rule, ...d }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}, null, 2));
```

**运行分析：**
```bash
node /tmp/sonar_analyze.js $PR_NUMBER > /tmp/sonar_analysis_$PR_NUMBER.json
```

## 报告格式

从分析生成格式化的报告：

```
📊 SonarCloud 分析 - PR #XXX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 执行摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

总问题数：{TOTAL}

按严重性：
🔴 Blocker/Critical：{COUNT}（{PERCENTAGE}%）
🟡 Major：{COUNT}（{PERCENTAGE}%）
🔵 Minor/Info：{COUNT}（{PERCENTAGE}%）

按类型：
🐛 Bug：{COUNT}
🛡️ 漏洞：{COUNT}
🧹 代码异味：{COUNT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 问题最多的前 10 个文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. src/components/UserProfile.tsx - 8 issues
2. src/services/auth.service.ts - 5 issues
3. src/utils/validation.ts - 4 issues
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 违反最多的前 5 条规则
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. typescript:S1854 (MAJOR) - 12 次
   "应移除死存储"

2. typescript:S3776 (CRITICAL) - 8 次
   "函数的认知复杂度不应过高"

3. typescript:S1186 (MINOR) - 6 次
   "函数不应为空"
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 操作计划
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

优先级 1 - CRITICAL/BLOCKER（{COUNT} 个问题）：
  • 合并前立即修复
  • 重点关注：{TOP_FILES}

优先级 2 - MAJOR（{COUNT} 个问题）：
  • 如有可能在此 PR 中处理
  • 范围大则考虑提技术债务工单

优先级 3 - MINOR/INFO（{COUNT} 个问题）：
  • 可在后续 PR 中处理
  • 添加到重构迭代的待办列表

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 链接
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

在 SonarCloud 中查看：
https://sonarcloud.io/project/pull_requests_list?id={PROJECT_KEY}&pullRequest={PR_NUMBER}
```

## 严重性映射

| SonarCloud | 符号 | 优先级 | 操作 |
|------------|--------|----------|--------|
| BLOCKER | 🔴 | P0 | 立即修复 |
| CRITICAL | 🔴 | P0 | 立即修复 |
| MAJOR | 🟡 | P1 | 在此 PR 中修复 |
| MINOR | 🔵 | P2 | 考虑后续处理 |
| INFO | 🔵 | P3 | 可选改进 |

## 问题类型

| 类型 | 符号 | 描述 |
|------|--------|-------------|
| BUG | 🐛 | 明确错误的代码 |
| VULNERABILITY | 🛡️ | 安全问题 |
| CODE_SMELL | 🧹 | 可维护性问题 |
| SECURITY_HOTSPOT | 🔒 | 需审查的安全敏感代码 |

## 清理

执行后始终清理临时文件：

```bash
rm -f /tmp/fetch_sonar.sh
rm -f /tmp/sonar_pr_$PR_NUMBER.json
rm -f /tmp/sonar_analyze.js
rm -f /tmp/sonar_analysis_$PR_NUMBER.json
```

## 错误处理

| 错误 | 原因 | 操作 |
|-------|-------|--------|
| Token 未设置 | `$SONARQUBE_TOKEN` 缺失 | 要求用户导出 token |
| 401 未授权 | token 无效或过期 | 从 SonarCloud 申请新 token |
| 404 未找到 | PR 在 SonarCloud 中不存在 | 验证 PR 编号和项目 key |
| 空响应 | 未发现问题 | 报告干净的 PR，祝贺团队 |
| >500 问题 | 超出分页限制 | 警告数据不完整，建议过滤 |
| 网络错误 | API 不可达 | 检查网络连接，重试 |

## 配置选项

### 项目级配置

创建 `.sonarcloud.properties` 或添加到 `CLAUDE.md`：

```properties
# SonarCloud 配置
SONAR_ORGANIZATION=your-org
SONAR_PROJECT_KEY=your-org_your-project
SONAR_EXCLUSIONS=**/*.test.ts,**/*.spec.ts,**/migrations/**
SONAR_COVERAGE_EXCLUSIONS=**/*.test.ts,src/test/**
```

### API 速率限制

SonarCloud API 限制：
- 免费套餐：10,000 次请求/天
- 付费套餐：不限

**提示：** 对同一 PR 的重复查询缓存结果。

## 集成示例

### GitHub Actions

```yaml
- name: SonarQube 分析
  run: |
    export SONARQUBE_TOKEN=${{ secrets.SONAR_TOKEN }}
    export SONAR_PROJECT_KEY=${{ secrets.SONAR_PROJECT }}
    claude -p "/sonarqube ${{ github.event.pull_request.number }}"
```

### 合并前钩子

添加到 `.claude/hooks/pre-merge.sh`：

```bash
#!/bin/bash
PR_NUMBER=$(gh pr view --json number -q .number)
claude -p "/sonarqube $PR_NUMBER"
```

## 红旗——绝不做

**绝不：**
- ❌ 修改代码或自动修复问题（仅分析命令）
- ❌ 跳过 token 验证（安全风险）
- ❌ 将临时文件留在 `/tmp` 中（需要清理）
- ❌ 将 SonarQube token 提交到仓库（使用环境变量）
- ❌ 不检查 token 过期就运行

**始终：**
- ✅ 生成结构化、可操作的报告
- ✅ 执行后清理
- ✅ 优雅处理 API 错误
- ✅ 在 API 调用前验证 token 有效
- ✅ 清晰地解析和呈现数据

## 高级用法

### 自定义过滤器

```bash
# 仅显示 critical/blocker 问题
/sonarqube 123 --severity BLOCKER,CRITICAL

# 仅显示 bug 和漏洞
/sonarqube 123 --types BUG,VULNERABILITY

# 特定文件模式
/sonarqube 123 --files "src/services/**"
```

### 多个 PR

```bash
# 比较多个 PR 间的问题
/sonarqube 123,124,125 --compare
```

## 故障排除

### 问题："curl: (22) 请求的 URL 返回错误：401"

**原因：** token 无效或缺失

**修复：**
```bash
# 在 SonarCloud 中重新生成 token
# 导出新 token
export SONARQUBE_TOKEN="new_token_here"
```

### 问题："空响应或无问题"

**原因：** 分析尚未完成或 PR 未被分析

**修复：** 等待 SonarCloud 分析完成（PR 创建后约 2-5 分钟）

### 问题："componentKeys 未找到"

**原因：** 项目 key 错误

**修复：** 在 SonarCloud URL 中验证项目 key：
```
https://sonarcloud.io/project/overview?id=YOUR_PROJECT_KEY
```

## 使用示例

```bash
# 基本用法
/sonarqube 170

# 带 PR 前缀
/sonarqube PR #234

# 使用 PR URL
/sonarqube https://github.com/org/repo/pull/170

# 自定义严重性过滤器（如已实现）
/sonarqube 170 --critical-only
```

PR 编号：$ARGUMENTS
