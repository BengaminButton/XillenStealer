import pyotp
import qrcode
import io
import base64
import secrets
import hashlib
import time
from datetime import datetime, timedelta

class TwoFactorAuth:
    def __init__(self):
        self.secret_key = None
        self.backup_codes = []
        self.is_enabled = False
        self.last_used_backup = None
        
    def generate_secret(self):
        """Generate a new secret key for 2FA"""
        self.secret_key = pyotp.random_base32()
        return self.secret_key
    
    def generate_qr_code(self, username, issuer="XillenStealer V5"):
        """Generate QR code for Google Authenticator"""
        if not self.secret_key:
            self.generate_secret()
        
        totp_uri = pyotp.totp.TOTP(self.secret_key).provisioning_uri(
            name=username,
            issuer_name=issuer
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        # Convert to base64 image
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'secret': self.secret_key,
            'qr_code': f"data:image/png;base64,{img_str}",
            'manual_key': self.secret_key
        }
    
    def generate_backup_codes(self, count=10):
        """Generate backup codes for 2FA"""
        self.backup_codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
            self.backup_codes.append(code)
        return self.backup_codes
    
    def verify_totp(self, token):
        """Verify TOTP token"""
        if not self.secret_key:
            return False
        
        totp = pyotp.TOTP(self.secret_key)
        
        # Allow some time drift (30 seconds window)
        return totp.verify(token, valid_window=1)
    
    def verify_backup_code(self, code):
        """Verify backup code"""
        if code in self.backup_codes:
            # Remove used backup code
            self.backup_codes.remove(code)
            self.last_used_backup = datetime.now()
            return True
        return False
    
    def enable_2fa(self, secret_key, backup_codes):
        """Enable 2FA with provided secret and backup codes"""
        self.secret_key = secret_key
        self.backup_codes = backup_codes
        self.is_enabled = True
        return True
    
    def disable_2fa(self):
        """Disable 2FA"""
        self.secret_key = None
        self.backup_codes = []
        self.is_enabled = False
        return True
    
    def get_remaining_backup_codes(self):
        """Get count of remaining backup codes"""
        return len(self.backup_codes)
    
    def is_2fa_enabled(self):
        """Check if 2FA is enabled"""
        return self.is_enabled and self.secret_key is not None

class TwoFactorManager:
    def __init__(self, db_path="xillen_v5.db"):
        self.db_path = db_path
        self.tfa = TwoFactorAuth()
        self.init_database()
    
    def init_database(self):
        """Initialize database for 2FA data"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create 2FA settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS two_factor_auth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                secret_key TEXT,
                backup_codes TEXT,
                is_enabled BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def setup_2fa(self, user_id):
        """Setup 2FA for user"""
        try:
            # Generate secret and QR code
            qr_data = self.tfa.generate_qr_code(user_id)
            
            # Generate backup codes
            backup_codes = self.tfa.generate_backup_codes()
            
            return {
                'status': 'success',
                'secret': qr_data['secret'],
                'qr_code': qr_data['qr_code'],
                'manual_key': qr_data['manual_key'],
                'backup_codes': backup_codes
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def verify_2fa_setup(self, user_id, token):
        """Verify 2FA setup with token"""
        try:
            if self.tfa.verify_totp(token):
                # Save to database
                self.save_2fa_data(user_id)
                return {
                    'status': 'success',
                    'message': '2FA setup verified successfully'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Invalid token'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def authenticate(self, user_id, token):
        """Authenticate user with 2FA token"""
        try:
            # Load user's 2FA data
            user_data = self.load_2fa_data(user_id)
            if not user_data:
                return {
                    'status': 'error',
                    'message': '2FA not enabled for user'
                }
            
            # Set up TFA with user's secret
            self.tfa.secret_key = user_data['secret_key']
            self.tfa.backup_codes = user_data['backup_codes']
            
            # Verify token
            if self.tfa.verify_totp(token):
                self.update_last_used(user_id)
                return {
                    'status': 'success',
                    'message': 'Authentication successful'
                }
            elif self.tfa.verify_backup_code(token):
                self.update_last_used(user_id)
                self.save_2fa_data(user_id)  # Save updated backup codes
                return {
                    'status': 'success',
                    'message': 'Authentication successful (backup code used)'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Invalid token'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def save_2fa_data(self, user_id):
        """Save 2FA data to database"""
        import sqlite3
        import json
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO two_factor_auth 
            (user_id, secret_key, backup_codes, is_enabled, last_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            self.tfa.secret_key,
            json.dumps(self.tfa.backup_codes),
            self.tfa.is_enabled,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def load_2fa_data(self, user_id):
        """Load 2FA data from database"""
        import sqlite3
        import json
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT secret_key, backup_codes, is_enabled, last_used
            FROM two_factor_auth
            WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'secret_key': result[0],
                'backup_codes': json.loads(result[1]) if result[1] else [],
                'is_enabled': bool(result[2]),
                'last_used': result[3]
            }
        return None
    
    def update_last_used(self, user_id):
        """Update last used timestamp"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE two_factor_auth
            SET last_used = ?
            WHERE user_id = ?
        ''', (datetime.now(), user_id))
        
        conn.commit()
        conn.close()
    
    def disable_2fa(self, user_id):
        """Disable 2FA for user"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM two_factor_auth
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {
            'status': 'success',
            'message': '2FA disabled successfully'
        }
    
    def get_2fa_status(self, user_id):
        """Get 2FA status for user"""
        user_data = self.load_2fa_data(user_id)
        if user_data:
            return {
                'status': 'success',
                'is_enabled': user_data['is_enabled'],
                'remaining_backup_codes': len(user_data['backup_codes']),
                'last_used': user_data['last_used']
            }
        else:
            return {
                'status': 'success',
                'is_enabled': False,
                'remaining_backup_codes': 0,
                'last_used': None
            }
    
    def regenerate_backup_codes(self, user_id):
        """Regenerate backup codes for user"""
        try:
            user_data = self.load_2fa_data(user_id)
            if not user_data:
                return {
                    'status': 'error',
                    'message': '2FA not enabled for user'
                }
            
            # Generate new backup codes
            self.tfa.secret_key = user_data['secret_key']
            new_backup_codes = self.tfa.generate_backup_codes()
            
            # Save to database
            import sqlite3
            import json
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE two_factor_auth
                SET backup_codes = ?
                WHERE user_id = ?
            ''', (json.dumps(new_backup_codes), user_id))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'backup_codes': new_backup_codes
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

# Global instance
tfa_manager = TwoFactorManager()

def setup_2fa(user_id):
    """Setup 2FA for user"""
    return tfa_manager.setup_2fa(user_id)

def verify_2fa_setup(user_id, token):
    """Verify 2FA setup"""
    return tfa_manager.verify_2fa_setup(user_id, token)

def authenticate_2fa(user_id, token):
    """Authenticate with 2FA"""
    return tfa_manager.authenticate(user_id, token)

def disable_2fa(user_id):
    """Disable 2FA"""
    return tfa_manager.disable_2fa(user_id)

def get_2fa_status(user_id):
    """Get 2FA status"""
    return tfa_manager.get_2fa_status(user_id)

def regenerate_backup_codes(user_id):
    """Regenerate backup codes"""
    return tfa_manager.regenerate_backup_codes(user_id)
