#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSD Batch Processor 一键构建脚本
自动构建所有三个版本
"""

import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"✅ {description} 完成！")
        return True
    else:
        print(f"❌ {description} 失败！")
        return False

def copy_files(output_dir):
    """复制必要文件到输出目录"""
    project_dir = Path(__file__).parent.parent
    
    # 复制 README
    if (project_dir / "README.md").exists():
        shutil.copy2(project_dir / "README.md", output_dir)
    
    # 复制文档
    guides_dir = output_dir / "docs" / "guides"
    guides_dir.mkdir(parents=True, exist_ok=True)
    
    for doc_file in ["START_HERE.txt", "QUICK_REFERENCE.txt"]:
        src = project_dir / "docs/guides" / doc_file
        if src.exists():
            shutil.copy2(src, guides_dir)
    
    # 复制脚本文件
    scripts_dir = output_dir / "scripts"
    if not scripts_dir.exists():
        source_scripts = project_dir / "scripts"
        if source_scripts.exists():
            shutil.copytree(source_scripts, scripts_dir)
    
    # 创建备份目录
    backups_dir = output_dir / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

def get_file_size(path):
    """获取文件大小"""
    if path.exists():
        size = path.stat().st_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"
    return "N/A"

def main():
    print("="*60)
    print("PSD Batch Processor 一键构建工具")
    print("="*60)
    
    project_dir = Path(__file__).parent.parent
    dist_dir = project_dir / "dist"
    
    # 清理旧的构建文件
    print("\n清理旧的构建文件...")
    for dir_name in ["build", "dist", "__pycache__"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  ✓ 删除 {dir_name}")
    
    # 定义排除模块
    exclude = [
        '--exclude-module=torch', '--exclude-module=torchvision', '--exclude-module=torchaudio',
        '--exclude-module=tensorflow', '--exclude-module=keras', '--exclude-module=scipy',
        '--exclude-module=numpy', '--exclude-module=sympy', '--exclude-module=onnxruntime',
        '--exclude-module=selenium', '--exclude-module=playwright', '--exclude-module=requests',
        '--exclude-module=beautifulsoup4', '--exclude-module=lxml', '--exclude-module=bs4',
        '--exclude-module=pandas', '--exclude-module=matplotlib', '--exclude-module=cv2',
        '--exclude-module=opencv-python', '--exclude-module=pytest', '--exclude-module=black',
        '--exclude-module=flake8', '--exclude-module=langchain', '--exclude-module=openai',
        '--exclude-module=anthropic', '--exclude-module=transformers', '--exclude-module=tokenizers',
        '--exclude-module=huggingface_hub', '--exclude-module=tkinter', '--exclude-module=turtle'
    ]
    
    # 定义隐藏导入
    hidden = ['--hidden-import=win32com', '--hidden-import=pythoncom', '--hidden-import=PIL', '--hidden-import=customtkinter']
    
    # 定义数据文件
    data = [
        '--add-data=docs/guides/START_HERE.txt;docs/guides',
        '--add-data=docs/guides/QUICK_REFERENCE.txt;docs/guides',
        '--add-data=scripts/production/*.jsx;scripts/production',
        '--add-data=scripts/templates/*.jsx;scripts/templates',
        '--add-data=scripts/examples/*.jsx;scripts/examples'
    ]
    
    results = {}
    
    # 构建窗口模式
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-Windowed', '--noconsole', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "构建窗口模式"):
        copy_files(dist_dir / "PSDBatchProcessor-Windowed")
        results['windowed'] = True
    else:
        results['windowed'] = False
    
    # 构建控制台模式
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-Console', '--console', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "构建控制台模式"):
        copy_files(dist_dir / "PSDBatchProcessor-Console")
        results['console'] = True
    else:
        results['console'] = False
    
    # 构建单文件模式
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-OneFile', '--noconsole', '--onefile', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "构建单文件模式"):
        # 移动到便携目录
        onefile_dir = dist_dir / "PSDBatchProcessor-OneFile-Portable"
        onefile_dir.mkdir(parents=True, exist_ok=True)
        
        source_exe = dist_dir / "PSDBatchProcessor-OneFile.exe"
        target_exe = onefile_dir / "PSDBatchProcessor-OneFile.exe"
        
        if source_exe.exists():
            shutil.move(str(source_exe), str(target_exe))
        
        copy_files(onefile_dir)
        results['onefile'] = True
    else:
        results['onefile'] = False
    
    # 显示结果
    print("\n" + "="*60)
    print("构建结果汇总")
    print("="*60)
    
    if results.get('windowed'):
        exe_path = dist_dir / "PSDBatchProcessor-Windowed" / "PSDBatchProcessor-Windowed.exe"
        print(f"\n✅ 窗口模式:")
        print(f"   路径: dist/PSDBatchProcessor-Windowed/")
        print(f"   文件: PSDBatchProcessor-Windowed.exe")
        print(f"   大小: {get_file_size(exe_path)}")
    
    if results.get('console'):
        exe_path = dist_dir / "PSDBatchProcessor-Console" / "PSDBatchProcessor-Console.exe"
        print(f"\n✅ 控制台模式:")
        print(f"   路径: dist/PSDBatchProcessor-Console/")
        print(f"   文件: PSDBatchProcessor-Console.exe")
        print(f"   大小: {get_file_size(exe_path)}")
    
    if results.get('onefile'):
        exe_path = dist_dir / "PSDBatchProcessor-OneFile-Portable" / "PSDBatchProcessor-OneFile.exe"
        print(f"\n✅ 单文件模式:")
        print(f"   路径: dist/PSDBatchProcessor-OneFile-Portable/")
        print(f"   文件: PSDBatchProcessor-OneFile.exe")
        print(f"   大小: {get_file_size(exe_path)}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n{'='*60}")
    if success_count == total_count:
        print(f"🎉 所有构建成功完成！ ({success_count}/{total_count})")
    else:
        print(f"⚠️  部分构建失败！ ({success_count}/{total_count})")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()