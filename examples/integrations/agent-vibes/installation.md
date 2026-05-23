---
title: "安装指南"
description: "Agent Vibes 安装指南 — macOS、Windows、Linux 的逐步设置说明"
tags: [integration, voice, installation, setup]
---

# 安装指南

本文档提供 Agent Vibes 的逐步安装说明。

## 系统要求

### 最低要求

| 组件     | 最低要求                              |
| -------- | ------------------------------------- |
| 操作系统 | macOS 12+、Windows 10+、Ubuntu 20.04+ |
| CPU      | 双核处理器，2.0 GHz                   |
| 内存     | 4 GB RAM                              |
| 存储     | 500 MB 可用空间                       |
| 网络     | 语音合成需要互联网连接                |
| Node.js  | 18.0+                                 |
| npm      | 9.0+                                  |

### 推荐配置

| 组件     | 推荐配置                             |
| -------- | ------------------------------------ |
| 操作系统 | macOS 14+、Windows 11、Ubuntu 22.04+ |
| CPU      | 四核处理器，3.0 GHz                  |
| 内存     | 8 GB RAM                             |
| 存储     | 1 GB 可用空间（用于缓存）            |
| 网络     | 宽带互联网连接                       |
| Node.js  | 20.0 LTS                             |
| npm      | 10.0+                                |

## 安装方法

### 方法 1：NPM（推荐）

```bash
# 全局安装
npm install -g agent-vibes

# 验证安装
agent-vibes --version
```

### 方法 2：从源码安装

```bash
# 克隆仓库
git clone https://github.com/your-org/agent-vibes.git
cd agent-vibes

# 安装依赖
npm install

# 构建
npm run build

# 链接（用于开发）
npm link
```

### 方法 3：二进制文件（无需 Node.js）

**macOS**：

```bash
# 下载二进制文件
curl -L https://github.com/your-org/agent-vibes/releases/latest/download/agent-vibes-darwin-x64 -o agent-vibes

# 移动至 PATH 路径
mv agent-vibes /usr/local/bin/
chmod +x /usr/local/bin/agent-vibes
```

**Windows**：

```powershell
# 下载二进制文件
Invoke-WebRequest -Uri "https://github.com/your-org/agent-vibes/releases/latest/download/agent-vibes-win-x64.exe" -OutFile "agent-vibes.exe"

# 移动至 PATH 路径
Move-Item agent-vibes.exe "C:\Windows\System32\"
```

**Linux**：

```bash
# 下载二进制文件
wget https://github.com/your-org/agent-vibes/releases/latest/download/agent-vibes-linux-x64

# 移动至 PATH 路径
mv agent-vibes-linux-x64 /usr/local/bin/agent-vibes
chmod +x /usr/local/bin/agent-vibes
```

## 平台特定设置

### macOS

1. **授予麦克风权限**：
   系统偏好 → 安全性与隐私 → 麦克风 → 添加你的终端应用
2. **授予辅助功能权限**（音效所需）：
   系统偏好 → 安全性与隐私 → 辅助功能 → 添加你的终端应用

### Windows

1. **安装 Windows 语音运行时**：

   ```powershell
   # 检查是否已安装
   Get-WindowsCapability -Online | Where-Object Name -like 'Language.Speech*'

   # 必要时安装英语语音识别
   Add-WindowsCapability -Online -Name Language.Speech~en-US~0.0.1.0
   ```

2. **配置音频设备**：

   设置 → 系统 → 声音 → 选择默认输出设备

### Linux

1. **安装音频依赖**：

   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y libasound2-dev pulseaudio pavucontrol

   # Fedora
   sudo dnf install -y alsa-lib-devel pulseaudio pavucontrol

   # Arch
   sudo pacman -S alsa-lib pulseaudio pavucontrol
   ```

2. **配置 PulseAudio**：

   ```bash
   # 启动 PulseAudio（如未运行）
   pulseaudio --start

   # 打开音量控制
   pavucontrol
   ```

3. **设置音频组**（如有权限问题）：

   ```bash
   sudo usermod -a -G audio $USER
   # 注销并重新登录
   ```

## 配置

### 基本设置

```bash
# 初始化配置
agent-vibes init

# 交互式地选择设置和偏好
```

### 高级配置

```bash
# 直接编辑配置文件
agent-vibes config edit

# 设置特定值
agent-vibes config set voice "en-US-JennyNeural"
agent-vibes config set rate 1.2
agent-vibes config set volume 0.8

# 查看当前配置
agent-vibes config show
```

### 配置文件

配置文件位置：

- **macOS/Linux**：`~/.config/agent-vibes/config.json`
- **Windows**：`%APPDATA%\agent-vibes\config.json`

默认配置：

```json
{
  "voice": {
    "name": "en-US-JennyNeural",
    "rate": 1.0,
    "pitch": 1.0,
    "volume": 0.8
  },
  "sounds": {
    "enabled": true,
    "volume": 0.6,
    "effects": {
      "toolCall": "default",
      "success": "default",
      "error": "default",
      "notification": "default"
    }
  },
  "ambient": {
    "enabled": false,
    "type": "rain",
    "volume": 0.3
  },
  "performance": {
    "cacheEnabled": true,
    "cacheSize": 100,
    "preload": true,
    "minLength": 50
  }
}
```

## 与 Claude Code 集成

### 通过 CLI 启用

```bash
# 在 Claude Code 中启用 Agent Vibes
claude config set agent-vibes.enabled true

# 验证设置
claude config get agent-vibes
```

### 通过 settings.json 启用

在 `.claude/settings.json` 或 `~/.claude/settings.json` 中添加：

```json
{
  "permissions": {
    "allow": ["Bash(agent-vibes:*)"]
  },
  "agent-vibes": {
    "enabled": true,
    "voice": "en-US-JennyNeural",
    "rate": 1.0,
    "sounds": true,
    "ambient": false
  }
}
```

### 验证集成

```bash
# 测试安装
agent-vibes test

