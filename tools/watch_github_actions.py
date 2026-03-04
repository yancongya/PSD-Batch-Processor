#!/usr/bin/env python3
"""
GitHub Actions 构建监控脚本
自动获取最新的构建状态
"""

import subprocess
import sys
from pathlib import Path

def get_latest_run():
    """获取最新的 GitHub Actions 运行状态"""
    try:
        # 检查是否安装了 gh CLI
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("GitHub CLI (gh) 未安装")
            print("请从 https://cli.github.com/ 下载安装")
            return None
        
        # 获取最新的 workflow 运行
        result = subprocess.run([
            'gh', 'run', 'list', '--limit', '1', '--json', 'conclusion,status,displayTitle,createdAt'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"获取运行状态失败: {result.stderr}")
            return None
        
        import json
        runs = json.loads(result.stdout)
        if runs:
            latest = runs[0]
            print(f"\n=== 最新构建状态 ===")
            print(f"标题: {latest['displayTitle']}")
            print(f"状态: {latest['status']}")
            print(f"结果: {latest['conclusion'] or '进行中'}")
            print(f"时间: {latest['createdAt']}")
            print(f"\n查看详细: gh run view {latest.get('databaseId', '')}")
            return latest
        else:
            print("没有找到构建记录")
            return None
            
    except Exception as e:
        print(f"错误: {e}")
        return None

def watch_run():
    """持续监控构建状态"""
    print("开始监控 GitHub Actions 构建状态...")
    print("按 Ctrl+C 停止监控\n")
    
    try:
        while True:
            latest = get_latest_run()
            if latest and latest['status'] == 'completed':
                print(f"\n构建完成！结果: {latest['conclusion']}")
                break
            
            # 等待 10 秒
            import time
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        watch_run()
    else:
        get_latest_run()