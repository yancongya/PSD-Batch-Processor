"""
测试 PyQt-Fluent-Widgets 安装和基本功能
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

def test_imports():
    """测试导入"""
    print("测试导入...")

    try:
        import PyQt5
        print("  [OK] PyQt5")
    except ImportError as e:
        print(f"  [ERROR] PyQt5: {e}")
        return False

    try:
        from PyQtFluentWidgets import FluentWindow
        print("  [OK] PyQt-Fluent-Widgets")
    except ImportError as e:
        print(f"  [ERROR] PyQt-Fluent-Widgets: {e}")
        return False

    try:
        from PyQt5.QtWidgets import QApplication
        print("  [OK] PyQt5.QtWidgets")
    except ImportError as e:
        print(f"  [ERROR] PyQt5.QtWidgets: {e}")
        return False

    try:
        from PyQtFluentWidgets import FluentWindow
        print("  [OK] PyQtFluentWidgets.FluentWindow")
    except ImportError as e:
        print(f"  [ERROR] PyQtFluentWidgets.FluentWindow: {e}")
        return False

    return True

def test_basic_ui():
    """测试基本 UI 创建"""
    print("\n测试基本 UI 创建...")

    try:
        from PyQt5.QtWidgets import QApplication
        from PyQtFluentWidgets import FluentWindow, SubtitleLabel

        # 创建应用
        app = QApplication(sys.argv)

        # 创建主窗口
        window = FluentWindow()
        window.setWindowTitle("测试窗口")
        window.resize(800, 600)

        # 创建测试界面
        test_widget = SubtitleLabel("PyQt-Fluent-Widgets 测试成功!")
        window.addSubInterface(test_widget, None, "测试")

        print("  [OK] 窗口创建成功")

        # 关闭窗口
        window.close()
        app.quit()

        print("  [OK] 窗口关闭成功")

        return True

    except Exception as e:
        print(f"  [ERROR] UI 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_components():
    """测试应用组件"""
    print("\n测试应用组件...")

    try:
        # 测试配置
        from app.config.settings import init_settings
        settings = init_settings()
        print("  [OK] 配置模块")

        # 测试日志
        from utils.logger import init_logger
        logger = init_logger()
        print("  [OK] 日志模块")

        # 测试处理器
        from app.core.processor import BatchProcessor
        processor = BatchProcessor()
        print("  [OK] 处理器模块")

        # 测试模型
        from app.models.file_item import FileItem, FileStatus
        print("  [OK] 模型模块")

        return True

    except Exception as e:
        print(f"  [ERROR] 组件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("PyQt-Fluent-Widgets 测试工具")
    print("=" * 60)
    print()

    success = True

    # 测试导入
    if not test_imports():
        success = False

    # 测试 UI 创建
    if not test_basic_ui():
        success = False

    # 测试应用组件
    if not test_app_components():
        success = False

    print("\n" + "=" * 60)
    if success:
        print("✅ 所有测试通过！PyQt-Fluent-Widgets 版本可以正常运行")
    else:
        print("❌ 测试失败，请检查依赖安装")
    print("=" * 60)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())