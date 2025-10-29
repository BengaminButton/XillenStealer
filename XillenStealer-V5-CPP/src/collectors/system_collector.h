#ifndef SYSTEM_COLLECTOR_H
#define SYSTEM_COLLECTOR_H

#include <string>

class SystemCollector {
public:
    static std::string GetRunningProcesses();
    static std::string GetNetworkConnections();
    static std::string GetInstalledSoftwareExtended();
};

#endif
