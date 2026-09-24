@echo off
chcp 65001 >nul
title GitHub 仓库同步助手 - monkey
cd /d "%~dp0"

echo ======================================================================
echo          同步代码到 GitHub: git@github.com:zhr2271854800/monkey.git
echo ======================================================================
echo.
echo [*] 添加修改...
git add .
set /p msg="请输入本次提交的说明 (直接回车默认更新): "
if "%msg%"=="" set msg=update: sync changes

git commit -m "%msg%"
echo.
echo [*] 正在推送至 GitHub main 分支...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] 恭喜！最新修改已成功推送到 GitHub 仓库！
    echo 仓库访问地址: https://github.com/zhr2271854800/monkey
    echo ======================================================================
) else (
    echo.
    echo [ERROR] 推送遇到问题，请检查网络或配置。
)

echo.
pause
