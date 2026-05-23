---
title: "Agent Vibes"
description: "Claude Code 的语音与音效集成，为 AI 交互增添氛围感"
tags: [integration, voice, audio, sound, vibes]
---

# Agent Vibes

为 Claude Code 添加语音与音效，让 AI 交互更具氛围感。

## 这是什么？

Agent Vibes 是一个 Claude Code 集成，为 AI 交互添加语音和音效：

- **语音输出**：Claude 的响应通过语音朗读
- **音效**：工具调用、成功、错误、通知等事件触发音效
- **氛围感**：为长时间工作会话提供背景音效
- **可定制**：选择不同声音、音效和音量设置

## 核心特性

| 特性       | 说明                                     |
| ---------- | ---------------------------------------- |
| 语音合成   | Claude 的响应通过高质量 TTS 朗读         |
| 事件音效   | 工具调用、成功、错误、通知等事件触发音效 |
| 背景氛围   | 可选的背景音效（雨声、咖啡馆、白噪音）   |
| 多语言支持 | 英语、法语、西班牙语、德语、日语等       |
| 可定制声音 | 选择不同声音、音调、语速                 |
| 音量控制   | 独立控制语音、音效和背景音的音量         |
| 平台支持   | macOS、Windows、Linux                    |

## 快速开始

1. 安装 Agent Vibes：

```bash
npm install -g agent-vibes
```

1. 在 Claude Code 中启用：

```bash
claude config set agent-vibes.enabled true
```

1. 启动 Claude Code：

```bash
claude
```

现在 Claude 的响应将通过语音朗读，事件会触发音效！

## 配置

### 声音设置

```bash
# 设置语音声音
claude config set agent-vibes.voice "en-US-JennyNeural"

# 设置语速
claude config set agent-vibes.rate 1.2

# 设置音调
claude config set agent-vibes.pitch 1.0

# 设置音量
claude config set agent-vibes.volume 0.8
```

### 音效设置

```bash
# 启用/禁用音效
claude config set agent-vibes.sound-effects true

# 设置音效音量
claude config set agent-vibes.sound-volume 0.6

# 自定义音效
claude config set agent-vibes.sound-tool-call "path/to/sound.mp3"
claude config set agent-vibes.sound-success "path/to/success.mp3"
claude config set agent-vibes.sound-error "path/to/error.mp3"
claude config set agent-vibes.sound-notification "path/to/notification.mp3"
```

### 背景氛围

```bash
# 启用背景氛围
claude config set agent-vibes.ambient-sounds true

# 选择氛围类型
claude config set agent-vibes.ambient-type "rain"

# 设置氛围音量
claude config set agent-vibes.ambient-volume 0.3
```

## 可用声音

### 英语声音

| 声音 ID             | 名称  | 性别 | 风格         |
| ------------------- | ----- | ---- | ------------ |
| `en-US-JennyNeural` | Jenny | 女   | 友好、清晰   |
| `en-US-GuyNeural`   | Guy   | 男   | 专业、权威   |
| `en-US-AriaNeural`  | Aria  | 女   | 温暖、热情   |
| `en-US-DavisNeural` | Davis | 男   | 冷静、沉稳   |
| `en-US-JaneNeural`  | Jane  | 女   | 活泼、有活力 |
| `en-US-JasonNeural` | Jason | 男   | 中性、平衡   |

### 其他语言

| 语言     | 声音 ID                | 名称   |
| -------- | ---------------------- | ------ |
| 法语     | `fr-FR-DeniseNeural`   | Denise |
| 西班牙语 | `es-ES-ElviraNeural`   | Elvira |
| 德语     | `de-DE-KatjaNeural`    | Katja  |
| 日语     | `ja-JP-NanamiNeural`   | 七海   |
| 韩语     | `ko-KR-SunHiNeural`    | 선희   |
| 中文     | `zh-CN-XiaoxiaoNeural` | 晓晓   |

## 可用音效

| 事件     | 默认音效            | 说明              |
| -------- | ------------------- | ----------------- |
| 工具调用 | `tool-call.mp3`     | Claude 调用工具时 |
| 成功     | `success.mp3`       | 工具执行成功时    |
| 错误     | `error.mp3`         | 工具执行失败时    |
| 通知     | `notification.mp3`  | Claude 发送通知时 |
| 会话开始 | `session-start.mp3` | 新会话开始时      |
| 会话结束 | `session-end.mp3`   | 会话结束时        |
| 思考     | `thinking.mp3`      | Claude 思考时     |

## 可用氛围

| 类型          | 说明       | 最佳场景   |
| ------------- | ---------- | ---------- |
| `rain`        | 雨声       | 专注、放松 |
| `cafe`        | 咖啡馆氛围 | 创意工作   |
| `white-noise` | 白噪音     | 消除干扰   |
| `forest`      | 森林音效   | 自然、平静 |
| `ocean`       | 海浪声     | 冥想、反思 |
| `fireplace`   | 壁炉声     | 舒适、温暖 |

## 使用场景

### 1. 编程助手

Claude 通过语音指导你完成复杂任务：

- 语音解释概念
- 朗读代码片段
- 提供逐步指导

### 2. 学习工具

通过语音增强学习体验：

- 朗读文档
- 解释复杂主题
- 提供听觉反馈

### 3. 无障碍访问

为视觉障碍用户提供支持：

- 屏幕阅读器替代方案
- 语音导航
- 听觉反馈

### 4. 多任务处理

