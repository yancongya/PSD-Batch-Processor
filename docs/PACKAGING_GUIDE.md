# 打包为 EXE 指南

## 📦 打包方案概述

可以使用 PyInstaller 将项目打包成独立的 EXE 文件，方便分发和使用。

## 🎯 推荐方案

### 方案 1：PyInstaller (最常用)
**优点**：
- 成熟稳定
- 社区支持好
- 配置灵活
- 支持复杂项目

**缺点**：
- 打包体积较大
- 需要配置 spec 文件

### 方案 2：Nuitka (性能优化)
**优点**：
- 编译为 C++，性能更好
- 启动速度更快
- 反编译困难

**缺点**：
- 打包时间长
- 配置相对复杂

### 方案 3：cx_Freeze (替代方案)
**优点**：
- 跨平台支持好
- 配置简单

**缺点**：
- 社区相对较小
- 文档不够完善

**推荐**：使用 PyInstaller，最成熟且适合本项目。

## 🔧 PyInstaller 打包配置

### 1. 安装 PyInstaller
```bash
pip install pyinstaller
```

### 2. 基础打包命令
```bash
# 基础打包（控制台版本）
pyinstaller --name="PSDBatchProcessor" src/main.py

# 窗口版本（无控制台）
pyinstaller --name="PSDBatchProcessor" --noconsole src/main.py
```

### 3. 完整配置 (推荐)
创建打包配置文件 `build.spec`：

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 分析所有导入
a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # 配置文件
        ('src/app/config/config.json', 'app/config'),

        # 文档
        ('docs/guides/START_HERE.txt', 'docs/guides'),
        ('docs/guides/QUICK_REFERENCE.txt', 'docs/guides'),

        # 脚本模板
        ('scripts/templates/auto_mode_template.jsx', 'scripts/templates'),

        # 示例脚本
        ('scripts/examples/*.jsx', 'scripts/examples'),

        # 生产脚本
        ('scripts/production/*.jsx', 'scripts/production'),

        # 依赖文件
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'win32com',
        'win32com.client',
        'pythoncom',
        'PIL',
        'customtkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 构建 exe
pyz = a.pure
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
    console=False,  # True=显示控制台, False=隐藏控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.ico'],  # 图标文件
)
```

### 4. 高级配置选项

#### 带图标的打包
```bash
pyinstaller --name="PSDBatchProcessor" \
    --noconsole \
    --icon=assets/icon.ico \
    --add-data="src/app/config/config.json;app/config" \
    --add-data="docs/guides/START_HERE.txt;docs/guides" \
    --add-data="scripts/production/*.jsx;scripts/production" \
    --hidden-import=win32com \
    --hidden-import=pythoncom \
    src/main.py
```

#### 单文件模式
```bash
pyinstaller --name="PSDBatchProcessor" \
    --noconsole \
    --onefile \
    --icon=assets/icon.ico \
    src/main.py
```

**注意**：单文件模式会将所有文件打包到一个 EXE 中，但可能会影响脚本文件的访问。

## 📁 项目结构适配

### 打包后的目录结构
```
dist/PSDBatchProcessor/
├── PSDBatchProcessor.exe      # 主程序
├── app/                       # 应用代码
│   ├── config/
│   ├── core/
│   ├── models/
│   └── ui/
├── utils/                     # 工具模块
├── scripts/                   # JSX 脚本
│   ├── templates/
│   ├── examples/
│   └── production/
├── docs/                      # 文档
│   └── guides/
├── backups/                   # 备份目录（运行时创建）
└── 配置文件等
```

### 路径处理
需要在代码中添加打包后的路径检测：

```python
# 在 main.py 或相关文件中添加
import sys
import os
from pathlib import Path

def get_base_path():
    """获取程序运行路径（支持打包后）"""
    if getattr(sys, 'frozen', False):
        # 打包后的 EXE
        return Path(sys.executable).parent
    else:
        # 开发环境
        return Path(__file__).parent

# 使用示例
BASE_DIR = get_base_path()
config_path = BASE_DIR / "src/app/config/config.json"
scripts_dir = BASE_DIR / "scripts/production"
```

## 🛠️ 自动化打包脚本

### Windows 批处理脚本

创建 `tools/build.bat`：

```batch
@echo off
chcp 65001 >nul

echo ========================================
echo PSD Batch Processor 打包工具
echo ========================================
echo.

REM 设置路径
set PROJECT_DIR=%~dp0..
set DIST_DIR=%PROJECT_DIR%\dist
set BUILD_DIR=%PROJECT_DIR%\build
set SPEC_FILE=%PROJECT_DIR%\build.spec

