"""
测试 PyQt-Fluent-Widgets V2 版本
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

def test_import():
    """测试导入"""
    print("测试导入...")

    try:
        from PyQt5.QtWidgets import QApplication
        print("  [OK] PyQt5.QtWidgets")
    except ImportError as e:
        print(f"  [ERROR] PyQt5.QtWidgets: {e}")
        return False

    try:
        from qfluentwidgets import FluentWindow
        print("  [OK] qfluentwidgets.FluentWindow")
    except ImportError as e:
        print(f"  [ERROR] qfluentwidgets: {e}")
        return False

    try:
        from app.ui.fluent_main_window_v2 import FluentMainWindowV2
        print("  [OK] app.ui.fluent_main_window_v2.FluentMainWindowV2")
    except ImportError as e:
        print(f"  [ERROR] fluent_main_window_v2: {e}")
        return False

    return True

def test_window_creation():
    """测试窗口创建"""
    print("\n测试窗口创建...")

    try:
        from PyQt5.QtWidgets import QApplication
        from app.ui.fluent_main_window_v2 import FluentMainWindowV2

        # 创建应用（不显示）
        app = QApplication(sys.argv)

        # 创建主窗口
        window = FluentMainWindowV2()
        print("  [OK] V2 窗口创建成功")

        # 检查关键组件
        assert hasattr(window, 'process_interface'), "缺少文件处理界面"
        assert hasattr(window, 'script_interface'), "缺少脚本管理界面"
        assert hasattr(window, 'settings_interface'), "缺少设置界面"
        assert hasattr(window, 'log_interface'), "缺少日志界面"
        print("  [OK] 所有界面组件存在")

        # 检查关键控件
        assert hasattr(window, 'file_tree'), "缺少文件列表"
        assert hasattr(window, 'script_combo'), "缺少脚本下拉框"
        assert hasattr(window, 'script_tree'), "缺少脚本树形列表"
        assert hasattr(window, 'start_btn'), "缺少开始按钮"
        print("  [OK] 所有关键控件存在")

        # 关闭窗口
        window.close()
        app.quit()

        print("  [OK] 窗口关闭成功")
        return True

    except Exception as e:
        print(f"  [ERROR] 窗口创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("PyQt-Fluent-Widgets V2 版本测试")
    print("=" * 60)
    print()

    success = True

    # 测试导入
    if not test_import():
        success = False

    # 测试窗口创建
    if success:
        if not test_window_creation():
            success = False

    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] PyQt-Fluent-Widgets V2 版本测试通过！")
        print("\n新界面特性:")
        print("  - 文件处理: 专门的文件处理页面")
        print("  - 脚本管理: 独立的脚本浏览和管理")
        print("  - 设置: 集中配置管理")
        print("  - 日志: 完整日志查看")
        print("\n启动命令:")
        print("  cd 'F:\\插件脚本开发\\PSD Batch Processor\\src'")
        print("  python main_fluent.py")
    else:
        print("[ERROR] PyQt-Fluent-Widgets V2 版本测试失败")
    print("=" * 60)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())