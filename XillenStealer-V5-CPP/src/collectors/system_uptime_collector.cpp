#include "system_uptime_collector.h"
#include <Windows.h>
#include <iostream>
#include <sstream>

std::string SystemUptimeCollector::GetSystemUptime() {
    std::ostringstream result;
    result << "\n=== SYSTEM UPTIME ===\n";
    
    DWORD tickCount = GetTickCount64();
    DWORD seconds = tickCount / 1000;
    DWORD minutes = seconds / 60;
    DWORD hours = minutes / 60;
    DWORD days = hours / 24;
    
    result << "System uptime: " << days << " days, " 
           << (hours % 24) << " hours, " 
           << (minutes % 60) << " minutes\n";
    
    return result.str();
}
