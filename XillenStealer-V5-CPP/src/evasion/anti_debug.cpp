#include "anti_debug.h"
#include <tlhelp32.h>
#include <cstring>

bool AntiDebug::IsDebuggerPresent() {
    return ::IsDebuggerPresent();
}

bool AntiDebug::CheckRemoteDebugger() {
    BOOL debugFlag = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &debugFlag);
    return debugFlag == TRUE;
}

bool AntiDebug::CheckParentProcess() {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) return false;
    
    PROCESSENTRY32 pe = { sizeof(pe) };
    DWORD parentPid = 0;
    DWORD currentPid = GetCurrentProcessId();
    
    if (Process32First(snapshot, &pe)) {
        do {
            if (pe.th32ProcessID == currentPid) {
                parentPid = pe.th32ParentProcessID;
                break;
            }
        } while (Process32Next(snapshot, &pe));
    }
    CloseHandle(snapshot);
    
    if (parentPid == 0) return true;
    
    snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (Process32First(snapshot, &pe)) {
        do {
            if (pe.th32ProcessID == parentPid) {
                CloseHandle(snapshot);
                char* exeName = (char*)pe.szExeFile;
                return (strcmp(exeName, "explorer.exe") != 0);
            }
        } while (Process32Next(snapshot, &pe));
    }
    CloseHandle(snapshot);
    return false;
}

bool AntiDebug::CloseHandleCheck() {
    HANDLE h = (HANDLE)0x1234;
    // __try {
    //     CloseHandle(h);
    // }
    // __except (EXCEPTION_EXECUTE_HANDLER) {
    //     return GetExceptionCode() == EXCEPTION_INVALID_HANDLE;
    // }
    CloseHandle(h);
    return true;
}

bool AntiDebug::ExceptionCheck() {
    return false;
}

bool AntiDebug::TimingCheck() {
    DWORD start = GetTickCount();
    Sleep(10);
    DWORD end = GetTickCount();
    return (end - start) > 100;
}

bool AntiDebug::HardwareBreakpointCheck() {
    CONTEXT ctx = {0};
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    if (!GetThreadContext(GetCurrentThread(), &ctx)) {
        return false;
    }
    return (ctx.Dr0 != 0) || (ctx.Dr1 != 0) || (ctx.Dr2 != 0) || (ctx.Dr3 != 0);
}

bool AntiDebug::NtSetInformationThread() {
    using NtSetInformationThread_t = NTSTATUS(WINAPI*)(HANDLE, DWORD, PVOID, ULONG);
    HMODULE ntdll = GetModuleHandle("ntdll.dll");
    if (!ntdll) return false;
    
    NtSetInformationThread_t NtSetInformationThread = 
        (NtSetInformationThread_t)GetProcAddress(ntdll, "NtSetInformationThread");
    if (!NtSetInformationThread) return false;
    
    NtSetInformationThread(GetCurrentThread(), 0x11, NULL, 0);
    return true;
}

bool AntiDebug::RunAllChecks() {
    return !IsDebuggerPresent() && !CheckRemoteDebugger();
}
