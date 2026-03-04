@echo off
chcp 65001 >nul

echo ========================================
echo PSD Batch Processor Build Tool
echo ========================================
echo.

set PROJECT_DIR=%~dp0..
set DIST_DIR=%PROJECT_DIR%\dist

echo Project directory: %PROJECT_DIR%
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python installed
echo.

echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [WARNING] PyInstaller not found, installing...
    pip install pyinstaller
)
echo [OK] PyInstaller installed
echo.

echo Select build mode:
echo 1. Windowed mode (recommended, no console)
echo 2. Console mode (for debugging)
echo 3. One-file mode (portable)
echo 4. Build all versions (windowed, console, onefile)
echo 5. Exit
echo.
set /p choice=Enter choice (1-5):

if "%choice%"=="1" goto build_windowed
if "%choice%"=="2" goto build_console
if "%choice%"=="3" goto build_onefile
if "%choice%"=="4" goto build_all
if "%choice%"=="5" goto end
echo [ERROR] Invalid choice!
pause
exit /b 1

:build_windowed
set BUILD_WINDOWED=1
set BUILD_CONSOLE=0
set BUILD_ONEFILE=0
goto start_build

:build_console
set BUILD_WINDOWED=0
set BUILD_CONSOLE=1
set BUILD_ONEFILE=0
goto start_build

:build_onefile
set BUILD_WINDOWED=0
set BUILD_CONSOLE=0
set BUILD_ONEFILE=1
goto start_build

:build_all
set BUILD_WINDOWED=1
set BUILD_CONSOLE=1
set BUILD_ONEFILE=1
goto start_build

:start_build
echo.
echo ========================================
echo Starting Build Process
echo ========================================
echo.

echo Cleaning old build files...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%PROJECT_DIR%\build" rmdir /s /q "%PROJECT_DIR%\build"
if exist "%PROJECT_DIR%\__pycache__" rmdir /s /q "%PROJECT_DIR%\__pycache__"
echo [OK] Old files cleaned
echo.

cd /d "%PROJECT_DIR%"

if "%BUILD_WINDOWED%"=="1" goto do_build_windowed
if "%BUILD_CONSOLE%"=="1" goto do_build_console
if "%BUILD_ONEFILE%"=="1" goto do_build_onefile
goto show_results

:do_build_windowed
echo.
echo ========================================
echo Building Windowed Mode
echo ========================================
echo.

