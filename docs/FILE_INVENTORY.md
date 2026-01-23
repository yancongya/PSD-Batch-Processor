# 文件清单

## 📦 项目文件总览

### 源代码 (src/)
```
src/
├── main.py                                    # 主程序入口 (70 行)
│
├── app/
│   ├── __init__.py                            # 包初始化
│   ├── config/
│   │   ├── __init__.py                        # 包初始化
│   │   ├── settings.py                        # 设置管理 (180 行)
│   │   └── config.json                        # 配置文件 (运行时生成)
│   ├── core/
│   │   ├── __init__.py                        # 包初始化
│   │   ├── photoshop_controller.py            # Photoshop 控制器 (200 行)
│   │   ├── processor.py                       # 批量处理器 (320 行)
│   │   └── script_args.py                     # 脚本参数传递 (270 行)
│   ├── models/
│   │   ├── __init__.py                        # 包初始化
│   │   └── file_item.py                       # 文件项模型 (200 行)
│   └── ui/
│       ├── __init__.py                        # 包初始化
│       └── main_window.py                     # 主窗口 (650 行)
│
└── utils/
    ├── __init__.py                            # 包初始化
    └── logger.py                              # 日志工具 (140 行)
```

### 脚本文件 (scripts/)
```
scripts/
├── templates/                                  # 模板脚本
│   └── auto_mode_template.jsx                 # 自动模式模板 (177 行)
│
├── examples/                                   # 示例脚本
│   ├── example_resize_50_percent.jsx          # 缩放 50% (103 行)
│   ├── example_convert_to_grayscale.jsx       # 转换为灰度 (97 行)
│   ├── example_flatten_image.jsx              # 压平图像 (97 行)
│   └── example_auto_flatten.jsx               # 自动压平 (97 行)
│
└── production/                                 # 生产脚本
    └── PsDeepCleaner.jsx                      # 元数据清理 (148 行)
```

### 文档文件 (docs/)
```
docs/
├── guides/                                     # 指南文档
│   ├── START_HERE.txt                         # 从这里开始 (纯文本)
│   ├── quick_start.md                         # 快速开始
│   ├── QUICK_REFERENCE.txt                    # 快速参考 (纯文本)
│   ├── AUTO_MODE_GUIDE.md                     # 自动模式指南
│   └── REMOVE_DIALOGS_GUIDE.md                # 脚本修改指南
│
├── archive/                                    # 归档文档
│   ├── AUTO_MODE_FIX_SUMMARY.md               # 自动模式修复总结
│   ├── QUICK_FIX_SUMMARY.md                   # 快速修复总结
│   ├── UI_SIMPLIFICATION_SUMMARY.md           # UI 简化总结
│   ├── PROJECT_CLEANUP_COMPLETE.md            # 整理完成总结
│   ├── checklist.md                           # 检查清单
│   ├── development_summary.md                 # 开发总结
│   ├── todo.md                                # 待办事项
│   ├── 快速参考.txt                           # 旧文档
│   ├── 使用说明.txt                           # 旧文档
│   ├── 文件清单.txt                           # 旧文档
│   └── 项目状态.txt                           # 旧文档
│
├── project_overview.md                        # 项目概览
├── project_structure.md                       # 项目结构
├── PROJECT_REORGANIZATION_SUMMARY.md          # 整理总结
├── PROJECT_STATUS.md                          # 项目状态
├── PACKAGING_GUIDE.md                         # 打包指南
├── QUICK_PACKAGING.md                         # 快速打包
└── FRONTEND_UI_OPTIONS.md                     # 前端 UI 方案
```

### 测试文件 (tests/)
```
tests/
├── test_env.py                                # 环境测试 (180 行)
├── test_auto_mode.py                          # 自动模式测试 (182 行)
└── quick_test.py                              # 快速测试
```

### 工具文件 (tools/)
```
tools/
├── install.bat                                # 安装脚本
├── run.bat                                    # 运行脚本
├── build.bat                                  # 打包脚本 (Windows)
└── build.py                                   # 打包脚本 (Python)
```

### 根目录文件
```
PSD Batch Processor/
├── README.md                                  # 项目说明
├── requirements.txt                           # Python 依赖
├── organize_project.py                        # 项目整理脚本 (478 行)
└── docs/                                      # 文档目录
```

## 📊 文件统计

### 按类型统计
| 类型 | 数量 | 说明 |
|------|------|------|
| Python 源代码 | 12 | 核心功能 |
| JSX 脚本 | 6 | Photoshop 脚本 |
| Markdown 文档 | 15 | 详细文档 |
| 纯文本文档 | 7 | 快速参考 |
| 测试文件 | 3 | 单元测试 |
| 工具脚本 | 4 | 辅助工具 |
| 配置文件 | 2 | 依赖和配置 |

### 按目录统计
| 目录 | 文件数 | 说明 |
|------|--------|------|
| src/ | 12 | 源代码 |
| scripts/ | 6 | 脚本文件 |
| docs/ | 22 | 文档 |
| tests/ | 3 | 测试 |
| tools/ | 4 | 工具 |
| 根目录 | 3 | 配置和说明 |

### 代码行数估算
| 类型 | 行数 | 说明 |
|------|------|------|
| Python 代码 | ~2000 | 核心逻辑 |
| JSX 脚本 | ~500 | Photoshop 脚本 |
| 文档内容 | ~3000 | 详细说明 |
| 配置文件 | ~50 | 依赖配置 |

## 📝 重要文件说明

### 核心文件（必须保留）

#### 主程序
- **src/main.py** - 程序入口，启动 GUI

