"""
Модуль для правильной загрузки шрифтов в Tkinter
"""

import os
import platform
import tkinter as tk
import tkinter.font as tkFont
from pathlib import Path

def install_font(font_path):
    """Устанавливает шрифт в систему"""
    try:
        if platform.system() == "Windows":
            import win32api
            import win32con
            win32api.AddFontResource(font_path)
        elif platform.system() == "Darwin":
            # macOS
            import subprocess
            subprocess.run(['cp', font_path, '~/Library/Fonts/'], shell=True)
        else:
            # Linux
            import subprocess
            subprocess.run(['cp', font_path, '~/.fonts/'], shell=True)
        return True
    except Exception as e:
        print(f"Ошибка установки шрифта: {e}")
        return False

def load_custom_font(font_path, font_name="CustomFont"):
    """Загружает кастомный шрифт"""
    try:
        if not os.path.exists(font_path):
            return None
            
        # Пытаемся установить шрифт в систему
        if install_font(font_path):
            # Проверяем, что шрифт доступен
            available_fonts = tkFont.families()
            if font_name in available_fonts:
                return font_name
                
        # Альтернативный способ - создаем объект шрифта напрямую
        try:
            # Создаем временный root для тестирования шрифта
            temp_root = tk.Tk()
            temp_root.withdraw()  # Скрываем окно
            
            # Пытаемся создать шрифт
            test_font = tkFont.Font(family=font_name, size=12)
            actual_family = test_font.actual('family')
            
            temp_root.destroy()
            
            if actual_family == font_name:
                return font_name
        except:
            pass
            
        return None
    except Exception as e:
        print(f"Ошибка загрузки шрифта: {e}")
        return None

def get_best_fonts():
    """Возвращает лучшие доступные шрифты для каждой платформы"""
    try:
        # Получаем список доступных шрифтов
        temp_root = tk.Tk()
        temp_root.withdraw()
        available_fonts = tkFont.families()
        temp_root.destroy()
        
        if platform.system() == "Windows":
            # Приоритетные шрифты для Windows
            font_priority = [
                "Segoe UI",
                "Microsoft YaHei UI", 
                "Calibri",
                "Arial",
                "Tahoma",
                "Verdana"
            ]
            
            for font in font_priority:
                if font in available_fonts:
                    base_font = font
                    break
            else:
                base_font = "TkDefaultFont"
                
            return {
                'main': (base_font, 11),
                'title': (base_font, 28, "bold"),
                'subtitle': (base_font, 18, "bold"),
                'button': (base_font, 11, "bold"),
                'entry': (base_font, 10),
                'log': ("Consolas", 9) if "Consolas" in available_fonts else (base_font, 9)
            }
            
        elif platform.system() == "Darwin":
            # macOS шрифты
            font_priority = [
                "SF Pro Display",
                "Helvetica Neue",
                "Arial",
                "Lucida Grande"
            ]
            
            for font in font_priority:
                if font in available_fonts:
                    base_font = font
                    break
            else:
                base_font = "TkDefaultFont"
                
            return {
                'main': (base_font, 11),
                'title': (base_font, 28, "bold"),
                'subtitle': (base_font, 18, "bold"),
                'button': (base_font, 11, "bold"),
                'entry': (base_font, 10),
                'log': ("SF Mono", 9) if "SF Mono" in available_fonts else (base_font, 9)
            }
        else:
            # Linux шрифты
            font_priority = [
                "Ubuntu",
                "Liberation Sans",
                "DejaVu Sans",
                "Arial"
            ]
            
            for font in font_priority:
                if font in available_fonts:
                    base_font = font
                    break
            else:
                base_font = "TkDefaultFont"
                
            return {
                'main': (base_font, 11),
                'title': (base_font, 28, "bold"),
                'subtitle': (base_font, 18, "bold"),
                'button': (base_font, 11, "bold"),
                'entry': (base_font, 10),
                'log': ("Ubuntu Mono", 9) if "Ubuntu Mono" in available_fonts else (base_font, 9)
            }
            
    except Exception as e:
        print(f"Ошибка получения шрифтов: {e}")
        # Fallback
        return {
            'main': ("Arial", 11),
            'title': ("Arial", 28, "bold"),
            'subtitle': ("Arial", 18, "bold"),
            'button': ("Arial", 11, "bold"),
            'entry': ("Arial", 10),
            'log': ("Courier New", 9)
        }

def get_fonts_with_minecraft(stealer_dir):
    """Возвращает шрифты с попыткой загрузки Minecraft шрифта"""
    try:
        # Пытаемся загрузить новый Minecraft Title Cyrillic шрифт
        minecraft_paths = [
            os.path.join(stealer_dir, "ofont.ru_Minecraft Title Cyrillic.ttf"),
            os.path.join(stealer_dir, "Minecraft.ttf")
        ]
        
        minecraft_font_name = None
        minecraft_path = None
        
        for path in minecraft_paths:
            if os.path.exists(path):
                print(f"Найден Minecraft шрифт: {path}")
                minecraft_path = path
                
                # Определяем имя шрифта
                if "Title Cyrillic" in path:
                    minecraft_font_name = "Minecraft Title Cyrillic"
                else:
                    minecraft_font_name = "Minecraft"
                break
        
        if minecraft_path and minecraft_font_name:
            # Пытаемся загрузить шрифт
            minecraft_font = load_custom_font(minecraft_path, minecraft_font_name)
            if minecraft_font:
                print(f"{minecraft_font_name} шрифт успешно загружен!")
                return {
                    'main': (minecraft_font_name, 11),
                    'title': (minecraft_font_name, 28, "bold"),
                    'subtitle': (minecraft_font_name, 18, "bold"),
                    'button': (minecraft_font_name, 11, "bold"),
                    'entry': (minecraft_font_name, 10),
                    'log': (minecraft_font_name, 9)
                }
            else:
                print("Не удалось загрузить Minecraft шрифт, используем системные")
        else:
            print("Minecraft шрифт не найден")
            
        # Fallback на системные шрифты
        return get_best_fonts()
        
    except Exception as e:
        print(f"Ошибка загрузки шрифтов: {e}")
        return get_best_fonts()

if __name__ == "__main__":
    # Тестирование
    fonts = get_fonts_with_minecraft(".")
    print("Загруженные шрифты:")
    for key, value in fonts.items():
        print(f"  {key}: {value}")
