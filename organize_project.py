#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目文件整理脚本
重新组织项目结构，使文件分类更清晰
"""

import shutil
from pathlib import Path

def create_directories():
    """创建新的目录结构"""
    base_dir = Path(__file__).parent

    directories = [
        # 源代码
        "src",
        "src/app",
        "src/app/config",
        "src/app/core",
        "src/app/models",
        "src/app/ui",
        "src/utils",

        # 脚本
        "scripts",
        "scripts/templates",      # 模板脚本
        "scripts/examples",       # 示例脚本
        "scripts/production",     # 生产脚本

        # 文档
        "docs",
        "docs/archive",           # 归档文档
        "docs/guides",            # 指南文档

        # 测试
        "tests",

        # 工具
        "tools",

        # 备份
        "backups",
    ]

    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] 创建目录: {dir_path}")

def move_files():
    """移动文件到新的位置"""
    base_dir = Path(__file__).parent

    # 文件移动映射
    file_moves = [
        # 配置文件
        ("config.json", "src/app/config/"),

        # 核心代码
        ("app/config/settings.py", "src/app/config/"),
        ("app/core/photoshop_controller.py", "src/app/core/"),
        ("app/core/processor.py", "src/app/core/"),
        ("app/core/script_args.py", "src/app/core/"),
        ("app/models/file_item.py", "src/app/models/"),
        ("app/ui/main_window.py", "src/app/ui/"),
        ("utils/logger.py", "src/utils/"),

        # 主程序
        ("main.py", "src/"),

        # 脚本文件
        ("scripts/auto_mode_template.jsx", "scripts/templates/"),
        ("scripts/example_auto_flatten.jsx", "scripts/examples/"),
        ("scripts/example_convert_to_grayscale.jsx", "scripts/examples/"),
        ("scripts/example_flatten_image.jsx", "scripts/examples/"),
        ("scripts/example_resize_50_percent.jsx", "scripts/examples/"),
        ("scripts/PsDeepCleaner.jsx", "scripts/production/"),

        # 文档
        ("docs/AUTO_MODE_FIX_SUMMARY.md", "docs/archive/"),
        ("docs/AUTO_MODE_GUIDE.md", "docs/guides/"),
        ("docs/QUICK_FIX_SUMMARY.md", "docs/archive/"),
        ("docs/REMOVE_DIALOGS_GUIDE.md", "docs/guides/"),
        ("docs/checklist.md", "docs/archive/"),
        ("docs/development_summary.md", "docs/archive/"),
        ("docs/project_overview.md", "docs/"),
        ("docs/project_structure.md", "docs/"),
        ("docs/quick_start.md", "docs/guides/"),
        ("docs/todo.md", "docs/archive/"),
        ("docs/UI_SIMPLIFICATION_SUMMARY.md", "docs/archive/"),

        # 测试文件
        ("test_auto_mode.py", "tests/"),
        ("test_env.py", "tests/"),
        ("quick_test.py", "tests/"),

        # 工具脚本
        ("install.bat", "tools/"),
        ("run.bat", "tools/"),

        # 说明文档
        ("QUICK_REFERENCE.txt", "docs/guides/"),
        ("START_HERE.txt", "docs/guides/"),

        # 旧的中文文档（归档）
        ("快速参考.txt", "docs/archive/"),
        ("使用说明.txt", "docs/archive/"),
        ("文件清单.txt", "docs/archive/"),
        ("项目状态.txt", "docs/archive/"),
    ]

    for src, dst in file_moves:
        src_path = base_dir / src
        dst_path = base_dir / dst

        if src_path.exists():
            # 确保目标目录存在
            dst_path.mkdir(parents=True, exist_ok=True)

            # 如果是文件，移动文件
            if src_path.is_file():
                # 如果目标是目录，保持原文件名
                if dst_path.is_dir():
                    dst_file = dst_path / src_path.name
                else:
                    dst_file = dst_path

                # 移动文件
                shutil.move(str(src_path), str(dst_file))
                print(f"[OK] 移动: {src} → {dst}")
            else:
                print(f"[WARN] 跳过目录: {src}")
        else:
            print(f"[WARN] 文件不存在: {src}")

def create_init_files():
    """创建 __init__.py 文件"""
    base_dir = Path(__file__).parent

    init_files = [
        "src/app/__init__.py",
        "src/app/config/__init__.py",
        "src/app/core/__init__.py",
        "src/app/models/__init__.py",
        "src/app/ui/__init__.py",
        "src/utils/__init__.py",
    ]

    for init_file in init_files:
        full_path = base_dir / init_file
        if not full_path.exists():
            full_path.write_text("# -*- coding: utf-8 -*-\n", encoding='utf-8')
            print(f"[OK] 创建: {init_file}")

def update_imports():
    """更新导入路径"""
    base_dir = Path(__file__).parent

    # 更新 main.py
    main_py = base_dir / "src/main.py"
    if main_py.exists():
        content = main_py.read_text(encoding='utf-8')

        # 更新导入路径
        content = content.replace("from app.", "from app.")
        content = content.replace("from utils.", "from utils.")

        main_py.write_text(content, encoding='utf-8')
        print("[OK] 更新 main.py 导入路径")

def create_project_structure_doc():
    """创建项目结构文档"""
    base_dir = Path(__file__).parent

    structure = """
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
"""

    structure_doc = base_dir / "docs/project_structure.md"
    structure_doc.write_text(structure, encoding='utf-8')
    print("[OK] 创建项目结构文档")

def create_readme():
    """创建或更新 README"""
    base_dir = Path(__file__).parent

    readme_content = """
