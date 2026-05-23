---
name: ship
description: 全面的部署前验证，确保发布就绪
argument-hint: "[--no-push] [--changelog-only] [--dry-run]"
effort: medium
disable-model-invocation: true
---

# 发布命令 - 部署前检查清单

全面的部署前验证，确保发布就绪。

## 目的

每次生产部署前运行，验证：
- 代码质量门
- 测试覆盖率
- 安全检查
- 文档更新
- 环境就绪

## 部署前检查清单

### 🔴 阻塞项（必须通过）

```bash
# 1. 所有测试通过
npm test 2>/dev/null || pnpm test 2>/dev/null || yarn test 2>/dev/null
echo "退出码：$?"

# 2. 无 TypeScript/lint 错误
npm run typecheck 2>/dev/null || npx tsc --noEmit
npm run lint 2>/dev/null || npx eslint .

# 3. 构建成功
npm run build 2>/dev/null || pnpm build 2>/dev/null

# 4. 代码中无密钥
grep -rn "API_KEY=\|SECRET=\|PASSWORD=" --include="*.{ts,js,json}" . 2>/dev/null | grep -v node_modules | grep -v ".env.example"
```

### 🟠 高优先级（应通过）

```bash
# 5. 安全审计
npm audit --audit-level=high 2>/dev/null || echo "手动运行：npm audit"

# 6. 生产代码中无 console.log
grep -rn "console\.log\|console\.debug" --include="*.{ts,js,tsx,jsx}" src/ 2>/dev/null | grep -v "// allowed" | head -10

# 7. 关键路径中无 TODO/FIXME
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.{ts,js}" src/ 2>/dev/null | head -10

# 8. 数据库迁移就绪
[ -d "prisma/migrations" ] && echo "Prisma migrations：$(ls prisma/migrations | wc -l) 个"
[ -d "migrations" ] && echo "迁移：$(ls migrations | wc -l) 个"
```

### 🟡 建议项（锦上添花）

```bash
# 9. 文档更新
git diff --name-only HEAD~5 | grep -E "README|CHANGELOG|docs/" | head -10

# 10. 版本号更新
cat package.json | jq -r '.version' 2>/dev/null || echo "手动检查版本"

# 11. 环境变量已文档化
[ -f ".env.example" ] && echo "✅ .env.example 存在" || echo "⚠️ 缺少 .env.example"
```

## 输出格式

---

### 🚀 发布就绪报告

**分支**：[当前分支]
**提交**：[HEAD 短 hash]
**目标**：[生产/预发布]
**时间戳**：[日期/时间]

### 阻塞项（部署前必须修复）

| 检查项 | 状态 | 详情 |
|-------|--------|---------|
| 测试 | ✅/❌ | X 通过，Y 失败 |
| TypeScript | ✅/❌ | X 个错误 |
| Lint | ✅/❌ | X 个警告，Y 个错误 |
| 构建 | ✅/❌ | 成功/失败 |
| 密钥 | ✅/❌ | X 个潜在泄露 |

### 高优先级

| 检查项 | 状态 | 操作 |
|-------|--------|--------|
| 安全审计 | ⚠️/✅ | X 个漏洞 |
| Console Log | ⚠️/✅ | src/ 中发现 X 个 |
| TODOs | ⚠️/✅ | X 个关键 TODO |
| 迁移 | ⚠️/✅ | X 个待处理 |

### 建议项

| 检查项 | 状态 | 说明 |
|-------|--------|------|
| 文档更新 | ⚠️/✅ | CHANGELOG 已更新 |
| 版本号更新 | ⚠️/✅ | 当前：X.Y.Z |
| 环境变量文档 | ⚠️/✅ | .env.example 存在 |

### 📊 总结

```
🔴 阻塞项：    X/5 通过
🟠 高优先级：  X/4 通过
🟡 建议项：    X/3 通过
─────────────────────────
总体：        [可以发布/不可发布]
```

### 🎯 操作项

1. [最需要修复的关键问题]
2. [第二优先级]
3. [第三优先级]

---

## 环境特定检查

### 生产部署

```bash
# 验证生产环境变量
[ -f ".env.production" ] && echo "生产环境配置存在"

# 检查调试标志
grep -rn "DEBUG=true\|NODE_ENV=development" .env* 2>/dev/null

# 验证 API 端点指向生产环境
grep -rn "localhost\|127\.0\.0\.1" --include="*.{ts,js,json}" src/ 2>/dev/null | grep -v test | head -5
```

### 预发布部署

```bash
# 预发布特定检查
[ -f ".env.staging" ] && echo "预发布环境配置存在"

# 预发布功能标志
grep -rn "FEATURE_FLAG\|ENABLE_" .env* 2>/dev/null
```

## CI/CD 集成

添加到你的流水线：

```yaml
# GitHub Actions 示例
ship-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: 运行发布检查清单
      run: |
        npm ci
        npm test
        npm run typecheck
        npm run lint
        npm run build
        npm audit --audit-level=high
```

## 部署后验证

部署后，验证：

```bash
# 1. 健康检查
curl -s https://your-app.com/health | jq .

# 2. 版本检查
curl -s https://your-app.com/version | jq .

# 3. 冒烟测试
npm run test:smoke 2>/dev/null || echo "手动运行冒烟测试"
```

## 回滚准备

发布前，确保可以回滚：

```bash
# 记下当前生产标签
git describe --tags --abbrev=0

# 验证回滚流程存在
[ -f "docs/runbooks/rollback.md" ] && echo "✅ 回滚文档存在"

# 检查数据库迁移可逆性
# Prisma：prisma migrate diff
# Rails：rails db:rollback (dry-run)
```

## 用法

**完整检查清单：**
```
/ship
```

**生产部署：**
```
/ship --production
```

**快速检查（仅阻塞项）：**
```
/ship --quick
```

**指定目标：**
```
/ship --target=staging
```

## 提示

1. **尽早频繁运行**：不要等到部署当天
2. **在 CI 中自动化**：使阻塞项导致流水线失败
3. **团队约定**：定义什么是阻塞项 vs 警告
4. **记录例外情况**：如果跳过检查，说明原因
5. **部署后持续监控**：监控确认成功才算发布完成

## 相关命令

- `/release-notes` - 生成变更日志和公告
- `/validate-changes` - 基于 LLM 的代码审查
- `/security` - 深度安全审计

$ARGUMENTS
