#ifndef ENTERPRISE_COLLECTOR_H
#define ENTERPRISE_COLLECTOR_H

#include <string>

class EnterpriseCollector {
public:
    static std::string CollectAllEnterprise();
    static std::string CollectSystemInfo();
    static std::string CollectNetworkInfo();
    static std::string CollectInstalledSoftware();
};

#endif
