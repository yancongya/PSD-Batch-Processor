@echo off
setlocal

echo Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo Installing dependencies...
python -m pip install --upgrade pip
pip install pyinstaller PyQt5 PyQt-Fluent-Widgets pywin32 pillow

echo Building Windowed Mode...
pyinstaller --name=PSDBatchProcessor-Windowed --noconsole --add-data="docs/guides/START_HERE.txt;docs/guides" --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" --add-data="scripts/production/*.jsx;scripts/production" --add-data="scripts/templates/*.jsx;scripts/templates" --add-data="scripts/examples/*.jsx;scripts/examples" --hidden-import=win32com --hidden-import=pythoncom --hidden-import=PIL --hidden-import=customtkinter --exclude-module=torch --exclude-module=torchvision --exclude-module=torchaudio --exclude-module=tensorflow --exclude-module=keras --exclude-module=scipy --exclude-module=numpy --exclude-module=sympy --exclude-module=onnxruntime --exclude-module=selenium --exclude-module=playwright --exclude-module=requests --exclude-module=beautifulsoup4 --exclude-module=lxml --exclude-module=bs4 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=cv2 --exclude-module=opencv-python --exclude-module=pytest --exclude-module=black --exclude-module=flake8 --exclude-module=langchain --exclude-module=openai --exclude-module=anthropic --exclude-module=transformers --exclude-module=tokenizers --exclude-module=huggingface_hub --exclude-module=tkinter --exclude-module=turtle --clean --noconfirm src/main.py

echo Building Console Mode...
pyinstaller --name=PSDBatchProcessor-Console --console --add-data="docs/guides/START_HERE.txt;docs/guides" --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" --add-data="scripts/production/*.jsx;scripts/production" --add-data="scripts/templates/*.jsx;scripts/templates" --add-data="scripts/examples/*.jsx;scripts/examples" --hidden-import=win32com --hidden-import=pythoncom --hidden-import=PIL --hidden-import=customtkinter --exclude-module=torch --exclude-module=torchvision --exclude-module=torchaudio --exclude-module=tensorflow --exclude-module=keras --exclude-module=scipy --exclude-module=numpy --exclude-module=sympy --exclude-module=onnxruntime --exclude-module=selenium --exclude-module=playwright --exclude-module=requests --exclude-module=beautifulsoup4 --exclude-module=lxml --exclude-module=bs4 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=cv2 --exclude-module=opencv-python --exclude-module=pytest --exclude-module=black --exclude-module=flake8 --exclude-module=langchain --exclude-module=openai --exclude-module=anthropic --exclude-module=transformers --exclude-module=tokenizers --exclude-module=huggingface_hub --exclude-module=tkinter --exclude-module=turtle --clean --noconfirm src/main.py

echo Building One-file Mode...
pyinstaller --name=PSDBatchProcessor-OneFile --noconsole --onefile --add-data="docs/guides/START_HERE.txt;docs/guides" --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" --add-data="scripts/production/*.jsx;scripts/production" --add-data="scripts/templates/*.jsx;scripts/templates" --add-data="scripts/examples/*.jsx;scripts/examples" --hidden-import=win32com --hidden-import=pythoncom --hidden-import=PIL --hidden-import=customtkinter --exclude-module=torch --exclude-module=torchvision --exclude-module=torchaudio --exclude-module=tensorflow --exclude-module=keras --exclude-module=scipy --exclude-module=numpy --exclude-module=sympy --exclude-module=onnxruntime --exclude-module=selenium --exclude-module=playwright --exclude-module=requests --exclude-module=beautifulsoup4 --exclude-module=lxml --exclude-module=bs4 --exclude-module=pandas --exclude-module=matplotlib --exclude-module=cv2 --exclude-module=opencv-python --exclude-module=pytest --exclude-module=black --exclude-module=flake8 --exclude-module=langchain --exclude-module=openai --exclude-module=anthropic --exclude-module=transformers --exclude-module=tokenizers --exclude-module=huggingface_hub --exclude-module=tkinter --exclude-module=turtle --clean --noconfirm src/main.py

echo Moving One-file executable...
if not exist "dist\PSDBatchProcessor-OneFile-Portable" mkdir "dist\PSDBatchProcessor-OneFile-Portable"
move /y "dist\PSDBatchProcessor-OneFile.exe" "dist\PSDBatchProcessor-OneFile-Portable\"

echo Copying files for Windowed Mode...
copy /y README.md dist\PSDBatchProcessor-Windowed\
if not exist "dist\PSDBatchProcessor-Windowed\docs\guides" mkdir "dist\PSDBatchProcessor-Windowed\docs\guides"
copy /y docs\guides\START_HERE.txt dist\PSDBatchProcessor-Windowed\docs\guides\
copy /y docs\guides\QUICK_REFERENCE.txt dist\PSDBatchProcessor-Windowed\docs\guides\
if not exist "dist\PSDBatchProcessor-Windowed\scripts" xcopy /e /i /y scripts dist\PSDBatchProcessor-Windowed\scripts
if not exist "dist\PSDBatchProcessor-Windowed\backups" mkdir "dist\PSDBatchProcessor-Windowed\backups"

echo Copying files for Console Mode...
copy /y README.md dist\PSDBatchProcessor-Console\
if not exist "dist\PSDBatchProcessor-Console\docs\guides" mkdir "dist\PSDBatchProcessor-Console\docs\guides"
copy /y docs\guides\START_HERE.txt dist\PSDBatchProcessor-Console\docs\guides\
copy /y docs\guides\QUICK_REFERENCE.txt dist\PSDBatchProcessor-Console\docs\guides\
if not exist "dist\PSDBatchProcessor-Console\scripts" xcopy /e /i /y scripts dist\PSDBatchProcessor-Console\scripts
if not exist "dist\PSDBatchProcessor-Console\backups" mkdir "dist\PSDBatchProcessor-Console\backups"

echo Copying files for OneFile Mode...
copy /y README.md dist\PSDBatchProcessor-OneFile-Portable\
if not exist "dist\PSDBatchProcessor-OneFile-Portable\docs\guides" mkdir "dist\PSDBatchProcessor-OneFile-Portable\docs\guides"
copy /y docs\guides\START_HERE.txt dist\PSDBatchProcessor-OneFile-Portable\docs\guides\
copy /y docs\guides\QUICK_REFERENCE.txt dist\PSDBatchProcessor-OneFile-Portable\docs\guides\
if not exist "dist\PSDBatchProcessor-OneFile-Portable\scripts" xcopy /e /i /y scripts dist\PSDBatchProcessor-OneFile-Portable\scripts
if not exist "dist\PSDBatchProcessor-OneFile-Portable\backups" mkdir "dist\PSDBatchProcessor-OneFile-Portable\backups"

echo Getting version...
set VERSION=%GITHUB_REF_NAME%
if "%VERSION%"=="" set VERSION=dev-%GITHUB_RUN_NUMBER%
echo version=%VERSION% >> %GITHUB_OUTPUT%

echo Creating release package...
set RELEASE_DIR=dist\PSDBatchProcessor-%VERSION%
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"
if exist "dist\PSDBatchProcessor-Windowed" xcopy /e /i /y "dist\PSDBatchProcessor-Windowed" "%RELEASE_DIR%\Windowed"
if exist "dist\PSDBatchProcessor-Console" xcopy /e /i /y "dist\PSDBatchProcessor-Console" "%RELEASE_DIR%\Console"
if exist "dist\PSDBatchProcessor-OneFile-Portable" xcopy /e /i /y "dist\PSDBatchProcessor-OneFile-Portable" "%RELEASE_DIR%\OneFile"
if exist "README.md" copy /y "README.md" "%RELEASE_DIR%\"

echo Created release package: %RELEASE_DIR%
echo Build completed successfully!