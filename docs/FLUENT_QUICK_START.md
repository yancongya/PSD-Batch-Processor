# PyQt-Fluent-Widgets 版本快速启动指南

## ✅ 安装状态

**已安装依赖**:
- ✅ Python 3.13.1
- ✅ PyQt5 5.15.11
- ✅ PyQt-Fluent-Widgets 1.11.0
- ✅ pywin32 311

## 🚀 快速启动

### 方法 1: 直接启动（推荐）
```bash
cd "F:\插件脚本开发\PSD Batch Processor\src"
python main_fluent.py
```

### 方法 2: 使用启动脚本
```bash
cd "F:\插件脚本开发\PSD Batch Processor"
python tools\run_fluent.py
```

### 方法 3: 运行测试验证
```bash
cd "F:\插件脚本开发\PSD Batch Processor"
python tests\test_fluent_app.py
```

## 🎯 首次使用步骤

### 1. 验证安装
```bash
python tests\test_fluent_app.py
```
应该显示：`[SUCCESS] PyQt-Fluent-Widgets 版本测试通过！`

### 2. 启动应用
```bash
cd "F:\插件脚本开发\PSD Batch Processor\src"
python main_fluent.py
```

### 3. 配置 Photoshop 路径
- 应用启动后，点击"浏览..."按钮
- 选择 Photoshop.exe 文件
- 通常路径：`C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe`

### 4. 刷新脚本列表
- 点击"刷新"按钮
- 系统会扫描 `scripts/` 目录及其子目录
- 从下拉框选择要执行的脚本

### 5. 添加文件并处理
- 点击"添加文件"选择 PSD 文件
- 或点击"添加文件夹"批量添加
- 点击"开始处理"按钮

## 📋 界面说明

### 主页界面
```
┌─────────────────────────────────────────────────────────┐
│ ⭐ PSD 批量处理器                                         │
├─────────────────────────────────────────────────────────┤
│ ⚙️ 设置                                                  │
│   Photoshop 路径: [浏览...]                              │
│   选择脚本:     [下拉框] [刷新]                          │
│   并发数:       [1]                                      │
├─────────────────────────────────────────────────────────┤
│ 📁 文件列表                                              │
│   [添加文件] [添加文件夹] [清空]                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │ 文件名          状态      路径                  │   │
│   └─────────────────────────────────────────────────┘   │
│   就绪 - 0 个文件                                        │
├─────────────────────────────────────────────────────────┤
│ [开始处理] [停止] [打开输出文件夹]                       │
├─────────────────────────────────────────────────────────┤
│ 📋 日志预览                                              │
│   [实时日志显示]                                         │
└─────────────────────────────────────────────────────────┘
```

### 导航栏
- **主页**: 文件处理核心功能
- **设置**: 主题和路径配置
- **日志**: 完整日志查看

## 🔧 常见问题

### 问题 1: 模块导入错误
**错误**: `ModuleNotFoundError: No module named 'PyQtFluentWidgets'`

**解决**: 模块名是 `qfluentwidgets`，不是 `PyQtFluentWidgets`
```bash
# 检查导入
python -c "from qfluentwidgets import FluentWindow; print('OK')"
```

### 问题 2: 图标找不到
**错误**: `AttributeError: type object 'FluentIcon' has no attribute 'FOLDER_OPEN'`

**解决**: 已修复为 `FluentIcon.FOLDER`

### 问题 3: TreeWidgetItem 错误
**错误**: `ImportError: cannot import name 'TreeWidgetItem'`

**解决**: 已修复为 `QTreeWidgetItem` (来自 PyQt5.QtWidgets)

### 问题 4: GUI 不显示
**可能原因**: 在远程桌面或无图形界面环境中

**解决**:
- 在有图形界面的环境中运行
- 或使用 VNC/远程桌面

## 📁 文件位置

### 配置文件
- **开发环境**: `src/config.json`
- **打包后**: `%APPDATA%\PSDBatchProcessor\config.json`

### 脚本目录
- **默认**: `scripts/`
- **子目录**: `production/`, `templates/`, `examples/`

### 备份目录
- **默认**: `backups/`
- **格式**: `backups/YYYYMMDD_HHMMSS/`

## 🎨 界面特性

### 现代化设计
- **Fluent Design**: Windows 11 风格
- **卡片布局**: 清晰的功能分区
- **多页面导航**: 主页/设置/日志
- **主题切换**: 深色/浅色主题

### 实时反馈
- **进度条**: 显示处理进度
- **日志预览**: 实时显示日志
- **信息提示**: 优雅的错误/警告/成功提示

### 响应式设计
- **自适应布局**: 窗口大小调整时自动适应
- **线程安全**: UI 不会卡顿
- **实时更新**: 进度和日志实时显示

## 📊 性能优化

### 并发处理
- **推荐设置**:
  - 低配电脑: 1-2
  - 中配电脑: 2-4
  - 高配电脑: 4-8

### 内存管理
- **自动清理**: 处理完成后自动清理临时文件
- **日志限制**: 自动限制日志行数避免内存溢出

## 🆘 获取帮助

### 查看文档
- **完整指南**: `docs/FLUENT_VERSION_GUIDE.md`
- **快速参考**: `docs/QUICK_REFERENCE_FLUENT.md`
- **主文档**: `README.md`
- **PyQt-Fluent-Widgets 文档**: `README_FLUENT.md`

### 测试脚本
```bash
# 测试应用启动
python tests\test_fluent_app.py

# 测试依赖
python tests\test_fluent_widgets.py

# 测试环境
python tests\test_env.py
```

## 🎉 成功标志

应用成功启动时，你会看到：
1. ✅ 现代化的 Fluent Design 界面
2. ✅ 三个导航页面（主页、设置、日志）
3. ✅ 卡片式布局
4. ✅ 实时日志显示
5. ✅ 可以添加文件和选择脚本

---

**版本**: 1.0.0
**更新日期**: 2026-01-24
**状态**: ✅ 生产就绪
**测试**: ✅ 通过