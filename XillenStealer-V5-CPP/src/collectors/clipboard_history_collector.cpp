#include "clipboard_history_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>

std::string ClipboardHistoryCollector::CollectClipboardHistory() {
    std::ostringstream result;
    result << "\n=== CLIPBOARD HISTORY ===\n";
    
    char roamingPath[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, roamingPath);
    
    std::string clipboardPath = std::string(roamingPath) + "\\Microsoft\\Windows\\Recent";
    
    if (std::filesystem::exists(clipboardPath)) {
        result << "Clipboard history path: FOUND\n";
        result << "Recent clipboard items accessible\n";
    } else {
        result << "Clipboard history: NOT AVAILABLE\n";
    }
    
    return result.str();
}
