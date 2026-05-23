<!-- 中文翻译版 · 基于上游 commit: dbeb30c -->

# 模块 06：钩子与事件

**时间**: 1 小时 | **难度**: ⭐⭐ 初级

## 目标

自动化系统事件的响应。创建在 Claude Code 操作之前或之后执行的脚本。

---

## 你将学到

- 钩子如何工作，何时触发
- 创建提交前验证
- 构建操作后通知
- 编写安全的自动化脚本
- 常见钩子模式

---

## 什么是钩子？

**钩子（Hook）** 是一个脚本，在响应某个事件时自动运行。

### 示例：提交前钩子

在你提交变更之前：

```
你执行：git commit -m "Fix bug"
       ↓
钩子运行：检查版本号是否一致
       ↓
如果版本不对：
  ❌ 提交被阻止
  错误信息告诉你怎么了
       ↓
你修复：更新 VERSION 文件
       ↓
提交成功
```

钩子可以防止常见错误流入 git。

### 钩子事件

钩子可以在以下时机触发：

| 事件 | 时机 | 用途 |
|------|------|------|
| PreToolUse | Claude 运行工具之前 | 验证请求 |
| PostToolUse | Claude 运行工具之后 | 记录结果、检查输出 |
| PreCommit | git 提交之前 | 验证变更 |
| PostPush | git 推送之后 | 通知团队 |

---

## 创建你的第一个钩子

钩子是 `.claude/hooks/` 目录下的 bash（或 PowerShell）脚本。

### 钩子基本结构

```bash
#!/bin/bash

# Hook: validate-version
# Event: PreCommit
# Description: 检查 VERSION 文件是否随其他变更一起更新

# 获取正在提交的文件
FILES=$(git diff --cached --name-only)

# 检查是否有 guide 文件被修改
if echo "$FILES" | grep -q "guide/"; then
  # 如果 guide/ 有变化，VERSION 也必须变
  if ! echo "$FILES" | grep -q "VERSION"; then
    echo "❌ 错误：guide/ 被修改了但没有更新 VERSION"
    echo "执行：echo '3.x.x' > VERSION"
    exit 1  # 阻止提交
  fi
fi

exit 0  # 允许提交
```

### 文件位置

```
my-project/
└── .claude/
    └── hooks/
        ├── validate-version.sh
        └── notify-team.sh
```

### 钩子退出码

```bash
exit 0   # 成功 — 允许操作继续
exit 1   # 失败 — 阻止操作并显示错误
exit 2   # 警告 — 允许但显示警告信息
```

---

## 钩子模式

### 模式 1：提交前验证

阻止验证失败的提交：

```bash
#!/bin/bash
# Hook: security-check.sh
# 如果发现安全问题，阻止提交

# 检查硬编码的 API 密钥
if grep -r "sk_live_" .; then
  echo "❌ 错误：发现硬编码的 Stripe 密钥"
  exit 1
fi

# 检查生产代码中的 console.log（不含测试目录）
if grep -r "console.log" src/ --exclude-dir=tests; then
  echo "❌ 错误：源代码中发现 console.log"
  exit 1
fi

# 检查 TODO 注释（只警告，不阻止）
if grep -r "TODO:" src/; then
  echo "⚠️  警告：发现 TODO 注释（未阻止）"
fi

exit 0
```

### 模式 2：提交后通知

提交成功后：

```bash
#!/bin/bash
# Hook: notify-team.sh
# 某些类型的提交后通知团队

COMMIT_MSG=$(git log -1 --pretty=%B)

# 如果是安全相关提交
if echo "$COMMIT_MSG" | grep -i "security"; then
  echo "🔐 安全提交：$COMMIT_MSG"
  # 发送到 Slack（可选）
  # curl -X POST $SLACK_WEBHOOK -d "Security update: $COMMIT_MSG"
fi

exit 0
```

### 模式 3：依赖检查

如果依赖需要更新，发出警告：

```bash
#!/bin/bash
# Hook: check-deps.sh
# 检查 package.json 变化后是否更新了锁文件

FILES=$(git diff --cached --name-only)

if echo "$FILES" | grep -q "package.json"; then
  if ! echo "$FILES" | grep -q "package-lock.json"; then
    echo "⚠️  警告：package.json 变了但没有更新锁文件"
    echo "执行：npm install"
  fi
fi

exit 0
```

---

## 注册钩子

钩子在 `.claude/settings.json` 中注册：

```json
{
  "hooks": {
    "pre_commit": ["validate-version.sh", "security-check.sh"],
    "post_commit": ["notify-team.sh"],
    "post_push": ["deploy-staging.sh"]
  }
}
```

或者在 `settings.yaml` 中：

