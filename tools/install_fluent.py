#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt-Fluent-Widgets 依赖安装脚本

自动安装 PyQt-Fluent-Widgets 版本所需的所有依赖
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """运行命令"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  [OK] {description} 成功")
            if result.stdout:
                print(f"  输出: {result.stdout.strip()}")
            return True
        else:
            print(f"  [ERROR] {description} 失败")
            if result.stderr:
                print(f"  错误: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  [ERROR] {description} 异常: {e}")
        return False

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")

    if version < (3, 8):
        print("[ERROR] 需要 Python 3.8 或更高版本")
        return False

    print("[OK] Python 版本符合要求")
    return True

def install_pip_package(package, version=None):
    """安装 pip 包"""
    if version:
        pkg = f"{package}=={version}"
    else:
        pkg = package

    print(f"\n安装 {pkg}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"  [OK] {pkg} 安装成功")
            return True
        else:
            print(f"  [ERROR] {pkg} 安装失败")
            print(f"  错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"  [ERROR] 安装异常: {e}")
        return False

def check_installed(package):
    """检查包是否已安装"""
    try:
        if package == "PyQt-Fluent-Widgets":
            from PyQtFluentWidgets import FluentWindow
        elif package == "pywin32":
            import win32com.client
        else:
            __import__(package)
        return True
    except ImportError:
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("PyQt-Fluent-Widgets 依赖安装脚本")
    print("=" * 60)

    # 检查 Python 版本
    if not check_python_version():
        input("\n按回车键退出...")
        return 1

    # 需要安装的包
    packages = [
        ("PyQt5", None, "PyQt5 框架"),
        ("PyQt-Fluent-Widgets", None, "PyQt-Fluent-Widgets 组件库"),
        ("pywin32", None, "Windows COM 支持"),
        ("Pillow", None, "图像处理支持"),
    ]

    # 检查已安装的包
    print("\n检查已安装的包...")
    installed = []
    missing = []

    for pkg, version, desc in packages:
        if check_installed(pkg):
            print(f"  [OK] {pkg} - {desc}")
            installed.append((pkg, desc))
        else:
            print(f"  [MISSING] {pkg} - {desc}")
            missing.append((pkg, version, desc))

    print(f"\n已安装: {len(installed)} 个")
    print(f"待安装: {len(missing)} 个")

    if not missing:
        print("\n✅ 所有依赖已安装，可以开始使用 PyQt-Fluent-Widgets 版本！")
        print("\n启动命令:")
        print("  python tools\\run_fluent.py")
        input("\n按回车键退出...")
        return 0

    # 确认安装
    print("\n将安装以下包:")
    for pkg, version, desc in missing:
        if version:
            print(f"  - {pkg}=={version} ({desc})")
        else:
            print(f"  - {pkg} ({desc})")

    confirm = input("\n是否继续安装? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是', 'y']:
        print("安装已取消")
        return 1

    # 安装缺失的包
    print("\n" + "=" * 60)
    print("开始安装依赖...")
    print("=" * 60)

    success_count = 0
    for pkg, version, desc in missing:
        if install_pip_package(pkg, version):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"安装完成: {success_count}/{len(missing)} 个包安装成功")
    print("=" * 60)

    if success_count == len(missing):
        print("\n✅ 所有依赖安装成功！")
        print("\n现在可以启动 PyQt-Fluent-Widgets 版本:")
        print("  python tools\\run_fluent.py")

        # 测试导入
        print("\n测试导入...")
        try:
            import PyQt5
            import PyQtFluentWidgets
            print("  [OK] PyQt5 导入成功")
            print("  [OK] PyQt-Fluent-Widgets 导入成功")
            print("\n🎉 准备就绪！可以开始使用了！")
        except ImportError as e:
            print(f"  [WARNING] 导入测试失败: {e}")
            print("  请重新启动终端或检查安装")
    else:
        print(f"\n⚠️  {len(missing) - success_count} 个包安装失败")
        print("请检查错误信息并手动安装")

    input("\n按回车键退出...")
    return 0 if success_count == len(missing) else 1

if __name__ == "__main__":
    sys.exit(main())