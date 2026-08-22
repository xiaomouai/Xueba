@echo off
chcp 65001 >nul
echo ========================================
echo  🚀 猫头鹰词典 - 完整启动流程
echo ========================================
echo.

cd /d "%~dp0"

echo 📋 启动检查清单：
echo    ☐ 1. 数据库初始化
echo    ☐ 2. 后端服务启动
echo    ☐ 3. 音频功能测试
echo    ☐ 4. Flutter应用启动
echo.
pause

REM ==================== 步骤1：数据库初始化 ====================
echo.
echo ========================================
echo  [1/4] 数据库初始化
echo ========================================
echo.

cd xuebaApi

python -c "import sqlite3; conn=sqlite3.connect('lioneng.db'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM dict_words'); count=cursor.fetchone()[0]; print(f'当前单词数: {count}'); conn.close()" 2>nul

if %errorlevel% neq 0 (
    echo ⚠️  数据库未初始化或为空
    echo.
    set /p init_db="是否现在初始化数据库？(y/n): "
    if /i "%init_db%"=="y" (
        cd ..
        call setup_database.bat
        cd xuebaApi
    ) else (
        echo ⏭️  跳过数据库初始化
    )
) else (
    echo ✅ 数据库已就绪
)

echo.
pause

REM ==================== 步骤2：启动后端服务 ====================
echo.
echo ========================================
echo  [2/4] 启动后端服务
echo ========================================
echo.

echo 正在启动Flask服务器...
echo 服务地址: http://localhost:5000
echo API文档: http://localhost:5000/api/docs
echo.
echo ⚠️  请保持此窗口打开！
echo.

start "猫头鹰词典-后端服务" cmd /k "cd /d "%~dp0xuebaApi" && python app.py"

echo 等待服务启动...
timeout /t 3 /nobreak >nul

REM 检查服务是否启动
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 后端服务启动成功
) else (
    echo ⚠️  后端服务可能未完全启动
    echo    请检查后端服务窗口的输出
)

echo.
pause

REM ==================== 步骤3：音频功能测试 ====================
echo.
echo ========================================
echo  [3/4] 音频功能测试
echo ========================================
echo.

set /p test_audio="是否测试音频功能？(y/n): "
if /i "%test_audio%"=="y" (
    cd ..
    call test_audio.bat
    cd xuebaApi
) else (
    echo ⏭️  跳过音频测试
)

echo.
pause

REM ==================== 步骤4：启动Flutter应用 ====================
echo.
echo ========================================
echo  [4/4] 启动Flutter应用
echo ========================================
echo.

cd ..\xuebaAPP

echo 清理Flutter缓存...
call flutter clean >nul 2>&1

echo 获取依赖...
call flutter pub get >nul 2>&1

echo.
echo 📱 请选择运行平台：
echo.
echo 1. Windows 桌面版（推荐，稳定）
echo 2. Edge 浏览器（已修复音频问题）
echo 3. Chrome 浏览器（已修复音频问题）
echo 4. 查看可用设备
echo.
set /p platform="请输入选项 (1-4): "

if "%platform%"=="1" (
    echo.
    echo 🚀 启动 Windows 桌面版...
    start "猫头鹰词典-Windows" cmd /k "cd /d "%~dp0xuebaAPP" && flutter run -d windows"
) else if "%platform%"=="2" (
    echo.
    echo 🌐 启动 Edge 浏览器版...
    start "猫头鹰词典-Edge" cmd /k "cd /d "%~dp0xuebaAPP" && flutter run -d edge"
) else if "%platform%"=="3" (
    echo.
    echo 🌐 启动 Chrome 浏览器版...
    start "猫头鹰词典-Chrome" cmd /k "cd /d "%~dp0xuebaAPP" && flutter run -d chrome"
) else if "%platform%"=="4" (
    echo.
    echo 📋 可用设备列表：
    flutter devices
    echo.
    pause
    goto :eof
) else (
    echo.
    echo ⚠️  无效选项，使用默认 Windows 版本
    start "猫头鹰词典-Windows" cmd /k "cd /d "%~dp0xuebaAPP" && flutter run -d windows"
)

cd ..

echo.
echo ========================================
echo  ✅ 所有服务已启动！
echo ========================================
echo.
echo 📝 服务信息：
echo    - 后端API: http://localhost:5000
echo    - API文档: http://localhost:5000/api/docs
echo    - Flutter应用已在新窗口启动
echo.
echo 💡 使用提示：
echo    1. 点击🔊按钮测试单词发音
echo    2. 选择词书开始学习
echo    3. 查看API文档了解接口详情
echo.
echo ⚠️  关闭说明：
echo    - 关闭本窗口不影响服务运行
echo    - 要停止服务，请关闭对应的窗口
echo    - 或按 Ctrl+C 停止服务
echo.
pause
