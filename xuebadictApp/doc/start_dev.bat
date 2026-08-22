@echo off
chcp 65001 >nul
echo ============================================================
echo 猫头鹰词典开发环境启动脚本
echo ============================================================
echo.

echo [1/2] 启动后端 API 服务...
echo.
start "猫头鹰词典 API" cmd /k "cd xuebaBackend && python app.py"

echo 等待 API 服务启动...
timeout /t 3 /nobreak >nul
echo.

echo [2/2] 启动 Flutter 应用...
echo.
cd xuebaAPP
flutter run

pause
