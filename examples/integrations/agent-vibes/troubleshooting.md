---
title: "故障排查"
description: "Agent Vibes 常见问题与解决方案 — 音频、语音、集成和性能问题"
tags: [integration, voice, troubleshooting, support]
---

# 故障排查

本文档提供 Agent Vibes 常见问题的解决方案。

## 快速诊断

运行诊断命令以识别常见问题：

```bash
# 运行完整诊断
agent-vibes diagnose

# 仅检查音频
agent-vibes diagnose --audio

# 仅检查语音
agent-vibes diagnose --voice

# 仅检查集成
agent-vibes diagnose --integration
```

## 常见问题

### 1. 无音频输出

**症状**：Agent Vibes 运行但无声音输出。

**解决方案**：

1. **检查音量设置**：

   ```bash
   # 检查 Agent Vibes 音量
   agent-vibes config get volume

   # 设置音量
   agent-vibes config set volume 0.8
   ```

2. **检查系统音频**：

   ```bash
   # 测试系统音频
   agent-vibes test-system-audio
   ```

3. **检查音频设备**：

   ```bash
   # 列出音频设备
   agent-vibes list-audio-devices

   # 设置音频设备
   agent-vibes config set audio-device "设备名称"
   ```

4. **检查权限**（macOS）：
   - 系统偏好 → 安全性与隐私 → 麦克风
   - 系统偏好 → 安全性与隐私 → 辅助功能

5. **检查 PulseAudio**（Linux）：

   ```bash
   # 检查 PulseAudio 是否运行
   pulseaudio --check

   # 启动 PulseAudio
   pulseaudio --start

   # 检查音量控制
   pavucontrol
   ```

### 2. 语音质量差

**症状**：语音输出模糊、断断续续或语速异常。

**解决方案**：

1. **调整语音设置**：

   ```bash
   # 调整语速
   agent-vibes config set rate 1.0

   # 调整音调
   agent-vibes config set pitch 1.0

   # 尝试不同声音
   agent-vibes config set voice "en-US-GuyNeural"
   ```

2. **检查网络连接**：

   ```bash
   # 测试网络连接
   agent-vibes test-network

   # 启用缓存以减少网络依赖
   agent-vibes config set cache-enabled true
   ```

3. **调整音频质量**：

   ```bash
   # 降低质量以提升性能
   agent-vibes config set audio-quality "medium"

   # 启用流式传输
   agent-vibes config set streaming true
   ```

### 3. 音效缺失或延迟

**症状**：音效未播放或延迟明显。

**解决方案**：

1. **检查音效设置**：

   ```bash
   # 启用音效
   agent-vibes config set sounds.enabled true

   # 设置音效音量
   agent-vibes config set sounds.volume 0.6

   # 预加载音效
   agent-vibes config set sounds.preload true
   ```

2. **检查音效文件**：

   ```bash
   # 验证音效文件
   agent-vibes verify-sounds

   # 重新下载音效
   agent-vibes sounds download
   ```

3. **调整性能设置**：

   ```bash
   # 减少音效延迟
   agent-vibes config set performance.sound-delay 0

   # 启用音效缓存
   agent-vibes config set performance.sound-cache true
   ```

### 4. 与 Claude Code 集成失败

**症状**：Agent Vibes 未在 Claude Code 中激活。

**解决方案**：

1. **检查集成设置**：

   ```bash
   # 检查 Claude Code 配置
   claude config get agent-vibes

   # 启用集成
   claude config set agent-vibes.enabled true
   ```

2. **检查权限**：

   ```bash
   # 检查 Claude Code 权限
   claude config get permissions

   # 添加 Agent Vibes 权限
   claude config set permissions.allow "Bash(agent-vibes:*)"
   ```

3. **验证连接**：

   ```bash
   # 测试连接
   agent-vibes test-claude-connection

   # 检查 Claude Code 版本
   claude --version
   ```

4. **重启 Claude Code**：

   ```bash
   # 退出 Claude Code
   exit

   # 重新启动
   claude
   ```

### 5. 高 CPU 或内存使用

**症状**：Agent Vibes 占用过多系统资源。

**解决方案**：