echo 项目目录: %PROJECT_DIR%
echo.

REM 检查 Python
echo 检查 Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python 未找到！
    pause
    exit /b 1
)
echo [OK] Python 已安装
echo.

REM 检查 PyInstaller
echo 检查 PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [WARNING] PyInstaller 未安装，正在安装...
    pip install pyinstaller
)
echo [OK] PyInstaller 已安装
echo.

REM 清理旧的构建文件
echo 清理旧的构建文件...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
echo [OK] 旧文件已清理
echo.

REM 选择打包模式
echo 选择打包模式：
echo 1. 窗口模式（推荐，无控制台）
echo 2. 控制台模式（调试用）
echo 3. 单文件模式（便携版）
echo 4. 自定义配置（使用 build.spec）
echo.
set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    set MODE=窗口模式
    set ARGS=--noconsole --icon=assets/icon.ico
) else if "%choice%"=="2" (
    set MODE=控制台模式
    set ARGS=--console --icon=assets/icon.ico
) else if "%choice%"=="3" (
    set MODE=单文件模式
    set ARGS=--noconsole --onefile --icon=assets/icon.ico
) else if "%choice%"=="4" (
    set MODE=自定义配置
    set ARGS=
) else (
    echo [ERROR] 无效选择！
    pause
    exit /b 1
)

echo.
echo 选择模式: %MODE%
echo.

REM 开始打包
echo 开始打包...
echo.

if "%choice%"=="4" (
    REM 使用 spec 文件
    pyinstaller "%SPEC_FILE%" --clean --noconfirm
) else (
    REM 使用命令行参数
    cd /d "%PROJECT_DIR%"

    pyinstaller ^
        --name="PSDBatchProcessor" ^
        %ARGS% ^
        --add-data="src/app/config/config.json;app/config" ^
        --add-data="docs/guides/START_HERE.txt;docs/guides" ^
        --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" ^
        --add-data="scripts/production/*.jsx;scripts/production" ^
        --add-data="scripts/templates/*.jsx;scripts/templates" ^
        --hidden-import=win32com ^
        --hidden-import=pythoncom ^
        --hidden-import=PIL ^
        --hidden-import=customtkinter ^
        --clean ^
        --noconfirm ^
        src/main.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] 打包失败！
    echo 请检查错误信息
    pause
    exit /b 1
)

echo.
echo [SUCCESS] 打包完成！
echo.

REM 显示打包结果
echo 打包结果：
echo - 可执行文件: dist\PSDBatchProcessor\PSDBatchProcessor.exe
echo - 文件大小:
dir /s /-c "%DIST_DIR%\PSDBatchProcessor\PSDBatchProcessor.exe" | findstr "bytes"

echo.
echo 复制必要文件...
xcopy /s /y "%PROJECT_DIR%\README.md" "%DIST_DIR%\PSDBatchProcessor\"
xcopy /s /y "%PROJECT_DIR%\docs\guides\START_HERE.txt" "%DIST_DIR%\PSDBatchProcessor\docs\guides\"
echo [OK] 文件复制完成

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 使用方法：
echo 1. 运行: dist\PSDBatchProcessor\PSDBatchProcessor.exe
echo 2. 首次运行会自动创建 backups/ 和 config.json
echo 3. 按照文档配置 Photoshop 路径和脚本目录
echo.

pause
```

### Python 打包脚本

创建 `tools/build.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSD Batch Processor 打包脚本
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def get_project_dir():
    """获取项目根目录"""
    return Path(__file__).parent.parent

def check_dependencies():
    """检查依赖"""
    print("检查依赖...")

    # 检查 Python
    try:
        version = subprocess.check_output(["python", "--version"],
                                         stderr=subprocess.STDOUT).decode().strip()
        print(f"[OK] {version}")
    except:
        print("[ERROR] Python 未找到！")
        return False

    # 检查 PyInstaller
    try:
        import PyInstaller
        print("[OK] PyInstaller 已安装")
    except:
        print("[WARNING] PyInstaller 未安装，正在安装...")
        subprocess.run(["pip", "install", "pyinstaller"], check=True)

    return True

def clean_build():
    """清理旧的构建文件"""
    print("\n清理旧的构建文件...")
    project_dir = get_project_dir()

    for dir_name in ["build", "dist", "__pycache__"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"[OK] 删除 {dir_name}")

    # 删除 spec 文件
    spec_file = project_dir / "PSDBatchProcessor.spec"
    if spec_file.exists():
        spec_file.unlink()
        print("[OK] 删除 spec 文件")

