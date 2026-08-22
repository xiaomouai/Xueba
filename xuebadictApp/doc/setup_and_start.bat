@echo off
chcp 65001 >nul
echo ========================================
echo 启动前检查和修复
echo ========================================
echo.

cd /d "%~dp0\xuebaApi"

echo [步骤1] 创建数据表...
mysql -u root -p xuebadict < add_new_tables.sql
if errorlevel 1 (
    echo ❌ 数据表创建失败
    pause
    exit /b 1
)
echo ✅ 数据表创建完成

echo.
echo [步骤2] 初始化会员数据...
mysql -u root -p xuebadict < init_membership_data.sql
if errorlevel 1 (
    echo ❌ 会员数据初始化失败
    pause
    exit /b 1
)
echo ✅ 会员数据初始化完成

echo.
echo [步骤3] 启动API服务...
python app.py

pause
