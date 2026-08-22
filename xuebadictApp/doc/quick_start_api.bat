@echo off
chcp 65001 >nul
echo ========================================
echo 快速启动 API 服务
echo ========================================
echo.

cd /d "%~dp0\xuebaApi"

echo [提示] 确保已完成以下步骤:
echo   1. 创建数据表: mysql -u root -p xuebadict ^< add_new_tables.sql
echo   2. 初始化数据: mysql -u root -p xuebadict ^< init_membership_data.sql
echo.
echo 按任意键开始启动服务...
pause >nul

echo.
echo [启动] 正在启动API服务...
python app.py

pause
