<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

# 模块 07：进阶模式

**时间**: 2-3 小时 | **难度**: ⭐⭐⭐ 进阶

## 目标

编排多智能体工作流。构建协调多个专业智能体的复杂自动化系统。

---

## 你将学到

- 多智能体架构模式
- 编排策略
- 错误处理和恢复
- 生产级自动化
- 团队工作流
- 真实场景

---

## 多智能体系统

**多智能体系统**是指多个专业智能体协作完成一个目标。

### 示例：代码发布工作流

不用一个 Claude 包揽所有事情：

```
你："发布 3.5.0 版本"
    ↓
    ├─→ [版本智能体] 更新 VERSION 文件
    │
    ├─→ [更新日志智能体] 创建发布说明
    │
    ├─→ [测试智能体] 运行完整测试套件
    │
    ├─→ [安全智能体] 安全审计
    │
    ├─→ [文档智能体] 更新文档
    │
    └─→ [发布智能体] 打标签、构建、发布

结果：完整的、经过测试的、有文档的发布
```

每个智能体在自己的专业任务上跑得飞快。

---

## 编排模式

### 模式 1：串行（流水线）

智能体一个接一个运行。前一个的输出成为后一个的输入。

```
输入
  ↓
[智能体 1：解析需求] → 输出：结构化需求
  ↓
[智能体 2：设计 Schema] → 输出：数据库 schema
  ↓
[智能体 3：生成代码] → 输出：代码骨架
  ↓
[智能体 4：写测试] → 输出：测试套件
  ↓
最终结果
```

**适用场景**：每一步依赖上一步的工作流。

**示例**：
```bash
/agent requirements-parser
把功能需求解析为技术规格

# 有了规格之后：
/agent database-designer
根据这些规格设计数据库 schema

# schema 批准后：
/agent code-generator
根据 schema 生成模型代码
```

### 模式 2：并行（分支-合并）

多个智能体同时工作，结果汇总。

```
          输入
            ↓
     ┌──────┼──────┐
     ↓      ↓      ↓
  [单元   [集成  [安全
   测试]   测试]  审计]
     ↓      ↓      ↓
     └──────┼──────┘
            ↓
       合并结果
            ↓
       最终报告
```

**适用场景**：独立的检查或任务。

**示例**：
```
请求："审查我的代码变更"

并行任务：
- 代码质量智能体审查
- 安全智能体扫描
- 测试覆盖率智能体检查
- 性能智能体分析

（以上同时运行）

结果合并为一份报告
```

### 模式 3：条件（如果-则）

根据条件路由到不同的智能体。

```
输入："修复这个 bug"
  ↓
[分析器：是安全问题吗？]
  ├─ 是 → [安全智能体]
  ├─ 性能 → [性能智能体]
  └─ 逻辑 → [逻辑智能体]
  ↓
结果
```

**示例**：
```bash
/agent bug-classifier
把这个问题分类：安全、性能、还是逻辑

# 根据回复：
# 如果安全：
/agent security-patcher
修复安全漏洞

# 如果性能：
/agent perf-optimizer
优化这段代码
```

---

## 构建发布工作流

### 场景

你想自动化发布流程。现在是手动做：
1. 更新 VERSION 文件
2. 更新 CHANGELOG
3. 跑测试
4. 跑安全扫描
5. 创建 git tag
6. 推送到远程
7. 部署到预发布环境

### 解决方案：多智能体工作流

**第一步：创建智能体**（各专攻一项）

`.claude/agents/version-manager.md`：
```markdown
---
name: version-manager
description: 管理版本文件和标签
capabilities:
  - read_files
  - write_files
  - NO: push
---

# Version Manager

## Purpose
更新 VERSION 文件并创建 git tag

## Tasks
- 升级版本（patch、minor、major）
- 更新 VERSION 文件
- 更新 package.json、pyproject.toml 等中的版本
- 创建带注释的 git tag
```

