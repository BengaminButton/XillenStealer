#include "anti_vm.h"
#include <tlhelp32.h>
#include <cstring>
#include <iphlpapi.h>

bool AntiVM::CheckRegistry() {
    const char* vmKeys[] = {
        "SOFTWARE\\VMware",
        "SOFTWARE\\VirtualBox",
        "HARDWARE\\ACPI\\DSDT\\VBOX_"
    };
    
    for (int i = 0; i < 3; i++) {
        HKEY hKey;
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, vmKeys[i], 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
            RegCloseKey(hKey);
            return true;
        }
    }
    return false;
}

bool AntiVM::CheckMAC() {
    PIP_ADAPTER_INFO adapter = new IP_ADAPTER_INFO[16];
    ULONG bufLen = sizeof(IP_ADAPTER_INFO) * 16;
    
    if (GetAdaptersInfo(adapter, &bufLen) == ERROR_SUCCESS) {
        PIP_ADAPTER_INFO info = adapter;
        while (info) {
            if (memcmp(info->Address, "\x00\x50\x56", 3) == 0) {
                delete[] adapter;
                return true;
            }
            info = info->Next;
        }
    }
    delete[] adapter;
    return false;
}

bool AntiVM::CheckBIOS() {
    HKEY hKey;
    char data[256] = {0};
    DWORD size = sizeof(data);
    
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        if (RegQueryValueExA(hKey, "SystemBiosVersion", NULL, NULL, (LPBYTE)data, &size) == ERROR_SUCCESS) {
            RegCloseKey(hKey);
            return (strstr(data, "VBOX") != NULL || strstr(data, "VMWare") != NULL);
        }
        RegCloseKey(hKey);
    }
    return false;
}

bool AntiVM::CheckCPU() {
    // int cpuInfo[4] = {0};
    // __cpuid(cpuInfo, 1);
    // return (cpuInfo[2] & 0x80000000) != 0;
    return false;
}

bool AntiVM::CheckDrivers() {
    const char* drivers[] = {"VBoxGuest", "vm3dmp", "vmci"};
    for (int i = 0; i < 3; i++) {
        if (GetModuleHandleA(drivers[i])) return true;
    }
    return false;
}

bool AntiVM::CheckProcesses() {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) return false;
    
    PROCESSENTRY32 pe = {sizeof(pe)};
    const char* vmProcesses[] = {"vmtoolsd.exe", "vboxservice.exe", "vmwaretray.exe"};
    
    if (Process32First(snapshot, &pe)) {
        do {
            for (int i = 0; i < 3; i++) {
                if (_stricmp((char*)pe.szExeFile, vmProcesses[i]) == 0) {
                    CloseHandle(snapshot);
                    return true;
                }
            }
        } while (Process32Next(snapshot, &pe));
    }
    CloseHandle(snapshot);
    return false;
}

bool AntiVM::CheckMemory() {
    MEMORYSTATUSEX memInfo = {sizeof(memInfo)};
    GlobalMemoryStatusEx(&memInfo);
    return (memInfo.ullTotalPhys / (1024ULL * 1024ULL)) < 4096;
}

bool AntiVM::RunAllChecks() {
    return !CheckRegistry() && !CheckProcesses();
}