1. **调整性能设置**：

   ```bash
   # 降低 CPU 使用
   agent-vibes config set performance.cpu-limit 50

   # 限制内存使用
   agent-vibes config set performance.memory-limit 256

   # 减少缓存大小
   agent-vibes config set performance.cache-size 50
   ```

2. **禁用非必要功能**：

   ```bash
   # 禁用背景氛围
   agent-vibes config set ambient.enabled false

   # 禁用音效
   agent-vibes config set sounds.enabled false

   # 减少语音质量
   agent-vibes config set voice.quality "low"
   ```

3. **检查并发使用**：

   ```bash
   # 限制并发语音请求
   agent-vibes config set performance.max-concurrent 1

   # 启用请求队列
   agent-vibes config set performance.queue-enabled true
   ```

### 6. 网络连接问题

**症状**：语音合成失败，网络错误。

**解决方案**：

1. **检查网络连接**：

   ```bash
   # 测试网络连接
   agent-vibes test-network

   # 检查代理设置
   agent-vibes config get network.proxy
   ```

2. **配置代理**：

   ```bash
   # 设置 HTTP 代理
   agent-vibes config set network.proxy "http://proxy.example.com:8080"

   # 设置 HTTPS 代理
   agent-vibes config set network.proxy-https "https://proxy.example.com:8080"

   # 设置不代理的地址
   agent-vibes config set network.no-proxy "localhost,127.0.0.1"
   ```

3. **使用离线模式**：

   ```bash
   # 启用离线模式
   agent-vibes config set network.offline true

   # 使用本地 TTS 引擎
   agent-vibes config set engine "local"
   ```

### 7. 安装问题

**症状**：安装失败或无法启动。

**解决方案**：

1. **检查依赖**：

   ```bash
   # 检查 Node.js 版本
   node --version

   # 检查 npm 版本
   npm --version

   # 检查系统依赖
   agent-vibes check-dependencies
   ```

2. **重新安装**：

   ```bash
   # 卸载
   npm uninstall -g agent-vibes

   # 清理缓存
   npm cache clean --force

   # 重新安装
   npm install -g agent-vibes
   ```

3. **使用二进制版本**：

   ```bash
   # 下载二进制文件（无需 Node.js）
   # 详见安装指南
   ```

### 8. 特定平台问题

#### macOS

**问题**：权限问题。

**解决方案**：

```bash
# 重置权限
sudo tccutil reset Microphone
sudo tccutil reset Accessibility

# 重新授予权限
# 系统偏好 → 安全性与隐私 → 麦克风
# 系统偏好 → 安全性与隐私 → 辅助功能
```

**问题**：音频设备切换。

**解决方案**：

```bash
# 设置默认音频设备
agent-vibes config set audio-device "内置输出"

# 或使用系统默认
agent-vibes config set audio-device "default"
```

#### Windows

**问题**：Windows 语音运行时缺失。

**解决方案**：

```powershell
# 安装 Windows 语音运行时
Add-WindowsCapability -Online -Name Language.Speech~en-US~0.0.1.0

# 重启 Agent Vibes
Restart-Service agent-vibes
```

**问题**：音频服务问题。

**解决方案**：

```powershell
# 重启音频服务
Restart-Service Audiosrv

# 检查音频设备
Get-PnpDevice -Class AudioEndpoint
```

#### Linux

**问题**：PulseAudio 问题。

**解决方案**：

```bash
# 重启 PulseAudio
pulseaudio -k
pulseaudio --start

# 检查 PulseAudio 状态
pactl info

# 设置默认接收器
pactl set-default-sink "alsa_output.pci-0000_00_1b.0.analog-stereo"
```

**问题**：ALSA 权限问题。

**解决方案**：

```bash
# 添加用户到音频组
sudo usermod -a -G audio $USER

# 注销并重新登录
# 或重启
```

### 9. 高级问题

#### 语音合成失败

**解决方案**：

```bash
# 检查语音服务状态
agent-vibes status voice

# 切换语音引擎
agent-vibes config set engine "azure"  # 或 "openai", "elevenlabs", "local"

# 检查 API 密钥
agent-vibes config get azure.speech-key
agent-vibes config get openai.api-key
agent-vibes config get elevenlabs.api-key
```

#### 音效文件损坏

**解决方案**：

```bash
# 验证音效文件
agent-vibes verify-sounds

# 重新下载音效
agent-vibes sounds download --force

# 使用自定义音效
agent-vibes config set sounds.effects.toolCall "custom/tool-call.mp3"
```

