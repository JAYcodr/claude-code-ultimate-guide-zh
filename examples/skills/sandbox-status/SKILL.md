---
name: sandbox-status
description: 显示原生沙箱状态、配置和最近违规
effort: low
disable-model-invocation: true
---

# 沙箱状态命令

检查原生 Claude Code 沙箱状态、活动配置和安全事件。

## 用法

```
/sandbox-status
```

## 功能

1. **检查沙箱可用性**
   - 验证 OS 原语是否安装（Linux 上为 bubblewrap，macOS 上为 Seatbelt）
   - 显示平台支持状态

2. **显示活动配置**
   - 沙箱模式（自动允许 vs 常规权限）
   - 文件系统策略（允许写入、拒绝读取）
   - 网络策略（域名允许列表/拒绝列表）
   - 排除的命令

3. **列出最近的沙箱违规**
   - 被阻止的文件系统访问尝试
   - 被阻止的网络连接
   - 逃生口调用（`dangerouslyDisableSandbox`）

## 实现

```bash
#!/bin/bash

echo "=== 原生沙箱状态 ==="
echo

# 1. 平台检查
echo "平台："
case "$OSTYPE" in
  darwin*)
    echo "  ✅ macOS（Seatbelt 内置）"
    ;;
  linux*)
    if which bubblewrap >/dev/null 2>&1; then
      echo "  ✅ Linux（bubblewrap 已安装）"
      bubblewrap --version 2>/dev/null | head -1
    else
      echo "  ❌ Linux（bubblewrap 未安装）"
      echo "     安装：sudo apt-get install bubblewrap socat"
    fi
    if which socat >/dev/null 2>&1; then
      echo "  ✅ socat 已安装"
    else
      echo "  ❌ socat 未安装"
    fi
    ;;
  *)
    echo "  ❌ 不支持的平台：$OSTYPE"
    ;;
esac
echo

# 2. 配置
echo "配置（来自 settings.json）："
if [ -f .claude/settings.json ]; then
  CONFIG=".claude/settings.json"
elif [ -f ~/.claude/settings.json ]; then
  CONFIG="~/.claude/settings.json"
else
  echo "  ⚠️  未找到 settings.json"
  CONFIG=""
fi

if [ -n "$CONFIG" ]; then
  echo "  来源：$CONFIG"

  # 自动允许模式
  AUTO_ALLOW=$(jq -r '.sandbox.autoAllowMode // "not set"' "$CONFIG" 2>/dev/null)
  echo "  自动允许：$AUTO_ALLOW"

  # 允许的写入路径
  WRITE_PATHS=$(jq -r '.sandbox.filesystem.allowedWritePaths[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  允许写入：${WRITE_PATHS:-未设置}"

  # 拒绝的读取路径
  DENIED_READS=$(jq -r '.sandbox.filesystem.deniedReadPaths[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  拒绝读取：${DENIED_READS:-未设置}"

  # 网络策略
  NET_POLICY=$(jq -r '.sandbox.network.policy // "not set"' "$CONFIG" 2>/dev/null)
  echo "  网络策略：$NET_POLICY"

  # 允许的域名
  DOMAINS=$(jq -r '.sandbox.network.allowedDomains[]? // empty' "$CONFIG" 2>/dev/null | head -3 | tr '\n' ', ')
  DOMAINS_COUNT=$(jq -r '.sandbox.network.allowedDomains | length' "$CONFIG" 2>/dev/null)
  if [ -n "$DOMAINS" ]; then
    echo "  允许的域名：$DOMAINS...（共 $DOMAINS_COUNT 个）"
  else
    echo "  允许的域名：未设置"
  fi

  # 排除的命令
  EXCLUDED=$(jq -r '.sandbox.excludedCommands[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  排除的命令：${EXCLUDED:-未设置}"
fi
echo

# 3. 最近违规（占位 - 实际实现应读取 Claude Code 日志）
echo "最近的沙箱违规："
echo "  ℹ️  日志检查尚未实现"
echo "  提示：检查 Claude Code 会话日志以获取沙箱违规通知"
echo

# 4. 开源运行时
echo "开源运行时："
if which npx >/dev/null 2>&1; then
  echo "  ✅ npx 可用 - 可使用 @anthropic-ai/sandbox-runtime"
  echo "  用法：npx @anthropic-ai/sandbox-runtime <command>"
else
  echo "  ⚠️  未找到 npx（安装 Node.js）"
fi
echo

# 5. 文档
echo "文档："
echo "  指南：guide/sandbox-native.md"
echo "  官方：https://code.claude.com/docs/en/sandboxing"
echo "  运行时：https://github.com/anthropic-experimental/sandbox-runtime"
```

## 示例输出

```
=== 原生沙箱状态 ===

平台：
  ✅ macOS（Seatbelt 内置）

配置（来自 settings.json）：
  来源：.claude/settings.json
  自动允许：true
  允许写入：${CWD}, /tmp
  拒绝读取：${HOME}/.ssh, ${HOME}/.aws, ${HOME}/.kube
  网络策略：deny
  允许的域名：api.anthropic.com, registry.npmjs.com, github.com...（共 9 个）
  排除的命令：docker, kubectl, podman

最近的沙箱违规：
  ℹ️  日志检查尚未实现
  提示：检查 Claude Code 会话日志以获取沙箱违规通知

开源运行时：
  ✅ npx 可用 - 可使用 @anthropic-ai/sandbox-runtime
  用法：npx @anthropic-ai/sandbox-runtime <command>

文档：
  指南：guide/sandbox-native.md
  官方：https://code.claude.com/docs/en/sandboxing
  运行时：https://github.com/anthropic-experimental/sandbox-runtime
```

## 用例

- **部署前**：在运行自主工作流前验证沙箱配置
- **调试**：调查为什么某些命令被阻止
- **安全审计**：审查允许的域名和文件系统访问
- **新人入职**：帮助新团队成员理解项目沙箱策略

## 另见

- [原生沙箱指南](../../guide/security/sandbox-native.md) — 完整技术参考
- [沙箱验证钩子](../hooks/bash/sandbox-validation.sh) — 命令前验证
- [沙箱配置示例](../config/sandbox-native.json) — 生产就绪设置


