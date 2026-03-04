#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

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
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    print(f"Current directory: {os.getcwd()}", flush=True)
    print(f"Script directory: {script_dir}", flush=True)
    print(f"src/main.py exists: {(Path('src/main.py').exists())}", flush=True)
    
    # List all files in current directory
    print("Files in current directory:", flush=True)
    for item in Path('.').iterdir():
        print(f"  {item.name}", flush=True)
    
    # Check src directory
    src_dir = Path('src')
    if src_dir.exists():
        print("Files in src directory:", flush=True)
        for item in src_dir.iterdir():
            print(f"  {item.name}", flush=True)
    else:
        print("src directory does not exist!", flush=True)
    
    clean()
    install()
    build()

if __name__ == '__main__':
    main()