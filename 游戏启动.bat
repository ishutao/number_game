@echo off
REM 检查是否有python环境
python --version >nul 2>&1
if %errorlevel% equ 0 (
    REM 检查文件完整性（示例：检查main.py是否存在）
    if exist "/mainpy/主界面.py" (
        python "/mainpy/主界面.py"
        goto :eof
    ) else (
        echo 文件缺失，请检查游戏文件完整性
        pause
        goto :eof
    )
)

REM 检查.venv能否使用
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" --version >nul 2>&1
    if %errorlevel% equ 0 (
        if exist "/mainpy/主界面.py" (
            ".venv\Scripts\python.exe" "/mainpy/主界面.py"
            goto :eof
        ) else (
            echo 文件缺失，请检查游戏文件完整性
            pause
            goto :eof
        )
    )
)

REM 跳转到下载页面（示例：打开浏览器访问下载地址）
echo 未检测到可用Python环境，正在打开下载页面...
start https://www.python.org/downloads/
pause
