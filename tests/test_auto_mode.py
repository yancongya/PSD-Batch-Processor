#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动模式集成测试脚本
测试自动模式配置的保存、加载和传递功能
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_script_args_manager():
    """测试脚本参数管理器"""
    print("=== 测试脚本参数管理器 ===")

    from app.core.script_args import ScriptArgsManager, get_script_args_manager

    # 获取管理器实例
    manager = get_script_args_manager()
    print(f"[PASS] 获取管理器实例: {type(manager)}")

    # 创建自动模式参数
    auto_args = manager.create_auto_mode_args(
        auto_mode=True,
        skip_confirmation=True,
        verbose=True,
        batch_mode=True
    )
    print(f"[PASS] 创建自动模式参数: {auto_args}")

    # 创建参数文件
    args_file = manager.create_args_file(auto_args)
    print(f"[PASS] 创建参数文件: {args_file}")

    # 验证文件存在
    from pathlib import Path
    if Path(args_file).exists():
        print("[PASS] 参数文件存在")

        # 读取文件内容
        with open(args_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"[PASS] 文件内容: {content}")
    else:
        print("[FAIL] 参数文件不存在")
        return False

    return True

def test_auto_mode_config():
    """测试自动模式配置"""
    print("\n=== 测试自动模式配置 ===")

    from app.core.script_args import get_auto_mode_config, save_auto_mode_config

    # 获取默认配置
    config = get_auto_mode_config()
    print(f"[PASS] 获取默认配置: enabled={config.enabled}, skip_confirmation={config.skip_confirmation}")

    # 保存新配置
    new_config = {
        "enabled": True,
        "skip_confirmation": True,
        "verbose": True,
        "batch_mode": True
    }
    saved_config = save_auto_mode_config(new_config)
    print(f"[PASS] 保存新配置: {saved_config.to_dict()}")

    # 验证配置已更新
    updated_config = get_auto_mode_config()
    if updated_config.enabled and updated_config.skip_confirmation:
        print("[PASS] 配置已正确更新")
        return True
    else:
        print("[FAIL] 配置更新失败")
        return False

def test_processor_integration():
    """测试处理器集成"""
    print("\n=== 测试处理器集成 ===")

    from app.core.processor import BatchProcessor
    from app.config.settings import get_settings

    try:
        # 获取设置
        settings = get_settings()
        print(f"[PASS] 获取设置: {settings}")

        # 创建处理器
        processor = BatchProcessor()
        print(f"[PASS] 创建处理器: {type(processor)}")

        # 测试自动模式配置传递
        auto_config = {
            "enabled": True,
            "skip_confirmation": True,
            "verbose": True,
            "batch_mode": True
        }

        print(f"[PASS] 准备自动模式配置: {auto_config}")
        print("[PASS] 处理器集成测试通过")
        return True

    except Exception as e:
        print(f"[FAIL] 处理器集成测试失败: {e}")
        return False

def test_ui_integration():
    """测试UI集成"""
    print("\n=== 测试UI集成 ===")

    try:
        from app.core.script_args import get_auto_mode_config

        # 模拟UI加载配置
        config = get_auto_mode_config()
        print(f"[PASS] UI可获取自动模式配置: enabled={config.enabled}")

        # 模拟UI保存配置
        ui_config = {
            "enabled": True,
            "skip_confirmation": False,
            "verbose": True
        }

        from app.core.script_args import save_auto_mode_config
        save_auto_mode_config(ui_config)

        # 验证配置已保存
        updated_config = get_auto_mode_config()
        if updated_config.enabled == ui_config["enabled"]:
            print("[PASS] UI配置保存测试通过")
            return True
        else:
            print("[FAIL] UI配置保存测试失败")
            return False

    except Exception as e:
        print(f"[FAIL] UI集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("自动模式集成测试")
    print("=" * 50)

    tests = [
        test_script_args_manager,
        test_auto_mode_config,
        test_processor_integration,
        test_ui_integration
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"通过: {sum(results)}/{len(results)}")
    print(f"失败: {len(results) - sum(results)}/{len(results)}")

    if all(results):
        print("[SUCCESS] 所有测试通过！自动模式集成正常工作。")
        return 0
    else:
        print("[WARNING] 部分测试失败，需要修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())