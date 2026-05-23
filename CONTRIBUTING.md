# 为 Claude Code 终极指南做贡献

**欢迎！** 无论是修复拼写错误还是添加新章节，每一份贡献都能帮助全球开发者掌握 Claude Code。

## 快速链接

- [报告问题](../../issues/new)
- [发起讨论](../../discussions)
- [行为准则](./CODE_OF_CONDUCT.md)

---

## 贡献方式

| 类型         | 示例                    | 工作量     |
| ------------ | ----------------------- | ---------- |
| **报告**     | Bug、过期信息、失效链接 | 2 分钟     |
| **改进**     | 修复拼写、澄清说明      | 5-15 分钟  |
| **添加示例** | 新模板、工作流、钩子    | 15-60 分钟 |
| **翻译**     | 帮助非英语用户          | 不定       |
| **分享**     | 你的工作流、成功案例    | 5 分钟     |

**不确定从哪开始？** 查看 [标记为 `good first issue` 的问题](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)。

---

## 报告问题

发现了错误或有建议？

1. **搜索已有问题** — 可能已有人报告
2. **提交新问题**，包含：
   - 清晰描述
   - 位置（文件、章节、行号）
   - 你的平台（macOS/Linux/Windows）
   - Windows 用户：请注明 PowerShell 版本

---

## Pull Request 流程

### 1. Fork 和克隆

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-ultimate-guide.git
cd claude-code-ultimate-guide
```

### 2. 创建分支

```bash
git checkout -b fix/typo-in-section-3
# 或
git checkout -b feature/add-debugging-guide
```

### 2.5. 安装预提交钩子

本仓库使用预提交钩子强制质量门禁（Markdown 检查、YAML 验证、版本一致性等）。设置一次即可：

```bash
# macOS/Linux
pip install pre-commit
pre-commit install

# Windows (PowerShell)
pip install pre-commit
pre-commit install
```

之后每次 `git commit` 都会自动运行预提交。也可手动运行：

```bash
pre-commit run --all-files
```

**钩子的检查项：**

- ✓ Markdown 格式一致性
- ✓ YAML 语法有效性
- ✓ VERSION 文件跨仓库一致性
- ✓ 无断开的符号链接或敏感文件

### 3. 进行修改

遵循下方的 [内容指南](#内容指南)。

### 4. 测试你的修改

- 预览 Markdown 渲染效果
- 在你的平台上测试代码片段
- 验证所有链接可用

### 5. 提交 PR

包含：

- 清晰的变更描述
- 为什么需要此变更
- 你测试了什么

---

## 内容指南

### 写作风格

- **简洁**：列表项优于长段落
- **实用**：每个概念都附带示例
- **跨平台**：同时支持 macOS/Linux 和 Windows
- **准确**：提交前测试所有代码

### 文档结构

````markdown
## 章节标题

简要介绍（1-2 句）。

### 子章节

| 列 1 | 列 2 |
| ---- | ---- |
| 数据 | 数据 |

**示例：**

```bash
code example here
```
````

````

### 平台特定代码

当命令不同时，始终提供两个版本：

```bash
# macOS/Linux
~/.claude/settings.json

# Windows
%USERPROFILE%\.claude\settings.json
````

---

## 质量清单

提交前检查：

- [ ] Markdown 渲染正确（在 GitHub 上预览）
- [ ] 所有链接可用
- [ ] 代码片段在你的平台上已测试
- [ ] 已提供 Windows 等效方案（如适用）
- [ ] 已进行拼写检查
- [ ] 遵循现有风格

---

## Windows 贡献（尤其欢迎！）

维护者使用 macOS。如果你是 Windows 用户：

- 用 PS 5.1+ 测试 PowerShell 脚本
- 验证路径处理
- 报告 Windows 特有错误
- 尽可能添加批处理文件替代方案

**你的贡献尤其宝贵！**

---

## 我们不接受的内容

- 营销语言或推广内容
- 未经验证或推测性的声明
- 未经事先讨论的大规模结构变更
- 对现有示例的破坏性修改

---

## 认可

贡献者通过以下方式获得认可：

- **Git 历史** — 你的提交永久归属
- **GitHub 贡献者** — 在仓库页面可见

重大贡献可能会在发布说明中突出展示。

---

## 有问题？

- **一般问题**：[GitHub Discussions](../../discussions)
- **Bug 报告**：[Issues](../../issues)
- **直接联系**：[LinkedIn](https://www.linkedin.com/in/florian-bruniaux-43408b83/)

---

**感谢你帮助改进这份指南！**
