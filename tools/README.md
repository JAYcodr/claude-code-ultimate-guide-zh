# 交互工具

适用于 Claude Code 设置和优化的提示词与实用工具。

## 目录

| 文件 | 描述 | 用法 |
|------|------|------|
| [audit-prompt.md](./audit-prompt.md) | 全面的设置审计，含个性化建议 | `cat audit-prompt.md \| claude` |
| [spec-completeness-audit.md](./spec-completeness-audit.md) | 审计项目对安全AI代理委派的规范完备程度（5层规范，评分/100） | `cat spec-completeness-audit.md \| claude` |
| [onboarding-prompt.md](./onboarding-prompt.md) | 基于个人资料的个性化引导教程 | `cat onboarding-prompt.md \| claude` |
| [mobile-access.md](./mobile-access.md) | 通过 ttyd + Tailscale 实现移动端访问的设置指南 | 分步指南 |

## 快速审计

如需快速自动化扫描，请改用脚本：

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/scripts/audit-scan.sh | bash
```

---

*返回[主README](../README.md)*