`.claude/agents/changelog-generator.md`：
```markdown
---
name: changelog-generator
description: 生成发布说明
---

# Changelog Generator

## Purpose
从 commit 生成可读的发布说明

## Output Format
- 版本标题
- 破坏性变更（如果有）
- 新功能
- Bug 修复
- 弃用说明
```

`.claude/agents/test-validator.md`：
```markdown
---
name: test-validator
description: 运行完整测试套件
---

# Test Validator

## Purpose
执行所有测试并验证覆盖率

## Minimum Requirements
- 所有测试通过
- 覆盖率 >80%
- 没有脆弱的测试
```

`.claude/agents/release-publisher.md`：
```markdown
---
name: release-publisher
description: 发布和部署
---

# Release Publisher

## Purpose
打标签并推送到远程

## Steps
1. 创建 git tag
2. 推送到远程
3. 触发 CI/CD 流水线
4. 监控部署
```

**第二步：创建发布工作流命令**

`.claude/commands/release-workflow.md`：
```markdown
# /release-workflow

编排完整的发布流程。

Usage:
```
/release-workflow patch|minor|major
```

## Process

1. 验证发布就绪状态
2. 更新版本（version-manager 智能体）
3. 生成更新日志（changelog-generator 智能体）
4. 跑测试（test-validator 智能体）
5. 安全扫描（security-auditor 智能体）
6. 发布和部署（release-publisher 智能体）

## Requirements
- 所有测试通过
- 没有未修复的安全问题
- 更新日志已更新
```

**第三步：使用工作流**

```bash
/release-workflow patch
```

Claude 会：
1. 调用 version-manager → 更新 VERSION
2. 调用 changelog-generator → 创建发布说明
3. 调用 test-validator → 验证测试通过
4. 调用 security-auditor → 扫描漏洞
5. 调用 release-publisher → 创建标签、推送
6. 你审查，然后批准每一步

---

## 多智能体系统的错误处理

### 模式：优雅降级

某个智能体失败时，其他的继续：

```
[测试智能体] ❌ 失败：3 个测试未通过
  ↓
[安全智能体] ✅ 通过：未发现漏洞
  ↓
[文档智能体] ✅ 通过：文档已更新
  ↓
[汇总结果]
  ⚠️  发布被阻止（测试未通过）
  ✅ 安全通过
  ✅ 文档就绪
  [先修好测试再来的提示]
```

### 模式：失败重试

针对暂时性故障（网络、超时）：

```bash
#!/bin/bash
# 在钩子或技能中

max_retries=3
retry=0

while [ $retry -lt $max_retries ]; do
  if /agent test-validator run-tests; then
    echo "✅ 测试通过"
    exit 0
  fi
  
  retry=$((retry + 1))
  if [ $retry -lt $max_retries ]; then
    echo "⚠️  第 $retry/$max_retries 次重试"
    sleep 5
  fi
done

echo "❌ 测试失败，已重试 $max_retries 次"
exit 1
```

### 模式：出错回滚

如果出问题，撤销变更：

```bash
#!/bin/bash
# 回滚辅助

ORIGINAL_VERSION=$(git rev-parse HEAD:VERSION)
ORIGINAL_TAG=$(git describe --tags --abbrev=0)

cleanup_and_exit() {
  echo "正在回滚..."
  git reset --hard HEAD~1
  git tag -d "$NEW_TAG"
  echo "VERSION 恢复到：$ORIGINAL_VERSION"
  exit 1
}

# 执行发布步骤
if ! /agent version-manager bump-version patch; then
  cleanup_and_exit
fi

if ! /agent test-validator validate-all; then
  cleanup_and_exit
fi

# 能走到这里，发布就成功了
exit 0
```

---

## 生产模式

### 模式 1：分阶段发布

逐步发布到不同环境：

```
/release major
  ↓
[开发环境] 部署并测试
  ✅ 验证通过
  ↓
[预发布环境] 部署并测试
  ✅ 验证通过
  ↓
[生产环境] 部署并监控
  ✅ 监控正常
  ↓
发布完成
```

### 模式 2：审批门禁

未经审查不能推进：

