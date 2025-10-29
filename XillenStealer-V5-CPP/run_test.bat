@echo off
chcp 65001 >nul
title XillenStealer V5 - Test Collector

echo.
echo ════════════════════════════════════════════════
echo   XILLENSTEALER V5 - DATA COLLECTOR
echo ════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo [*] Запуск сбора данных...
echo.

python test_stealer.py

echo.
echo [*] Готово!
pause
