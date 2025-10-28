@echo off
echo ====================================
echo   GitHub Auto-Updater
echo ====================================
echo.

set GIT_EMAIL=vladsfedin@yandex.ru

git config --global user.name "BengaminButton"
git config --global user.email "%GIT_EMAIL%"

echo [1/4] Добавление всех файлов...
git add .

echo.
echo [2/4] Коммит изменений...
git commit -m "Fix: Standalone build support - all DLLs included

- Updated electron_builder/builder_backend.py for standalone builds
- Removed exclude_binaries=True to include Python DLL
- Added a.binaries, a.zipfiles, a.datas to EXE parameters
- Added uac_admin=True for admin privileges
- Extended hiddenimports list (telebot, cv2, sounddevice, etc.)
- EXE now includes all dependencies (40-50 MB standalone)
- Works without Python installed
- Added build_v4_standalone.py for direct V4 builds
- Added BUILD_INSTRUCTIONS.md with detailed build guide"

echo.
echo [3/4] Push в GitHub...
echo Введи токен при запросе пароля
git push origin main

echo.
echo ====================================
echo   ГОТОВО!
echo ====================================
echo.
echo Изменения успешно отправлены в GitHub!
echo Проверь: https://github.com/BengaminButton/XillenStealer
echo.

pause
