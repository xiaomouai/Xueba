@echo off
chcp 65001 >nul
echo ============================================================
echo 🦁 狮子英语 API - Swagger 文档版
echo ============================================================
echo.

echo 📦 检查依赖...
pip show flasgger >nul 2>&1
if errorlevel 1 (
    echo ❌ flasgger 未安装，正在安装...
    pip install flasgger flask-swagger-ui
) else (
    echo ✅ flasgger 已安装
)

echo.
echo 🚀 启动服务...
echo.
echo 📖 Swagger 文档: http://localhost:5000/api/docs
echo 📋 Swagger JSON: http://localhost:5000/apispec.json
echo 💚 健康检查: http://localhost:5000/health
echo.
echo ============================================================
echo.

python app.py
