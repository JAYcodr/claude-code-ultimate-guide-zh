---
title: "TTS 设置工作流 - Agent Vibes 安装"
description: "在 macOS 上为 Claude Code 添加文字转语音朗读"
tags: [workflow, tts, tutorial]
---

# TTS 设置工作流 - Agent Vibes 安装

**目标**：为 Claude Code 添加文字转语音朗读
**时间**：18 分钟
**难度**：中级
**系统**：macOS（需要 Homebrew）

---

## 决策点：你应该安装 TTS 吗？

使用这个快速评估：

| 问题 | 回答 | 分数 |
|----------|--------|-------|
| 你做长代码评审吗？ | 是 | +2 |
| 你在调试时多任务吗？ | 是 | +2 |
| 你喜欢音频通知吗？ | 是 | +1 |
| 你需要离线 TTS（无云）吗？ | 是 | +2 |
| 延迟关键（需要 <100ms）吗？ | 是 | -2 |
| 你在公共场所工作（不能音频）吗？ | 是 | -3 |
| 你喜欢安静的工作环境吗？ | 是 | -2 |

**分数**：
- **≥3**：安装 TTS（适合）
- **0-2**：可选（试试，可以卸载）
- **<0**：跳过 TTS（不适合）

---

## 工作流概述

```
阶段 1: 先决条件（5 分钟）
    ↓
阶段 2: Agent Vibes 安装（5 分钟）
    ↓
阶段 3: Piper TTS + 语音（5 分钟）
    ↓
阶段 4: 测试和配置（3 分钟）
    ↓
阶段 5: 验证（1 分钟）
```

---

## 阶段 1：先决条件（5 分钟）

### 检查点 1.1：系统要求

```bash
# 验证 macOS 版本
sw_vers
# 要求：macOS 10.15+

# 验证 Homebrew
brew --version
# 如果缺失：/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 验证 Node.js
node --version
# 要求：16.0.0+
```

### 检查点 1.2：安装 Bash 5.x

```bash
# 安装
brew install bash

# 验证
/opt/homebrew/bin/bash --version
# 预期：GNU bash, version 5.x

# ✅ 检查点：Bash 5.x 已安装
```

### 检查点 1.3：安装依赖

```bash
# 安装音频工具
brew install sox ffmpeg util-linux espeak-ng

# 验证所有已安装
command -v sox && command -v ffmpeg && command -v espeak-ng && echo "✅ Dependencies OK"

# ✅ 检查点：依赖已安装
```

**阶段 1 总时间**：约 5 分钟

---

## 阶段 2：Agent Vibes 安装（5 分钟）

### 步骤 2.1：启动安装程序

```bash
# 导航到你的项目
cd /path/to/your/claude-project

# 启动交互式安装程序
npx agentvibes install
```

**预期**：ASCII banner + 4 页交互式安装程序

### 步骤 2.2：导航页面

**页面 1/4 - 依赖**：
- 审查：应该显示所有 ✓ 绿色勾选
- 操作：点击"下一步 →"

**页面 2/4 - 提供者**：
- **选择**：`Piper TTS`（最佳质量，离线）
- 操作：点击"下一步 →"

**页面 3/4 - 语音**：
- **法语**：选择 `fr_FR-tom-medium`（男声，专业）
- **英语**：选择 `en_US-ryan-high`（最佳质量）
- 操作：点击"下一步 →"

**页面 4/4 - 设置**：
- **混响**：`轻`（推荐）
- **背景音乐**：`禁用`（避免分心）
- **详细程度**：`低`（更少唠叨）
- 操作：点击"开始安装"

### 检查点 2.3：验证安装

```bash
# 检查已安装的文件
ls .claude/hooks/play-tts.sh
ls .claude/commands/agent-vibes/
cat .claude/tts-provider.txt
# 预期：文件存在，提供者显示 "macos" 或 "piper"

# ✅ 检查点：Agent Vibes 已安装
```

**阶段 2 总时间**：约 5 分钟

---

## 阶段 3：Piper TTS + 法语语音（5 分钟）

### 步骤 3.1：通过 pipx 安装 Piper

