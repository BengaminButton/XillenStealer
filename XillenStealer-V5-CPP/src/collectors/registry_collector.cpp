#include "registry_collector.h"
#include <Windows.h>
#include <iostream>
#include <sstream>
#include <winreg.h>

std::string RegistryCollector::CollectRegistryData() {
    std::ostringstream result;
    result << "\n=== REGISTRY DATA ===\n";
    
    // Collect Windows product key
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        char productName[255];
        DWORD productNameSize = sizeof(productName);
        
        if (RegQueryValueExA(hKey, "ProductName", NULL, NULL, (LPBYTE)productName, &productNameSize) == ERROR_SUCCESS) {
            result << "Windows: " << productName << "\n";
        }
        
        RegCloseKey(hKey);
    }
    
    return result.str();
}
