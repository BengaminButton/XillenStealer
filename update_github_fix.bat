@echo off
chcp 65001 >nul
echo ========================================
echo   ОБНОВЛЕНИЕ GITHUB
echo ========================================
echo.

echo [1/3] Добавление изменений...
git add requirements.txt
git add build_stealer.bat
git add stealer.spec
git add FIX_V4_INSTRUCTIONS.md
git add update_github_fix.bat
if errorlevel 1 (
    echo ОШИБКА: Не удалось добавить файлы!
    pause
    exit /b 1
)
echo OK Файлы добавлены

echo.
echo [2/3] Коммит изменений...
git commit -m "Fix: добавлены все зависимости включая pynput, cv2, sounddevice в requirements.txt и stealer.spec для исправления ошибки ModuleNotFoundError при запуске без Python"
if errorlevel 1 (
    echo ОШИБКА: Не удалось создать коммит!
    pause
    exit /b 1
)
echo OK Коммит создан

echo.
echo [3/3] Загрузка на GitHub...
git push origin main
if errorlevel 1 (
    echo ОШИБКА: Не удалось загрузить на GitHub!
    pause
    exit /b 1
)
echo OK Изменения загружены на GitHub

echo.
echo ========================================
echo   ГОТОВО!
echo ========================================
echo.
echo GitHub обновлен с исправлениями
echo.
pause
