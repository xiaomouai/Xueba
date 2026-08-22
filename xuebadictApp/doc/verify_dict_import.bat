@echo off
chcp 65001 >nul
echo ========================================
echo 验证词书数据导入
echo ========================================
echo.

python verify_dict_import.py

echo.
pause