```bash
# 在 .claude/hooks/pre-prod-deploy.sh 中

echo "🚨 生产部署"
echo "变更：$CHANGES"
echo "测试：通过"
echo "安全：通过"
echo ""
read -p "输入 'I approve' 确认部署到生产环境：" approval

if [ "$approval" != "I approve" ]; then
  echo "❌ 部署已取消"
  exit 1
fi

exit 0
```

### 模式 3：监控与回滚

部署后验证健康状态：

```bash
#!/bin/bash
# 部署后钩子

sleep 10  # 等待服务启动

# 健康检查
if ! curl -f https://api.example.com/health; then
  echo "❌ 健康检查失败"
  echo "正在回滚..."
  git revert -n HEAD
  git commit -m "回滚：部署后健康检查失败"
  exit 1
fi

echo "✅ 部署成功，服务健康"
exit 0
```

---

## 练习：构建你的第一个多智能体工作流

### 场景

你有一个数据科学项目。发布检查清单：
1. 更新模型版本
2. 跑验证测试
3. 生成性能报告
4. 更新文档
5. 创建发布标签

### 第一步：创建智能体

在 `.claude/agents/` 中创建：
- `model-versioner.md` — 更新 VERSION、模型元数据
- `validator.md` — 跑验证测试
- `report-generator.md` — 创建性能指标
- `doc-updater.md` — 更新 README、API 文档
- `release-tagger.md` — 创建 git tag

### 第二步：创建编排命令

`.claude/commands/ml-release.md`：
```markdown
# /ml-release

发布新版模型。

Usage：
```
/ml-release [major|minor|patch]
```

## Workflow
1. 版本智能体升级版本
2. 验证器跑测试套件
3. 报告智能体生成指标
4. 文档智能体更新文档
5. 打标签智能体创建发布标签
```

### 第三步：测试

```bash
/ml-release patch
```

观察智能体们如何协作完成整个发布流程。

---

## 进阶系统的最佳实践

### 应该

✅ 将智能体设计为**可组合**的（输出能对接下一个智能体）

✅ **记录一切**（有助于排查故障）

✅ **先在小的变更上测试**工作流

✅ **记录编排流程**（让其他人能理解）

✅ 为有风险的操作加入**审批门禁**

✅ **自动化后仍要监控**（验证是否成功）

### 不应该

❌ 链式调用太多智能体（超过 7 个就难调试了）

❌ 让智能体**相互依赖**（优先松耦合）

❌ 跳过**错误处理**（总会出问题的）

❌ **不经测试**就部署自动化发布

❌ 以为智能体**永远一致**（要预设冲突解决方案）

---

## 验证：完成本模块的标志

✓ 你能解释多智能体编排模式

✓ 你至少创建了 2-3 个协作的智能体

✓ 你理解错误处理策略

✓ 你知道如何设计带审批门禁的工作流

✓ 你能为你的项目构建一个发布自动化

---

## 下一步

你已经完成了 7 个模块的学习路径！现在你掌握了：

- ✅ 安装和设置
- ✅ 核心循环和上下文
- ✅ 记忆和配置
- ✅ 智能体专业化
- ✅ 技能和知识
- ✅ 钩子和自动化
- ✅ 进阶编排

### 接下来做什么

**选项 A：深入一个领域**
- 深入安全：`guide/security/`
- 深入 DevOps：`guide/ops/`
- 深入架构：`guide/core/architecture.md`

**选项 B：动手构建**
- 为你的项目创建一个多智能体工作流
- 实现本路径中的某个练习
- 构建一个插件包与团队分享

**选项 C：从示例中学习**
- 在 `examples/agents/` 中查看生产级智能体
- 在 `examples/plugins/` 中学习插件包
- 在 `guide/core/skill-design-patterns.md` 中探索技能

**选项 D：自我评估**
- 执行 `/self-assessment comprehensive` 找出差距
- 获取个性化推荐
- 为薄弱环节创建学习计划

---

**已完成模块 07？** → 你已经是 Claude Code 高阶用户了！🚀

完整指南请移步 `guide/ultimate-guide.md` 深入阅读，或把你学到的教给别人。
