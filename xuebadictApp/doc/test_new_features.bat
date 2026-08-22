@echo off
chcp 65001 >nul
echo ========================================
echo 测试会员系统、闯关和听写模块
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 检查服务是否运行...
curl -s http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ API服务未启动，请先运行: python app.py
    pause
    exit /b 1
)
echo ✅ API服务正常运行

echo.
echo [2/2] 开始测试...
python test_new_features.py

echo.
echo ========================================
echo 测试完成！
echo ========================================
pause
