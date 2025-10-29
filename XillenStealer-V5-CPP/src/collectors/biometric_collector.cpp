#include "biometric_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>

std::string BiometricCollector::CollectBiometricData() {
    std::ostringstream result;
    result << "\n=== BIOMETRIC DATA ===\n";
    
    HKEY hKey;
    LONG ret = RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Authentication\\Biometrics", 0, KEY_READ, &hKey);
    
    if (ret == ERROR_SUCCESS) {
        result << "Windows Hello: ENABLED\n";
        RegCloseKey(hKey);
    } else {
        result << "Windows Hello: NOT FOUND\n";
    }
    
    return result.str();
}
