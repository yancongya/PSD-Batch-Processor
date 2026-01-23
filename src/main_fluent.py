"""
PyQt-Fluent-Widgets 版 PSD Batch Processor 启动脚本

使用现代化的 Fluent Design 界面
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

def check_dependencies():
    """检查依赖是否安装"""
    missing_deps = []

    # 检查 PyQt5
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")

    # 检查 PyQt-Fluent-Widgets
    try:
        from PyQtFluentWidgets import FluentWindow
    except ImportError:
        missing_deps.append("PyQt-Fluent-Widgets")

    # 检查 pywin32
    try:
        import win32com.client
    except ImportError:
        missing_deps.append("pywin32")

    # 检查 customtkinter (可选，保留兼容性)
    try:
        import customtkinter
    except ImportError:
        print("[WARNING] customtkinter 未安装，但不影响 PyQt 版本运行")

    if missing_deps:
        print("[ERROR] 缺少必要的依赖:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n请安装缺失的依赖:")
        print("  pip install PyQt5 PyQt-Fluent-Widgets pywin32")
        return False

    return True


def main():
    """主函数"""
    print("=" * 60)
    print("PSD Batch Processor - PyQt-Fluent-Widgets 版本")
    print("=" * 60)
    print()

    # 检查依赖
    if not check_dependencies():
        input("\n按回车键退出...")
        return 1

    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("[ERROR] 需要 Python 3.8 或更高版本")
        print(f"当前版本: {sys.version}")
        input("\n按回车键退出...")
        return 1

    print("[OK] 依赖检查通过")
    print(f"[INFO] Python 版本: {sys.version}")
    print(f"[INFO] 工作目录: {Path.cwd()}")
    print(f"[INFO] 源码目录: {src_dir}")
    print()

    # 设置高 DPI 支持
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    try:
        # 导入并启动应用
        from app.ui.fluent_main_window import main as run_fluent_app

        print("[INFO] 正在启动 PyQt-Fluent-Widgets 版本...")
        print("[INFO] 这可能需要几秒钟时间...")
        print()

        run_fluent_app()

    except Exception as e:
        print(f"\n[ERROR] 启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())