#### 配置冲突

**解决方案**：

```bash
# 备份当前配置
agent-vibes config backup

# 重置为默认配置
agent-vibes config reset

# 恢复配置
agent-vibes config restore
```

## 调试模式

启用调试模式以获取详细信息：

```bash
# 启用调试日志
agent-vibes config set debug true

# 设置详细级别
agent-vibes config set log-level "debug"

# 查看日志
agent-vibes logs

# 实时跟踪日志
agent-vibes logs --follow

# 导出日志
agent-vibes logs --export > debug.log
```

## 日志文件位置

| 平台    | 日志文件位置                                      |
| ------- | ------------------------------------------------- |
| macOS   | `~/Library/Logs/agent-vibes/agent-vibes.log`      |
| Linux   | `~/.local/share/agent-vibes/logs/agent-vibes.log` |
| Windows | `%APPDATA%\agent-vibes\logs\agent-vibes.log`      |

## 错误代码

| 错误代码               | 说明         | 解决方案              |
| ---------------------- | ------------ | --------------------- |
| `ERR_AUDIO_DEVICE`     | 音频设备问题 | 检查音频设备设置      |
| `ERR_AUDIO_PERMISSION` | 音频权限问题 | 授予音频权限          |
| `ERR_VOICE_SYNTHESIS`  | 语音合成失败 | 检查语音引擎设置      |
| `ERR_NETWORK`          | 网络连接问题 | 检查网络连接和代理    |
| `ERR_CONFIG`           | 配置问题     | 验证配置文件          |
| `ERR_INTEGRATION`      | 集成问题     | 检查 Claude Code 集成 |
| `ERR_PERFORMANCE`      | 性能问题     | 调整性能设置          |
| `ERR_DEPENDENCY`       | 依赖问题     | 检查系统依赖          |

## 获取帮助

### 自助排查

1. **运行诊断**：

   ```bash
   agent-vibes diagnose --all
   ```

2. **检查状态**：

   ```bash
   agent-vibes status --all
   ```

3. **查看文档**：

   ```bash
   agent-vibes docs
   ```

### 社区支持

- [GitHub Issues](https://github.com/your-org/agent-vibes/issues)
- [Discord](https://discord.gg/agent-vibes)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/agent-vibes)

### 报告问题

报告问题时请包含：

1. **Agent Vibes 版本**：

   ```bash
   agent-vibes --version
   ```

2. **系统信息**：

   ```bash
   agent-vibes system-info
   ```

3. **错误日志**：

   ```bash
   agent-vibes logs --last 100
   ```

4. **配置信息**（敏感信息已脱敏）：

   ```bash
   agent-vibes config show --safe
   ```

## 预防措施

### 定期维护

```bash
# 清理缓存
agent-vibes cache clean

# 更新音效
agent-vibes sounds update

# 检查更新
agent-vibes update check

# 备份配置
agent-vibes config backup
```

### 性能优化

```bash
# 优化设置
agent-vibes optimize

# 监控性能
agent-vibes monitor

# 生成报告
agent-vibes report
```

### 安全最佳实践

```bash
# 保护 API 密钥
agent-vibes config secure

# 审核权限
agent-vibes audit

# 检查漏洞
agent-vibes security-check
```

## 已知问题

### 1. macOS Ventura 及更高版本

**问题**：辅助功能权限需要手动授予。

**解决方案**：首次运行时在系统提示中授予权限。

### 2. Windows 11 22H2

**问题**：音频服务偶尔崩溃。

**解决方案**：更新音频驱动或使用 WASAPI 模式。

### 3. Ubuntu 22.04

**问题**：PipeWire 与 PulseAudio 冲突。

**解决方案**：使用 PipeWire 兼容模式或切换回 PulseAudio。

### 4. 网络限制环境

**问题**：语音合成需要互联网连接。

**解决方案**：使用本地 TTS 引擎或配置代理。

## 更新日志

查看 [CHANGELOG.md](https://github.com/your-org/agent-vibes/blob/main/CHANGELOG.md) 获取已知问题的修复信息。

---

_遇到未列出的问题？请[提交 Issue](https://github.com/your-org/agent-vibes/issues) 并提供详细信息。_
