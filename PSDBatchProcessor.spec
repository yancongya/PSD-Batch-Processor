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
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PSDBatchProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
