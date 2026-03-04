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
echo 4. Build all versions (windowed, console, onefile)
echo 5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    set BUILD_WINDOWED=1
    set BUILD_CONSOLE=0
    set BUILD_ONEFILE=0
) else if "%choice%"=="2" (
    set BUILD_WINDOWED=0
    set BUILD_CONSOLE=1
    set BUILD_ONEFILE=0
) else if "%choice%"=="3" (
    set BUILD_WINDOWED=0
    set BUILD_CONSOLE=0
    set BUILD_ONEFILE=1
) else if "%choice%"=="4" (
    set BUILD_WINDOWED=1
    set BUILD_CONSOLE=1
    set BUILD_ONEFILE=1
) else if "%choice%"=="5" (
    echo Exiting...
    pause
    exit /b 0
) else (
    echo [ERROR] Invalid choice!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Build Process
echo ========================================
echo.

REM Clean old build files
echo Cleaning old build files...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%PROJECT_DIR%\build" rmdir /s /q "%PROJECT_DIR%\build"
if exist "%PROJECT_DIR%\__pycache__" rmdir /s /q "%PROJECT_DIR%\__pycache__"
echo [OK] Old files cleaned
echo.

cd /d "%PROJECT_DIR%"

REM Define exclude modules
set EXCLUDE_MODULES=^
    --exclude-module=torch ^
    --exclude-module=torchvision ^
    --exclude-module=torchaudio ^
    --exclude-module=tensorflow ^
    --exclude-module=keras ^
    --exclude-module=scipy ^
    --exclude-module=numpy ^
    --exclude-module=sympy ^
    --exclude-module=onnxruntime ^
    --exclude-module=selenium ^
    --exclude-module=playwright ^
    --exclude-module=requests ^
    --exclude-module=beautifulsoup4 ^
    --exclude-module=lxml ^
    --exclude-module=bs4 ^
    --exclude-module=pandas ^
    --exclude-module=matplotlib ^
    --exclude-module=cv2 ^
    --exclude-module=opencv-python ^
    --exclude-module=pytest ^
    --exclude-module=black ^
    --exclude-module=flake8 ^
    --exclude-module=langchain ^
    --exclude-module=openai ^
    --exclude-module=anthropic ^
    --exclude-module=transformers ^
    --exclude-module=tokenizers ^
    --exclude-module=huggingface_hub ^
    --exclude-module=tkinter ^
    --exclude-module=turtle

REM Define hidden imports
set HIDDEN_IMPORTS=^
    --hidden-import=win32com ^
    --hidden-import=pythoncom ^
    --hidden-import=PIL ^
    --hidden-import=customtkinter

REM Define add data
set ADD_DATA=^
    --add-data="docs/guides/START_HERE.txt;docs/guides" ^
    --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" ^
    --add-data="scripts/production/*.jsx;scripts/production" ^
    --add-data="scripts/templates/*.jsx;scripts/templates" ^
    --add-data="scripts/examples/*.jsx;scripts/examples"

REM Function to copy additional files
:copy_files
set OUTPUT_DIR=%~1
xcopy /y "%PROJECT_DIR%\README.md" "%OUTPUT_DIR%\" >nul 2>&1
if not exist "%OUTPUT_DIR%\docs\guides" mkdir "%OUTPUT_DIR%\docs\guides"
xcopy /y "%PROJECT_DIR%\docs\guides\START_HERE.txt" "%OUTPUT_DIR%\docs\guides\" >nul 2>&1
xcopy /y "%PROJECT_DIR%\docs\guides\QUICK_REFERENCE.txt" "%OUTPUT_DIR%\docs\guides\" >nul 2>&1

if not exist "%OUTPUT_DIR%\scripts" (
    xcopy /e /i /y "%PROJECT_DIR%\scripts" "%OUTPUT_DIR%\scripts" >nul 2>&1
)

if not exist "%OUTPUT_DIR%\backups" (
    mkdir "%OUTPUT_DIR%\backups"
)
goto :eof

REM Build Windowed mode
if "%BUILD_WINDOWED%"=="1" (
    echo.
    echo ========================================
    echo Building Windowed Mode
    echo ========================================
    echo.

    pyinstaller ^
        --name="PSDBatchProcessor-Windowed" ^
        --noconsole ^
        %ADD_DATA% ^
        %HIDDEN_IMPORTS% ^
        %EXCLUDE_MODULES% ^
        --clean ^
        --noconfirm ^
        src/main.py

    if errorlevel 1 (
        echo.
        echo [ERROR] Windowed mode build failed!
        echo Continuing with next build mode...
        goto :skip_windowed
    )

    echo.
    echo [SUCCESS] Windowed mode build completed!
    echo.

    call :copy_files "%DIST_DIR%\PSDBatchProcessor-Windowed"
)

:skip_windowed

REM Build Console mode
if "%BUILD_CONSOLE%"=="1" (
    echo.
    echo ========================================
    echo Building Console Mode
    echo ========================================
    echo.

    pyinstaller ^
        --name="PSDBatchProcessor-Console" ^
        --console ^
        %ADD_DATA% ^
        %HIDDEN_IMPORTS% ^
        %EXCLUDE_MODULES% ^
        --clean ^
        --noconfirm ^
        src/main.py

    if errorlevel 1 (
        echo.
        echo [ERROR] Console mode build failed!
        echo Continuing with next build mode...
        goto :skip_console
    )

    echo.
    echo [SUCCESS] Console mode build completed!
    echo.

    call :copy_files "%DIST_DIR%\PSDBatchProcessor-Console"
)

:skip_console

REM Build Console mode
if "%BUILD_CONSOLE%"=="1" (
    echo.
    echo ========================================
    echo Building Console Mode
    echo ========================================
    echo.

    pyinstaller ^
        --name="PSDBatchProcessor-Console" ^
        --console ^
        %ADD_DATA% ^
        %HIDDEN_IMPORTS% ^
        %EXCLUDE_MODULES% ^
        --clean ^
        --noconfirm ^
        src/main.py

    if errorlevel 1 (
        echo.
        echo [ERROR] Console mode build failed!
        pause
        exit /b 1
    )

    echo.
    echo [SUCCESS] Console mode build completed!
    echo.

    call :copy_files "%DIST_DIR%\PSDBatchProcessor-Console"
)

REM Build One-file mode
if "%BUILD_ONEFILE%"=="1" (
    echo.
    echo ========================================
    echo Building One-file Mode
    echo ========================================
    echo.

    pyinstaller ^
        --name="PSDBatchProcessor-OneFile" ^
        --noconsole ^
        --onefile ^
        %ADD_DATA% ^
        %HIDDEN_IMPORTS% ^
        %EXCLUDE_MODULES% ^
        --clean ^
        --noconfirm ^
        src/main.py

    if errorlevel 1 (
        echo.
        echo [ERROR] One-file mode build failed!
        echo Continuing with result display...
        goto :skip_onefile
    )

    echo.
    echo [SUCCESS] One-file mode build completed!
    echo.

    REM For one-file mode, create output directory structure
    set ONEFILE_DIR=%DIST_DIR%\PSDBatchProcessor-OneFile-Portable
    if not exist "%ONEFILE_DIR%" mkdir "%ONEFILE_DIR%"

    move /y "%DIST_DIR%\PSDBatchProcessor-OneFile.exe" "%ONEFILE_DIR%\" >nul 2>&1
    call :copy_files "%ONEFILE_DIR%"
)

:skip_onefile

echo.
echo ========================================
echo All Builds Complete!
echo ========================================
echo.

REM Show build results
echo Build results:
echo.

if "%BUILD_WINDOWED%"=="1" (
    echo [Windowed Mode]
    echo - Directory: dist\PSDBatchProcessor-Windowed\
    echo - Executable: PSDBatchProcessor-Windowed.exe
    for %%A in ("%DIST_DIR%\PSDBatchProcessor-Windowed\PSDBatchProcessor-Windowed.exe") do echo - Size: %%~zA bytes
    echo.
)

if "%BUILD_CONSOLE%"=="1" (
    echo [Console Mode]
    echo - Directory: dist\PSDBatchProcessor-Console\
    echo - Executable: PSDBatchProcessor-Console.exe
    for %%A in ("%DIST_DIR%\PSDBatchProcessor-Console\PSDBatchProcessor-Console.exe") do echo - Size: %%~zA bytes
    echo.
)

if "%BUILD_ONEFILE%"=="1" (
    echo [One-file Mode]
    echo - Directory: dist\PSDBatchProcessor-OneFile-Portable\
    echo - Executable: PSDBatchProcessor-OneFile.exe
    for %%A in ("%DIST_DIR%\PSDBatchProcessor-OneFile-Portable\PSDBatchProcessor-OneFile.exe") do echo - Size: %%~zA bytes
    echo.
)

echo.
echo ========================================
echo Usage Instructions
echo ========================================
echo.
echo 1. Windowed Mode (推荐):
echo    - Run: dist\PSDBatchProcessor-Windowed\PSDBatchProcessor-Windowed.exe
echo    - No console window, suitable for production
echo.
echo 2. Console Mode (调试用):
echo    - Run: dist\PSDBatchProcessor-Console\PSDBatchProcessor-Console.exe
echo    - Shows console output, suitable for debugging
echo.
echo 3. One-file Mode (便携版):
echo    - Run: dist\PSDBatchProcessor-OneFile-Portable\PSDBatchProcessor-OneFile.exe
echo    - Single executable, portable distribution
echo.
echo Quick start guide:
echo   Each version includes docs\guides\START_HERE.txt
echo.
echo ========================================
echo Build process completed!
echo Press any key to close this window...
echo ========================================

pause