```yaml
hooks:
  pre_commit:
    - path: hooks/validate-version.sh
      description: "检查 VERSION 文件是否已更新"
      blocking: true
    - path: hooks/security-check.sh
      blocking: true
  post_commit:
    - path: hooks/notify-team.sh
      blocking: false
```

---

## 安全钩子的最佳实践

### 应该

✅ 让钩子**幂等**（多次执行也安全）
✅ 记录钩子在做什么
✅ 给出清晰的错误信息再退出
✅ 顶部加 `set -e`，遇到第一个错误就退出
✅ 让钩子可执行：`chmod +x hook.sh`

### 不应该

❌ 让钩子耗时 >5 秒（会阻塞工作流）
❌ 让钩子做网络调用（不可靠）
❌ 让钩子修改文件（它们只做验证）
❌ 让钩子过于严格（会激怒开发者）
❌ 忘记先在本地测试钩子

---

## 安全钩子模板

```bash
#!/bin/bash
set -euo pipefail

# 安全、清晰的自动化钩子模板

HOOK_NAME="my-hook"
HOOK_VERSION="1.0.0"

# 输出颜色
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # 无色

log_error() {
  echo -e "${RED}❌ $1${NC}"
}

log_warn() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# 主要验证逻辑
main() {
  echo "正在执行：$HOOK_NAME（$HOOK_VERSION）"
  
  # 你的检查在这里
  if some_check_fails; then
    log_error "检查未通过，原因：X"
    return 1
  fi
  
  log_success "所有检查通过"
  return 0
}

# 执行并退出
main
exit $?
```

---

## 练习：创建一个验证钩子

### 场景

你想阻止意外的提交，规则如下：
- 行尾有空白字符
- 新增代码缺少测试文件
- 未解决的合并冲突

### 第一步：创建钩子

```bash
cat > .claude/hooks/pre-commit-validation.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo "🔍 正在执行提交前验证..."

# 检查 1：没有行尾空白
if git diff --cached | grep -E '^[+].*\s+$' > /dev/null; then
  echo "❌ 发现行尾空白："
  git diff --cached | grep -E '^[+].*\s+$'
  exit 1
fi

# 检查 2：没有合并冲突标记
if git diff --cached | grep -E '^[+].*<<<<<<|^[+].*======|^[+].*>>>>>>' > /dev/null; then
  echo "❌ 发现合并冲突标记"
  exit 1
fi

# 检查 3：新增文件应该有测试
STAGED_FILES=$(git diff --cached --name-only)
for file in $STAGED_FILES; do
  if [[ $file == src/*.ts && $file != *test* ]]; then
    TEST_FILE="${file%.ts}.test.ts"
    if ! git ls-files | grep -q "$TEST_FILE"; then
      echo "⚠️  警告：新文件 $file 没有对应的测试文件"
    fi
  fi
done

echo "✅ 提交前验证通过"
exit 0
EOF

chmod +x .claude/hooks/pre-commit-validation.sh
```

### 第二步：在 settings.json 中注册

```json
{
  "hooks": {
    "pre_commit": ["hooks/pre-commit-validation.sh"]
  }
}
```

### 第三步：测试它

创建一个带行尾空格的文件：

```bash
echo "test line   " > test.txt  # 注意末尾的空格
git add test.txt
```

尝试提交：

```bash
git commit -m "Test hook"
```

钩子会阻止：

```
❌ 发现行尾空白：
+test line
```

### 第四步：修复重试

```bash
echo "test line" > test.txt  # 移除行尾空格
git add test.txt
git commit -m "Test hook (fixed)"
```

现在成功了：

```
✅ 提交前验证通过
```

---

## 调试钩子

如果钩子莫名其妙地失败：

1. **手动运行**：
```bash
bash .claude/hooks/my-hook.sh
```

2. **添加调试输出**：
```bash
set -x  # 打印每条命令
```

3. **检查退出码**：
```bash
bash .claude/hooks/my-hook.sh; echo "Exit: $?"
```

4. **测试钩子条件**：
```bash
# 测试某个文件是否被修改
git diff --cached --name-only | grep "VERSION"
echo $?  # 0 = 找到了，1 = 没找到
```

---

## 验证：完成本模块的标志

✓ 你至少创建了一个钩子脚本

✓ 你理解钩子事件类型（pre-commit、post-commit 等）

✓ 你能在 settings.json 或 settings.yaml 中注册钩子

✓ 你在本地测试过一个钩子

✓ 你知道退出码的含义（0 = 成功，1 = 失败）

---

## 下一步

**模块 07：进阶模式**讲的是：
- 多智能体编排
- 构建复杂工作流
- 错误处理和恢复
- 生产级自动化
- 团队协作模式

这教你如何把前面所有概念组合成复杂的多智能体系统。

---

**已完成模块 06？** → 准备进入模块 07：进阶模式
