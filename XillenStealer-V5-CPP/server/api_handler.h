#ifndef API_HANDLER_H
#define API_HANDLER_H

#include <string>
#include <map>
#include <vector>

struct LogEntry {
    std::string uuid;
    std::string country;
    std::string ip;
    std::string tag;
    int passwords;
    int cookies;
    int cards;
    int wallets;
    int apps;
    std::string date;
    std::string os_version;
    double size;
};

class APIHandler {
public:
    static std::string HandleRequest(const std::string& method, const std::string& path, const std::string& body);
    
    static std::string GetStats();
    static std::string GetLogs(int limit = 10);
    static std::string AddLog(const LogEntry& log);
    static std::string DeleteLog(const std::string& uuid);
    
    static std::string GetCountries();
    static std::string GetTopCountries();
    
private:
    static std::vector<LogEntry> logs;
    static int totalInfected;
    static int totalPasswords;
    static int totalCookies;
    static int totalCards;
    static int totalWallets;
    static int totalApps;
};

#endif
