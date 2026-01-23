#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt-Fluent-Widgets 版本启动器

快速启动现代化界面的 PSD Batch Processor
"""

import sys
import os
import subprocess
from pathlib import Path

def get_project_dir():
    """获取项目目录"""
    return Path(__file__).parent.parent

def check_python():
    """检查 Python"""
    try:
        version = subprocess.check_output(["python", "--version"],
                                         stderr=subprocess.STDOUT).decode().strip()
        print(f"[OK] {version}")
        return True
    except:
        print("[ERROR] Python 未找到！")
        print("请安装 Python 3.8+ 并添加到 PATH")
        return False

def install_dependencies():
    """安装依赖"""
    print("\n检查依赖...")

    try:
        import PyQt5
        print("[OK] PyQt5 已安装")
    except ImportError:
        print("[WARNING] PyQt5 未安装，正在安装...")
        subprocess.run(["pip", "install", "PyQt5"], check=True)

    try:
        import PyQtFluentWidgets
        print("[OK] PyQt-Fluent-Widgets 已安装")
    except ImportError:
        print("[WARNING] PyQt-Fluent-Widgets 未安装，正在安装...")
        subprocess.run(["pip", "install", "PyQt-Fluent-Widgets"], check=True)

    try:
        import win32com.client
        print("[OK] pywin32 已安装")
    except ImportError:
        print("[WARNING] pywin32 未安装，正在安装...")
        subprocess.run(["pip", "install", "pywin32"], check=True)

def main():
    """主函数"""
    print("=" * 60)
    print("PSD Batch Processor - PyQt-Fluent-Widgets 启动器")
    print("=" * 60)

    # 获取项目目录
    project_dir = get_project_dir()
    print(f"\n项目目录: {project_dir}")

    # 检查 Python
    print("\n检查 Python...")
    if not check_python():
        input("\n按回车键退出...")
        return 1

    # 安装依赖
    try:
        install_dependencies()
    except Exception as e:
        print(f"\n[ERROR] 依赖安装失败: {e}")
        input("\n按回车键退出...")
        return 1

    # 切换到项目目录
    os.chdir(project_dir)

    # 添加 src 到 Python 路径
    src_dir = project_dir / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    print("\n" + "=" * 60)
    print("启动 PyQt-Fluent-Widgets 版本...")
    print("=" * 60)

    try:
        # 导入并运行主程序
        from main_fluent import main as run_app
        return run_app()
    except Exception as e:
        print(f"\n[ERROR] 启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        return 1

if __name__ == "__main__":
    sys.exit(main())