# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['stealer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
<<<<<<< HEAD
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'pynput._util',
        'pynput._util.win32',
        'pynput._util.darwin',
        'pynput._util.xorg',
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.ciphers',
        'cryptography.hazmat.backends',
        'cryptography.hazmat.backends.openssl',
        'requests',
        'win32api',
        'win32con',
        'win32security',
        'win32wnet',
        'winreg',
        'psutil',
        'PIL',
        'PIL.Image',
        'PIL.ImageGrab',
        'PIL._tkinter_finder',
        'base64',
        'io',
        'json',
        'sqlite3',
        'shutil',
        'zipfile',
        'tempfile',
        'subprocess',
        'struct',
        'ctypes',
        'win32crypt',
        'keyring',
        'pycryptodome',
        'Crypto',
        'Crypto.Cipher',
        'Crypto.Cipher.AES',
=======
        # Core dependencies
        'requests', 'psutil', 'PIL', 'pillow', 'browser_cookie3', 'pyTelegramBotAPI',
        
        # Cryptography
        'pycryptodome', 'Crypto', 'cryptography', 'secretstorage',
        
        # System input capture - CRITICAL FOR V4
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'pynput._util.win32',
        'pynput._util',
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        
        # Computer vision and audio
        'cv2',
        'sounddevice',
        'scipy',
        'scipy.io.wavfile',
        
        # Windows API
        'win32api', 'win32con', 'win32process', 'win32security', 'win32wnet', 'winreg', 'win32com.client',
        
        # Optional dependencies
        'dns',
        'icmplib',
        
        # Standard library modules
        'base64', 'io', 'json', 'sqlite3', 'shutil', 'zipfile', 'tempfile', 'subprocess',
        'struct', 'ctypes', 'win32crypt', 'keyring',
        'hashlib', 'random', 'string', 'pickle', 'gzip',
        'html', 'xml.etree.ElementTree', 'configparser',
        'threading', 'datetime', 'pathlib', 'glob',
        'array', 'mmap', 'socket', 'select',
>>>>>>> b660952d800004577688f6a7206ecb24280dc912
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
    name='Xillena',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
<<<<<<< HEAD
=======
    argv_emulation=False,
>>>>>>> b660952d800004577688f6a7206ecb24280dc912
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=False,
)
<<<<<<< HEAD
=======

>>>>>>> b660952d800004577688f6a7206ecb24280dc912
