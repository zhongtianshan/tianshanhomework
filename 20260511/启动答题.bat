@echo off
title 天津中考物理 · 2026预测题
cd /d "%~dp0"
echo 正在启动答题服务...
echo.
python app.py
if errorlevel 1 (
    echo.
    echo 启动失败，请确保已安装 Python 和 Flask
    echo 安装命令: pip install flask
    echo.
    pause
)
