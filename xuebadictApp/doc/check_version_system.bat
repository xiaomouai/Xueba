@echo off
REM 版本更新系统诊断脚本
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo 版本更新系统诊断检查
echo ============================================================
echo.

REM 检查 Python 环境
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 环境正常
    python --version
) else (
    echo ❌ Python 环境未找到
    goto :error
)

echo.

REM 检查后端文件
echo [2/5] 检查后端文件...
if exist "xuebaApi\api\version.py" (
    echo ✅ version.py 存在
) else (
    echo ❌ version.py 未找到
    goto :error
)

if exist "xuebaApi\models\version_model.py" (
    echo ✅ version_model.py 存在
) else (
    echo ❌ version_model.py 未找到
    goto :error
)

echo.

REM 检查前端文件
echo [3/5] 检查前端文件...
if exist "xuebaAPP\lib\pages\settings_page.dart" (
    echo ✅ settings_page.dart 存在
) else (
    echo ❌ settings_page.dart 未找到
    goto :error
)

if exist "xuebaAPP\lib\utils\auto_update_service.dart" (
    echo ✅ auto_update_service.dart 存在
) else (
    echo ❌ auto_update_service.dart 未找到
    goto :error
)

if exist "xuebaAPP\lib\utils\settings_helper.dart" (
    echo ✅ settings_helper.dart 存在
) else (
    echo ❌ settings_helper.dart 未找到
    goto :error
)

echo.

REM 检查测试文件
echo [4/5] 检查测试文件...
if exist "test_version_update.py" (
    echo ✅ test_version_update.py 存在
) else (
    echo ❌ test_version_update.py 未找到
    goto :error
)

if exist "test_version_update.dart" (
    echo ✅ test_version_update.dart 存在
) else (
    echo ❌ test_version_update.dart 未找到
    goto :error
)

echo.

REM 运行测试
echo [5/5] 运行测试...
chcp 65001 >nul
python test_version_update.py
if %errorlevel% equ 0 (
    echo ✅ 测试通过
) else (
    echo ❌ 测试失败
    goto :error
)

echo.
echo ============================================================
echo ✅ 所有检查通过！版本更新系统正常。
echo ============================================================
pause
exit /b 0

:error
echo.
echo ============================================================
echo ❌ 检查失败，请解决上述问题。
echo ============================================================
pause
exit /b 1
