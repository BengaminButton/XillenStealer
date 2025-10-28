import ctypes
import platform
import os

class AntiAnalysis:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.ntdll = ctypes.windll.ntdll
        
    def check_hardware(self):
        cpu_cores = os.cpu_count()
        ram_gb = os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE') / (1024**3) if hasattr(os, 'sysconf') else 8
        
        stats = os.statvfs('/') if hasattr(os, 'statvfs') else None
        disk_gb = stats.f_frsize * stats.f_blocks / (1024**3) if stats else 80
        
        if cpu_cores <= 2 or (stats and disk_gb < 80):
            return False
        return True
        
    def check_vm(self):
        vm_artifacts = [
            'vmware', 'virtualbox', 'vbox', 'qemu', 'kvm',
            'xen', 'parallels', 'hyper-v', 'bhyve'
        ]
        
        for artifact in vm_artifacts:
            if self._check_registry(artifact):
                return True
            if self._check_processes(artifact):
                return True
            if self._check_mac(artifact):
                return True
                
        if self._check_cpuid():
            return True
            
        return False
        
    def _check_registry(self, keyword):
        try:
            import winreg
            keys = [
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft"),
            ]
            
            for hkey, path in keys:
                try:
                    key = winreg.OpenKey(hkey, path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey = winreg.EnumKey(key, i)
                        if keyword.lower() in subkey.lower():
                            return True
                    winreg.CloseKey(key)
                except:
                    pass
        except:
            pass
        return False
        
    def _check_processes(self, keyword):
        import subprocess
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True, timeout=2)
            if keyword.lower() in result.stdout.lower():
                return True
        except:
            pass
        return False
        
    def _check_mac(self, keyword):
        import uuid
        mac = hex(uuid.getnode())
        
        vm_macs = {
            'vmware': '005056',
            'virtualbox': '080027',
            'parallels': '001c42',
            'hyper-v': '0003ff'
        }
        
        for vm, mac_prefix in vm_macs.items():
            if mac_prefix in mac and vm == keyword:
                return True
        return False
        
    def _check_cpuid(self):
        try:
            result = self.ntdll.IsProcessorFeaturePresent(0x80000001)
            return result != 0
        except:
            pass
        return False
        
    def check_debugger(self):
        if self.kernel32.IsDebuggerPresent():
            return True
            
        debug_flag = ctypes.c_ulong(0)
        if self.kernel32.CheckRemoteDebuggerPresent(-1, ctypes.byref(debug_flag)):
            if debug_flag.value != 0:
                return True
                
        peb = ctypes.c_void_p()
        self.ntdll.RtlGetCurrentPeb(ctypes.byref(peb))
        
        if peb.value:
            being_debugged = ctypes.cast(
                peb.value + 2, ctypes.POINTER(ctypes.c_ubyte)
            )
            if being_debugged.contents.value != 0:
                return True
                
        return False
        
    def check_sandbox(self):
        import time
        import ctypes.wintypes
        
        start = time.time()
        self.kernel32.GetTickCount()
        elapsed = time.time() - start
        
        if elapsed > 0.1:
            return True
            
        cursor_pos = ctypes.wintypes.POINT()
        if self.kernel32.GetCursorPos(ctypes.byref(cursor_pos)):
            time.sleep(1)
            new_pos = ctypes.wintypes.POINT()
            if self.kernel32.GetCursorPos(ctypes.byref(new_pos)):
                if cursor_pos.x == new_pos.x and cursor_pos.y == new_pos.y:
                    return True
                    
        return False
