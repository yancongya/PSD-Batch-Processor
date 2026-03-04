#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions Build Script for PSD Batch Processor
纯 Python 构建，不依赖批处理或 PowerShell
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """执行命令并返回结果"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"SUCCESS: {description} completed!")
            return True
        else:
            print(f"FAILED: {description} failed with code {result.returncode}")
            return False
    except Exception as e:
        print(f"ERROR: {description} raised exception: {e}")
        return False

def copy_files(output_dir, project_dir):
    """复制必要文件到输出目录"""
    print(f"\nCopying files to {output_dir}...")
    
    # 复制 README
    readme_src = project_dir / "README.md"
    if readme_src.exists():
        shutil.copy2(readme_src, output_dir)
        print(f"  [OK] Copied README.md")
    
    # 复制文档
    guides_dir = output_dir / "docs" / "guides"
    guides_dir.mkdir(parents=True, exist_ok=True)
    
    for doc_file in ["START_HERE.txt", "QUICK_REFERENCE.txt"]:
        src = project_dir / "docs" / "guides" / doc_file
        if src.exists():
            shutil.copy2(src, guides_dir)
            print(f"  [OK] Copied {doc_file}")
    
    # 复制脚本文件
    scripts_dir = output_dir / "scripts"
    if not scripts_dir.exists():
        source_scripts = project_dir / "scripts"
        if source_scripts.exists():
            shutil.copytree(source_scripts, scripts_dir)
            print(f"  [OK] Copied scripts directory")
    
    # 创建备份目录
    backups_dir = output_dir / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [OK] Created backups directory")

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
    print("GitHub Actions Build Script")
    print("PSD Batch Processor")
    print("="*60)
    
    # 获取项目目录
    project_dir = Path(__file__).parent.parent
    print(f"\nProject directory: {project_dir}")
    print(f"Working directory: {os.getcwd()}")
    
    # 清理旧构建文件
    print("\nCleaning old build files...")
    for dir_name in ["build", "dist", "__pycache__"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  [OK] Deleted {dir_name}")
    
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
    
    dist_dir = project_dir / "dist"
    results = {}
    
    # 构建窗口模式
    print("\n" + "="*60)
    print("Building Windowed Mode")
    print("="*60)
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-Windowed', '--noconsole', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "Building Windowed Mode"):
        copy_files(dist_dir / "PSDBatchProcessor-Windowed", project_dir)
        results['windowed'] = True
    else:
        results['windowed'] = False
    
    # 构建控制台模式
    print("\n" + "="*60)
    print("Building Console Mode")
    print("="*60)
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-Console', '--console', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "Building Console Mode"):
        copy_files(dist_dir / "PSDBatchProcessor-Console", project_dir)
        results['console'] = True
    else:
        results['console'] = False
    
    # 构建单文件模式
    print("\n" + "="*60)
    print("Building One-file Mode")
    print("="*60)
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-OneFile', '--noconsole', '--onefile', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "Building One-file Mode"):
        # 移动到便携目录
        onefile_dir = dist_dir / "PSDBatchProcessor-OneFile-Portable"
        onefile_dir.mkdir(parents=True, exist_ok=True)
        
        source_exe = dist_dir / "PSDBatchProcessor-OneFile.exe"
        target_exe = onefile_dir / "PSDBatchProcessor-OneFile.exe"
        
        if source_exe.exists():
            shutil.move(str(source_exe), str(target_exe))
        
        copy_files(onefile_dir, project_dir)
        results['onefile'] = True
    else:
        results['onefile'] = False
    
    # 显示结果
    print("\n" + "="*60)
    print("Build Results Summary")
    print("="*60)
    
    if results.get('windowed'):
        exe_path = dist_dir / "PSDBatchProcessor-Windowed" / "PSDBatchProcessor-Windowed.exe"
        print(f"\n[OK] Windowed Mode:")
        print(f"   Path: dist/PSDBatchProcessor-Windowed/")
        print(f"   File: PSDBatchProcessor-Windowed.exe")
        print(f"   Size: {get_file_size(exe_path)}")
    
    if results.get('console'):
        exe_path = dist_dir / "PSDBatchProcessor-Console" / "PSDBatchProcessor-Console.exe"
        print(f"\n[OK] Console Mode:")
        print(f"   Path: dist/PSDBatchProcessor-Console/")
        print(f"   File: PSDBatchProcessor-Console.exe")
        print(f"   Size: {get_file_size(exe_path)}")
    
    if results.get('onefile'):
        exe_path = dist_dir / "PSDBatchProcessor-OneFile-Portable" / "PSDBatchProcessor-OneFile.exe"
        print(f"\n[OK] One-file Mode:")
        print(f"   Path: dist/PSDBatchProcessor-OneFile-Portable/")
        print(f"   File: PSDBatchProcessor-OneFile.exe")
        print(f"   Size: {get_file_size(exe_path)}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n{'='*60}")
    if success_count == total_count:
        print(f"SUCCESS: All builds completed! ({success_count}/{total_count})")
        sys.exit(0)
    else:
        print(f"WARNING: Some builds failed! ({success_count}/{total_count})")
        sys.exit(1)
    print(f"{'='*60}")

if __name__ == "__main__":
    main()