#### 配置管理
- **src/app/config/settings.py** - 设置管理
- **src/app/config/config.json** - 配置文件（运行时生成）

#### 核心逻辑
- **src/app/core/photoshop_controller.py** - Photoshop 控制器
- **src/app/core/processor.py** - 批量处理器
- **src/app/core/script_args.py** - 脚本参数传递

#### 数据模型
- **src/app/models/file_item.py** - 文件项模型

#### 用户界面
- **src/app/ui/main_window.py** - 主窗口

#### 工具模块
- **src/utils/logger.py** - 日志工具

### 脚本文件（按需使用）

#### 生产脚本
- **scripts/production/PsDeepCleaner.jsx** - 元数据清理（已优化）

#### 示例脚本
- **scripts/examples/*.jsx** - 功能演示

#### 模板脚本
- **scripts/templates/auto_mode_template.jsx** - 创建新脚本的模板

### 文档文件（按需查阅）

#### 快速入门
- **docs/guides/START_HERE.txt** - 从这里开始（必读）
- **docs/guides/quick_start.md** - 快速开始
- **docs/guides/QUICK_REFERENCE.txt** - 快速参考

#### 高级指南
- **docs/guides/AUTO_MODE_GUIDE.md** - 自动模式指南
- **docs/guides/REMOVE_DIALOGS_GUIDE.md** - 脚本修改指南

#### 项目信息
- **docs/project_structure.md** - 项目结构
- **docs/PROJECT_STATUS.md** - 项目状态
- **docs/FRONTEND_UI_OPTIONS.md** - 前端 UI 方案

#### 打包指南
- **docs/QUICK_PACKAGING.md** - 快速打包
- **docs/PACKAGING_GUIDE.md** - 详细打包指南

### 工具文件（按需使用）

#### 运行工具
- **tools/run.bat** - 运行程序
- **tools/install.bat** - 安装依赖

#### 打包工具
- **tools/build.py** - Python 打包脚本
- **tools/build.bat** - Windows 打包脚本

## 🔧 配置文件

### Python 依赖 (requirements.txt)
```
customtkinter>=5.2.2
pywin32>=306
pillow>=9.0.0
```

### 配置文件 (config.json)
首次运行自动生成：
```json
{
  "photoshop_path": "",
  "script_dir": "",
  "backup_dir": "backups",
  "last_script": "",
  "max_workers": 1,
  "include_subfolders": false,
  "theme": "dark"
}
```

## 📦 打包文件

### 打包结果
```
dist/PSDBatchProcessor/
├── PSDBatchProcessor.exe          # 主程序 (60-80 MB)
├── README.md                      # 项目说明
├── docs/
│   └── guides/
│       ├── START_HERE.txt         # 快速开始
│       └── QUICK_REFERENCE.txt    # 快速参考
└── (其他依赖文件)
```

### 打包脚本
- **tools/build.py** - 推荐使用
- **tools/build.bat** - Windows 专用

## 🗑️ 可删除文件

### 开发过程中生成
- `__pycache__/` - Python 缓存
- `build/` - PyInstaller 构建目录
- `*.spec` - PyInstaller spec 文件

### 旧文件（已归档）
- `docs/archive/` 中的旧文档
- `organize_project.py` - 整理脚本（已完成）

### 测试文件（可选）
- `tests/` - 如果不需要测试可以删除

## 📋 文件完整性检查

### 必须存在的文件
- [x] src/main.py
- [x] src/app/config/settings.py
- [x] src/app/core/photoshop_controller.py
- [x] src/app/core/processor.py
- [x] src/app/core/script_args.py
- [x] src/app/models/file_item.py
- [x] src/app/ui/main_window.py
- [x] src/utils/logger.py
- [x] scripts/production/PsDeepCleaner.jsx
- [x] docs/guides/START_HERE.txt
- [x] tools/run.bat
- [x] requirements.txt
- [x] README.md

### 推荐存在的文件
- [x] scripts/templates/auto_mode_template.jsx
- [x] scripts/examples/*.jsx
- [x] docs/guides/*.md
- [x] tests/*.py
- [x] tools/build.py
- [x] docs/PACKAGING_GUIDE.md

## 💡 文件使用建议

### 开发阶段
1. **核心代码**：`src/` 目录
2. **测试验证**：`tests/` 目录
3. **文档编写**：`docs/guides/` 目录
4. **脚本开发**：`scripts/examples/` 目录

### 打包阶段
1. **运行打包**：`python tools/build.py`
2. **测试 EXE**：`dist/PSDBatchProcessor/PSDBatchProcessor.exe`
3. **分发**：压缩 `dist/PSDBatchProcessor/` 文件夹

### 用户使用
1. **运行程序**：双击 EXE 文件
2. **查看文档**：`docs/guides/START_HERE.txt`
3. **配置路径**：按照界面提示操作
4. **开始处理**：添加文件并运行

## 🎯 文件组织原则

### 1. 功能分离
- 源代码 → `src/`
- 脚本 → `scripts/`
- 文档 → `docs/`
- 测试 → `tests/`
- 工具 → `tools/`

### 2. 分类清晰
- 脚本：模板/示例/生产
- 文档：指南/归档
- 测试：环境/功能/快速

### 3. 易于查找
- 常用文档在 `guides/`
- 历史文档在 `archive/`
- 核心代码在 `src/app/`

### 4. 便于维护
- 模块化设计
- 清晰的命名
- 完整的文档

---

**文件清单完成！** 📋

现在项目的所有文件都有清晰的分类和说明，便于管理和使用！