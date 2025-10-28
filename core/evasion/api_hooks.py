import ctypes
from ctypes import wintypes

class ApiHooks:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.psapi = ctypes.windll.psapi
        self.hooks = []
        
    def hook_crypt_protect_memory(self):
        try:
            crypt32 = ctypes.windll.crypt32
            func_addr = ctypes.addressof(crypt32.CryptProtectMemory)
            return self._install_inline_hook(func_addr, "CryptProtectMemory")
        except:
            return False
            
    def hook_bcrypt_encrypt(self):
        try:
            bcrypt = ctypes.windll.bcrypt
            func_addr = ctypes.addressof(bcrypt.BCryptEncrypt)
            return self._install_inline_hook(func_addr, "BCryptEncrypt")
        except:
            return False
            
    def hook_ncrypt_decrypt(self):
        try:
            ncrypt = ctypes.windll.ncrypt
            func_addr = ctypes.addressof(ncrypt.NCryptDecryptKey)
            return self._install_inline_hook(func_addr, "NCryptDecryptKey")
        except:
            return False
            
    def _install_inline_hook(self, func_addr, func_name):
        old_protect = ctypes.c_ulong(0)
        PAGE_EXECUTE_READWRITE = 0x40
        
        detour = self._create_detour(func_addr)
        
        if self.kernel32.VirtualProtect(
            func_addr, len(detour), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)
        ):
            ctypes.memmove(func_addr, detour, len(detour))
            self.hooks.append({
                "function": func_name,
                "address": func_addr,
                "original": detour
            })
            return True
        return False
        
    def _create_detour(self, original_addr):
        detour = bytearray([0x48, 0xB8])
        detour.extend(original_addr.to_bytes(8, 'little'))
        detour.extend([0xFF, 0xE0])
        return bytes(detour)
        
    def unhook_all(self):
        PAGE_EXECUTE_READWRITE = 0x40
        for hook in self.hooks:
            old_protect = ctypes.c_ulong(0)
            self.kernel32.VirtualProtect(
                hook["address"], len(hook["original"]), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)
            )
            ctypes.memmove(hook["address"], hook["original"], len(hook["original"]))
        self.hooks.clear()
