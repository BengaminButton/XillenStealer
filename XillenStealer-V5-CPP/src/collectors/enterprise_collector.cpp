#include "enterprise_collector.h"
#include <Windows.h>
#include <string>
#include <sstream>
#include <iomanip>
#include <psapi.h>
#include <iphlpapi.h>

#pragma comment(lib, "psapi.lib")
#pragma comment(lib, "iphlpapi.lib")

std::string EnterpriseCollector::CollectAllEnterprise() {
    std::string result;
    
    result += "\n╔═══════════════════════════════════════════════════════════╗\n";
    result += "║   🌐 SYSTEM INFORMATION                                    ║\n";
    result += "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    result += CollectSystemInfo();
    result += "\n";
    result += CollectNetworkInfo();
    result += "\n";
    result += CollectInstalledSoftware();
    
    return result;
}

std::string EnterpriseCollector::CollectSystemInfo() {
    std::ostringstream info;
    
    info << "═══════════════════════════════════════════════════════════\n";
    info << "   📊 SYSTEM INFORMATION                                    \n";
    info << "═══════════════════════════════════════════════════════════\n\n";
    
    OSVERSIONINFOEX osvi;
    ZeroMemory(&osvi, sizeof(OSVERSIONINFOEX));
    osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);
    GetVersionEx((OSVERSIONINFO*)&osvi);
    
    info << "OS Version: Windows " << osvi.dwMajorVersion << "." << osvi.dwMinorVersion << "\n";
    info << "Build Number: " << osvi.dwBuildNumber << "\n";
    
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    
    info << "Processor Architecture: ";
    if (si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64) info << "x64\n";
    else if (si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_INTEL) info << "x86\n";
    else if (si.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_ARM) info << "ARM\n";
    else info << "Unknown\n";
    
    info << "CPU Cores: " << si.dwNumberOfProcessors << "\n";
    
    MEMORYSTATUSEX mem;
    mem.dwLength = sizeof(MEMORYSTATUSEX);
    GlobalMemoryStatusEx(&mem);
    
    info << "Total RAM: " << std::fixed << std::setprecision(2) << (double)mem.ullTotalPhys / (1024 * 1024 * 1024) << " GB\n";
    info << "Available RAM: " << std::fixed << std::setprecision(2) << (double)mem.ullAvailPhys / (1024 * 1024 * 1024) << " GB\n";
    
    char computerName[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD size = sizeof(computerName);
    if (GetComputerNameA(computerName, &size)) {
        info << "Computer Name: " << computerName << "\n";
    }
    
    char userName[UNLEN + 1];
    size = sizeof(userName);
    if (GetUserNameA(userName, &size)) {
        info << "Current User: " << userName << "\n";
    }
    
    TCHAR windowsPath[MAX_PATH];
    if (GetWindowsDirectoryA(windowsPath, MAX_PATH)) {
        info << "Windows Path: " << windowsPath << "\n";
    }
    
    return info.str();
}

std::string EnterpriseCollector::CollectNetworkInfo() {
    std::ostringstream info;
    
    info << "═══════════════════════════════════════════════════════════\n";
    info << "   🌐 NETWORK INFORMATION                                   \n";
    info << "═══════════════════════════════════════════════════════════\n\n";
    
    IP_ADAPTER_INFO adapterInfo[16];
    DWORD dwBufLen = sizeof(adapterInfo);
    DWORD dwStatus = GetAdaptersInfo(adapterInfo, &dwBufLen);
    
    if (dwStatus == ERROR_SUCCESS) {
        PIP_ADAPTER_INFO pAdapterInfo = adapterInfo;
        do {
            if (pAdapterInfo->Type == MIB_IF_TYPE_ETHERNET || pAdapterInfo->Type == IF_TYPE_IEEE80211) {
                info << "Adapter: " << pAdapterInfo->Description << "\n";
                info << "MAC Address: ";
                for (UINT i = 0; i < pAdapterInfo->AddressLength; i++) {
                    info << std::hex << std::setfill('0') << std::setw(2) << (int)pAdapterInfo->Address[i];
                    if (i < pAdapterInfo->AddressLength - 1) info << ":";
                }
                info << std::dec << "\n";
                info << "IP Address: " << pAdapterInfo->IpAddressList.IpAddress.String << "\n";
                info << "Subnet Mask: " << pAdapterInfo->IpAddressList.IpMask.String << "\n";
                info << "Gateway: " << pAdapterInfo->GatewayList.IpAddress.String << "\n";
                info << "DNS: " << pAdapterInfo->DnsServerList.IpAddress.String << "\n";
                info << "\n";
            }
            pAdapterInfo = pAdapterInfo->Next;
        } while (pAdapterInfo);
    }
    
    return info.str();
}

std::string EnterpriseCollector::CollectInstalledSoftware() {
    std::ostringstream info;
    
    info << "═══════════════════════════════════════════════════════════\n";
    info << "   💻 INSTALLED SOFTWARE (Top 20)                          \n";
    info << "═══════════════════════════════════════════════════════════\n\n";
    
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        DWORD index = 0;
        char subKeyName[256];
        DWORD subKeyNameSize;
        
        int count = 0;
        while (RegEnumKeyExA(hKey, index, subKeyName, &(subKeyNameSize = sizeof(subKeyName)), NULL, NULL, NULL, NULL) == ERROR_SUCCESS && count < 20) {
            HKEY hSubKey;
            if (RegOpenKeyExA(hKey, subKeyName, 0, KEY_READ, &hSubKey) == ERROR_SUCCESS) {
                char displayName[256];
                DWORD displayNameSize = sizeof(displayName);
                DWORD type;
                
                if (RegQueryValueExA(hSubKey, "DisplayName", NULL, &type, (LPBYTE)displayName, &displayNameSize) == ERROR_SUCCESS) {
                    info << displayName << "\n";
                    count++;
                }
                
                RegCloseKey(hSubKey);
            }
            index++;
        }
        
        RegCloseKey(hKey);
    }
    
    return info.str();
}
