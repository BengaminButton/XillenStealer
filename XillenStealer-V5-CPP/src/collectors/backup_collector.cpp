#include "backup_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string BackupCollector::CollectBackups() {
    std::ostringstream result;
    result << "\n=== BACKUP FILES ===\n";
    
    char userprofile[MAX_PATH], documents[MAX_PATH], desktop[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, SHGFP_TYPE_CURRENT, userprofile);
    SHGetFolderPathA(NULL, CSIDL_MYDOCUMENTS, NULL, SHGFP_TYPE_CURRENT, documents);
    SHGetFolderPathA(NULL, CSIDL_DESKTOP, NULL, SHGFP_TYPE_CURRENT, desktop);
    
    std::vector<std::string> backupPatterns = {".bak", ".backup", ".old", ".save", ".tmp"};
    std::vector<std::string> searchPaths = {userprofile, documents, desktop};
    
    int foundCount = 0;
    for (const auto& searchPath : searchPaths) {
        for (const auto& pattern : backupPatterns) {
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(searchPath)) {
                    if (p.is_regular_file() && foundCount < 20) {
                        std::string filename = p.path().extension().string();
                        if (filename == pattern) {
                            try {
                                auto fileSize = std::filesystem::file_size(p.path());
                                if (fileSize < 5 * 1024 * 1024) { // Max 5MB
                                    result << "Backup: " << p.path().filename().string() 
                                           << " (" << fileSize << " bytes)\n";
                                    foundCount++;
                                }
                            } catch (...) {}
                        }
                    }
                }
            } catch (...) {
                // Skip
            }
            if (foundCount >= 20) break;
        }
        if (foundCount >= 20) break;
    }
    
    result << "Total backups found: " << foundCount << "\n";
    
    return result.str();
}
