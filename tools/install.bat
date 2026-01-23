@echo off
chcp 65001 >nul
echo ========================================
echo PSD Batch Processor - Install Dependencies
echo ========================================
echo.

echo [1/3] Checking Python version...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
echo [OK] Python check passed
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo [3/3] Verifying installation...
python -c "import customtkinter; import win32com.client; print('[OK] All dependencies OK')"
if errorlevel 1 (
    echo [WARNING] Verification failed, but may still work
)

echo.
echo ========================================
echo Installation complete!
echo.
echo Run the following command to start:
echo   python main.py
echo.
echo Or double-click main.py
echo ========================================
pause