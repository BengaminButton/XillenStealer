import hashlib
import hmac
import time
import json
import base64
import os
import requests
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3

class LicensingSystem:
    def __init__(self):
        self.license_active = False
        self.license_type = "FREE"  # FREE, BASIC, PRO, ENTERPRISE
        self.license_expires = None
        self.license_features = []
        self.hardware_id = self._get_hardware_id()
        self.server_url = "https://xillenstealer-premium.com/api"  # Premium server
        
    def _get_hardware_id(self):
        """Generate unique hardware ID"""
        try:
            import wmi
            c = wmi.WMI()
            
            # Get CPU ID
            cpu_id = ""
            for cpu in c.Win32_Processor():
                cpu_id += cpu.ProcessorId
                
            # Get Motherboard ID
            mb_id = ""
            for board in c.Win32_BaseBoard():
                mb_id += board.SerialNumber
                
            # Get Hard Drive ID
            hd_id = ""
            for disk in c.Win32_DiskDrive():
                hd_id += disk.SerialNumber
                
            # Combine and hash
            combined = cpu_id + mb_id + hd_id
            return hashlib.sha256(combined.encode()).hexdigest()[:16]
            
        except:
            # Fallback method
            import platform
            import uuid
            return hashlib.sha256(
                f"{platform.node()}{platform.processor()}{uuid.getnode()}".encode()
            ).hexdigest()[:16]
    
    def check_license(self):
        """Check license status"""
        print("🔑 Checking license status...")
        
        try:
            # Check local license first
            local_license = self._check_local_license()
            if local_license:
                return local_license
                
            # Check online license
            online_license = self._check_online_license()
            if online_license:
                self._save_local_license(online_license)
                return online_license
                
            # Return free license
            return self._get_free_license()
            
        except Exception as e:
            print(f"❌ License check error: {e}")
            return self._get_free_license()
    
    def _check_local_license(self):
        """Check local license file"""
        try:
            license_file = os.path.join(os.path.dirname(__file__), "license.dat")
            if os.path.exists(license_file):
                with open(license_file, 'r') as f:
                    license_data = json.loads(f.read())
                    
                # Verify license
                if self._verify_license(license_data):
                    return license_data
                    
        except Exception as e:
            print(f"❌ Local license check error: {e}")
            
        return None
    
    def _check_online_license(self):
        """Check license online"""
        try:
            # Prepare request data
            request_data = {
                'hardware_id': self.hardware_id,
                'action': 'check_license',
                'timestamp': int(time.time())
            }
            
            # Sign request
            signature = self._sign_request(request_data)
            request_data['signature'] = signature
            
            # Send request
            response = requests.post(
                f"{self.server_url}/license/check",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                license_data = response.json()
                if license_data.get('status') == 'success':
                    return license_data.get('license')
                    
        except Exception as e:
            print(f"❌ Online license check error: {e}")
            
        return None
    
    def _verify_license(self, license_data):
        """Verify license authenticity"""
        try:
            # Check hardware ID
            if license_data.get('hardware_id') != self.hardware_id:
                return False
                
            # Check expiration
            expires = license_data.get('expires')
            if expires and datetime.fromisoformat(expires) < datetime.now():
                return False
                
            # Verify signature
            signature = license_data.pop('signature', '')
            if not self._verify_signature(license_data, signature):
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ License verification error: {e}")
            return False
    
    def _sign_request(self, data):
        """Sign request data"""
        try:
            # Create signature
            message = json.dumps(data, sort_keys=True)
            signature = hmac.new(
                b'xillen_premium_secret_key_2024',
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            return signature
            
        except Exception as e:
            print(f"❌ Request signing error: {e}")
            return ""
    
    def _verify_signature(self, data, signature):
        """Verify signature"""
        try:
            # Recreate signature
            expected_signature = self._sign_request(data)
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            print(f"❌ Signature verification error: {e}")
            return False
    
    def _save_local_license(self, license_data):
        """Save license locally"""
        try:
            license_file = os.path.join(os.path.dirname(__file__), "license.dat")
            with open(license_file, 'w') as f:
                f.write(json.dumps(license_data))
                
        except Exception as e:
            print(f"❌ License save error: {e}")
    
    def _get_free_license(self):
        """Get free license"""
        return {
            'type': 'FREE',
            'hardware_id': self.hardware_id,
            'expires': None,
            'features': [
                'basic_browser_collection',
                'basic_app_collection',
                'basic_extension_collection',
                'basic_protection',
                'basic_ui'
            ],
            'limits': {
                'max_builds': 5,
                'max_logs': 100,
                'max_browsers': 50,
                'max_apps': 30,
                'max_extensions': 100
            }
        }
    
    def activate_license(self, license_key):
        """Activate license with key"""
        print(f"🔑 Activating license: {license_key[:8]}...")
        
        try:
            # Prepare activation request
            request_data = {
                'hardware_id': self.hardware_id,
                'license_key': license_key,
                'action': 'activate',
                'timestamp': int(time.time())
            }
            
            # Sign request
            signature = self._sign_request(request_data)
            request_data['signature'] = signature
            
            # Send activation request
            response = requests.post(
                f"{self.server_url}/license/activate",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    license_data = result.get('license')
                    self._save_local_license(license_data)
                    print("License activated successfully!")
                    return True
                else:
                    print(f"❌ Activation failed: {result.get('message', 'Unknown error')}")
            else:
                print(f"❌ Activation request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ License activation error: {e}")
            
        return False
    
    def get_license_info(self):
        """Get current license information"""
        license_data = self.check_license()
        
        return {
            'type': license_data.get('type', 'FREE'),
            'expires': license_data.get('expires'),
            'features': license_data.get('features', []),
            'limits': license_data.get('limits', {}),
            'hardware_id': self.hardware_id,
            'active': self._verify_license(license_data)
        }
    
    def has_feature(self, feature_name):
        """Check if license has specific feature"""
        license_data = self.check_license()
        features = license_data.get('features', [])
        return feature_name in features
    
    def get_limit(self, limit_name):
        """Get license limit"""
        license_data = self.check_license()
        limits = license_data.get('limits', {})
        return limits.get(limit_name, 0)
    
    def upgrade_license(self, new_type):
        """Upgrade license type"""
        print(f"⬆️ Upgrading to {new_type} license...")
        
        try:
            # Prepare upgrade request
            request_data = {
                'hardware_id': self.hardware_id,
                'new_type': new_type,
                'action': 'upgrade',
                'timestamp': int(time.time())
            }
            
            # Sign request
            signature = self._sign_request(request_data)
            request_data['signature'] = signature
            
            # Send upgrade request
            response = requests.post(
                f"{self.server_url}/license/upgrade",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    license_data = result.get('license')
                    self._save_local_license(license_data)
                    print(f"Upgraded to {new_type} successfully!")
                    return True
                else:
                    print(f"❌ Upgrade failed: {result.get('message', 'Unknown error')}")
            else:
                print(f"❌ Upgrade request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ License upgrade error: {e}")
            
        return False
    
    def get_available_plans(self):
        """Get available subscription plans"""
        return {
            'FREE': {
                'price': 0,
                'currency': 'USD',
                'features': [
                    'basic_browser_collection',
                    'basic_app_collection',
                    'basic_extension_collection',
                    'basic_protection',
                    'basic_ui'
                ],
                'limits': {
                    'max_builds': 5,
                    'max_logs': 100,
                    'max_browsers': 50,
                    'max_apps': 30,
                    'max_extensions': 100
                }
            },
            'BASIC': {
                'price': 99,
                'currency': 'USD',
                'period': 'monthly',
                'features': [
                    'extended_browser_collection',
                    'extended_app_collection',
                    'extended_extension_collection',
                    'advanced_protection',
                    'premium_ui',
                    'cloud_sync',
                    'priority_support'
                ],
                'limits': {
                    'max_builds': 50,
                    'max_logs': 1000,
                    'max_browsers': 150,
                    'max_apps': 100,
                    'max_extensions': 300
                }
            },
            'PRO': {
                'price': 299,
                'currency': 'USD',
                'period': 'monthly',
                'features': [
                    'all_basic_features',
                    'ai_target_detection',
                    'advanced_evasion',
                    'polymorphic_morpher',
                    'cloud_panel',
                    'api_access',
                    'custom_modules',
                    'analytics_dashboard'
                ],
                'limits': {
                    'max_builds': 200,
                    'max_logs': 10000,
                    'max_browsers': 500,
                    'max_apps': 300,
                    'max_extensions': 1000
                }
            },
            'ENTERPRISE': {
                'price': 599,
                'currency': 'USD',
                'period': 'monthly',
                'features': [
                    'all_pro_features',
                    'white_label',
                    'custom_deployment',
                    'dedicated_support',
                    'sla_guarantee',
                    'custom_integrations',
                    'team_management',
                    'audit_logs'
                ],
                'limits': {
                    'max_builds': -1,  # Unlimited
                    'max_logs': -1,    # Unlimited
                    'max_browsers': -1, # Unlimited
                    'max_apps': -1,    # Unlimited
                    'max_extensions': -1 # Unlimited
                }
            }
        }

# Global instance
licensing_system = LicensingSystem()

def check_license():
    """Check license status"""
    return licensing_system.check_license()

def activate_license(license_key):
    """Activate license"""
    return licensing_system.activate_license(license_key)

def has_feature(feature_name):
    """Check if license has feature"""
    return licensing_system.has_feature(feature_name)

def get_limit(limit_name):
    """Get license limit"""
    return licensing_system.get_limit(limit_name)

def get_license_info():
    """Get license information"""
    return licensing_system.get_license_info()

def get_available_plans():
    """Get available plans"""
    return licensing_system.get_available_plans()

def upgrade_license(new_type):
    """Upgrade license"""
    return licensing_system.upgrade_license(new_type)

if __name__ == "__main__":
    print("🔑 XillenStealer V5 - Premium Licensing System")
    print("=" * 50)
    
    # Check license
    license_info = get_license_info()
    print(f"📊 License Info: {license_info}")
    
    # Show available plans
    plans = get_available_plans()
    print("\n💰 Available Plans:")
    for plan_name, plan_info in plans.items():
        price = plan_info.get('price', 0)
        period = plan_info.get('period', '')
        print(f"  {plan_name}: ${price}/{period}")
    
    # Check features
    features_to_check = [
        'ai_target_detection',
        'cloud_panel',
        'advanced_evasion',
        'polymorphic_morpher'
    ]
    
    print("\n🔍 Feature Check:")
    for feature in features_to_check:
        has_feat = has_feature(feature)
        status = "✅" if has_feat else "❌"
        print(f"  {status} {feature}")
    
    print("\n🎯 Limits:")
    limits_to_check = ['max_builds', 'max_logs', 'max_browsers']
    for limit in limits_to_check:
        limit_value = get_limit(limit)
        print(f"  {limit}: {limit_value}")
