import os
import sys
import shutil
import subprocess
import winreg
import psutil
import tempfile
import time
import ctypes
import win32con
import win32api
import win32service
import win32serviceutil
import json
import sqlite3
import hashlib
import threading
import requests
import zipfile
import base64
from pathlib import Path
import win32file
import win32security
import win32net
import win32netcon

class XillenAntidote:
    def __init__(self):
        self.stealer_signatures = [
            "XillenStealer", "steler.py", "builder.py", "builds",
            "WindowsSystemMaintenance", "WindowsUpdateService",
            "advanced-stealer", "browser_cookie3", "pyTelegramBotAPI",
            "electron_builder", "primer", "stealer.py", "XillenStealerAntiDot.py",
            "telebot", "PIL", "psutil", "win32api", "win32con", "win32process",
            "win32com.client", "configparser", "xml.etree.ElementTree", "winreg",
            "struct", "hashlib", "random", "string", "cryptography.fernet",
            "pickle", "gzip", "io", "pynput", "cv2", "sounddevice", "scipy",
            "dns.resolver", "icmplib", "ctypes.wintypes", "fcntl", "array",
            "mmap", "socket", "select", "shutil", "pathlib", "requests",
            "zipfile", "base64", "threading", "subprocess", "tempfile",
            "datetime", "glob", "getpass", "stat", "traceback", "html",
            "time", "win32api", "win32con", "win32process", "win32com.client"
        ]
        
        self.stealer_processes = [
            "python.exe", "pythonw.exe", "steler.exe", 
            "WindowsUpdate.exe", "svchost_stealer.exe", "XillenStealer.exe",
            "builder.exe", "electron.exe", "node.exe", "npm.exe"
        ]
        
        self.temp_files_patterns = [
            "debug.log", "advanced_stealer_crash.log", "report.html",
            "report.txt", "screen.jpg", "stealer_", "xillen_", "aura_",
            "cookies_", "firefox_cookies_", "stealer_data", "browser_data",
            "crypto_wallets", "system_info", "network_analysis", "clipboard_",
            "file_changes", "password_managers", "social_tokens", "linpeas_",
            "game_launchers", "enhanced_cookies", "fingerprint", "webrtc_",
            "docker_", "kubernetes_", "iot_", "tpm_", "uefi_", "gpu_",
            "ebpf_", "dma_", "wifi_", "cloud_", "payment_", "mobile_",
            "emulator_", "totp_", "biometric_", "memory_", "container_",
            "persistence_", "injection_", "anti_debug", "anti_vm", "screenshot",
            "audio_", "keylogger", "webcam_", "documents_", "desktop_",
            "downloads_", "config_", "ftp_", "ssh_", "database_", "backup_",
            "software_", "network_", "process_", "cloud_metadata", "aws_",
            "kubeconfig", "kubernetes_secret", "service_mesh", "credit_card"
        ]
        
        self.stealer_file_extensions = [
            '.py', '.exe', '.pyc', '.pyo', '.pyd', '.so', '.dll', '.log',
            '.html', '.txt', '.json', '.xml', '.ini', '.cfg', '.conf',
            '.db', '.sqlite', '.sqlite3', '.dat', '.cache', '.tmp'
        ]
        
        self.stealer_hashes = [
            # Добавим известные хеши файлов стиллера
            "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",  # Пример хеша
        ]
        
        self.network_indicators = [
            "api.telegram.org", "t.me", "github.com/BengaminButton",
            "XillenKillers", "XillenAdapter", "BengaminButton"
        ]

    def is_admin(self):
        """Проверка прав администратора"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_as_admin(self):
        """Перезапуск с правами администратора"""
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)

    def kill_stealer_processes(self):
        """Убийство процессов стиллера"""
        print("[+] Завершение процессов стиллера...")
        killed = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'exe']):
            try:
                proc_name = proc.info['name'].lower()
                cmdline = ' '.join(proc.info['cmdline'] or []).lower()
                exe_path = proc.info['exe'] or ""
                
                # Проверяем по имени процесса, командной строке и пути
                if (any(sig.lower() in proc_name for sig in self.stealer_processes) or 
                    any(sig.lower() in cmdline for sig in self.stealer_signatures) or
                    any(sig.lower() in exe_path.lower() for sig in self.stealer_signatures)):
                    
                    print(f"    Обнаружен процесс: {proc.info['name']} (PID: {proc.info['pid']})")
                    print(f"    Путь: {exe_path}")
                    print(f"    Командная строка: {cmdline[:100]}...")
                    
                    # Сначала пытаемся завершить мягко
                    try:
                        psutil.Process(proc.info['pid']).terminate()
                        time.sleep(2)
                    except:
                        pass
                    
                    # Если процесс еще жив, принудительно убиваем
                    if psutil.pid_exists(proc.info['pid']):
                        try:
                            psutil.Process(proc.info['pid']).kill()
                            time.sleep(1)
                        except:
                            # Последняя попытка через taskkill
                            try:
                                subprocess.run(['taskkill', '/f', '/pid', str(proc.info['pid'])], 
                                             capture_output=True, timeout=5)
                            except:
                                pass
                    
                    killed += 1
                    print(f"    ✓ Процесс завершен")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        print(f"[+] Завершено процессов: {killed}")
    
    def scan_memory_for_stealer(self):
        """Сканирование памяти на наличие стиллера"""
        print("[+] Сканирование памяти...")
        found = 0
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(sig.lower() in proc_name for sig in self.stealer_processes):
                        # Проверяем память процесса на наличие сигнатур
                        memory_info = proc.info['memory_info']
                        if memory_info.rss > 50 * 1024 * 1024:  # Больше 50MB
                            print(f"    Подозрительный процесс: {proc.info['name']} - {memory_info.rss // 1024 // 1024}MB")
                            found += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"    ⚠ Ошибка сканирования памяти: {e}")
        
        print(f"[+] Найдено подозрительных процессов в памяти: {found}")
    
    def check_file_hashes(self, file_path):
        """Проверка хеша файла"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                return file_hash in self.stealer_hashes
        except:
            return False
    
    def deep_scan_files(self):
        """Глубокое сканирование файлов"""
        print("[+] Глубокое сканирование файлов...")
        scanned = 0
        infected = 0
        
        search_dirs = [
            os.environ['USERPROFILE'],
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            os.path.join(os.environ['USERPROFILE'], 'Documents'),
            os.path.join(os.environ['USERPROFILE'], 'AppData'),
            os.path.join(os.environ['PROGRAMDATA']),
            os.path.dirname(os.path.abspath(__file__))
        ]
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(search_dir):
                    # Пропускаем системные папки
                    if any(skip in root for skip in ['Windows', 'Program Files', 'ProgramData']):
                        continue
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        scanned += 1
                        
                        # Проверяем по расширению
                        if any(file.endswith(ext) for ext in self.stealer_file_extensions):
                            # Проверяем по имени
                            if any(sig.lower() in file.lower() for sig in self.stealer_signatures):
                                print(f"    Зараженный файл: {file_path}")
                                infected += 1
                                
                                # Проверяем хеш
                                if self.check_file_hashes(file_path):
                                    print(f"    ✓ Подтверждено по хешу: {file_path}")
                                
                                # Удаляем файл
                                try:
                                    os.remove(file_path)
                                    print(f"    ✓ Файл удален")
                                except Exception as e:
                                    print(f"    ⚠ Не удалось удалить: {e}")
                        
                        # Проверяем содержимое файла
                        try:
                            if file.endswith(('.py', '.txt', '.log', '.html', '.json')):
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read(1024)  # Первые 1024 символа
                                    if any(sig.lower() in content.lower() for sig in self.stealer_signatures):
                                        print(f"    Зараженный контент: {file_path}")
                                        infected += 1
                                        try:
                                            os.remove(file_path)
                                            print(f"    ✓ Файл удален")
                                        except:
                                            pass
                        except:
                            pass
                            
            except Exception as e:
                print(f"    ⚠ Ошибка сканирования {search_dir}: {e}")
        
        print(f"[+] Просканировано файлов: {scanned}")
        print(f"[+] Найдено зараженных: {infected}")
    
    def clean_browser_extensions(self):
        """Очистка расширений браузеров"""
        print("[+] Очистка расширений браузеров...")
        
        browser_extensions_paths = [
            # Chrome
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Extensions'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Profile 1', 'Extensions'),
            # Firefox
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'),
            # Edge
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Extensions'),
        ]
        
        cleaned = 0
        for ext_path in browser_extensions_paths:
            if not os.path.exists(ext_path):
                continue
                
            try:
                for root, dirs, files in os.walk(ext_path):
                    for file in files:
                        if any(sig.lower() in file.lower() for sig in self.stealer_signatures):
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                cleaned += 1
                                print(f"    Удалено расширение: {file}")
                            except:
                                pass
            except Exception as e:
                print(f"    ⚠ Ошибка очистки расширений: {e}")
        
        print(f"[+] Удалено расширений: {cleaned}")
    
    def clean_network_connections(self):
        """Очистка сетевых соединений"""
        print("[+] Очистка сетевых соединений...")
        
        try:
            # Получаем все сетевые соединения
            connections = psutil.net_connections()
            suspicious_connections = 0
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    remote_ip = conn.raddr.ip
                    remote_port = conn.raddr.port
                    
                    # Проверяем подозрительные порты
                    suspicious_ports = [4444, 5555, 6666, 7777, 8888, 9999, 1337, 31337]
                    if remote_port in suspicious_ports:
                        print(f"    Подозрительное соединение: {remote_ip}:{remote_port}")
                        suspicious_connections += 1
            
            print(f"[+] Найдено подозрительных соединений: {suspicious_connections}")
            
        except Exception as e:
            print(f"    ⚠ Ошибка проверки соединений: {e}")
    
    def clean_dns_cache_advanced(self):
        """Расширенная очистка DNS кэша"""
        print("[+] Расширенная очистка DNS кэша...")
        
        try:
            # Очищаем DNS кэш
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True, timeout=10)
            
            # Очищаем кэш ARP
            subprocess.run(['arp', '-d', '*'], capture_output=True, timeout=10)
            
            # Очищаем кэш NetBIOS
            subprocess.run(['nbtstat', '-R'], capture_output=True, timeout=10)
            
            print("    ✓ DNS, ARP и NetBIOS кэши очищены")
            
        except Exception as e:
            print(f"    ⚠ Ошибка очистки кэшей: {e}")
    
    def clean_windows_event_logs(self):
        """Очистка журналов событий Windows"""
        print("[+] Очистка журналов событий...")
        
        try:
            # Очищаем основные журналы
            logs_to_clear = ['Application', 'System', 'Security', 'Setup']
            
            for log_name in logs_to_clear:
                try:
                    subprocess.run(['wevtutil', 'cl', log_name], 
                                 capture_output=True, timeout=30)
                    print(f"    ✓ Журнал {log_name} очищен")
                except:
                    pass
                    
        except Exception as e:
            print(f"    ⚠ Ошибка очистки журналов: {e}")
    
    def clean_windows_prefetch(self):
        """Очистка Prefetch папки"""
        print("[+] Очистка Prefetch...")
        
        try:
            prefetch_path = os.path.join(os.environ['SYSTEMROOT'], 'Prefetch')
            if os.path.exists(prefetch_path):
                for file in os.listdir(prefetch_path):
                    if any(sig.lower() in file.lower() for sig in self.stealer_signatures):
                        try:
                            os.remove(os.path.join(prefetch_path, file))
                            print(f"    Удален: {file}")
                        except:
                            pass
        except Exception as e:
            print(f"    ⚠ Ошибка очистки Prefetch: {e}")
    
    def clean_windows_thumbnails(self):
        """Очистка миниатюр Windows"""
        print("[+] Очистка миниатюр...")
        
        try:
            thumbnails_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'Explorer')
            if os.path.exists(thumbnails_path):
                for file in os.listdir(thumbnails_path):
                    if file.startswith('thumbcache_'):
                        try:
                            os.remove(os.path.join(thumbnails_path, file))
                        except:
                            pass
        except Exception as e:
            print(f"    ⚠ Ошибка очистки миниатюр: {e}")
    
    def create_advanced_protection(self):
        """Создание расширенной защиты"""
        print("[+] Создание расширенной защиты...")
        
        try:
            # Создаем файлы-ловушки
            trap_files = [
                os.path.join(os.environ['USERPROFILE'], 'Desktop', 'stealer.py'),
                os.path.join(os.environ['USERPROFILE'], 'Downloads', 'builder.py'),
                os.path.join(os.environ['USERPROFILE'], 'Documents', 'XillenStealer.py'),
                os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', 'steler.exe')
            ]
            
            for trap_file in trap_files:
                try:
                    with open(trap_file, 'w') as f:
                        f.write('# XillenStealer Antidote Protection - Do not execute\n')
                        f.write('# This file is monitored by XillenStealer Antidote\n')
                        f.write('import sys\n')
                        f.write('sys.exit(0)\n')
                    
                    # Делаем файл скрытым
                    subprocess.run(['attrib', '+h', '+s', trap_file], capture_output=True)
                    print(f"    Создана ловушка: {trap_file}")
                except:
                    pass
            
            # Создаем мониторинг процессов
            self.create_process_monitor()
            
            print("    ✓ Расширенная защита установлена")
            
        except Exception as e:
            print(f"    ⚠ Ошибка создания защиты: {e}")
    
    def create_process_monitor(self):
        """Создание монитора процессов"""
        try:
            monitor_script = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'xillen_monitor.py')
            
            monitor_code = '''
import psutil
import time
import os
import subprocess

def monitor_processes():
    stealer_processes = [
        "python.exe", "pythonw.exe", "steler.exe", 
        "WindowsUpdate.exe", "svchost_stealer.exe", "XillenStealer.exe",
        "builder.exe", "electron.exe", "node.exe", "npm.exe"
    ]
    
    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() in stealer_processes:
                    print(f"ALERT: Stealer process detected: {proc.info['name']}")
                    # Можно добавить уведомление или автоматическое завершение
            time.sleep(10)
        except:
            pass

if __name__ == "__main__":
    monitor_processes()
'''
            
            with open(monitor_script, 'w') as f:
                f.write(monitor_code)
            
            # Скрываем файл
            subprocess.run(['attrib', '+h', '+s', monitor_script], capture_output=True)
            
        except Exception as e:
            print(f"    ⚠ Ошибка создания монитора: {e}")

    def remove_registry_entries(self):
        """Удаление записей реестра"""
        print("[+] Очистка реестра...")
        registry_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce")
        ]
        
        removed = 0
        for root, path in registry_paths:
            try:
                key = winreg.OpenKey(root, path, 0, winreg.KEY_ALL_ACCESS)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        
                        # Проверяем на наличие сигнатур стиллера
                        if any(sig.lower() in name.lower() or sig.lower() in value.lower() 
                               for sig in self.stealer_signatures):
                            print(f"    Удаление: {name} -> {value}")
                            winreg.DeleteValue(key, name)
                            removed += 1
                        i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(key)
            except WindowsError:
                continue
        
        print(f"[+] Удалено записей реестра: {removed}")

    def remove_scheduled_tasks(self):
        """Удаление задач планировщика"""
        print("[+] Удаление задач планировщика...")
        try:
            # Используем PowerShell для удаления задач
            powershell_cmds = [
                'Get-ScheduledTask | Where-Object {$_.TaskName -like "*WindowsSystemMaintenance*" -or $_.TaskName -like "*Xillen*" -or $_.TaskName -like "*Stealer*"} | Unregister-ScheduledTask -Confirm:$false',
                'Get-ScheduledTask | Where-Object {$_.Description -like "*Xillen*" -or $_.Description -like "*Stealer*"} | Unregister-ScheduledTask -Confirm:$false'
            ]
            
            for cmd in powershell_cmds:
                result = subprocess.run(
                    ['powershell', '-Command', cmd],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    print("    ✓ Задачи планировщика удалены")
                    
        except Exception as e:
            print(f"    ⚠ Ошибка удаления задач: {e}")

    def remove_windows_services(self):
        """Удаление служб Windows"""
        print("[+] Удаление служб...")
        service_names = ["WindowsUpdateService", "XillenService", "SystemMaintenance"]
        
        for service_name in service_names:
            try:
                # Останавливаем службу
                subprocess.run(['sc', 'stop', service_name], 
                             capture_output=True, timeout=10)
                time.sleep(2)
                
                # Удаляем службу
                subprocess.run(['sc', 'delete', service_name],
                             capture_output=True, timeout=10)
                print(f"    ✓ Служба {service_name} удалена")
                
            except Exception as e:
                # Служба может не существовать - это нормально
                pass

    def clean_temp_files(self):
        """Очистка временных файлов"""
        print("[+] Очистка временных файлов...")
        temp_dirs = [
            tempfile.gettempdir(),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCookies'),
        ]
        
        cleaned = 0
        for temp_dir in temp_dirs:
            if not os.path.exists(temp_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Проверяем по шаблонам имен
                        if any(pattern in file for pattern in self.temp_files_patterns):
                            try:
                                os.remove(file_path)
                                cleaned += 1
                                print(f"    Удален: {file}")
                            except:
                                pass
                                
                        # Также удаляем файлы .py и .exe в temp
                        elif file.endswith(('.py', '.exe', '.log')) and any(sig in file for sig in self.stealer_signatures):
                            try:
                                os.remove(file_path)
                                cleaned += 1
                                print(f"    Удален: {file}")
                            except:
                                pass
            except Exception:
                continue
        
        print(f"[+] Удалено временных файлов: {cleaned}")

    def remove_startup_entries(self):
        """Удаление из автозагрузки"""
        print("[+] Удаление из автозагрузки...")
        startup_paths = [
            os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
            os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        ]
        
        removed = 0
        for startup_path in startup_paths:
            if not os.path.exists(startup_path):
                continue
                
            for file in os.listdir(startup_path):
                file_path = os.path.join(startup_path, file)
                if any(sig in file for sig in self.stealer_signatures):
                    try:
                        os.remove(file_path)
                        removed += 1
                        print(f"    Удален: {file}")
                    except:
                        pass
        
        print(f"[+] Удалено из автозагрузки: {removed}")

    def clean_browser_data(self):
        """Очистка данных браузеров"""
        print("[+] Очистка данных браузеров...")
        browser_paths = [
            # Chrome
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data'),
            # Firefox
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Mozilla', 'Firefox'),
            # Edge
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data'),
        ]
        
        for browser_path in browser_paths:
            if not os.path.exists(browser_path):
                continue
                
            # Ищем файлы, связанные со стиллером
            for root, dirs, files in os.walk(browser_path):
                for file in files:
                    if any(sig in file for sig in ['stealer', 'xillen', 'steler']):
                        try:
                            os.remove(os.path.join(root, file))
                            print(f"    Удален: {file}")
                        except:
                            pass

    def reset_winsock(self):
        """Сброс сетевых настроек"""
        print("[+] Сброс сетевых настроек...")
        try:
            subprocess.run(['netsh', 'winsock', 'reset'], 
                         capture_output=True, timeout=30)
            print("    ✓ Winsock сброшен")
        except:
            print("    ⚠ Ошибка сброса Winsock")

    def clear_dns_cache(self):
        """Очистка DNS кэша"""
        print("[+] Очистка DNS кэша...")
        try:
            subprocess.run(['ipconfig', '/flushdns'], 
                         capture_output=True, timeout=10)
            print("    ✓ DNS кэш очищен")
        except:
            print("    ⚠ Ошибка очистки DNS кэша")

    def remove_stealer_files(self):
        """Удаление файлов стиллера"""
        print("[+] Поиск и удаление файлов стиллера...")
        
        # Папки для поиска
        search_dirs = [
            os.environ['USERPROFILE'],
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            os.path.join(os.environ['USERPROFILE'], 'Documents'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp'),
            os.path.dirname(os.path.abspath(__file__))  # Текущая директория
        ]
        
        removed = 0
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(search_dir):
                    # Пропускаем системные папки
                    if any(skip in root for skip in ['Windows', 'Program Files', 'ProgramData']):
                        continue
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Проверяем файлы по имени и расширению
                        if (any(sig in file for sig in self.stealer_signatures) or
                            file in ['steler.py', 'builder.py', 'builderold.py', 'buildernew.py']):
                            
                            try:
                                os.remove(file_path)
                                removed += 1
                                print(f"    Удален: {file_path}")
                            except Exception as e:
                                print(f"    ⚠ Не удалось удалить: {file_path} - {e}")
                                
                    # Удаляем папки builds
                    for dir in dirs:
                        if 'builds' in dir.lower():
                            dir_path = os.path.join(root, dir)
                            try:
                                shutil.rmtree(dir_path)
                                removed += 1
                                print(f"    Удалена папка: {dir_path}")
                            except:
                                pass
                                
            except Exception as e:
                print(f"    ⚠ Ошибка поиска в {search_dir}: {e}")
        
        print(f"[+] Удалено файлов и папок: {removed}")

    def system_optimization(self):
        """Оптимизация системы после очистки"""
        print("[+] Оптимизация системы...")
        
        try:
            # Очистка кэша ICON
            subprocess.run(['ie4uinit.exe', '-show'], capture_output=True)
            
            # Перезапуск проводника
            subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], capture_output=True)
            time.sleep(2)
            subprocess.Popen('explorer.exe')
            
            print("    ✓ Система оптимизирована")
            
        except Exception as e:
            print(f"    ⚠ Ошибка оптимизации: {e}")

    def create_protection(self):
        """Создание защиты от повторного заражения"""
        print("[+] Создание защиты...")
        
        try:
            # Создаем пустой файл-маркер в ключевых местах
            protection_files = [
                os.path.join(os.environ['SYSTEMROOT'], 'System32', 'drivers', 'etc', 'hosts.xillen_protect'),
                os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'xillen_protect'),
                os.path.join(os.environ['PROGRAMDATA'], 'xillen_protect')
            ]
            
            for file_path in protection_files:
                try:
                    with open(file_path, 'w') as f:
                        f.write('XillenStealer Protection - Do not remove\n')
                    # Скрываем файл
                    subprocess.run(['attrib', '+h', '+s', file_path], capture_output=True)
                except:
                    pass
            
            print("    ✓ Защита установлена")
            
        except Exception as e:
            print(f"    ⚠ Ошибка установки защиты: {e}")

    def run_full_clean(self):
        """Полная очистка системы"""
        print("🔍 XillenStealer Antidote v2.0 - Advanced Edition")
        print("=" * 60)
        print("🛡️  Полноценный антивирус для XillenStealer")
        print("=" * 60)
        
        if not self.is_admin():
            print("⚠ Требуются права администратора!")
            self.run_as_admin()
            return
        
        try:
            print("\n🔍 ЭТАП 1: Анализ и обнаружение")
            print("-" * 40)
            self.scan_memory_for_stealer()
            self.clean_network_connections()
            
            print("\n💀 ЭТАП 2: Уничтожение процессов")
            print("-" * 40)
            self.kill_stealer_processes()
            time.sleep(3)
            
            print("\n🗑️  ЭТАП 3: Глубокая очистка файлов")
            print("-" * 40)
            self.deep_scan_files()
            self.remove_stealer_files()
            self.clean_temp_files()
            
            print("\n🔧 ЭТАП 4: Очистка системы")
            print("-" * 40)
            self.remove_startup_entries()
            self.remove_registry_entries()
            self.remove_scheduled_tasks()
            self.remove_windows_services()
            self.clean_browser_data()
            self.clean_browser_extensions()
            
            print("\n🌐 ЭТАП 5: Очистка сети")
            print("-" * 40)
            self.clean_dns_cache_advanced()
            self.reset_winsock()
            
            print("\n📋 ЭТАП 6: Очистка Windows")
            print("-" * 40)
            self.clean_windows_event_logs()
            self.clean_windows_prefetch()
            self.clean_windows_thumbnails()
            
            print("\n🛡️  ЭТАП 7: Установка защиты")
            print("-" * 40)
            self.create_advanced_protection()
            self.system_optimization()
            
            print("\n" + "=" * 60)
            print("✅ ПОЛНАЯ ОЧИСТКА ЗАВЕРШЕНА УСПЕШНО!")
            print("=" * 60)
            print("📊 Статистика очистки:")
            print("   • Процессы стиллера: УНИЧТОЖЕНЫ")
            print("   • Файлы стиллера: УДАЛЕНЫ")
            print("   • Реестр: ОЧИЩЕН")
            print("   • Сеть: ОЧИЩЕНА")
            print("   • Браузеры: ОЧИЩЕНЫ")
            print("   • Защита: УСТАНОВЛЕНА")
            print("\n💡 РЕКОМЕНДАЦИИ:")
            print("   • Перезагрузите компьютер")
            print("   • Проверьте антивирусом")
            print("   • Смените пароли")
            print("   • Обновите браузеры")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
            print("🆘 Попробуйте запустить от имени администратора")
    
    def run_quick_scan(self):
        """Быстрое сканирование"""
        print("🔍 XillenStealer Antidote v2.0 - Quick Scan")
        print("=" * 50)
        
        try:
            print("[+] Быстрое сканирование...")
            self.scan_memory_for_stealer()
            self.kill_stealer_processes()
            self.clean_temp_files()
            self.remove_stealer_files()
            
            print("\n✅ Быстрое сканирование завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка быстрого сканирования: {e}")
    
    def run_custom_scan(self, options):
        """Пользовательское сканирование"""
        print("🔍 XillenStealer Antidote v2.0 - Custom Scan")
        print("=" * 50)
        
        try:
            if 'processes' in options:
                print("[+] Сканирование процессов...")
                self.kill_stealer_processes()
            
            if 'files' in options:
                print("[+] Сканирование файлов...")
                self.deep_scan_files()
            
            if 'registry' in options:
                print("[+] Сканирование реестра...")
                self.remove_registry_entries()
            
            if 'network' in options:
                print("[+] Сканирование сети...")
                self.clean_network_connections()
            
            if 'browsers' in options:
                print("[+] Сканирование браузеров...")
                self.clean_browser_data()
                self.clean_browser_extensions()
            
            print("\n✅ Пользовательское сканирование завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка пользовательского сканирования: {e}")

