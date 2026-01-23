"""
PSD Batch Processor 主程序入口

一个用于批量处理 Photoshop PSD 文件的 Windows GUI 应用程序
通过 COM 接口控制 Photoshop 执行 JSX 脚本
"""

import sys
from pathlib import Path


def check_dependencies():
    """检查依赖是否安装"""
    missing = []

    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")

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
        print("  pip install customtkinter pywin32")
        print("=" * 60)
        return False
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("PSD Batch Processor")
    print("PSD 批量处理器")
    print("=" * 60)
    print(f"Python 版本: {sys.version}")
    print(f"工作目录: {Path.cwd()}")
    print("=" * 60)

    # 检查依赖
    if not check_dependencies():
        input("\n按回车键退出...")
        return 1

    # 导入主窗口（在检查依赖后）
    try:
        from app.ui.main_window import MainWindow
        import customtkinter as ctk

        print("\n[OK] 依赖检查通过")
        print("[INFO] 正在启动应用程序...")

        # 设置 CTk 的 DPI 感知（Windows）
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        # 创建并显示主窗口
        app = MainWindow()
        print("[OK] 界面初始化完成")
        print("[INFO] 开始主事件循环")
        print("=" * 60)

        # 启动主循环
        app.mainloop()

        return 0

    except Exception as e:
        print(f"\n[ERROR] 启动应用程序时出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