def build_exe(mode="windowed"):
    """打包 EXE"""
    print(f"\n开始打包 ({mode} 模式)...")
    project_dir = get_project_dir()

    # 基础命令
    cmd = [
        "pyinstaller",
        "--name=PSDBatchProcessor",
        "--clean",
        "--noconfirm",
    ]

    # 模式选项
    if mode == "windowed":
        cmd.extend(["--noconsole", "--icon=assets/icon.ico"])
    elif mode == "console":
        cmd.extend(["--console", "--icon=assets/icon.ico"])
    elif mode == "onefile":
        cmd.extend(["--noconsole", "--onefile", "--icon=assets/icon.ico"])

    # 添加数据文件
    data_files = [
        "src/app/config/config.json;app/config",
        "docs/guides/START_HERE.txt;docs/guides",
        "docs/guides/QUICK_REFERENCE.txt;docs/guides",
        "scripts/production/*.jsx;scripts/production",
        "scripts/templates/*.jsx;scripts/templates",
    ]

    for data in data_files:
        cmd.extend(["--add-data", data])

    # 隐藏导入
    hidden_imports = [
        "win32com",
        "pythoncom",
        "PIL",
        "customtkinter",
    ]

    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])

    # 主程序
    cmd.append(str(project_dir / "src/main.py"))

    # 执行打包
    print(f"命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(project_dir))

    if result.returncode == 0:
        print("\n[SUCCESS] 打包完成！")
        return True
    else:
        print("\n[ERROR] 打包失败！")
        return False

def show_result():
    """显示打包结果"""
    project_dir = get_project_dir()
    exe_path = project_dir / "dist" / "PSDBatchProcessor" / "PSDBatchProcessor.exe"

    if exe_path.exists():
        size = exe_path.stat().st_size
        size_mb = size / (1024 * 1024)

        print("\n" + "=" * 60)
        print("打包结果")
        print("=" * 60)
        print(f"可执行文件: {exe_path}")
        print(f"文件大小: {size_mb:.2f} MB")
        print(f"文件大小: {size:,} bytes")
        print("\n使用方法:")
        print(f"  {exe_path}")
        print("\n首次运行会自动创建:")
        print("  - backups/ 目录")
        print("  - src/app/config/config.json")
        print("\n请按照文档配置:")
        print("  docs/guides/START_HERE.txt")
        print("=" * 60)

def main():
    """主函数"""
    print("=" * 60)
    print("PSD Batch Processor 打包工具")
    print("=" * 60)

    # 检查依赖
    if not check_dependencies():
        return 1

    # 选择模式
    print("\n选择打包模式:")
    print("1. 窗口模式 (推荐，无控制台)")
    print("2. 控制台模式 (调试用)")
    print("3. 单文件模式 (便携版)")
    print("4. 退出")

    choice = input("\n请输入选择 (1-4): ").strip()

    modes = {
        "1": "windowed",
        "2": "console",
        "3": "onefile",
        "4": "exit"
    }

    if choice not in modes:
        print("[ERROR] 无效选择！")
        return 1

    if modes[choice] == "exit":
        return 0

    # 清理旧文件
    clean_build()

    # 打包
    if build_exe(modes[choice]):
        # 显示结果
        show_result()

        # 复制必要文件
        print("\n复制必要文件...")
        project_dir = get_project_dir()
        dist_dir = project_dir / "dist" / "PSDBatchProcessor"

        try:
            shutil.copy2(project_dir / "README.md", dist_dir)
            shutil.copy2(project_dir / "docs/guides/START_HERE.txt",
                        dist_dir / "docs" / "guides")
            print("[OK] 文件复制完成")
        except Exception as e:
            print(f"[WARNING] 文件复制失败: {e}")

        print("\n打包完成！")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## 🎨 添加图标

### 1. 准备图标文件
创建 `assets/icon.ico` (Windows 图标格式)

### 2. 图标要求
- **格式**: .ico (Windows) 或 .icns (macOS)
- **尺寸**: 256x256, 128x128, 64x64, 48x48, 32x32, 16x16
- **工具**: 可使用在线图标生成器或 Photoshop

### 3. 如果没有图标
可以暂时不使用图标：
```bash
pyinstaller --name="PSDBatchProcessor" --noconsole src/main.py
```

## 📋 打包步骤

### 快速打包（推荐）

1. **创建打包脚本**
   ```bash
   # 复制上面的 Python 打包脚本
   # 保存为 tools/build.py
   ```

2. **运行打包**
   ```bash
   cd "F:\插件脚本开发\PSD Batch Processor"
   python tools/build.py
   ```

3. **选择模式**
   - 选择 **1** (窗口模式) - 推荐
   - 等待打包完成

4. **获取结果**
   ```
   dist/PSDBatchProcessor/PSDBatchProcessor.exe
   ```

### 手动打包

1. **安装 PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **执行打包命令**
   ```bash
   cd "F:\插件脚本开发\PSD Batch Processor"

   pyinstaller ^
       --name="PSDBatchProcessor" ^
       --noconsole ^
       --icon=assets/icon.ico ^
       --add-data="src/app/config/config.json;app/config" ^
       --add-data="docs/guides/START_HERE.txt;docs/guides" ^
       --add-data="scripts/production/*.jsx;scripts/production" ^
       --hidden-import=win32com ^
       --hidden-import=pythoncom ^
       src/main.py
   ```

3. **获取结果**
   ```
   dist/PSDBatchProcessor/PSDBatchProcessor.exe
   ```

## ⚠️ 常见问题

### 1. 文件找不到错误
**问题**：打包后找不到脚本或配置文件

**解决**：使用 `get_base_path()` 函数处理路径：
```python
import sys
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent
```

### 2. 缺少依赖
**问题**：运行时提示缺少模块

**解决**：在打包命令中添加 `--hidden-import`：
```bash
--hidden-import=win32com --hidden-import=pythoncom
```

### 3. 杀毒软件误报
**问题**：EXE 被杀毒软件拦截

**解决**：
- 使用代码签名证书（推荐）
- 在杀毒软件中添加例外
- 使用 UPX 压缩（可能减少误报）

### 4. 文件体积过大
**问题**：打包后文件体积大（50-100MB）

**解决**：
- 使用 UPX 压缩：`--upx-dir=upx`
- 排除不必要的库：`--exclude-module=unused_module`
- 接受正常体积（Python 运行时需要）

## 📊 打包体积估算

### 基础打包（窗口模式）
- **文件大小**: 60-80 MB
- **包含**: Python 运行时 + 所有依赖 + 项目文件
- **优点**: 用户双击运行，无需安装 Python

### 单文件模式
- **文件大小**: 60-80 MB
- **包含**: 所有文件打包到一个 EXE
- **优点**: 便携，单个文件
- **缺点**: 启动稍慢，解压到临时目录运行

### 调试模式（控制台）
- **文件大小**: 60-80 MB
- **包含**: 控制台窗口
- **优点**: 可以看到错误信息
- **适合**: 开发和调试

## 🚀 部署分发

### 1. 创建发布包
```bash
dist/PSDBatchProcessor/
├── PSDBatchProcessor.exe      # 主程序
├── README.md                  # 说明文档
├── docs/
│   └── guides/
│       └── START_HERE.txt     # 快速开始
└── backups/                   # 运行时自动创建
```

### 2. 压缩分发
```bash
# 使用 7-Zip 或 WinRAR
# 压缩为 PSDBatchProcessor_v1.0.zip
```

### 3. 发布说明
创建 `RELEASE_NOTES.txt`：
```
PSD Batch Processor v1.0

功能特性：
- 批量处理 PSD 文件
- 自动备份原始文件
- 支持自定义 JSX 脚本
- 无人值守处理
- 实时进度显示

系统要求：
- Windows 10/11
- Photoshop (已安装)

使用方法：
1. 双击运行 PSDBatchProcessor.exe
2. 按照向导配置路径
3. 添加 PSD 文件并开始处理

详细说明：docs/guides/START_HERE.txt
```

## 📝 后续优化

### 1. 自动更新
可以添加自动更新功能：
- 检查 GitHub Releases
- 下载新版本
- 替换 EXE 文件

### 2. 安装程序
使用 Inno Setup 或 NSIS 创建安装程序：
- 开始菜单快捷方式
- 桌面快捷方式
- 文件关联（可选）

### 3. 代码签名
购买代码签名证书：
- 避免杀毒软件误报
- 提升用户信任度
- Windows SmartScreen 通过

## 🎯 推荐方案总结

### 对于个人使用
```bash
# 窗口模式打包
python tools/build.py
# 选择 1 (窗口模式)
```

### 对于分发
```bash
# 单文件模式 + 图标
python tools/build.py
# 选择 3 (单文件模式)
```

### 对于调试
```bash
# 控制台模式
python tools/build.py
# 选择 2 (控制台模式)
```

## 📚 相关资源

- **PyInstaller 官方文档**: https://pyinstaller.org/en/stable/
- **PyInstaller 问题排查**: https://pyinstaller.org/en/stable/usage.html
- **Windows 图标生成器**: https://www.favicon.cc/
- **Inno Setup**: https://jrsoftware.org/isinfo.php (创建安装程序)

---

**打包完成！** 🎉

现在你可以将项目打包成独立的 EXE 文件，方便分发给其他用户使用！