def show_menu():
    """Показать главное меню"""
    print("\n" + "=" * 60)
    print("XILLENSTEALER ANTIDOTE v2.0 - ADVANCED EDITION")
    print("=" * 60)
    print("Выберите режим работы:")
    print("1. Полная очистка системы (РЕКОМЕНДУЕТСЯ)")
    print("2. Быстрое сканирование")
    print("3. Пользовательское сканирование")
    print("4. Только анализ (без удаления)")
    print("5. Только установка защиты")
    print("6. Выход")
    print("=" * 60)

def main():
    antidote = XillenAntidote()
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == '-full':
            antidote.run_full_clean()
        elif sys.argv[1] == '-quick':
            antidote.run_quick_scan()
        elif sys.argv[1] == '-silent':
            antidote.run_full_clean()
            return
        elif sys.argv[1] == '-custom':
            options = ['processes', 'files', 'registry', 'network', 'browsers']
            antidote.run_custom_scan(options)
        else:
            print("Использование:")
            print("  python XillenStealerAntiDot.py -full    # Полная очистка")
            print("  python XillenStealerAntiDot.py -quick  # Быстрое сканирование")
            print("  python XillenStealerAntiDot.py -silent  # Тихий режим")
            print("  python XillenStealerAntiDot.py -custom  # Пользовательское сканирование")
            return
    else:
        # Интерактивное меню
        while True:
            show_menu()
            try:
                choice = input("Введите номер (1-6): ").strip()
                
                if choice == '1':
                    antidote.run_full_clean()
                elif choice == '2':
                    antidote.run_quick_scan()
                elif choice == '3':
                    print("\nВыберите компоненты для сканирования:")
                    print("1. Процессы")
                    print("2. Файлы")
                    print("3. Реестр")
                    print("4. Сеть")
                    print("5. Браузеры")
                    print("6. Все компоненты")
                    
                    custom_choice = input("Введите номера через пробел (например: 1 2 3): ").strip()
                    options = []
                    
                    if '1' in custom_choice:
                        options.append('processes')
                    if '2' in custom_choice:
                        options.append('files')
                    if '3' in custom_choice:
                        options.append('registry')
                    if '4' in custom_choice:
                        options.append('network')
                    if '5' in custom_choice:
                        options.append('browsers')
                    if '6' in custom_choice:
                        options = ['processes', 'files', 'registry', 'network', 'browsers']
                    
                    if options:
                        antidote.run_custom_scan(options)
                    else:
                        print("❌ Не выбрано ни одного компонента!")
                        
                elif choice == '4':
                    print("\n🔍 Анализ системы...")
                    antidote.scan_memory_for_stealer()
                    antidote.clean_network_connections()
                    print("\n✅ Анализ завершен!")
                    
                elif choice == '5':
                    print("\n🛡️  Установка защиты...")
                    antidote.create_advanced_protection()
                    print("\n✅ Защита установлена!")
                    
                elif choice == '6':
                    print("\n👋 До свидания!")
                    break
                else:
                    print("❌ Неверный выбор! Попробуйте снова.")
                
                if choice in ['1', '2', '3', '4', '5']:
                    input("\nНажмите Enter для продолжения...")
                    
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем.")
                break
            except Exception as e:
                print(f"\nОшибка: {e}")
                input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
