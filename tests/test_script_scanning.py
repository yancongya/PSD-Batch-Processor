#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本扫描功能
验证是否能正确扫描子目录中的脚本文件
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_script_scanning():
    """测试脚本扫描功能"""
    print("=" * 60)
    print("测试脚本扫描功能")
    print("=" * 60)

    # 导入必要的模块
    try:
        from app.config.settings import get_settings, init_settings
    except ImportError as e:
        print(f"[ERROR] 无法导入模块: {e}")
        return False

    # 初始化设置
    settings = init_settings()
    script_dir = settings.get_script_dir_path()

    print(f"\n脚本目录: {script_dir}")
    print(f"目录存在: {script_dir.exists()}")

    if not script_dir.exists():
        print("[ERROR] 脚本目录不存在！")
        return False

    # 递归扫描所有.jsx文件
    jsx_files = list(script_dir.rglob("*.jsx"))
    print(f"\n找到 {len(jsx_files)} 个 JSX 脚本文件:")

    script_items = []
    for jsx_file in jsx_files:
        try:
            # 计算相对于脚本目录的相对路径
            rel_path = jsx_file.relative_to(script_dir)

            # 如果在子目录中，显示为 "子目录/脚本名"
            if rel_path.parent.name != ".":
                display_name = str(rel_path)
            else:
                display_name = rel_path.name

            script_items.append({
                'display': display_name,
                'full_path': str(jsx_file),
                'size': jsx_file.stat().st_size
            })

            print(f"  [{len(script_items):2d}] {display_name}")
            print(f"       路径: {jsx_file}")
            print(f"       大小: {jsx_file.stat().st_size} bytes")
            print()

        except ValueError as e:
            print(f"  [ERROR] 无法处理文件 {jsx_file}: {e}")

    # 按显示名称排序
    script_items.sort(key=lambda x: x['display'])

    print(f"\n排序后的脚本列表:")
    for item in script_items:
        print(f"  {item['display']}")

    # 创建路径映射
    script_path_map = {item['display']: item['full_path'] for item in script_items}

    print(f"\n路径映射:")
    for display, full_path in script_path_map.items():
        print(f"  {display} -> {full_path}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

    return True

def test_ui_script_refresh():
    """测试UI脚本刷新逻辑"""
    print("\n" + "=" * 60)
    print("测试UI脚本刷新逻辑")
    print("=" * 60)

    try:
        from app.config.settings import get_settings, init_settings
        from pathlib import Path

        # 初始化设置
        settings = init_settings()
        script_dir = settings.get_script_dir_path()

        # 模拟UI刷新逻辑
        if not script_dir.exists():
            print("[ERROR] 脚本目录不存在！")
            return False

        # 递归扫描所有.jsx文件（包括子目录）
        jsx_files = list(script_dir.rglob("*.jsx"))

        # 创建相对路径显示，便于用户识别
        script_items = []
        for jsx_file in jsx_files:
            try:
                # 计算相对于脚本目录的相对路径
                rel_path = jsx_file.relative_to(script_dir)

                # 如果在子目录中，显示为 "子目录/脚本名"
                if rel_path.parent.name != ".":
                    display_name = str(rel_path)
                else:
                    display_name = rel_path.name

                script_items.append({
                    'display': display_name,
                    'full_path': str(jsx_file)
                })
            except ValueError:
                # 如果无法计算相对路径，直接使用文件名
                script_items.append({
                    'display': jsx_file.name,
                    'full_path': str(jsx_file)
                })

        # 按显示名称排序
        script_items.sort(key=lambda x: x['display'])

        # 模拟下拉框内容
        display_names = [item['display'] for item in script_items]

        print(f"\n下拉框将显示的脚本列表:")
        for i, name in enumerate(display_names, 1):
            print(f"  {i:2d}. {name}")

        # 存储完整的路径映射
        script_path_map = {item['display']: item['full_path'] for item in script_items}

        print(f"\n选择脚本时的路径解析:")
        for display in display_names[:5]:  # 只显示前5个
            full_path = script_path_map[display]
            print(f"  选择: {display}")
            print(f"  路径: {full_path}")
            print(f"  存在: {Path(full_path).exists()}")
            print()

        print("=" * 60)
        print("UI脚本刷新逻辑测试完成！")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 运行测试
    success1 = test_script_scanning()
    success2 = test_ui_script_refresh()

    if success1 and success2:
        print("\n[SUCCESS] 所有测试通过！")
        sys.exit(0)
    else:
        print("\n[ERROR] 测试失败！")
        sys.exit(1)