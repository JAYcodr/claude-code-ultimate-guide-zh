---
name: generate-tests
description: 为指定代码生成全面的测试
argument-hint: "<文件或模块> [--framework jest|vitest|pytest]"
effort: medium
disable-model-invocation: true
---

# 生成测试

为指定代码生成全面的测试。

## 使用说明

1. 读取目标文件
2. 识别可测试单元（函数、类、方法）
3. 按照项目约定生成测试
4. 确保边缘用例的高覆盖率

## 测试生成流程

### 1. 分析目标
- 识别公共接口
- 理解依赖关系
- 注意边缘用例和边界

### 2. 检测测试框架
检查是否存在：
- `jest.config.js` → Jest
- `vitest.config.ts` → Vitest
- `pytest.ini` → pytest
- `mocha` in package.json → Mocha

### 3. 生成测试
遵循检测到的框架约定。

## 测试类别

### 正常路径
有效输入下的预期行为。

### 边缘用例
- 空输入
- 空/未定义值
- 边界值（0、-1、MAX_INT）
- 单个项 vs 多个项

### 错误用例
- 无效输入类型
- 缺少必需参数
- 网络/IO 失败
- 超时场景

### 集成点
- 数据库交互
- 外部 API 调用
- 文件系统操作

## 输出格式

```typescript
describe('[组件名]', () => {
  describe('[方法名]', () => {
    // 正常路径
    it('当 [条件] 时应 [预期行为]', () => {
      // Arrange
      // Act
      // Assert
    });

    // 边缘用例
    it('应处理空输入', () => {});
    it('应处理空值', () => {});

    // 错误用例
    it('当 [无效条件] 时应抛出异常', () => {});
  });
});
```

## 约定

- 每个测试一个断言（可行时）
- 描述性测试名称
- AAA 模式（Arrange-Act-Assert）
- 测试间无依赖
- 模拟外部依赖

## 用法

```
/generate-tests src/utils/calculator.ts
/generate-tests src/services/
```

$ARGUMENTS
