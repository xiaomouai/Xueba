@echo off
chcp 65001 >nul
echo ========================================
echo  项目健康检查工具
echo ========================================
echo.

set ERROR_COUNT=0

echo [1/6] 检查Flutter环境...
flutter doctor >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flutter环境异常
    set /a ERROR_COUNT+=1
) else (
    echo ✅ Flutter环境正常
)

echo.
echo [2/6] 检查依赖包...
cd "%~dp0xuebaAPP"
flutter pub get >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 依赖包获取失败
    set /a ERROR_COUNT+=1
) else (
    echo ✅ 依赖包正常
)

echo.
echo [3/6] 分析代码质量...
flutter analyze --no-pub >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 代码分析发现问题（可能不影响运行）
) else (
    echo ✅ 代码分析通过
)

echo.
echo [4/6] 检查后端数据库...
cd "%~dp0xuebaApi"
python -c "import sqlite3; conn=sqlite3.connect('lioneng.db'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM dict_words'); count=cursor.fetchone()[0]; conn.close(); exit(0 if count > 0 else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 数据库未导入或为空
    echo    请运行: setup_database.bat
    set /a ERROR_COUNT+=1
) else (
    echo ✅ 数据库正常
)

echo.
echo [5/6] 检查后端配置...
if not exist "app.py" (
    echo ❌ 后端文件不存在
    set /a ERROR_COUNT+=1
) else (
    echo ✅ 后端文件存在
)

echo.
echo [6/6] 检查临时目录权限...
rd /s /q "%LOCALAPPDATA%\Temp\flutter_tools_test" >nul 2>&1
mkdir "%LOCALAPPDATA%\Temp\flutter_tools_test" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 临时目录权限受限（建议使用管理员权限）
) else (
    rd /s /q "%LOCALAPPDATA%\Temp\flutter_tools_test" >nul 2>&1
    echo ✅ 临时目录权限正常
)

cd "%~dp0"

echo.
echo ========================================
echo  检查结果
echo ========================================
echo.

if %ERROR_COUNT% equ 0 (
    echo ✅ 所有检查通过！项目可以正常运行
    echo.
    echo 🚀 启动步骤：
    echo    1. 运行 start_dev.bat 启动后端
    echo    2. 运行 run_flutter_app.bat 启动应用
    echo.
) else (
    echo ❌ 发现 %ERROR_COUNT% 个错误，需要修复
    echo.
    echo 🔧 修复步骤：
    if %ERROR_COUNT% gtr 2 (
        echo    1. 运行 fix_flutter_permission.bat
        echo    2. 运行 setup_database.bat
        echo    3. 重新运行此检查工具
    ) else (
        echo    请根据上面的提示逐个修复问题
    )
    echo.
)

echo ========================================
echo.
pause
