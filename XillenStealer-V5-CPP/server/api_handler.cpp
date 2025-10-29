#include "api_handler.h"
#include <sstream>
#include <algorithm>
#include <ctime>
#include <iomanip>

std::vector<LogEntry> APIHandler::logs;
int APIHandler::totalInfected = 10896;
int APIHandler::totalPasswords = 550768;
int APIHandler::totalCookies = 543178;
int APIHandler::totalCards = 5473;
int APIHandler::totalWallets = 16332;
int APIHandler::totalApps = 27317;

std::string APIHandler::HandleRequest(const std::string& method, const std::string& path, const std::string& body) {
    if (path == "/api/stats") {
        return GetStats();
    }
    else if (path == "/api/logs") {
        return GetLogs();
    }
    else if (path == "/api/countries") {
        return GetCountries();
    }
    
    return "{\"error\":\"Not found\"}";
}

std::string APIHandler::GetStats() {
    std::ostringstream json;
    json << "{"
         << "\"totalInfected\":" << totalInfected << ","
         << "\"infected24h\":68,"
         << "\"totalPasswords\":" << totalPasswords << ","
         << "\"passwords24h\":3634,"
         << "\"totalCookies\":" << totalCookies << ","
         << "\"cookies24h\":3258,"
         << "\"totalCards\":" << totalCards << ","
         << "\"cards24h\":36,"
         << "\"totalWallets\":" << totalWallets << ","
         << "\"wallets24h\":96,"
         << "\"totalApps\":" << totalApps << ","
         << "\"apps24h\":159,"
         << "\"totalData\":1842,"
         << "\"data24h\":12"
         << "}";
    return json.str();
}

std::string APIHandler::GetLogs(int limit) {
    std::ostringstream json;
    json << "{\"logs\":[";
    
    // Sample data
    if (logs.empty()) {
        LogEntry e1 = {"1", "US", "228.222.129.56", "crypto", 18, 69, 1, 3, 0, "2025-07-02 22:47:47", "Windows", 23.01};
        LogEntry e2 = {"2", "CA", "156.123.45.67", "bank", 45, 120, 3, 1, 2, "2025-07-02 21:30:12", "Windows", 39.94};
        LogEntry e3 = {"3", "DE", "192.168.1.100", "game", 12, 34, 0, 2, 5, "2025-07-02 20:15:33", "Windows", 15.67};
        logs = {e1, e2, e3};
    }
    
    for (size_t i = 0; i < logs.size() && i < limit; i++) {
        if (i > 0) json << ",";
        const auto& log = logs[i];
        json << "{"
             << "\"uuid\":\"" << log.uuid << "\","
             << "\"country\":\"" << log.country << "\","
             << "\"ip\":\"" << log.ip << "\","
             << "\"tag\":\"" << log.tag << "\","
             << "\"passwords\":" << log.passwords << ","
             << "\"cookies\":" << log.cookies << ","
             << "\"cards\":" << log.cards << ","
             << "\"wallets\":" << log.wallets << ","
             << "\"apps\":" << log.apps << ","
             << "\"date\":\"" << log.date << "\","
             << "\"os_version\":\"" << log.os_version << "\","
             << "\"size\":" << log.size
             << "}";
    }
    
    json << "]}";
    return json.str();
}

std::string APIHandler::AddLog(const LogEntry& log) {
    logs.push_back(log);
    totalInfected++;
    totalPasswords += log.passwords;
    totalCookies += log.cookies;
    totalCards += log.cards;
    totalWallets += log.wallets;
    totalApps += log.apps;
    
    return "{\"status\":\"ok\"}";
}

std::string APIHandler::DeleteLog(const std::string& uuid) {
    logs.erase(
        std::remove_if(logs.begin(), logs.end(), [&uuid](const LogEntry& e) { return e.uuid == uuid; }),
        logs.end()
    );
    
    return "{\"status\":\"ok\"}";
}

std::string APIHandler::GetCountries() {
    return "{\"countries\":["
           "{\"code\":\"US\",\"name\":\"United States\",\"count\":3284},"
           "{\"code\":\"CA\",\"name\":\"Canada\",\"count\":2158},"
           "{\"code\":\"BR\",\"name\":\"Brazil\",\"count\":1547},"
           "{\"code\":\"ES\",\"name\":\"Spain\",\"count\":1118},"
           "{\"code\":\"DE\",\"name\":\"Germany\",\"count\":859}"
           "]}";
}

std::string APIHandler::GetTopCountries() {
    return GetCountries();
}
