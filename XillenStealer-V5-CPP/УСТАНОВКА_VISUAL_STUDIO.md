# Установка Visual Studio Build Tools

## Ссылки:

### Вариант 1: Visual Studio Build Tools (Только компилятор)
**Скачать:** https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
- На странице выбрать "Build Tools for Visual Studio 2022"
- Скачать **build tools** (не полный Visual Studio)

### Вариант 2: Visual Studio Community (Полная IDE)
**Скачать:** https://visualstudio.microsoft.com/ru/vs/community/
- Скачать Visual Studio 2022 Community
- При установке выбрать "Desktop development with C++"

## Установка:

1. Запустить установщик
2. Выбрать "Desktop development with C++"
3. Установить
4. Перезагрузить компьютер
5. Открыть "Developer Command Prompt for VS 2022"

## Сборка проекта:

После установки, в терминале Developer Command Prompt:

```cmd
cd C:\Users\user\Desktop\XillenStealer-main\XillenStealer-V5-CPP
cl.exe /EHsc /std:c++20 /Fe:xillen_v5.exe src\core\main.cpp src\core\stealer.cpp [остальные файлы...] /link
```

Или создать `.bat` файл для автоматической сборки.

## Альтернатива: mingw-w64 (Проще)
Если Visual Studio слишком большой, можно использовать:
- Скачать: https://github.com/niXman/mingw-builds-binaries/releases
- Или использовать MSYS2 который уже установлен

## Быстрая установка через Chocolatey:

Если установлен Chocolatey:
```cmd
choco install visualstudio2022buildtools
```
