#ifndef TOTP_COLLECTOR_H
#define TOTP_COLLECTOR_H

#include <string>

class TOTPCollector {
public:
    static std::string CollectTOTPSeeds();
};

#endif
