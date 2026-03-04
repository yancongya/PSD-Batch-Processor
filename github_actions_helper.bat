@echo off
echo ========================================
echo PSD Batch Processor - GitHub Actions Helper
echo ========================================
echo.
echo 选择操作:
echo 1. 触发 GitHub Actions 构建
echo 2. 打开 GitHub Actions 页面
echo 3. 本地测试构建
echo 4. 退出
echo.
set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" goto trigger
if "%choice%"=="2" goto open
if "%choice%"=="3" goto local
if "%choice%"=="4" goto end
goto invalid

:trigger
echo.
echo 正在触发 GitHub Actions 构建...
echo 请在浏览器中手动点击 "Run workflow" 按钮
echo.
start https://github.com/yancongya/PSD-Batch-Processor/actions/workflows/build.yml
goto end

:open
echo.
echo 打开 GitHub Actions 页面...
start https://github.com/yancongya/PSD-Batch-Processor/actions
goto end

:local
echo.
echo 开始本地构建测试...
echo.
python .github/scripts/build.py
echo.
echo 本地构建完成！
pause
goto end

:invalid
echo.
echo 无效选项，请重新运行脚本
pause
goto end

:end
echo.
echo 完成！