# 测试语音
agent-vibes test-voice

# 测试音效
agent-vibes test-sounds

# 测试氛围
agent-vibes test-ambient
```

## 可选依赖

### 语音引擎

Agent Vibes 默认使用 Azure Speech Services。你可以配置其他引擎：

**本地 TTS（离线）**：

```bash
# macOS（系统 TTS）
agent-vibes config set engine "macos-say"

# Windows（Windows 语音运行时）
agent-vibes config set engine "windows-sapi"

# Linux（espeak-ng）
sudo apt-get install espeak-ng
agent-vibes config set engine "espeak-ng"
```

**OpenAI TTS**：

```bash
# 设置 OpenAI API 密钥
export OPENAI_API_KEY="your-key"

# 配置 TTS
agent-vibes config set engine "openai"
agent-vibes config set openai-model "tts-1"
agent-vibes config set openai-voice "nova"
```

**ElevenLabs TTS**：

```bash
# 设置 ElevenLabs API 密钥
export ELEVENLABS_API_KEY="your-key"

# 配置 TTS
agent-vibes config set engine "elevenlabs"
agent-vibes config set elevenlabs-voice "21m00Tcm4TlvDq8ikWAM"
```

### 音效库

**内置音效**（默认）：
无需额外安装。

**自定义音效**：

```bash
# 创建音效目录
mkdir -p ~/.agent-vibes/sounds

# 添加音效文件
cp custom-sound.mp3 ~/.agent-vibes/sounds/

# 配置自定义音效
agent-vibes config set sounds.toolCall "custom-sound.mp3"
```

**外部音效包**：

```bash
# 从 URL 安装音效包
agent-vibes sounds install https://example.com/sound-pack.zip

# 列出已安装的音效包
agent-vibes sounds list

# 选择音效包
agent-vibes sounds use "pack-name"
```

## Docker 安装

### 使用 Docker

```bash
# 拉取镜像
docker pull agent-vibes/agent-vibes:latest

# 运行
docker run -d \
  --name agent-vibes \
  -p 3000:3000 \
  -v ~/.agent-vibes:/data \
  agent-vibes/agent-vibes:latest
```

### 使用 Docker Compose

```yaml
version: "3.8"
services:
  agent-vibes:
    image: agent-vibes/agent-vibes:latest
    container_name: agent-vibes
    ports:
      - "3000:3000"
    volumes:
      - ~/.agent-vibes:/data
    environment:
      - TTS_ENGINE=azure
      - AZURE_SPEECH_KEY=${AZURE_SPEECH_KEY}
      - AZURE_SPEECH_REGION=${AZURE_SPEECH_REGION}
    restart: unless-stopped
```

```bash
# 启动
docker-compose up -d

# 检查状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 环境变量

| 变量                     | 说明                | 默认值                          |
| ------------------------ | ------------------- | ------------------------------- |
| `AGENT_VIBES_HOME`       | 数据目录            | `~/.agent-vibes`                |
| `AGENT_VIBES_CONFIG`     | 配置文件路径        | `$AGENT_VIBES_HOME/config.json` |
| `AGENT_VIBES_LOG_LEVEL`  | 日志级别            | `info`                          |
| `AGENT_VIBES_CACHE_DIR`  | 缓存目录            | `$AGENT_VIBES_HOME/cache`       |
| `AGENT_VIBES_SOUNDS_DIR` | 音效目录            | `$AGENT_VIBES_HOME/sounds`      |
| `AZURE_SPEECH_KEY`       | Azure 语音密钥      | -                               |
| `AZURE_SPEECH_REGION`    | Azure 语音区域      | `eastus`                        |
| `OPENAI_API_KEY`         | OpenAI API 密钥     | -                               |
| `ELEVENLABS_API_KEY`     | ElevenLabs API 密钥 | -                               |

## 卸载

### 卸载 Agent Vibes

```bash
# 卸载 NPM 包
npm uninstall -g agent-vibes

# 删除数据目录
rm -rf ~/.agent-vibes

# 删除配置
# macOS/Linux
rm -rf ~/.config/agent-vibes

# Windows
Remove-Item -Recurse -Force "$env:APPDATA\agent-vibes"
```

### 从 Claude Code 断开

```bash
# 禁用集成
claude config set agent-vibes.enabled false

# 从 settings.json 中删除配置
claude config remove agent-vibes
```

### 清理残留文件

```bash
# 删除缓存
rm -rf ~/Library/Caches/agent-vibes  # macOS
rm -rf ~/.cache/agent-vibes         # Linux
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\agent-vibes"  # Windows

# 删除日志
rm -rf ~/Library/Logs/agent-vibes   # macOS
rm -rf ~/.local/share/agent-vibes/logs  # Linux
```

## 安装过程验证

```bash
# 运行验证脚本
agent-vibes verify

# 手动检查
agent-vibes --version          # 版本号
agent-vibes config show        # 配置
agent-vibes test-voice         # 语音
agent-vibes test-sounds        # 音效
agent-vibes test-ambient       # 氛围（如已启用）
```

## 下一步

- [基本用法](./usage.md)
- [故障排查](./troubleshooting.md)
- [语音目录](./voice-catalog.md)
- [配置参考](./configuration.md)

## 支持

安装遇到问题？请查看[故障排查指南](./troubleshooting.md)或[提交 Issue](https://github.com/your-org/agent-vibes/issues)。

---

_让 AI 交互更具氛围感 — 正确安装，尽享体验。_
