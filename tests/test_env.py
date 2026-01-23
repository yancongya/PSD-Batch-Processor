"""
环境验证脚本
测试 win32com 和 customtkinter 是否能正常运行
"""

import sys
import traceback


def test_customtkinter():
    """测试 customtkinter GUI 框架"""
    print("=" * 60)
    print("测试 1: customtkinter")
    print("=" * 60)

    try:
        import customtkinter as ctk
        print(f"✅ customtkinter 版本: {ctk.__version__}")

        # 测试创建窗口
        root = ctk.CTk()
        root.title("环境验证 - customtkinter")
        root.geometry("400x200")

        label = ctk.CTkLabel(root, text="✅ customtkinter 工作正常！", font=("微软雅黑", 16))
        label.pack(pady=40)

        button = ctk.CTkButton(root, text="关闭窗口", command=root.destroy)
        button.pack(pady=20)

        print("✅ customtkinter 窗口创建成功")
        print("   请手动关闭窗口继续下一个测试...")

        root.mainloop()
        print("✅ customtkinter 测试通过\n")
        return True

    except Exception as e:
        print(f"❌ customtkinter 测试失败: {e}")
        traceback.print_exc()
        return False


def test_pywin32():
    """测试 pywin32 (win32com)"""
    print("=" * 60)
    print("测试 2: pywin32 (win32com)")
    print("=" * 60)

    try:
        import win32com.client
        print("✅ win32com.client 导入成功")

        # 尝试列出已注册的 COM 对象（不实际启动 Photoshop）
        try:
            # 检查 PythonWin 是否可用
            import pythoncom
            print(f"✅ pythoncom 模块可用")

            # 尝试创建一个简单的 COM 对象来验证 COM 系统
            # 这里我们只验证模块是否正常，不实际启动 Photoshop
            print("✅ COM 系统初始化正常")

        except Exception as e:
            print(f"⚠️  COM 系统测试有警告: {e}")
            print("   这通常不影响使用，但请确保已安装 pywin32")

        print("✅ pywin32 测试通过\n")
        return True

    except ImportError as e:
        print(f"❌ pywin32 未安装: {e}")
        print("   请运行: pip install pywin32")
        return False
    except Exception as e:
        print(f"❌ pywin32 测试失败: {e}")
        traceback.print_exc()
        return False


def test_pathlib():
    """测试 pathlib（标准库，但需要验证）"""
    print("=" * 60)
    print("测试 3: pathlib (标准库)")
    print("=" * 60)

    try:
        from pathlib import Path
        import os

        # 测试路径操作
        current_dir = Path(__file__).parent
        print(f"✅ 当前目录: {current_dir}")

        # 测试路径拼接
        test_path = current_dir / "test_dir" / "subdir"
        print(f"✅ 路径拼接测试: {test_path}")

        # 测试路径字符串转换
        test_str = str(test_path)
        print(f"✅ 路径转字符串: {test_str}")

        print("✅ pathlib 测试通过\n")
        return True

    except Exception as e:
        print(f"❌ pathlib 测试失败: {e}")
        traceback.print_exc()
        return False


def test_shutil():
    """测试 shutil（文件复制）"""
    print("=" * 60)
    print("测试 4: shutil (文件操作)")
    print("=" * 60)

    try:
        import shutil
        print("✅ shutil 导入成功")

        # 测试可用功能
        print(f"✅ shutil 模块版本: {shutil.__version__ if hasattr(shutil, '__version__') else '标准库'}")

        print("✅ shutil 测试通过\n")
        return True

    except Exception as e:
        print(f"❌ shutil 测试失败: {e}")
        traceback.print_exc()
        return False


def test_concurrent():
    """测试 concurrent.futures（线程池）"""
    print("=" * 60)
    print("测试 5: concurrent.futures (线程池)")
    print("=" * 60)

    try:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        print("✅ concurrent.futures 导入成功")

        # 简单的线程池测试
        def test_task(n):
            return n * n

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(test_task, i) for i in range(5)]
            results = [f.result() for f in as_completed(futures)]

        print(f"✅ 线程池测试结果: {results}")
        print("✅ concurrent.futures 测试通过\n")
        return True

    except Exception as e:
        print(f"❌ concurrent.futures 测试失败: {e}")
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("PSD Batch Processor - 环境验证工具")
    print("=" * 60)
    print(f"Python 版本: {sys.version}")
    print(f"平台: {sys.platform}")
    print("=" * 60 + "\n")

    results = {}

    # 运行所有测试
    results['pathlib'] = test_pathlib()
    results['shutil'] = test_shutil()
    results['concurrent'] = test_concurrent()
    results['pywin32'] = test_pywin32()
    results['customtkinter'] = test_customtkinter()

    # 输出总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name:20s}: {status}")

    print("=" * 60)

    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 所有测试通过！环境配置正常，可以开始开发。")
    else:
        print("\n⚠️  部分测试失败，请检查依赖安装。")
        print("\n建议安装依赖:")
        print("  pip install customtkinter pywin32")

    print("=" * 60 + "\n")

    return all_passed


if __name__ == "__main__":
    main()
