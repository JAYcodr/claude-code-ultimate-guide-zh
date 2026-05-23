---
name: tdd-workflow
description: 测试驱动开发工作流和最佳实践
effort: low
---

# TDD 工作流技能

## TDD 循环

```
RED → GREEN → REFACTOR
 ↑__________________|
```

### 1. RED：编写会失败的测试
- 编写最小的会失败的测试
- 测试应因正确的原因失败
- 确保测试实际运行

### 2. GREEN：让它通过
- 编写最少的代码使测试通过
- 先不优化
- 代码丑陋没关系

### 3. REFACTOR：清理
- 改进代码结构
- 消除重复
- 保持测试通过

## TDD 最佳实践

### 测试命名约定
```
should_[预期行为]_when_[条件]
```

示例：
- `should_return_empty_array_when_no_items`
- `should_throw_error_when_invalid_input`
- `should_calculate_total_when_items_present`

### 测试结构（AAA）
```typescript
it('should calculate discount when coupon applied', () => {
  // Arrange - 设置测试数据
  const cart = new Cart();
  cart.addItem({ price: 100 });
  const coupon = new Coupon('10OFF', 10);

  // Act - 执行行为
  cart.applyCoupon(coupon);

  // Assert - 验证结果
  expect(cart.total).toBe(90);
});
```

### 测试隔离
- 每个测试应独立
- 测试间无共享状态
- 使用 `beforeEach` 进行通用设置
- 在 `afterEach` 中清理

## TDD 工作流示例

### 功能：向购物车添加项目

**步骤 1：RED**
```typescript
describe('Cart', () => {
  it('should add item to cart', () => {
    const cart = new Cart();
    cart.addItem({ id: 1, name: 'Book', price: 29.99 });
    expect(cart.items).toHaveLength(1);
  });
});
```
运行测试 → 失败（Cart 不存在）

**步骤 2：GREEN**
```typescript
class Cart {
  items = [];

  addItem(item) {
    this.items.push(item);
  }
}
```
运行测试 → 通过

**步骤 3：REFACTOR**
```typescript
class Cart {
  private _items: CartItem[] = [];

  get items(): ReadonlyArray<CartItem> {
    return this._items;
  }

  addItem(item: CartItem): void {
    this._items.push(item);
  }
}
```
运行测试 → 仍通过

### 下一轮迭代：计算总额
为每个新行为重复循环。

## 何时使用 TDD

### 适合 TDD
- 业务逻辑
- 复杂算法
- API 端点
- 状态管理
- 工具函数

### 不太适合
- UI 布局（视觉测试更好）
- 数据库迁移
- 外部集成（使用集成测试）
- 探索性/原型代码

## 常见 TDD 错误

1. **写了太多测试** — 从最小的失败测试开始
2. **写了太多代码** — 只写到能通过
3. **跳过重构** — 技术债务积累
4. **测试实现** — 测试行为，而非内部
5. **忽视失败的测试** — 修复或删除，绝不跳过

## 测试替身

| 类型 | 用途 | 示例 |
|------|---------|---------|
| Stub | 返回固定数据 | `jest.fn().mockReturnValue(42)` |
| Mock | 验证交互 | `expect(mock).toHaveBeenCalled()` |
| Spy | 追踪调用 | `jest.spyOn(obj, 'method')` |
| Fake | 简化实现 | 内存数据库 |


