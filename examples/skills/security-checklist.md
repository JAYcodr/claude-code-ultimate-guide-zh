---
name: security-checklist
description: Web 应用程序安全清单
effort: medium
---

# Security Checklist 技能

## 快速安全审计

### 身份认证
- [ ] 密码使用 bcrypt/argon2 哈希（cost factor >= 10）
- [ ] 会话令牌为加密随机生成
- [ ] JWT token 短时效（access 15 分钟，refresh 7 天）
- [ ] 登录端点限速
- [ ] 多次失败尝试后锁定账户

### 授权
- [ ] 每个 API 端点检查权限
- [ ] 无 IDOR（不安全的直接对象引用）
- [ ] 实现基于角色的访问控制
- [ ] 敏感操作需要重新认证

### 输入验证
- [ ] 所有用户输入在服务端验证
- [ ] 文件上传限制类型和大小
- [ ] SQL 查询使用参数化语句
- [ ] HTML 输出编码以防止 XSS

### 数据保护
- [ ] 敏感数据静态加密
- [ ] 全站强制 HTTPS
- [ ] 安全 cookie（HttpOnly、Secure、SameSite）
- [ ] URL 和日志中不含敏感数据

### 头部与 CORS
- [ ] 设置 Content-Security-Policy 头部
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY（或 SAMEORIGIN）
- [ ] 启用 Strict-Transport-Security
- [ ] 正确限制 CORS

## 代码模式

### SQL 注入防护
```javascript
// 有漏洞
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// 安全
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### XSS 防护
```javascript
// 有漏洞
element.innerHTML = userInput;

// 安全
element.textContent = userInput;

// 安全（经过消毒）
element.innerHTML = DOMPurify.sanitize(userInput);
```

### CSRF 防护
```javascript
// 生成 token
const csrfToken = crypto.randomBytes(32).toString('hex');
session.csrfToken = csrfToken;

// POST 时验证
if (req.body.csrf !== session.csrfToken) {
  throw new ForbiddenError('无效的 CSRF token');
}
```

### 密钥管理
```javascript
// 绝不写在代码中
const API_KEY = 'sk-abc123...';

// 用环境变量
const API_KEY = process.env.API_KEY;

// 用密钥管理器（生产环境）
const secret = await secretsManager.getSecret('api-key');
```

## 安全头部示例

```javascript
// Express 中间件
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

## 依赖安全

```bash
# 检查漏洞
npm audit

# 自动修复
npm audit fix

# 检查过时包
npm outdated

# 更新依赖
npm update
```

## 记录安全事件

```javascript
// 需要记录的事件
logger.security({
  event: 'login_failed',
  ip: req.ip,
  email: req.body.email,
  reason: 'invalid_password',
  timestamp: new Date().toISOString()
});

// 绝不记录
// - 密码
// - 完整信用卡号
// - 会话令牌
// - 个人数据（生产环境）
```

## 部署前检查清单

1. [ ] 运行 `npm audit` — 无严重漏洞
2. [ ] 所有密钥在环境变量中
3. [ ] 关闭调试模式
4. [ ] 错误消息不暴露内部信息
5. [ ] 仅 HTTPS（HTTP 重定向到 HTTPS）
6. [ ] 数据库凭证已轮换
7. [ ] 日志已配置（不记录敏感数据）
8. [ ] 备份策略已测试
