import json
import requests
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sqlite3
import hashlib
import base64
import logging

class TelegramSubscriptionManager:
    def __init__(self):
        self.bot_token = None
        self.bot_active = False
        self.subscriptions = {}
        self.pending_activations = {}
        self.webhook_url = None
        
        # Database setup
        self._init_database()
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _init_database(self):
        """Initialize subscription database"""
        try:
            conn = sqlite3.connect('subscriptions.db')
            cursor = conn.cursor()
            
            # Subscriptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE,
                    username TEXT,
                    subscription_type TEXT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    status TEXT,
                    payment_method TEXT,
                    amount REAL,
                    currency TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Activation codes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activation_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    subscription_type TEXT,
                    duration_days INTEGER,
                    max_uses INTEGER DEFAULT 1,
                    used_count INTEGER DEFAULT 0,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            ''')
            
            # Payment history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    subscription_type TEXT,
                    amount REAL,
                    currency TEXT,
                    payment_method TEXT,
                    status TEXT,
                    transaction_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Database init error: {e}")
    
    def setup_bot(self, bot_token, webhook_url=None):
        """Setup Telegram bot"""
        print("🤖 Setting up Telegram Subscription Bot...")
        
        try:
            self.bot_token = bot_token
            self.webhook_url = webhook_url
            
            # Test bot connection
            if self._test_bot_connection():
                self.bot_active = True
                
                # Setup webhook if provided
                if webhook_url:
                    self._setup_webhook(webhook_url)
                
                # Start bot polling
                self._start_bot_polling()
                
                print("Telegram Bot setup successful!")
                return True
            else:
                print("Telegram Bot setup failed!")
                return False
                
        except Exception as e:
            print(f"❌ Bot setup error: {e}")
            return False
    
    def _test_bot_connection(self):
        """Test bot connection"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                print(f"Bot connected: @{bot_info['result']['username']}")
                return True
            else:
                print(f"❌ Bot connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Bot test error: {e}")
            return False
    
    def _setup_webhook(self, webhook_url):
        """Setup webhook for bot"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/setWebhook"
            data = {'url': webhook_url}
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                print("Webhook setup successful!")
                return True
            else:
                print(f"❌ Webhook setup failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Webhook setup error: {e}")
            return False
    
    def _start_bot_polling(self):
        """Start bot polling for updates"""
        def polling_worker():
            last_update_id = 0
            
            while self.bot_active:
                try:
                    url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
                    params = {'offset': last_update_id + 1, 'timeout': 30}
                    
                    response = requests.get(url, params=params, timeout=35)
                    
                    if response.status_code == 200:
                        updates = response.json()
                        
                        for update in updates.get('result', []):
                            last_update_id = update['update_id']
                            self._handle_update(update)
                    
                except Exception as e:
                    self.logger.error(f"Polling error: {e}")
                    time.sleep(5)
        
        polling_thread = threading.Thread(target=polling_worker, daemon=True)
        polling_thread.start()
    
    def _handle_update(self, update):
        """Handle incoming update"""
        try:
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')
                user_id = str(message['from']['id'])
                username = message['from'].get('username', '')
                
                # Handle commands
                if text.startswith('/'):
                    self._handle_command(chat_id, user_id, username, text)
                else:
                    self._handle_message(chat_id, user_id, username, text)
                    
        except Exception as e:
            self.logger.error(f"Update handling error: {e}")
    
    def _handle_command(self, chat_id, user_id, username, command):
        """Handle bot commands"""
        try:
            if command == '/start':
                self._send_welcome_message(chat_id)
            elif command == '/help':
                self._send_help_message(chat_id)
            elif command == '/status':
                self._send_status_message(chat_id, user_id)
            elif command == '/plans':
                self._send_plans_message(chat_id)
            elif command == '/activate':
                self._send_activation_message(chat_id, user_id)
            elif command == '/admin':
                self._handle_admin_command(chat_id, user_id)
            else:
                self._send_message(chat_id, "❌ Unknown command. Use /help for available commands.")
                
        except Exception as e:
            self.logger.error(f"Command handling error: {e}")
    
    def _handle_message(self, chat_id, user_id, username, text):
        """Handle regular messages"""
        try:
            # Check if user is waiting for activation code
            if user_id in self.pending_activations:
                self._process_activation_code(chat_id, user_id, username, text)
            else:
                self._send_message(chat_id, "Use /help for available commands.")
                
        except Exception as e:
            self.logger.error(f"Message handling error: {e}")
    
    def _send_welcome_message(self, chat_id):
        """Send welcome message"""
        message = """
🎉 Welcome to XillenStealer V5 Premium!

I'm your subscription manager bot. Here's what I can do:

🔑 License Management
📊 Subscription Status
💳 Payment Processing
🎯 Activation Codes

Use /help for detailed commands.
        """
        self._send_message(chat_id, message)
    
    def _send_help_message(self, chat_id):
        """Send help message"""
        message = """
📋 Available Commands:

/start - Welcome message
/help - This help message
/status - Check your subscription status
/plans - View available subscription plans
/activate - Activate subscription with code
/admin - Admin commands (admin only)

💡 How to use:
1. Use /plans to see available plans
2. Contact admin for payment
3. Use /activate with your activation code
4. Check /status to verify activation
        """
        self._send_message(chat_id, message)
    
    def _send_status_message(self, chat_id, user_id):
        """Send subscription status"""
        try:
            subscription = self._get_user_subscription(user_id)
            
            if subscription:
                status = subscription['status']
                sub_type = subscription['subscription_type']
                end_date = subscription['end_date']
                
                if status == 'active':
                    message = f"""
✅ Subscription Status: ACTIVE
📦 Plan: {sub_type.upper()}
📅 Expires: {end_date}
🎯 Features: All premium features enabled
                    """
                else:
                    message = f"""
❌ Subscription Status: {status.upper()}
📦 Plan: {sub_type.upper()}
📅 Expired: {end_date}
🔒 Features: Limited to free tier
                    """
            else:
                message = """
❌ No active subscription found
🔒 You're using the free version
💡 Use /plans to see available plans
                """
            
            self._send_message(chat_id, message)
            
        except Exception as e:
            self.logger.error(f"Status message error: {e}")
    
    def _send_plans_message(self, chat_id):
        """Send available plans"""
        message = """
💰 Available Subscription Plans:

🆓 FREE
• Basic browser collection
• Basic app collection
• Basic protection
• 5 builds limit
• 100 logs limit

💎 BASIC - $99/month
• Extended browser collection (150+ browsers)
• Extended app collection (100+ apps)
• Advanced protection
• Cloud sync
• 50 builds limit
• 1000 logs limit

🚀 PRO - $299/month
• All BASIC features
• AI target detection
• Advanced evasion
• Polymorphic morpher
• Cloud panel
• API access
• 200 builds limit
• 10000 logs limit

🏢 ENTERPRISE - $599/month
• All PRO features
• White label
• Custom deployment
• Dedicated support
• Unlimited builds
• Unlimited logs

Contact admin for payment and activation code.
        """
        self._send_message(chat_id, message)
    
    def _send_activation_message(self, chat_id, user_id):
        """Send activation prompt"""
        message = """
🔑 Subscription Activation

Please send your activation code to activate your subscription.

Format: ACTIVATE-XXXX-XXXX-XXXX

Example: ACTIVATE-1234-5678-9ABC
        """
        self._send_message(chat_id, message)
        self.pending_activations[user_id] = 'waiting_for_code'
    
    def _process_activation_code(self, chat_id, user_id, username, code):
        """Process activation code"""
        try:
            # Validate code format
            if not code.startswith('ACTIVATE-'):
                self._send_message(chat_id, "❌ Invalid code format. Use ACTIVATE-XXXX-XXXX-XXXX")
                return
            
            # Extract code
            activation_code = code.replace('ACTIVATE-', '').replace('-', '')
            
            # Check if code exists
            conn = sqlite3.connect('subscriptions.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM activation_codes 
                WHERE code = ? AND used_count < max_uses 
                AND (expires_at IS NULL OR expires_at > datetime('now'))
            ''', (activation_code,))
            
            code_data = cursor.fetchone()
            
            if code_data:
                # Activate subscription
                subscription_type = code_data[2]
                duration_days = code_data[3]
                
                start_date = datetime.now()
                end_date = start_date + timedelta(days=duration_days)
                
                # Update or insert subscription
                cursor.execute('''
                    INSERT OR REPLACE INTO subscriptions 
                    (user_id, username, subscription_type, start_date, end_date, status)
                    VALUES (?, ?, ?, ?, ?, 'active')
                ''', (user_id, username, subscription_type, start_date, end_date))
                
                # Update code usage
                cursor.execute('''
                    UPDATE activation_codes 
                    SET used_count = used_count + 1 
                    WHERE code = ?
                ''', (activation_code,))
                
                conn.commit()
                conn.close()
                
                # Remove from pending
                del self.pending_activations[user_id]
                
                # Send success message
                message = f"""
✅ Subscription Activated Successfully!

📦 Plan: {subscription_type.upper()}
📅 Valid until: {end_date.strftime('%Y-%m-%d %H:%M:%S')}
🎯 All premium features are now enabled!

Use /status to check your subscription anytime.
                """
                self._send_message(chat_id, message)
                
            else:
                self._send_message(chat_id, "❌ Invalid or expired activation code.")
            
        except Exception as e:
            self.logger.error(f"Activation processing error: {e}")
            self._send_message(chat_id, "❌ Activation failed. Please try again.")
    
    def _handle_admin_command(self, chat_id, user_id):
        """Handle admin commands"""
        # Check if user is admin
        if not self._is_admin(user_id):
            self._send_message(chat_id, "❌ Admin access denied.")
            return
        
        message = """
👑 Admin Commands:

/create_code TYPE DURATION USES
Example: /create_code PRO 30 1

/list_codes - List all activation codes
/list_subscriptions - List all subscriptions
/stats - Show bot statistics

Use /help for regular commands.
        """
        self._send_message(chat_id, message)
    
    def _is_admin(self, user_id):
        """Check if user is admin"""
        # Add your admin user IDs here
        admin_ids = ['123456789', '987654321']  # Replace with actual admin IDs
        return user_id in admin_ids
    
    def _get_user_subscription(self, user_id):
        """Get user subscription"""
        try:
            conn = sqlite3.connect('subscriptions.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM subscriptions 
                WHERE user_id = ? AND status = 'active'
                ORDER BY end_date DESC LIMIT 1
            ''', (user_id,))
            
            subscription = cursor.fetchone()
            conn.close()
            
            if subscription:
                return {
                    'user_id': subscription[1],
                    'username': subscription[2],
                    'subscription_type': subscription[3],
                    'start_date': subscription[4],
                    'end_date': subscription[5],
                    'status': subscription[6]
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Get subscription error: {e}")
            return None
    
    def _send_message(self, chat_id, text):
        """Send message to user"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code != 200:
                self.logger.error(f"Send message failed: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Send message error: {e}")
    
    def create_activation_code(self, subscription_type, duration_days, max_uses=1, created_by="admin"):
        """Create activation code"""
        try:
            # Generate unique code
            code = self._generate_activation_code()
            
            # Calculate expiry date
            expires_at = datetime.now() + timedelta(days=30)  # Codes expire in 30 days
            
            # Save to database
            conn = sqlite3.connect('subscriptions.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO activation_codes 
                (code, subscription_type, duration_days, max_uses, created_by, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (code, subscription_type, duration_days, max_uses, created_by, expires_at))
            
            conn.commit()
            conn.close()
            
            print(f"Activation code created: ACTIVATE-{code}")
            return f"ACTIVATE-{code}"
            
        except Exception as e:
            print(f"❌ Create code error: {e}")
            return None
    
    def _generate_activation_code(self):
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
    
    def get_subscription_stats(self):
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
            
            conn.close()
            
            return {
                'total_subscriptions': total_subs,
                'active_subscriptions': active_subs,
                'by_type': by_type,
                'total_revenue': revenue
            }
            
        except Exception as e:
            self.logger.error(f"Stats error: {e}")
            return {}
    
    def stop_bot(self):
        """Stop bot"""
        self.bot_active = False
        print("Telegram Bot stopped!")

# Global instance
telegram_subscription_manager = TelegramSubscriptionManager()

def setup_telegram_bot(bot_token, webhook_url=None):
    """Setup Telegram bot"""
    return telegram_subscription_manager.setup_bot(bot_token, webhook_url)

def create_activation_code(subscription_type, duration_days, max_uses=1):
    """Create activation code"""
    return telegram_subscription_manager.create_activation_code(
        subscription_type, duration_days, max_uses
    )

def get_subscription_stats():
    """Get subscription statistics"""
    return telegram_subscription_manager.get_subscription_stats()

def stop_telegram_bot():
    """Stop Telegram bot"""
    telegram_subscription_manager.stop_bot()

if __name__ == "__main__":
    print("🤖 XillenStealer V5 - Telegram Subscription Manager")
    print("=" * 60)
    
    # Test bot setup
    bot_token = "YOUR_BOT_TOKEN_HERE"  # Replace with actual bot token
    
    if setup_telegram_bot(bot_token):
        print("Bot setup successful!")
        
        # Create some test activation codes
        print("\n🔑 Creating test activation codes...")
        
        basic_code = create_activation_code("BASIC", 30, 1)
        pro_code = create_activation_code("PRO", 30, 1)
        enterprise_code = create_activation_code("ENTERPRISE", 30, 1)
        
        print(f"BASIC Code: {basic_code}")
        print(f"PRO Code: {pro_code}")
        print(f"ENTERPRISE Code: {enterprise_code}")
        
        # Get stats
        stats = get_subscription_stats()
        print(f"\n📊 Subscription Stats: {stats}")
        
        # Keep bot running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_telegram_bot()
    else:
        print("❌ Bot setup failed!")
