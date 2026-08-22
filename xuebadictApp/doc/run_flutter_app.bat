@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo  Flutter 应用启动器
echo ========================================
echo.

echo 🧹 预清理...
taskkill /F /IM chrome.exe /T >nul 2>&1
rd /s /q "%LOCALAPPDATA%\Temp\flutter_tools*" >nul 2>&1

cd xuebaAPP

echo.
echo 📱 请选择运行平台：
echo.
echo 1. Windows 桌面版（推荐，稳定）
echo 2. Edge 浏览器
echo 3. Chrome 浏览器
echo 4. Android 模拟器
echo 5. 查看可用设备
echo.
set /p choice="请输入选项 (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 启动 Windows 桌面版...
    flutter run -d windows
) else if "%choice%"=="2" (
    echo.
    echo 🌐 启动 Edge 浏览器版...
    flutter run -d edge
) else if "%choice%"=="3" (
    echo.
    echo 🌐 启动 Chrome 浏览器版...
    flutter run -d chrome
) else if "%choice%"=="4" (
    echo.
    echo 📱 启动 Android 模拟器版...
    flutter run
) else if "%choice%"=="5" (
    echo.
    echo 📋 可用设备列表：
    flutter devices
    echo.
    pause
    goto :eof
) else (
    echo.
    echo ⚠️ 无效选项，使用默认 Windows 版本
    flutter run -d windows
)

pause