```bash
# 安装 Piper TTS
pipx install piper-tts

# 验证
piper --help
# 预期：Piper 使用说明

# ✅ 检查点：Piper 已安装
```

### 步骤 3.2：下载法语语音

```bash
# 创建语音目录
mkdir -p ~/.claude/piper-voices
cd ~/.claude/piper-voices

# 下载法语男声（推荐）
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"

# 下载法语女声（可选）
curl -L -o fr_FR-siwis-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx"
curl -L -o fr_FR-siwis-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"

# ✅ 检查点：语音已下载（约 120MB）
```

**阶段 3 总时间**：约 5 分钟

---

## 阶段 4：配置和测试（3 分钟）

### 步骤 4.1：配置提供者和语音

```bash
# 设置 Piper 作为提供者
echo "piper" > .claude/tts-provider.txt

# 设置法语男声
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# 验证配置
cat .claude/tts-provider.txt  # 预期：piper
cat .claude/tts-voice.txt     # 预期：fr_FR-tom-medium

# ✅ 检查点：配置已设置
```

### 步骤 4.2：测试音频管道

```bash
# 直接测试 Piper
echo "Bonjour, je suis Claude et je parle français" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test-fr.wav && afplay /tmp/test-fr.wav

# 测试 TTS 钩子
~/.claude/hooks/play-tts.sh "Ceci est un test audio"

# ✅ 检查点：音频工作
```

**预期**：你应该听到法语男声。

**阶段 4 总时间**：约 3 分钟

---

## 阶段 5：Claude Code 中验证（1 分钟）

### 步骤 5.1：启动并测试

```bash
# 启动 Claude Code
claude

# 在 Claude 中运行：
/agent-vibes:whoami
# 预期：显示 "piper" 提供者和 "fr_FR-tom-medium" 语音

# 测试简单请求
> "Dis-moi bonjour en français"
# 预期：法语男声音频响应

# ✅ 检查点：TTS 在 Claude Code 中激活
```

### 步骤 5.2：配置偏好

```bash
# 降低详细程度（推荐）
/agent-vibes:verbosity low

# 如果命令杂乱则隐藏 34 个命令
/agent-vibes:hide

# ✅ 检查点：偏好已设置
```

**阶段 5 总时间**：约 1 分钟

---

## 总时间：约 18 分钟 ✅

---

## 安装后建议

### 针对你的工作流优化

**用于代码评审**：
```bash
/agent-vibes:verbosity low
/agent-vibes:effects off
```

**用于专注工作**：
```bash
/agent-vibes:mute  # 临时静音
# 无音频工作
/agent-vibes:unmute  # 完成后再启用
```

**用于电池优化**：
```bash
# 切换到 macOS Say（即时，无 CPU 峰值）
/agent-vibes:provider switch macos
```

### 添加到 .gitignore

```bash
# 防止提交大音频文件
echo ".claude/audio/" >> .gitignore
echo ".claude/piper-voices/" >> .gitignore
echo "*.wav" >> .gitignore
echo "*.onnx" >> .gitignore
```

---

## 故障排除快速参考

| 问题 | 快速修复 |
|-------|-----------|
| 无音频 | 检查 `cat .claude/tts-provider.txt` |
| 错误语音 | 运行 `/agent-vibes:switch fr_FR-tom-medium` |
| 太唠叨 | 运行 `/agent-vibes:verbosity low` |
| 命令杂乱 | 运行 `/agent-vibes:hide` |

**完整故障排除**：[Agent Vibes 故障排除](../../examples/integrations/agent-vibes/troubleshooting.md)

---

## 下一步

- **[语音目录](../../examples/integrations/agent-vibes/voice-catalog.md)** - 探索 15 种语音
- **[集成指南](../../examples/integrations/agent-vibes/README.md)** - 学习命令
- **[安装详情](../../examples/integrations/agent-vibes/installation.md)** - 深入了解

---

## 卸载说明

完全移除 Agent Vibes：

```bash
# 自动卸载
npx agentvibes uninstall --yes

# 手动清理（如需要）
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/
rm -rf ~/.claude/piper-voices/
pipx uninstall piper-tts
```

---

*工作流指南由 [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) 维护*
*最后更新：2026-01-22 | Agent Vibes v3.0.0*