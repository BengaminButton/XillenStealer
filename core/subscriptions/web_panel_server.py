from flask import Flask, request, jsonify, render_template_string
import sqlite3
import json
from datetime import datetime, timedelta
import os
import threading
import time

app = Flask(__name__)

# Load web panel HTML
def load_web_panel():
    try:
        with open('core/subscriptions/web_panel.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Failed to load web panel: {e}")
        return "<h1>Web Panel Not Found</h1>"

@app.route('/')
def index():
    """Serve the web panel"""
    return load_web_panel()

@app.route('/api/stats')
def get_stats():
    """Get subscription statistics"""
    try:
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        # Total subscriptions
        cursor.execute('SELECT COUNT(*) FROM subscriptions')
        total_subs = cursor.fetchone()[0]
        
        # Active subscriptions
        cursor.execute('SELECT COUNT(*) FROM subscriptions WHERE status = "active"')
        active_subs = cursor.fetchone()[0]
        
        # By type
        cursor.execute('''
            SELECT subscription_type, COUNT(*) 
            FROM subscriptions 
            WHERE status = "active" 
            GROUP BY subscription_type
        ''')
        by_type = dict(cursor.fetchall())
        
        # Revenue
        cursor.execute('''
            SELECT SUM(amount) FROM payments 
            WHERE status = "completed"
        ''')
        revenue = cursor.fetchone()[0] or 0
        
        # Pending activations (codes not used)
        cursor.execute('''
            SELECT COUNT(*) FROM activation_codes 
            WHERE used_count < max_uses 
            AND (expires_at IS NULL OR expires_at > datetime('now'))
        ''')
        pending_activations = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_subscriptions': total_subs,
            'active_subscriptions': active_subs,
            'by_type': by_type,
            'total_revenue': revenue,
            'pending_activations': pending_activations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscriptions')
def get_subscriptions():
    """Get all subscriptions"""
    try:
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, subscription_type, start_date, end_date, status
            FROM subscriptions 
            ORDER BY created_at DESC
        ''')
        
        subscriptions = []
        for row in cursor.fetchall():
            subscriptions.append({
                'user_id': row[0],
                'username': row[1],
                'subscription_type': row[2],
                'start_date': row[3],
                'end_date': row[4],
                'status': row[5]
            })
        
        conn.close()
        
        return jsonify(subscriptions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/codes')
def get_codes():
    """Get all activation codes"""
    try:
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, code, subscription_type, duration_days, max_uses, 
                   used_count, created_at, expires_at
            FROM activation_codes 
            ORDER BY created_at DESC
        ''')
        
        codes = []
        for row in cursor.fetchall():
            codes.append({
                'id': row[0],
                'code': row[1],
                'subscription_type': row[2],
                'duration_days': row[3],
                'max_uses': row[4],
                'used_count': row[5],
                'created_at': row[6],
                'expires_at': row[7]
            })
        
        conn.close()
        
        return jsonify(codes)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-code', methods=['POST'])
def create_code():
    """Create new activation code"""
    try:
        data = request.get_json()
        
        subscription_type = data.get('subscription_type')
        duration_days = data.get('duration_days')
        max_uses = data.get('max_uses', 1)
        
        if not subscription_type or not duration_days:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Generate unique code
        code = generate_activation_code()
        
        # Calculate expiry date
        expires_at = datetime.now() + timedelta(days=30)
        
        # Save to database
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activation_codes 
            (code, subscription_type, duration_days, max_uses, created_by, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (code, subscription_type, duration_days, max_uses, 'admin', expires_at))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'code': f'ACTIVATE-{code}',
            'message': 'Activation code created successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/delete-code/<int:code_id>', methods=['DELETE'])
def delete_code(code_id):
    """Delete activation code"""
    try:
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM activation_codes WHERE id = ?', (code_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Code deleted successfully'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': 'Code not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/search-user')
def search_user():
    """Search for user"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        # Search by user_id or username
        cursor.execute('''
            SELECT user_id, username, subscription_type, start_date, end_date, status
            FROM subscriptions 
            WHERE user_id LIKE ? OR username LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'user_id': user[0],
                'username': user[1],
                'subscription_type': user[2],
                'start_date': user[3],
                'end_date': user[4],
                'status': user[5]
            })
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/deactivate-user/<user_id>', methods=['POST'])
def deactivate_user(user_id):
    """Deactivate user subscription"""
    try:
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE subscriptions 
            SET status = 'inactive' 
            WHERE user_id = ?
        ''', (user_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'User deactivated successfully'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/extend-subscription/<user_id>', methods=['POST'])
def extend_subscription(user_id):
    """Extend user subscription"""
    try:
        data = request.get_json()
        days = data.get('days')
        
        if not days or days <= 0:
            return jsonify({'success': False, 'message': 'Invalid number of days'}), 400
        
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        # Get current end date
        cursor.execute('SELECT end_date FROM subscriptions WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            current_end = datetime.fromisoformat(result[0])
            new_end = current_end + timedelta(days=days)
            
            cursor.execute('''
                UPDATE subscriptions 
                SET end_date = ?, status = 'active'
                WHERE user_id = ?
            ''', (new_end.isoformat(), user_id))
            
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Subscription extended successfully'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def generate_activation_code():
    """Generate unique activation code"""
    import random
    import string
    
    while True:
        # Generate 12-character code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        # Check if code already exists
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM activation_codes WHERE code = ?', (code,))
        count = cursor.fetchone()[0]
        
        conn.close()
        
        if count == 0:
            return code

def start_web_panel(host='127.0.0.1', port=5000, debug=False):
    """Start the web panel server"""
    print(f"🌐 Starting Web Panel Server...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        print(f"❌ Web panel error: {e}")

if __name__ == "__main__":
    print("🌐 XillenStealer V5 - Premium Web Panel Server")
    print("=" * 60)
    
    # Start web panel
    start_web_panel(debug=True)
