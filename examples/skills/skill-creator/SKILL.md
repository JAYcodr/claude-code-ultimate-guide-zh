---
name: skill-creator
description: "搭建新的 Claude Code 技能，包含 SKILL.md、YAML frontmatter 和捆绑资源。用于创建自定义技能、在团队中标准化技能结构、或将技能打包分发。"
allowed-tools: Write Bash
effort: low
---

# 技能创建器

生成新的 Claude Code 技能，包含正确的目录结构、YAML frontmatter 和可选的捆绑资源。

## 何时使用

- 为项目创建新的自定义技能
- 在团队中标准化技能结构
- 生成带脚本、引用和资产的技能模板
- 打包技能以供分发

## 技能目录结构

```
skill-name/
├── SKILL.md          # 必需：主技能文件，含 YAML frontmatter
├── scripts/          # 可选：用于确定性任务的可执行代码
├── references/       # 可选：按需加载的文档
└── assets/           # 可选：模板、图片、样板文件（不加载到上下文中）
```

## 工作流

### 1. 创建技能

```
在 ~/.claude/skills/ 中创建一个名为 "my-skill-name" 的新技能
```

或指定特定目的：

```
创建一个从 git 提交生成发布说明的技能，
附带 CHANGELOG.md 和 Slack 通知的模板
```

或通过初始化脚本：

```bash
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <输出目录>
```

### 2. 生成的 SKILL.md 模板

创建的 SKILL.md 遵循以下结构：

```markdown
---
name: skill-name
description: "技能用途。当 [触发条件] 时使用。"
---

# 技能名称

## 何时使用
- 触发条件 1
- 触发条件 2

## 此技能的作用
1. **步骤 1**：描述
2. **步骤 2**：描述

## 如何使用
[使用示例]

## 示例
**用户**："示例 prompt"
**输出**：[示例输出]
```

### 3. 验证技能

创建后，验证：

1. **Frontmatter**：`name` 为 kebab-case，1-64 字符；`description` 为带 "Use when" 子句的引用字符串
2. **内容**：有"何时使用"部分（含触发条件）和至少一个使用示例
3. **结构**：SKILL.md 不超过 5000 词；引用和资产在正确的子目录中
4. **测试**：用真实用例调用技能并确认预期输出

### 4. 打包分发（可选）

```bash
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [输出目录]
```

## 组织模式

| 模式 | 最适合 | 结构 |
|---------|----------|-----------|
| **工作流型** | 顺序步骤 | 逐步说明 |
| **任务型** | 多个操作 | 任务集合 |
| **参考/指南型** | 标准、规范 | 规则和示例 |
| **能力型** | 相关功能 | 功能描述 |

## 示例：创建发布说明技能

**用户**："创建一个生成 3 种输出格式的发布说明的技能"

**步骤**：
1. 初始化：`init_skill.py release-notes-generator --path ~/.claude/skills/`
2. 添加模板到 `assets/`：`changelog-template.md`、`pr-release-template.md`、`slack-template.md`
3. 添加规则到 `references/`：`tech-to-product-mappings.md`
4. 完善 `SKILL.md` 中的使用说明
5. 验证：检查 frontmatter，用真实的提交范围测试
6. 打包：`package_skill.py ~/.claude/skills/release-notes-generator`

## 提示

- 保持 SKILL.md 在 5000 词以内以高效使用上下文
- 对不常变化的领域知识使用 `references/`
- 将模板放在 `assets/` 中，使其不会被自动加载到上下文中
- 始终在 description frontmatter 中包含 "Use when" 子句
- 打包前用真实用例测试
