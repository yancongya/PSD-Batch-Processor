# 移除脚本弹窗指南

## 概述

为了让脚本支持无人值守的批量处理，需要移除所有弹窗对话框（`confirm()` 和 `alert()`），改为直接执行或使用日志输出。

## 修改方法

### 1. 移除 confirm() 对话框

#### 原代码：
```javascript
if (confirm("Start to clean?")) {
    start();
}
```

#### 修改后：
```javascript
// 直接执行，不询问用户
start();
```

#### 如果需要条件判断：
```javascript
// 原代码
if (confirm("确定要处理吗？")) {
    // 处理逻辑
}

// 修改后 - 直接处理
// 处理逻辑
```

### 2. 替换 alert() 为日志输出

#### 原代码：
```javascript
alert("处理完成");
alert("错误: " + error_message);
```

#### 修改后：
```javascript
// 成功信息
$.writeln("✅ 处理完成");

// 错误信息（总是输出）
$.writeln("❌ 错误: " + error_message);

// 警告信息
$.writeln("⚠ 警告: 某些图层无法处理");

// 信息性消息
$.writeln("ℹ 正在处理图层: " + layerName);
```

### 3. 完整示例

#### 修改前：
```javascript
function start(){
    if (confirm("确定要清理元数据吗？")) {
        deleteDocumentAncestorsMetadata();
        alert("清理完成");
    } else {
        alert("用户取消操作");
    }
}

try{
    start();
} catch (e) {
    alert("清理失败: " + e);
}
```

#### 修改后：
```javascript
function start(){
    // 直接执行清理，不询问
    deleteDocumentAncestorsMetadata();
    $.writeln("✅ 清理完成");
}

try{
    start();
} catch (e) {
    $.writeln("❌ 清理失败: " + e);
}
```

## 日志级别说明

| 级别 | 前缀 | 使用场景 |
|------|------|----------|
| 成功 | `✅ ` | 操作成功完成 |
| 错误 | `❌ ` | 发生错误（总是输出） |
| 警告 | `⚠ ` | 警告信息 |
| 信息 | `ℹ ` | 信息性消息 |

## 常见弹窗模式及修改

### 1. 确认后执行
```javascript
// 修改前
if (confirm("要执行吗？")) {
    doSomething();
}

// 修改后
doSomething();
```

### 2. 显示结果
```javascript
// 修改前
alert("处理完成！\n文件: " + fileName + "\n耗时: " + time + "s");

// 修改后
$.writeln("✅ 处理完成！文件: " + fileName + " 耗时: " + time + "s");
```

### 3. 错误提示
```javascript
// 修改前
alert("错误: " + errorMsg);

// 修改后
$.writeln("❌ 错误: " + errorMsg);
```

### 4. 条件确认
```javascript
// 修改前
if (layerCount > 1) {
    if (confirm("有 " + layerCount + " 个图层，要压平吗？")) {
        doc.flatten();
    }
}

// 修改后
if (layerCount > 1) {
    $.writeln("ℹ 压平 " + layerCount + " 个图层");
    doc.flatten();
}
```

## 批量处理最佳实践

### 1. 错误处理
```javascript
try {
    // 处理逻辑
    $.writeln("✅ 操作成功");
} catch (e) {
    $.writeln("❌ 操作失败: " + e.message);
    // 不要抛出异常，让批处理继续
}
```

### 2. 进度反馈
```javascript
$.writeln("ℹ 开始处理: " + doc.name);
$.writeln("ℹ 图层数量: " + doc.layers.length);
// ... 处理逻辑
$.writeln("✅ 处理完成: " + doc.name);
```

### 3. 跳过不适用的情况
```javascript
if (doc.mode == DocumentMode.GRAYSCALE) {
    $.writeln("ℹ 文档已经是灰度模式，跳过");
    return; // 直接返回，不弹窗
}
```

## 测试修改后的脚本

### 1. 手动测试
```javascript
// 在 Photoshop 中打开一个文档
// 然后执行脚本，应该：
// - 不显示任何确认对话框
// - 不显示 alert 弹窗
// - 在控制台输出日志信息
```

### 2. 批量测试
```javascript
// 使用 PSD Batch Processor 批量处理多个文件
// 应该：
// - 自动处理所有文件
// - 不需要人工干预
// - 在日志中显示处理进度
```

## 注意事项

### 1. 保留重要信息
- 错误信息应该保留，但改为日志输出
- 成功提示可以简化或省略
- 进度信息有助于调试

### 2. 错误恢复
- 不要让错误中断整个批处理
- 使用 try-catch 捕获异常
- 记录错误但继续处理下一个文件

### 3. 性能考虑
- 减少不必要的日志输出
- 批量处理时避免过多的控制台输出
- 保持脚本简洁高效

## 示例脚本

项目中提供了几个无弹窗版本的示例脚本：

- `example_resize_50_percent.jsx` - 缩放图像
- `example_convert_to_grayscale.jsx` - 转换为灰度
- `example_flatten_image.jsx` - 压平图像
- `PsDeepCleaner.jsx` - 元数据清理（已修改）

这些脚本都可以直接用于批量处理，无需人工干预。

## 快速修改清单

- [ ] 移除所有 `confirm()` 调用
- [ ] 替换所有 `alert()` 为 `$.writeln()`
- [ ] 添加适当的日志前缀（✅ ❌ ⚠ ℹ）
- [ ] 添加 try-catch 错误处理
- [ ] 测试脚本确保无弹窗
- [ ] 验证日志输出是否正常

## 下一步

1. **测试脚本**：在 Photoshop 中手动运行修改后的脚本
2. **批量验证**：使用 PSD Batch Processor 批量处理文件
3. **其他脚本**：按相同方式修改其他需要批量处理的脚本