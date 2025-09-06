import os
import subprocess
import winreg
import psutil
import time
from colorama import init, Fore, Style

init(autoreset=True)

KEYWORDS = ["xillen", "steler", "stealer", "builder", "steal", "explorer", "minecraft", "audio_video"]

BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════════════╗
║        {Fore.YELLOW}АНТИДОТ XillenStealer | github.com/BengaminButton/XillenStealer{Fore.CYAN}        ║
║   {Fore.GREEN}Разработано github.com/BengaminButton и командой Xillen Killers (t.me/XillenAdapter){Fore.CYAN}   ║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

def remove_schtasks():
    found = []
    try:
        result = subprocess.run(['schtasks'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            for key in KEYWORDS:
                if key in line.lower():
                    task_name = line.split()[0]
                    subprocess.run(['schtasks', '/Delete', '/TN', task_name, '/F'], check=False)
                    print(f"{Fore.GREEN}[+] Удалена задача планировщика: {task_name}")
                    found.append(task_name)
    except Exception as e:
        print(f"{Fore.RED}[-] Ошибка при удалении задач: {e}")
    return found

def remove_from_startup_registry():
    deleted = []
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
        i = 0
        to_delete = []
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                for k in KEYWORDS:
                    if k in name.lower() or k in str(value).lower():
                        to_delete.append(name)
                i += 1
            except OSError:
                break
        for name in to_delete:
            winreg.DeleteValue(key, name)
            print(f"{Fore.GREEN}[+] Удалено из автозагрузки (реестр): {name}")
            deleted.append(name)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"{Fore.RED}[-] Ошибка при чистке автозагрузки (реестр): {e}")
    return deleted

def remove_from_startup_folder():
    deleted = []
    startup_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    for file in os.listdir(startup_path):
        for k in KEYWORDS:
            if k in file.lower():
                try:
                    os.remove(os.path.join(startup_path, file))
                    print(f"{Fore.GREEN}[+] Удалено из папки автозагрузки: {file}")
                    deleted.append(file)
                except Exception as e:
                    print(f"{Fore.RED}[-] Не удалось удалить {file}: {e}")
    return deleted

def kill_processes():
    killed = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            proc_name = (proc.info['name'] or '') + ' ' + ' '.join(proc.info.get('cmdline') or [])
            for k in KEYWORDS:
                if k in proc_name.lower():
                    proc.kill()
                    print(f"{Fore.GREEN}[+] Процесс завершён: {proc.info['name']}")
                    killed.append(proc.info['name'])
        except Exception:
            pass
    return killed

def check_leftovers():
    leftovers = {"tasks": [], "startup_reg": [], "startup_folder": [], "processes": []}
    # Check schtasks
    try:
        result = subprocess.run(['schtasks'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            for key in KEYWORDS:
                if key in line.lower():
                    leftovers["tasks"].append(line.split()[0])
    except Exception:
        pass
    # Check registry
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_READ)
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                for k in KEYWORDS:
                    if k in name.lower() or k in str(value).lower():
                        leftovers["startup_reg"].append(name)
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
    except Exception:
        pass
    # Check startup folder
    startup_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    for file in os.listdir(startup_path):
        for k in KEYWORDS:
            if k in file.lower():
                leftovers["startup_folder"].append(file)
    # Check processes
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            proc_name = (proc.info['name'] or '') + ' ' + ' '.join(proc.info.get('cmdline') or [])
            for k in KEYWORDS:
                if k in proc_name.lower():
                    leftovers["processes"].append(proc.info['name'])
        except Exception:
            pass
    return leftovers

def auto_clean_leftovers():
    """Пытается удалить все остатки до полной чистоты (до 5 попыток)."""
    for attempt in range(5):
        leftovers = check_leftovers()
        if not any(leftovers.values()):
            return True
        if leftovers["tasks"]:
            remove_schtasks()
        if leftovers["startup_reg"]:
            remove_from_startup_registry()
        if leftovers["startup_folder"]:
            remove_from_startup_folder()
        if leftovers["processes"]:
            kill_processes()
        time.sleep(1)
    return False

def main():
    print(BANNER)
    remove_schtasks()
    remove_from_startup_registry()
    remove_from_startup_folder()
    kill_processes()
    print(f"{Fore.CYAN}[*] Антидот выполнен. Проверяю остатки...")
    if auto_clean_leftovers():
        print(f"{Fore.GREEN}[+] Всё чисто! Ничего подозрительного не найдено.")
    else:
        leftovers = check_leftovers()
        print(f"{Fore.RED}[!] Обнаружены остатки:")
        if leftovers["tasks"]:
            print(f"  {Fore.YELLOW}Задачи в планировщике:", leftovers["tasks"])
        if leftovers["startup_reg"]:
            print(f"  {Fore.YELLOW}Автозагрузка (реестр):", leftovers["startup_reg"])
        if leftovers["startup_folder"]:
            print(f"  {Fore.YELLOW}Автозагрузка (папка):", leftovers["startup_folder"])
        if leftovers["processes"]:
            print(f"  {Fore.YELLOW}Процессы:", leftovers["processes"])
        print(f"{Fore.CYAN}[*] Рекомендуется удалить вручную или перезагрузить ПК.")

if __name__ == "__main__":
    main()