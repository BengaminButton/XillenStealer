#include "system_collector.h"
#include <Windows.h>
#include <tlhelp32.h>
#include <winreg.h>
#include <iphlpapi.h>
#include <iostream>
#include <sstream>
#include <psapi.h>

#pragma comment(lib, "iphlpapi.lib")

std::string SystemCollector::GetRunningProcesses() {
    std::ostringstream result;
    result << "\n=== RUNNING PROCESSES ===\n";
    
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return result.str();
    }
    
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    
    if (Process32First(hSnapshot, &pe32)) {
        int count = 0;
        do {
            if (count < 30) { // Limit to 30 processes
                result << "PID: " << pe32.th32ProcessID << " - " << pe32.szExeFile << "\n";
                count++;
            }
        } while (Process32Next(hSnapshot, &pe32) && count < 30);
        
        result << "\nTotal processes: " << count << "\n";
    }
    
    CloseHandle(hSnapshot);
    
    return result.str();
}

std::string SystemCollector::GetNetworkConnections() {
    std::ostringstream result;
    result << "\n=== NETWORK CONNECTIONS ===\n";
    
    ULONG ulOutBufLen = sizeof(MIB_TCPTABLE_OWNER_PID);
    PMIB_TCPTABLE_OWNER_PID pTcpTable = (MIB_TCPTABLE_OWNER_PID*)malloc(ulOutBufLen);
    
    if (GetExtendedTcpTable(pTcpTable, &ulOutBufLen, TRUE, AF_INET, TCP_TABLE_OWNER_PID_ALL, 0) == ERROR_INSUFFICIENT_BUFFER) {
        free(pTcpTable);
        pTcpTable = (MIB_TCPTABLE_OWNER_PID*)malloc(ulOutBufLen);
    }
    
    if (pTcpTable != NULL) {
        int count = 0;
        for (DWORD i = 0; i < pTcpTable->dwNumEntries && count < 20; i++) {
            if (pTcpTable->table[i].dwOwningPid != 0) {
                struct in_addr addr;
                addr.S_un.S_addr = pTcpTable->table[i].dwLocalAddr;
                
                result << "PID: " << pTcpTable->table[i].dwOwningPid 
                       << " - Port: " << ntohs((u_short)pTcpTable->table[i].dwLocalPort)
                       << " - State: " << pTcpTable->table[i].dwState << "\n";
                count++;
            }
        }
        
        free(pTcpTable);
        result << "\nActive connections: " << count << "\n";
    }
    
    return result.str();
}

std::string SystemCollector::GetInstalledSoftwareExtended() {
    std::ostringstream result;
    result << "\n=== INSTALLED SOFTWARE (EXTENDED) ===\n";
    
    HKEY hKey;
    LONG ret = RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", 0, KEY_READ, &hKey);
    
    if (ret == ERROR_SUCCESS) {
        DWORD index = 0;
        char subKeyName[255];
        DWORD subKeyNameSize = sizeof(subKeyName);
        
        int count = 0;
        while (RegEnumKeyExA(hKey, index, subKeyName, &subKeyNameSize, NULL, NULL, NULL, NULL) == ERROR_SUCCESS && count < 50) {
            HKEY hSubKey;
            if (RegOpenKeyExA(hKey, subKeyName, 0, KEY_READ, &hSubKey) == ERROR_SUCCESS) {
                char displayName[255];
                DWORD displayNameSize = sizeof(displayName);
                
                if (RegQueryValueExA(hSubKey, "DisplayName", NULL, NULL, (LPBYTE)displayName, &displayNameSize) == ERROR_SUCCESS) {
                    result << displayName << "\n";
                    count++;
                }
                
                RegCloseKey(hSubKey);
            }
            
            subKeyNameSize = sizeof(subKeyName);
            index++;
        }
        
        RegCloseKey(hKey);
        result << "\nTotal installed apps: " << count << "\n";
    }
    
    return result.str();
}
