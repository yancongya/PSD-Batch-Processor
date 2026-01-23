"""
PSD Batch Processor 主程序入口

使用 PyQt-Fluent-Widgets 的现代化 GUI 应用程序
通过 COM 接口控制 Photoshop 执行 JSX 脚本
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))


def check_dependencies():
    """检查依赖是否安装"""
    missing = []

    # 检查 PyQt5
    try:
        import PyQt5
    except ImportError:
        missing.append("PyQt5")

    # 检查 PyQt-Fluent-Widgets
    try:
        from qfluentwidgets import FluentWindow
    except ImportError:
        missing.append("PyQt-Fluent-Widgets")

    # 检查 pywin32
    try:
        import win32com.client
    except ImportError:
        missing.append("pywin32")

    if missing:
        print("=" * 60)
        print("错误：缺少必要的依赖包")
        print("=" * 60)
        print(f"缺少的包: {', '.join(missing)}")
        print("\n请运行以下命令安装依赖:")
        print("  pip install PyQt5 PyQt-Fluent-Widgets pywin32")
        print("=" * 60)
        return False
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("PSD Batch Processor")
    print("PSD 批量处理器 - PyQt-Fluent-Widgets 版本")
    print("=" * 60)
    print(f"Python 版本: {sys.version}")
    print(f"工作目录: {Path.cwd()}")
    print("=" * 60)

    # 检查依赖
    if not check_dependencies():
        input("\n按回车键退出...")
        return 1

    # 设置高 DPI 支持
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    try:
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication
        from app.ui.fluent_main_window_v2 import FluentMainWindowV2

        print("\n[OK] 依赖检查通过")
        print("[INFO] 正在启动 PyQt-Fluent-Widgets 应用程序...")

        # 设置高DPI支持
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # 创建应用
        app = QApplication(sys.argv)

        # 设置应用信息
        app.setApplicationName("PSD Batch Processor")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("PSD Processor")

        # 创建并显示主窗口
        window = FluentMainWindowV2()
        window.show()

        print("[OK] 界面初始化完成")
        print("[INFO] 开始主事件循环")
        print("=" * 60)

        # 启动主循环
        exit_code = app.exec_()

        return exit_code

    except Exception as e:
        print(f"\n[ERROR] 启动应用程序时出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
