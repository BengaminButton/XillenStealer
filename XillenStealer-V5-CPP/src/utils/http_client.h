#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

#include <string>
#include <vector>
#include <cstdint>

class HttpClient {
public:
    static bool SendTelegram(const std::string& botToken, const std::string& chatId, const std::string& message);
    static bool SendDiscord(const std::string& webhook, const std::string& message);
    static bool UploadFile(const std::string& url, const std::vector<uint8_t>& data);
    static std::string EscapeJson(const std::string& str);
};

#endif
