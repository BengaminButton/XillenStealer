import sqlite3
import shutil
import base64
import json
import os

shutil.copy2(r'C:\Users\user\AppData\Local\Google\Chrome\User Data\Default\Login Data', r'C:\Users\user\AppData\Local\Temp\test.db')

conn = sqlite3.connect(r'C:\Users\user\AppData\Local\Temp\test.db')
cursor = conn.cursor()
cursor.execute('SELECT password_value FROM logins LIMIT 1')
row = cursor.fetchone()
pw = row[0]

print(f'Password bytes (first 50): {pw[:50]}')
print(f'Total length: {len(pw)}')
print(f'Starts with v10: {pw.startswith(b"v10")}')
print(f'Starts with v11: {pw.startswith(b"v11")}')
print(f'Starts with v20: {pw.startswith(b"v20")}')
print(f'First 3 bytes: {pw[:3]}')
print(f'Full password (hex): {pw.hex()}')

# Get master key
local_state_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')
with open(local_state_path, 'r', encoding='utf-8') as f:
    local_state = json.load(f)

encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
encrypted_key = encrypted_key[5:]

import win32crypt
master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
print(f'Master key length: {len(master_key)}')

# Try decryption
from Crypto.Cipher import AES

if pw.startswith(b'v10') or pw.startswith(b'v11') or pw.startswith(b'v20'):
    version = 'v10' if pw.startswith(b'v10') else ('v11' if pw.startswith(b'v11') else 'v20')
    print(f'Using {version} decryption')
    nonce = pw[3:15]
    ciphertext_data = pw[15:-16]
    tag = pw[-16:]
    
    print(f'Nonce length: {len(nonce)}')
    print(f'Ciphertext length: {len(ciphertext_data)}')
    print(f'Tag length: {len(tag)}')
    
    try:
        cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext_data, tag)
        print(f'Decrypted via AES-GCM: {plaintext.decode("utf-8")}')
    except Exception as e:
        print(f'AES-GCM decryption failed: {e}')
        print('Trying DPAPI decryption...')
        try:
            import win32crypt
            decrypted = win32crypt.CryptUnprotectData(pw, None, None, None, 0)
            print(f'Decrypted via DPAPI: {decrypted[1].decode("utf-8")}')
        except Exception as e2:
            print(f'DPAPI decryption failed: {e2}')

conn.close()
