# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('docs/guides/START_HERE.txt', 'docs/guides'), ('docs/guides/QUICK_REFERENCE.txt', 'docs/guides'), ('scripts/production/*.jsx', 'scripts/production'), ('scripts/templates/*.jsx', 'scripts/templates'), ('scripts/examples/*.jsx', 'scripts/examples')],
    hiddenimports=['win32com', 'pythoncom', 'PIL', 'customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'torchaudio', 'tensorflow', 'keras', 'scipy', 'numpy', 'sympy', 'onnxruntime', 'selenium', 'playwright', 'requests', 'beautifulsoup4', 'lxml', 'bs4', 'pandas', 'matplotlib', 'cv2', 'opencv-python', 'pytest', 'black', 'flake8', 'langchain', 'openai', 'anthropic', 'transformers', 'tokenizers', 'huggingface_hub', 'tkinter', 'turtle'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PSDBatchProcessor-Console',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PSDBatchProcessor-Console',
)
