"""
快速测试脚本
验证项目核心模块是否能正常导入
"""

import sys
from pathlib import Path

print("=" * 60)
print("PSD Batch Processor - 快速测试")
print("=" * 60)
print()

# 测试 1: 检查 Python 版本
print("[1/6] 检查 Python 版本...")
print(f"Python 版本: {sys.version}")
if sys.version_info >= (3, 10):
    print("[OK] Python 版本符合要求 (3.10+)")
else:
    print("[警告] Python 版本低于 3.10，可能不兼容")
print()

# 测试 2: 检查目录结构
print("[2/6] 检查目录结构...")
required_dirs = ["app", "app/ui", "app/core", "app/models", "app/config", "utils", "scripts", "backups", "logs"]
missing_dirs = []
for dir_path in required_dirs:
    if not Path(dir_path).exists():
        missing_dirs.append(dir_path)

if missing_dirs:
    print(f"[错误] 缺少目录: {missing_dirs}")
else:
    print("[OK] 所有必需目录都存在")
print()

# 测试 3: 检查核心文件
print("[3/6] 检查核心文件...")
required_files = [
    "main.py",
    "app/ui/main_window.py",
    "app/core/photoshop_controller.py",
    "app/core/processor.py",
    "app/models/file_item.py",
    "app/config/settings.py",
    "utils/logger.py",
]
missing_files = []
for file_path in required_files:
    if not Path(file_path).exists():
        missing_files.append(file_path)

if missing_files:
    print(f"[错误] 缺少文件: {missing_files}")
else:
    print("[OK] 所有必需文件都存在")
print()

# 测试 4: 导入 customtkinter
print("[4/6] 测试 customtkinter 导入...")
try:
    import customtkinter as ctk
    print(f"[OK] customtkinter 导入成功，版本: {ctk.__version__}")
except ImportError as e:
    print(f"[错误] customtkinter 导入失败: {e}")
    print("  请运行: pip install customtkinter")
except Exception as e:
    print(f"[错误] customtkinter 测试失败: {e}")
print()

# 测试 5: 导入 pywin32
print("[5/6] 测试 pywin32 导入...")
try:
    import win32com.client
    import pythoncom
    print("[OK] pywin32 导入成功")
except ImportError as e:
    print(f"[错误] pywin32 导入失败: {e}")
    print("  请运行: pip install pywin32")
except Exception as e:
    print(f"[错误] pywin32 测试失败: {e}")
print()

# 测试 6: 导入项目模块
print("[6/6] 测试项目模块导入...")
try:
    # 添加当前目录到 Python 路径
    sys.path.insert(0, str(Path.cwd()))

    from app.config.settings import Settings, get_settings
    print("[OK] app.config.settings 导入成功")

    from utils.logger import Logger, get_logger
    print("[OK] utils.logger 导入成功")

    from app.models.file_item import FileItem, FileList, FileStatus
    print("[OK] app.models.file_item 导入成功")

    from app.core.photoshop_controller import PhotoshopController
    print("[OK] app.core.photoshop_controller 导入成功")

    from app.core.processor import BatchProcessor
    print("[OK] app.core.processor 导入成功")

    print("[OK] 所有项目模块导入成功")

except ImportError as e:
    print(f"[错误] 项目模块导入失败: {e}")
except Exception as e:
    print(f"[错误] 项目模块测试失败: {e}")
print()

print("=" * 60)
print("测试完成！")
print("=" * 60)
print()
print("如果所有测试都通过，可以运行: python main.py")
print("如果测试失败，请检查依赖是否正确安装")
print()
