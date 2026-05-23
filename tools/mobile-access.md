# Claude Code 移动端访问

> **⚠️ 状态：进行中/未经测试**
>
> 本指南仍在编写中。该设置尚未在不同环境中得到充分测试。
> 请自行承担使用风险。欢迎贡献和反馈。

---

## 问题描述

Claude Code CLI 是一个**本地交互进程**，而非带有会话 API 的服务。每个实例都是独立的。即使是 `claude --remote` 也只是卸载执行——并不会创建中继系统。

**缺失的是什么**：一个原生的 `claude --serve` 模式，能够暴露 WebSocket API、允许多客户端、并保持同一会话上下文。

**变通方案**：使用 `ttyd` 通过网络浏览器暴露你的终端，并通过 `Tailscale` VPN 从任何地方访问。

---

## 解决方案：ttyd + Tailscale

```
YOUR COMPUTER                     YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │◄──────────────│  Browser        │
│  (runs here)    │   Tailscale   │  (same session) │
│                 │   (VPN)       │                 │
└─────────────────┘               └─────────────────┘
```

- **ttyd**：在网络浏览器中暴露你的终端
- **Tailscale**：免费 VPN，给你的电脑分配固定 IP，可从任何地方访问（4G、公共 WiFi 等）
- **tmux**：即使关闭浏览器也能保持会话存活

**使用场景**：从手机端跟踪和继续 Claude Code 会话（通勤途中、离开办公桌等）

---

## 架构对比

### ttyd + Tailscale（自托管）

```
YOUR COMPUTER                     YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │◄──────────────│  Browser        │
│  (runs here)    │   Tailscale   │  (same session) │
│  ┌───────────┐  │   VPN         │                 │
│  │   ttyd    │  │               └─────────────────┘
│  └───────────┘  │
└─────────────────┘
✅ ToS-Safe: CLI officiel, pas d'intermédiaire cloud
```

### Happy Coder（原生应用）

```
YOUR COMPUTER                     YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │               │  Happy App      │
│  (CLI officiel) │◄─────────────►│  (Expo native)  │
│       ▲         │   Local sync  │                 │
│  subprocess     │               └─────────────────┘
│  ┌───────────┐  │
│  │ Happy Hub │  │
│  └───────────┘  │
└─────────────────┘
✅ ToS-Safe: Wrapper local, subprocess Node.js
```

### Remoto.sh（云端中继）

```
REMOTO CLOUD                      YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Docker         │◄──────────────│  Browser        │
│  Container      │   WebSocket   │                 │
│  ┌───────────┐  │               └─────────────────┘
│  │ Claude    │  │
│  │ Code CLI  │  │
│  └───────────┘  │
└─────────────────┘
⚠️ ToS Risk: Cloud wrapping = potentiel "proxy non autorisé"
```

---

## 为什么选择此方案？

### 服务条款考量

一些第三方包装器（如 OpenCode）因违反服务条款而被 Anthropic 封禁。此方案是**符合服务条款安全**的，因为：

- 你使用的是**官方 Claude Code CLI**
- ttyd 仅通过网络浏览器暴露你的终端（无包装器）
- Tailscale 只是用于安全访问的 VPN
- 没有第三方客户端与 Claude 的 API 交互

---

## 前置要求

- macOS 或 Linux
- 已安装并认证的 Claude Code CLI
- Tailscale 账户（免费版即可）

---

## 安装

### 快速设置脚本

```bash
#!/bin/bash
# claude-mobile-setup.sh

set -e

echo "=== Setup Claude Code Mobile ==="

# 1. Install ttyd + tmux
echo "[1/2] Installing ttyd..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ttyd tmux
else
    sudo apt install -y tmux
    sudo snap install ttyd --classic
fi

# 2. Install Tailscale
echo "[2/2] Installing Tailscale..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install tailscale
else
    curl -fsSL https://tailscale.com/install.sh | sh
fi

# 3. Create launcher script
mkdir -p ~/.local/bin
cat > ~/.local/bin/claude-mobile << 'EOF'
#!/bin/bash
PORT=7681
PASS="${CLAUDE_MOBILE_PASS:-claude123}"

TS_IP=$(tailscale ip -4 2>/dev/null || echo "not connected")

echo "══════════════════════════════════"
echo "  CLAUDE CODE MOBILE"
echo "══════════════════════════════════"
echo "  URL:  http://$TS_IP:$PORT"
echo "  User: claude"
echo "  Pass: $PASS"
echo "══════════════════════════════════"
echo ""
echo "Open this URL on your phone."
echo "Press Ctrl+C to stop."
echo ""

# Kill existing session if any
tmux kill-session -t cc 2>/dev/null || true

# Start Claude in tmux, expose via ttyd
tmux new-session -d -s cc 'claude'
exec ttyd -W -p $PORT -c "claude:$PASS" tmux attach -t cc
EOF

chmod +x ~/.local/bin/claude-mobile

# Add to PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run: tailscale up"
echo "  2. Run: source ~/.zshrc"
echo "  3. Run: claude-mobile"
echo ""
```

### 手动安装

```bash
# macOS
brew install ttyd tmux tailscale

# Linux (Debian/Ubuntu)
sudo apt install -y tmux
sudo snap install ttyd --classic
curl -fsSL https://tailscale.com/install.sh | sh
```

---

## 使用方法

### 首次设置

```bash
# 1. Connect to Tailscale (one-time)
tailscale up
# Follow the link to authenticate with Google/GitHub/etc.

# 2. Install Tailscale on your phone
# iOS: App Store → Tailscale
# Android: Play Store → Tailscale
# Login with same account

# 3. Start Claude Code Mobile
claude-mobile
```

