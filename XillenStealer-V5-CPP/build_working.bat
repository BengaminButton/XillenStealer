@echo off
cd /d "%~dp0"

echo Building XillenStealer V5 (Base Version)...
echo.

REM Сначала компилируем main.cpp напрямую без всех зависимостей
C:\msys64\mingw64\bin\g++.exe -o xillen_v5.exe src\core\main.cpp src\core\stealer.cpp -std=c++17 -static -O3

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [+] BUILD SUCCESS!
    dir /b xillen_v5.exe
    echo.
    echo Size:
    for %%A in (xillen_v5.exe) do echo %%~zA bytes
) else (
    echo.
    echo [!] BUILD FAILED!
    echo Checking main.cpp...
    type src\core\main.cpp | findstr /C:"#include"
)

pause

