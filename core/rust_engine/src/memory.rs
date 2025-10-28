use winapi::um::memoryapi::{VirtualAlloc, VirtualFree, VirtualProtect};
use winapi::um::winnt::{MEM_COMMIT, MEM_RESERVE, MEM_RELEASE, PAGE_READWRITE, PAGE_EXECUTE_READWRITE};
use winapi::shared::minwindef::{DWORD, FALSE};
use std::collections::HashMap;
use std::ptr;

pub struct MemoryManager {
    allocations: HashMap<u64, usize>,
    secure_heap: Vec<SecureBlock>,
}

struct SecureBlock {
    address: u64,
    size: usize,
    is_encrypted: bool,
}

impl MemoryManager {
    pub fn new() -> Self {
        MemoryManager {
            allocations: HashMap::new(),
            secure_heap: Vec::new(),
        }
    }

    pub fn secure_allocate(&mut self, size: usize) -> u64 {
        unsafe {
            let aligned_size = (size + 4095) & !4095;
            
            let addr = VirtualAlloc(
                ptr::null_mut(),
                aligned_size,
                MEM_COMMIT | MEM_RESERVE,
                PAGE_READWRITE
            ) as u64;

            if addr != 0 {
                self.allocations.insert(addr, aligned_size);
                
                let block = SecureBlock {
                    address: addr,
                    size: aligned_size,
                    is_encrypted: false,
                };
                self.secure_heap.push(block);
                
                self.zero_memory(addr, aligned_size);
            }

            addr
        }
    }

    pub fn secure_free(&mut self, addr: u64) -> bool {
        if let Some(&size) = self.allocations.get(&addr) {
            self.zero_memory(addr, size);
            
            unsafe {
                let result = VirtualFree(addr as *mut _, 0, MEM_RELEASE) != 0;
                if result {
                    self.allocations.remove(&addr);
                    self.secure_heap.retain(|block| block.address != addr);
                }
                result
            }
        } else {
            false
        }
    }

    pub fn zero_memory(&self, addr: u64, size: usize) -> bool {
        if addr == 0 || size == 0 {
            return false;
        }

        unsafe {
            let ptr = addr as *mut u8;
            for i in 0..size {
                *ptr.add(i) = 0;
            }
        }

        self.flush_cpu_cache(addr, size);
        true
    }

    pub fn encrypt_memory_block(&mut self, addr: u64, key: &[u8; 32]) -> bool {
        if let Some(block_idx) = self.secure_heap.iter().position(|b| b.address == addr) {
            if !self.secure_heap[block_idx].is_encrypted {
                unsafe {
                    let ptr = addr as *mut u8;
                    let size = self.secure_heap[block_idx].size;
                    
                    for i in 0..size {
                        let byte_ptr = ptr.add(i);
                        *byte_ptr ^= key[i % 32];
                    }
                }
                
                self.secure_heap[block_idx].is_encrypted = true;
                return true;
            }
        }
        false
    }

    pub fn decrypt_memory_block(&mut self, addr: u64, key: &[u8; 32]) -> bool {
        if let Some(block_idx) = self.secure_heap.iter().position(|b| b.address == addr) {
            if self.secure_heap[block_idx].is_encrypted {
                unsafe {
                    let ptr = addr as *mut u8;
                    let size = self.secure_heap[block_idx].size;
                    
                    for i in 0..size {
                        let byte_ptr = ptr.add(i);
                        *byte_ptr ^= key[i % 32];
                    }
                }
                
                self.secure_heap[block_idx].is_encrypted = false;
                return true;
            }
        }
        false
    }

    pub fn make_executable(&self, addr: u64, size: usize) -> bool {
        unsafe {
            let mut old_protect: DWORD = 0;
            VirtualProtect(
                addr as *mut _,
                size,
                PAGE_EXECUTE_READWRITE,
                &mut old_protect
            ) != 0
        }
    }

    pub fn hook_memory_allocations(&self) -> bool {
        unsafe {
            let ntdll = winapi::um::libloaderapi::GetModuleHandleA(
                b"ntdll.dll\0".as_ptr() as *const i8
            );
            
            if ntdll.is_null() {
                return false;
            }

            let nt_allocate_virtual_memory = winapi::um::libloaderapi::GetProcAddress(
                ntdll,
                b"NtAllocateVirtualMemory\0".as_ptr() as *const i8
            );

            !nt_allocate_virtual_memory.is_null()
        }
    }

    pub fn detect_heap_spray(&self) -> bool {
        let total_allocated: usize = self.allocations.values().sum();
        let allocation_count = self.allocations.len();
        
        if allocation_count > 100 {
            return true;
        }
        
        if total_allocated > 100 * 1024 * 1024 {
            return true;
        }
        
        false
    }

    pub fn stack_pivot(&self, new_stack: u64, stack_size: usize) -> bool {
        if new_stack == 0 || stack_size == 0 {
            return false;
        }

        unsafe {
            let mut old_protect: DWORD = 0;
            let result = VirtualProtect(
                new_stack as *mut _,
                stack_size,
                PAGE_EXECUTE_READWRITE,
                &mut old_protect
            );

            if result != 0 {
                std::arch::asm!(
                    "mov rsp, {0}",
                    in(reg) new_stack + stack_size as u64 - 8,
                    options(nostack)
                );
                return true;
            }
        }
        false
    }

    pub fn memory_scan_evasion(&self, target_addr: u64, size: usize) -> bool {
        unsafe {
            let guard_pages = 2;
            let guard_size = 4096;
            
            for i in 0..guard_pages {
                let guard_addr = target_addr - ((i + 1) as u64 * guard_size);
                
                VirtualAlloc(
                    guard_addr as *mut _,
                    guard_size as usize,
                    MEM_COMMIT | MEM_RESERVE,
                    winapi::um::winnt::PAGE_NOACCESS
                );
            }
            
            for i in 0..guard_pages {
                let guard_addr = target_addr + size as u64 + (i as u64 * guard_size);
                
                VirtualAlloc(
                    guard_addr as *mut _,
                    guard_size as usize,
                    MEM_COMMIT | MEM_RESERVE,
                    winapi::um::winnt::PAGE_NOACCESS
                );
            }
        }
        true
    }

    fn flush_cpu_cache(&self, addr: u64, size: usize) {
        unsafe {
            for i in (0..size).step_by(64) {
                let cache_line = (addr + i as u64) as *const u8;
                std::arch::x86_64::_mm_clflush(cache_line);
            }
            std::arch::x86_64::_mm_mfence();
        }
    }

    pub fn anti_dump_protection(&self, base_addr: u64, size: usize) -> bool {
        unsafe {
            let pages = (size + 4095) / 4096;
            let mut success_count = 0;

            for i in 0..pages {
                let page_addr = base_addr + (i * 4096) as u64;
                let mut old_protect: DWORD = 0;
                
                if VirtualProtect(
                    page_addr as *mut _,
                    4096,
                    winapi::um::winnt::PAGE_GUARD | winapi::um::winnt::PAGE_READWRITE,
                    &mut old_protect
                ) != 0 {
                    success_count += 1;
                }
            }

            success_count > pages / 2
        }
    }
}

impl Drop for MemoryManager {
    fn drop(&mut self) {
        for (&addr, &size) in &self.allocations {
            self.zero_memory(addr, size);
            unsafe {
                VirtualFree(addr as *mut _, 0, MEM_RELEASE);
            }
        }
    }
}
