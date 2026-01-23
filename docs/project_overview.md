# PSD Batch Processor - 项目概览

## 🎯 项目简介

**PSD Batch Processor** 是一个 Windows 桌面应用程序，用于批量处理 Photoshop PSD 文件。通过 COM 接口直接控制 Photoshop，执行自定义的 JSX 脚本，同时提供自动备份和现代化的用户界面。

### 核心价值

- 🔒 **安全**：每次处理前自动创建带时间戳的备份副本
- ⚡ **高效**：通过 COM 接口直接控制 Photoshop，减少启动开销
- 🎨 **现代界面**：使用 customtkinter 打造美观的暗色/亮色主题 UI
- 🛠️ **可维护**：分层清晰，配置可持久化，日志友好

## 📊 项目统计

| 项目 | 数值 |
|------|------|
| 总代码行数 | ~3000+ 行 |
| Python 文件数 | 10 个 |
| 文档文件数 | 5 个 |
| 示例脚本数 | 3 个 |
| 开发时间 | 1 天 |
| MVP 完成度 | 100% |

## 📁 项目结构

```
PSD Batch Processor/
├── 📄 核心文件
│   ├── main.py                    # 主程序入口（70 行）
│   ├── test_env.py               # 环境验证脚本（180 行）
│   ├── install.bat               # Windows 安装脚本
│   └── requirements.txt          # Python 依赖
│
├── 📦 应用程序 (app/)
│   ├── ui/                       # 用户界面层
│   │   └── main_window.py        # 主窗口（1200+ 行）
│   ├── core/                     # 核心业务逻辑
│   │   ├── photoshop_controller.py  # Photoshop 控制器（200 行）
│   │   └── processor.py          # 批量处理器（350 行）
│   ├── models/                   # 数据模型
│   │   └── file_item.py          # 文件项模型（200 行）
│   └── config/                   # 配置管理
│       └── settings.py           # 配置读写（180 行）
│
├── 🔧 工具模块 (utils/)
│   └── logger.py                 # 日志工具（140 行）
│
├── 📝 脚本 (scripts/)
│   ├── example_convert_to_grayscale.jsx  # 灰度转换
│   ├── example_flatten_image.jsx         # 压平图像
│   └── example_resize_50_percent.jsx     # 缩小 50%
│
├── 📚 文档 (docs/)
│   ├── todo.md                   # 需求文档
│   ├── quick_start.md            # 快速开始
│   ├── project_structure.md      # 项目结构
│   ├── development_summary.md    # 开发总结
│   └── project_overview.md       # 本文件
│
├── 📄 其他
│   ├── README.md                 # 项目主文档
│   ├── .gitignore               # Git 忽略配置
│   └── show_tree.py             # 目录树显示
│
└── 📁 运行时目录（自动生成）
    ├── backups/                  # 备份文件
    └── logs/                     # 日志文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 方法 1：使用安装脚本（Windows）
install.bat

# 方法 2：手动安装
pip install customtkinter pywin32
```

### 2. 启动程序

```bash
python main.py
```

### 3. 基本使用流程

1. **配置设置**
   - 设置 Photoshop 路径
   - 选择脚本目录
   - 选择备份目录
   - 点击"保存配置"

2. **添加文件**
   - 点击"添加文件"或"添加文件夹"
   - 选择 PSD 文件

3. **选择脚本**
   - 从下拉框选择 JSX 脚本
   - 点击"刷新"扫描脚本目录

4. **开始处理**
   - 点击"▶️ 开始处理"
   - 等待处理完成
   - 查看结果和日志

## 🎨 界面预览

