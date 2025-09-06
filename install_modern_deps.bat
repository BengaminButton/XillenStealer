@echo off
echo Установка современных зависимостей для красивого интерфейса...
echo.

echo Устанавливаем ttkbootstrap...
pip install ttkbootstrap

echo.
echo Устанавливаем дополнительные зависимости...
pip install pycryptodome
pip install browser-cookie3
pip install pillow
pip install psutil
pip install pyTelegramBotAPI
pip install requests

echo.
echo Установка завершена!
echo Теперь можно запустить: python builder_modern.py
pause