在专注其他任务时听取 Claude 的响应：

- 编码时听取解释
- 设计时听取反馈
- 写作时听取建议

## 高级用法

### 自定义语音提示

```bash
# 在特定提示前添加语音指令
claude config set agent-vibes.voice-prefix "请用清晰、缓慢的语速朗读："

# 在特定提示后添加语音指令
claude config set agent-vibes.voice-suffix "朗读完毕。"
```

### 条件语音

```bash
# 仅在响应长度超过阈值时朗读
claude config set agent-vibes.min-length 100

# 仅在特定工具调用后朗读
claude config set agent-vibes.voice-after-tools "Read,Analyze,Explain"

# 排除特定内容类型
claude config set agent-vibes.exclude-patterns "代码块,表格,JSON"
```

### 音效规则

```bash
# 为特定工具设置自定义音效
claude config set agent-vibes.tool-sounds.Bash "path/to/bash.mp3"
claude config set agent-vibes.tool-sounds.Edit "path/to/edit.mp3"
claude config set agent-vibes.tool-sounds.Read "path/to/read.mp3"

# 基于工具结果设置音效
claude config set agent-vibes.result-sounds.success "path/to/success.mp3"
claude config set agent-vibes.result-sounds.error "path/to/error.mp3"
claude config set agent-vibes.result-sounds.warning "path/to/warning.mp3"
```

## 性能考量

### 资源使用

| 组件     | CPU 使用 | 内存使用 | 网络使用     |
| -------- | -------- | -------- | ------------ |
| 语音合成 | 中       | 中       | 低（缓存后） |
| 音效播放 | 低       | 低       | 无           |
| 背景氛围 | 低       | 低       | 无           |

### 优化建议

1. **启用缓存**：缓存语音输出以减少网络请求
2. **预加载音效**：启动时预加载常用音效
3. **调整质量**：降低语音质量以减少带宽使用
4. **限制频率**：设置最小响应长度以避免频繁语音

## 故障排查

### 常见问题

**Q: 没有声音输出**
A: 检查音量设置、音频设备连接和权限

**Q: 语音质量差**
A: 尝试不同声音、调整语速和音调

**Q: 音效延迟**
A: 预加载音效、检查网络连接

**Q: 背景音效干扰**
A: 降低氛围音量或禁用背景音效

### 调试模式

```bash
# 启用调试日志
claude config set agent-vibes.debug true

# 查看语音合成状态
claude config get agent-vibes.*

# 测试音效
agent-vibes test-sounds
```

## 与其他集成配合

### 与 MCP 服务器配合

```bash
# 启用 MCP 语音服务器
claude config set mcp.servers.voice.enabled true

# 配置语音 MCP 服务器
claude config set mcp.servers.voice.command "agent-vibes mcp-server"
```

### 与钩子配合

```bash
# 在钩子中触发音效
.claude/hooks/notification.sh:
#!/bin/bash
agent-vibes play-sound notification
```

### 与技能配合

```bash
# 在技能中启用语音
.claude/skills/my-skill/SKILL.md:
## 语音设置
voice_enabled: true
voice_style: "专业"
```

## 开发

### 架构

```
┌──────────────┐    HTTP/WebSocket    ┌──────────────┐
│ Claude Code  │ ───────────────────► │ Agent Vibes  │
│              │                      │  服务器      │
│  工具调用    │                      │              │
│  响应        │                      │ 语音合成     │
│  通知        │                      │ 音效播放     │
└──────────────┘                      │ 氛围控制     │
                                      └──────────────┘
```

### API 端点

| 端点            | 方法 | 说明           |
| --------------- | ---- | -------------- |
| `/speak`        | POST | 合成并播放语音 |
| `/play-sound`   | POST | 播放音效       |
| `/play-ambient` | POST | 播放背景氛围   |
| `/stop`         | POST | 停止所有播放   |
| `/status`       | GET  | 获取状态信息   |

### 扩展

创建自定义音效包：

```bash
# 创建音效包目录
mkdir -p ~/.agent-vibes/sounds/custom

# 添加音效文件
cp my-sound.mp3 ~/.agent-vibes/sounds/custom/

# 在配置中引用
claude config set agent-vibes.sound-tool-call "custom/my-sound.mp3"
```

创建自定义语音配置：

```bash
# 创建语音配置
cat > ~/.agent-vibes/voices/custom.json << EOF
{
  "name": "自定义声音",
  "voice": "en-US-CustomNeural",
  "rate": 1.0,
  "pitch": 1.0,
  "volume": 0.8
}
EOF

# 在配置中引用
claude config set agent-vibes.voice-config "custom"
```

## 贡献

欢迎贡献！请查看[贡献指南](CONTRIBUTING.md)。

### 开发设置

```bash
# 克隆仓库
git clone https://github.com/your-org/agent-vibes.git
cd agent-vibes

# 安装依赖
npm install

# 构建
npm run build

# 测试
npm test

# 本地运行
npm start
```

### 待办事项

- [ ] 更多语音选项
- [ ] 自定义音效库
- [ ] 语音命令
- [ ] 离线模式
- [ ] 移动端支持

## 许可证

MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 支持

- [文档](https://docs.agent-vibes.com)
- [GitHub Issues](https://github.com/your-org/agent-vibes/issues)
- [Discord](https://discord.gg/agent-vibes)
- [Twitter](https://twitter.com/agent_vibes)

---

_让 AI 交互更具氛围感_