pyinstaller --name="PSDBatchProcessor-Windowed" --noconsole --add-data="docs/guides/START_HERE.txt;docs/guides" --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" --add-data="scripts/production/*.jsx;scripts/production" --add-data="scripts/templates/*.jsx;scripts/templates" --add-data="scripts/examples/*.jsx;scripts/examples" --hidden-import=win32com --hidden-import=pythoncom --hidden-import=PIL --hidden-import=customtkinter --exclude-module=torch --exclude-module=torchvision --exclude-module=torchaudio --exclude-module=tensorflow --exclude-module=keras --exclude-module=scipy --exclude-module=numpy --exclude-module=sympy --exclude-module=onnxruntime --exclude-module=selenium --exclude-module=playwright --exclude-module=requests --exclude-module=beautifulsoup4 --exclude-module=lxml --exclude-module=bs4 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=cv2 --exclude-module=opencv-python --exclude-module=pytest --exclude-module=black --exclude-module=flake8 --exclude-module=langchain --exclude-module=openai --exclude-module=anthropic --exclude-module=transformers --exclude-module=tokenizers --exclude-module=huggingface_hub --exclude-module=tkinter --exclude-module=turtle --clean --noconfirm src/main.py

if errorlevel 1 (
    echo [ERROR] Windowed mode build failed!
) else (
    echo [SUCCESS] Windowed mode build completed!
    call :copy_files "%DIST_DIR%\PSDBatchProcessor-Windowed"
)

if "%BUILD_CONSOLE%"=="1" goto do_build_console
if "%BUILD_ONEFILE%"=="1" goto do_build_onefile
goto show_results

:do_build_console
echo.
echo ========================================
echo Building Console Mode
echo ========================================
echo.

pyinstaller --name="PSDBatchProcessor-Console" --console --add-data="docs/guides/START_HERE.txt;docs/guides" --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" --add-data="scripts/production/*.jsx;scripts/production" --add-data="scripts/templates/*.jsx;scripts/templates" --add-data="scripts/examples/*.jsx;scripts/examples" --hidden-import=win32com --hidden-import=pythoncom --hidden-import=PIL --hidden-import=customtkinter --exclude-module=torch --exclude-module=torchvision --exclude-module=torchaudio --exclude-module=tensorflow --exclude-module=keras --exclude-module=scipy --exclude-module=numpy --exclude-module=sympy --exclude-module=onnxruntime --exclude-module=selenium --exclude-module=playwright --exclude-module=requests --exclude-module=beautifulsoup4 --exclude-module=lxml --exclude-module=bs4 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=cv2 --exclude-module=opencv-python --exclude-module=pytest --exclude-module=black --exclude-module=flake8 --exclude-module=langchain --exclude-module=openai --exclude-module=anthropic --exclude-module=transformers --exclude-module=tokenizers --exclude-module=huggingface_hub --exclude-module=tkinter --exclude-module=turtle --clean --noconfirm src/main.py

if errorlevel 1 (
    echo [ERROR] Console mode build failed!
) else (
    echo [SUCCESS] Console mode build completed!
    call :copy_files "%DIST_DIR%\PSDBatchProcessor-Console"
)

if "%BUILD_ONEFILE%"=="1" goto do_build_onefile
goto show_results

:do_build_onefile
echo.
echo ========================================
echo Building One-file Mode
echo ========================================
echo.

pyinstaller --name="PSDBatchProcessor-OneFile" --noconsole --onefile --add-data="docs/guides/START_HERE.txt;docs/guides" --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" --add-data="scripts/production/*.jsx;scripts/production" --add-data="scripts/templates/*.jsx;scripts/templates" --add-data="scripts/examples/*.jsx;scripts/examples" --hidden-import=win32com --hidden-import=pythoncom --hidden-import=PIL --hidden-import=customtkinter --exclude-module=torch --exclude-module=torchvision --exclude-module=torchaudio --exclude-module=tensorflow --exclude-module=keras --exclude-module=scipy --exclude-module=numpy --exclude-module=sympy --exclude-module=onnxruntime --exclude-module=selenium --exclude-module=playwright --exclude-module=requests --exclude-module=beautifulsoup4 --exclude-module=lxml --exclude-module=bs4 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=cv2 --exclude-module=opencv-python --exclude-module=pytest --exclude-module=black --exclude-module=flake8 --exclude-module=langchain --exclude-module=openai --exclude-module=anthropic --exclude-module=transformers --exclude-module=tokenizers --exclude-module=huggingface_hub --exclude-module=tkinter --exclude-module=turtle --clean --noconfirm src/main.py

if errorlevel 1 (
    echo [ERROR] One-file mode build failed!
) else (
    echo [SUCCESS] One-file mode build completed!
    set ONEFILE_DIR=%DIST_DIR%\PSDBatchProcessor-OneFile-Portable
    if not exist "%ONEFILE_DIR%" mkdir "%ONEFILE_DIR%"
    move /y "%DIST_DIR%\PSDBatchProcessor-OneFile.exe" "%ONEFILE_DIR%\" >nul 2>&1
    call :copy_files "%ONEFILE_DIR%"
)

goto show_results

:copy_files
set OUTPUT_DIR=%~1
xcopy /y "%PROJECT_DIR%\README.md" "%OUTPUT_DIR%\" >nul 2>&1
if not exist "%OUTPUT_DIR%\docs\guides" mkdir "%OUTPUT_DIR%\docs\guides"
xcopy /y "%PROJECT_DIR%\docs\guides\START_HERE.txt" "%OUTPUT_DIR%\docs\guides\" >nul 2>&1
xcopy /y "%PROJECT_DIR%\docs\guides\QUICK_REFERENCE.txt" "%OUTPUT_DIR%\docs\guides\" >nul 2>&1
if not exist "%OUTPUT_DIR%\scripts" xcopy /e /i /y "%PROJECT_DIR%\scripts" "%OUTPUT_DIR%\scripts" >nul 2>&1
if not exist "%OUTPUT_DIR%\backups" mkdir "%OUTPUT_DIR%\backups"
goto :eof

:show_results
echo.
echo ========================================
echo Build Results
echo ========================================
echo.

if "%BUILD_WINDOWED%"=="1" (
    echo [Windowed Mode]
    echo Directory: dist\PSDBatchProcessor-Windowed\
    if exist "%DIST_DIR%\PSDBatchProcessor-Windowed\PSDBatchProcessor-Windowed.exe" (
        echo Executable: PSDBatchProcessor-Windowed.exe
        for %%A in ("%DIST_DIR%\PSDBatchProcessor-Windowed\PSDBatchProcessor-Windowed.exe") do echo Size: %%~zA bytes
    ) else (
        echo [FAILED] Executable not found
    )
    echo.
)

if "%BUILD_CONSOLE%"=="1" (
    echo [Console Mode]
    echo Directory: dist\PSDBatchProcessor-Console\
    if exist "%DIST_DIR%\PSDBatchProcessor-Console\PSDBatchProcessor-Console.exe" (
        echo Executable: PSDBatchProcessor-Console.exe
        for %%A in ("%DIST_DIR%\PSDBatchProcessor-Console\PSDBatchProcessor-Console.exe") do echo Size: %%~zA bytes
    ) else (
        echo [FAILED] Executable not found
    )
    echo.
)

if "%BUILD_ONEFILE%"=="1" (
    echo [One-file Mode]
    echo Directory: dist\PSDBatchProcessor-OneFile-Portable\
    if exist "%DIST_DIR%\PSDBatchProcessor-OneFile-Portable\PSDBatchProcessor-OneFile.exe" (
        echo Executable: PSDBatchProcessor-OneFile.exe
        for %%A in ("%DIST_DIR%\PSDBatchProcessor-OneFile-Portable\PSDBatchProcessor-OneFile.exe") do echo Size: %%~zA bytes
    ) else (
        echo [FAILED] Executable not found
    )
    echo.
)

echo ========================================
echo Usage Instructions
echo ========================================
echo.
echo 1. Windowed Mode (推荐):
echo    Run: dist\PSDBatchProcessor-Windowed\PSDBatchProcessor-Windowed.exe
echo.
echo 2. Console Mode (调试用):
echo    Run: dist\PSDBatchProcessor-Console\PSDBatchProcessor-Console.exe
echo.
echo 3. One-file Mode (便携版):
echo    Run: dist\PSDBatchProcessor-OneFile-Portable\PSDBatchProcessor-OneFile.exe
echo.
echo Quick start guide: docs\guides\START_HERE.txt
echo.
echo ========================================
echo Press any key to close...
echo ========================================
pause

:end
exit /b 0