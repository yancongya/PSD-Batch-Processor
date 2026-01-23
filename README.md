
# PSD Batch Processor

一个用于批量处理 PSD 文件的 Python 应用程序，支持通过 Photoshop 脚本自动化处理。

## 🎨 界面版本

本项目已全面升级为 **PyQt-Fluent-Widgets** 版本，提供现代化的 Fluent Design 界面。

### 版本对比

| 特性 | CustomTkinter (已弃用) | PyQt-Fluent-Widgets (推荐) |
|------|-------------------|-------------------------|
| **界面风格** | 现代化，类似 Material Design | Fluent Design (Windows 11 风格) |
| **导航方式** | 单页面布局 | 多页面导航 (侧边栏) |
| **控件丰富度** | 基础控件 | 丰富的高级控件 |
| **依赖大小** | 较小 (~50MB) | 较大 (~80MB) |
| **启动速度** | 快 (~1-2秒) | 中等 (~2-3秒) |
| **推荐场景** | ❌ 已停止维护 | ✅ 完整功能、美观界面 |

### 快速启动

#### PyQt-Fluent-Widgets 版本（推荐）
```bash
# 安装依赖（首次使用）
python tools\install_fluent.py

# 启动应用
python tools\run_fluent.py

# 或直接运行
python src\main_fluent.py
```

#### 传统版本（已弃用）
CustomTkinter 版本已备份为 `src/app/ui/main_window.py.backup`，不再维护。

## ✨ 功能特性

- 📁 **批量处理**: 一次处理多个 PSD 文件
- 🔄 **自动备份**: 处理前自动备份原始文件
- 🎨 **Photoshop 集成**: 通过 COM 接口控制 Photoshop
- 📝 **脚本支持**: 支持自定义 JSX 脚本（支持子目录）
- 🎯 **无人值守**: 脚本无弹窗，完全自动化
- 📊 **实时进度**: 显示处理进度和状态
- 🌙 **主题支持**: 深色/浅色主题切换
- 📋 **完整日志**: 实时日志查看和保存
- 🗂️ **多页面布局**: 文件处理、脚本管理、设置、日志四页分离

## 🖥️ 界面预览

PyQt-Fluent-Widgets V2 版本采用四页布局，功能分离更清晰：

### 1. 文件处理页 (主页)
- 添加文件/文件夹
- 选择脚本和并发数
- 开始/停止处理
- 实时进度显示

### 2. 脚本管理页
- 浏览所有可用脚本
- 支持子目录结构
- 脚本说明和路径显示
- 一键刷新脚本列表

### 3. 设置页
- Photoshop 路径配置
- 脚本目录和备份目录设置
- 并发数调整
- 主题切换

### 4. 日志页
- 完整处理日志
- 日志清空和保存
- 实时更新显示

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+ (推荐 3.10+)
- Photoshop (Windows 版本)
- Windows 操作系统

### 2. 安装依赖

#### 自动安装（推荐）
```bash
# 自动安装所有依赖（PyQt5 + PyQt-Fluent-Widgets + pywin32）
python tools\install_fluent.py
```

#### 手动安装
```bash
pip install -r requirements.txt
```

### 3. 运行程序

```bash
# Windows - 推荐方式
python tools\run_fluent.py

# 或直接运行
python src\main_fluent.py
```

> 💡 **提示**: 首次运行会自动检查并安装缺失的依赖

### 4. 基本使用
1. 设置 Photoshop 路径
2. 选择脚本目录和脚本
3. 添加要处理的 PSD 文件
4. 点击"开始处理"
5. 查看日志和处理结果

## 📁 项目结构

```
PSD Batch Processor/
├── src/              # 源代码
├── scripts/          # JSX 脚本
├── docs/             # 文档
├── tests/            # 测试文件
├── tools/            # 工具脚本
└── backups/          # 备份目录
```

详细结构：查看 [docs/project_structure.md](docs/project_structure.md)

## 📚 文档

### PyQt-Fluent-Widgets 版本
- [快速开始指南](docs/FLUENT_QUICK_START.md)
- [版本指南](docs/FLUENT_VERSION_GUIDE.md)
- [界面说明](docs/FLUENT_INTERFACE_GUIDE.md)

### 脚本开发
- [模板脚本](scripts/templates/auto_mode_template.jsx)
- [脚本修改指南](docs/guides/REMOVE_DIALOGS_GUIDE.md)
- [示例脚本](scripts/examples/)

### 高级功能
- [自动模式指南](docs/guides/AUTO_MODE_GUIDE.md)
- [打包指南](docs/PACKAGING_GUIDE.md)

## 🔧 核心组件

### 应用程序 (src/app/)
- **config/**: 配置管理
- **core/**: 核心业务逻辑
- **models/**: 数据模型
- **ui/**: 用户界面

### 脚本 (scripts/)
- **templates/**: 模板脚本
- **examples/**: 示例脚本
- **production/**: 生产脚本

## 🧪 测试

```bash
# 环境测试
python tests/test_env.py

# 自动模式测试
python tests/test_auto_mode.py
```

## 📝 开发指南

### 添加新功能
1. 在 `src/app/` 对应模块中开发
2. 在 `tests/` 中添加测试
3. 更新 `docs/guides/` 中的文档

### 创建新脚本
1. 复制 `scripts/templates/auto_mode_template.jsx`
2. 修改为你的需求
3. 保存到 `scripts/examples/` 或 `scripts/production/`

## 🔄 更新日志

查看 [docs/development_summary.md](docs/archive/development_summary.md) 了解开发历程。

## 📄 许可证

本项目仅供学习和个人使用。

## 📞 支持

如有问题，请查看文档或提交 Issue。

---

**最后更新**: 2026-01-23
