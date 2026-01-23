@echo off
chcp 65001 >nul

echo ========================================
echo PSD Batch Processor Build Tool
echo ========================================
echo.

REM Set paths
set PROJECT_DIR=%~dp0..
set DIST_DIR=%PROJECT_DIR%\dist

echo Project directory: %PROJECT_DIR%
echo.

REM Check Python
echo Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ and add to PATH
    pause
    exit /b 1
)
echo [OK] Python installed
echo.

REM Check PyInstaller
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [WARNING] PyInstaller not found, installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] PyInstaller installation failed!
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller installed
echo.

REM Select build mode
echo Select build mode:
echo 1. Windowed mode (recommended, no console)
echo 2. Console mode (for debugging)
echo 3. One-file mode (portable)
echo 4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    set MODE=Windowed
    set ARGS=--noconsole
) else if "%choice%"=="2" (
    set MODE=Console
    set ARGS=--console
) else if "%choice%"=="3" (
    set MODE=One-file
    set ARGS=--noconsole --onefile
) else if "%choice%"=="4" (
    echo Exiting...
    pause
    exit /b 0
) else (
    echo [ERROR] Invalid choice!
    pause
    exit /b 1
)

echo.
echo Selected mode: %MODE%
echo.

REM Clean old build files
echo Cleaning old build files...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%PROJECT_DIR%\build" rmdir /s /q "%PROJECT_DIR%\build"
if exist "%PROJECT_DIR%\__pycache__" rmdir /s /q "%PROJECT_DIR%\__pycache__"
echo [OK] Old files cleaned
echo.

REM Start building
echo Starting build...
echo.

cd /d "%PROJECT_DIR%"

pyinstaller ^
    --name="PSDBatchProcessor" ^
    %ARGS% ^
    --add-data="docs/guides/START_HERE.txt;docs/guides" ^
    --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" ^
    --add-data="scripts/production/*.jsx;scripts/production" ^
    --add-data="scripts/templates/*.jsx;scripts/templates" ^
    --add-data="scripts/examples/*.jsx;scripts/examples" ^
    --hidden-import=win32com ^
    --hidden-import=pythoncom ^
    --hidden-import=PIL ^
    --hidden-import=customtkinter ^
    --clean ^
    --noconfirm ^
    src/main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Please check the error messages
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build completed!
echo.

REM Copy additional files
echo Copying additional files...
xcopy /y "%PROJECT_DIR%\README.md" "%DIST_DIR%\PSDBatchProcessor\" >nul 2>&1
if not exist "%DIST_DIR%\PSDBatchProcessor\docs\guides" mkdir "%DIST_DIR%\PSDBatchProcessor\docs\guides"
xcopy /y "%PROJECT_DIR%\docs\guides\START_HERE.txt" "%DIST_DIR%\PSDBatchProcessor\docs\guides\" >nul 2>&1
xcopy /y "%PROJECT_DIR%\docs\guides\QUICK_REFERENCE.txt" "%DIST_DIR%\PSDBatchProcessor\docs\guides\" >nul 2>&1

REM Copy scripts directory
if not exist "%DIST_DIR%\PSDBatchProcessor\scripts" (
    xcopy /e /i /y "%PROJECT_DIR%\scripts" "%DIST_DIR%\PSDBatchProcessor\scripts" >nul 2>&1
    echo [OK] Scripts directory copied
) else (
    echo [INFO] Scripts directory already exists
)

REM Create backups directory
if not exist "%DIST_DIR%\PSDBatchProcessor\backups" (
    mkdir "%DIST_DIR%\PSDBatchProcessor\backups"
    echo [OK] Backups directory created
)

echo [OK] Files copied
echo.

REM Show build results
echo Build results:
echo - Executable: dist\PSDBatchProcessor\PSDBatchProcessor.exe
echo - Size:
dir /s /-c "%DIST_DIR%\PSDBatchProcessor\PSDBatchProcessor.exe" | findstr "bytes"

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Usage:
echo 1. Run: dist\PSDBatchProcessor\PSDBatchProcessor.exe
echo 2. First run will automatically create backups/ and config.json
echo 3. Follow documentation to configure Photoshop path and scripts directory
echo.
echo Quick start guide:
echo   dist\PSDBatchProcessor\docs\guides\START_HERE.txt
echo.

pause