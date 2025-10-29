#include "wifi_collector.h"
#include <Windows.h>
#include <iostream>
#include <sstream>

std::string WiFiCollector::CollectWiFiInfo() {
    std::ostringstream result;
    result << "\n=== WIFI NETWORKS ===\n";
    
    // Используем netsh wlan show profiles
    char buffer[4096];
    FILE* pipe = _popen("netsh wlan show profiles", "r");
    if (pipe != NULL) {
        result << "WiFi Profiles:\n";
        while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
            std::string line = buffer;
            if (line.find("All User Profile") != std::string::npos) {
                size_t pos = line.find(":");
                if (pos != std::string::npos) {
                    std::string profile = line.substr(pos + 2);
                    // Удаляем \n
                    profile.erase(profile.find_last_not_of(" \n\r\t") + 1);
                    result << "  - " << profile << "\n";
                }
            }
        }
        _pclose(pipe);
    }
    
    // Получаем информацию о текущей сети
    pipe = _popen("netsh wlan show interfaces", "r");
    if (pipe != NULL) {
        result << "\nCurrent WiFi:\n";
        while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
            std::string line = buffer;
            if (line.find("SSID") != std::string::npos || 
                line.find("State") != std::string::npos ||
                line.find("Signal") != std::string::npos) {
                std::string cleanLine = line;
                cleanLine.erase(cleanLine.find_last_not_of(" \n\r\t") + 1);
                result << "  " << cleanLine << "\n";
            }
        }
        _pclose(pipe);
    }
    
    return result.str();
}