# PSD Batch Processor

一个用于批量处理 PSD 文件的 Python 应用程序，支持通过 Photoshop 脚本自动化处理。

## ✨ 功能特性

- 📁 **批量处理**: 一次处理多个 PSD 文件
- 🔄 **自动备份**: 处理前自动备份原始文件
- 🎨 **Photoshop 集成**: 通过 COM 接口控制 Photoshop
- 📝 **脚本支持**: 支持自定义 JSX 脚本
- 🎯 **无人值守**: 脚本无弹窗，完全自动化
- 📊 **实时进度**: 显示处理进度和状态
- 🌙 **主题支持**: 深色/浅色主题切换

## 🚀 快速开始

### 1. 环境要求
- Python 3.10+
- Photoshop (Windows 版本)
- Windows 操作系统

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行程序
```bash
# Windows
tools\\run.bat

# 或直接运行
python src/main.py
```

### 4. 基本使用
1. 设置 Photoshop 路径
2. 选择脚本目录和脚本
3. 添加要处理的 PSD 文件
4. 点击"开始处理"

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

### 快速入门
- [快速开始指南](docs/guides/quick_start.md)
- [从这里开始](docs/guides/START_HERE.txt)
- [快速参考](docs/guides/QUICK_REFERENCE.txt)

### 脚本开发
- [模板脚本](scripts/templates/auto_mode_template.jsx)
- [脚本修改指南](docs/guides/REMOVE_DIALOGS_GUIDE.md)
- [示例脚本](scripts/examples/)

### 高级功能
- [自动模式指南](docs/guides/AUTO_MODE_GUIDE.md)

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
"""

    readme = base_dir / "README.md"
    readme.write_text(readme_content, encoding='utf-8')
    print("[OK] 更新 README.md")

def main():
    """主函数"""
    print("=" * 60)
    print("项目文件整理工具")
    print("=" * 60)

    try:
        # 1. 创建目录结构
        print("\n1. 创建目录结构...")
        create_directories()

        # 2. 移动文件
        print("\n2. 移动文件...")
        move_files()

        # 3. 创建 __init__.py 文件
        print("\n3. 创建 __init__.py 文件...")
        create_init_files()

        # 4. 更新导入路径
        print("\n4. 更新导入路径...")
        update_imports()

        # 5. 创建项目结构文档
        print("\n5. 创建项目结构文档...")
        create_project_structure_doc()

        # 6. 更新 README
        print("\n6. 更新 README...")
        create_readme()

        print("\n" + "=" * 60)
        print("[SUCCESS] 项目整理完成！")
        print("=" * 60)
        print("\n新的项目结构：")
        print("- 源代码: src/")
        print("- 脚本: scripts/")
        print("- 文档: docs/")
        print("- 测试: tests/")
        print("- 工具: tools/")
        print("\n请查看 docs/project_structure.md 了解详细结构")

    except Exception as e:
        print(f"\n[ERROR] 整理过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()