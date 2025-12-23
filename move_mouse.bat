@echo off
REM 自动移动鼠标脚本 - Windows 批处理入口
REM 适用于 Windows 命令提示符和 PowerShell

setlocal

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%move_mouse.py

REM 检查 Python 是否安装
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where python3 >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo 错误: 未找到 Python
        echo 请先安装 Python 3.6 或更高版本
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

echo 使用 Python: %PYTHON_CMD%

REM 检查 pyautogui 是否安装
%PYTHON_CMD% -c "import pyautogui" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 警告: pyautogui 未安装
    echo 正在尝试安装...
    %PYTHON_CMD% -m pip install pyautogui
    if %ERRORLEVEL% NEQ 0 (
        echo 错误: 无法安装 pyautogui
        echo 请手动运行: pip install pyautogui
        exit /b 1
    )
)

REM 运行 Python 脚本并传递所有参数
%PYTHON_CMD% "%PYTHON_SCRIPT%" %*

endlocal

