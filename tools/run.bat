@echo off
chcp 65001 >nul
echo ========================================
echo PSD Batch Processor
echo ========================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ and add it to PATH
    pause
    exit /b 1
)
echo [OK] Python found
echo.

echo Starting PSD Batch Processor...
echo.
cd /d "%~dp0.."
python src/main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start the application
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo Application closed
echo ========================================
pause