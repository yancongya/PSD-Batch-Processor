#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSD Batch Processor 打包脚本
将项目打包为独立的 EXE 文件
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def get_project_dir():
    """获取项目根目录"""
    return Path(__file__).parent.parent

def check_dependencies():
    """检查依赖"""
    print("检查依赖...")

    # 检查 Python
    try:
        version = subprocess.check_output(["python", "--version"],
                                         stderr=subprocess.STDOUT).decode().strip()
        print(f"[OK] {version}")
    except:
        print("[ERROR] Python 未找到！")
        return False

    # 检查 PyInstaller
    try:
        import PyInstaller
        print("[OK] PyInstaller 已安装")
    except:
        print("[WARNING] PyInstaller 未安装，正在安装...")
        subprocess.run(["pip", "install", "pyinstaller"], check=True)

    return True

def clean_build():
    """清理旧的构建文件"""
    print("\n清理旧的构建文件...")
    project_dir = get_project_dir()

    for dir_name in ["build", "dist", "__pycache__"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"[OK] 删除 {dir_name}")

    # 删除 spec 文件
    spec_file = project_dir / "PSDBatchProcessor.spec"
    if spec_file.exists():
        spec_file.unlink()
        print("[OK] 删除 spec 文件")

def build_exe(mode="windowed"):
    """打包 EXE"""
    print(f"\n开始打包 ({mode} 模式)...")
    project_dir = get_project_dir()

    # 基础命令
    cmd = [
        "pyinstaller",
        "--name=PSDBatchProcessor",
        "--clean",
        "--noconfirm",
    ]

    # 模式选项
    if mode == "windowed":
        cmd.extend(["--noconsole"])
        # 如果有图标文件，取消注释下面这行
        # cmd.extend(["--icon=assets/icon.ico"])
    elif mode == "console":
        cmd.extend(["--console"])
        # 如果有图标文件，取消注释下面这行
        # cmd.extend(["--icon=assets/icon.ico"])
    elif mode == "onefile":
        cmd.extend(["--noconsole", "--onefile"])
        # 如果有图标文件，取消注释下面这行
        # cmd.extend(["--icon=assets/icon.ico"])

    # 添加数据文件
    # 注意：单文件模式下，脚本文件会被打包到EXE内部
    # 配置文件会存储在用户数据目录（%APPDATA%/PSDBatchProcessor）
    data_files = [
        "docs/guides/START_HERE.txt;docs/guides",
        "docs/guides/QUICK_REFERENCE.txt;docs/guides",
        "scripts/production/*.jsx;scripts/production",
        "scripts/templates/*.jsx;scripts/templates",
        "scripts/examples/*.jsx;scripts/examples",
    ]

    for data in data_files:
        cmd.extend(["--add-data", data])

    # 隐藏导入
    hidden_imports = [
        "win32com",
        "pythoncom",
        "PIL",
        "customtkinter",
    ]

    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])

    # 排除不必要的模块（加速构建，减小文件大小）
    exclude_modules = [
        # 深度学习框架
        "torch", "torchvision", "torchaudio",
        "tensorflow", "keras",
        # 科学计算
        "scipy", "numpy", "sympy",
        # ONNX
        "onnxruntime",
        # 爬虫和网页相关
        "selenium", "playwright", "requests",
        "beautifulsoup4", "lxml", "bs4",
        # 数据处理
        "pandas", "matplotlib",
        # 其他大型库
        "cv2", "opencv-python",
        # 开发工具
        "pytest", "black", "flake8",
        # AI/ML 相关
        "langchain", "openai", "anthropic",
        "transformers", "tokenizers",
        "huggingface_hub",
        # 其他
        "tkinter", "turtle",
    ]

    for mod in exclude_modules:
        cmd.extend(["--exclude-module", mod])

    # 主程序
    cmd.append(str(project_dir / "src/main.py"))

    # 执行打包
    print(f"命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(project_dir))

    if result.returncode == 0:
        print("\n[SUCCESS] 打包完成！")
        return True
    else:
        print("\n[ERROR] 打包失败！")
        return False

def show_result():
    """显示打包结果"""
    project_dir = get_project_dir()
    exe_path = project_dir / "dist" / "PSDBatchProcessor" / "PSDBatchProcessor.exe"

    if exe_path.exists():
        size = exe_path.stat().st_size
        size_mb = size / (1024 * 1024)

        print("\n" + "=" * 60)
        print("打包结果")
        print("=" * 60)
        print(f"可执行文件: {exe_path}")
        print(f"文件大小: {size_mb:.2f} MB")
        print(f"文件大小: {size:,} bytes")
        print("\n使用方法:")
        print(f"  {exe_path}")
        print("\n首次运行会自动创建:")
        print("  - backups/ 目录 (在EXE所在目录)")
        print("  - 配置文件 (在 %APPDATA%/PSDBatchProcessor/config.json)")
        print("\n脚本文件位置:")
        print("  - 内置脚本: 打包在EXE内部")
        print("  - 自定义脚本: 可以放在任意位置，通过界面设置路径")
        print("\n请按照文档配置:")
        print("  docs/guides/START_HERE.txt")
        print("=" * 60)

def copy_files():
    """复制必要文件到打包目录"""
    print("\n复制必要文件...")
    project_dir = get_project_dir()
    dist_dir = project_dir / "dist" / "PSDBatchProcessor"

    try:
        # 复制 README
        if (project_dir / "README.md").exists():
            shutil.copy2(project_dir / "README.md", dist_dir)
            print("[OK] 复制 README.md")

        # 复制快速开始文档
        guides_dir = dist_dir / "docs" / "guides"
        guides_dir.mkdir(parents=True, exist_ok=True)

        start_here = project_dir / "docs/guides/START_HERE.txt"
        if start_here.exists():
            shutil.copy2(start_here, guides_dir)
            print("[OK] 复制 START_HERE.txt")

        quick_ref = project_dir / "docs/guides/QUICK_REFERENCE.txt"
        if quick_ref.exists():
            shutil.copy2(quick_ref, guides_dir)
            print("[OK] 复制 QUICK_REFERENCE.txt")

        # 复制脚本文件（如果dist目录中没有）
        scripts_dir = dist_dir / "scripts"
        if not scripts_dir.exists():
            source_scripts = project_dir / "scripts"
            if source_scripts.exists():
                shutil.copytree(source_scripts, scripts_dir)
                print("[OK] 复制 scripts 目录")
        else:
            print("[INFO] scripts 目录已存在，跳过复制")

        # 复制备份目录模板
        backups_dir = dist_dir / "backups"
        if not backups_dir.exists():
            backups_dir.mkdir(parents=True, exist_ok=True)
            print("[OK] 创建 backups 目录")

        print("[OK] 文件复制完成")

    except Exception as e:
        print(f"[WARNING] 文件复制失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("PSD Batch Processor 打包工具")
    print("=" * 60)

    # 检查依赖
    if not check_dependencies():
        return 1

    # 选择模式
    print("\n选择打包模式:")
    print("1. 窗口模式 (推荐，无控制台)")
    print("2. 控制台模式 (调试用)")
    print("3. 单文件模式 (便携版)")
    print("4. 退出")

    choice = input("\n请输入选择 (1-4): ").strip()

    modes = {
        "1": "windowed",
        "2": "console",
        "3": "onefile",
        "4": "exit"
    }

    if choice not in modes:
        print("[ERROR] 无效选择！")
        return 1

    if modes[choice] == "exit":
        return 0

    # 清理旧文件
    clean_build()

    # 打包
    if build_exe(modes[choice]):
        # 显示结果
        show_result()

        # 复制必要文件
        copy_files()

        print("\n" + "=" * 60)
        print("🎉 打包完成！")
        print("=" * 60)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())