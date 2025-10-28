# 🔨 Сборка XillenStealer Builder V4.0

## Быстрая сборка:

```bash
.\build_builder_release.bat
```

## Что будет создано:

### 1. Portable версия:
- `XillenStealer Builder.exe` (~100 MB)
- Работает без установки
- Все зависимости внутри

### 2. ZIP архив:
- `XillenStealer-V4-Builder-Windows.zip` (~100 MB)
- Готовый релиз для GitHub

## Где файлы:

```
electron_builder/
  dist_release/
    XillenStealer Builder.exe       (portable)
    XillenStealer-V4-Builder-Windows.zip (архив)
```

## Иконка:

Используется: `electron_builder/renderer/assets/logo.png`

## Создание GitHub Release:

После сборки:

1. Перейти в `electron_builder/dist_release`
2. Взять `XillenStealer-V4-Builder-Windows.zip`
3. Создать Release на GitHub
4. Загрузить ZIP как asset

## Проверка:

После сборки запусти:
```bash
cd electron_builder\dist_release
.\XillenStealer Builder.exe
```

Должен запуститься билдер с UI!
