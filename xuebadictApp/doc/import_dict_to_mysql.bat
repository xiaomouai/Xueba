@echo off
chcp 65001 >nul
echo ========================================
echo 词书数据导入MySQL数据库
echo ========================================
echo.

echo 【重要提示】
echo 1. 请确保MySQL服务已启动
echo 2. 请修改 .env.dict_import 文件中的数据库配置
echo 3. 导入过程可能需要较长时间，请耐心等待
echo.

set /p confirm=确认开始导入? (Y/N): 
if /i not "%confirm%"=="Y" (
    echo 已取消导入
    pause
    exit /b
)

echo.
echo 开始导入词书数据...
echo.

python import_dict_to_mysql.py

echo.
echo ========================================
echo 导入完成
echo ========================================
pause
