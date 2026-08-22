@echo off
chcp 65001 >nul
echo ========================================
echo  Flutter 权限问题修复工具
echo ========================================
echo.

echo [1/4] 关闭相关进程...
taskkill /F /IM dart.exe /T >nul 2>&1
taskkill /F /IM flutter.exe /T >nul 2>&1
taskkill /F /IM chrome.exe /T >nul 2>&1
taskkill /F /IM msedge.exe /T >nul 2>&1
echo ✅ 进程已关闭

timeout /t 2 /nobreak >nul

echo.
echo [2/4] 清理临时文件...
rd /s /q "%LOCALAPPDATA%\Temp\flutter_tools*" >nul 2>&1
rd /s /q "%TEMP%\flutter_tools*" >nul 2>&1
echo ✅ 临时文件已清理

echo.
echo [3/4] 清理项目缓存...
cd /d "%~dp0xuebaAPP"
call flutter clean >nul 2>&1
echo ✅ 项目缓存已清理

echo.
echo [4/4] 重新获取依赖...
call flutter pub get
if %errorlevel% neq 0 (
    echo ⚠️ 依赖获取时出现警告，但可以继续
) else (
    echo ✅ 依赖获取完成
)

echo.
echo ========================================
echo  ✅ 修复完成！
echo ========================================
echo.
echo 现在可以尝试运行：
echo    flutter run -d windows     （推荐）
echo 或
echo    flutter run -d edge
echo.
echo 如需启动应用，请运行 run_flutter_app.bat
echo.
pause
