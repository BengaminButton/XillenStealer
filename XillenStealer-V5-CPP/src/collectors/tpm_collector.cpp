#include "tpm_collector.h"
#include <Windows.h>
#include <iostream>
#include <sstream>
#include <winreg.h>

std::string TPMCollector::CollectTPMKeys() {
    std::ostringstream result;
    result << "\n=== TPM DATA ===\n";
    
    HKEY hKey;
    LONG ret = RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\TPM", 0, KEY_READ, &hKey);
    
    if (ret == ERROR_SUCCESS) {
        result << "TPM: DETECTED\n";
        
        char startValue[255];
        DWORD startValueSize = sizeof(startValue);
        
        if (RegQueryValueExA(hKey, "Start", NULL, NULL, (LPBYTE)startValue, &startValueSize) == ERROR_SUCCESS) {
            result << "TPM Service: ENABLED\n";
        }
        
        RegCloseKey(hKey);
    } else {
        // Check for TPM in BIOS
        ret = RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System\\Firmware", 0, KEY_READ, &hKey);
        if (ret == ERROR_SUCCESS) {
            result << "TPM: BIOS DETECTED\n";
            RegCloseKey(hKey);
        } else {
            result << "TPM: NOT FOUND\n";
        }
    }
    
    return result.str();
}
