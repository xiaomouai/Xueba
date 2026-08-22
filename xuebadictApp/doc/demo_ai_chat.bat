@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 狮子英语AI聊天功能演示
echo ========================================
echo.
echo 本演示将展示AI聊天功能的完整流程
echo.
pause

echo.
echo [1/3] 启动后端服务...
echo ----------------------------------------
cd /d "%~dp0xuebaApi"
start "狮子英语后端" cmd /k "python app.py"
timeout /t 5 /nobreak >nul

echo.
echo [2/3] 等待服务启动完成...
timeout /t 3 /nobreak >nul

echo.
echo [3/3] 运行测试脚本...
echo ----------------------------------------
python test_ai_chat.py

echo.
echo ========================================
echo ✅ 演示完成
echo ========================================
echo.
echo 📖 查看文档：
echo    - AI_CHAT_API.md - API接口文档
echo    - AI_INTEGRATION_COMPLETE.md - 集成说明
echo.
echo 🌐 访问Swagger文档：
echo    http://localhost:5000/api/docs
echo.
pause
