@echo off
cd /d "%~dp0"

echo Building XillenStealer V5...
echo.

C:\msys64\mingw64\bin\g++.exe -o xillen_v5.exe src\core\main.cpp src\core\stealer.cpp -std=c++17 -Wall 2>&1 | more

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [+] BUILD SUCCESS!
    dir /b xillen_v5.exe
) else (
    echo.
    echo [!] BUILD FAILED!
)

pause