### 输出

```
══════════════════════════════════
  CLAUDE CODE MOBILE
══════════════════════════════════
  URL:  http://100.78.42.15:7681
  User: claude
  Pass: claude123
══════════════════════════════════
```

### 在手机上操作

1. 打开 Safari/Chrome
2. 访问 `http://100.78.42.15:7681`（使用你的实际 Tailscale IP）
3. 使用 `claude` / `claude123` 登录
4. 现在你的浏览器中已拥有 Claude Code

---

## 配置

### 修改密码

```bash
export CLAUDE_MOBILE_PASS="your-secure-password"
claude-mobile
```

Or add to your shell config:

```bash
echo 'export CLAUDE_MOBILE_PASS="your-secure-password"' >> ~/.zshrc
```

### 修改端口

编辑 `~/.local/bin/claude-mobile` 并将 `PORT=7681` 更改为你偏好的端口。

---

## 安全性

| 层面 | 保护措施 |
|------|----------|
| **网络** | Tailscale 使用 WireGuard 加密 |
| **认证** | 通过 ttyd 的基本认证（用户名:密码） |
| **访问控制** | 仅可从你的 Tailscale 网络访问 |

**建议**：
- 使用强密码（不要使用默认的 `claude123`）
- 不要在没有 Tailscale 的情况下直接将 ttyd 暴露在互联网上
- 在所有设备上保持 Tailscale 客户端更新

---

## 故障排除

### 显示"not connected"而非 IP

```bash
# Check Tailscale status
tailscale status

# If disconnected, reconnect
tailscale up
```

### 无法从手机访问

1. 确保手机已安装 Tailscale 应用并登录同一账户
2. 检查防火墙未阻止端口 7681
3. 先尝试本地访问：`http://localhost:7681`

### 会话未持久化

tmux 会话应该是持续存在的。如需手动重新连接：

```bash
tmux attach -t cc
```

### ttyd 命令未找到

```bash
# macOS
brew reinstall ttyd

# Linux
sudo snap install ttyd --classic
```

---

## 替代方案对比

| 方案 | 类型 | 优点 | 缺点 | 服务条款 | 星标 |
|------|------|------|------|---------|------|
| **ttyd + Tailscale** ✅ | 自托管 | 免费、最大控制、官方CLI | 手动设置、终端体验 | ✅ 安全 | N/A |
| [Happy Coder](https://github.com/slopus/happy) | 原生应用 | 语音、加密、多实例、移动优先 | 依赖第三方项目 | ✅ 安全 | 7.8K |
| [Remoto.sh](https://remoto.sh) | 云端中继 | 快速设置、仅浏览器 | 云端包装、延迟、成本 | ⚠️ 风险 | N/A |
| tmux + SSH | 自托管 | 零依赖、官方CLI | 需要移动SSH客户端 | ✅ 安全 | N/A |

我们选择 ttyd + Tailscale 是因为：
- 只是通过浏览器暴露你的终端
- 没有围绕 Claude Code 的第三方包装器
- 零服务条款风险——你使用的是官方 CLI

---

### Happy Coder - 推荐替代方案

Si vous préférez une **app native** plutôt qu'un terminal web :

- **Repo** : [github.com/slopus/happy](https://github.com/slopus/happy)
- **Stars** : 7.8K (janvier 2026)
- **License** : MIT
- **Stack** : Tauri (desktop) + Expo (mobile)
- **Providers** : Claude Code, Codex, Gemini

**Pourquoi ToS-safe** : Happy Coder est un wrapper local qui exécute le CLI officiel via subprocess Node.js. Pas d'appels API directs, pas de proxy cloud.

**Installation** :
```bash
npm i -g happy-coder && happy
```

---

### Remoto.sh - 云端替代方案（存在风险）

**Pourquoi risqué** : Remoto.sh utilise des conteneurs Docker cloud comme relay. Selon les ToS Anthropic (§4.2), les "proxies non autorisés qui masquent l'origine des requêtes" sont interdits. Des suspensions ont été signalées sur Reddit/HN pour usage similaire.

> **Recommandation** : Préférer Happy Coder ou ttyd+Tailscale pour éviter les risques ToS.

---

## 相关资源

- [ttyd GitHub](https://github.com/tsl0922/ttyd) - 网页终端服务器
- [Tailscale](https://tailscale.com/) - 零配置 VPN
- [ttyd + Claude Code 指南](https://aiengineerguide.com/blog/agentic-cli-browser-ttyd/) - 社区教程
- [VPS 设置指南](https://joshualent.com/snippets/claude-phone/) - 替代方案：在 VPS 上运行

---

## 来源

- [Happy Coder GitHub](https://github.com/slopus/happy) - 7.8K ⭐, MIT 许可证
- [ttyd GitHub](https://github.com/tsl0922/ttyd) - 网页终端服务器
- [Tailscale](https://tailscale.com/) - 零配置 VPN
- [Remoto.sh](https://remoto.sh) - 云终端（已注明的服务条款风险）
- ToS Anthropic §4.2 - Proxies non autorisés

---

## 贡献

本文档为**进行中/未经测试**。如果你测试了这个设置，请分享：
- 你的操作系统/环境
- 遇到的任何问题
- 建议的改进

在此仓库提交 issue 或 PR。

---

*最后更新：2026年1月 | 状态：进行中/未经测试 | 数据已验证：Happy Coder 7.8K ⭐ (2026-01-19)*
