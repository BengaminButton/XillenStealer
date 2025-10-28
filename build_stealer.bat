@echo off
chcp 65001 >nul
echo ========================================
echo   КОМПИЛЯЦИЯ Xillena.exe
echo ========================================
echo.

echo [1/4] Проверка PyInstaller...
python -m pip install pyinstaller --upgrade --quiet
if errorlevel 1 (
    echo ОШИБКА: PyInstaller не установлен!
    pause
    exit /b 1
)
echo OK PyInstaller найден

echo.
echo [2/4] Установка зависимостей...
python -m pip install pynput cryptography requests pillow psutil pywin32 pycryptodome --quiet
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости!
    pause
    exit /b 1
)
echo OK Зависимости установлены

echo.
echo [3/4] Компиляция в EXE...
pyinstaller --clean stealer.spec
if errorlevel 1 (
    echo ОШИБКА: Компиляция не удалась!
    pause
    exit /b 1
)
echo OK Компиляция завершена

echo.
echo [4/4] Проверка результата...
if exist "dist\Xillena.exe" (
    echo.
    echo ========================================
    echo   КОМПИЛЯЦИЯ УСПЕШНА!
    echo ========================================
    echo.
    echo Файл создан: dist\Xillena.exe
    echo.
) else (
    echo ОШИБКА: Xillena.exe не найден!
    pause
    exit /b 1
)

echo Готово! Запусти dist\Xillena.exe для проверки
echo.
pause