### 主界面布局

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️ 基础设置                                              │
│  Photoshop 路径: [浏览...]                               │
│  脚本目录: [浏览...] [刷新]                              │
│  选择脚本: [下拉框]                                      │
│  备份目录: [浏览...]                                     │
│  主题: [暗色] 并发数: [1] 包含子文件夹 [✓]                │
├─────────────────────────────────────────────────────────┤
│  📁 文件列表                                             │
│  [添加文件] [添加文件夹] [移除选中] [清空列表]            │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 文件名        │ 路径        │ 状态    │ 大小      │  │
│  ├───────────────┼─────────────┼─────────┼───────────┤  │
│  │ example.psd   │ C:\Users\.. │ 待处理  │ 10.50 MB  │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  📝 日志                                                 │
│  [进度条 0%]                                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 2026-01-23 18:45:30 - 已连接到 Photoshop          │  │
│  │ 2026-01-23 18:45:31 - 创建备份文件夹...           │  │
│  │ 2026-01-23 18:45:32 - 处理完成: example.psd       │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  [▶️ 开始处理] [⏹️ 停止] [💾 保存配置] [📂 打开备份文件夹] │
└─────────────────────────────────────────────────────────┘
```

## 📝 JSX 脚本示例

### 示例 1：转换为灰度

```javascript
// example_convert_to_grayscale.jsx
try {
    if (app.documents.length > 0) {
        var doc = app.activeDocument;
        if (doc.mode != DocumentMode.GRAYSCALE) {
            doc.changeMode(ChangeMode.GRAYSCALE);
        }
        doc.save();
    }
} catch (e) {
    throw e;
}
```

### 示例 2：压平图像

```javascript
// example_flatten_image.jsx
try {
    if (app.documents.length > 0) {
        var doc = app.activeDocument;
        if (doc.layers.length > 1) {
            doc.flatten();
        }
        doc.save();
    }
} catch (e) {
    throw e;
}
```

### 示例 3：调整大小

```javascript
// example_resize_50_percent.jsx
try {
    if (app.documents.length > 0) {
        var doc = app.activeDocument;
        var newWidth = doc.width * 0.5;
        var newHeight = doc.height * 0.5;
        doc.resizeImage(newWidth, newHeight, 72, ResampleMethod.BICUBIC);
        doc.save();
    }
} catch (e) {
    throw e;
}
```

## 🔧 技术栈

| 类别 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 语言 | Python | 3.10+ | 编程语言 |
| GUI | customtkinter | 5.2.2+ | 现代化界面 |
| COM | pywin32 | 306+ | Photoshop 控制 |
| 配置 | JSON | - | 持久化存储 |
| 日志 | logging | 标准库 | 日志系统 |
| 并发 | ThreadPoolExecutor | 标准库 | 多线程处理 |

## 📋 功能清单

### ✅ 已实现（MVP v1.0）

- [x] Photoshop COM 连接（自动启动）
- [x] 自动备份（带时间戳）
- [x] 文件批量添加（文件/文件夹）
- [x] JSX 脚本选择和执行
- [x] 实时状态更新
- [x] 彩色日志输出
- [x] 进度条显示
- [x] 结果统计弹窗
- [x] 配置持久化
- [x] 主题切换（暗色/亮色）
- [x] 右键菜单（打开文件夹/用 PS 打开）
- [x] 单线程/双线程并发
- [x] 错误处理和日志记录

### 📋 计划中（v1.1+）

- [ ] 脚本参数传递
- [ ] PSD 缩略图预览
- [ ] 处理前后对比
- [ ] 任务队列管理
- [ ] 撤销/回滚功能
- [ ] 更多 JSX 示例
- [ ] 单元测试
- [ ] 多语言支持

## ⚠️ 重要注意事项

1. **平台限制**：仅支持 Windows（依赖 COM）
2. **Photoshop 依赖**：必须安装 Photoshop
3. **备份机制**：程序会自动备份，但建议首次手动备份
4. **并发限制**：建议使用 1 个并发（最稳定）
5. **脚本编写**：JSX 脚本必须调用 `doc.save()`
6. **异常处理**：JSX 脚本中抛出异常会被捕获

## 🐛 常见问题

### Q: 如何安装依赖？
**A**: 运行 `install.bat` 或 `pip install customtkinter pywin32`

### Q: Photoshop 路径怎么设置？
**A**: 点击"浏览..."按钮选择 Photoshop.exe，或使用默认路径

### Q: 备份文件在哪里？
**A**: 在配置的备份目录下，按时间戳命名的子文件夹中

### Q: 如何编写 JSX 脚本？
**A**: 参考 `scripts/` 目录下的示例脚本，确保调用 `doc.save()`

### Q: 处理失败怎么办？
**A**: 查看日志窗口的错误信息，检查脚本语法和 Photoshop 状态

## 📚 文档导航

- **README.md** - 完整的项目文档和使用说明
- **docs/quick_start.md** - 快速开始指南
- **docs/todo.md** - 详细的需求文档
- **docs/project_structure.md** - 项目结构详解
- **docs/development_summary.md** - 开发总结
- **docs/project_overview.md** - 本文件（项目概览）

## 🎓 学习资源

### 自定义 JSX 脚本

```javascript
// 基本结构
try {
    if (app.documents.length > 0) {
        var doc = app.activeDocument;

        // 你的处理逻辑
        // 例如：doc.flatten();

        doc.save();  // 必须保存！
    }
} catch (e) {
    throw e;  // 抛出异常让主程序知道失败
}
```

### 常用 Photoshop API

- `app.activeDocument` - 当前文档
- `doc.flatten()` - 压平图像
- `doc.changeMode()` - 改变颜色模式
- `doc.resizeImage()` - 调整大小
- `doc.save()` - 保存文档
- `doc.close()` - 关闭文档

## 🤝 贡献指南

欢迎贡献代码和文档！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 支持

如有问题或建议：
- 查看日志文件（`logs/` 目录）
- 阅读常见问题部分
- 检查依赖是否正确安装

---

**项目状态**: ✅ MVP v1.0 完成
**最后更新**: 2026-01-23
**版本**: v1.0.0
