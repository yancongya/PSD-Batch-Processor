#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

# Force immediate output
sys.stderr.write("=== BUILD SCRIPT STARTED ===\n")
sys.stderr.flush()

def clean():
    for d in ['build', 'dist', '__pycache__']:
        p = Path(d)
        if p.exists():
            shutil.rmtree(p)
            print(f"Removed {d}")

def install():
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', 'PyQt5', 'PyQt-Fluent-Widgets', 'pywin32', 'pillow'], check=True)

def build():
    base = ['pyinstaller', '--clean', '--noconfirm']
    data = ['--add-data=docs/guides/START_HERE.txt;docs/guides',
            '--add-data=docs/guides/QUICK_REFERENCE.txt;docs/guides',
            '--add-data=scripts/production/*.jsx;scripts/production',
            '--add-data=scripts/templates/*.jsx;scripts/templates',
            '--add-data=scripts/examples/*.jsx;scripts/examples']
    hidden = ['--hidden-import=win32com', '--hidden-import=pythoncom', '--hidden-import=PIL', '--hidden-import=customtkinter']
    exclude = ['--exclude-module=torch', '--exclude-module=torchvision', '--exclude-module=torchaudio',
               '--exclude-module=tensorflow', '--exclude-module=keras', '--exclude-module=scipy',
               '--exclude-module=numpy', '--exclude-module=sympy', '--exclude-module=onnxruntime',
               '--exclude-module=selenium', '--exclude-module=playwright', '--exclude-module=requests',
               '--exclude-module=beautifulsoup4', '--exclude-module=lxml', '--exclude-module=bs4',
               '--exclude-module=pandas', '--exclude-module=matplotlib', '--exclude-module=cv2',
               '--exclude-module=opencv-python', '--exclude-module=pytest', '--exclude-module=black',
               '--exclude-module=flake8', '--exclude-module=langchain', '--exclude-module=openai',
               '--exclude-module=anthropic', '--exclude-module=transformers', '--exclude-module=tokenizers',
               '--exclude-module=huggingface_hub', '--exclude-module=tkinter', '--exclude-module=turtle']
    
    modes = [
        ('Windowed', '--noconsole'),
        ('Console', '--console'),
        ('OneFile', '--noconsole --onefile')
    ]
    
    for name, opts in modes:
        cmd = base + ['--name=PSDBatchProcessor-' + name] + opts.split() + data + hidden + exclude + ['src/main.py']
        subprocess.run(cmd, check=True)
        print(f"Built {name}")

def main():
    # Get the project root directory (parent of .github directory)
    script_file = Path(__file__).resolve()
    project_root = script_file.parent.parent
    
    sys.stderr.write(f"Script file: {script_file}\n")
    sys.stderr.write(f"Project root: {project_root}\n")
    sys.stderr.write(f"Current directory: {os.getcwd()}\n")
    sys.stderr.flush()
    
    # Change to project root directory
    os.chdir(project_root)
    sys.stderr.write(f"After chdir - Current directory: {os.getcwd()}\n")
    sys.stderr.flush()
    
    # Check if src directory exists
    src_dir = Path('src')
    sys.stderr.write(f"src directory exists: {src_dir.exists()}\n")
    sys.stderr.flush()
    
    if src_dir.exists():
        sys.stderr.write("Files in src directory:\n")
        for item in src_dir.iterdir():
            sys.stderr.write(f"  {item.name}\n")
        sys.stderr.flush()
    
    # Check if main.py exists
    main_py = Path('src/main.py')
    sys.stderr.write(f"src/main.py exists: {main_py.exists()}\n")
    sys.stderr.write(f"src/main.py absolute path: {main_py.absolute()}\n")
    sys.stderr.flush()
    
    clean()
    install()
    build()

if __name__ == '__main__':
    main()