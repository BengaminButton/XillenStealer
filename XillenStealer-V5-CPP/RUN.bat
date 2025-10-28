@echo off
cd /d "%~dp0"
echo.
echo ============================================
echo   XILLENSTEALER V5 - READY TO RUN
echo ============================================
echo.
if exist xillen_v5.exe (
    echo Found: xillen_v5.exe
    echo.
    echo Starting...
    echo.
    xillen_v5.exe
) else (
    echo Error: xillen_v5.exe not found!
    echo Please run BUILD_V5.bat first
)
echo.
echo ============================================
pause
