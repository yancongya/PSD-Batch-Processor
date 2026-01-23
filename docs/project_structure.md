
# 项目文件结构

```
PSD Batch Processor/
├── src/                          # 源代码
│   ├── main.py                   # 主程序入口
│   ├── app/                      # 应用程序
│   │   ├── config/               # 配置管理
│   │   │   ├── __init__.py
│   │   │   └── settings.py       # 设置管理
│   │   ├── core/                 # 核心逻辑
│   │   │   ├── __init__.py
│   │   │   ├── photoshop_controller.py  # Photoshop 控制器
│   │   │   ├── processor.py              # 批量处理器
│   │   │   └── script_args.py            # 脚本参数传递
│   │   ├── models/               # 数据模型
│   │   │   ├── __init__.py
│   │   │   └── file_item.py              # 文件项模型
│   │   └── ui/                   # 用户界面
│   │       ├── __init__.py
│   │       └── main_window.py            # 主窗口
│   └── utils/                    # 工具模块
│       ├── __init__.py
│       └── logger.py                     # 日志工具
│
├── scripts/                      # JSX 脚本
│   ├── templates/                # 模板脚本（用于创建新脚本）
│   │   └── auto_mode_template.jsx
│   ├── examples/                 # 示例脚本（演示功能）
│   │   ├── example_resize_50_percent.jsx
│   │   ├── example_convert_to_grayscale.jsx
│   │   └── example_flatten_image.jsx
│   └── production/               # 生产脚本（实际使用）
│       └── PsDeepCleaner.jsx
│
├── docs/                         # 文档
│   ├── guides/                   # 指南文档
│   │   ├── quick_start.md        # 快速开始
│   │   ├── AUTO_MODE_GUIDE.md    # 自动模式指南
│   │   ├── REMOVE_DIALOGS_GUIDE.md  # 脚本修改指南
│   │   ├── QUICK_REFERENCE.txt   # 快速参考
│   │   └── START_HERE.txt        # 从这里开始
│   ├── archive/                  # 归档文档
│   │   ├── AUTO_MODE_FIX_SUMMARY.md
│   │   ├── QUICK_FIX_SUMMARY.md
│   │   ├── UI_SIMPLIFICATION_SUMMARY.md
│   │   ├── checklist.md
│   │   ├── development_summary.md
│   │   ├── todo.md
│   │   ├── 快速参考.txt
│   │   ├── 使用说明.txt
│   │   ├── 文件清单.txt
│   │   └── 项目状态.txt
│   ├── project_overview.md       # 项目概览
│   └── project_structure.md      # 项目结构
│
├── tests/                        # 测试文件
│   ├── test_env.py              # 环境测试
│   ├── test_auto_mode.py        # 自动模式测试
│   └── quick_test.py            # 快速测试
│
├── tools/                        # 工具脚本
│   ├── install.bat              # 安装脚本
│   └── run.bat                  # 运行脚本
│
├── backups/                      # 备份目录（自动生成）
│
├── config.json                   # 配置文件（运行时生成）
│
├── requirements.txt              # Python 依赖
├── README.md                     # 项目说明
│
└── organize_project.py           # 项目整理脚本（本文件）
```

## 文件分类说明

### 源代码 (src/)
- **app/**: 应用程序核心代码
  - **config/**: 配置管理
  - **core/**: 核心业务逻辑
  - **models/**: 数据模型
  - **ui/**: 用户界面
- **utils/**: 工具函数和辅助类

### 脚本 (scripts/)
- **templates/**: 模板脚本，用于创建新脚本
- **examples/**: 示例脚本，演示功能用法
- **production/**: 生产环境使用的脚本

### 文档 (docs/)
- **guides/**: 使用指南和教程
- **archive/**: 历史文档和归档资料

### 测试 (tests/)
- 环境测试、功能测试、快速测试

### 工具 (tools/)
- 安装、运行等辅助脚本

## 使用说明

### 开发新功能
1. 在 `src/app/` 对应模块中添加代码
2. 在 `tests/` 中添加测试
3. 在 `docs/guides/` 中更新文档

### 添加新脚本
1. 参考 `scripts/templates/auto_mode_template.jsx`
2. 在 `scripts/examples/` 中创建示例
3. 如需生产使用，复制到 `scripts/production/`

### 查看文档
1. 新手：从 `docs/guides/START_HERE.txt` 开始
2. 快速参考：`docs/guides/QUICK_REFERENCE.txt`
3. 详细指南：查看 `docs/guides/` 目录
