#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSD Batch Processor One-click Build Script
Automatically builds all three versions
"""

import subprocess
import shutil
from pathlib import Path

# Set stdout encoding
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Switch to project root directory
import os
os.chdir(Path(__file__).parent.parent)
print(f"Working directory: {os.getcwd()}")


def run_command(cmd, description):
    """Execute command and display result"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"SUCCESS: {description} completed!")
        return True
    else:
        print(f"FAILED: {description} failed!")
        return False

def copy_files(output_dir):
    """Copy necessary files to output directory"""
    project_dir = Path(__file__).parent.parent
    
    # Copy README
    if (project_dir / "README.md").exists():
        shutil.copy2(project_dir / "README.md", output_dir)
    
    # Copy documentation
    guides_dir = output_dir / "docs" / "guides"
    guides_dir.mkdir(parents=True, exist_ok=True)
    
    for doc_file in ["START_HERE.txt", "QUICK_REFERENCE.txt"]:
        src = project_dir / "docs/guides" / doc_file
        if src.exists():
            shutil.copy2(src, guides_dir)
    
    # Copy script files
    scripts_dir = output_dir / "scripts"
    if not scripts_dir.exists():
        source_scripts = project_dir / "scripts"
        if source_scripts.exists():
            shutil.copytree(source_scripts, scripts_dir)
    
    # Create backup directory
    backups_dir = output_dir / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

def get_file_size(path):
    """Get file size"""
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
    print("PSD Batch Processor One-click Build Tool")
    print("="*60)
    
    project_dir = Path(__file__).parent.parent
    dist_dir = project_dir / "dist"
    
    # Clean old build files
    print("\nCleaning old build files...")
    for dir_name in ["build", "dist", "__pycache__"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  [OK] Deleted {dir_name}")
    
    # Define exclude modules
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
    
    # Define hidden imports
    hidden = ['--hidden-import=win32com', '--hidden-import=pythoncom', '--hidden-import=PIL', '--hidden-import=customtkinter']
    
    # Define data files
    data = [
        '--add-data=docs/guides/START_HERE.txt;docs/guides',
        '--add-data=docs/guides/QUICK_REFERENCE.txt;docs/guides',
        '--add-data=scripts/production/*.jsx;scripts/production',
        '--add-data=scripts/templates/*.jsx;scripts/templates',
        '--add-data=scripts/examples/*.jsx;scripts/examples'
    ]
    
    results = {}
    
    # Build windowed mode
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-Windowed', '--noconsole', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "Building Windowed Mode"):
        copy_files(dist_dir / "PSDBatchProcessor-Windowed")
        results['windowed'] = True
    else:
        results['windowed'] = False
    
    # Build console mode
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-Console', '--console', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "Building Console Mode"):
        copy_files(dist_dir / "PSDBatchProcessor-Console")
        results['console'] = True
    else:
        results['console'] = False
    
    # Build one-file mode
    cmd = ['pyinstaller', '--name=PSDBatchProcessor-OneFile', '--noconsole', '--onefile', '--clean', '--noconfirm']
    cmd.extend(data)
    cmd.extend(hidden)
    cmd.extend(exclude)
    cmd.append('src/main.py')
    
    if run_command(cmd, "Building One-file Mode"):
        # Move to portable directory
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
    
    # Display results
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
    else:
        print(f"WARNING: Some builds failed! ({success_count}/{total_count})")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()